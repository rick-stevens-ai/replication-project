#!/usr/bin/env python3
"""
Generate validation figures for the drift-flux replication.
Reproduces Figs 3-7 from Chen, Yu & Lai (2006).
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import os

BASE = os.path.expanduser('~/Dropbox/REPLICATE-PROJECT/drift-flux-indoor-particles')
RESULTS = os.path.join(BASE, 'results/case_U0.225')
FIELDS = os.path.join(BASE, 'data/openfoam_fields')
FIGS = os.path.join(BASE, 'report/figures')
os.makedirs(FIGS, exist_ok=True)

# Load grid
xc = np.load(os.path.join(FIELDS, 'xc.npy'))
yc = np.load(os.path.join(FIELDS, 'yc.npy'))
zc = np.load(os.path.join(FIELDS, 'zc.npy'))
Ux = np.load(os.path.join(FIELDS, 'Ux.npy'))
Uy = np.load(os.path.join(FIELDS, 'Uy.npy'))
Uz = np.load(os.path.join(FIELDS, 'Uz.npy'))

NX, NY, NZ = Ux.shape
iy_center = NY // 2  # center plane y=0.2m


def fig3_velocity_field():
    """Fig 3: Velocity vector field at center plane."""
    fig, ax = plt.subplots(figsize=(10, 5))

    X, Z = np.meshgrid(xc, zc, indexing='ij')
    U_center = Ux[:, iy_center, :]
    W_center = Uz[:, iy_center, :]
    speed = np.sqrt(U_center**2 + W_center**2)

    # Quiver plot
    skip = 2
    ax.quiver(X[::skip, ::skip], Z[::skip, ::skip],
              U_center[::skip, ::skip], W_center[::skip, ::skip],
              speed[::skip, ::skip], cmap='viridis',
              scale=1.5, width=0.003, alpha=0.8)

    # Mark inlet and outlet
    ax.plot([0, 0], [0.34, 0.38], 'r-', linewidth=3, label='Inlet')
    ax.plot([0.8, 0.8], [0.02, 0.06], 'b-', linewidth=3, label='Outlet')

    ax.set_xlabel('x (m)', fontsize=12)
    ax.set_ylabel('z (m)', fontsize=12)
    ax.set_title('Fig 3: Airflow pattern at center plane (y=0.2m)\nInlet velocity 0.225 m/s', fontsize=13)
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 0.4)
    ax.set_aspect('equal')
    ax.legend(loc='lower left')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'fig3_velocity_field.png'), dpi=150)
    plt.close()
    print("Fig 3 saved")


def fig4_velocity_profiles():
    """Fig 4: x-velocity profiles at x=0.2, 0.4, 0.6m."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5), sharey=True)

    x_locs = [0.2, 0.4, 0.6]
    labels = ['(a) x = 0.2 m', '(b) x = 0.4 m', '(c) x = 0.6 m']

    for ax, x_loc, label in zip(axes, x_locs, labels):
        ix = np.argmin(np.abs(xc - x_loc))
        ux_profile = Ux[ix, iy_center, :]

        ax.plot(ux_profile, zc, 'b-', linewidth=2, label='Simulation')
        ax.set_xlabel('x velocity (m/s)', fontsize=11)
        ax.set_title(label, fontsize=12)
        ax.set_xlim(-0.1, 0.25)
        ax.set_ylim(0, 0.4)
        ax.axvline(x=0, color='k', linestyle='--', alpha=0.3)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)

    axes[0].set_ylabel('z (m)', fontsize=11)
    fig.suptitle('Fig 4: Velocity profiles at center plane (inlet velocity 0.225 m/s)', fontsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'fig4_velocity_profiles.png'), dpi=150)
    plt.close()
    print("Fig 4 saved")


