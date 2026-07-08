"""
Bonus experiment for arXiv:1910.12085.

Paper (Section 1, Introduction): "a device could score well on Linear XEB while
being far from correct in total variation distance by, for example, always
outputting the items with the k highest probabilities."

Here we DEMONSTRATE that observation with a classical top-k "spoofer" that
requires access to the ideal probabilities (i.e. a full statevector sim -- this
is only feasible at small n). The paper's whole point is that this route is
hard *without* being able to compute those amplitudes efficiently.

We compare 4 samplers on n=6..8 qubit random circuits:
  (A) ideal   -- sample from the true distribution         -> b ~ 2
  (B) uniform -- uniform random bitstrings                 -> b ~ 1
  (C) top-k   -- output the k=n_samples heaviest strings   -> b >> 2   (spoof)
  (D) top-1   -- output the single heaviest string k times -> b maximal
"""

import json
from pathlib import Path

import cirq
import numpy as np

from xeb_demo import (
    random_google_style_circuit,
    ideal_probabilities,
    sample_ideal,
    sample_uniform,
    xeb_scores,
)


def sample_topk(probs: np.ndarray, n_samples: int) -> np.ndarray:
    """Return the top-n_samples heaviest indices (with repetition if needed).

    NOTE: XHOG (Problem 1) requires *distinct* samples; here we deliberately
    allow repetition just to show the extreme naive-cheating score. We also
    report the *distinct* version separately.
    """
    dim = probs.shape[0]
    order = np.argsort(-probs)  # descending
    if n_samples <= dim:
        return order[:n_samples]
    reps = n_samples // dim + 1
    return np.tile(order, reps)[:n_samples]


def sample_topk_distinct(probs: np.ndarray, k_distinct: int) -> np.ndarray:
    dim = probs.shape[0]
    k_distinct = min(k_distinct, dim)
    order = np.argsort(-probs)
    return order[:k_distinct]


def sample_top1(probs: np.ndarray, n_samples: int) -> np.ndarray:
    dim = probs.shape[0]
    top = int(np.argmax(probs))
    return np.full(n_samples, top, dtype=np.int64)


def main():
    rng = np.random.default_rng(1234)
    rows = []
    for n, depth in [(6, 12), (7, 14), (8, 16)]:
        n_samples = 20000
        n_circuits = 20
        agg = {"ideal": [], "uniform": [], "topk": [], "top1": [], "topk_distinct_b": []}
        for _ in range(n_circuits):
            circ = random_google_style_circuit(n, depth, rng)
            probs = ideal_probabilities(circ, n)

            # ideal
            idx = sample_ideal(probs, n_samples, rng)
            agg["ideal"].append(xeb_scores(probs, idx, n)["b_xhog"])

            # uniform spoof
            idx = sample_uniform(n, n_samples, rng)
            agg["uniform"].append(xeb_scores(probs, idx, n)["b_xhog"])

            # top-k spoof (needs full statevector: infeasible at large n -- point of paper)
            idx = sample_topk(probs, n_samples)
            agg["topk"].append(xeb_scores(probs, idx, n)["b_xhog"])

            # top-1 all-in
            idx = sample_top1(probs, n_samples)
            agg["top1"].append(xeb_scores(probs, idx, n)["b_xhog"])

            # top-k distinct with k = min(2^n, 100) as a smaller XHOG-legal batch
            k_distinct = min(2 ** n, 100)
            idx = sample_topk_distinct(probs, k_distinct)
            agg["topk_distinct_b"].append(xeb_scores(probs, idx, n)["b_xhog"])

        def stats(vals):
            arr = np.array(vals, dtype=float)
            return float(arr.mean()), float(arr.std(ddof=1) / np.sqrt(len(arr)))

        row = {"n": n, "depth": depth}
        for k, v in agg.items():
            m, sem = stats(v)
            row[f"b_{k}_mean"] = m
            row[f"b_{k}_sem"] = sem
        rows.append(row)
        print(
            f"n={n} d={depth}  "
            f"ideal={row['b_ideal_mean']:.3f}+/-{row['b_ideal_sem']:.3f}  "
            f"unif={row['b_uniform_mean']:.3f}+/-{row['b_uniform_sem']:.3f}  "
            f"topk={row['b_topk_mean']:.3f}+/-{row['b_topk_sem']:.3f}  "
            f"top1={row['b_top1_mean']:.3f}+/-{row['b_top1_sem']:.3f}  "
            f"topk_distinct(k=100)={row['b_topk_distinct_b_mean']:.3f}+/-{row['b_topk_distinct_b_sem']:.3f}"
        )

    Path("report/evidence/spoof_topk.json").write_text(json.dumps({"rows": rows}, indent=2))
    print("Wrote report/evidence/spoof_topk.json")


if __name__ == "__main__":
    main()
