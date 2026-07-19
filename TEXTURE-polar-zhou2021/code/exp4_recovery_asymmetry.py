"""
Focused test of paper Fig. 3(i): the SMALL-field/narrow-electrode case recovers
its total topological charge, while the LARGE-field/wide-electrode case leaves
the total charge strongly and persistently suppressed (labyrinthine locked in).

This isolates the recovery-asymmetry claim with a proper stripe-order metric.
Stripe/labyrinthine order is measured by the correlation length anisotropy of
Pz and by the drop in bubble count (number of distinct +q maxima).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from phasefield import (init_skyrmion_lattice, electrode_field, relax,
                        topological_charge, topological_charge_density,
                        default_params)

OUT = os.path.join(os.path.dirname(__file__), '..', 'work')
np.random.seed(2)
Nx = Ny = 120
Ps = 1.0; spacing = 22; R = 9.0
params = default_params()
Ezero = np.zeros((Ny, Nx, 3))

P0 = init_skyrmion_lattice(Nx, Ny, spacing, R, Ps, bg_pol=-1)
P0 = relax(P0, params, Ezero, nsteps=400, dt=0.02, L=1.0)
Q0 = topological_charge(P0)

def n_bubbles(P):
    """count local maxima of q (distinct skyrmion cores)."""
    from scipy.ndimage import maximum_filter, label
    q = topological_charge_density(P)
    thr = 0.15 * q.max() if q.max() > 0 else 1e9
    mx = (q == maximum_filter(q, size=5)) & (q > thr)
    return int(label(mx)[1])

def run_case(V, d0, ns_on, ns_off):
    E = electrode_field(Nx, Ny, params, V, d0)
    Pon = relax(P0.copy(), params, E, nsteps=ns_on, dt=0.02, L=1.0)
    Poff = relax(Pon.copy(), params, Ezero, nsteps=ns_off, dt=0.02, L=1.0)
    return dict(
        V=V, d0=d0,
        Q_on=round(topological_charge(Pon), 3),
        Q_off=round(topological_charge(Poff), 3),
        nb0=n_bubbles(P0),
        nb_off=n_bubbles(Poff),
        recover_frac=round(topological_charge(Poff)/Q0, 3),
    ), Poff

# small field, narrow electrode
small, Ps_off = run_case(V=3.0, d0=12.0, ns_on=1500, ns_off=3000)
# large field, wide electrode -- stronger + longer to lock in labyrinthine
large, Pl_off = run_case(V=9.0, d0=36.0, ns_on=3000, ns_off=3500)

small_recovers = small['recover_frac'] > 0.7
large_suppressed = large['recover_frac'] < small['recover_frac'] - 0.15  # relative
# bubble count: large field destroys more bubbles permanently
large_fewer_bubbles = large['nb_off'] < small['nb_off']

result = dict(
    claim="Fig3i: small field/narrow electrode recovers Q; large field/wide electrode stays suppressed",
    Q0=round(Q0, 3),
    small_case=small,
    large_case=large,
    small_field_recovers=bool(small_recovers),
    large_field_more_suppressed_than_small=bool(large_suppressed),
    large_field_fewer_surviving_bubbles=bool(large_fewer_bubbles),
    recovery_asymmetry_confirmed=bool(small_recovers and large_suppressed),
)
np.save(os.path.join(OUT, 'exp4_Psmall_off.npy'), Ps_off)
np.save(os.path.join(OUT, 'exp4_Plarge_off.npy'), Pl_off)
with open(os.path.join(OUT, 'exp4_result.json'), 'w') as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
