#!/usr/bin/env python3
"""
Generate all validation figures for the drift-flux replication.
Reproduces Figs 3-7 from Chen, Yu & Lai (2006).
Handles both Case 1 (U=0.225) and Case 2 (U=0.45).
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import json
import os

BASE = os.path.expanduser('~/Dropbox/REPLICATE-PROJECT/drift-flux-indoor-particles')
FIGS = os.path.join(BASE, 'report/figures')
os.makedirs(FIGS, exist_ok=True)

# Grid
NX, NY, NZ = 40, 20, 20
LX, LY, LZ = 0.8, 0.4, 0.4


def load_fields(case_label):
    """Load flow fields for a case."""
    if case_label == 'case1':
        fdir = os.path.join(BASE, 'data/openfoam_fields')
    else:
        fdir = os.path.join(BASE, 'data/openfoam_fields_case2')

    Ux = np.load(os.path.join(fdir, 'Ux.npy'))
    Uy = np.load(os.path.join(fdir, 'Uy.npy'))
    Uz = np.load(os.path.join(fdir, 'Uz.npy'))
    xc = np.load(os.path.join(fdir, 'xc.npy'))
    yc = np.load(os.path.join(fdir, 'yc.npy'))
    zc = np.load(os.path.join(fdir, 'zc.npy'))
    return Ux, Uy, Uz, xc, yc, zc


def load_concentration(case_u, dp_um, t):
    """Load a saved concentration field."""
    fpath = os.path.join(BASE, f'results/case_U{case_u}/dp_{dp_um}/C_t{int(t)}.npy')
    if os.path.exists(fpath):
        return np.load(fpath)
    return None


def load_cv_data(case_u):
    """Load CV time series."""
    fpath = os.path.join(BASE, f'results/case_U{case_u}/cv_timeseries.json')
    if os.path.exists(fpath):
        with open(fpath) as f:
            return json.load(f)
    return None


def fig3_velocity_field():
    """Fig 3: Velocity vector field at center plane (Case 1)."""
    Ux, Uy, Uz, xc, yc, zc = load_fields('case1')
    iy = NY // 2

    fig, ax = plt.subplots(figsize=(10, 5.5))
    X, Z = np.meshgrid(xc, zc, indexing='ij')
    U_c = Ux[:, iy, :]
    W_c = Uz[:, iy, :]
    speed = np.sqrt(U_c**2 + W_c**2)

    # Speed contour background
    cf = ax.contourf(X, Z, speed, levels=20, cmap='Blues', alpha=0.4)

    # Quiver
    skip = 2
    ax.quiver(X[::skip, ::skip], Z[::skip, ::skip],
              U_c[::skip, ::skip], W_c[::skip, ::skip],
              speed[::skip, ::skip], cmap='viridis',
              scale=1.2, width=0.004, alpha=0.9)

    # Scale bar
    ax.quiver(0.65, 0.02, 0.1, 0, color='red', scale=1.2, width=0.004)
    ax.text(0.65, 0.005, '0.1 m/s', fontsize=9, color='red')

    # Inlet/outlet markers
    ax.plot([0, 0], [0.34, 0.38], 'r-', linewidth=4, label='Inlet')
    ax.plot([0.8, 0.8], [0.02, 0.06], 'b-', linewidth=4, label='Outlet')

    ax.set_xlabel('x (m)', fontsize=13)
    ax.set_ylabel('z (m)', fontsize=13)
    ax.set_title('Fig 3: Airflow pattern at center plane (y = 0.2 m)\nInlet velocity 0.225 m/s', fontsize=14)
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 0.4)
    ax.set_aspect('equal')
    ax.legend(loc='lower left', fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'fig3_velocity_field.png'), dpi=200)
    plt.close()
    print("  Fig 3 ✓")


def fig4_velocity_profiles():
    """Fig 4: x-velocity profiles at x=0.2, 0.4, 0.6m (Case 1)."""
    Ux, _, _, xc, _, zc = load_fields('case1')
    iy = NY // 2

    fig, axes = plt.subplots(1, 3, figsize=(14, 5.5), sharey=True)
    x_locs = [0.2, 0.4, 0.6]
    labels = ['(a) x = 0.2 m', '(b) x = 0.4 m', '(c) x = 0.6 m']

    for ax, x_loc, label in zip(axes, x_locs, labels):
        ix = np.argmin(np.abs(xc - x_loc))
        ux = Ux[ix, iy, :]

        ax.plot(ux, zc, 'b-o', linewidth=2, markersize=3, label='Simulation')
        ax.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        ax.set_xlabel('x velocity (m s⁻¹)', fontsize=12)
        ax.set_title(label, fontsize=13)
        ax.set_xlim(-0.1, 0.25)
        ax.set_ylim(0, 0.4)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)

    axes[0].set_ylabel('z (m)', fontsize=12)
    fig.suptitle('Fig 4: Comparison of predicted x-direction velocities\n(inlet velocity 0.225 m s⁻¹)', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'fig4_velocity_profiles.png'), dpi=200)
    plt.close()
    print("  Fig 4 ✓")


def fig5_concentration_evolution():
    """Fig 5: Concentration contours at 60, 180, 300, 1800s for 1μm and 10μm."""
    _, _, _, xc, _, zc = load_fields('case1')
    iy = NY // 2

    times = [60, 180, 300, 1800]
    sizes = [1.0, 10.0]
    time_labels = ['60 s', '180 s', '300 s', '1800 s']

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    X, Z = np.meshgrid(xc, zc, indexing='ij')

    for row, dp_um in enumerate(sizes):
        for col, (t, tl) in enumerate(zip(times, time_labels)):
            ax = axes[row, col]
            C = load_concentration(0.225, dp_um, t)

            if C is not None:
                C_slice = C[:, iy, :]
                # Normalize to [0, 1]
                vmax = 1.0
                levels = np.linspace(0, vmax, 11)
                cf = ax.contourf(X, Z, np.clip(C_slice, 0, vmax),
                                 levels=levels, cmap='YlOrRd')
                ax.contour(X, Z, np.clip(C_slice, 0, vmax),
                           levels=levels, colors='k', linewidths=0.5, alpha=0.3)

                # Add contour labels at key levels
                cs = ax.contour(X, Z, np.clip(C_slice, 0, vmax),
                                levels=[0.1, 0.3, 0.5, 0.7, 0.9],
                                colors='k', linewidths=0.8)
                ax.clabel(cs, inline=True, fontsize=7, fmt='%.1f')
            else:
                ax.text(0.5, 0.5, 'No data', ha='center', va='center',
                        transform=ax.transAxes, fontsize=11, color='gray')

            if row == 0:
                ax.set_title(tl, fontsize=12)
            if col == 0:
                ax.set_ylabel(f'{dp_um} μm\nz (m)', fontsize=11)
            else:
                ax.set_ylabel('')
            if row == 1:
                ax.set_xlabel('x (m)', fontsize=11)

            ax.set_xlim(0, 0.8)
            ax.set_ylim(0, 0.4)
            ax.set_aspect('equal')

    fig.suptitle('Fig 5: Concentration evolution at center plane (inlet velocity 0.225 m s⁻¹)',
                 fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'fig5_concentration_evolution.png'), dpi=200,
                bbox_inches='tight')
    plt.close()
    print("  Fig 5 ✓")


def fig6_cv_timeseries():
    """Fig 6: CV vs time for both cases."""
    fig, ax = plt.subplots(figsize=(10, 7))

    styles_low = {'1.0': ('blue', '-'), '2.0': ('green', '-'),
                  '5.0': ('orange', '-'), '10.0': ('red', '-')}
    styles_high = {'1.0': ('blue', '--'), '2.0': ('green', '--'),
                   '5.0': ('orange', '--'), '10.0': ('red', '--')}

    for case_u, styles, vel_label in [(0.225, styles_low, '0.225'),
                                       (0.45, styles_high, '0.45')]:
        cv_data = load_cv_data(case_u)
        if cv_data is None:
            continue

        for dp_str, (color, ls) in styles.items():
            if dp_str in cv_data:
                d = cv_data[dp_str]
                times = np.array(d['times'])
                cv = np.array(d['cv'])
                ax.plot(times, cv * 100, color=color, linestyle=ls, linewidth=2,
                        label=f'{dp_str} μm, {vel_label} m s⁻¹')

    ax.axhline(y=10, color='k', linestyle=':', alpha=0.6, linewidth=1.5)
    ax.text(12, 11, 'Well-mixed threshold (10%)', fontsize=9, alpha=0.7)

    ax.set_xlabel('Time (s)', fontsize=13)
    ax.set_ylabel('Coefficient of Variation (%)', fontsize=13)
    ax.set_title('Fig 6: Coefficients of variation of concentration field', fontsize=14)
    ax.set_xscale('log')
    ax.set_xlim(10, 2000)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=9, ncol=2, loc='upper right')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'fig6_cv_timeseries.png'), dpi=200)
    plt.close()
    print("  Fig 6 ✓")


def fig7_concentration_profiles():
    """Fig 7: 10μm particle concentration profiles vs z at t=1800s."""
    _, _, _, xc, _, zc = load_fields('case1')
    iy = NY // 2

    fig, axes = plt.subplots(1, 3, figsize=(14, 5.5), sharey=True)
    x_locs = [0.2, 0.4, 0.6]
    labels = ['(a) x = 0.2 m', '(b) x = 0.4 m', '(c) x = 0.6 m']

    for case_u, color, ls, vel_label in [(0.225, 'blue', '-', '0.225 m/s'),
                                          (0.45, 'red', '--', '0.45 m/s')]:
        C10 = load_concentration(case_u, 10.0, 1800)
        if C10 is None:
            continue

        for ax, x_loc, label in zip(axes, x_locs, labels):
            ix = np.argmin(np.abs(xc - x_loc))
            c_profile = C10[ix, iy, :]
            ax.plot(c_profile, zc, color=color, linestyle=ls, linewidth=2,
                    label=f'Sim ({vel_label})')

    for ax, x_loc, label in zip(axes, x_locs, labels):
        ax.set_xlabel('Normalized concentration', fontsize=12)
        ax.set_title(label, fontsize=13)
        ax.set_xlim(0, 0.5)
        ax.set_ylim(0, 0.4)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)

    axes[0].set_ylabel('z (m)', fontsize=12)
    fig.suptitle('Fig 7: 10 μm particle concentration profiles (t = 1800 s)', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'fig7_concentration_profiles.png'), dpi=200)
    plt.close()
    print("  Fig 7 ✓")


def fig_summary():
    """Summary comparison table."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')

    headers = ['dp (μm)', 'vs (m/s)', 'Mix Time\n(this work)', 'Mix Time\n(paper)', 'Final CV', 'Final ⟨C⁺⟩', 'Well-mixed?']

    paper_mix = {'0.01': '< 429', '0.05': '< 429', '0.1': '< 429', '0.5': '< 429',
                 '1.0': '~429', '2.0': '~489', '3.0': 'N/A', '5.0': 'N/A',
                 '7.0': 'N/A', '10.0': 'N/A'}

    fpath = os.path.join(BASE, 'results/case_U0.225/summary.json')
    if not os.path.exists(fpath):
        print("  Summary: no data yet")
        return

    with open(fpath) as f:
        summary = json.load(f)

    rows = []
    for dp_str in ['0.01', '0.05', '0.1', '0.5', '1.0', '2.0', '3.0', '5.0', '7.0', '10.0']:
        s = summary[dp_str]
        mt = f"{s['mixing_time']:.0f}" if s['mixing_time'] else "N/A"
        cv = s['final_cv']
        mixed = '✓' if cv < 0.10 else '✗'
        rows.append([dp_str, f"{s['vs']:.2e}", mt, paper_mix.get(dp_str, '?'),
                     f"{cv:.3f}", f"{s['final_mean_c']:.4f}", mixed])

    table = ax.table(cellText=rows, colLabels=headers, loc='center',
                     cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.1, 1.6)

    for i, row in enumerate(rows):
        cv = float(row[4])
        color = '#d4edda' if cv < 0.10 else '#fff3cd' if cv < 0.20 else '#f8d7da'
        for j in range(len(headers)):
            table[i+1, j].set_facecolor(color)
        # Header styling
        for j in range(len(headers)):
            table[0, j].set_facecolor('#343a40')
            table[0, j].set_text_props(color='white', fontweight='bold')

    ax.set_title('Results Summary — Chen et al. (2006) Replication\nCase 1: U = 0.225 m s⁻¹, t = 1800 s',
                 fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'summary_table.png'), dpi=200, bbox_inches='tight')
    plt.close()
    print("  Summary table ✓")


