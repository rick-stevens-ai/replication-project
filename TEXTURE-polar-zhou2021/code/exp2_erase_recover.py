"""
Claim 2 (small potential, narrow electrode): skyrmions under the electrode are
reversibly ERASED then RECOVERED after the field is removed. (paper Fig. 2)
Claim 3: skyrmions in the neighbouring region become ASYMMETRIC while the field
is on, and this asymmetric->symmetric transition is TOPOLOGICALLY PROTECTED
(local Q stays +1 for a surviving neighbouring bubble). (paper Fig. 2d,e)

Protocol:
  1. Build a skyrmion lattice, relax to equilibrium (field off).
  2. Count skyrmions under the electrode region (N_under_before).
  3. Apply a small potential V_small through a NARROW electrode; relax.
     -> expect skyrmions under electrode erased (N_under_field ~ 0),
        total Q drops.
  4. Check a surviving neighbouring bubble: its Pontryagin density line profile
     becomes single-peaked (asymmetric) while local Q ~ +1 (protected).
  5. Remove the field; relax. -> expect recovery (N_under_after > 0,
     total Q recovers toward the initial value).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from phasefield import (init_skyrmion_lattice, electrode_field, relax,
                        topological_charge, topological_charge_density,
                        pontryagin_density_continuous, default_params)

OUT = os.path.join(os.path.dirname(__file__), '..', 'work')
os.makedirs(OUT, exist_ok=True)

np.random.seed(0)
Nx = Ny = 120
Ps = 1.0
spacing = 22
R = 9.0
params = default_params()

P = init_skyrmion_lattice(Nx, Ny, spacing, R, Ps, bg_pol=-1)
Ezero = np.zeros((Ny, Nx, 3))
# equilibrate
P = relax(P, params, Ezero, nsteps=400, dt=0.02, L=1.0)
Q0 = topological_charge(P)

def count_under_electrode(P, d0):
    """Count skyrmions (positive q clusters) whose centre lies under electrode."""
    q = topological_charge_density(P)  # (Ny-1,Nx-1)
    Q_local = q.sum() / (4 * np.pi)
    xc = q.shape[1] / 2.0
    x = np.arange(q.shape[1])[None, :] - xc
    xg = np.broadcast_to(x, q.shape)
    under = np.abs(xg) <= d0
    Q_under = q[under].sum() / (4 * np.pi)
    return Q_under

d0 = 12.0          # narrow electrode half-width (grid units)
V_small = 3.0      # small potential (reduced units)

Q_under_before = count_under_electrode(P, d0)

# ---- apply small field ----
Efield = electrode_field(Nx, Ny, params, V_small, d0)
P_field = relax(P.copy(), params, Efield, nsteps=1500, dt=0.02, L=1.0)
Q_field = topological_charge(P_field)
Q_under_field = count_under_electrode(P_field, d0)

# ---- inspect a neighbouring surviving bubble for asymmetry ----
# pick region just outside the electrode edge
q_field = pontryagin_density_continuous(P_field)
edge_x = int(Nx / 2 + d0 + R)          # just right of electrode
band = slice(max(0, edge_x - 2*int(R)), min(Nx, edge_x + 2*int(R)))
# find the row with max |q| in that band => a bubble centre
sub = np.abs(q_field[:, band])
by = np.unravel_index(np.argmax(sub), sub.shape)[0]
line_neighbor = q_field[by, band]
from scipy.signal import find_peaks
al = np.abs(line_neighbor)
pk, _ = find_peaks(al, height=0.3*al.max(), distance=3) if al.max() > 0 else (np.array([]), None)
neighbor_single_peak = (len(pk) == 1)
# local topological charge of that neighbouring bubble window
win_y = slice(max(0, by-int(R)-2), min(q_field.shape[0], by+int(R)+2))
Pwin = P_field[win_y, band, :]
Q_neighbor = topological_charge(Pwin)

# ---- remove field, relax (recovery) ----
P_recover = relax(P_field.copy(), params, Ezero, nsteps=2500, dt=0.02, L=1.0)
Q_recover = topological_charge(P_recover)
Q_under_recover = count_under_electrode(P_recover, d0)

erased = (Q_under_field < 0.4 * Q_under_before)          # strong drop under electrode
recovered = (Q_under_recover > 0.6 * Q_under_before)     # substantial recovery
total_recovered = (abs(Q_recover) > 0.7 * abs(Q0))

result = dict(
    claim="small V / narrow electrode: reversible erase+recover; neighbour asymmetric but Q protected",
    Q0_total=round(Q0, 3),
    Q_under_before=round(Q_under_before, 3),
    Q_under_field=round(Q_under_field, 3),
    Q_under_recover=round(Q_under_recover, 3),
    Q_field_total=round(Q_field, 3),
    Q_recover_total=round(Q_recover, 3),
    erased_under_electrode=bool(erased),
    recovered_under_electrode=bool(recovered),
    total_charge_recovered=bool(total_recovered),
    neighbor_line_n_peaks=int(len(pk)),
    neighbor_asymmetric_single_peak=bool(neighbor_single_peak),
    neighbor_local_Q=round(Q_neighbor, 3),
    neighbor_Q_protected_near_1=bool(abs(round(Q_neighbor)) == 1),
)
np.save(os.path.join(OUT, 'exp2_P0.npy'), P)
np.save(os.path.join(OUT, 'exp2_Pfield.npy'), P_field)
np.save(os.path.join(OUT, 'exp2_Precover.npy'), P_recover)
with open(os.path.join(OUT, 'exp2_result.json'), 'w') as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
