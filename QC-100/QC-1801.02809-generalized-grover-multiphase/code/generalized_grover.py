#!/usr/bin/env python3
"""
Independent replication of arXiv:1801.02809 (Byrnes, Forster, Tessler 2018)
"Generalized Grover's algorithm for multiple phase inversion states"

Reproduces the key claim (Fig. 2 of the paper): for the generalized Grover
gate-based iteration with N source states and M target states,

    G = 1 - 2 P_S ,   O = 1 - 2 P_T

where P_S = sum_{n in S} |psi_n><psi_n| and P_T = sum_{n in T} |n><n|,
the naive initial state |psi_n> (Fig 2a) fails to produce clean oscillations
and reaches only low target probability, whereas the constructed initial
state |Psi_n(t=0)>  (Eq. 12, Fig 2c) produces near-sinusoidal Rabi
oscillations that reach probability ~1 in the target subspace at times
proportional to 1/|c_n|.

We run this using Qiskit's Aer statevector simulator, at the same problem
size as Fig 2 of the paper (D=32 to keep to 2^n for a clean Qiskit
register with n=5 qubits; N=M=5 source/target dimensions; orthonormal
random source states).

Outputs:
  data/naive_run.json          -- P_T(k) for naive |psi_1> initial state
  data/constructed_run.json    -- P_T(k) for constructed |Psi_1(t=0)> initial state
  data/standard_grover.json    -- Standard Grover baseline (single-target, single source)
  data/summary.json            -- Peak P_T etc. for the verdict
"""
import json
import os
import sys
import time
import numpy as np
from pathlib import Path

# Qiskit imports (v2.5 API)
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator

RNG_SEED = 20260703
rng = np.random.default_rng(RNG_SEED)

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
DATA.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------
# Build the generalized Grover pieces as explicit D-dim unitaries.
# We construct P_S and P_T on the D-dim Hilbert space and use
# Operator(...) to convert to a Qiskit unitary gate (Aer statevector).
# -----------------------------------------------------------------
def random_orthonormal_source_states(D, N, target_indices, rng):
    """Return an (N, D) matrix whose rows are orthonormal random complex
    vectors in C^D. They are NOT orthogonal to the target subspace (we
    verify hpsi_n|P_T|psi_n> > 0 for each n, per the paper's assumption).
    """
    # Random complex Gaussian
    X = rng.standard_normal((N, D)) + 1j * rng.standard_normal((N, D))
    # Gram-Schmidt (QR) -> orthonormal rows
    Q, _ = np.linalg.qr(X.T)          # Q: (D, N), orthonormal columns
    psi = Q.T                          # (N, D) rows are orthonormal
    # Verify assumption hpsi_n | P_T | psi_n> > 0.
    # P_T |psi_n> = sum_{t in T} <t|psi_n>|t>, so <psi_n|P_T|psi_n> = sum_{t in T} |<t|psi_n>|^2
    for n in range(N):
        w = float(np.sum(np.abs(psi[n, target_indices]) ** 2))
        assert w > 1e-9, f"source state {n} has vanishing overlap with target space"
    return psi


def build_projector(vectors_as_rows):
    """P = sum_k |v_k><v_k| given vectors as rows of a (K, D) matrix."""
    V = np.asarray(vectors_as_rows)
    return V.conj().T @ V


def target_basis_projector(D, target_indices):
    P = np.zeros((D, D), dtype=complex)
    for t in target_indices:
        P[t, t] = 1.0
    return P


def unitary_from_projector(P):
    """U = I - 2 P (reflection about the subspace complement of P).
    P must be Hermitian projector."""
    D = P.shape[0]
    return np.eye(D) - 2.0 * P


def run_grover_iterations(initial_state, U_G, U_O, P_T, k_max):
    """Apply (U_G U_O)^k to initial_state, return P_T probability at each k."""
    U_step = U_G @ U_O
    state = initial_state.astype(complex).copy()
    prob = [float(np.real(state.conj() @ P_T @ state))]
    for k in range(1, k_max + 1):
        state = U_step @ state
        # Renormalize numerically
        state = state / np.linalg.norm(state)
        prob.append(float(np.real(state.conj() @ P_T @ state)))
    return prob


