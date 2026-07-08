"""Trace a few iterations of ChebAE to see what's happening."""
import numpy as np
from ae_algorithms import (T, _find_next_cheb, sample_Td_squared,
                            clopper_pearson, clopper_pearson_max_halfwidth,
                            _invert_TK_squared_interval)

rng = np.random.default_rng(123)
a_true = 0.5
epsilon = 1e-2
delta = 0.05
Nshots = 100
r = 2.0
nu = 8.0

import math
T_bound = max(1, int(np.ceil(math.log(1.0/max(2*epsilon, 1e-30), r))))
alpha_per_iter = delta / T_bound
eps_pmax = clopper_pearson_max_halfwidth(Nshots, alpha_per_iter)
print(f"T_bound={T_bound}, alpha/iter={alpha_per_iter:.4f}, eps_pmax={eps_pmax:.4f}")

amin, amax = 0.0, 1.0
nheads, nflips = 0, 0
d = 1
total = 0
for it in range(30):
    d_new = _find_next_cheb(amin, amax)
    reset = d_new >= r*d
    if reset:
        d = d_new
        nheads, nflips = 0, 0

    denom = abs(T(d, amax) - T(d, amin))
    late = False
    if denom > 1e-15:
        if eps_pmax * ((amax-amin)/denom) <= epsilon * nu:
            late = True

    n = 1 if late else Nshots
    h = sample_Td_squared(d, a_true, n, rng)
    nheads += h
    nflips += n
    total += n*d

    pmin, pmax = clopper_pearson(nheads, nflips, alpha_per_iter)
    new_amin, new_amax = _invert_TK_squared_interval(d, amin, amax, pmin, pmax)
    print(f"[{it:2d}] d={d:4d}  interval=[{amin:.5f},{amax:.5f}]  n={n:3d}  h/f={nheads}/{nflips}  p=[{pmin:.4f},{pmax:.4f}]  new=[{new_amin:.5f},{new_amax:.5f}]  Q={total}  late={late}")
    amin, amax = max(new_amin,amin), min(new_amax,amax)
    if amin>amax: amin,amax = new_amin,new_amax
    if amax-amin < 2*epsilon:
        print(f"CONVERGED at iter {it}: a_hat = {0.5*(amin+amax):.6f}  Q={total}")
        break
