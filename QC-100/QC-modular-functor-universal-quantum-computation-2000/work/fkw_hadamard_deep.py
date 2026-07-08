#!/usr/bin/env python3
"""Deeper Hadamard approximation search: BFS up to length 15 in B_3,
avoiding trivial cancellations, to demonstrate convergence toward
the target as braid length grows (universality-in-action).
"""
import math, cmath, time, json, os
import numpy as np
from fkw_replication import build_rep, gate_distance, q

def main():
    tabs, Es, sigmas = build_rep((2, 1))
    invs = [np.linalg.inv(S) for S in sigmas]
    dim = sigmas[0].shape[0]
    T = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)

    # Signed generators
    gens = [1, 2, -1, -2]

    # BFS with pruning + level-by-level best reporting.
    # State: matrix U (as tuple of complex rounded), last generator, depth
    # We iterate by length.
    frontier = [ (np.eye(dim, dtype=complex), []) ]
    best_by_length = {0: gate_distance(np.eye(dim, dtype=complex), T)}
    t0 = time.time()
    for depth in range(1, 16):
        new_frontier = []
        best_dist = 1e9
        best_word = None
        for U, w in frontier:
            for g in gens:
                if w and w[-1] == -g:
                    continue
                i = abs(g) - 1
                if g > 0:
                    Unew = sigmas[i] @ U
                else:
                    Unew = invs[i] @ U
                nw = w + [g]
                d = gate_distance(Unew, T)
                if d < best_dist:
                    best_dist = d; best_word = nw
                new_frontier.append((Unew, nw))
        frontier = new_frontier
        best_by_length[depth] = best_dist
        print(f"depth {depth:2d}  states={len(frontier):>7}  best_dist={best_dist:.5f}  word={best_word[:20]}{'...' if len(best_word)>20 else ''}")
        # Prune to avoid explosion: keep 400,000 max
        if len(frontier) > 400_000:
            print("  (pruning frontier)")
            # Keep those with distance to target in top half.
            frontier.sort(key=lambda x: gate_distance(x[0], T))
            frontier = frontier[:200_000]

    elapsed = time.time() - t0
    print(f"total elapsed {elapsed:.1f}s")

    outdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(outdir, "fkw_hadamard_deep.json"), "w") as f:
        json.dump({
            "best_by_length": {str(k): v for k, v in best_by_length.items()},
            "elapsed_seconds": elapsed,
        }, f, indent=2)

if __name__ == "__main__":
    main()
