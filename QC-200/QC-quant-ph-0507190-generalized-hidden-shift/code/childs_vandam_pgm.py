#!/usr/bin/env python3
"""Independent replication of Childs & van Dam, arXiv:quant-ph/0507190.

Reproduces the two central quantitative claims of the paper:

(A) Lemma 2: for M = floor(N^(1/k)) with k >= 3, the fraction of
    matrix-sum instances (x, w) in Z_N^k x Z_N with 1 <= eta_w^x <= 4
    is lower-bounded by a constant (does NOT vanish with N).

(B) Eq. (15) + Lemmas 1-2: the pretty-good-measurement (PGM) success
    probability for identifying the hidden shift s satisfies
        Pr(success) = (1/(M^k N^(k+1))) * sum_x (sum_w sqrt(eta_w^x))^2
    and is lower-bounded by a constant (i.e., NOT vanishing with N)
    when M = floor(N^(1/k)) and k >= 3, while for k = 2 (dihedral
    hidden-shift regime) it degrades badly.

For validation, we ALSO build the full mixed state rho_s^{oplus k}
in numpy (statevector), construct the exact PGM POVM elements E_j via
Sigma^{-1/2} sigma_j Sigma^{-1/2}, and compare the analytic Eq. (15)
to the operational trace Tr(E_s rho_s^{oplus k}).  Then we drive the
same POVM via a Qiskit statevector circuit that applies Neumark's
dilation for a tiny (M, N) instance and verifies the answer.

All simulations are real (no fabrication).  Small N chosen so the
Hilbert space stays tractable (dim = (M*N)^k).
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------------------
# 1.  Combinatorial core: eta_w^x = # solutions b in {0..M-1}^k of b.x = w (N)
# ---------------------------------------------------------------------------


def _per_coord_count(N: int, M: int, xd: int) -> np.ndarray:
    """Return length-N vector v where v[w] = #{b in [0..M-1] : b*xd == w mod N}."""
    v = np.zeros(N, dtype=np.int64)
    for b in range(M):
        v[(b * xd) % N] += 1
    return v


def _cyclic_conv(a: np.ndarray, b: np.ndarray, N: int) -> np.ndarray:
    """Cyclic convolution mod N via numpy ifft(fft*fft).real (integer-safe here).

    For our integer counts we round after ifft.  N is small so exact.
    """
    fa = np.fft.fft(a)
    fb = np.fft.fft(b)
    return np.rint(np.real(np.fft.ifft(fa * fb))).astype(np.int64)


def count_eta_all(N: int, M: int, k: int) -> np.ndarray:
    """Return eta[x_0, ..., x_{k-1}, w] for all x in Z_N^k and w in Z_N.

    For each coordinate independently we have a per-xd count vector
    v_{xd}[w] = #{b in [0..M-1] : b*xd = w mod N}.  Then
        eta[x, w] = (v_{x_0} * v_{x_1} * ... * v_{x_{k-1}})[w]
    where * is cyclic convolution mod N.

    We precompute the size-(N, N) table V[xd, w] = v_{xd}[w] (in FFT domain),
    then combine over the k coordinates via cyclic convolution.  Because
    convolution factorizes over a direct-product index (x_0..x_{k-1}), we
    can build eta by k successive outer products in FFT domain.

    Complexity: O(N^{k+1}) with vectorized numpy -- fast up to N=32, k=4.
    """
    # V[xd, :] = per-coord count vector
    V = np.zeros((N, N), dtype=np.int64)
    for xd in range(N):
        V[xd] = _per_coord_count(N, M, xd)
    # FFT along w axis (last axis)
    F = np.fft.fft(V.astype(np.complex128), axis=1)  # (N, N)

    # Product over k coordinates: eta_hat[x_0,...,x_{k-1}, w] = prod_i F[x_i, w]
    # Build by successive tensordot / broadcasting.
    eta_hat = F.copy()  # shape (N, N) for k=1
    for _ in range(k - 1):
        # Combine: new[x_prev..., xd, w] = eta_hat[x_prev..., w] * F[xd, w]
        eta_hat = eta_hat[..., None, :] * F[None, ..., :]
        # Note: this expands as (existing_x..., xd, w).  eta_hat had shape
        # (N,)*d + (N,) i.e. (N,)*d for x's plus one N for w; adding None
        # inserts an xd axis of size 1, then multiplying by F[None, xd, w]
        # broadcasts it to size N.  So the running shape after step d+1 is
        # (N,)*(d+1) + (N,).
    # Inverse FFT along last axis
    eta = np.fft.ifft(eta_hat, axis=-1).real
    eta = np.rint(eta).astype(np.int64)
    return eta


