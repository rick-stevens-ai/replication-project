#!/usr/bin/env python3
"""Analyze PeleC ignition kernel results — kernel cooling, ignition propensity."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path.home() / "Dropbox/REPLICATE-PROJECT/1559043-ignition-kernel-turbulent/replication-pelec"
with open(BASE / "analysis" / "timeseries.json") as f:
    data = json.load(f)

phis = sorted(data.keys(), key=float)
colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(phis)))

# Extract arrays per phi
series = {}
for phi in phis:
    recs = data[phi]
    t = np.array([r['time'] for r in recs]) * 1e3  # s -> ms
    Tmax = np.array([r['temp_max'] for r in recs])
    Tmin = np.array([r['temp_min'] for r in recs])
    pmax = np.array([r.get('pres_max', np.nan) for r in recs])
    series[phi] = {'t': t, 'Tmax': Tmax, 'Tmin': Tmin, 'pmax': pmax}

# === Figure 1: Kernel cooling curves (Tmax vs time) ===
fig, ax = plt.subplots(figsize=(7, 5))
for phi, c in zip(phis, colors):
    s = series[phi]
    ax.plot(s['t']*1e3, s['Tmax'], '-', color=c, linewidth=1.5, label=f'φ = {phi}')
ax.set_xlabel('Time (μs)')
ax.set_ylabel(r'Maximum temperature $T_\mathrm{max}$ (K)')
ax.set_title('Kernel cooling: 4-φ sweep (PeleC compressible LES)')
ax.legend(title='Equivalence ratio', loc='upper right')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1000)
fig.tight_layout()
fig.savefig(BASE / "analysis" / "fig_cooling.png", dpi=150)
fig.savefig(BASE / "analysis" / "fig_cooling.pdf")
print("fig_cooling written")

# === Figure 2: Log-scale early-time detail (0-100 μs, kernel ejection phase) ===
fig, ax = plt.subplots(figsize=(7, 5))
for phi, c in zip(phis, colors):
    s = series[phi]
    mask = s['t']*1e3 <= 100
    ax.semilogy(s['t'][mask]*1e3, s['Tmax'][mask], '-', color=c, linewidth=1.5, label=f'φ = {phi}')
ax.set_xlabel('Time (μs)')
ax.set_ylabel(r'$T_\mathrm{max}$ (K, log)')
ax.set_title('Early-time kernel behavior (0–100 μs)')
ax.axhline(1500, ls='--', c='r', alpha=0.5, label='Ignition threshold (1500 K)')
ax.legend(loc='upper right')
ax.grid(True, which='both', alpha=0.3)
ax.set_xlim(0, 100)
fig.tight_layout()
fig.savefig(BASE / "analysis" / "fig_earlytime.png", dpi=150)
fig.savefig(BASE / "analysis" / "fig_earlytime.pdf")
print("fig_earlytime written")

# === Figure 3: Ignition propensity approximation ===
# Paper's ignition propensity = P(sustained combustion at t=t_end).
# We use simplified metric: max(Tmax > 1500K for t > 500 μs) — did kernel maintain
# ignition-capable temperature in the second half of the simulation?
# Also report fraction of sim time above 1500K.
metrics = {}
for phi in phis:
    s = series[phi]
    mask_late = s['t'] * 1e3 > 500  # t > 500 μs
    frac_hot_late = np.mean(s['Tmax'][mask_late] > 1500) if mask_late.any() else 0.0
    t_peak = s['t'][np.argmax(s['Tmax'])] * 1e3  # μs
    T_peak = s['Tmax'].max()
    T_at_100us = np.interp(0.1, s['t']*1e3, s['Tmax'])  # T at 100 μs
    T_at_500us = np.interp(0.5, s['t']*1e3, s['Tmax'])
    T_at_1ms = s['Tmax'][-1]
    metrics[phi] = dict(
        T_peak=T_peak, t_peak_us=t_peak,
        T_100us=T_at_100us, T_500us=T_at_500us, T_1ms=T_at_1ms,
        frac_hot_late=frac_hot_late,
    )

# Save metrics
with open(BASE / "analysis" / "metrics.json", 'w') as f:
    json.dump(metrics, f, indent=2)
print("metrics.json written")
for phi, m in metrics.items():
    print(f"  φ={phi}: T_peak={m['T_peak']:.0f}K @{m['t_peak_us']:.1f}μs, T@1ms={m['T_1ms']:.1f}K, fracHot(>500μs)={m['frac_hot_late']:.2%}")

# === Figure 3: Simulation ignition propensity vs equivalence ratio ===
# Our metric: 1 - (T_1ms - T_crossflow) / (T_peak - T_crossflow) = 0 means full cool, 1 means sustained
Tcross = 456.0
phi_arr = np.array([float(p) for p in phis])
ip_ours = np.array([(metrics[p]['T_1ms'] - Tcross) / (metrics[p]['T_peak'] - Tcross) for p in phis])
# Paper's ignition propensity from Fig 3 (Jaravel 2019), extracted approximate:
ip_paper = np.array([0.0, 0.20, 0.65, 0.90])  # φ=0.6,0.8,1.0,1.2 from paper Fig 3 LES
ip_exp   = np.array([0.0, 0.30, 0.75, 1.00])  # Sforzo et al experiment (approximate)

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(phi_arr, ip_exp,   'o-', color='black',  label='Experiment (Sforzo et al.)', markersize=9)
ax.plot(phi_arr, ip_paper, 's-', color='tab:blue',  label='Paper LES (CharLES$^X$)', markersize=9)
ax.plot(phi_arr, ip_ours,  '^-', color='tab:red',   label='This work (PeleC, proxy metric)', markersize=9)
ax.set_xlabel('Equivalence ratio φ')
ax.set_ylabel('Ignition propensity (or proxy)')
ax.set_title('Paper Fig. 3 comparison')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim(-0.05, 1.1)
fig.tight_layout()
fig.savefig(BASE / "analysis" / "fig_propensity.png", dpi=150)
fig.savefig(BASE / "analysis" / "fig_propensity.pdf")
print("fig_propensity written")

# === Figure 4: Min temperature (indicator of cooling front penetration) ===
fig, ax = plt.subplots(figsize=(7, 5))
for phi, c in zip(phis, colors):
    s = series[phi]
    ax.plot(s['t']*1e3, s['Tmin'], '-', color=c, linewidth=1.5, label=f'φ = {phi}')
ax.set_xlabel('Time (μs)')
ax.set_ylabel(r'$T_\mathrm{min}$ (K)')
ax.set_title('Minimum temperature — cold-side behavior')
ax.legend(loc='best')
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(BASE / "analysis" / "fig_tmin.png", dpi=150)
print("fig_tmin written")

print("\nAll figures written to", BASE / "analysis")
