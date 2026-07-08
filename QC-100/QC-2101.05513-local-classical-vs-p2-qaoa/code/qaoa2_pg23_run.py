#!/usr/bin/env python
"""
Optimize QAOA_2 on the PG(2,3) incidence graph (26 vertices, 4-regular, girth 6).
Setup ~70s one-time; each eval ~10s.  Budget: ~40 min total.

Strategy: 4 random restarts with COBYLA (maxiter=40 each) = 160 evals + setup
= roughly 30 min.  We also seed one restart from a known-good QAOA_2 region
for high-girth 3-regular graphs (small gamma, small beta).
"""
import time, sys, os, json
sys.path.insert(0, "code")
import numpy as np
from scipy.optimize import minimize
from qaoa2_aer import cost_eval_factory
from pg23_incidence import build_incidence_graph

G = build_incidence_graph()
D = 4
target = 0.6693  # paper Table 1: QAOA_2 improvement 0.1693 -> cut fraction 0.6693

print("[pg23-qaoa2] setup...")
t0 = time.time()
evaluator, n, m, _, _ = cost_eval_factory(G)
print(f"[pg23-qaoa2] setup {time.time()-t0:.1f}s  n={n} m={m}")

# Seeds: mix known-good starting regions + random
seeds = [
    [0.4, 0.3, 0.6, 0.2],   # smallish gammas, beta ~ pi/8
    [0.3, 0.4, 0.5, 0.3],
    [0.6, 0.2, 0.4, 0.4],
    [0.5, 0.35, 0.55, 0.25],
]

overall_best = -np.inf
overall_best_x = None
history = []

for k, x0 in enumerate(seeds):
    tk = time.time()
    print(f"[pg23-qaoa2] restart {k}: x0 = {x0}")
    # count evals
    call_count = [0]
    def wrapped(x):
        call_count[0] += 1
        return -evaluator(x)
    res = minimize(wrapped, x0, method="COBYLA",
                   options={"maxiter": 40, "rhobeg": 0.10})
    val = -res.fun
    history.append({"restart": k, "x0": x0,
                    "x": [float(z) for z in res.x],
                    "cut": float(val),
                    "n_evals": call_count[0],
                    "elapsed_sec": time.time() - tk})
    print(f"[pg23-qaoa2] restart {k}: cut={val:.4f} frac={val/m:.4f} "
          f"n_evals={call_count[0]} in {time.time()-tk:.1f}s")
    if val > overall_best:
        overall_best = val
        overall_best_x = res.x.tolist()

cut_frac = overall_best / m
print(f"\n[pg23-qaoa2] BEST cut fraction = {cut_frac:.5f}  (paper: {target:.5f})")
print(f"[pg23-qaoa2] abs diff = {abs(cut_frac - target):.5f}")
print(f"[pg23-qaoa2] best params: {overall_best_x}")

out = {
    "graph": "pg23_incidence",
    "n_vertices": n, "n_edges": m, "D": D, "girth": 6,
    "expected_cut_edges": float(overall_best),
    "cut_fraction": float(cut_frac),
    "paper_target_cut_fraction": target,
    "paper_target_improvement_over_random": target - 0.5,
    "achieved_improvement_over_random": float(cut_frac - 0.5),
    "abs_diff_vs_paper": float(abs(cut_frac - target)),
    "best_params": overall_best_x,
    "method": "seeded COBYLA restarts",
    "history": history,
}
os.makedirs("report/evidence", exist_ok=True)
with open("report/evidence/qaoa2_pg23.json", "w") as f:
    json.dump(out, f, indent=2)
print("[pg23-qaoa2] wrote report/evidence/qaoa2_pg23.json")
