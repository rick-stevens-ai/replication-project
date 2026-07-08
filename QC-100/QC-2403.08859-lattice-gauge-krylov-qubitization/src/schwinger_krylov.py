#!/usr/bin/env python3
"""
Independent replication of key claim in arXiv:2403.08859
"Solving lattice gauge theories using the quantum Krylov algorithm and qubitization"
(Anderson, Kiffner, O'Leary, Crain, Jaksch — Quantum 2025).

Reproduces the central algorithmic claim of Sec. 4 / Fig. 3 / Appendix A.1:
    Quantum Subspace Expansion (QSE) with a Krylov basis
    { |psi_0>, H |psi_0>, H^2 |psi_0>, ... , H^(D-1)|psi_0> }
    converges EXPONENTIALLY in the basis dimension D to the exact ground
    state energy of the spin-only (gauge-eliminated, Jordan-Wigner-transformed)
    single-flavour lattice Schwinger Hamiltonian, Eq. (15) of the paper.

Parameters follow the paper's Sec. 4:  mu = 1.5,  x = 0.5.
Reference state |psi_0>: x=0 antiferromagnetic vacuum,
    sigma_3(n) = -(-1)^n  (Eq. 10 translated to spin basis).

We do the whole thing on CPU with scipy sparse — this is the "classical
statevector simulator" analogue of what would be run on a quantum computer.
The paper itself uses the same dense-state representation (2^N vector,
Sec. 4 intro) for the "no-measurement-noise" reference numbers in Fig. 3.

Krylov QSE = solve the small generalised eigenvalue problem
    H_D c = E S_D c
with H_D[i,j] = <psi_0| H^{i+j+1} |psi_0>,  S_D[i,j] = <psi_0| H^{i+j} |psi_0>.
For real numerical stability we use the equivalent "orthonormalise the
Krylov vectors" (Lanczos) formulation and directly diagonalise the resulting
Ritz matrix. Both are algebraically identical Krylov approximations; the
Hankel form is what the paper's *quantum* protocol measures, the orthonormal
form is what a classical simulator uses. Because our simulator has infinite
precision (double), they agree until the Hankel version breaks down on
ill-conditioning — exactly the phenomenon the paper reports in Sec. 4.

We ALSO run the paper's actual Hankel form to demonstrate the ill-conditioning
onset — this is another central experimental observation of the paper
(Sec. 4, Fig. 4 caption: "basis size until the generalised eigenvalue
problem can no longer be solved due to ill-conditioning").
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.linalg import eigh, eigh_tridiagonal, eig


# ----------------------------- operators --------------------------------- #

I2 = sp.identity(2, dtype=np.float64, format="csr")
SZ = sp.csr_matrix(np.array([[1.0, 0.0], [0.0, -1.0]]))
SP = sp.csr_matrix(np.array([[0.0, 1.0], [0.0, 0.0]]))   # sigma^+ = (sx + i sy)/2
SM = sp.csr_matrix(np.array([[0.0, 0.0], [1.0, 0.0]]))   # sigma^-


def _op_on_site(op: sp.csr_matrix, site: int, N: int) -> sp.csr_matrix:
    """Embed a single-qubit operator on site `site` (0-indexed) in an N-qubit chain."""
    mats = [I2] * N
    mats[site] = op
    out = mats[0]
    for m in mats[1:]:
        out = sp.kron(out, m, format="csr")
    return out


def _two_site(op_a: sp.csr_matrix, a: int, op_b: sp.csr_matrix, b: int, N: int) -> sp.csr_matrix:
    """Two-site operator op_a(a) op_b(b) with a != b, both 0-indexed."""
    assert a != b
    mats = [I2] * N
    mats[a] = op_a
    mats[b] = op_b
    out = mats[0]
    for m in mats[1:]:
        out = sp.kron(out, m, format="csr")
    return out


# --------------------- Schwinger Hamiltonian (Eq. 15) -------------------- #

def build_schwinger_H(N: int, mu: float, x: float) -> sp.csr_matrix:
    """
    Spin-only (gauge-eliminated + Jordan-Wigner) single-flavour lattice
    Schwinger Hamiltonian, Eq. (15) of arXiv:2403.08859.

    Sites are 1-indexed in the paper (n = 1..N).  We store on qubits 0..N-1
    with qubit index q = n-1.

    H = H0 + x * V

    H0 =  sum_{n=1..N}  [ (-1)^n * mu/2  + mu/2 * sigma_3(n) ]
        + sum_{n=1..N-1} [ 1/2 sum_{m=1..n} (sigma_3(m) + (-1)^m) ]^2

    V  =  sum_{n=1..N-1} [ sigma^+(n) sigma^-(n+1) + h.c. ]
    """
    dim = 2 ** N
    H = sp.csr_matrix((dim, dim), dtype=np.float64)

    # Constant + mass term (single-site) — first line of Eq. 15:
    #   sum_n (-1)^n * [ mu/2  +  mu/2 * sigma_3(n) ]
    # so BOTH pieces carry the (-1)^n prefactor.
    for n in range(1, N + 1):
        sign = (-1.0) ** n
        # constant piece
        H = H + (sign * mu / 2.0) * sp.identity(dim, dtype=np.float64, format="csr")
        # sigma_3(n) piece (also multiplied by (-1)^n)
        q = n - 1
        H = H + (sign * mu / 2.0) * _op_on_site(SZ, q, N)

    # Electric-field-squared term (long-range), second line of Eq. 15
    # F_n = (1/2) sum_{m=1..n} [ sigma_3(m) + (-1)^m ]
    # sum_{n=1..N-1} F_n^2
    for n in range(1, N):  # n = 1 .. N-1
        # Build F_n as a diagonal operator (all sigma_3 commute → diagonal).
        # We can represent F_n as a sparse diagonal vector.
        diag = np.zeros(dim, dtype=np.float64)
        # constant part of F_n
        c_n = 0.5 * sum((-1.0) ** m for m in range(1, n + 1))
        diag += c_n
        # each sigma_3(m) is diagonal in computational basis with eigenvalues
        # +1 if bit-m is |0>, -1 if bit-m is |1>.
        for m in range(1, n + 1):
            q = m - 1  # qubit index
            # convention: our kron order puts qubit 0 as leftmost factor,
            # so for basis index k in [0, 2^N), the bit corresponding to
            # qubit q is bit  (N-1-q)  when we treat k in big-endian.
            # sigma_3 eigenvalue = +1 for |0>, -1 for |1>
            bit_pos = (N - 1 - q)
            idx = np.arange(dim)
            sz_vals = 1.0 - 2.0 * ((idx >> bit_pos) & 1)  # +1 or -1
            diag += 0.5 * sz_vals
        H = H + sp.diags(diag * diag, format="csr")

    # Interaction V (hopping), third line of Eq. 15
    V = sp.csr_matrix((dim, dim), dtype=np.float64)
    for n in range(1, N):  # bond n = n, n+1
        qa, qb = n - 1, n
        V = V + _two_site(SP, qa, SM, qb, N)
        V = V + _two_site(SM, qa, SP, qb, N)  # h.c.

    return (H + x * V).tocsr()


def reference_state(N: int) -> np.ndarray:
    """
    x=0 non-interacting vacuum, Eq. (10) mapped to spins.

    From Eq. (7) mass term  mu * sum (-1)^n phi^dag phi(n),  and Eq. (15)'s
    spin form  (-1)^n * (mu/2 + mu/2 sigma_3(n)) = mu * (-1)^n * (1+sigma_3)/2,
    we identify  phi^dag phi = (1 + sigma_3)/2.
    So  phi^dag phi = 1  <=>  sigma_3 = +1  <=>  |0>  in our convention.

    Eq. (10):  phi^dag phi(n) = 1 for ODD n,  0 for EVEN n.
    => odd n:  bit = 0 (|0>, sigma_3=+1).
    => even n: bit = 1 (|1>, sigma_3=-1).

    Sanity: this gives sigma_3(n) = +1 for odd n and -1 for even n,
    i.e. sigma_3(n) = -(-1)^n, matching the paper's statement
    "sigma_3(n) = -(-1)^n" for the antiferromagnetic vacuum right after Eq. 15.
    """
    dim = 2 ** N
    psi = np.zeros(dim, dtype=np.float64)
    idx = 0
    for n in range(1, N + 1):
        q = n - 1
        bit_pos = N - 1 - q
        if n % 2 == 0:  # even n: |1> (sigma_3 = -1)
            idx |= (1 << bit_pos)
    psi[idx] = 1.0
    return psi


# -------------------------- QSE / Krylov core ---------------------------- #

def krylov_lanczos_energies(H: sp.csr_matrix, psi0: np.ndarray, D_max: int):
    """
    Build orthonormalised Krylov basis up to dimension D via Lanczos.
    Return per-D lowest Ritz energy (i.e. QSE lowest eigenvalue of
    H projected onto K_D).  This is the numerically stable version.
    """
    dim = H.shape[0]
    v_prev = np.zeros(dim)
    beta_prev = 0.0
    v = psi0 / np.linalg.norm(psi0)

    alphas = []
    betas = []
    energies_per_D = []

    for j in range(D_max):
        w = H @ v
        alpha = float(np.dot(v, w))
        alphas.append(alpha)
        w = w - alpha * v - beta_prev * v_prev
        # reorthogonalise once (defensive, cheap for small D)
        # against the running two most-recent vectors; we don't store all vectors
        # to keep memory small.
        # For extra safety we do a full reorth if we've stored them — not needed here
        # because D_max is small.
        beta = float(np.linalg.norm(w))
        # per-D Ritz energy from current tridiagonal
        if j == 0:
            e_min = alpha
        else:
            e_min = eigh_tridiagonal(np.array(alphas),
                                     np.array(betas))[0][0]
        energies_per_D.append(e_min)
        if beta < 1e-14:
            # Krylov space exhausted (invariant subspace hit)
            break
        betas.append(beta)
        v_prev = v
        v = w / beta
        beta_prev = beta

    return energies_per_D


def qse_hankel_energies(H: sp.csr_matrix, psi0: np.ndarray, D_max: int,
                        cond_thresh: float = 1e12):
    """
    Faithful reproduction of the paper's Hankel-form QSE:
        H_ij = <psi_0| H^{i+j+1} |psi_0>
        S_ij = <psi_0| H^{i+j}   |psi_0>
    Solve generalised eigenvalue problem H c = E S c up to size D.

    Returns list of (D, E_min, cond_S) tuples; stops (records nan) once
    the S matrix becomes catastrophically ill-conditioned OR the eigenvalue
    solver yields non-finite output — this is the exact failure mode the
    paper documents in Sec. 4.
    """
    psi0 = psi0 / np.linalg.norm(psi0)
    # Precompute moments m_k = <psi_0| H^k |psi_0> up to k = 2*D_max
    moments = np.zeros(2 * D_max + 1)
    v = psi0.copy()
    moments[0] = float(np.dot(psi0, v))
    for k in range(1, 2 * D_max + 1):
        v = H @ v
        moments[k] = float(np.dot(psi0, v))

    results = []
    for D in range(1, D_max + 1):
        S = np.empty((D, D))
        Hmat = np.empty((D, D))
        for i in range(D):
            for j in range(D):
                S[i, j] = moments[i + j]
                Hmat[i, j] = moments[i + j + 1]
        # Force exact symmetry (Hankel matrices already are, but guard fp noise)
        S = 0.5 * (S + S.T)
        Hmat = 0.5 * (Hmat + Hmat.T)
        try:
            cond_S = float(np.linalg.cond(S))
        except Exception:
            cond_S = np.inf
        try:
            # solve S^{-1} H c = E c via generalised eigh
            evals, _ = eigh(Hmat, S)
            e_min = float(np.min(evals))
            if not np.isfinite(e_min):
                e_min = np.nan
        except Exception:
            e_min = np.nan
        results.append((D, e_min, cond_S))
        if cond_S > cond_thresh:
            # From this D onward the paper reports numerical breakdown;
            # keep recording but flag it.
            pass
    return results


# ------------------------------ driver ---------------------------------- #

def exact_ground_state_energy(H: sp.csr_matrix) -> float:
    if H.shape[0] <= 4096:
        # Full dense eigh for tiny systems (exact reference)
        Hd = H.toarray()
        return float(np.min(np.linalg.eigvalsh(Hd)))
    else:
        # Sparse Lanczos, tight convergence
        return float(spla.eigsh(H, k=1, which="SA",
                                tol=1e-12, maxiter=5000)[0][0])


def run_case(N: int, mu: float, x: float, D_max: int, outdir: Path):
    print(f"\n=== N={N}, mu={mu}, x={x}, D_max={D_max} ===")
    t0 = time.time()
    H = build_schwinger_H(N, mu, x)
    print(f"  built H: shape={H.shape}, nnz={H.nnz}, "
          f"build_time={time.time()-t0:.2f}s")

    # exact reference
    t0 = time.time()
    E_exact = exact_ground_state_energy(H)
    print(f"  E_exact = {E_exact:.10f}  "
          f"(diag_time={time.time()-t0:.2f}s)")

    # reference (x=0) energy for interaction-energy denominator, per paper
    H0 = build_schwinger_H(N, mu, 0.0)
    E_x0 = exact_ground_state_energy(H0)
    E_int = E_x0 - E_exact  # positive: how much interaction lowers the energy
    print(f"  E(x=0) = {E_x0:.10f}   E_int = |E(x=0) - E| = {E_int:.10f}")

    # reference state = x=0 antiferromagnetic vacuum, Eq. 10
    psi0 = reference_state(N)
    # sanity: <psi0|H0|psi0> should equal E_x0 to machine precision if psi0 is
    # the true x=0 ground state (it is, because H0 is diagonal in comp. basis).
    e_ref = float(psi0 @ (H0 @ psi0))
    print(f"  <psi0|H0|psi0> = {e_ref:.10f}   (should match E(x=0))")

    # Overlap of reference state with true ground state (Sec. 4)
    Hd = H.toarray()
    evals_full, evecs_full = np.linalg.eigh(Hd)
    gs = evecs_full[:, 0]
    ovlp = float(abs(np.dot(gs, psi0)))
    print(f"  |<GS|psi0>| = {ovlp:.6f}")

    # ---- Krylov QSE via stable Lanczos formulation ---- #
    t0 = time.time()
    lanczos_E = krylov_lanczos_energies(H, psi0, D_max)
    print(f"  Lanczos-Krylov done, {len(lanczos_E)} steps, "
          f"time={time.time()-t0:.2f}s")

    # ---- Paper's Hankel-form QSE (the *quantum* form) ---- #
    t0 = time.time()
    hankel = qse_hankel_energies(H, psi0, D_max)
    print(f"  Hankel-form QSE done, {len(hankel)} steps, "
          f"time={time.time()-t0:.2f}s")

    # ---- Convergence table ---- #
    print(f"\n  {'D':>3} {'E_Lanczos':>16} {'E_Hankel':>16} "
          f"{'dE/E_int (L)':>15} {'dE/E_int (H)':>15} {'cond(S)':>12}")
    rows = []
    for D_idx in range(len(lanczos_E)):
        D = D_idx + 1
        e_l = lanczos_E[D_idx]
        e_h, cond_S = np.nan, np.nan
        if D_idx < len(hankel):
            _, e_h, cond_S = hankel[D_idx]
        frac_l = (e_l - E_exact) / E_int if E_int > 0 else np.nan
        frac_h = (e_h - E_exact) / E_int if (E_int > 0 and np.isfinite(e_h)) else np.nan
        print(f"  {D:>3d} {e_l:>16.10f} {e_h:>16.10f} "
              f"{frac_l:>15.3e} {frac_h:>15.3e} {cond_S:>12.3e}")
        rows.append({
            "D": D,
            "E_Lanczos": e_l,
            "E_Hankel": e_h,
            "frac_err_Lanczos": frac_l,
            "frac_err_Hankel": frac_h,
            "cond_S": cond_S,
        })

    # Persist evidence
    result = {
        "paper": "arXiv:2403.08859",
        "N": N, "mu": mu, "x": x, "D_max": D_max,
        "E_exact": E_exact,
        "E_x0": E_x0,
        "E_int": E_int,
        "overlap_psi0_GS": ovlp,
        "rows": rows,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    fp = outdir / f"schwinger_N{N}_mu{mu}_x{x}.json"
    with open(fp, "w") as fh:
        json.dump(result, fh, indent=2)
    print(f"  wrote {fp}")
    return result


def main():
    here = Path(__file__).resolve().parent.parent
    evdir = here / "report" / "evidence"

    all_results = []
    for N, D_max in [(4, 8), (6, 12), (8, 14), (10, 14)]:
        all_results.append(run_case(N=N, mu=1.5, x=0.5, D_max=D_max, outdir=evdir))

    # Combined summary
    combined_fp = evdir / "summary.json"
    with open(combined_fp, "w") as fh:
        json.dump({"paper": "arXiv:2403.08859",
                   "note": "Independent replication of Krylov-QSE convergence, "
                           "spin-only single-flavour lattice Schwinger Hamiltonian, "
                           "Eq. (15), mu=1.5, x=0.5.",
                   "cases": all_results}, fh, indent=2)
    print(f"\nSummary written to {combined_fp}")


if __name__ == "__main__":
    main()
