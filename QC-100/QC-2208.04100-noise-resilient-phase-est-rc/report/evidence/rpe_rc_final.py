"""
Final well-designed sweep. Key insight: we need noise angles where
  (a) the bare bias eps*L is still in the linear regime for our chosen Lmax
      (so no phase-wrap aliasing:  2*(phi + eps/2)*Lmax stays inside a coherent branch),
  (b) RC's residual is above the shot-noise floor (~1/sqrt(Ns*Nr)).

For Lmax=100 and phi_true~0.37, aliasing kicks in when 2*eps*Lmax approaches 2*pi,
i.e. eps ~ pi/Lmax ~ 0.031. So we must LOWER Lmax OR restrict eps to a moderate range.

Strategy: use Lmax=32 (bare aliasing threshold now eps ~ pi/32 ~ 0.098), high shots
+ high Nr to drive the RC floor down, and sweep eps in a decade where both slopes are
measurable.
"""

import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpe_rc
import numpy as np

# ---- overrides ----
rpe_rc.L_LIST         = [1, 2, 4, 8, 16, 32]
rpe_rc.NOISE_ANGLES   = [0.006, 0.010, 0.015, 0.025, 0.040, 0.060]
rpe_rc.NS_PER_CIRCUIT = 20000
rpe_rc.NR             = 80

# also widen phi search a bit
_orig = rpe_rc.estimate_phi_from_curve
def wider(L_list, p0_list):
    p0 = np.array(p0_list)
    L  = np.array(L_list, dtype=float)
    phis = np.linspace(rpe_rc.PHI_TRUE - 0.3, rpe_rc.PHI_TRUE + 0.3, 60001)
    best = None
    for phi in phis:
        pred = (1 + np.cos(2*phi*L))/2
        err = float(np.sum((p0 - pred)**2))
        if best is None or err < best[0]:
            best = (err, float(phi))
    return best[1]
rpe_rc.estimate_phi_from_curve = wider

if __name__ == "__main__":
    rpe_rc.main()
