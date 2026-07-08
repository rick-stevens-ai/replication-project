"""
Follow-up run at STRONGER coherent-noise angles so RC-mitigated error rises
above the shot-noise floor and its power-law slope becomes measurable.

Paper's Fig 3(a): unmitigated ~theta^1.04, mitigated ~theta^2.73 in the
STRONG-noise regime. Weak-noise regime is Nr-limited (~1/sqrt(Nr)).
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpe_rc

# override globals
rpe_rc.NOISE_ANGLES   = [0.05, 0.10, 0.20, 0.30, 0.50, 0.80]
rpe_rc.NS_PER_CIRCUIT = 8000
rpe_rc.NR             = 40    # more compilations -> lower stochastic residual

# widen the phi search window since strong noise pushes bare phi_est far
_orig_est = rpe_rc.estimate_phi_from_curve
def wide_estimator(L_list, p0_list):
    import numpy as np
    p0 = np.array(p0_list)
    L  = np.array(L_list, dtype=float)
    phis = np.linspace(rpe_rc.PHI_TRUE - 1.0, rpe_rc.PHI_TRUE + 1.0, 40001)
    best = None
    for phi in phis:
        pred = (1 + np.cos(2*phi*L))/2
        err = float(np.sum((p0 - pred)**2))
        if best is None or err < best[0]:
            best = (err, float(phi))
    return best[1]
rpe_rc.estimate_phi_from_curve = wide_estimator

if __name__ == "__main__":
    rpe_rc.main()
