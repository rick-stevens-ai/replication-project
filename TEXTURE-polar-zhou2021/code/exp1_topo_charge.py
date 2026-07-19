"""
Claim 1: A single symmetric polar skyrmion bubble carries topological charge
Q = +1, and its Pontryagin density forms a RING (two peaks on a line profile
through the centre) -- paper Fig. 1(d,e).

We build a single analytic Neel skyrmion, relax it under the phase-field
dynamics (no field), and verify:
  (a) Q rounds to exactly +1,
  (b) the continuous Pontryagin density q(x,y) is a ring (radial profile
      peaks at intermediate r, ~0 at core and far field),
  (c) a horizontal line profile through the centre has TWO symmetric peaks.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from phasefield import (neel_skyrmion, topological_charge,
                        pontryagin_density_continuous, dF_dP, relax,
                        default_params)

OUT = os.path.join(os.path.dirname(__file__), '..', 'work')
os.makedirs(OUT, exist_ok=True)

Nx = Ny = 81
Ps = 1.0
R = 16.0
params = default_params()

# single skyrmion on down background
P = np.zeros((Ny, Nx, 3)); P[..., 2] = -1.0
sky, mask = neel_skyrmion(Nx, Ny, Nx/2, Ny/2, R, Ps, pol=+1, chir=+1)
P[mask] = sky[mask]
mag = np.linalg.norm(P, axis=-1, keepdims=True); P = P / mag * Ps

Q_init = topological_charge(P)

# relax a little (no field) so it settles to the model's own bubble
Ezero = np.zeros((Ny, Nx, 3))
P = relax(P, params, Ezero, nsteps=300, dt=0.02, L=1.0)
Q_relaxed = topological_charge(P)

q = pontryagin_density_continuous(P)
# radial profile of |q|
yc, xc = Ny // 2, Nx // 2
yy, xx = np.mgrid[0:Ny, 0:Nx]
rr = np.sqrt((xx - xc) ** 2 + (yy - yc) ** 2)
rbins = np.arange(0, R + 8, 1.0)
qr = np.array([q[(rr >= rbins[i]) & (rr < rbins[i + 1])].mean()
               if np.any((rr >= rbins[i]) & (rr < rbins[i + 1])) else 0.0
               for i in range(len(rbins) - 1)])
r_peak = rbins[np.argmax(np.abs(qr))]
ring_is_ring = (0.15 * R < r_peak < 0.95 * R) and (abs(qr[0]) < 0.5 * np.max(np.abs(qr)))

# horizontal line profile through centre: count peaks
line = q[yc, :]
# smooth + find local maxima of |line|
from scipy.signal import find_peaks
absline = np.abs(line)
peaks, _ = find_peaks(absline, height=0.2 * absline.max(), distance=4)
two_peaks = len(peaks) == 2

result = dict(
    claim="Q=+1 symmetric skyrmion, Pontryagin density is a ring w/ two-peak line profile",
    Q_init=round(Q_init, 4),
    Q_relaxed=round(Q_relaxed, 4),
    Q_rounds_to_plus1=bool(round(Q_relaxed) == 1),
    ring_peak_radius=float(r_peak),
    R=float(R),
    ring_structure_confirmed=bool(ring_is_ring),
    n_line_peaks=int(len(peaks)),
    two_symmetric_peaks=bool(two_peaks),
    line_peak_positions=[int(p) for p in peaks],
)
np.save(os.path.join(OUT, 'exp1_P.npy'), P)
np.save(os.path.join(OUT, 'exp1_q.npy'), q)
with open(os.path.join(OUT, 'exp1_result.json'), 'w') as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
