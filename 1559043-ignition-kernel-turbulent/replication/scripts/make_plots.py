#!/usr/bin/env python3
"""Generate publication figures from simulation results."""
import numpy as np
import json, os, glob

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12,
    'figure.dpi': 150, 'savefig.dpi': 150, 'savefig.bbox': 'tight',
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(BASE, 'results')
FIG = os.path.join(BASE, 'figures')
os.makedirs(FIG, exist_ok=True)

with open(os.path.join(RES, 'results.json')) as f:
    data = json.load(f)

phis = [0.6, 0.8, 1.0, 1.2]
colors = {0.6: 'blue', 0.8: 'green', 1.0: 'orange', 1.2: 'red'}

# ---- Fig 1: Heat release rate history (cf. paper Fig 5) ----
fig, ax = plt.subplots(figsize=(8,5))
for phi in phis:
    for i, r in enumerate(data['results'][f'phi_{phi}']):
        t = np.array(r['t'])
        Q = np.array(r['Qdot'])
        Q_pos = np.maximum(Q, 1e-3)
        label = f'$\\phi={phi}$' if i==0 else None
        ax.plot(t, Q_pos, color=colors[phi], alpha=0.5 if i>0 else 1,
                ls='-' if i==0 else '--', label=label, lw=1.5 if i==0 else 0.8)
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Total Heat Release Rate (W/m)')
ax.set_title('Heat Release Rate Evolution\n(cf. Jaravel et al. 2019, Fig. 5)')
ax.legend(loc='upper right')
ax.set_xlim(0, 2); ax.set_yscale('log')
ax.set_ylim(1e-2, 1e3)
ax.grid(True, alpha=0.3)
fig.savefig(os.path.join(FIG, 'fig1_heat_release.png'))
plt.close(fig)
print("fig1_heat_release.png")

# ---- Fig 2: Max temperature history ----
fig, ax = plt.subplots(figsize=(8,5))
for phi in phis:
    for i, r in enumerate(data['results'][f'phi_{phi}']):
        t = np.array(r['t'])
        Tm = np.array(r['Tmax'])
        label = f'$\\phi={phi}$' if i==0 else None
        ax.plot(t, Tm, color=colors[phi], alpha=0.5 if i>0 else 1,
                ls='-' if i==0 else '--', label=label, lw=1.5 if i==0 else 0.8)
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Maximum Temperature (K)')
ax.set_title('Peak Temperature Evolution')
ax.legend()
ax.set_xlim(0, 2)
ax.axhline(y=456, color='gray', ls=':', alpha=0.5, label='$T_{in}$')
ax.grid(True, alpha=0.3)
fig.savefig(os.path.join(FIG, 'fig2_tmax.png'))
plt.close(fig)
print("fig2_tmax.png")

# ---- Fig 3: Ignition propensity (cf. paper Fig 7) ----
fig, ax = plt.subplots(figsize=(7,5))
P_exp = [0.05, 0.40, 0.60, 0.80]  # Experimental from Sforzo et al.
IP_means = [data['summary'][f'phi_{p}']['IP_mean'] for p in phis]
IP_stds = [data['summary'][f'phi_{p}']['IP_std'] for p in phis]

ax.errorbar(phis, IP_means, yerr=IP_stds, fmt='s-', color='red',
            markersize=8, capsize=5, label='This work (2D, coarse)')
ax.plot(phis, P_exp, 'o--', color='black', markersize=8,
        label='Experiment (Sforzo et al.)')
# Paper numerical (approximate)
IP_paper = [0.0, 0.5, 0.65, 0.85]
ax.plot(phis, IP_paper, '^-.', color='blue', markersize=8,
        label='Paper LES (Jaravel et al.)')

ax.set_xlabel('Equivalence Ratio $\\phi$')
ax.set_ylabel('Ignition Propensity / Probability')
ax.set_title('Ignition Propensity vs. Equivalence Ratio\n(cf. Jaravel et al. 2019, Fig. 7)')
ax.legend()
ax.set_xlim(0.4, 1.4); ax.set_ylim(-0.05, 1.1)
ax.grid(True, alpha=0.3)
fig.savefig(os.path.join(FIG, 'fig3_ignition_propensity.png'))
plt.close(fig)
print("fig3_ignition_propensity.png")

