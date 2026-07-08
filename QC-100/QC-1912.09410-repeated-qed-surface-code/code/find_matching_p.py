#!/usr/bin/env python3
"""
Find the effective depolarizing p that reproduces the paper's headline number:
   p_s(N=10) ~ 6e-4  (their master-equation sim value, per Fig 5(c) caption/text)
by running additional Stim shots at larger p.  Also emit a summary comparison.
"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import numpy as np
from sim_repeated_qed import build_circuit

def measure(p, R=10, shots=200000, basis="Z"):
    c = build_circuit(R, p, basis)
    s = c.compile_detector_sampler(seed=int(1_000_000*p)+123)
    det, obs = s.sample(shots=shots, separate_observables=True)
    success = ~det.any(axis=1)
    ps = success.mean()
    return ps, det.mean(), obs[success].mean() if success.any() else float("nan"), int(success.sum())

points = []
for p in [0.012, 0.015, 0.018, 0.020, 0.025, 0.030, 0.035, 0.040]:
    ps, drate, lerr_post, ns = measure(p, R=10, shots=200000, basis="Z")
    print(f"p={p:.4f}  p_s(10)={ps:.4g}   det_rate={drate:.4g}  logerr_postsel={lerr_post}  ps_shots={ns}", flush=True)
    points.append(dict(p=p, R=10, p_s_10=ps, det_rate=drate, logerr_postsel=float(lerr_post), ps_shots=ns))

with open("report/evidence/matching_p_sweep.json","w") as f:
    json.dump(points, f, indent=2)
