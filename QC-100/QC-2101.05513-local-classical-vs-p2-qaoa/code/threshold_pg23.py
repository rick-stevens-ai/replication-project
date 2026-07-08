#!/usr/bin/env python
"""
Run threshold_1 and threshold_2 on PG(2,3) incidence graph (D=4, girth=6).
Compare to paper Table 1: Threshold_2(3,4) improvement=0.2128 -> cut fraction 0.7128.
"""
import sys, os, json, time
sys.path.insert(0, "code")
import numpy as np
from threshold_maxcut import threshold_algorithm, sweep_threshold2
from pg23_incidence import build_incidence_graph
import networkx as nx

G = build_incidence_graph()
n = G.number_of_nodes()
m = G.number_of_edges()
D = 4
girth = int(nx.girth(G))
print(f"[thr-pg23] graph=pg23_incidence n={n} m={m} D={D} girth={girth}")

# Paper Table 1 (D=4, girth>5):
# Threshold_1 (tau=3): 0.5 + 0.1406 = 0.6406
# Threshold_2 (tau1=3, tau2=4): 0.5 + 0.2128 = 0.7128
# QAOA_2: 0.5 + 0.1693 = 0.6693
# So Threshold_2 (classical) > QAOA_2 by 0.7128 - 0.6693 = 0.0435.

targets = {
    "thr1_tau3": 0.6406,
    "thr2_tau3_4": 0.7128,
    "qaoa2": 0.6693,
}

n_trials = 30000
seed = 20260703

print(f"[thr-pg23] running Threshold_1 (tau=3) with {n_trials} trials...")
t0 = time.time()
r_thr1 = threshold_algorithm(G, [3], n_trials=n_trials, seed=seed)
print(f"  cut = {r_thr1['mean']:.4f} +/- {r_thr1['sem']:.4f}  (paper: {targets['thr1_tau3']}) in {time.time()-t0:.1f}s")

print(f"[thr-pg23] running Threshold_2 (tau1=3, tau2=4) with {n_trials} trials...")
t0 = time.time()
r_thr2 = threshold_algorithm(G, [3, 4], n_trials=n_trials, seed=seed + 1)
print(f"  cut = {r_thr2['mean']:.4f} +/- {r_thr2['sem']:.4f}  (paper: {targets['thr2_tau3_4']}) in {time.time()-t0:.1f}s")

# also try a few other tau pairs
print(f"[thr-pg23] sweeping (tau1, tau2) in 1..5 with {n_trials//4} trials each...")
t0 = time.time()
sweep = sweep_threshold2(G, list(range(1, 6)), n_trials=n_trials // 4, seed=seed + 100)
print(f"  sweep done in {time.time()-t0:.1f}s")
best_key = max(sweep, key=lambda k: sweep[k]["mean"])
print(f"  empirical best: {best_key} -> {sweep[best_key]['mean']:.4f} +/- {sweep[best_key]['sem']:.4f}")

out = {
    "graph": "pg23_incidence",
    "n_vertices": n, "n_edges": m, "D": D, "girth": girth,
    "n_trials": n_trials,
    "thr1_tau3": r_thr1,
    "thr2_tau3_4": r_thr2,
    "paper_targets": targets,
    "sweep_full": sweep,
    "empirical_best_key": best_key,
    "empirical_best_cut_fraction": sweep[best_key]["mean"],
    "empirical_best_sem": sweep[best_key]["sem"],
}
os.makedirs("report/evidence", exist_ok=True)
with open("report/evidence/thr_pg23.json", "w") as f:
    json.dump(out, f, indent=2)

# Print comparative summary
print()
print("=== D=4 girth=6 (PG(2,3) incidence, n=26, m=52) ===")
print(f"  Threshold_1 (τ=3):        {r_thr1['mean']:.4f} ± {r_thr1['sem']:.4f}   (paper 0.6406)")
print(f"  Threshold_2 (τ=3,4):      {r_thr2['mean']:.4f} ± {r_thr2['sem']:.4f}   (paper 0.7128)")
print(f"  Best sweep {best_key}: {sweep[best_key]['mean']:.4f} ± {sweep[best_key]['sem']:.4f}")
print(f"  (QAOA_2 target from paper: 0.6693)")
print("[thr-pg23] wrote report/evidence/thr_pg23.json")