# ---- Fig 4: Temperature snapshots (cf. paper Fig 6) ----
snap_times = sorted(glob.glob(os.path.join(RES, 'snap_phi0.6_r0', '*.npz')))
available_times = [os.path.basename(f).replace('.npz','') for f in snap_times]
# Pick 0.2ms and 2.0ms equivalent
early_t = [t for t in available_times if '0.2' in t]
late_t = [t for t in available_times if '2.0' in t or '1.8' in t]

for phi_plot in [0.6, 1.0, 1.2]:
    snap_dir = os.path.join(RES, f'snap_phi{phi_plot}_r0')
    if not os.path.isdir(snap_dir):
        continue
    snaps = sorted(glob.glob(os.path.join(snap_dir, '*.npz')))
    n_snaps = len(snaps)
    if n_snaps < 2:
        continue
    
    fig, axes = plt.subplots(1, min(n_snaps, 5), figsize=(4*min(n_snaps,5), 3.5))
    if not hasattr(axes, '__len__'):
        axes = [axes]
    
    selected = snaps[::max(1, n_snaps//5)][:5]
    for ax, sf in zip(axes, selected):
        d = np.load(sf)
        T = d['T']
        x = np.arange(T.shape[0]) * 1.0  # mm (1mm grid)
        z = np.arange(T.shape[1]) * 1.0
        im = ax.pcolormesh(x, z, T.T, vmin=456, vmax=3000, cmap='hot', shading='auto')
        tname = os.path.basename(sf).replace('.npz','').replace('t_','t=')
        ax.set_title(tname, fontsize=9)
        ax.set_xlabel('x (mm)')
        if ax == axes[0]:
            ax.set_ylabel('z (mm)')
        ax.set_aspect('equal')
    
    fig.colorbar(im, ax=axes, label='T (K)', shrink=0.8)
    fig.suptitle(f'Temperature Fields, $\\phi={phi_plot}$\n(cf. Fig. 6)', fontsize=12)
    fig.tight_layout(rect=[0,0,0.92,0.92])
    fname = f'fig4_temp_phi{phi_plot}.png'
    fig.savefig(os.path.join(FIG, fname))
    plt.close(fig)
    print(fname)

# ---- Fig 5: Heat release field at selected time ----
for phi_plot in [0.6, 1.0, 1.2]:
    snap_dir = os.path.join(RES, f'snap_phi{phi_plot}_r0')
    if not os.path.isdir(snap_dir):
        continue
    snaps = sorted(glob.glob(os.path.join(snap_dir, '*.npz')))
    if len(snaps) < 2:
        continue
    
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    for ax, sf in zip(axes, [snaps[len(snaps)//4], snaps[-1]]):
        d = np.load(sf)
        if 'q_dot' in d:
            q = np.maximum(d['q_dot'], 1e-1)
            x = np.arange(q.shape[0]) * 1.0
            z = np.arange(q.shape[1]) * 1.0
            im = ax.pcolormesh(x, z, q.T, cmap='inferno',
                               norm=mcolors.LogNorm(vmin=1, vmax=1e6), shading='auto')
            plt.colorbar(im, ax=ax, label='$\\dot{Q}$ (W/m³)')
        tname = os.path.basename(sf).replace('.npz','').replace('t_','t=')
        ax.set_title(tname, fontsize=9)
        ax.set_xlabel('x (mm)')
        ax.set_ylabel('z (mm)')
        ax.set_aspect('equal')
    
    fig.suptitle(f'Heat Release Rate, $\\phi={phi_plot}$', fontsize=12)
    fig.tight_layout(rect=[0,0,1,0.92])
    fname = f'fig5_qdot_phi{phi_plot}.png'
    fig.savefig(os.path.join(FIG, fname))
    plt.close(fig)
    print(fname)

print(f"\nAll figures in {FIG}/")