# -----------------------------------------------------------------
# Constructed initial state |Psi_n(t=0)>  from Eq. 12 of the paper.
# We build the C=P_T P_S P_T submatrix in the M-dim target subspace,
# diagonalize it to get |c_n|^2, then form
#    |Psi_n> = sqrt((1+|c_n|)/2) |eps^+_n>  +  sqrt((1-|c_n|)/2) |eps^-_n>
# where
#    |eps^+/-_n> = sqrt((1-/+|c_n|)/2) |eps_n^Tbar>  +/-  sqrt((1+/-|c_n|)/2) |eps_n^T>
# so, algebraically:
#    |Psi_n(0)> = ( 1/sqrt(2) ) ( U_S^{-1}(sign |eps_n^Tbar>)... )
# The cleanest closed-form (see Eq. 12 in the paper) is:
#    |Psi_n(t=0)> = sqrt((1+|c_n|)/2)|eps_n^+> + sqrt((1-|c_n|)/2)|eps_n^->
# which is the initial state that produces clean Rabi oscillation on the
# n-th pair of eigenstates.
# -----------------------------------------------------------------
def construct_initial_state_eq12(psi_sources, D, target_indices):
    """Return initial state |Psi_1(t=0)> (n=1 mode) per Eq. 12 of the paper.

    We construct C = P_T P_S P_T restricted to the target subspace (M x M),
    diagonalize it -> eigenvalues 1 + |c_n|^2 (Eq. 5), so |c_n|^2 = lambda - 1
    with |c_n|^2 in [0,1]; eigenvectors |eps_n^T> live in target subspace.
    Similarly A = Pbar P_S Pbar restricted to Tbar (D-M x D-M) gives
    eigenvalues 1 - |c_n|^2 (Eq. 7), eigenvectors |eps_n^Tbar>.

    Then |eps^+/-_n> follows Eq. 9 and |Psi_n(0)> follows Eq. 12.
    """
    N = psi_sources.shape[0]
    M = len(target_indices)
    tbar_indices = [i for i in range(D) if i not in set(target_indices)]

    P_S = build_projector(psi_sources)
    P_T = target_basis_projector(D, target_indices)
    P_Tbar = np.eye(D) - P_T

    # C = P_T P_S P_T; restrict to target subspace
    C_full = P_T @ P_S @ P_T
    C_sub = C_full[np.ix_(target_indices, target_indices)]   # (M, M)
    # Eigendecomp; eigenvalues are 1+|c_n|^2 (Eq. 5 says lambda_C = 1+|c_n|^2)
    # However Eq. 5 in the paper reads (Lambda_C)_{nn'} = (1+|c_n|^2) delta_{nn'}.
    # In practice the C submatrix P_T P_S P_T is just PTPST viewed in T; its
    # eigenvalues are |c_n|^2 (the *plus PT* on the diagonal of the block form
    # gives the +1 shift). To recover c_n^2 unambiguously we compute directly
    # the overlap block:
    #   PTPST -> take PT|psi_n>-like blocks -> singular values are |c_n|.
    # The cleanest route: SVD of PT (as rows of target basis) applied to psi.
    #   PT * psi_n^T  ==> project each source vector onto target basis
    # is an M x N matrix M_TS with M_TS[t, n] = <t|psi_n>. SVD singular values
    # of M_TS are exactly the |c_n|.
    M_TS = psi_sources[:, target_indices].T   # (M, N)  M_TS[t,n] = <t|psi_n>
    U, s, Vh = np.linalg.svd(M_TS, full_matrices=False)
    # s are the |c_n|; U's columns are |eps_n^T> expressed in the target basis
    # V's columns are |eps_n^S> (source basis).  We take n=1 (index 0).
    c1 = float(s[0])
    eps_T_target_coords = U[:, 0]           # (M,) coefficients in target basis
    # Embed into full D-dim vector
    eps_T = np.zeros(D, dtype=complex)
    for i_t, t in enumerate(target_indices):
        eps_T[t] = eps_T_target_coords[i_t]

    # |eps_n^Tbar>: from A = P_Tbar P_S P_Tbar; we need the eigenvector matching
    # eigenvalue 1 - |c_n|^2. Equivalently, the SVD of M_TbarS = <tbar|psi_n>
    # gives singular values sqrt(1 - |c_n|^2) (since P_S = P_T P_S P_T +
    # P_Tbar P_S P_T + h.c. + P_Tbar P_S P_Tbar and columns of psi are unit norm).
    # More directly: PT_bar psi_n gives the Tbar-component of each source; its
    # SVD gives sqrt(1-|c_n|^2) as singular values.
    M_TbarS = psi_sources[:, tbar_indices].T  # (D-M, N)
    Ub, sb, Vhb = np.linalg.svd(M_TbarS, full_matrices=False)
    # Match to the SAME source-side eigenvector V[:,0] (largest c_n).
    # By construction of the block SVD structure, Ub's columns are ordered by
    # descending sqrt(1-|c_n|^2), i.e. ASCENDING |c_n|. To pair with c1 =
    # largest |c_n|, we grab the LAST column of Ub (smallest sing. value).
    # But that assumes matching indexing; to be safe we recompute Tbar
    # eigenvector directly from source-space eigenvector V[:,0]:
    #     |eps_n^Tbar> propto P_Tbar |eps_n^S>
    #     |eps_n^S> = sum_k Vh[0, k] |psi_k>
    eps_S_source_coords = Vh.conj()[:, 0]   # (N,) coefficients in source basis
    # Reconstruct |eps_n^S> in full D-dim
    eps_S = eps_S_source_coords @ psi_sources    # (D,)
    # |eps_n^Tbar> = normalize( P_Tbar |eps_n^S> )
    eps_Tbar_unnorm = P_Tbar @ eps_S
    norm_Tbar = np.linalg.norm(eps_Tbar_unnorm)
    if norm_Tbar < 1e-12:
        # Degenerate: c_n = 1 case, source lies entirely in target => skip
        eps_Tbar = np.zeros(D, dtype=complex)
    else:
        eps_Tbar = eps_Tbar_unnorm / norm_Tbar

    # Eq. 9:  |eps^+/-_n> = sqrt((1 -/+ |c_n|)/2) |eps_n^Tbar> +/- sqrt((1 +/- |c_n|)/2) |eps_n^T>
    #   |eps^+_n> = sqrt((1-|c_n|)/2)|eps_n^Tbar> + sqrt((1+|c_n|)/2)|eps_n^T>
    #   |eps^-_n> = sqrt((1+|c_n|)/2)|eps_n^Tbar> - sqrt((1-|c_n|)/2)|eps_n^T>
    a_plus_Tbar = np.sqrt((1 - c1) / 2.0)
    a_plus_T    = np.sqrt((1 + c1) / 2.0)
    a_minus_Tbar = np.sqrt((1 + c1) / 2.0)
    a_minus_T   = np.sqrt((1 - c1) / 2.0)
    eps_plus  = a_plus_Tbar  * eps_Tbar + a_plus_T  * eps_T
    eps_minus = a_minus_Tbar * eps_Tbar - a_minus_T * eps_T

    # Eq. 12:  |Psi_n(t=0)> = sqrt((1+|c_n|)/2)|eps_n^+> + sqrt((1-|c_n|)/2)|eps_n^->
    b_plus  = np.sqrt((1 + c1) / 2.0)
    b_minus = np.sqrt((1 - c1) / 2.0)
    Psi_n = b_plus * eps_plus + b_minus * eps_minus
    Psi_n = Psi_n / np.linalg.norm(Psi_n)
    return Psi_n, c1


