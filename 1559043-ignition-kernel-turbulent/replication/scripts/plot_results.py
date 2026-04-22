#!/usr/bin/env python3
"""
Generate publication-quality plots replicating key figures from
Jaravel et al. (2019), OSTI 1559043.
"""

import numpy as np
import json
import os
import sys

# Use Agg backend for headless
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.gridspec import GridSpec

plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

# Domain params
Lx, Lz = 73.0, 50.0  # mm
dx = dz = 0.5  # mm


def load_results():
    with open(os.path.join(RESULTS_DIR, 'simulation_results.json')) as f:
        data = json.load(f)
    return data


def plot_heat_release_history(data):
    """Fig. 5 equivalent: Total heat release rate vs time for all phi."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    colors = {'phi_0.6': 'blue', 'phi_0.8': 'green', 'phi_1.0': 'orange', 'phi_1.2': 'red'}
    labels = {'phi_0.6': r'$\phi=0.6$', 'phi_0.8': r'$\phi=0.8$',
              'phi_1.0': r'$\phi=1.0$', 'phi_1.2': r'$\phi=1.2$'}
    
    for key in ['phi_0.6', 'phi_0.8', 'phi_1.0', 'phi_1.2']:
        for i, r in enumerate(data['results'][key]):
            t = np.array(r['t_history'])
            Q = np.array(r['Qdot_history'])
            label = labels[key] if i == 0 else None
            alpha = 0.7 if i > 0 else 1.0
            ls = '-' if i == 0 else '--'
            ax.plot(t, Q, color=colors[key], alpha=alpha, ls=ls, label=label)
    
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Total Heat Release Rate (W/m)')
    ax.set_title('Heat Release Rate Evolution\n(cf. Jaravel et al. 2019, Fig. 5)')
    ax.legend(loc='upper left')
    ax.set_xlim(0, 2)
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    fig.savefig(os.path.join(FIGURES_DIR, 'heat_release_history.png'))
    plt.close(fig)
    print("Saved heat_release_history.png")


def plot_tmax_history(data):
    """Maximum temperature vs time."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    colors = {'phi_0.6': 'blue', 'phi_0.8': 'green', 'phi_1.0': 'orange', 'phi_1.2': 'red'}
    labels = {'phi_0.6': r'$\phi=0.6$', 'phi_0.8': r'$\phi=0.8$',
              'phi_1.0': r'$\phi=1.0$', 'phi_1.2': r'$\phi=1.2$'}
    
    for key in ['phi_0.6', 'phi_0.8', 'phi_1.0', 'phi_1.2']:
        for i, r in enumerate(data['results'][key]):
            t = np.array(r['t_history'])
            Tm = np.array(r['T_max_history'])
            label = labels[key] if i == 0 else None
            ax.plot(t, Tm, color=colors[key], alpha=0.7 if i > 0 else 1.0,
                    ls='-' if i == 0 else '--', label=label)
    
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Maximum Temperature (K)')
    ax.set_title('Peak Temperature Evolution')
    ax.legend()
    ax.set_xlim(0, 2)
    ax.grid(True, alpha=0.3)
    
    fig.savefig(os.path.join(FIGURES_DIR, 'tmax_history.png'))
    plt.close(fig)
    print("Saved tmax_history.png")


def plot_ignition_propensity(data):
    """Fig. 7 equivalent: Ignition propensity vs equivalence ratio."""
    fig, ax = plt.subplots(figsize=(7, 5))
    
    phis = [0.6, 0.8, 1.0, 1.2]
    
    # Paper experimental data (approximate from Fig. 7)
    P_ign_exp = [0.05, 0.40, 0.60, 0.80]
    
    IP_means = []
    IP_stds = []
    for phi in phis:
        key = f'phi_{phi}'
        s = data['summary'][key]
        IP_means.append(s['IP_mean'])
        IP_stds.append(s['IP_std'])
    
    ax.errorbar(phis, IP_means, yerr=IP_stds, fmt='s-', color='red',
                markersize=8, capsize=5, label='Simulation (IP)')
    ax.plot(phis, P_ign_exp, 'o--', color='black', markersize=8,
            label='Experiment (Sforzo et al.)')
    
    ax.set_xlabel('Equivalence Ratio $\\phi$')
    ax.set_ylabel('Ignition Propensity / Probability')
    ax.set_title('Ignition Propensity vs. Equivalence Ratio\n(cf. Jaravel et al. 2019, Fig. 7)')
    ax.legend()
    ax.set_xlim(0.4, 1.4)
    ax.set_ylim(-0.05, 1.1)
    ax.grid(True, alpha=0.3)
    
    fig.savefig(os.path.join(FIGURES_DIR, 'ignition_propensity.png'))
    plt.close(fig)
    print("Saved ignition_propensity.png")