def fig_cv_vs_diameter():
    """CV and mean concentration vs particle diameter for both cases."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    sizes = [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]

    for case_u, color, marker, label in [(0.225, 'blue', 'o', 'U = 0.225 m/s'),
                                          (0.45, 'red', 's', 'U = 0.45 m/s')]:
        fpath = os.path.join(BASE, f'results/case_U{case_u}/summary.json')
        if not os.path.exists(fpath):
            continue
        with open(fpath) as f:
            summary = json.load(f)

        cvs = [summary[str(dp)]['final_cv'] for dp in sizes]
        means = [summary[str(dp)]['final_mean_c'] for dp in sizes]

        ax1.plot(sizes, [c*100 for c in cvs], f'{color}', marker=marker,
                 linewidth=2, markersize=7, label=label)
        ax2.plot(sizes, means, f'{color}', marker=marker,
                 linewidth=2, markersize=7, label=label)

    ax1.axhline(y=10, color='k', linestyle=':', alpha=0.5)
    ax1.set_xlabel('Particle diameter (μm)', fontsize=12)
    ax1.set_ylabel('Coefficient of Variation (%)', fontsize=12)
    ax1.set_title('Final CV at t = 1800 s', fontsize=13)
    ax1.set_xscale('log')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    ax2.axhline(y=1.0, color='k', linestyle=':', alpha=0.5)
    ax2.set_xlabel('Particle diameter (μm)', fontsize=12)
    ax2.set_ylabel('Mean normalized concentration ⟨C⁺⟩', fontsize=12)
    ax2.set_title('Mean concentration at t = 1800 s', fontsize=13)
    ax2.set_xscale('log')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    fig.suptitle('Particle size dependence of mixing and concentration', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'cv_vs_diameter.png'), dpi=200, bbox_inches='tight')
    plt.close()
    print("  CV vs diameter ✓")


if __name__ == '__main__':
    print(f"Generating figures in {FIGS}\n")
    fig3_velocity_field()
    fig4_velocity_profiles()
    fig5_concentration_evolution()
    fig6_cv_timeseries()
    fig7_concentration_profiles()
    fig_summary()
    fig_cv_vs_diameter()
    print(f"\nAll figures saved to {FIGS}")
