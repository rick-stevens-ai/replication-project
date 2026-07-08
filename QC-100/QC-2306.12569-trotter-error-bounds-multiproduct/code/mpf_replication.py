#!/usr/bin/env python3
"""
Independent replication of core numerical claim from arXiv:2306.12569
(Zhuk, Robertson, Bravyi — "Trotter error bounds and dynamic multi-product formulas
for Hamiltonian simulation").

We reproduce the setup of Section V (numerical experiments):
  - Hamiltonian: Childs–Maslov spin chain
      H = sum_{j=0..n-2} (X_j X_{j+1} + Y_j Y_{j+1} + Z_j Z_{j+1})
          + sum_{j=0..n-1} h_j Z_j,      h_j ~ U(-1, 1)
  - Initial state: |psi_in> = |1010...10> (Néel-type)
  - Base product formula: second-order S_2 defined via the 5-factor split
        F1 = F5 = (1/2) * sum_{odd j} (XX+YY+ZZ)
        F2 = F4 = (1/2) * sum_j h_j Z_j
        F3 = sum_{even j} (XX+YY+ZZ)
        S_2(t) = exp(-i t F5) exp(-i t F4) exp(-i t F3) exp(-i t F2) exp(-i t F1)
  - rho_k(t) := S_2(t/k)^k |psi_in><psi_in| S_2(t/k)^{-k}
  - Multi-product formula (MPF), p=2 case, (k1,k2,k3) = lambda * (4, 13, 17),
      coefficients (c1,c2,c3) = (0.016088, -1.794934, 2.778846).
      mu(t) = c1 rho_{k1}(t) + c2 rho_{k2}(t) + c3 rho_{k3}(t).

We compute:
  A. Trotter error   E_Trot(k) = || rho(t) - rho_k(t) ||_1
  B. MPF error       E_MPF     = || rho(t) - mu(t)   ||_1
  C. Compare to fitting ansatze from the paper:
        eps'_fit = 0.6 * n * t^3 / k^2                  (Trotter, Eq. 32)
        eps_fit  = 0.06 * n^2 * t^6 * sum_i |c_i|/k_i^4 (MPF, Eq. 31)

We keep instance small (n=3..4 qubits, t=1.0, lambda=1..3) so it finishes
in seconds and uses full statevector; the paper's own figures use n up to 14.
"""

import json, os, sys, time
import numpy as np
from qiskit.quantum_info import Operator, Statevector, SparsePauliOp
from qiskit.circuit import QuantumCircuit
from scipy.linalg import expm

# ------------------------- Hamiltonian construction --------------------------

def hamiltonian_terms(n, h):
    """Return (H_full, F_list) as dense numpy arrays.
    F_list = [F1, F2, F3, F4, F5]."""
    # Build each F using SparsePauliOp for clarity.
    # F1 = F5 = (1/2) * sum_{odd j} (X_j X_{j+1} + Y_j Y_{j+1} + Z_j Z_{j+1})
    # F3       =         sum_{even j} (X_j X_{j+1} + Y_j Y_{j+1} + Z_j Z_{j+1})
    # F2 = F4  = (1/2) * sum_j h_j Z_j
    def pair_terms(js, prefactor):
        labels = []
        coeffs = []
        for j in js:
            for P in ('X', 'Y', 'Z'):
                lab = ['I'] * n
                lab[j] = P
                lab[j+1] = P
                # Qiskit label is little-endian (index 0 rightmost) — SparsePauliOp
                # accepts a string where char index 0 is qubit n-1. Convert:
                labels.append(''.join(reversed(lab)))
                coeffs.append(prefactor)
        return SparsePauliOp(labels, coeffs) if labels else SparsePauliOp(['I'*n], [0.0])

    def z_field(prefactor):
        labels = []
        coeffs = []
        for j in range(n):
            lab = ['I'] * n
            lab[j] = 'Z'
            labels.append(''.join(reversed(lab)))
            coeffs.append(prefactor * h[j])
        return SparsePauliOp(labels, coeffs)

    odd_js  = [j for j in range(n-1) if j % 2 == 1]
    even_js = [j for j in range(n-1) if j % 2 == 0]

    F1 = pair_terms(odd_js, 0.5)
    F5 = pair_terms(odd_js, 0.5)
    F3 = pair_terms(even_js, 1.0)
    F2 = z_field(0.5)
    F4 = z_field(0.5)

    # Total H = sum_all_pairs (XX+YY+ZZ) + sum_j h_j Z_j
    #        = 2 F1 + F3 + 2 F2 = F1+F5 + F3 + F2+F4
    H_full = (F1 + F2 + F3 + F4 + F5)

    return H_full.to_matrix(), [F.to_matrix() for F in (F1, F2, F3, F4, F5)]

