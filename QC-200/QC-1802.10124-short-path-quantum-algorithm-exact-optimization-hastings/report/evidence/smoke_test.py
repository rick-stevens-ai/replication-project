#!/usr/bin/env python3
"""Quick smoke test at N=6 to verify short_path_sim mechanics."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from short_path_sim import (
    random_maxk2_instance, random_sk_instance, analyze_instance
)
import numpy as np, time

rng = np.random.default_rng(20260705)
J, h = random_maxk2_instance(6, rng)
print("Instance J[0,1]=", J[0,1])
t=time.time()
res = analyze_instance(6, J, h, K_values=[3,5], b_values=[0.3, 0.6, 0.9])
print(f"analyze N=6 took {time.time()-t:.2f}s")
for r in res:
    print(f"K={r['K']} b={r['b']}: P_ov={r['P_ov_plus_psi01']:.4f} min_gap={r['min_gap']:.4f} "
          f"eff_short={r['eff_queries_short']:.3f} eff_grover={r['eff_queries_grover']:.3f} "
          f"ratio={r['ratio_short_over_grover']:.4f} #gs={r['num_ground_states']}")
