#!/usr/bin/env python3
"""
Replication core for Cleve & Wang, arXiv:1612.09512
"Efficient Quantum Algorithms for Simulating Lindblad Evolution"

We do NOT implement the full quantum-circuit LCU compilation (that's the paper's
gate-complexity result and needs block encodings + oblivious amplitude
amplification). We DO implement, at the *linear-algebraic* level, the exact
kernel that the paper's LCU-Taylor construction targets:

  Lindblad master equation
      dρ/dt = -i [H, ρ]  +  sum_j ( L_j ρ L_j†  -  1/2 {L_j† L_j, ρ} )

vectorized (column-stacking, vec(ABC) = (C^T ⊗ A) vec(B)) as a linear ODE on
vec(ρ) with generator

      𝓛_vec = -i (I ⊗ H  -  H^T ⊗ I)
              + sum_j ( L_j* ⊗ L_j  - 1/2 I⊗(L_j† L_j) - 1/2 (L_j† L_j)^T ⊗ I )

whose exact evolution is  vec(ρ(t)) = exp(t 𝓛_vec) vec(ρ(0)).

The paper's algorithm approximates exp(t 𝓛_vec) via a truncated-Taylor / LCU
expansion:   exp(t 𝓛_vec) ≈ Σ_{k=0..K} (t 𝓛_vec)^k / k!
We check the *convergence rate* of this truncation, which is the mathematical
content the paper exploits to get polylog(1/eps) query cost.

Model system (n=2 qubits): a driven qubit + qubit environment style toy.
  H = 0.7 * XI + 0.3 * IZ + 0.2 * XX          (Hermitian, 4x4)
  L = sqrt(gamma) * (|00><01|)                 amplitude damping on qubit-2
"""

from __future__ import annotations
import json, math, os, sys, time
import numpy as np
import scipy.linalg as sla

# ---------- Pauli / operator utilities ---------------------------------------
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def kron(*ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out

# ---------- Model ------------------------------------------------------------
def build_model(gamma: float = 0.9):
    # 2-qubit Hamiltonian (Hermitian, 4x4)
    H = 0.7 * kron(X, I2) + 0.3 * kron(I2, Z) + 0.2 * kron(X, X)
    assert np.allclose(H, H.conj().T), "H must be Hermitian"

    # Amplitude damping on qubit-2:  L = sqrt(gamma) |0><1|_2  ⊗ I_1
    # We take L = sqrt(gamma) * (I ⊗ sigma_-) with sigma_- = |0><1|
    sigma_minus = np.array([[0, 1], [0, 0]], dtype=complex)
    L1 = math.sqrt(gamma) * kron(I2, sigma_minus)

    # A second Lindblad operator: dephasing on qubit-1
    #   L2 = sqrt(0.3) * (Z ⊗ I) / sqrt(2)  gives pure-dephasing rate 0.3
    L2 = math.sqrt(0.3) * kron(Z, I2) / math.sqrt(2)

    Ls = [L1, L2]
    return H, Ls

# ---------- Vectorized Liouvillian ------------------------------------------
def liouvillian(H: np.ndarray, Ls: list[np.ndarray]) -> np.ndarray:
    """
    vec-convention: vec(A) stacks columns of A (numpy default when using .flatten('F')).
    For column-stack vec:  vec(A X B) = (B^T ⊗ A) vec(X).
    So  vec([H, ρ]) = (I ⊗ H - H^T ⊗ I) vec(ρ)
        vec(L ρ L†)  = ((L†)^T ⊗ L) vec(ρ) = (L* ⊗ L) vec(ρ)
        vec(L†L ρ)   = (I ⊗ L†L) vec(ρ)
        vec(ρ L†L)   = ((L†L)^T ⊗ I) vec(ρ)
    """
    d = H.shape[0]
    Id = np.eye(d, dtype=complex)
    Lv = -1j * (np.kron(Id, H) - np.kron(H.T, Id))
    for L in Ls:
        LdL = L.conj().T @ L
        Lv += (np.kron(L.conj(), L)
               - 0.5 * np.kron(Id, LdL)
               - 0.5 * np.kron(LdL.T, Id))
    return Lv

def vec_col(A: np.ndarray) -> np.ndarray:
    """Column-stack vec (Fortran order)."""
    return A.flatten(order='F')

def unvec_col(v: np.ndarray, d: int) -> np.ndarray:
    return v.reshape((d, d), order='F')

# ---------- Exact evolution --------------------------------------------------
def exact_evolve(Lv: np.ndarray, rho0: np.ndarray, t: float) -> np.ndarray:
    d = rho0.shape[0]
    U = sla.expm(t * Lv)                       # gold-standard matrix exponential
    v = U @ vec_col(rho0)
    return unvec_col(v, d)

# ---------- Truncated-Taylor / LCU approximation -----------------------------
def taylor_evolve(Lv: np.ndarray, rho0: np.ndarray, t: float, K: int) -> np.ndarray:
    """
    Approximate exp(t*Lv) by  sum_{k=0..K} (t*Lv)^k / k!.
    This is the mathematical object the paper's LCU-Taylor algorithm
    coherently prepares. We evaluate it directly to test the truncation error.
    """
    d = rho0.shape[0]
    v = vec_col(rho0)
    tLv = t * Lv
    term = np.eye(d * d, dtype=complex)          # (tLv)^0 / 0!
    approx = term.copy()
    for k in range(1, K + 1):
        term = term @ tLv / k                    # (tLv)^k / k!
        approx = approx + term
    v_out = approx @ v
    return unvec_col(v_out, d)

# ---------- Diagnostics ------------------------------------------------------
def frobenius(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b, ord='fro'))

