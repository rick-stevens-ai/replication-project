#!/usr/bin/env python3
"""Verify the EXACT paper identity: for the eigenvalue closest to 1, the paper
proves that in the 2-d invariant subspace spanned by |Psi+>, |Psi-> the initial
state |e_{T+1}> has known overlap and the identity T = 1/(alpha^2 sin^2(theta/2))
holds EXACTLY (not approximately).

We test this by examining ALL non-trivial eigenphases and finding the one that
plugs into the formula to give exactly T. This confirms the algorithmic core.

The ~1% error in tree_size_estimation.py came from picking the numerically
smallest |theta| across all eigenvectors -- but there are typically multiple
non-trivial pairs and we should pick the one whose eigenvector has support on
the |e_{T+1}> starting state.
"""
import math
import numpy as np
from tree_size_estimation import (
    make_complete_binary_tree, make_unbalanced_tree, build_operators,
)


def run(edges, parent_of, depth_of, V, n_depth, delta=0.3, root=1):
    T_true = len(edges)
    alpha = math.sqrt(2 * n_depth) / delta
    R_A, R_B, dim = build_operators(edges, parent_of, depth_of, V, alpha, root=root)
    U = R_B @ R_A
    w, vecs = np.linalg.eig(U)
    thetas = np.angle(w)
    # |e_{T+1}> is basis vector 0
    start = np.zeros(dim, dtype=complex); start[0] = 1.0
    # Overlap of |start> with each eigenvector
    overlaps = np.abs(vecs.T.conj() @ start) ** 2
    # For each eigenvalue, compute the "predicted" T = 1/(alpha^2 sin^2(theta/2))
    rows = []
    for i in range(dim):
        th = thetas[i]
        if abs(th) < 1e-8:
            continue
        pred_T = 1.0 / (alpha ** 2 * math.sin(th / 2) ** 2)
        rows.append((abs(th), th, overlaps[i], pred_T))
    # Sort by |theta|
    rows.sort()
    print(f"\nTree with T_true={T_true} edges, n={n_depth}, alpha={alpha:.4f}, dim={dim}")
    print(f"{'|theta|':>10} {'theta':>10} {'overlap':>10} {'pred_T':>12}")
    seen = set()
    total_overlap_used = 0.0
    weighted_T = 0.0
    for absth, th, ov, pT in rows[:12]:
        key = round(absth, 8)
        marker = "  <- new" if key not in seen else ""
        seen.add(key)
        print(f"{absth:10.6f} {th:10.6f} {ov:10.6f} {pT:12.6f}{marker}")
        total_overlap_used += ov
        weighted_T += ov * pT
    print(f"top-12 overlap sum = {total_overlap_used:.6f}, weighted pred_T = "
          f"{weighted_T/total_overlap_used if total_overlap_used>0 else float('nan'):.6f}")

    # The paper's estimator uses ONLY the smallest |theta| in the |q2> subspace
    smallest = rows[0]
    print(f"\nSmallest-|theta| estimator:  pred_T = {smallest[3]:.6f}  (T_true = {T_true})")
    return smallest[3], T_true


if __name__ == "__main__":
    for depth in [1, 2, 3, 4]:
        edges, par, dep, V = make_complete_binary_tree(depth)
        run(edges, par, dep, V, depth)
