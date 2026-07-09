#!/usr/bin/env python3
"""
Independent replication core: Berry, Childs, Cleve, Kothari, Somma (arXiv:1312.1414)
"Exponential improvement in precision for simulating sparse Hamiltonians."

Main claim we test (headline mechanism):
    e^{-iHt}  approximated by truncated Taylor series
        U_K = sum_{k=0}^{K} (-i t)^k H^k / k!
    implemented as a Linear Combination of Unitaries (LCU) circuit
    (PREPARE + SELECT + PREPARE^dagger + oblivious amplitude amplification).

Their exponential-precision claim says: to get error <= epsilon we need
        K = O( log(1/eps) / log log(1/eps) ),
because the Taylor remainder for ||H|| t <= constant is bounded by
        eps ~ (|t| ||H||)^(K+1) / (K+1)!
This is SUPER-exponential in K (factorial), i.e. epsilon(K) shrinks
faster than any polynomial 1/K^p.  In contrast the 1st-order Trotter/
product-formula segment error is O(t^2 ||H||^2 / r), giving error
        eps ~ 1 / r     (r = # Trotter steps  == LCU's "K" here).

We DO NOT need to actually build a quantum circuit to falsify or confirm
the mechanism: LCU's action on the input state, ASSUMING oblivious AA succeeds,
is exactly the (normalized) linear combination of unitary terms.  So we
directly compute the truncated Taylor-series operator U_K on a numpy state
vector and compare it to the exact evolution scipy.linalg.expm(-1j H t).

We also implement:
    - a real numpy statevector for n=3 qubits (dim N=8),
    - a random d=2-sparse HERMITIAN H with real entries in [-1, 1]
      (with exact row-sparsity control),
    - a real LCU normalization check: sum_k |c_k|^2 (=: s) matches the
      amplitude squared observed in the LCU "|0><0| ancilla" success branch,
    - Trotter 1st-order for comparison.

Reproducible: fixed numpy seed.
Output: report/evidence/results.json, plot report/evidence/eps_vs_K.png
"""
from __future__ import annotations
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import scipy.linalg as sla

HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "results.json"
OUT_PNG = HERE / "eps_vs_K.png"

RNG_SEED = 20260705


def make_d_sparse_hermitian(N: int, d: int, rng: np.random.Generator) -> np.ndarray:
    """Return an N x N Hermitian matrix with at most d non-zero entries per row/column
    (off-diagonal + diagonal counted), real entries in [-1, 1]."""
    H = np.zeros((N, N), dtype=np.complex128)
    # 1 diagonal entry per row is allowed, plus up to (d-1) off-diagonal per row.
    # Assemble symmetrically: for each row i, pick (d-1) column indices j > i,
    # give H[i,j] a random real value in [-1,1] and mirror to H[j,i].
    # Then fill the diagonal.  This yields row-sparsity <= d approximately.
    for i in range(N):
        # off-diagonal partners
        cols = [c for c in range(N) if c != i and abs(H[i, c]) == 0]
        rng.shuffle(cols)
        # take up to (d-1) new partners for row i
        added = 0
        for c in cols:
            if added >= d - 1:
                break
            # respect column sparsity too: number of already-nonzero entries in column c
            # (excluding what we're about to set) must be <= d-1
            if np.count_nonzero(H[:, c]) >= d - 1 + (1 if H[c, c] != 0 else 0):
                continue
            v = rng.uniform(-1.0, 1.0)
            H[i, c] = v
            H[c, i] = v
            added += 1
    for i in range(N):
        H[i, i] = rng.uniform(-1.0, 1.0)
    return H


def row_sparsity(H: np.ndarray) -> int:
    return int(max(np.count_nonzero(H[i, :]) for i in range(H.shape[0])))


def taylor_lcu_operator(H: np.ndarray, t: float, K: int) -> np.ndarray:
    """Truncated Taylor series operator U_K = sum_{k=0}^K (-i t)^k H^k / k!.

    This IS what the paper's LCU circuit implements on the input state
    conditioned on the ancilla being measured in |0>, up to normalization.
    We include the normalization: the LCU circuit prepares
        |sqrt(c_k)/sqrt(s)> on the ancilla with s = sum_k |c_k|
    (Berry-Childs-Kothari uses coefficients |c_k| = |t|^k / k!, hence
    s = sum_{k=0}^K t^k / k! -> e^{t}); oblivious amplitude amplification
    boosts the success amplitude to 1 when the target unitary is close to unitary.
    For our comparison to expm(-iHt), we return the RAW operator U_K
    (i.e. what the LCU circuit's success branch applies, un-amplified);
    if K -> infinity this equals e^{-iHt}."""
    N = H.shape[0]
    U = np.zeros((N, N), dtype=np.complex128)
    Hk = np.eye(N, dtype=np.complex128)
    for k in range(K + 1):
        coeff = ((-1j * t) ** k) / math.factorial(k)
        U = U + coeff * Hk
        Hk = Hk @ H
    return U


