#!/usr/bin/env python3
"""Confirm the bandwidth-vs-accuracy pattern across multiple seeds; average results."""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_bandwidth_sweep import (
    build_data, run_one_lambda, LAMBDAS, EVIDENCE
)

SEEDS = [20260703, 20260704, 20260705, 20260706, 20260707]

def main():
    all_rows = []
    per_lambda = {lam: [] for lam in LAMBDAS}
    for seed in SEEDS:
        # override the seed used inside build_data
        Xtr, Xte, ytr, yte = build_data(seed=seed)
        for lam in LAMBDAS:
            r = run_one_lambda(lam, Xtr, Xte, ytr, yte, C_svm=1.0)
            r["seed"] = seed
            all_rows.append(r)
            per_lambda[lam].append(r["test_acc"])
            print(f"[seed={seed} lam={lam:>7.4f}] train={r['train_acc']:.3f} test={r['test_acc']:.3f}")
    summary = []
    print("\n=== mean test accuracy across {} seeds ===".format(len(SEEDS)))
    for lam in LAMBDAS:
        arr = np.array(per_lambda[lam])
        summary.append({
            "lambda": lam, "mean_test_acc": float(arr.mean()),
            "std_test_acc": float(arr.std(ddof=1)) if len(arr) > 1 else 0.0,
            "n_seeds": len(arr),
        })
        print(f"lambda={lam:>7.4f}  mean_test={arr.mean():.3f}  std={arr.std(ddof=1):.3f}  n={len(arr)}")
    out = {
        "seeds": SEEDS,
        "lambdas": LAMBDAS,
        "per_run": all_rows,
        "summary": summary,
    }
    outp = os.path.join(EVIDENCE, "bandwidth_sweep_multiseed.json")
    with open(outp, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[write] {outp}")

if __name__ == "__main__":
    main()