def fig6_cv_timeseries():
    """Fig 6: Coefficient of variation vs time for various particle sizes."""
    with open(os.path.join(RESULTS, 'cv_timeseries.json')) as f:
        cv_data = json.load(f)

    fig, ax = plt.subplots(figsize=(10, 7))

    colors = {'1.0': 'blue', '2.0': 'green', '5.0': 'orange', '10.0': 'red'}
    linestyles = {'1.0': '-', '2.0': '--', '5.0': '-.', '10.0': ':'}

    for dp_str in ['1.0', '2.0', '5.0', '10.0']:
        if dp_str in cv_data:
            d = cv_data[dp_str]
            times = np.array(d['times'])
            cv = np.array(d['cv'])
            ax.plot(times, cv * 100, color=colors[dp_str],
                    linestyle=linestyles[dp_str], linewidth=2,
                    label=f'{dp_str} μm, 0.225 m/s')

    ax.axhline(y=10, color='k', linestyle='--', alpha=0.5, label='10% threshold')
    ax.set_xlabel('Time (s)', fontsize=12)
    ax.set_ylabel('Coefficient of Variation (%)', fontsize=12)
    ax.set_title('Fig 6: Coefficients of variation of concentration field', fontsize=13)
    ax.set_xscale('log')
    ax.set_xlim(10, 1800)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'fig6_cv_timeseries.png'), dpi=150)
    plt.close()
    print("Fig 6 saved")


def fig7_concentration_profiles():
    """Fig 7: Concentration profiles of 10μm particles at t=1800s."""
    # Load the saved concentration field
    # The solver saves C fields via cv_timeseries but not spatial fields to disk
    # by default. Let's reconstruct from the summary or re-extract.
    # For now, use the CV data which has mean_c

    # Actually, let's read the saved .npy files if they exist
    c_files = {}
    for dp in [10.0]:
        # Check if spatial concentration was saved
        fpath = os.path.join(RESULTS, f'C_dp{dp}_t1800.npy')
        if os.path.exists(fpath):
            c_files[dp] = np.load(fpath)

    if not c_files:
        print("Fig 7: No saved concentration fields found — need to re-run with field saving")
        # Create a placeholder figure from the summary data
        fig, axes = plt.subplots(1, 3, figsize=(14, 5), sharey=True)
        for ax, x_loc in zip(axes, [0.2, 0.4, 0.6]):
            ax.text(0.5, 0.5, 'Concentration field\nnot saved to disk',
                    ha='center', va='center', transform=ax.transAxes, fontsize=11)
            ax.set_xlabel('Normalized concentration', fontsize=11)
            ax.set_title(f'x = {x_loc} m', fontsize=12)
            ax.set_xlim(0, 1.2)
            ax.set_ylim(0, 0.4)
        axes[0].set_ylabel('z (m)', fontsize=11)
        fig.suptitle('Fig 7: 10 μm particle concentration profiles (t=1800s, U=0.225 m/s)\n[Need to re-run with field saving]', fontsize=13)
        plt.tight_layout()
        plt.savefig(os.path.join(FIGS, 'fig7_concentration_profiles.png'), dpi=150)
        plt.close()
        print("Fig 7 saved (placeholder)")
        return

    C10 = c_files[10.0]
    fig, axes = plt.subplots(1, 3, figsize=(14, 5), sharey=True)
    x_locs = [0.2, 0.4, 0.6]
    labels = ['(a) x = 0.2 m', '(b) x = 0.4 m', '(c) x = 0.6 m']

    for ax, x_loc, label in zip(axes, x_locs, labels):
        ix = np.argmin(np.abs(xc - x_loc))
        c_profile = C10[ix, iy_center, :]
        ax.plot(c_profile, zc, 'b-', linewidth=2, label='Simulation')
        ax.set_xlabel('Normalized concentration', fontsize=11)
        ax.set_title(label, fontsize=12)
        ax.set_xlim(0, 1.2)
        ax.set_ylim(0, 0.4)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)

    axes[0].set_ylabel('z (m)', fontsize=11)
    fig.suptitle('Fig 7a: 10 μm particle concentration (t=1800s, inlet velocity 0.225 m/s)', fontsize=13)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'fig7_concentration_profiles.png'), dpi=150)
    plt.close()
    print("Fig 7 saved")