# -----------------------------------------------------------------
# Standard single-target Grover baseline (n=5 qubits, D=32, single marked)
# using Qiskit's Aer statevector simulator to explicitly demonstrate
# that we can drive a REAL Qiskit gate-level circuit.
# -----------------------------------------------------------------
def standard_grover_qiskit(n_qubits, marked_index, k_iter):
    """Run standard Grover on Aer statevector; return P(marked) after each k."""
    from qiskit.circuit.library import PhaseOracle  # not needed
    D = 2 ** n_qubits
    # Diffusion: 2|+><+| - I  =  H^n (2|0><0| - I) H^n
    # Oracle for single marked: flip phase of |marked>.
    # We build both as full D-dim unitaries and stitch into a Qiskit circuit
    # via Operator, then run with AerSimulator statevector method.
    Pmark = np.zeros((D, D), dtype=complex)
    Pmark[marked_index, marked_index] = 1.0
    U_oracle = np.eye(D) - 2.0 * Pmark
    plus = np.ones(D, dtype=complex) / np.sqrt(D)
    Pplus = np.outer(plus, plus.conj())
    U_diff = 2.0 * Pplus - np.eye(D)   # = -(I - 2|+><+|), equivalent up to global phase

    sim = AerSimulator(method="statevector")
    probs = []
    # k=0 baseline
    qc0 = QuantumCircuit(n_qubits)
    qc0.h(range(n_qubits))
    qc0.save_statevector()
    result0 = sim.run(qc0).result()
    sv0 = np.asarray(result0.get_statevector(qc0))
    probs.append(float(np.abs(sv0[marked_index]) ** 2))

    for k in range(1, k_iter + 1):
        qc = QuantumCircuit(n_qubits)
        qc.h(range(n_qubits))
        # Compose oracle+diffusion as one D-dim Operator per iteration
        # (avoids re-transpiling large Operators k times)
        step_op = Operator(U_diff @ U_oracle)
        for _ in range(k):
            qc.append(step_op, range(n_qubits))
        qc.save_statevector()
        res = sim.run(qc).result()
        sv = np.asarray(res.get_statevector(qc))
        probs.append(float(np.abs(sv[marked_index]) ** 2))
    return probs


