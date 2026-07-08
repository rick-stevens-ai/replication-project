#!/usr/bin/env python3
"""
Second key finding of Childs et al. 2018 (arXiv:1711.10980):
  Empirical Trotter error is MUCH smaller than the analytical worst-case bound.
  This is why "higher-order product formulas prevail if empirical error
  estimates suffice" -- the rigorous bounds drastically over-estimate the
  resources needed.

Here we compare, for PF1 (first-order Lie-Trotter), the measured spectral-norm
error against the standard analytical worst-case commutator bound:

    ||U_exact - U_PF1||  <=  (t^2 / 2r) * sum_{i<j} || [H_i, H_j] ||

(This is the textbook first-order Trotter bound; the paper develops tighter
variants but the point is the same: the a-priori bound is orders of magnitude
looser than the observed error.)
"""
import numpy as np
from scipy.linalg import expm
import json, os
from trotter_error import (build_terms, total_H, pf1, spectral_error, I2, X, Y, Z)

np.random.seed(20260702)

def main():
    n = 6; h = 1.0; t = 1.0
    h_field = np.random.uniform(-h, h, size=n)
    terms = build_terms(n, h_field)
    H = total_H(terms)
    U_exact = expm(-1j * H * t)

    # analytical commutator sum
    comm_sum = 0.0
    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            c = terms[i] @ terms[j] - terms[j] @ terms[i]
            comm_sum += np.linalg.norm(c, ord=2)

    print(f"sum_{{i<j}} ||[H_i,H_j]||_2 = {comm_sum:.4f}")
    print()
    print(f"{'r':>5} {'empirical':>14} {'bound (t^2/2r * S)':>20} {'bound/empirical':>16}")
    rows = []
    for r in [1, 2, 4, 8, 16, 32, 64, 128]:
        emp = spectral_error(U_exact, pf1(terms, t, r))
        bound = (t ** 2) / (2 * r) * comm_sum
        ratio = bound / emp if emp > 0 else float('inf')
        print(f"{r:>5} {emp:>14.4e} {bound:>20.4e} {ratio:>16.1f}")
        rows.append({"r": r, "empirical": float(emp), "bound": float(bound),
                     "bound_over_empirical": float(ratio)})

    out = {"comm_sum": float(comm_sum), "rows": rows}
    p = os.path.join(os.path.dirname(__file__), "..", "results", "bound_vs_empirical.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {os.path.abspath(p)}")

if __name__ == "__main__":
    main()
