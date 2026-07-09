#!/usr/bin/env python3
"""
Extended replication run: sample many solvable 3-SAT instances at varying
clause density, measure classical T and the walk's phase-gap-derived iteration
count k_q, and fit the log-log slope. If Montanaro's Theorem 2 holds (and thus
Belovs' spectral gap 1/sqrt(Tn) for the tree walk), we expect
    k_q ~ sqrt(T)  when n fixed.
"""
from __future__ import annotations
import json, math, random, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from replicate import (gen_3sat, dpll_build_tree, build_walk_operator,
                       walk_spectral_analysis, grover_style_simulation)

def main():
    rng = random.Random(20260706)
    n = 10
    per_instance = []
    trials = 0
    target_bins = list(range(6))  # 6 T-bins
    # bin ranges (widened)
    bin_edges = [(15,50),(50,120),(120,250),(250,500),(500,1000),(1000,2000)]
    filled = {i: [] for i in target_bins}
    per_bin_target = 4

    start = time.time()
    while any(len(v) < per_bin_target for v in filled.values()) and trials < 3000 and time.time()-start < 300:
        trials += 1
        m = rng.randint(18, 55)
        clauses = gen_3sat(n, m, rng)
        nodes, sol = dpll_build_tree(clauses, n, node_cap=2200)
        if sol is None:
            continue
        T = len(nodes)
        for i,(lo,hi) in enumerate(bin_edges):
            if lo <= T <= hi and len(filled[i]) < per_bin_target:
                # only run walk if T is small enough for eig cost (T^3)
                if T > 1500:
                    filled[i].append(dict(T=T, m=m, n=n, skipped='too_big_for_eig'))
                    break
                RA, RB, T2 = build_walk_operator(nodes, sol)
                spec = walk_spectral_analysis(RA, RB, 0)
                filled[i].append(dict(T=T, m=m, n=n,
                    k_q=spec['n_walk_iters_for_detection'],
                    gap=spec['smallest_nonzero_phase'],
                    trial=trials))
                print(f"  bin={i} T={T} m={m} k_q={spec['n_walk_iters_for_detection']:.2f}  "
                      f"gap={spec['smallest_nonzero_phase']:.4f}   [trial {trials}]")
                break

    all_pts = [pt for lst in filled.values() for pt in lst if 'k_q' in pt and math.isfinite(pt.get('k_q', float('nan')))]
    if len(all_pts) >= 3:
        Ts = np.array([p['T'] for p in all_pts], dtype=float)
        Ks = np.array([p['k_q'] for p in all_pts], dtype=float)
        logs_T = np.log(Ts); logs_K = np.log(Ks)
        A = np.vstack([logs_T, np.ones_like(logs_T)]).T
        m,b = np.linalg.lstsq(A, logs_K, rcond=None)[0]
        pred = A @ np.array([m,b])
        ss_res = float(((logs_K - pred)**2).sum())
        ss_tot = float(((logs_K - logs_K.mean())**2).sum())
        r2 = 1 - ss_res/ss_tot if ss_tot > 0 else float('nan')
        fit = dict(slope=float(m), intercept=float(b), r2=float(r2), N=len(all_pts))
    else:
        fit = dict(slope=None, N=len(all_pts))

    print("\n=== SCALING FIT ===")
    print(f"N points: {fit.get('N')}")
    print(f"slope    : {fit.get('slope')}")
    print(f"R^2      : {fit.get('r2')}")
    print(f"expected : 0.5  (for k_q ~ sqrt(T))")

    Path(__file__).parent.joinpath("results_v2.json").write_text(json.dumps(dict(
        paper="arXiv:1509.02374",
        n_variables=n,
        instances=all_pts,
        trials=trials,
        fit_kq_vs_T=fit,
        expected_slope=0.5,
    ), indent=2, default=str))
    print("Wrote results_v2.json")

if __name__ == "__main__":
    main()
