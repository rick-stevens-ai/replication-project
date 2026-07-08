"""
Main experiment for the VQAE replication.
Runs:
  (A) Classical MC amplitude estimation over a sweep of N_shots
  (B) MLAE (linear schedule) over a sweep of M
  (C) Naïve VQAE (k=1, small M) for a headline point
Compares scaling of δθ vs Nq to the paper's expected behaviour:
  MC:   δθ ~ Nq^(-1/2)
  MLAE: δθ ~ Nq^(-3/4)  (linear schedule)
  VQAE: intermediate, saturating to Nq^(-1/2) at large M
"""

import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)

from vqae_core import (
    cauchy_lorentz_probs, linear_f, build_state_chi0, true_a, theta_from_a,
    classical_mc, mlae_run, naive_vqae, prob_ancilla_one, delta_theta, a_from_theta,
)

OUT = os.path.abspath(os.path.join(HERE, "..", "report", "evidence"))
os.makedirs(OUT, exist_ok=True)


def median_stat(vals):
    return float(np.median(vals)), float(np.percentile(vals, 25)), float(np.percentile(vals, 75))


def run_mc_scan(n, chi0, theta_true, N_list, n_trials, seed=1):
    rng = np.random.default_rng(seed)
    results = []
    for Nshots in N_list:
        errs = []
        for t in range(n_trials):
            a_hat = classical_mc(chi0, n, Nshots, rng)
            # convert to theta (clip to valid range)
            a_hat = min(max(a_hat, 1e-9), 1.0 - 1e-9)
            theta_hat = math.asin(math.sqrt(a_hat))
            errs.append(delta_theta(theta_hat, theta_true))
        med, lo, hi = median_stat(errs)
        results.append({"Nq": int(Nshots), "median_dtheta": med,
                        "q25": lo, "q75": hi, "n_trials": n_trials})
        print(f"  MC  Nq={Nshots:8d}  median δθ={med:.4e}  (trials={n_trials})")
    return results


def run_mlae_scan(n, chi0, theta_true, M_list, h, n_trials, seed=2):
    rng = np.random.default_rng(seed)
    results = []
    for M in M_list:
        errs = []
        Nq_val = None
        for t in range(n_trials):
            theta_hat, Nq = mlae_run(chi0, n, M, h, rng)
            Nq_val = Nq
            errs.append(delta_theta(theta_hat, theta_true))
        med, lo, hi = median_stat(errs)
        results.append({"M": int(M), "Nq": int(Nq_val),
                        "median_dtheta": med, "q25": lo, "q75": hi,
                        "n_trials": n_trials})
        print(f"  MLAE  M={M:3d}  Nq={Nq_val:8d}  median δθ={med:.4e}  (trials={n_trials})")
    return results


def run_vqae_point(n, chi0, theta_true, M, h, d, n_trials, seed=3, n_sweeps=25):
    rng = np.random.default_rng(seed)
    errs = []
    all_infids = []
    Nq_val = None
    for t in range(n_trials):
        theta_hat, Nq, infids = naive_vqae(chi0, n, M, h, d, rng, n_sweeps=n_sweeps)
        Nq_val = Nq
        errs.append(delta_theta(theta_hat, theta_true))
        all_infids.append(infids)
    med, lo, hi = median_stat(errs)
    mean_infid_by_m = np.mean(all_infids, axis=0).tolist() if all_infids else []
    print(f"  VQAE  M={M} d={d}  Nq_samp={Nq_val}  median δθ={med:.4e} (trials={n_trials})")
    return {
        "M": int(M), "d": int(d), "Nq_samp": int(Nq_val),
        "median_dtheta": med, "q25": lo, "q75": hi,
        "n_trials": n_trials,
        "mean_infidelity_by_m": mean_infid_by_m,
    }


def fit_loglog(x, y):
    """Return (slope, intercept) of a linear fit log10(y) = slope*log10(x) + intercept.
    Robust to a few zeros/nans."""
    x = np.asarray(x); y = np.asarray(y)
    mask = (y > 0) & (x > 0)
    lx = np.log10(x[mask]); ly = np.log10(y[mask])
    if lx.size < 2:
        return float("nan"), float("nan")
    A = np.vstack([lx, np.ones_like(lx)]).T
    m, b = np.linalg.lstsq(A, ly, rcond=None)[0]
    return float(m), float(b)


