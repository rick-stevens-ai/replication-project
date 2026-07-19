"""
Claim 4 (high potential, wide electrode): skyrmion -> labyrinthine/stripe
domain; the topological charge transition +1 -> 0 occurs BEFORE full bubble
destruction (a bubble develops alternating +/- Pontryagin density, net Q ~ 0,
while still visibly a bubble). Total skyrmion number drops and does NOT recover.
(paper Fig. 3)

Claim 5 (dielectric): as skyrmions shrink/burst under increasing field, the
local dielectric permittivity underneath the electrode DECREASES (paper Fig 4h;
absolute value ~650 and 80% reduction are OUT OF SCOPE -- need full multiphysics
-- but the MONOTONIC DECREASE with field is checkable). We compute a reduced
"local permittivity" proxy eps ~ d<Pz>/dEz + eps_b under the electrode as a
function of applied V, and check it decreases as skyrmions are erased.

Also compares recovery under small vs large field (paper Fig 3i): small field ->
total Q recovers; large field/wide electrode -> total Q stays suppressed.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from phasefield import (init_skyrmion_lattice, electrode_field, relax,
                        topological_charge, topological_charge_density,
                        pontryagin_density_continuous, default_params)

OUT = os.path.join(os.path.dirname(__file__), '..', 'work')
os.makedirs(OUT, exist_ok=True)

np.random.seed(1)
Nx = Ny = 120
Ps = 1.0
spacing = 22
R = 9.0
params = default_params()
Ezero = np.zeros((Ny, Nx, 3))

P0 = init_skyrmion_lattice(Nx, Ny, spacing, R, Ps, bg_pol=-1)
P0 = relax(P0, params, Ezero, nsteps=400, dt=0.02, L=1.0)
Q0 = topological_charge(P0)

def stripe_metric(P):
    """
    Labyrinthine/stripe order: fraction of in-plane power in a single dominant
    in-plane wavevector orientation (stripes = anisotropic FFT), plus mean |Pxy|.
    Higher anisotropy => more stripe-like/labyrinthine than a bubble lattice.
    """
    Pxy = np.hypot(P[..., 0], P[..., 1])
    F = np.abs(np.fft.fftshift(np.fft.fft2(P[..., 2] - P[..., 2].mean())))**2
    ny, nx = F.shape
    cy, cx = ny//2, nx//2
    F[cy, cx] = 0
    # angular anisotropy of the power spectrum
    yy, xx = np.mgrid[0:ny, 0:nx]
    ang = np.arctan2(yy-cy, xx-cx)
    rmask = (np.hypot(yy-cy, xx-cx) > 3)
    # bin power by angle, measure concentration
    bins = np.linspace(-np.pi, np.pi, 37)
    hist = np.array([F[rmask & (ang>=bins[i]) & (ang<bins[i+1])].sum()
                     for i in range(len(bins)-1)])
    aniso = hist.max()/(hist.mean()+1e-12)
    return dict(aniso=float(aniso), mean_Pxy=float(Pxy.mean()))

# --- high field, wide electrode ---
d0_wide = 30.0
V_high = 7.0
E_high = electrode_field(Nx, Ny, params, V_high, d0_wide)
P_high = relax(P0.copy(), params, E_high, nsteps=2500, dt=0.02, L=1.0)
Q_high = topological_charge(P_high)
P_high_recover = relax(P_high.copy(), params, Ezero, nsteps=3000, dt=0.02, L=1.0)
Q_high_recover = topological_charge(P_high_recover)
sm0 = stripe_metric(P0)
smH = stripe_metric(P_high_recover)

# --- small field, narrow electrode (recovery comparison) ---
d0_narrow = 12.0
V_low = 3.0
E_low = electrode_field(Nx, Ny, params, V_low, d0_narrow)
P_low = relax(P0.copy(), params, E_low, nsteps=1500, dt=0.02, L=1.0)
P_low_recover = relax(P_low.copy(), params, Ezero, nsteps=2500, dt=0.02, L=1.0)
Q_low_recover = topological_charge(P_low_recover)

# Claim 3i: small recovers, large does not
small_recovers = abs(Q_low_recover) > 0.7*abs(Q0)
large_suppressed = abs(Q_high_recover) < 0.6*abs(Q0)

# --- Claim 4: local bubble reaches Q~0 before destruction ---
# during high-field ramp, snapshot a bubble at edge and track its local Q
# take an intermediate high-field state (before full stripe formation)
P_mid = relax(P0.copy(), params, E_high, nsteps=500, dt=0.02, L=1.0)
q_mid = pontryagin_density_continuous(P_mid)
# search windows across the plane for a bubble with BOTH strong +q and -q lobes
# (alternating +/- => net ~0) while still localized
best = None
win = int(R)+3
for cy in range(win, Ny-win, 6):
    for cx in range(win, Nx-win, 6):
        w = q_mid[cy-win:cy+win, cx-win:cx+win]
        pos = w[w>0].sum(); neg = -w[w<0].sum()
        if pos+neg < 1e-6: continue
        net = (pos-neg)
        # localized bubble: significant magnitude, near-cancelling lobes
        mixing = min(pos,neg)/(max(pos,neg)+1e-12)
        score = mixing*(pos+neg)
        if (best is None or score > best['score']):
            Pw = P_mid[cy-win:cy+win, cx-win:cx+win, :]
            best = dict(score=float(score), pos=float(pos/(4*np.pi)),
                        neg=float(neg/(4*np.pi)), netQ=float(net/(4*np.pi)),
                        mixing=float(mixing), cy=cy, cx=cx)
partial_Q0_bubble = bool(best is not None and best['mixing']>0.4
                         and abs(best['netQ'])<0.5 and (best['pos']>0.15))

# --- Claim 5: dielectric proxy vs field ---
eps_b = 40.0   # background dielectric (paper: k_ij = 40)
Vs = [0.0, 1.5, 3.0, 4.5, 6.0, 7.5]
xc = Nx/2.0
xg = np.broadcast_to(np.arange(Nx)[None,:]-xc, (Ny,Nx))
under = np.abs(xg) <= d0_narrow
eps_list = []
dV = 0.4
for V in Vs:
    Ea = electrode_field(Nx, Ny, params, V, d0_narrow)
    Pa = relax(P0.copy(), params, Ea, nsteps=1200, dt=0.02, L=1.0)
    Eb = electrode_field(Nx, Ny, params, V+dV, d0_narrow)
    Pb = relax(Pa.copy(), params, Eb, nsteps=250, dt=0.02, L=1.0)
    dPz = (Pb[...,2]-Pa[...,2])[under].mean()
    dEz = (Eb[...,2]-Ea[...,2])[under].mean()
    eps = abs(dPz/ (dEz+1e-12)) + eps_b if abs(dEz)>1e-9 else eps_b
    # also skyrmion area proxy under electrode
    sky_area = float((np.abs(topological_charge_density(Pa))[:, :]).sum())
    eps_list.append(dict(V=V, eps=float(eps), sky_area=sky_area))

eps_vals = [e['eps'] for e in eps_list]
eps_monotonic_decrease = all(eps_vals[i] >= eps_vals[i+1]-1e-6 for i in range(len(eps_vals)-1))
eps_net_drop = eps_vals[0] > eps_vals[-1]

result = dict(
    claim="high V/wide electrode -> labyrinthine, Q suppressed & unrecovered; Q+1->0 before destruction; dielectric drops with field",
    Q0=round(Q0,3),
    Q_high_field=round(Q_high,3),
    Q_high_recover=round(Q_high_recover,3),
    Q_low_recover=round(Q_low_recover,3),
    small_field_recovers=bool(small_recovers),
    large_field_stays_suppressed=bool(large_suppressed),
    stripe_aniso_initial=round(sm0['aniso'],3),
    stripe_aniso_after_high=round(smH['aniso'],3),
    stripe_order_increased=bool(smH['aniso']>sm0['aniso']),
    partial_bubble_netQ=(round(best['netQ'],3) if best else None),
    partial_bubble_mixing=(round(best['mixing'],3) if best else None),
    Q_plus1_to_0_before_destruction=bool(partial_Q0_bubble),
    dielectric_vs_V=[{k:(round(v,3) if isinstance(v,float) else v) for k,v in e.items()} for e in eps_list],
    dielectric_monotonic_decrease=bool(eps_monotonic_decrease),
    dielectric_net_drop=bool(eps_net_drop),
)
np.save(os.path.join(OUT,'exp3_P_high_recover.npy'), P_high_recover)
np.save(os.path.join(OUT,'exp3_P_low_recover.npy'), P_low_recover)
with open(os.path.join(OUT,'exp3_result.json'),'w') as f:
    json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