def summary_table():
    """Generate summary results table."""
    with open(os.path.join(RESULTS, 'summary.json')) as f:
        summary = json.load(f)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')

    # Paper reference values (approximate from text)
    paper_mix = {
        '1.0': '~429', '2.0': '~489', '5.0': 'N/A', '10.0': 'N/A',
        '0.01': '<429', '0.05': '<429', '0.1': '<429', '0.5': '<429',
        '3.0': 'N/A', '7.0': 'N/A'
    }

    headers = ['dp (μm)', 'vs (m/s)', 'Mix Time (s)', 'Paper Mix Time', 'Final CV', 'Final ⟨C⁺⟩']
    rows = []
    for dp_str in ['0.01', '0.05', '0.1', '0.5', '1.0', '2.0', '3.0', '5.0', '7.0', '10.0']:
        s = summary[dp_str]
        mt = f"{s['mixing_time']:.0f}" if s['mixing_time'] else "N/A"
        rows.append([dp_str, f"{s['vs']:.2e}", mt,
                     paper_mix.get(dp_str, '?'),
                     f"{s['final_cv']:.3f}", f"{s['final_mean_c']:.4f}"])

    table = ax.table(cellText=rows, colLabels=headers, loc='center',
                     cellLoc='center', colWidths=[0.1, 0.15, 0.13, 0.15, 0.12, 0.12])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    # Color coding
    for i, row in enumerate(rows):
        cv = float(row[4])
        color = '#d4edda' if cv < 0.10 else '#fff3cd' if cv < 0.20 else '#f8d7da'
        for j in range(len(headers)):
            table[i+1, j].set_facecolor(color)

    ax.set_title('Results Summary — Drift-Flux Model Replication\nChen, Yu & Lai (2006), U = 0.225 m/s', fontsize=13, pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'summary_table.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Summary table saved")


def fig_cv_vs_diameter():
    """Additional figure: Final CV and mean concentration vs particle diameter."""
    with open(os.path.join(RESULTS, 'summary.json')) as f:
        summary = json.load(f)

    sizes = [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    cvs = [summary[str(dp)]['final_cv'] for dp in sizes]
    means = [summary[str(dp)]['final_mean_c'] for dp in sizes]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(sizes, [c*100 for c in cvs], 'ro-', linewidth=2, markersize=8)
    ax1.axhline(y=10, color='k', linestyle='--', alpha=0.5, label='10% threshold')
    ax1.set_xlabel('Particle diameter (μm)', fontsize=12)
    ax1.set_ylabel('Coefficient of Variation (%)', fontsize=12)
    ax1.set_title('Final CV at t=1800s', fontsize=13)
    ax1.set_xscale('log')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(sizes, means, 'bs-', linewidth=2, markersize=8)
    ax2.axhline(y=1.0, color='k', linestyle='--', alpha=0.5, label='C⁺ = 1 (inlet)')
    ax2.set_xlabel('Particle diameter (μm)', fontsize=12)
    ax2.set_ylabel('Mean normalized concentration ⟨C⁺⟩', fontsize=12)
    ax2.set_title('Mean concentration at t=1800s', fontsize=13)
    ax2.set_xscale('log')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    fig.suptitle('Particle size dependence — U = 0.225 m/s', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, 'cv_vs_diameter.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("CV vs diameter figure saved")


if __name__ == '__main__':
    print(f"Generating figures in {FIGS}")
    fig3_velocity_field()
    fig4_velocity_profiles()
    fig6_cv_timeseries()
    fig7_concentration_profiles()
    summary_table()
    fig_cv_vs_diameter()
    print(f"\nAll figures saved to {FIGS}")
