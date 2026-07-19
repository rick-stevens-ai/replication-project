"""Generate figures for the replication report."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from phasefield import pontryagin_density_continuous

W = os.path.join(os.path.dirname(__file__), '..', 'work')
F = os.path.join(os.path.dirname(__file__), '..', 'figs')
os.makedirs(F, exist_ok=True)

def show_P(ax, P, title, step=4):
    Pz = P[..., 2]
    ax.imshow(Pz, cmap='RdBu_r', origin='lower', vmin=-1, vmax=1)
    Ny, Nx = Pz.shape
    ys, xs = np.mgrid[0:Ny:step, 0:Nx:step]
    ax.quiver(xs, ys, P[::step, ::step, 0], P[::step, ::step, 1],
              color='k', scale=25, width=0.002)
    ax.set_title(title, fontsize=9); ax.set_xticks([]); ax.set_yticks([])

# Fig A: single skyrmion + Pontryagin ring (exp1)
P1 = np.load(os.path.join(W, 'exp1_P.npy'))
q1 = np.load(os.path.join(W, 'exp1_q.npy'))
fig, ax = plt.subplots(1, 3, figsize=(11, 3.4))
show_P(ax[0], P1, 'Symmetric skyrmion (Pz + in-plane vec)')
im = ax[1].imshow(q1, cmap='seismic', origin='lower'); ax[1].set_title('Pontryagin density q (ring), Q=+1', fontsize=9)
ax[1].set_xticks([]); ax[1].set_yticks([]); plt.colorbar(im, ax=ax[1], fraction=0.046)
ax[2].plot(q1[q1.shape[0]//2, :]); ax[2].set_title('Line profile through centre (2 peaks)', fontsize=9)
ax[2].set_xlabel('x'); ax[2].set_ylabel('q')
plt.tight_layout(); plt.savefig(os.path.join(F, 'figA_single_skyrmion.png'), dpi=110); plt.close()

# Fig B: erase/recover (exp2)
P0 = np.load(os.path.join(W, 'exp2_P0.npy'))
Pf = np.load(os.path.join(W, 'exp2_Pfield.npy'))
Pr = np.load(os.path.join(W, 'exp2_Precover.npy'))
fig, ax = plt.subplots(1, 3, figsize=(11, 3.6))
show_P(ax[0], P0, 'Initial skyrmion lattice')
show_P(ax[1], Pf, 'Small V ON: erased under electrode')
show_P(ax[2], Pr, 'V OFF: recovered')
for a in ax:
    a.axvline(P0.shape[1]/2-12, color='lime', ls='--', lw=1)
    a.axvline(P0.shape[1]/2+12, color='lime', ls='--', lw=1)
plt.tight_layout(); plt.savefig(os.path.join(F, 'figB_erase_recover.png'), dpi=110); plt.close()

# Fig C: high vs low recovery (exp4)
Ps = np.load(os.path.join(W, 'exp4_Psmall_off.npy'))
Pl = np.load(os.path.join(W, 'exp4_Plarge_off.npy'))
fig, ax = plt.subplots(1, 2, figsize=(8, 3.8))
show_P(ax[0], Ps, 'Small V off: skyrmions recovered')
show_P(ax[1], Pl, 'Large V off: labyrinthine locked in')
plt.tight_layout(); plt.savefig(os.path.join(F, 'figC_recovery_asymmetry.png'), dpi=110); plt.close()

# Fig D: dielectric vs V (exp3)
import json
d = json.load(open(os.path.join(W, 'exp3_result.json')))
dv = d['dielectric_vs_V']
Vs = [e['V'] for e in dv]; eps = [e['eps'] for e in dv]; area = [e['sky_area'] for e in dv]
fig, ax1 = plt.subplots(figsize=(5.5, 4))
ax1.plot(Vs, eps, 'o-', color='C0'); ax1.set_xlabel('Applied V (reduced)')
ax1.set_ylabel('Local permittivity proxy', color='C0')
ax2 = ax1.twinx(); ax2.plot(Vs, area, 's--', color='C3')
ax2.set_ylabel('Skyrmion area proxy', color='C3')
ax1.set_title('Dielectric proxy & skyrmion area decrease with field')
plt.tight_layout(); plt.savefig(os.path.join(F, 'figD_dielectric.png'), dpi=110); plt.close()

print("figures written:", os.listdir(F))