# -----------------------------------------------------------------
# Main experiment.
# -----------------------------------------------------------------
def main():
    n_qubits = 5
    D = 2 ** n_qubits              # 32
    N = 5                           # source dim
    M = 5                           # target dim
    k_max = 40

    # Deterministic target indices (first M basis states)
    target_indices = list(range(M))

    # Build random orthonormal source states
    psi = random_orthonormal_source_states(D, N, target_indices, rng)

    # Build projectors & unitaries on the D-dim space
    P_S = build_projector(psi)
    P_T = target_basis_projector(D, target_indices)
    U_G = unitary_from_projector(P_S)      # 1 - 2 P_S
    U_O = unitary_from_projector(P_T)      # 1 - 2 P_T

    # Sanity checks: U_G, U_O are unitary
    assert np.allclose(U_G @ U_G.conj().T, np.eye(D), atol=1e-9), "U_G not unitary"
    assert np.allclose(U_O @ U_O.conj().T, np.eye(D), atol=1e-9), "U_O not unitary"

    # --- Naive initial state = |psi_1>  (Fig 2a-like, but for gate iter)
    psi1 = psi[0]
    naive_probs = run_grover_iterations(psi1, U_G, U_O, P_T, k_max)

    # --- Constructed initial state Eq. 12
    Psi_init, c1 = construct_initial_state_eq12(psi, D, target_indices)
    constructed_probs = run_grover_iterations(Psi_init, U_G, U_O, P_T, k_max)

    # --- Also verify with a Qiskit circuit for the constructed state:
    # We prepare Psi_init on n_qubits via Qiskit's `initialize` and apply the
    # gate-based iteration by embedding U_G, U_O as full n-qubit Operators.
    sim = AerSimulator(method="statevector")
    qiskit_constructed_probs = []
    qc = QuantumCircuit(n_qubits)
    qc.initialize(Psi_init.tolist(), range(n_qubits))
    qc.save_statevector(label="sv0")
    step_op = Operator(U_G @ U_O)
    # We'll run for each k separately so we get P_T probability curve.
    for k in range(k_max + 1):
        qck = QuantumCircuit(n_qubits)
        qck.initialize(Psi_init.tolist(), range(n_qubits))
        for _ in range(k):
            qck.append(step_op, range(n_qubits))
        qck.save_statevector()
        res = sim.run(qck).result()
        sv = np.asarray(res.get_statevector(qck))
        p_T = float(np.real(sv.conj() @ P_T @ sv))
        qiskit_constructed_probs.append(p_T)

    # --- Standard Grover baseline (single marked, D=32)
    std_probs = standard_grover_qiskit(n_qubits, marked_index=0, k_iter=k_max)

    # --- Peak values
    peak_naive = float(max(naive_probs))
    k_naive_peak = int(np.argmax(naive_probs))
    peak_constructed = float(max(constructed_probs))
    k_constructed_peak = int(np.argmax(constructed_probs))
    peak_qiskit = float(max(qiskit_constructed_probs))
    k_qiskit_peak = int(np.argmax(qiskit_constructed_probs))
    peak_std = float(max(std_probs))
    k_std_peak = int(np.argmax(std_probs))

    # Save
    def dump(name, obj):
        p = DATA / name
        p.write_text(json.dumps(obj, indent=2))
        print(f"wrote {p}")

    dump("naive_run.json", {
        "description": "Generalized Grover gate iteration, naive init |psi_1>",
        "n_qubits": n_qubits, "D": D, "N": N, "M": M,
        "target_indices": target_indices,
        "rng_seed": RNG_SEED,
        "k_range": list(range(k_max + 1)),
        "P_T_k": naive_probs,
        "peak_P_T": peak_naive, "k_peak": k_naive_peak,
    })
    dump("constructed_run.json", {
        "description": "Generalized Grover gate iteration, Eq.12 init |Psi_1(t=0)>",
        "n_qubits": n_qubits, "D": D, "N": N, "M": M,
        "target_indices": target_indices,
        "rng_seed": RNG_SEED,
        "c1": c1,
        "k_range": list(range(k_max + 1)),
        "P_T_k": constructed_probs,
        "peak_P_T": peak_constructed, "k_peak": k_constructed_peak,
        "qiskit_P_T_k": qiskit_constructed_probs,
        "qiskit_peak_P_T": peak_qiskit, "qiskit_k_peak": k_qiskit_peak,
    })
    dump("standard_grover.json", {
        "description": "Standard Grover, single marked, run in Qiskit Aer statevector",
        "n_qubits": n_qubits, "D": D, "marked_index": 0,
        "k_range": list(range(k_max + 1)),
        "P_T_k": std_probs,
        "peak_P_T": peak_std, "k_peak": k_std_peak,
    })
    dump("summary.json", {
        "paper": "arXiv:1801.02809 (Byrnes, Forster, Tessler 2018)",
        "setup": {
            "n_qubits": n_qubits, "D": D, "N": N, "M": M,
            "target_indices": target_indices,
            "rng_seed": RNG_SEED,
            "qiskit_version_expected": "2.5.x",
        },
        "results": {
            "peak_P_T_naive_init": peak_naive,
            "k_peak_naive": k_naive_peak,
            "peak_P_T_constructed_init_numpy": peak_constructed,
            "k_peak_constructed_numpy": k_constructed_peak,
            "peak_P_T_constructed_init_qiskit": peak_qiskit,
            "k_peak_constructed_qiskit": k_qiskit_peak,
            "peak_P_T_standard_grover_single_target": peak_std,
            "k_peak_standard_grover": k_std_peak,
            "c1_largest_singular_value_of_PT_psi": c1,
        },
        "paper_claim_check": {
            "claim_C1": "Constructed initial state (Eq.12) produces clean Rabi oscillations "
                        "reaching probability ~1 in target subspace; naive init |psi_n> does not.",
            "verdict_C1_pass": bool(peak_constructed > 0.90 and peak_naive < 0.60),
            "claim_C2": "Numpy analytic construction agrees with Qiskit Aer statevector "
                        "gate-based iteration.",
            "verdict_C2_pass": bool(abs(peak_constructed - peak_qiskit) < 1e-6),
            "claim_C3": "Standard single-target Grover on Qiskit produces expected "
                        "high success probability at k ~ (pi/4) sqrt(D).",
            "verdict_C3_pass": bool(peak_std > 0.95),
        }
    })
    print("--- SUMMARY ---")
    print(json.dumps({
        "peak_P_T_naive_init": peak_naive,
        "peak_P_T_constructed_init_numpy": peak_constructed,
        "peak_P_T_constructed_init_qiskit": peak_qiskit,
        "peak_P_T_standard_grover_single_target": peak_std,
        "k_peaks": [k_naive_peak, k_constructed_peak, k_qiskit_peak, k_std_peak],
        "c1": c1,
    }, indent=2))


if __name__ == "__main__":
    main()