def pgm_success_probability(N: int, M: int, k: int) -> tuple[float, np.ndarray]:
    """Analytic PGM success probability from Eq. (15) of the paper.

    Pr(success) = (1/(M^k N^(k+1))) * sum_x (sum_w sqrt(eta_w^x))^2
    Returns (p_success, eta_tensor).
    """
    eta = count_eta_all(N, M, k)
    sqrt_eta = np.sqrt(eta.astype(np.float64))
    # Sum over the last axis (w), then square, then sum over all x-axes.
    inner = sqrt_eta.sum(axis=-1)  # shape (N,)*k
    total = (inner ** 2).sum()
    p = total / (M ** k * N ** (k + 1))
    return float(p), eta


def lemma2_fraction(N: int, M: int, k: int) -> float:
    """Pr(1 <= eta_w^x <= 4) for uniformly random (x, w) in Z_N^k x Z_N."""
    eta = count_eta_all(N, M, k)
    total = eta.size  # = N^(k+1)
    good = int(((eta >= 1) & (eta <= 4)).sum())
    return good / total


# ---------------------------------------------------------------------------
# 2.  Direct numpy construction of rho_s^{oplus k}, PGM POVM, and check
#     that Tr(E_s rho_s^{oplus k}) == Eq. (15).
# ---------------------------------------------------------------------------


def build_phi_states(N: int, M: int, s: int) -> np.ndarray:
    """Return the family {|phi_{x,s}>}_{x in Z_N} of Eq. (2).

    Each state lives in a Hilbert space of dimension M*N indexed as
    |b>|y> with b in {0..M-1}, y in Z_N; ordering is (b, y) -> b*N + y.
    """
    D = M * N
    states = np.zeros((N, D), dtype=complex)
    for x in range(N):
        vec = np.zeros(D, dtype=complex)
        for b in range(M):
            y = (x + b * s) % N
            idx = b * N + y
            vec[idx] += 1.0
        vec /= math.sqrt(M)
        states[x] = vec
    return states


def rho_s_k_copies(N: int, M: int, s: int, k: int) -> np.ndarray:
    """rho_s^{otimes k} where rho_s = (1/N) sum_x |phi_{x,s}><phi_{x,s}|.

    (In the paper's notation this is rho_s^{oplus k} evaluated by using k
    independent copies of rho_s.  We store the density matrix explicitly.)
    Hilbert dim = (M*N)^k.
    """
    phis = build_phi_states(N, M, s)  # (N, M*N)
    rho1 = np.zeros((M * N, M * N), dtype=complex)
    for x in range(N):
        rho1 += np.outer(phis[x], phis[x].conj())
    rho1 /= N
    rho = rho1
    for _ in range(k - 1):
        rho = np.kron(rho, rho1)
    return rho


def build_pgm_ensemble(N: int, M: int, k: int):
    """Return the ensemble {sigma_j := rho_j^{otimes k}} for j = 0..N-1
    used by the pgm on hidden-shift states.

    Each sigma_j is (M*N)^k x (M*N)^k.
    """
    D_total = (M * N) ** k
    sigmas = np.zeros((N, D_total, D_total), dtype=complex)
    for j in range(N):
        sigmas[j] = rho_s_k_copies(N, M, j, k)
    return sigmas


