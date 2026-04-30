#!/usr/bin/env python3
"""
Generate publication-quality figures for the replication.

Figures:
1. E(T) fit comparison — raw data, GPR fit, exact
2. C_V(T) comparison — FD vs Spline vs GPR vs exact (main result)
3. S(T) comparison — all methods vs exact
4. Noise sweep — GPR advantage grows with noise level
"""

import numpy as np
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Style
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 13,
    'axes.titlesize': 13,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
})

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)


def load_data(system_name):
    """Load JSON data for a system."""
    fname = os.path.join(RESULTS_DIR, f'{system_name}_data.json')
    with open(fname) as f:
        return json.load(f)


def plot_energy_fit(system_name, title):
    """Figure 1: Energy fit comparison."""
    d = load_data(system_name)

    fig, ax = plt.subplots(figsize=(8, 5))

    # Noisy data
    ax.scatter(d['T_data'], d['E_noisy'], s=8, alpha=0.3, color='gray',
               label='Noisy data (synthetic DMQMC)', zorder=1)

    # Exact
    ax.plot(d['T_eval'], d['E_exact'], 'k-', lw=2, label='Exact', zorder=3)

    # GPR fit
    if 'E_gpr_T' in d:
        ax.plot(d['T_eval'], d['E_gpr_T'], 'r--', lw=2,
                label='GPR fit', zorder=2)

    ax.set_xlabel(r'Temperature $T$ (arb. units)')
    ax.set_ylabel(r'Energy $E(T)$')
    ax.set_title(title)
    ax.legend()

    fname = os.path.join(FIGURES_DIR, f'{system_name}_energy_fit.png')
    fig.savefig(fname)
    plt.close(fig)
    print(f"  Saved {fname}")


def plot_cv_comparison(system_name, title):
    """Figure 2: C_V comparison (main result of paper)."""
    d = load_data(system_name)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: full view
    ax = axes[0]
    ax.plot(d['T_eval'], d['cv_exact'], 'k-', lw=2.5, label='Exact', zorder=4)

    if 'cv_gpr_T' in d:
        ax.plot(d['T_eval'], d['cv_gpr_T'], 'r-', lw=1.5,
                label='GPR', alpha=0.9, zorder=3)

    if 'cv_fd_T' in d:
        ax.plot(d['T_fd'], d['cv_fd_T'], 'b.--', lw=0.8, ms=3,
                label='Finite Diff.', alpha=0.7, zorder=2)

    if 'cv_spline_T' in d:
        ax.plot(d['T_eval'], d['cv_spline_T'], 'g:', lw=1.2,
                label='Cubic Spline', alpha=0.7, zorder=1)

    ax.set_xlabel(r'Temperature $T$')
    ax.set_ylabel(r'Specific heat $C_V$ ($k_B$)')
    ax.set_title(f'{title} — Full range')
    ax.legend()
    ax.set_ylim(bottom=-0.5)

    # Right: zoom into low-T (where noise matters most)
    ax = axes[1]
    T_eval = np.array(d['T_eval'])
    mask = T_eval < np.median(T_eval)

    ax.plot(T_eval[mask], np.array(d['cv_exact'])[mask],
            'k-', lw=2.5, label='Exact', zorder=4)

    if 'cv_gpr_T' in d:
        ax.plot(T_eval[mask], np.array(d['cv_gpr_T'])[mask],
                'r-', lw=1.5, label='GPR', alpha=0.9, zorder=3)

    if 'cv_fd_T' in d:
        T_fd = np.array(d['T_fd'])
        cv_fd = np.array(d['cv_fd_T'])
        mask_fd = T_fd < np.median(T_eval)
        ax.plot(T_fd[mask_fd], cv_fd[mask_fd], 'b.--', lw=0.8, ms=3,
                label='Finite Diff.', alpha=0.7, zorder=2)

    if 'cv_spline_T' in d:
        ax.plot(T_eval[mask], np.array(d['cv_spline_T'])[mask],
                'g:', lw=1.2, label='Cubic Spline', alpha=0.7, zorder=1)

    ax.set_xlabel(r'Temperature $T$')
    ax.set_ylabel(r'Specific heat $C_V$ ($k_B$)')
    ax.set_title(f'{title} — Low-T zoom')
    ax.legend()

    fig.tight_layout()
    fname = os.path.join(FIGURES_DIR, f'{system_name}_cv_comparison.png')
    fig.savefig(fname)
    plt.close(fig)
    print(f"  Saved {fname}")


def plot_entropy_comparison(system_name, title):
    """Figure 3: Entropy comparison."""
    d = load_data(system_name)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(d['T_eval'], d['S_exact'], 'k-', lw=2.5, label='Exact', zorder=4)

    if 'S_gpr_T' in d and d['S_gpr_T'] is not None:
        ax.plot(d['T_eval'], d['S_gpr_T'], 'r-', lw=1.5,
                label='GPR', alpha=0.9, zorder=3)

    if 'S_fd' in d:
        ax.plot(d['T_fd'], d['S_fd'], 'b.--', lw=0.8, ms=3,
                label='Finite Diff.', alpha=0.7, zorder=2)

    if 'S_spline' in d and d['S_spline'] is not None:
        ax.plot(d['T_eval'], d['S_spline'], 'g:', lw=1.2,
                label='Cubic Spline', alpha=0.7, zorder=1)

    ax.set_xlabel(r'Temperature $T$')
    ax.set_ylabel(r'Entropy $S$ ($k_B$)')
    ax.set_title(title)
    ax.legend()

    fname = os.path.join(FIGURES_DIR, f'{system_name}_entropy.png')
    fig.savefig(fname)
    plt.close(fig)
    print(f"  Saved {fname}")


