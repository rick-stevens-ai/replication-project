#!/usr/bin/env python3
"""Classical baseline empirical measurement of probes to find the minimum.

For an unsorted table of N distinct values, the argmin scan requires exactly
N probes deterministically (must look at every element to be sure). We
measure this and compare to the quantum Durr-Hoyer results.
"""
import json
import math
import random
import statistics
import sys
sys.path.insert(0, ".")
from durr_hoyer_independent import classical_linear_scan


def main():
    rows = []
    rng = random.Random(0)
    for N in [4, 8, 16, 32, 64, 128, 256, 512]:
        probes_list = []
        correct = 0
        trials = 100
        for _ in range(trials):
            perm = list(range(N))
            rng.shuffle(perm)
            idx, probes = classical_linear_scan(perm)
            probes_list.append(probes)
            true_min_idx = perm.index(min(perm))
            if idx == true_min_idx:
                correct += 1
        rows.append({
            "N": N,
            "trials": trials,
            "success_prob": correct / trials,
            "mean_probes": statistics.mean(probes_list),
            "min_probes": min(probes_list),
            "max_probes": max(probes_list),
            "expected_O_N": N,
            "quantum_leading_bound_22_5_sqrtN": 22.5 * math.sqrt(N),
        })

    print(f"{'N':>4} {'p_succ':>7} {'mean_probes':>12} {'min':>4} {'max':>4} {'O(N)=N':>7} {'22.5√N':>9}")
    for r in rows:
        print(f"{r['N']:>4} {r['success_prob']:>7.3f} {r['mean_probes']:>12.1f} {r['min_probes']:>4} {r['max_probes']:>4} {r['expected_O_N']:>7} {r['quantum_leading_bound_22_5_sqrtN']:>9.2f}")

    with open("report/evidence/classical_baseline.json", "w") as f:
        json.dump({"rows": rows}, f, indent=2)
    print("[wrote] report/evidence/classical_baseline.json")


if __name__ == "__main__":
    main()
