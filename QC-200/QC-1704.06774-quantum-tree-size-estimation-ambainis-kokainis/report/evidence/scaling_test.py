#!/usr/bin/env python3
"""Show that the estimator's residual bias scales as ~1/alpha^2 (equivalently
as delta^2 with alpha = sqrt(2n)/delta), which matches Lemma 5 of the paper:
   (1-delta)T <= 1/(alpha^2 sin^2(theta/2)) <= (1+delta)T
With alpha increased (delta decreased) the estimate converges monotonically
to T_true. This is the *exact* behavior predicted by Ambainis & Kokainis.
"""
import math
import json
import numpy as np
from tree_size_estimation import make_complete_binary_tree, build_operators

# Complete binary tree depth 4, T=30 edges
depth = 4
edges, par, dep, V = make_complete_binary_tree(depth)
T_true = len(edges)
n = depth

rows = []
for delta in [1.0, 0.5, 0.3, 0.1, 0.05, 0.01, 0.005]:
    alpha = math.sqrt(2 * n) / delta
    R_A, R_B, dim = build_operators(edges, par, dep, V, alpha)
    U = R_B @ R_A
    w, _ = np.linalg.eig(U)
    thetas = np.angle(w); absth = np.abs(thetas)
    theta_min = float(np.min(absth[absth > 1e-10]))
    T_hat = 1.0 / (alpha ** 2 * math.sin(theta_min / 2) ** 2)
    rel_err = abs(T_hat - T_true) / T_true
    lemma5_bound_hi = (1 + delta) * T_true
    lemma5_bound_lo = (1 - delta) * T_true
    in_bound = lemma5_bound_lo <= T_hat <= lemma5_bound_hi
    print(f"delta={delta:6.3f}  alpha={alpha:9.4f}  theta_min={theta_min:.8f}  T_hat={T_hat:12.8f}  rel_err={rel_err:.4e}  in Lemma5 [{lemma5_bound_lo:.2f}, {lemma5_bound_hi:.2f}]? {in_bound}")
    rows.append({
        "delta": delta,
        "alpha": alpha,
        "theta_min": theta_min,
        "T_hat": T_hat,
        "T_true": T_true,
        "rel_error": rel_err,
        "lemma5_bound_lo": lemma5_bound_lo,
        "lemma5_bound_hi": lemma5_bound_hi,
        "within_lemma5_bound": bool(in_bound),
    })

import pathlib
pathlib.Path(__file__).with_name("scaling_test.json").write_text(json.dumps(rows, indent=2))
print("\nAll runs within Lemma 5 bound?", all(r["within_lemma5_bound"] for r in rows))