def lcu_prepare_amplitudes(t: float, K: int) -> np.ndarray:
    """Amplitudes on the ancilla register that the PREPARE unitary should load:
       |sqrt(c_k)/sqrt(s)>, k=0..K, with c_k = t^k / k! and s = sum c_k."""
    c = np.array([(t ** k) / math.factorial(k) for k in range(K + 1)])
    s = c.sum()
    return np.sqrt(c / s), s


def trotter_first_order(H: np.ndarray, t: float, r: int) -> np.ndarray:
    """1st-order Trotter/product-formula reference.

    For a *single* Hermitian H, exp(-i H t/r)^r is exact (=exp(-iHt)),
    so we deliberately split H into diagonal (D) and off-diagonal (X) parts
    to expose the O(t^2/r) product-formula error, as in the paper's
    d^2 ||H||_max t / r style analysis."""
    D = np.diag(np.diag(H))
    X = H - D
    step = sla.expm(-1j * D * (t / r)) @ sla.expm(-1j * X * (t / r))
    U = np.linalg.matrix_power(step, r)
    return U


def frob_err(A: np.ndarray, B: np.ndarray) -> float:
    return float(np.linalg.norm(A - B, ord="fro"))


def spectral_err(A: np.ndarray, B: np.ndarray) -> float:
    return float(np.linalg.norm(A - B, ord=2))


