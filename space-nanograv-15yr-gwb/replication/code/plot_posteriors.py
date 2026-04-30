#!/usr/bin/env python3
"""
Generate corner plots and posterior comparisons for NG15 GWB analysis.

Reproduces key aspects of Figures 4 and 5 from Agazie et al. 2023.
"""

import sys
import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

TUTORIAL_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', '15yr_stochastic_analysis', 'tutorials')
FIGURES_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

sys.path.insert(0, TUTORIAL_DIR)

from la_forge import core


def plot_curn_corner():
    """Corner plot for CURN model (gamma vs log10_A)."""
    print("Generating CURN corner plot...")
    
    c = core.Core(corepath=os.path.join(TUTORIAL_DIR, 'presampled_cores', 'curn_14f_pl_vg.core'))
    
    gamma_idx = c.params.index('gw_gamma')
    A_idx = c.params.index('gw_log10_A')
    
    gamma = c.chain[:, gamma_idx]
    log10_A = c.chain[:, A_idx]
    
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))
    
    # Upper left: gamma histogram
    ax = axes[0, 0]
    ax.hist(gamma, bins=50, density=True, alpha=0.7, color='#2196F3')
    ax.axvline(np.median(gamma), color='k', linestyle='--', linewidth=1.5)
    ax.axvline(13/3, color='red', linestyle=':', linewidth=1.5, label=r'$\gamma=13/3$')
    ax.set_xlabel(r'$\gamma_\mathrm{CURN}$', fontsize=12)
    ax.set_ylabel('PDF', fontsize=12)
    ax.legend(fontsize=10)
    
    # Upper right: empty
    axes[0, 1].axis('off')
    
    # Lower left: 2D contour
    ax = axes[1, 0]
    H, xedges, yedges = np.histogram2d(gamma, log10_A, bins=40, density=True)
    X, Y = np.meshgrid(0.5*(xedges[:-1]+xedges[1:]), 0.5*(yedges[:-1]+yedges[1:]))
    
    # Sort for contour levels
    H_flat = H.flatten()
    H_sort = np.sort(H_flat)[::-1]
    H_cumsum = np.cumsum(H_sort) / np.sum(H_sort)
    levels_68 = H_sort[np.searchsorted(H_cumsum, 0.68)]
    levels_95 = H_sort[np.searchsorted(H_cumsum, 0.95)]
    
    ax.contourf(X, Y, H.T, levels=[levels_95, levels_68, H.max()], 
                colors=['#90CAF9', '#2196F3'], alpha=0.7)
    ax.contour(X, Y, H.T, levels=[levels_95, levels_68], colors='#1565C0', linewidths=1)
    
    # Paper truth
    ax.axvline(13/3, color='red', linestyle=':', alpha=0.7)
    ax.axhline(np.log10(2.4e-15), color='red', linestyle=':', alpha=0.7)
    ax.plot(13/3, np.log10(2.4e-15), 'r+', markersize=15, markeredgewidth=2)
    
    ax.set_xlabel(r'$\gamma_\mathrm{CURN}$', fontsize=12)
    ax.set_ylabel(r'$\log_{10} A_\mathrm{CURN}$', fontsize=12)
    
    # Lower right: log10_A histogram
    ax = axes[1, 1]
    ax.hist(log10_A, bins=50, density=True, alpha=0.7, color='#2196F3', orientation='horizontal')
    ax.axhline(np.median(log10_A), color='k', linestyle='--', linewidth=1.5)
    ax.axhline(np.log10(2.4e-15), color='red', linestyle=':', linewidth=1.5, label=r'$A=2.4\times10^{-15}$')
    ax.set_ylabel(r'$\log_{10} A_\mathrm{CURN}$', fontsize=12)
    ax.set_xlabel('PDF', fontsize=12)
    ax.legend(fontsize=9)
    
    fig.suptitle('CURN Model Posteriors (NANOGrav 15yr)', fontsize=14, y=1.01)
    plt.tight_layout()
    
    outpath = os.path.join(FIGURES_DIR, 'curn_corner.png')
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    print(f"Saved: {outpath}")
    plt.close()