# ------------------------- Trotter S_2 -------------------------------

def s2_step(F_mats, dt):
    """Return the S_2(dt) operator as a dense unitary matrix."""
    U = np.eye(F_mats[0].shape[0], dtype=complex)
    # S_2(t) = exp(-i t F5) exp(-i t F4) exp(-i t F3) exp(-i t F2) exp(-i t F1)
    for F in reversed(F_mats):  # apply F1 first (rightmost) up through F5
        U = expm(-1j * dt * F) @ U
    return U

def rho_k(F_mats, t, k, psi_in):
    """Density matrix from k Trotter steps of S_2(t/k)."""
    U_step = s2_step(F_mats, t / k)
    U_full = np.linalg.matrix_power(U_step, k)
    psi = U_full @ psi_in
    return np.outer(psi, psi.conj())

def rho_exact(H, t, psi_in):
    U = expm(-1j * t * H)
    psi = U @ psi_in
    return np.outer(psi, psi.conj())

def trace_norm(A):
    """||A||_1 = sum of singular values."""
    return float(np.sum(np.linalg.svd(A, compute_uv=False)))

# ------------------------- MPF ------------------------------------------

def mpf_state(F_mats, t, ks, cs, psi_in):
    """mu(t) = sum_i c_i rho_{k_i}(t) as a Hermitian (not necessarily PSD) matrix."""
    dim = psi_in.shape[0]
    mu = np.zeros((dim, dim), dtype=complex)
    for ci, ki in zip(cs, ks):
        mu = mu + ci * rho_k(F_mats, t, ki, psi_in)
    return mu

# ------------------------- Experiment ------------------------------------

def neel_state(n):
    """|1010...10> where qubit 0 is the leftmost '1'."""
    idx = 0
    for j in range(n):
        bit = 1 if (j % 2 == 0) else 0
        idx += bit << j  # little-endian: qubit j is bit j
    psi = np.zeros(2**n, dtype=complex)
    psi[idx] = 1.0
    return psi

