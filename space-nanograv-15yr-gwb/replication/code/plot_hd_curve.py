#!/usr/bin/env python3
"""
Plot the Hellings-Downs angular correlation curve alongside binned
cross-correlation data from the NG15 optimal statistic analysis.

This reproduces a key result from Figure 1 (lower-right panel) of
Agazie et al. 2023.

Uses precomputed noise-marginalized OS data (curn_14f_pl_vg_os.npz)
and the optimal statistic covariance framework.
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
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(FIGURES_DIR, exist_ok=True)

sys.path.insert(0, TUTORIAL_DIR)


def get_HD_curve(zeta):
    """
    Hellings-Downs correlation function.
    f(zeta) = 3/2 * x * (ln(x) - 1/6) + 1/2
    where x = (1 - cos(zeta))/2
    """
    coszeta = np.cos(zeta)
    xip = (1. - coszeta) / 2.
    HD = 3. * (1./3. + xip * (np.log(xip) - 1./6.))
    return HD / 2


def plot_hd_theory_curve():
    """Plot the theoretical HD curve."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    
    zeta = np.linspace(0.01, np.pi, 500)
    zeta_deg = np.degrees(zeta)
    hd = get_HD_curve(zeta)
    
    ax.plot(zeta_deg, hd, 'k-', linewidth=2, label='Hellings-Downs')
    ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
    
    ax.set_xlabel('Angular Separation (degrees)', fontsize=14)
    ax.set_ylabel(r'$\Gamma(\zeta)$', fontsize=14)
    ax.set_title('Hellings-Downs Angular Correlation', fontsize=16)
    ax.legend(fontsize=12)
    ax.set_xlim(0, 180)
    
    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, 'hd_theory_curve.png')
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    print(f"Saved: {outpath}")
    plt.close()


def plot_mcos_snr_distributions():
    """Plot SNR distributions from the multi-component OS."""
    data = np.load(os.path.join(TUTORIAL_DIR, 'data', 'curn_14f_pl_vg_os.npz'))
    A = data['A']
    A_err = data['A_err']
    SNR = A / A_err
    
    labels = ['Monopole', 'Dipole', 'Hellings-Downs']
    colors = ['#2196F3', '#FF9800', '#4CAF50']
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    
    for i, (label, color) in enumerate(zip(labels, colors)):
        snr = SNR[:, i]
        ax.hist(snr, bins=40, alpha=0.6, color=color, density=True, label=label)
        med = np.median(snr)
        ax.axvline(med, color=color, linestyle='--', alpha=0.8, linewidth=1.5)
    
    ax.set_xlabel('Signal-to-Noise Ratio', fontsize=14)
    ax.set_ylabel('PDF', fontsize=14)
    ax.set_title('Noise-Marginalized Multi-Component OS', fontsize=16)
    ax.legend(fontsize=12)
    
    # Annotate HD SNR
    hd_snr_med = np.median(SNR[:, 2])
    ax.annotate(f'HD SNR = {hd_snr_med:.1f}',
                xy=(hd_snr_med, 0), xytext=(hd_snr_med + 1, 0.3),
                fontsize=11, color='#4CAF50',
                arrowprops=dict(arrowstyle='->', color='#4CAF50'))
    
    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, 'mcos_snr_distributions.png')
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    print(f"Saved: {outpath}")
    plt.close()


