#!/usr/bin/env python3
"""Retest DRY case at a shorter t_end so the wet-dry front hasn't
propagated too far — checks whether the sub-first-order convergence
is a wet-dry artifact vs. a solver bug.
"""
import math
from dambreak_1d import solve_dambreak, ritter_dry, L1_error

hl, hr, x0, L = 0.005, 0.0, 5.0, 10.0
c0 = math.sqrt(9.81 * hl)
# short time: wet-dry front travels 2*c0*t; pick t so front at ~0.5m past x0
t_short = 0.5 / (2.0 * c0)     # ~1.13 s
print(f"short t_end = {t_short:.4f} s (front reaches x = {x0 + 2*c0*t_short:.2f} m)")

prev_L1 = None
prev_dx = None
for N in [100, 1000, 10000]:
    x, h, hu, t = solve_dambreak(N, hl, hr, L=L, x0=x0, t_end=t_short)
    h_ana, u_ana = ritter_dry(x, t, hl, x0)
    l1h = L1_error(h, h_ana, L / N)
    dx = L / N
    R = None
    if prev_L1 is not None:
        R = math.log(prev_L1 / l1h) / math.log(prev_dx / dx)
    print(f"  N={N:>6d}  t={t:.4f}s  L1(h)={l1h:.3e}" +
          (f"  R(h)={R:.3f}" if R is not None else ""))
    prev_L1, prev_dx = l1h, dx