def plot_multi_system_cv():
    """Figure 4: C_V for all systems in one figure (like paper's Fig. 2)."""
    systems = [
        ('hubbard_2site_U4', 'Hubbard 2-site (U/t=4)'),
        ('hubbard_2site_U8', 'Hubbard 2-site (U/t=8)'),
        ('chain_4site', '4-site chain'),
        ('hubbard_2site_U4_noisy', 'Hubbard U/t=4 (high noise)'),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    for ax, (sysname, label) in zip(axes.flat, systems):
        try:
            d = load_data(sysname)
        except FileNotFoundError:
            ax.set_title(f'{label} — data not found')
            continue

        ax.plot(d['T_eval'], d['cv_exact'], 'k-', lw=2, label='Exact')

        if 'cv_gpr_T' in d:
            ax.plot(d['T_eval'], d['cv_gpr_T'], 'r-', lw=1.5,
                    label='GPR', alpha=0.9)

        if 'cv_fd_T' in d:
            ax.plot(d['T_fd'], d['cv_fd_T'], 'b.', ms=3,
                    label='Finite Diff.', alpha=0.5)

        if 'cv_spline_T' in d:
            ax.plot(d['T_eval'], d['cv_spline_T'], 'g:', lw=1,
                    label='Cubic Spline', alpha=0.6)

        ax.set_xlabel(r'$T$')
        ax.set_ylabel(r'$C_V$ ($k_B$)')
        ax.set_title(label)
        ax.legend(fontsize=8)

        # Clip y to sensible range
        cv_max = max(d['cv_exact']) * 1.5
        ax.set_ylim(-0.3, max(cv_max, 1.0))

    fig.suptitle(r'Specific Heat $C_V(T)$: GPR vs Finite Difference vs Cubic Spline',
                 fontsize=14, y=1.01)
    fig.tight_layout()

    fname = os.path.join(FIGURES_DIR, 'multi_system_cv.png')
    fig.savefig(fname)
    plt.close(fig)
    print(f"  Saved {fname}")


def plot_noise_sweep():
    """Figure 5: RMSE vs noise level."""
    fname_data = os.path.join(RESULTS_DIR, 'hubbard_2site_U4_noise_sweep.json')
    if not os.path.exists(fname_data):
        print("  Noise sweep data not found, skipping")
        return

    with open(fname_data) as f:
        sweep = json.load(f)

    noise_levels = [s['noise_scale'] for s in sweep]
    rmse_fd = [s['rmse_fd'] for s in sweep]
    rmse_sp = [s['rmse_spline'] for s in sweep]
    rmse_gpr = [s['rmse_gpr'] for s in sweep]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: absolute RMSE
    ax = axes[0]
    ax.plot(noise_levels, rmse_fd, 'bs-', label='Finite Diff.', lw=2, ms=8)
    ax.plot(noise_levels, rmse_sp, 'g^-', label='Cubic Spline', lw=2, ms=8)
    ax.plot(noise_levels, rmse_gpr, 'ro-', label='GPR', lw=2, ms=8)
    ax.set_xlabel('Noise scale')
    ax.set_ylabel(r'RMSE of $C_V$')
    ax.set_title(r'$C_V$ RMSE vs Noise Level')
    ax.legend()
    ax.set_yscale('log')

    # Right: GPR improvement ratio
    ax = axes[1]
    ratio_fd = [g/f if f > 0 else 1 for g, f in zip(rmse_gpr, rmse_fd)]
    ratio_sp = [g/s if s > 0 else 1 for g, s in zip(rmse_gpr, rmse_sp)]
    ax.plot(noise_levels, ratio_fd, 'bs-', label='GPR/FD', lw=2, ms=8)
    ax.plot(noise_levels, ratio_sp, 'g^-', label='GPR/Spline', lw=2, ms=8)
    ax.axhline(1.0, color='gray', ls='--', alpha=0.5)
    ax.set_xlabel('Noise scale')
    ax.set_ylabel('RMSE ratio')
    ax.set_title('GPR Improvement Factor')
    ax.legend()

    fig.tight_layout()
    fname = os.path.join(FIGURES_DIR, 'noise_sweep.png')
    fig.savefig(fname)
    plt.close(fig)
    print(f"  Saved {fname}")


def main():
    print("Generating figures...")

    systems = [
        ('hubbard_2site_U4', 'Hubbard 2-site (U/t=4, moderate noise)'),
        ('hubbard_2site_U8', 'Hubbard 2-site (U/t=8, moderate noise)'),
        ('chain_4site', '4-site tight-binding chain'),
        ('hubbard_2site_U4_noisy', 'Hubbard 2-site (U/t=4, high noise)'),
    ]

    for sysname, title in systems:
        try:
            print(f"\n{sysname}:")
            plot_energy_fit(sysname, title)
            plot_cv_comparison(sysname, title)
            plot_entropy_comparison(sysname, title)
        except FileNotFoundError:
            print(f"  Data not found for {sysname}, skipping")

    print("\nMulti-system comparison:")
    plot_multi_system_cv()

    print("\nNoise sweep:")
    plot_noise_sweep()

    print(f"\nAll figures saved to {FIGURES_DIR}/")


if __name__ == '__main__':
    main()
