#!/usr/bin/env python3
"""Demonstrate the quadratic speedup: for complete binary trees of increasing
depth, count actual classical query cost (edges visited by exhaustive DFS
enumeration; the ONLY way to *exactly* determine T when the tree is unknown)
and compare with the theoretical quantum leading-order cost.

Classical lower bound for exact tree-size on an unknown tree: Omega(T).
    (Adversary hides an unexplored edge -> can flip T by 1 arbitrarily.)
    Fully counting T requires visiting every edge, so classical = T queries.

Quantum (Ambainis-Kokainis Theorem 2, up to sub-poly factors):
    Q = c * sqrt(n T) / delta^{1.5}
for constant delta (say 0.3) and small constant c ~ O(1). Setting c=1 for the
leading behavior we illustrate: speedup ~ sqrt(T/n) which is quadratic in T
when depth n grows slower than T (which is the case for wide trees where
n = O(log T)).

We also fit the observed theta_min ~ 1/sqrt(nT) which is the key phase-gap
lemma from the paper (Lemma 15 / Theorem 12 area).
"""
import math
import json
import numpy as np
from tree_size_estimation import make_complete_binary_tree, build_operators


def theta_min_of_tree(depth, delta=0.3):
    edges, par, dep, V = make_complete_binary_tree(depth)
    T = len(edges); n = depth
    alpha = math.sqrt(2 * n) / delta
    R_A, R_B, dim = build_operators(edges, par, dep, V, alpha)
    U = R_B @ R_A
    w, _ = np.linalg.eig(U)
    absth = np.abs(np.angle(w))
    return float(np.min(absth[absth > 1e-10])), T, n, alpha, dim


print(f"{'depth':>5} {'T':>6} {'dim':>6} {'alpha':>10} {'theta_min':>12} {'sqrt(nT) estimate for theta_min':>32}")
rows = []
for depth in range(1, 8):  # depth 7 -> dim 255, still fast
    tm, T, n, alpha, dim = theta_min_of_tree(depth)
    # Paper implies theta_min ~ C / (alpha * sqrt(T))  (rearranging the identity)
    # since T = 1/(alpha^2 sin^2(theta/2)) => sin(theta/2) = 1/(alpha sqrt(T))
    # => theta ~ 2/(alpha sqrt(T)) for small theta
    # => theta ~ 2/(sqrt(2n)/delta * sqrt(T)) = 2 delta / sqrt(2 n T) ~ 1/sqrt(nT)
    theoretical = 2.0 * 0.3 / math.sqrt(2 * n * T)
    rows.append({
        "depth": depth, "T_edges": T, "dim_H": dim,
        "alpha": alpha, "theta_min_measured": tm,
        "theta_min_theory_leading": theoretical,
        "ratio_measured_over_theory": tm / theoretical,
    })
    print(f"{depth:>5} {T:>6} {dim:>6} {alpha:>10.4f} {tm:>12.6f} {theoretical:>18.6f}   ratio={tm/theoretical:.4f}")

# Classical vs quantum query complexity across depths (theoretical + regression)
print(f"\n{'depth':>5} {'T':>8} {'classical':>10} {'quantum_lead':>14} {'speedup':>10}")
comp_rows = []
for depth in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
    T = 2**(depth+1) - 2
    classical = T
    quantum = math.sqrt(depth * T) / (0.3 ** 1.5)
    comp_rows.append({
        "depth": depth, "T_edges": T,
        "classical_queries": classical, "quantum_leading": quantum,
        "speedup_ratio": classical / quantum,
    })
    print(f"{depth:>5} {T:>8} {classical:>10.0f} {quantum:>14.2f} {classical/quantum:>10.2f}x")

import pathlib
pathlib.Path(__file__).with_name("quadratic_speedup.json").write_text(json.dumps({
    "phase_gap": rows, "complexity": comp_rows
}, indent=2))
print("\nJSON saved: quadratic_speedup.json")

# Sanity: log-log fit of measured theta_min against T (with n=depth) to confirm
# theta_min ~ T^{-1/2} scaling
import numpy as np
Ts = np.array([r["T_edges"] for r in rows])
tms = np.array([r["theta_min_measured"] for r in rows])
ns = np.array([r["depth"] for r in rows])
# Regress log(theta_min) on log(sqrt(nT))
x = 0.5 * np.log(ns * Ts)
y = np.log(tms)
# Slope should be -1
A = np.vstack([x, np.ones_like(x)]).T
slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
print(f"\nlog-log fit of theta_min vs sqrt(nT): slope={slope:.4f} (paper predicts -1)")
print(f"intercept = {intercept:.4f} => constant factor = exp(intercept) = {math.exp(intercept):.4f}")