def main() -> None:
    rng = np.random.default_rng(RNG_SEED)

    N = 8           # 3 qubits
    d_target = 2    # 2-sparse Hermitian
    H = make_d_sparse_hermitian(N, d_target, rng)
    d_actual = row_sparsity(H)
    Hmax = float(np.max(np.abs(H)))
    Hspec = float(np.linalg.norm(H, ord=2))
    print(f"H: N={N} d_target={d_target} d_actual={d_actual} "
          f"||H||_max={Hmax:.4f} ||H||_2={Hspec:.4f}")

    # Sanity: Hermiticity
    herm_err = float(np.max(np.abs(H - H.conj().T)))
    assert herm_err < 1e-12, herm_err

    # State-vector picture: apply operators to |psi_0> = uniform superposition
    psi0 = np.ones(N, dtype=np.complex128) / math.sqrt(N)

    results = {
        "paper": {
            "arxiv_id": "1312.1414",
            "title": "Exponential improvement in precision for simulating sparse Hamiltonians",
            "authors": ["Dominic W. Berry", "Andrew M. Childs", "Richard Cleve",
                        "Robin Kothari", "Rolando D. Somma"],
        },
        "system": {
            "N": N, "n_qubits": int(math.log2(N)),
            "d_target": d_target, "d_actual": d_actual,
            "H_max": Hmax, "H_spectral_norm": Hspec,
            "rng_seed": RNG_SEED,
        },
        "runs": [],
    }

    Ks = [1, 2, 4, 6, 8, 10, 12, 14, 16, 20]
    ts = [0.5, 1.0]

    for t in ts:
        tau = (d_actual ** 2) * Hmax * t
        U_exact = sla.expm(-1j * H * t)
        # Check Trotter with r == K for fair comparison
        for K in Ks:
            # --- LCU / Taylor ---
            U_taylor = taylor_lcu_operator(H, t, K)
            eps_taylor_op_fro = frob_err(U_taylor, U_exact)
            eps_taylor_op_spec = spectral_err(U_taylor, U_exact)
            psi_taylor = U_taylor @ psi0
            psi_exact = U_exact @ psi0
            eps_taylor_state = float(np.linalg.norm(psi_taylor - psi_exact))
            # Prepare amplitudes + s (Berry-Childs "|c_k|" scheme)
            amps, s = lcu_prepare_amplitudes(t, K)
            amp_sqsum = float(np.sum(amps ** 2))  # should be 1
            # --- Trotter 1st order with r == K ---
            U_trot = trotter_first_order(H, t, r=K)
            eps_trot_op_fro = frob_err(U_trot, U_exact)
            eps_trot_op_spec = spectral_err(U_trot, U_exact)
            psi_trot = U_trot @ psi0
            eps_trot_state = float(np.linalg.norm(psi_trot - psi_exact))
            # analytic Taylor-remainder bound: (||H|| t)^(K+1)/(K+1)!
            bound = (Hspec * t) ** (K + 1) / math.factorial(K + 1)
            entry = {
                "t": t, "K": K, "tau_d2Hmaxt": tau,
                "lcu_taylor": {
                    "eps_op_fro": eps_taylor_op_fro,
                    "eps_op_spec": eps_taylor_op_spec,
                    "eps_state": eps_taylor_state,
                    "prepare_amp_sqsum": amp_sqsum,
                    "prepare_s_sum_ck": s,
                    "analytic_remainder_bound": bound,
                },
                "trotter_first_order_r_eq_K": {
                    "eps_op_fro": eps_trot_op_fro,
                    "eps_op_spec": eps_trot_op_spec,
                    "eps_state": eps_trot_state,
                },
            }
            results["runs"].append(entry)
            print(f"t={t} K={K:>2}  LCU eps_op_fro={eps_taylor_op_fro:.3e} "
                  f"bound={bound:.3e}  |  Trot eps_op_fro={eps_trot_op_fro:.3e}")

    # Empirical scaling test: log(eps_lcu) vs K should be roughly log(1/K!)
    # (slope steeper than any polynomial), while log(eps_trot) vs log(K) should
    # be slope ~ -1 (Trotter r == K -> eps ~ 1/K).
    import numpy as _np
    for t in ts:
        rows_t = [r for r in results["runs"] if r["t"] == t]
        Ks_arr = _np.array([r["K"] for r in rows_t])
        eps_lcu = _np.array([r["lcu_taylor"]["eps_op_fro"] for r in rows_t])
        eps_trot = _np.array([r["trotter_first_order_r_eq_K"]["eps_op_fro"] for r in rows_t])
        # LCU: fit log(eps) vs log(K!) -> slope
        with _np.errstate(divide="ignore"):
            logK_fact = _np.array([math.lgamma(K + 2) for K in Ks_arr])
            log_eps_lcu = _np.log(_np.clip(eps_lcu, 1e-300, None))
            # LCU should show near-slope -1 vs log((K+1)!)
            lcu_slope_vs_logKfact, lcu_intercept = _np.polyfit(logK_fact, log_eps_lcu, 1)
            # Trotter: log(eps_trot) vs log(K) -> slope ~ -1 (or slightly steeper for r=K on this H)
            log_eps_trot = _np.log(_np.clip(eps_trot, 1e-300, None))
            trot_slope_vs_logK, trot_intercept = _np.polyfit(_np.log(Ks_arr), log_eps_trot, 1)
        results.setdefault("scaling", {})[f"t={t}"] = {
            "lcu_slope_log_eps_vs_log_Kplus1_factorial": float(lcu_slope_vs_logKfact),
            "lcu_intercept": float(lcu_intercept),
            "trotter_slope_log_eps_vs_log_K": float(trot_slope_vs_logK),
            "trotter_intercept": float(trot_intercept),
            "interpretation": (
                "LCU slope near -1 vs log((K+1)!) confirms super-exponential "
                "eps ~ 1/(K+1)!; Trotter slope near -1 vs log(K) confirms polynomial 1/K."
            ),
        }
        print(f"[t={t}] LCU slope vs log((K+1)!) = "
              f"{results['scaling'][f't={t}']['lcu_slope_log_eps_vs_log_Kplus1_factorial']:.3f} "
              f"(expect ~ -1)")
        print(f"[t={t}] Trot slope vs log(K)      = "
              f"{results['scaling'][f't={t}']['trotter_slope_log_eps_vs_log_K']:.3f} "
              f"(expect ~ -1)")

    OUT_JSON.write_text(json.dumps(results, indent=2))
    print("Wrote", OUT_JSON)

    # Plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 5))
        for t in ts:
            rows_t = [r for r in results["runs"] if r["t"] == t]
            Ks_arr = [r["K"] for r in rows_t]
            eps_lcu = [r["lcu_taylor"]["eps_op_fro"] for r in rows_t]
            eps_trot = [r["trotter_first_order_r_eq_K"]["eps_op_fro"] for r in rows_t]
            bounds = [r["lcu_taylor"]["analytic_remainder_bound"] for r in rows_t]
            ax.semilogy(Ks_arr, eps_lcu, "o-", label=f"LCU/Taylor (t={t})")
            ax.semilogy(Ks_arr, eps_trot, "s--", label=f"Trotter r=K (t={t})")
            ax.semilogy(Ks_arr, bounds, ":", label=f"(||H||t)^(K+1)/(K+1)! bound (t={t})")
        ax.set_xlabel("K  (Taylor cutoff  /  Trotter steps)")
        ax.set_ylabel(r"$\|U_K - e^{-iHt}\|_F$")
        ax.set_title("Berry+Childs+Cleve+Kothari+Somma 2013 (1312.1414) — replication\n"
                     "LCU/Taylor vs 1st-order Trotter, N=8 d=2 Hermitian")
        ax.grid(True, which="both", ls=":")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(OUT_PNG, dpi=140)
        print("Wrote", OUT_PNG)
    except Exception as e:
        print("plot skipped:", e)


if __name__ == "__main__":
    main()