def plot_temperature_snapshots(data):
    """Fig. 6 equivalent: Temperature fields at t=0.5ms and t=2.0ms."""
    phis = [0.6, 0.8, 1.0, 1.2]
    times = ['t_0.5ms', 't_2.0ms']
    
    fig, axes = plt.subplots(len(phis), len(times), figsize=(14, 12))
    
    for i, phi in enumerate(phis):
        snap_dir = os.path.join(RESULTS_DIR, f'snapshots_phi{phi}_r0')
        for j, tkey in enumerate(times):
            ax = axes[i, j]
            fpath = os.path.join(snap_dir, f'{tkey}.npz')
            if os.path.exists(fpath):
                d = np.load(fpath)
                T = d['T']
                x = np.arange(T.shape[0]) * 0.5  # mm
                z = np.arange(T.shape[1]) * 0.5  # mm
                im = ax.pcolormesh(x, z, T.T, vmin=456, vmax=3000,
                                   cmap='hot', shading='auto')
                ax.set_aspect('equal')
            else:
                ax.text(0.5, 0.5, 'No data', transform=ax.transAxes,
                        ha='center', va='center')
            
            if j == 0:
                ax.set_ylabel(f'$\\phi={phi}$\nz (mm)')
            if i == len(phis) - 1:
                ax.set_xlabel('x (mm)')
            if i == 0:
                ax.set_title(tkey.replace('_', '=').replace('ms', ' ms'))
    
    fig.colorbar(im, ax=axes, label='Temperature (K)', shrink=0.6)
    fig.suptitle('Temperature Fields\n(cf. Jaravel et al. 2019, Fig. 6)', fontsize=14)
    fig.tight_layout(rect=[0, 0, 0.92, 0.95])
    
    fig.savefig(os.path.join(FIGURES_DIR, 'temperature_snapshots.png'))
    plt.close(fig)
    print("Saved temperature_snapshots.png")


def plot_species_snapshots(data):
    """Species mass fraction fields at t=2.0ms."""
    phis = [0.6, 1.0, 1.2]
    species = ['Y_CH4', 'Y_O2', 'Y_NO']
    sp_labels = ['$Y_{CH_4}$', '$Y_{O_2}$', '$Y_{NO}$']
    
    fig, axes = plt.subplots(len(phis), len(species), figsize=(14, 9))
    
    for i, phi in enumerate(phis):
        snap_dir = os.path.join(RESULTS_DIR, f'snapshots_phi{phi}_r0')
        fpath = os.path.join(snap_dir, 't_2.0ms.npz')
        if os.path.exists(fpath):
            d = np.load(fpath)
            for j, (sp, lab) in enumerate(zip(species, sp_labels)):
                ax = axes[i, j]
                field = d[sp]
                x = np.arange(field.shape[0]) * 0.5
                z = np.arange(field.shape[1]) * 0.5
                im = ax.pcolormesh(x, z, field.T, cmap='viridis', shading='auto')
                ax.set_aspect('equal')
                plt.colorbar(im, ax=ax, fraction=0.046)
                if j == 0:
                    ax.set_ylabel(f'$\\phi={phi}$\nz (mm)')
                if i == 0:
                    ax.set_title(lab)
                if i == len(phis) - 1:
                    ax.set_xlabel('x (mm)')
    
    fig.suptitle('Species Mass Fractions at t=2.0 ms', fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(FIGURES_DIR, 'species_snapshots.png'))
    plt.close(fig)
    print("Saved species_snapshots.png")


def plot_heat_release_field(data):
    """Heat release rate field at t=2.0ms."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    for idx, phi in enumerate([0.6, 0.8, 1.0, 1.2]):
        ax = axes[idx // 2, idx % 2]
        snap_dir = os.path.join(RESULTS_DIR, f'snapshots_phi{phi}_r0')
        fpath = os.path.join(snap_dir, 't_2.0ms.npz')
        if os.path.exists(fpath):
            d = np.load(fpath)
            if 'q_dot' in d:
                q = d['q_dot']
                x = np.arange(q.shape[0]) * 0.5
                z = np.arange(q.shape[1]) * 0.5
                im = ax.pcolormesh(x, z, q.T, cmap='inferno',
                                   norm=mcolors.LogNorm(vmin=1e3, vmax=1e9),
                                   shading='auto')
                plt.colorbar(im, ax=ax, label='$\\dot{Q}$ (W/m³)')
        ax.set_title(f'$\\phi={phi}$')
        ax.set_xlabel('x (mm)')
        ax.set_ylabel('z (mm)')
        ax.set_aspect('equal')
    
    fig.suptitle('Heat Release Rate Fields at t=2.0 ms\n(cf. Jaravel et al. 2019, Fig. 8)', fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(FIGURES_DIR, 'heat_release_fields.png'))
    plt.close(fig)
    print("Saved heat_release_fields.png")


def main():
    data = load_results()
    plot_heat_release_history(data)
    plot_tmax_history(data)
    plot_ignition_propensity(data)
    plot_temperature_snapshots(data)
    plot_species_snapshots(data)
    plot_heat_release_field(data)
    print(f"\nAll figures saved to {FIGURES_DIR}/")


if __name__ == '__main__':
    main()