def plot_hd_corner():
    """Corner plot for HD-correlated model."""
    print("Generating HD corner plot...")
    
    c = core.Core(corepath=os.path.join(TUTORIAL_DIR, 'presampled_cores', 'hd_14f_pl_vg.core'))
    
    gamma_idx = c.params.index('gw__gamma')
    A_idx = c.params.index('gw__log10_A')
    
    gamma = c.chain[:, gamma_idx]
    log10_A = c.chain[:, A_idx]
    
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))
    
    # Upper left: gamma histogram
    ax = axes[0, 0]
    ax.hist(gamma, bins=50, density=True, alpha=0.7, color='#4CAF50')
    ax.axvline(np.median(gamma), color='k', linestyle='--', linewidth=1.5)
    ax.axvline(13/3, color='red', linestyle=':', linewidth=1.5, label=r'$\gamma=13/3$')
    ax.set_xlabel(r'$\gamma_\mathrm{HD}$', fontsize=12)
    ax.set_ylabel('PDF', fontsize=12)
    ax.legend(fontsize=10)
    
    # Upper right: empty
    axes[0, 1].axis('off')
    
    # Lower left: 2D contour
    ax = axes[1, 0]
    H, xedges, yedges = np.histogram2d(gamma, log10_A, bins=40, density=True)
    X, Y = np.meshgrid(0.5*(xedges[:-1]+xedges[1:]), 0.5*(yedges[:-1]+yedges[1:]))
    
    H_flat = H.flatten()
    H_sort = np.sort(H_flat)[::-1]
    H_cumsum = np.cumsum(H_sort) / np.sum(H_sort)
    levels_68 = H_sort[np.searchsorted(H_cumsum, 0.68)]
    levels_95 = H_sort[np.searchsorted(H_cumsum, 0.95)]
    
    ax.contourf(X, Y, H.T, levels=[levels_95, levels_68, H.max()], 
                colors=['#A5D6A7', '#4CAF50'], alpha=0.7)
    ax.contour(X, Y, H.T, levels=[levels_95, levels_68], colors='#2E7D32', linewidths=1)
    
    ax.axvline(13/3, color='red', linestyle=':', alpha=0.7)
    ax.axhline(np.log10(2.4e-15), color='red', linestyle=':', alpha=0.7)
    ax.plot(13/3, np.log10(2.4e-15), 'r+', markersize=15, markeredgewidth=2)
    
    ax.set_xlabel(r'$\gamma_\mathrm{HD}$', fontsize=12)
    ax.set_ylabel(r'$\log_{10} A_\mathrm{HD}$', fontsize=12)
    
    # Lower right: log10_A histogram
    ax = axes[1, 1]
    ax.hist(log10_A, bins=50, density=True, alpha=0.7, color='#4CAF50', orientation='horizontal')
    ax.axhline(np.median(log10_A), color='k', linestyle='--', linewidth=1.5)
    ax.axhline(np.log10(2.4e-15), color='red', linestyle=':', linewidth=1.5)
    ax.set_ylabel(r'$\log_{10} A_\mathrm{HD}$', fontsize=12)
    ax.set_xlabel('PDF', fontsize=12)
    
    fig.suptitle('HD-Correlated Model Posteriors (NANOGrav 15yr)', fontsize=14, y=1.01)
    plt.tight_layout()
    
    outpath = os.path.join(FIGURES_DIR, 'hd_corner.png')
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    print(f"Saved: {outpath}")
    plt.close()