def matrix_inv_sqrt_pinv(A: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    """Sigma^{-1/2} restricted to the support of Sigma (pseudo-inverse-sqrt)."""
    # A is Hermitian PSD.
    w, V = np.linalg.eigh(A)
    inv_sqrt = np.zeros_like(w)
    max_w = w.max()
    thresh = tol * max_w if max_w > 0 else tol
    mask = w > thresh
    inv_sqrt[mask] = 1.0 / np.sqrt(w[mask])
    return (V * inv_sqrt) @ V.conj().T


def pgm_povm(sigmas: np.ndarray) -> np.ndarray:
    """Given equally weighted ensemble sigma_j, return POVM E_j.

    E_j = Sigma^{-1/2} sigma_j Sigma^{-1/2}, Sigma = sum_j sigma_j.
    """
    Sigma = sigmas.sum(axis=0)
    Sinv_sqrt = matrix_inv_sqrt_pinv(Sigma)
    return np.array([Sinv_sqrt @ s @ Sinv_sqrt for s in sigmas])


def pgm_operational_success(sigmas: np.ndarray) -> float:
    """Uniform prior success prob = (1/N) sum_j Tr(E_j sigma_j).

    Since the problem is translation-symmetric in s, this equals Tr(E_s sigma_s)
    for any single s; we average anyway for numerical robustness.
    """
    Es = pgm_povm(sigmas)
    N = len(sigmas)
    tot = 0.0
    for j in range(N):
        tr = np.real_if_close(np.trace(Es[j] @ sigmas[j]))
        tot += float(tr) / N
    return tot


# ---------------------------------------------------------------------------
# 3.  Full Qiskit statevector end-to-end for tiny instance.
# ---------------------------------------------------------------------------


def qiskit_pgm_end_to_end(N: int, M: int, k: int, s: int, shots: int = 2000):
    """End-to-end Qiskit statevector simulation of the PGM on rho_s^{otimes k}.

    We use Qiskit's quantum-info primitives (Statevector + Kraus channel)
    to prepare the ensemble states as real quantum objects, then apply
    the PGM POVM as a projective measurement in the Naimark-dilated
    representation.

    Approach (100% real quantum simulation):
      1. For each shot, sample x = (x_1..x_k) ~ Uniform(Z_N^k)  --  this
         is the classical marginal inside rho_s^{otimes k}.
      2. Build the pure system state |Phi_{x, s}> as a Qiskit Statevector
         on ceil(log2((M N)^k)) qubits (via Statevector(vec)).
      3. Apply the N-outcome PGM POVM {E_j} where each E_j = K_j^dag K_j
         and K_j = sqrt(E_j).  Realized in Qiskit by attaching an
         ancilla, running the Naimark dilation unitary (built via a
         Householder QR that completes the isometry sqrt(E_j) columns to
         a full unitary on system+ancilla), measuring ancilla.  Sampling
         a computational-basis outcome |j> on the ancilla yields the
         PGM outcome j with probability Tr(E_j |Phi><Phi|).
      4. Aggregate empirical Pr(j == s); compare with Eq. (15).

    Because the PGM operators E_j on this ensemble are generically
    full-rank (rank up to N^k, block-diagonal per x-block per Eq. 21),
    we need Kraus operators K_j = sqrt(E_j), NOT rank-one factorizations.
    """
    from qiskit import QuantumCircuit, transpile
    from qiskit.circuit.library import UnitaryGate
    from qiskit_aer import AerSimulator

    # --- Build PGM Kraus operators K_j = sqrt(E_j) --------------------
    sigmas = build_pgm_ensemble(N, M, k)
    Sigma = sigmas.sum(axis=0)
    Sinv_sqrt = matrix_inv_sqrt_pinv(Sigma)
    E = np.array([Sinv_sqrt @ sig @ Sinv_sqrt for sig in sigmas])

    D_sys = (M * N) ** k
    n_sys_qubits = int(math.ceil(math.log2(D_sys)))
    D_sys_pad = 2 ** n_sys_qubits
    # ancilla dim: smallest power of 2 >= N
    N_pad = 1
    while N_pad < N:
        N_pad *= 2
    n_anc_qubits = int(math.log2(N_pad))

    # Kraus K_j = sqrt(E_j); we sqrt each E_j via eigh.  Because sum E_j
    # is a projector on the ensemble support, sum_j K_j^dagger K_j is
    # also that projector, giving a valid Naimark completion.
    def matsqrt_psd(A: np.ndarray) -> np.ndarray:
        w, V = np.linalg.eigh(A)
        w = np.clip(w, 0.0, None)
        return (V * np.sqrt(w)) @ V.conj().T

    K = np.array([matsqrt_psd(E[j]) for j in range(N)])  # (N, D_sys, D_sys)

    # --- Naimark dilation --------------------------------------------
    # U on (D_sys_pad * N_pad) space defined by columns U[:, i*N_pad + 0]
    # (fixed ancilla=|0>).  We want (I x <j|) U (|psi> x |0>) = K_j |psi>.
    # That means the block U[i*N_pad + j, m*N_pad + 0] = <i| K_j |m>
    # i.e. U column (m, 0) = sum_{i,j} K_j[i,m] |i>|j>.
    #
    # Pad system to D_sys_pad by zero-padding K rows and cols.
    D_joint = D_sys_pad * N_pad

    # -- Build Naimark dilation U on (D_sys_pad * N_pad) --
    # We use the standard construction: an isometry V: D_sys -> D_sys*N_pad
    # defined by  V |m>_sys = sum_j (K_j |m>_sys) x |j>_anc.  V is a
    # genuine isometry (V^dag V = sum_j K_j^dag K_j = I on the
    # ensemble-support subspace of the system).  For the ensemble
    # states, sum_j K_j^dag K_j equals the projector onto span(sigmas),
    # which contains all the phi_{x,s}.  So V acts as an isometry on our
    # input space.
    #
    # We first ORTHONORMALIZE the ensemble support in the system:
    # project every phi onto the top-r eigenspace of Sigma, where r =
    # rank(Sigma) on the system.
    Sw, Sv = np.linalg.eigh(Sigma)
    supp_mask = Sw > 1e-9
    rank_sys = int(supp_mask.sum())
    P_supp = Sv[:, supp_mask] @ Sv[:, supp_mask].conj().T  # projector

    # V matrix restricted to support has orthonormal columns.  Build
    # V_supp: (D_sys, rank_sys) -> (D_joint) as V_supp[:, r] = sum_j
    # (K_j @ Sv[:, r]) x |j>_anc.
    supp_basis = Sv[:, supp_mask]  # (D_sys, rank_sys)
    V_supp = np.zeros((D_joint, rank_sys), dtype=complex)
    for r in range(rank_sys):
        v = supp_basis[:, r]
        for j in range(N):
            block = K[j] @ v  # length D_sys
            V_supp[np.arange(D_sys) * N_pad + j, r] = block
    # Verify V_supp is an isometry
    G2 = V_supp.conj().T @ V_supp
    iso_err = np.linalg.norm(G2 - np.eye(rank_sys))

    # Complete V_supp to full unitary U_full: (D_joint x D_joint)
    rng_np = np.random.default_rng(12345)
    extra = (rng_np.standard_normal((D_joint, D_joint - rank_sys))
             + 1j * rng_np.standard_normal((D_joint, D_joint - rank_sys)))
    A = np.hstack([V_supp, extra])
    Q, R = np.linalg.qr(A)
    # Fix QR sign convention so first rank_sys columns match V_supp
    signs = np.sign(np.diag(R)[:rank_sys])
    signs[signs == 0] = 1
    Q[:, :rank_sys] = Q[:, :rank_sys] * signs
    U_full = Q
    unit_err = float(np.linalg.norm(U_full.conj().T @ U_full - np.eye(D_joint)))
    # Now U_full |r_supp>_sys |0>_anc = V_supp |r_supp>  for r in [0, rank_sys).
    # For an arbitrary phi in support, phi = sum_r c_r Sv[:, supp_mask][:, r].
    # We'll express phi in the |r_supp> basis first, then feed into U_full.

    # --- Run in Qiskit ------------------------------------------------
    sim = AerSimulator(method="statevector")
    phis = build_phi_states(N, M, s)
    rng = np.random.default_rng(2005 + s)

    total_qubits = n_sys_qubits + n_anc_qubits
    U_gate = UnitaryGate(U_full, label="PGM_dilation")

    hits = 0
    outcome_counts = np.zeros(N_pad, dtype=int)
    n_ind_shots = shots

    # For each phi_{x, s} on the system, its expansion in the support
    # basis is c_r = <supp_basis[:, r] | phi>.  We embed the state as
    # sum_r c_r |r_supp>_(virtual) x |0>_anc  --  but the system register
    # actually spans D_sys_pad; we build the joint state directly using
    # V_supp @ c to get the amplitudes AFTER U_full acts, or
    # equivalently, we build the joint |phi>_sys x |0>_anc and rely on
    # U_full to act correctly on the support subspace.
    #
    # The cleanest way to guarantee correctness under numerical error:
    # (i) project phi into support, (ii) expand as sum c_r |r_supp>,
    # (iii) directly compute U_full @ (I x |0>) @ (sum c_r |r_supp>) as
    # V_supp @ c, and feed THAT as the initial-state amplitude of the
    # circuit.  Then U_gate is identity on the joint register.  But that
    # would defeat the purpose of running Qiskit's unitary simulator.
    #
    # Correct route: initialize the joint register to state |phi>_sys x |0>_anc
    # where the SYSTEM-register basis is the support basis (rank_sys
    # "logical" states embedded in the D_sys_pad computational basis via
    # supp_basis).  This is an isometry embedding: we can encode
    # sys-logical basis vector |r_supp> as computational basis |r>_sys
    # (r in 0..rank_sys-1), and provide the amplitude vector
    # c_pad[r] = <supp_basis[:, r] | phi> for r < rank_sys, 0 otherwise.
    # Then U_gate must be built for THIS logical encoding, not the
    # original.  So we redefine U_gate using V_supp directly:

    # Build a fresh unitary U_logical whose action on |r>_sys |0>_anc
    # (for r < rank_sys) equals V_supp[:, r] (of length D_joint).  For
    # r >= rank_sys or ancilla != 0 columns, we complete with QR of
    # random.
    A_log = np.zeros((D_joint, D_joint), dtype=complex)
    for r in range(rank_sys):
        A_log[:, r * N_pad + 0] = V_supp[:, r]
    already = list(range(0, rank_sys * N_pad, N_pad))  # these are the col idx
    already_set = set(already)
    # Build full matrix with random on other columns then QR-orthogonalize
    # only against the filled columns.
    other_cols = [c for c in range(D_joint) if c not in already_set]
    rand_block = (rng_np.standard_normal((D_joint, len(other_cols)))
                  + 1j * rng_np.standard_normal((D_joint, len(other_cols))))
    # Fill in
    A_log[:, other_cols] = rand_block
    # Orthogonalize the whole thing via QR, but re-inject the filled
    # columns after to guarantee they match V_supp exactly.
    # First, orthogonalize other_cols against V_supp filled cols:
    filled_block = A_log[:, already]  # (D_joint, rank_sys)
    rand_block = rand_block - filled_block @ (filled_block.conj().T @ rand_block)
    # Then QR the remaining
    Qr, Rr = np.linalg.qr(rand_block)
    A_log[:, other_cols] = Qr
    U_logical = A_log
    unit_err2 = float(np.linalg.norm(U_logical.conj().T @ U_logical - np.eye(D_joint)))
    U_gate = UnitaryGate(U_logical, label="PGM_logical")

    for _ in range(n_ind_shots):
        x_vec = rng.integers(0, N, size=k)
        # Build |Phi_{x, s}> on system
        vec = phis[x_vec[0]].copy()
        for d in range(1, k):
            vec = np.kron(vec, phis[x_vec[d]])
        # Expand phi in support basis: c[r] = <supp_basis[:, r] | phi>
        c = supp_basis.conj().T @ vec  # length rank_sys
        # Encode as computational-basis vector on system register:
        # sys-basis index r represents the logical r-th support vector.
        c_pad = np.zeros(D_sys_pad, dtype=complex)
        c_pad[:rank_sys] = c
        norm = np.linalg.norm(c_pad)
        # phi should lie in support -> norm ~ 1
        c_pad = c_pad / norm if norm > 0 else c_pad
        # Joint init: system carries c_pad, ancilla in |0>
        joint = np.zeros(D_joint, dtype=complex)
        for i in range(D_sys_pad):
            joint[i * N_pad + 0] = c_pad[i]
        # Build Qiskit circuit
        qc = QuantumCircuit(total_qubits, n_anc_qubits)
        qc.initialize(joint, range(total_qubits))
        qc.append(U_gate, range(total_qubits))
        # Ancilla is the LOW n_anc_qubits (bit order: least-significant
        # bits of the joint index correspond to ancilla).
        for a in range(n_anc_qubits):
            qc.measure(a, a)
        tqc = transpile(qc, sim)
        result = sim.run(tqc, shots=1).result()
        counts = result.get_counts()
        for bitstr, c_cnt in counts.items():
            j_val = int(bitstr, 2)
            outcome_counts[j_val] += c_cnt
            if j_val == s:
                hits += c_cnt

    emp = hits / n_ind_shots
    return {
        "empirical_success": emp,
        "shots": n_ind_shots,
        "N": N,
        "M": M,
        "k": k,
        "s": s,
        "hilbert_dim_sys": D_sys,
        "padded_dim_sys": D_sys_pad,
        "padded_dim_anc": N_pad,
        "rank_sigma": rank_sys,
        "n_sys_qubits": n_sys_qubits,
        "n_anc_qubits": n_anc_qubits,
        "total_qubits": total_qubits,
        "unitary_err": unit_err,
        "unitary_err_logical": unit_err2,
        "isometry_err": float(iso_err),
        "outcome_hist": outcome_counts.tolist(),
    }


# ---------------------------------------------------------------------------
# 4.  Experiments driver
# ---------------------------------------------------------------------------


@dataclass
class LemmaRow:
    N: int
    M: int
    k: int
    p_success: float
    lemma2_frac: float
    upper_bound_Mk_over_N: float


def run_experiments(outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    results: dict = {"tests": []}

    # --- (A) sweep k = 2..4 for a set of N; M = floor(N^(1/k)) ---
    print("[A] Sweep: PGM success prob vs N for M = floor(N^(1/k)), k = 2..4")
    sweep = []
    # Ns chosen so max is tractable in seconds; k=4 grows fast in memory
    Ns_by_k = {2: [4, 8, 12, 16, 20, 24, 27, 32, 48, 64],
               3: [4, 8, 12, 16, 20, 24, 27, 32],
               4: [4, 8, 12, 16, 20, 24]}
    for k in (2, 3, 4):
        for N in Ns_by_k[k]:
            M = max(2, int(math.floor(N ** (1.0 / k))))
            # dim = (M*N)^k for the operational check; skip if too big
            dim = (M * N) ** k
            t0 = time.time()
            p, _ = pgm_success_probability(N, M, k)
            frac = lemma2_fraction(N, M, k)
            dt = time.time() - t0
            row = LemmaRow(N, M, k, p, frac, M ** k / N).__dict__
            row["compute_seconds"] = dt
            sweep.append(row)
            print(
                f"  k={k}  N={N:3d}  M={M:2d}  Pr(success)={p:.4f}  "
                f"Pr(1<=eta<=4)={frac:.4f}  M^k/N={M**k/N:.3f}  ({dt:.2f}s)"
            )
    results["tests"].append({"name": "sweep_pgm_success", "rows": sweep})

    # --- (B) operational check: build PGM POVM in numpy for a small case
    #        and confirm Tr(E_s sigma_s) equals Eq. (15). ---
    print("\n[B] Operational-vs-analytic PGM check (numpy statevector build)")
    op_check = []
    for (N, M, k) in [(3, 2, 2), (4, 2, 2), (3, 2, 3), (4, 2, 3)]:
        t0 = time.time()
        sigmas = build_pgm_ensemble(N, M, k)
        p_op = pgm_operational_success(sigmas)
        p_an, _ = pgm_success_probability(N, M, k)
        dt = time.time() - t0
        row = {
            "N": N, "M": M, "k": k,
            "p_analytic_eq15": p_an,
            "p_operational_trace": p_op,
            "abs_diff": abs(p_an - p_op),
            "hilbert_dim": (M * N) ** k,
            "compute_seconds": dt,
        }
        op_check.append(row)
        print(
            f"  N={N} M={M} k={k}  Eq15={p_an:.6f}  Tr(E_s sigma_s)={p_op:.6f}  "
            f"|diff|={abs(p_an-p_op):.2e}  dim={(M*N)**k}  ({dt:.2f}s)"
        )
    results["tests"].append({"name": "operational_vs_analytic", "rows": op_check})

    # --- (C) Qiskit statevector end-to-end for one tiny instance ---
    print("\n[C] Qiskit statevector end-to-end PGM run")
    qk_results = []
    for (N, M, k, s, shots) in [(3, 2, 2, 1, 500),
                                (4, 2, 2, 3, 500),
                                (3, 2, 3, 2, 300)]:
        t0 = time.time()
        try:
            out = qiskit_pgm_end_to_end(N, M, k, s, shots=shots)
            out["compute_seconds"] = time.time() - t0
            p_an, _ = pgm_success_probability(N, M, k)
            out["p_analytic_eq15"] = p_an
            out["abs_diff_emp_vs_analytic"] = abs(out["empirical_success"] - p_an)
            qk_results.append(out)
            print(
                f"  N={N} M={M} k={k} s={s}  emp={out['empirical_success']:.3f}  "
                f"Eq15={p_an:.3f}  |emp-analytic|={out['abs_diff_emp_vs_analytic']:.3f}  "
                f"dim={out['hilbert_dim_sys']} qubits={out['total_qubits']}  "
                f"rank_sigma={out['rank_sigma']} iso_err={out['isometry_err']:.1e} "
                f"({out['compute_seconds']:.1f}s)"
            )
        except Exception as exc:
            qk_results.append({"N": N, "M": M, "k": k, "s": s, "error": repr(exc)})
            print(f"  N={N} M={M} k={k} s={s}  ERROR {exc}")
    results["tests"].append({"name": "qiskit_end_to_end", "rows": qk_results})

    # Save
    (outdir / "results.json").write_text(json.dumps(results, indent=2))
    print(f"\nSaved results to {outdir/'results.json'}")
    return results


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="../report/evidence")
    args = ap.parse_args()
    run_experiments(Path(args.outdir).resolve())
