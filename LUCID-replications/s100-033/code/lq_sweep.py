#!/usr/bin/env python3
"""Sweep (alpha, beta) to find the regime that reproduces the paper's
30.37% claim (Fig. 7a, first-fraction hypo-vs-hyper kill comparison).

40 Gy total, hyper = 5 fx (8 Gy/fx), hypo = 2 fx (20 Gy/fx).

For a single fraction with kill = 1 - exp(-(a D + b D^2)):
  kill_hypo (20 Gy)
  kill_hyper(8 Gy)
  excess = (kill_hypo - kill_hyper) / kill_hyper * 100 %
"""
import math
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "evidence", "lq_sweep.txt")

def excess(alpha, beta):
    k_hyper = 1 - math.exp(-(alpha * 8 + beta * 64))
    k_hypo  = 1 - math.exp(-(alpha * 20 + beta * 400))
    return (k_hypo - k_hyper) / k_hyper * 100.0, k_hyper, k_hypo

best = None
with open(OUT, "w") as f:
    f.write("LQ parameter sweep targeting paper's 30.37% claim\n")
    f.write("==================================================\n")
    f.write(f"{'alpha':>8} {'beta':>10} {'k_hyper%':>10} {'k_hypo%':>10} {'excess%':>10}\n")
    for alpha in np.linspace(0.005, 0.5, 25):
        for beta in [0.0, alpha / 100, alpha / 30, alpha / 10, alpha / 3]:
            try:
                ex, kh, ko = excess(alpha, beta)
            except OverflowError:
                continue
            f.write(f"{alpha:8.4f} {beta:10.5f} {kh*100:10.3f} {ko*100:10.3f} {ex:10.3f}\n")
            if best is None or abs(ex - 30.37) < abs(best[0] - 30.37):
                best = (ex, alpha, beta, kh, ko)
    f.write("\n")
    f.write(f"Closest match to 30.37%:\n")
    f.write(f"  alpha = {best[1]:.4f} 1/Gy\n")
    f.write(f"  beta  = {best[2]:.5f} 1/Gy^2\n")
    f.write(f"  k_hyper = {best[3]*100:.2f}%   k_hypo = {best[4]*100:.2f}%   excess = {best[0]:.2f}%\n")

print(f"Best LQ match: alpha={best[1]:.4f}, beta={best[2]:.5f}, excess={best[0]:.2f}%")
print(f"Wrote {OUT}")