def main():
    t0 = time.time()
    n = 4              # 4 problem qubits + 1 ancilla = 5-qubit statevector
    h = 200            # shots per MLAE step (paper uses 2000; we scale down for wall-clock)
    n_trials = 25      # trials per data point (paper's Fig 4 uses many; we use enough for medians)

    # ---- Problem: shifted Cauchy-Lorentz PDF, f(x)=x  ----
    p = cauchy_lorentz_probs(n, x0=0.5, gamma=0.1)
    N = 2 ** n
    x = np.arange(N) / N
    f = linear_f(x)
    chi0 = build_state_chi0(n, p, f)
    a = true_a(p, f)
    theta_true = theta_from_a(a)
    p1_check = prob_ancilla_one(chi0, n)
    print(f"Problem: n={n}, dist=Cauchy-Lorentz(x0=0.5, γ=0.1), f(x)=x")
    print(f"  a_true = {a:.8f}   (check: Prob(anc=1) = {p1_check:.8f})")
    print(f"  θ_true = {theta_true:.8f} rad\n")

    # (A) Classical MC scan
    print("=== (A) Classical MC ===")
    N_list = [100, 300, 1000, 3000, 10000, 30000, 100000, 300000]
    mc_results = run_mc_scan(n, chi0, theta_true, N_list, n_trials)

    # (B) MLAE scan (linear schedule) — Nq scales as h*M*(M+2)
    print("\n=== (B) MLAE (linear schedule) ===")
    M_list = [1, 2, 3, 5, 8, 12, 18, 25]
    mlae_results = run_mlae_scan(n, chi0, theta_true, M_list, h, n_trials)

    # (C) Naïve VQAE headline point — small M, k=1, PQC depth d=3
    print("\n=== (C) Naïve VQAE (k=1) — headline points ===")
    vqae_results = []
    for M in [3, 5, 8]:
        vqae_results.append(run_vqae_point(n, chi0, theta_true, M=M, h=h, d=3,
                                            n_trials=6, n_sweeps=20))

    # Scaling fits
    mc_Nq   = [r["Nq"] for r in mc_results]
    mc_err  = [r["median_dtheta"] for r in mc_results]
    mlae_Nq = [r["Nq"] for r in mlae_results]
    mlae_err = [r["median_dtheta"] for r in mlae_results]

    mc_slope, mc_intercept = fit_loglog(mc_Nq, mc_err)
    mlae_slope, mlae_intercept = fit_loglog(mlae_Nq, mlae_err)

    print("\n=== Scaling fits (log10 δθ vs log10 Nq) ===")
    print(f"  Classical MC:  slope = {mc_slope:.3f}   (paper predicts -0.500)")
    print(f"  MLAE (linear): slope = {mlae_slope:.3f}   (paper predicts -0.750)")

    # Save all evidence
    evidence = {
        "problem": {
            "n": n, "distribution": "cauchy_lorentz",
            "x0": 0.5, "gamma": 0.1, "f": "x",
            "a_true": a, "theta_true": theta_true,
            "N_grid": N,
        },
        "shots_per_mlae_step": h,
        "trials_per_point": n_trials,
        "classical_mc": mc_results,
        "mlae_linear": mlae_results,
        "naive_vqae_k1_d3": vqae_results,
        "scaling_fits": {
            "classical_mc": {"slope": mc_slope, "intercept": mc_intercept,
                             "paper_prediction": -0.5},
            "mlae_linear": {"slope": mlae_slope, "intercept": mlae_intercept,
                            "paper_prediction": -0.75},
        },
        "wall_seconds": time.time() - t0,
    }
    with open(os.path.join(OUT, "experiment_results.json"), "w") as fh:
        json.dump(evidence, fh, indent=2)
    print(f"\nWrote {OUT}/experiment_results.json")
    print(f"Total wall time: {evidence['wall_seconds']:.1f} s")


if __name__ == "__main__":
    main()