def trace(rho: np.ndarray) -> complex:
    return complex(np.trace(rho))

def is_psd_like(rho: np.ndarray, tol: float = 1e-9) -> tuple[bool, float]:
    # symmetrize numerically
    rho_h = 0.5 * (rho + rho.conj().T)
    eigs = np.linalg.eigvalsh(rho_h)
    return bool(np.min(eigs) > -tol), float(np.min(eigs))

# ---------- Main experiment --------------------------------------------------
def main(out_json: str) -> None:
    np.set_printoptions(precision=4, suppress=True)
    H, Ls = build_model(gamma=0.9)
    d = H.shape[0]
    Lv = liouvillian(H, Ls)

    # Initial state: pure |+>|1>  (has coherence AND excitation to damp)
    plus = np.array([1, 1], dtype=complex) / math.sqrt(2)
    one  = np.array([0, 1], dtype=complex)
    psi0 = np.kron(plus, one)
    rho0 = np.outer(psi0, psi0.conj())
    assert np.isclose(np.trace(rho0), 1.0)

    # ---- (b) exact evolution at 3 t-values ----------------------------------
    t_vals = [0.5, 1.0, 2.0]
    K_vals = [4, 8, 16]

    result = {
        "paper": "arXiv:1612.09512",
        "system": {
            "n_qubits": 2,
            "H_norm_spectral": float(np.linalg.norm(H, ord=2)),
            "L_norms_spectral": [float(np.linalg.norm(L, ord=2)) for L in Ls],
            "num_Lindblad_ops": len(Ls),
            "Liouvillian_spectral_norm": float(np.linalg.norm(Lv, ord=2)),
        },
        "runs": [],
        "trace_check": [],
    }

    # ---- (c,d) LCU-Taylor approximation + Frobenius error -------------------
    for t in t_vals:
        rho_ex = exact_evolve(Lv, rho0, t)
        tr_ex = trace(rho_ex)
        psd_ok, min_eig = is_psd_like(rho_ex)
        result["trace_check"].append({
            "t": t,
            "trace_exact_real": float(tr_ex.real),
            "trace_exact_imag_abs": float(abs(tr_ex.imag)),
            "trace_dev_from_1": float(abs(tr_ex - 1.0)),
            "min_eig_exact": min_eig,
            "psd_ok_exact": psd_ok,
        })
        for K in K_vals:
            rho_lcu = taylor_evolve(Lv, rho0, t, K)
            eps = frobenius(rho_ex, rho_lcu)
            tr_lcu = trace(rho_lcu)
            result["runs"].append({
                "t": t,
                "K": K,
                "frobenius_error": eps,
                "trace_lcu_real": float(tr_lcu.real),
                "trace_lcu_dev_from_1": float(abs(tr_lcu - 1.0)),
            })

    # ---- (e) empirical K = O(log(1/eps)) scaling ----------------------------
    # For each t, sweep K = 1..K_max and record eps(K); check that eps decays
    # faster than any polynomial, i.e. log(eps) is roughly linear in K (Taylor
    # truncation is super-exponential in K for fixed t).
    scaling = []
    for t in t_vals:
        rho_ex = exact_evolve(Lv, rho0, t)
        Ks, errs = [], []
        for K in range(1, 31):
            rho_lcu = taylor_evolve(Lv, rho0, t, K)
            eps = frobenius(rho_ex, rho_lcu)
            Ks.append(K)
            errs.append(eps)
        # Take the linear-in-log-eps regime: strip trailing values <= 1e-14
        Ks_np = np.array(Ks, dtype=float)
        errs_np = np.array(errs, dtype=float)
        mask = errs_np > 1e-13
        if mask.sum() >= 3:
            slope, intercept = np.polyfit(Ks_np[mask], np.log10(errs_np[mask]), 1)
        else:
            slope, intercept = float('nan'), float('nan')
        scaling.append({
            "t": t,
            "Ks": Ks,
            "errs": errs,
            "log10_eps_vs_K_slope": float(slope),
            "log10_eps_vs_K_intercept": float(intercept),
            "interpretation": (
                "eps(K) ~ 10^(slope*K + intercept). Negative slope with |slope|>0.3 "
                "means eps decays super-exponentially in K, i.e. K = O(log(1/eps)) "
                "to reach a target precision. That is the polylog(1/eps) claim, "
                "reduced to the mathematical Taylor-truncation regime."
            ),
        })
    result["K_scaling"] = scaling

    # ---- (f) trace preservation across the trajectory -----------------------
    N_traj = 25
    tmax = 2.0
    traj = []
    for k in range(N_traj + 1):
        tk = tmax * k / N_traj
        rk = exact_evolve(Lv, rho0, tk)
        traj.append({"t": tk,
                     "trace": float(np.trace(rk).real),
                     "trace_dev": float(abs(np.trace(rk) - 1.0))})
    result["trajectory_trace"] = traj

    # ---- Verdict logic ------------------------------------------------------
    good_t_count = 0
    per_t_min_err = {}
    for t in t_vals:
        errs_at_t = [r["frobenius_error"] for r in result["runs"] if r["t"] == t]
        per_t_min_err[str(t)] = min(errs_at_t)
        if min(errs_at_t) < 1e-6:
            good_t_count += 1
    slopes = [s["log10_eps_vs_K_slope"] for s in scaling]
    trace_max_dev = max(abs(x["trace_dev"]) for x in traj)
    convergent_slopes = sum(1 for s in slopes if s < -0.3)
    if (good_t_count == 3 and trace_max_dev < 1e-9 and convergent_slopes == 3):
        verdict = "REPLICATED"
    elif good_t_count >= 1:
        verdict = "PARTIAL"
    else:
        verdict = "SPOT-CHECK"

    result["summary"] = {
        "t_values_tested": t_vals,
        "K_values_tested": K_vals,
        "per_t_min_frobenius_error": per_t_min_err,
        "slopes_log10eps_per_K": slopes,
        "convergent_slopes_count_of_3": convergent_slopes,
        "trajectory_trace_max_dev_from_1": trace_max_dev,
        "num_t_reaching_1e-6": good_t_count,
        "verdict": verdict,
    }

    with open(out_json, "w") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result["summary"], indent=2))

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "results.json")
    if len(sys.argv) > 1:
        out = sys.argv[1]
    main(out)