def plot_curn_vs_hd_comparison():
    """Overlay CURN and HD posteriors."""
    print("Generating CURN vs HD comparison...")
    
    c_curn = core.Core(corepath=os.path.join(TUTORIAL_DIR, 'presampled_cores', 'curn_14f_pl_vg.core'))
    c_hd = core.Core(corepath=os.path.join(TUTORIAL_DIR, 'presampled_cores', 'hd_14f_pl_vg.core'))
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # gamma comparison
    ax = axes[0]
    gamma_curn = c_curn.chain[:, c_curn.params.index('gw_gamma')]
    gamma_hd = c_hd.chain[:, c_hd.params.index('gw__gamma')]
    
    ax.hist(gamma_curn, bins=50, density=True, alpha=0.5, color='#2196F3', label='CURN')
    ax.hist(gamma_hd, bins=50, density=True, alpha=0.5, color='#4CAF50', label='HD')
    ax.axvline(13/3, color='red', linestyle=':', linewidth=2, label=r'$\gamma_\mathrm{SMBHB}=13/3$')
    ax.set_xlabel(r'$\gamma$', fontsize=14)
    ax.set_ylabel('PDF', fontsize=14)
    ax.set_title('Spectral Index Posterior', fontsize=14)
    ax.legend(fontsize=11)
    
    # log10_A comparison
    ax = axes[1]
    A_curn = c_curn.chain[:, c_curn.params.index('gw_log10_A')]
    A_hd = c_hd.chain[:, c_hd.params.index('gw__log10_A')]
    
    ax.hist(A_curn, bins=50, density=True, alpha=0.5, color='#2196F3', label='CURN')
    ax.hist(A_hd, bins=50, density=True, alpha=0.5, color='#4CAF50', label='HD')
    ax.axvline(np.log10(2.4e-15), color='red', linestyle=':', linewidth=2, 
               label=r'$A=2.4\times10^{-15}$')
    ax.set_xlabel(r'$\log_{10} A$', fontsize=14)
    ax.set_ylabel('PDF', fontsize=14)
    ax.set_title('GWB Amplitude Posterior', fontsize=14)
    ax.legend(fontsize=11)
    
    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, 'curn_vs_hd_posteriors.png')
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    print(f"Saved: {outpath}")
    plt.close()


def plot_free_spectrum():
    """Plot the free-spectrum posterior (violin plot)."""
    print("Generating free spectrum plot...")
    
    c = core.Core(corepath=os.path.join(TUTORIAL_DIR, 'presampled_cores', 'hd_30f_fs.core'))
    
    rho_params = sorted([p for p in c.params if 'log10_rho' in p],
                       key=lambda x: int(x.split('_')[-1]))
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    
    n_freqs = len(rho_params)
    freq_indices = range(1, n_freqs + 1)
    
    medians = []
    ci_lo = []
    ci_hi = []
    ci_95_lo = []
    ci_95_hi = []
    
    for p in rho_params:
        idx = c.params.index(p)
        vals = c.chain[:, idx]
        pct = np.percentile(vals, [5, 16, 50, 84, 95])
        ci_95_lo.append(pct[0])
        ci_lo.append(pct[1])
        medians.append(pct[2])
        ci_hi.append(pct[3])
        ci_95_hi.append(pct[4])
    
    medians = np.array(medians)
    ci_lo = np.array(ci_lo)
    ci_hi = np.array(ci_hi)
    ci_95_lo = np.array(ci_95_lo)
    ci_95_hi = np.array(ci_95_hi)
    
    # Plot 95% CI
    ax.fill_between(freq_indices, ci_95_lo, ci_95_hi, alpha=0.15, color='#4CAF50')
    # Plot 68% CI
    ax.fill_between(freq_indices, ci_lo, ci_hi, alpha=0.3, color='#4CAF50')
    # Plot medians
    ax.plot(freq_indices, medians, 'o-', color='#2E7D32', markersize=5, linewidth=1.5)
    
    # Power law reference (gamma = 13/3)
    f_ref = np.array(list(freq_indices), dtype=float)
    # log10(rho) for power law: log10(A^2 / (12 pi^2)) - gamma * log10(f/f_ref) + const
    # Approximate: use median amplitude
    gamma_ref = 13/3
    # Normalize to match low-frequency bins
    powerlaw_ref = medians[0] - gamma_ref * np.log10(f_ref / f_ref[0])
    ax.plot(freq_indices, powerlaw_ref, 'r--', linewidth=1.5, alpha=0.7,
            label=r'$\gamma=13/3$ power law')
    
    ax.set_xlabel('Frequency bin index $i$ ($f_i = i/T$)', fontsize=13)
    ax.set_ylabel(r'$\log_{10} \rho_i$', fontsize=13)
    ax.set_title('HD Free-Spectrum Recovery (30 bins)', fontsize=14)
    ax.legend(fontsize=11)
    
    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, 'free_spectrum.png')
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    print(f"Saved: {outpath}")
    plt.close()


def main():
    print("Generating posterior figures...")
    
    plot_curn_corner()
    plot_hd_corner()
    plot_curn_vs_hd_comparison()
    plot_free_spectrum()
    
    print(f"\nAll figures saved to {FIGURES_DIR}")


if __name__ == '__main__':
    main()