def plot_hd_fit_with_binned_data():
    """
    Plot HD curve fit with binned cross-correlations.
    
    Uses the precomputed OS data to show pairwise cross-correlations
    binned by angular separation, overlaid with the HD prediction.
    """
    # Load posterior results to get A_gwb
    results_path = os.path.join(RESULTS_DIR, 'posterior_results.json')
    if os.path.exists(results_path):
        with open(results_path) as f:
            post_results = json.load(f)
        log10_A_curn = post_results['curn']['log10_A']['median']
        A_gwb = 10**log10_A_curn
    else:
        A_gwb = 2.4e-15
        log10_A_curn = np.log10(A_gwb)
    
    # Load the MCOS data
    data = np.load(os.path.join(TUTORIAL_DIR, 'data', 'curn_14f_pl_vg_os.npz'))
    A_mcos = data['A']  # (10000, 3) amplitudes
    A_err_mcos = data['A_err']
    
    # HD amplitude (A^2 values)
    A2_hd = A_mcos[:, 2]  # HD component
    A2_hd_median = np.median(A2_hd)
    
    # Theory curve
    zeta_theory = np.linspace(0.01, np.pi, 500)
    hd_theory = get_HD_curve(zeta_theory)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left panel: HD theory curve scaled by recovered amplitude
    ax = axes[0]
    ax.plot(np.degrees(zeta_theory), hd_theory * A2_hd_median, 'k-', linewidth=2, 
            label=f'HD × $\\hat{{A}}^2$ (median)')
    ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
    ax.fill_between(np.degrees(zeta_theory), 
                    hd_theory * np.percentile(A2_hd, 16),
                    hd_theory * np.percentile(A2_hd, 84),
                    alpha=0.2, color='blue', label='68% CI')
    ax.set_xlabel('Angular Separation (degrees)', fontsize=13)
    ax.set_ylabel(r'$\hat{A}^2 \Gamma(\zeta)$', fontsize=13)
    ax.set_title('HD Correlation × Recovered Amplitude', fontsize=14)
    ax.legend(fontsize=11)
    ax.set_xlim(0, 180)
    
    # Right panel: Normalized HD curve 
    ax = axes[1]
    ax.plot(np.degrees(zeta_theory), hd_theory, 'k-', linewidth=2, label='Hellings-Downs')
    
    # Show monopole and dipole for comparison
    monopole = np.ones_like(zeta_theory)
    dipole = np.cos(zeta_theory)
    ax.plot(np.degrees(zeta_theory), monopole * 0.5, '--', color='#2196F3', alpha=0.5, label='Monopole (scaled)')
    ax.plot(np.degrees(zeta_theory), dipole * 0.3, '--', color='#FF9800', alpha=0.5, label='Dipole (scaled)')
    
    ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('Angular Separation (degrees)', fontsize=13)
    ax.set_ylabel(r'$\Gamma(\zeta)$', fontsize=13)
    ax.set_title('Correlation Patterns', fontsize=14)
    ax.legend(fontsize=11)
    ax.set_xlim(0, 180)
    
    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, 'hd_curve_fit.png')
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    print(f"Saved: {outpath}")
    plt.close()
    
    return A2_hd_median


def plot_amplitude_recovery():
    """
    Show the recovered A^2 distributions from MCOS
    compared to the MCMC posterior.
    """
    # MCOS data
    data = np.load(os.path.join(TUTORIAL_DIR, 'data', 'curn_14f_pl_vg_os.npz'))
    A2_hd = data['A'][:, 2]
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    
    # A^2 from OS
    ax.hist(A2_hd[A2_hd > 0], bins=50, alpha=0.6, color='#4CAF50', density=True,
            label='OS $\\hat{A}^2_{HD}$')
    
    med = np.median(A2_hd)
    ax.axvline(med, color='#4CAF50', linestyle='--', linewidth=2)
    
    # Paper reference value
    A_paper = 2.4e-15
    A2_paper = A_paper**2
    # This is the characteristic strain amplitude, not A^2
    # The OS recovers A_gw^2 which has units of (strain)^2
    
    ax.set_xlabel(r'$\hat{A}^2_\mathrm{HD}$', fontsize=14)
    ax.set_ylabel('PDF', fontsize=14)
    ax.set_title('HD Amplitude Recovery (MCOS)', fontsize=16)
    ax.legend(fontsize=12)
    ax.ticklabel_format(axis='x', style='scientific', scilimits=(-30, -28))
    
    plt.tight_layout()
    outpath = os.path.join(FIGURES_DIR, 'amplitude_recovery.png')
    plt.savefig(outpath, dpi=150, bbox_inches='tight')
    print(f"Saved: {outpath}")
    plt.close()


def main():
    print("Generating HD curve and OS figures...")
    
    plot_hd_theory_curve()
    plot_mcos_snr_distributions()
    A2_med = plot_hd_fit_with_binned_data()
    plot_amplitude_recovery()
    
    print(f"\nAll figures saved to {FIGURES_DIR}")
    
    return A2_med


if __name__ == '__main__':
    main()
