#!/usr/bin/env python3
"""Quantify C3: BBHT expected iterations vs t (number of marked items).

Paper claim (attributed to BBHT [2] in Dürr–Høyer 1996): expected number of
Grover iterations to find a marked item, when t >= 1 items are marked, is
O(sqrt(N/t)). We measure this directly.
"""
import json
import math
import random
import statistics
import sys
import numpy as np

sys.path.insert(0, ".")
from durr_hoyer_independent import bbht_search


def sweep(N, ts, trials=500, seed=42):
    rng = random.Random(seed)
    n_qubits = int(round(math.log2(N)))
    rows = []
    for t in ts:
        if t > N or t < 1:
            continue
        iters_list = []
        for _ in range(trials):
            marks = rng.sample(range(N), t)
            mask = np.zeros(N, dtype=bool)
            for i in marks:
                mask[i] = True
            # give BBHT a generous ceiling (100x expected O(sqrt(N/t)))
            budget = int(100 * math.ceil(math.sqrt(N / t)) + 200)
            idx, used = bbht_search(n_qubits, mask, rng, budget)
            if idx is not None:
                iters_list.append(used)
        mean_i = statistics.mean(iters_list)
        median_i = statistics.median(iters_list)
        std_i = statistics.pstdev(iters_list)
        sqrt_bound = math.sqrt(N / t)
        rows.append({
            "N": N, "t": t,
            "trials_completed": len(iters_list),
            "mean_iters": mean_i,
            "median_iters": median_i,
            "std_iters": std_i,
            "sqrt_N_over_t": sqrt_bound,
            "mean_over_sqrt_bound": mean_i / sqrt_bound,
        })
    return rows


def main():
    all_rows = []
    for N in [16, 32, 64, 128]:
        ts = sorted(set([1, 2, 4, max(1, N // 8), max(1, N // 4), N // 2]))
        ts = [t for t in ts if 1 <= t <= N]
        all_rows.extend(sweep(N, ts, trials=300))

    print(f"{'N':>4} {'t':>4} {'mean_it':>9} {'med_it':>7} {'std':>7} {'sqrt(N/t)':>10} {'mean/bound':>10}")
    for r in all_rows:
        print(f"{r['N']:>4} {r['t']:>4} {r['mean_iters']:>9.2f} {r['median_iters']:>7.1f} {r['std_iters']:>7.2f} {r['sqrt_N_over_t']:>10.3f} {r['mean_over_sqrt_bound']:>10.3f}")

    with open("report/evidence/bbht_t_sweep.json", "w") as f:
        json.dump({"rows": all_rows,
                   "note": "BBHT expected iterations vs t. Ratio mean_iters/sqrt(N/t) should be bounded (const)."},
                  f, indent=2)
    print("[wrote] report/evidence/bbht_t_sweep.json")


if __name__ == "__main__":
    main()
