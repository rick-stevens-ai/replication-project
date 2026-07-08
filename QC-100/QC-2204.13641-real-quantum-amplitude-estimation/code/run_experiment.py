"""End-to-end empirical study reproducing the RQAE headline (Figure 6):
  N_oracle scales as ~1/eps for RQAE (quantum-speedup), vs ~1/eps^2 for classical.

Runs at multiple target precisions eps in {0.05, 0.02, 0.01, 0.005}, using
q ∈ {2}, gamma=0.05, and R=25 repetitions per (a_true, eps). Reports
mean N_oracle and RMSE(a_hat vs a_true) per configuration.

Compares to classical (unamplified) oracle calls at the same target eps.
Saves JSON to report/evidence/results.json.
"""
from __future__ import annotations
import json, math, os, sys, time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rqae import rqae, classical_amplitude_estimate, ENCODING_SCALE

OUT = Path(__file__).resolve().parents[1] / "report" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)

A_TRUES = [0.3, 0.7, -0.4]
EPS_LIST = [0.05, 0.02, 0.01, 0.005]
REPS = 25
GAMMA = 0.05
# For classical (unamplified) reference, shots explode as 1/eps^2. We cap
# classical eps to a moderate value and use fewer reps for the smaller eps.
CLASSICAL_EPS_LIST = [0.05, 0.02, 0.01]  # skip 0.005 (would be 2M shots/side)
CLASSICAL_REPS = {0.05: 25, 0.02: 15, 0.01: 5}

results = {"config": {"a_trues": A_TRUES, "eps_list": EPS_LIST, "reps": REPS,
                      "gamma": GAMMA, "q": 2.0, "encoding_scale": ENCODING_SCALE,
                      "sim": "qiskit_aer.AerSimulator (shot-based)"},
           "rqae": [], "classical": []}

t0 = time.time()
for a_true in A_TRUES:
    for eps in EPS_LIST:
        rec = {"a_true": a_true, "eps_target_true": eps,
               "eps_target_scaled": eps / ENCODING_SCALE,
               "reps": REPS, "runs": []}
        errs = []
        calls = []
        eps_finals = []
        for r in range(REPS):
            res = rqae(a_true=a_true, eps_target=eps / ENCODING_SCALE,
                       gamma=GAMMA, q=2.0, seed=1000 * r + int(1000 * (a_true + 1)))
            err = res.a_hat - a_true
            errs.append(err)
            calls.append(res.n_oracle)
            eps_finals.append(res.epsilon_final)
            rec["runs"].append({"seed_offset": r, "a_hat": res.a_hat,
                                 "eps_final_true": res.epsilon_final,
                                 "n_oracle": res.n_oracle,
                                 "n_iters": res.n_iters,
                                 "k_max": res.k_max_used})
        errs = np.array(errs); calls = np.array(calls); eps_finals = np.array(eps_finals)
        rec["rmse"] = float(np.sqrt(np.mean(errs ** 2)))
        rec["max_abs_err"] = float(np.max(np.abs(errs)))
        rec["mean_n_oracle"] = float(np.mean(calls))
        rec["median_n_oracle"] = float(np.median(calls))
        rec["mean_eps_final_true"] = float(np.mean(eps_finals))
        rec["coverage_within_eps"] = float(np.mean(np.abs(errs) <= eps))
        results["rqae"].append(rec)
        print(f"[RQAE] a={a_true:+.2f} eps={eps:.3f}  RMSE={rec['rmse']:.4f}  "
              f"N_q~{rec['mean_n_oracle']:.0f}  cov={rec['coverage_within_eps']:.2f}")

print("\n-- Classical (unamplified) reference --")
for a_true in A_TRUES:
    for eps in CLASSICAL_EPS_LIST:
        reps_here = CLASSICAL_REPS[eps]
        rec = {"a_true": a_true, "eps_target_true": eps, "reps": reps_here, "runs": []}
        errs = []; calls = []
        for r in range(reps_here):
            res = classical_amplitude_estimate(a_true=a_true, eps_target=eps,
                                               gamma=GAMMA, seed=2000 * r + int(1000 * (a_true + 1)))
            err = res["a_hat"] - a_true
            errs.append(err); calls.append(res["n_oracle"])
            rec["runs"].append({"seed_offset": r, "a_hat": res["a_hat"],
                                 "n_oracle": res["n_oracle"]})
        errs = np.array(errs); calls = np.array(calls)
        rec["rmse"] = float(np.sqrt(np.mean(errs ** 2)))
        rec["mean_n_oracle"] = float(np.mean(calls))
        rec["coverage_within_eps"] = float(np.mean(np.abs(errs) <= eps))
        results["classical"].append(rec)
        print(f"[CLASSICAL] a={a_true:+.2f} eps={eps:.3f}  RMSE={rec['rmse']:.4f}  "
              f"N_q~{rec['mean_n_oracle']:.0f}  cov={rec['coverage_within_eps']:.2f}")

# --- Scaling analysis: fit log10(N_q) = alpha * log10(1/eps) + beta ---
def fit_scaling(records):
    xs = np.log10([1.0 / r["eps_target_true"] for r in records])
    ys = np.log10([r["mean_n_oracle"] for r in records])
    slope, intercept = np.polyfit(xs, ys, 1)
    return float(slope), float(intercept)

# Aggregate across all a_trues per eps for both methods
def aggregate_by_eps(records):
    from collections import defaultdict
    agg = defaultdict(list)
    for r in records:
        agg[r["eps_target_true"]].append(r["mean_n_oracle"])
    out = []
    for eps, vs in sorted(agg.items(), reverse=True):
        out.append({"eps_target_true": eps, "mean_n_oracle": float(np.mean(vs))})
    return out

rqae_agg = aggregate_by_eps(results["rqae"])
classical_agg = aggregate_by_eps(results["classical"])
rqae_slope, rqae_intercept = fit_scaling(rqae_agg)
classical_slope, classical_intercept = fit_scaling(classical_agg)

results["scaling_fit"] = {
    "rqae": {"slope_log10_Nq_vs_log10_inv_eps": rqae_slope,
             "intercept": rqae_intercept,
             "interpretation": "slope ≈ 1 means N_q ~ 1/eps (quadratic speedup)",
             "paper_claim": "N_q scales approximately as 1/eps (Fig 6, Sec 3.2)",
             "aggregated_points": rqae_agg},
    "classical": {"slope_log10_Nq_vs_log10_inv_eps": classical_slope,
                  "intercept": classical_intercept,
                  "interpretation": "slope ≈ 2 means N_q ~ 1/eps^2 (classical)",
                  "aggregated_points": classical_agg}
}

results["headline"] = {
    "rqae_scaling_exponent": rqae_slope,
    "classical_scaling_exponent": classical_slope,
    "speedup_ratio_at_smallest_eps": (
        classical_agg[-1]["mean_n_oracle"] / rqae_agg[-1]["mean_n_oracle"]),
    "smallest_eps": rqae_agg[-1]["eps_target_true"],
}

results["wall_time_seconds"] = time.time() - t0

with open(OUT / "results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n=== SCALING FIT ===")
print(f"RQAE:      slope = {rqae_slope:.3f}  (paper claims ~1.0, quadratic speedup)")
print(f"CLASSICAL: slope = {classical_slope:.3f}  (theory ~2.0, unamplified)")
print(f"Speedup ratio at eps={rqae_agg[-1]['eps_target_true']}: "
      f"{results['headline']['speedup_ratio_at_smallest_eps']:.1f}x")
print(f"\nWrote {OUT / 'results.json'}  (elapsed {results['wall_time_seconds']:.1f}s)")