def run_experiment(n, t, lambdas, seed=1):
    rng = np.random.default_rng(seed)
    h = rng.uniform(-1.0, 1.0, size=n)

    H_full, F_mats = hamiltonian_terms(n, h)
    psi_in = neel_state(n)

    rho_ex = rho_exact(H_full, t, psi_in)

    # MPF coefficients from the paper (Eq. below Eq. 30):
    cs = np.array([0.016088, -1.794934, 2.778846])
    base_ks = np.array([4, 13, 17])

    results = {
        "n": n, "t": t, "seed": seed,
        "h_field": h.tolist(),
        "H_norm_2": float(np.linalg.norm(H_full, ord=2)),
        "mpf_coeffs": cs.tolist(),
        "mpf_base_ks": base_ks.tolist(),
        "lambdas": [],
    }

    for lam in lambdas:
        ks = base_ks * lam

        # Compute individual Trotter errors for each k
        trot_errs = {}
        for k in ks:
            rk = rho_k(F_mats, t, k, psi_in)
            trot_errs[int(k)] = trace_norm(rho_ex - rk)

        # MPF error
        mu = mpf_state(F_mats, t, ks, cs, psi_in)
        # trace-preservation sanity check (should be sum c_i = 1)
        trace_mu = float(np.real(np.trace(mu)))
        mpf_err = trace_norm(rho_ex - mu)

        # Best single-Trotter error at the same maximum k
        k_max = int(ks[-1])
        best_trot_err = trot_errs[k_max]

        # Paper fitting ansatze
        eps_trot_fit = 0.6 * n * (t**3) / (k_max**2)
        eps_mpf_fit  = 0.06 * (n**2) * (t**6) * float(np.sum(np.abs(cs) / (ks**4)))

        entry = {
            "lambda": int(lam),
            "ks": [int(x) for x in ks],
            "k_max": k_max,
            "trotter_errors_per_k": {str(k): v for k, v in trot_errs.items()},
            "best_single_trotter_err_at_kmax": best_trot_err,
            "mpf_err": mpf_err,
            "mpf_trace": trace_mu,
            "ratio_trot_over_mpf": best_trot_err / mpf_err if mpf_err > 0 else float('inf'),
            "eps_trot_fit_paper_Eq32": eps_trot_fit,
            "eps_mpf_fit_paper_Eq31":  eps_mpf_fit,
        }
        results["lambdas"].append(entry)
        print(f"[n={n}, t={t}, lambda={lam}]  k_max={k_max}  "
              f"best_trot={best_trot_err:.3e}  mpf={mpf_err:.3e}  "
              f"ratio={entry['ratio_trot_over_mpf']:.2f}x  "
              f"fit_trot={eps_trot_fit:.3e}  fit_mpf={eps_mpf_fit:.3e}", flush=True)

    return results


def scaling_experiment(n, t_values, seed=1):
    """Test Trotter error scaling with k (should be ~1/k^2 for S_2)."""
    rng = np.random.default_rng(seed)
    h = rng.uniform(-1.0, 1.0, size=n)
    H_full, F_mats = hamiltonian_terms(n, h)
    psi_in = neel_state(n)

    out = {"n": n, "seed": seed, "h_field": h.tolist(), "t_scan": []}
    for t in t_values:
        rho_ex = rho_exact(H_full, t, psi_in)
        ks = [2, 4, 8, 16, 32, 64]
        errs = {}
        for k in ks:
            rk = rho_k(F_mats, t, k, psi_in)
            errs[k] = trace_norm(rho_ex - rk)
        # Fit log(err) = a + b log(k) using the last 4 (large-k asymptotic regime)
        k_arr = np.array(ks[-4:], dtype=float)
        e_arr = np.array([errs[k] for k in ks[-4:]], dtype=float)
        slope, intercept = np.polyfit(np.log(k_arr), np.log(e_arr), 1)
        out["t_scan"].append({
            "t": t,
            "errors_by_k": {str(k): errs[k] for k in ks},
            "fitted_slope_log_err_vs_log_k_large_k": float(slope),
            "expected_slope_for_S2": -2.0,
        })
        print(f"[scaling n={n} t={t}] slope={slope:.3f} (expect ~-2)  errs="
              f"{[f'{errs[k]:.2e}' for k in ks]}", flush=True)
    return out


if __name__ == "__main__":
    outdir = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.abspath(os.path.join(outdir, "..", "report", "evidence"))
    os.makedirs(outdir, exist_ok=True)

    t0 = time.time()

    # ---- Main MPF replication: n = 3 and n = 4, t = 1.0, lambda = 1, 2, 3 ----
    all_results = {"paper": "arXiv:2306.12569", "sections": {}}

    for n in (3, 4):
        r = run_experiment(n=n, t=1.0, lambdas=[1, 2, 3], seed=1)
        all_results["sections"][f"MPF_n{n}_t1.0"] = r

    # ---- Trotter S_2 scaling check ----
    for n in (3, 4):
        r = scaling_experiment(n=n, t_values=[0.5, 1.0])
        all_results["sections"][f"Scaling_n{n}"] = r

    all_results["runtime_seconds"] = time.time() - t0

    out_path = os.path.join(outdir, "mpf_results.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nWrote {out_path}")
    print(f"Runtime: {all_results['runtime_seconds']:.2f}s")
