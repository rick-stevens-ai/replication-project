#!/usr/bin/env python3
"""
Independent sanity check on the Grover core used inside our Dürr–Høyer
replication. Verifies that a single Grover run with k marked items and the
theoretically optimal rotation count r* = round(pi/4 * sqrt(N/k)) yields
success probability very close to 1 (matching sin^2((2r+1)*theta) where
sin(theta) = sqrt(k/N)).

Runs across (N, k) grid, prints empirical vs closed-form probabilities.
"""
import math
import json
import sys
import random
import numpy as np

sys.path.insert(0, ".")
from durr_hoyer_independent import (
    uniform_superposition, grover_iterate, measure
)


def closed_form_grover(N: int, k: int, r: int) -> float:
    """Theoretical single-run success prob for r Grover iterations on N with k marked."""
    theta = math.asin(math.sqrt(k / N))
    amp_marked = math.sin((2 * r + 1) * theta)
    return amp_marked ** 2


def empirical(N, k, r, trials=2000, seed=0):
    rng = random.Random(seed)
    n_qubits = int(round(math.log2(N)))
    assert (1 << n_qubits) == N
    marked_indices = rng.sample(range(N), k)
    mask = np.zeros(N, dtype=bool)
    for i in marked_indices:
        mask[i] = True
    hits = 0
    for _ in range(trials):
        s = uniform_superposition(n_qubits)
        s = grover_iterate(s, mask, r)
        idx = measure(s, rng)
        if mask[idx]:
            hits += 1
    return hits / trials


def main():
    print(f"{'N':>4} {'k':>3} {'r*':>4} {'closed':>8} {'empirical':>10} {'|diff|':>8}")
    rows = []
    for N in [16, 32, 64]:
        for k in [1, 2, 4, N // 2]:
            if k > N:
                continue
            r_star = round((math.pi / 4) * math.sqrt(N / k))
            if r_star < 1:
                r_star = 1
            cf = closed_form_grover(N, k, r_star)
            em = empirical(N, k, r_star, trials=2000)
            diff = abs(cf - em)
            print(f"{N:>4} {k:>3} {r_star:>4} {cf:>8.4f} {em:>10.4f} {diff:>8.4f}")
            rows.append({"N": N, "k": k, "r_star": r_star, "closed_form_prob": cf, "empirical_prob": em, "abs_diff": diff})
    with open("report/evidence/grover_sanity.json", "w") as f:
        json.dump({"rows": rows}, f, indent=2)
    print("[wrote] report/evidence/grover_sanity.json")


if __name__ == "__main__":
    main()
