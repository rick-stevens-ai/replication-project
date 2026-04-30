#!/usr/bin/env python3
"""
Master script to run the full NANOGrav 15-year GWB replication analysis.

Steps:
1. Analyze MCMC posteriors (amplitude, spectral index)
2. Compute optimal statistic (HD signal-to-noise)
3. Generate HD correlation curve and OS figures
4. Generate posterior corner plots
5. Compile final results JSON
"""

import sys
import os
import json
import numpy as np

# Set up paths
BASEDIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASEDIR, '..', 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

# Import analysis modules
sys.path.insert(0, BASEDIR)

from analyze_posteriors import main as analyze_posteriors
from compute_optimal_statistic import main as compute_optimal_statistic
from plot_hd_curve import main as plot_hd_curve
from plot_posteriors import main as plot_posteriors


def compile_final_results(posterior_results, os_results):
    """Compile all results into a single summary JSON."""
    
    # Paper reference values
    paper = {
        'A_GWB': 2.4e-15,
        'log10_A_GWB': float(np.log10(2.4e-15)),
        'gamma_SMBHB': 13/3,
        'gamma_recovered': 3.2,  # Paper median
        'HD_SNR_MCOS': 3.5,     # Paper Table 2
        'n_pulsars': 67,
        'n_frequencies': 14,
        'reference': 'Agazie et al. 2023, ApJL 951 L8',
        'arxiv': '2306.16213',
    }
    
    # Our recovered values
    our = {}
    
    if posterior_results and 'curn' in posterior_results:
        our['curn_log10_A'] = posterior_results['curn'].get('log10_A', {}).get('median')
        our['curn_gamma'] = posterior_results['curn'].get('gamma', {}).get('median')
        our['curn_A_linear'] = posterior_results['curn'].get('log10_A', {}).get('A_linear')
    
    if posterior_results and 'hd' in posterior_results:
        our['hd_log10_A'] = posterior_results['hd'].get('log10_A', {}).get('median')
        our['hd_gamma'] = posterior_results['hd'].get('gamma', {}).get('median')
        our['hd_A_linear'] = posterior_results['hd'].get('log10_A', {}).get('A_linear')
    
    if os_results and 'mcos' in os_results:
        our['hd_snr_median'] = os_results['mcos'].get('hellings_downs', {}).get('median_SNR')
        our['hd_snr_mean'] = os_results['mcos'].get('hellings_downs', {}).get('mean_SNR')
        our['monopole_snr'] = os_results['mcos'].get('monopole', {}).get('median_SNR')
        our['dipole_snr'] = os_results['mcos'].get('dipole', {}).get('median_SNR')
    
    our['n_pulsars'] = 67
    our['n_frequencies'] = 14
    
    # Agreement assessment
    agreement = {}
    
    if our.get('curn_log10_A') and our.get('curn_gamma'):
        sigma_A = posterior_results['curn']['log10_A']['std']
        sigma_gamma = posterior_results['curn']['gamma']['std']
        
        # Compare with paper gamma ~3.2 (the measured value, not the prediction 13/3)
        agreement['log10_A_offset_sigma'] = float(abs(our['curn_log10_A'] - paper['log10_A_GWB']) / sigma_A)
        agreement['gamma_vs_SMBHB_offset_sigma'] = float(abs(our['curn_gamma'] - paper['gamma_SMBHB']) / sigma_gamma)
        agreement['gamma_vs_paper_offset_sigma'] = float(abs(our['curn_gamma'] - paper['gamma_recovered']) / sigma_gamma)
        
        agreement['amplitude_consistent'] = agreement['log10_A_offset_sigma'] < 2.0
        agreement['gamma_consistent_with_SMBHB'] = agreement['gamma_vs_SMBHB_offset_sigma'] < 3.0
    
    if our.get('hd_snr_median'):
        agreement['hd_snr_consistent'] = abs(our['hd_snr_median'] - paper['HD_SNR_MCOS']) < 1.5
    
    final = {
        'paper_reference': paper,
        'our_results': our,
        'agreement': agreement,
        'method': {
            'posterior_analysis': 'Presampled MCMC chains from NANOGrav data release',
            'optimal_statistic': 'Noise-marginalized multi-component OS (10,000 realizations)',
            'software': ['enterprise v3.4.4', 'enterprise_extensions v3.0.3', 'la_forge v1.1.0'],
            'data': 'NANOGrav 15yr public data release (67 pulsars, feather format)',
        },
        'honest_gaps': [
            'Used presampled MCMC chains rather than running full Bayesian inference from scratch',
            'Full MCMC with 67 pulsars requires weeks of CPU time; chains provided by NANOGrav team',
            'Did not re-run the noise-marginalized OS computation (requires ~1h per 10k realizations + enterprise model setup)',
            'Used precomputed optimal statistic amplitudes from data release',
            'Free-spectrum and spline-ORF analyses use provided chains, not independent runs',
            'Model comparison (Bayes factor) from hypermodel chain, not independently computed',
        ],
    }
    
    outpath = os.path.join(RESULTS_DIR, 'final_results.json')
    with open(outpath, 'w') as f:
        json.dump(final, f, indent=2)
    
    print(f"\n{'='*60}")
    print("FINAL RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"\nPaper: A_GWB = {paper['A_GWB']:.2e}, gamma = {paper['gamma_SMBHB']:.4f}")
    if our.get('curn_A_linear'):
        print(f"Ours:  A_GWB = {our['curn_A_linear']:.2e}, gamma = {our['curn_gamma']:.4f}")
    if our.get('hd_snr_median'):
        print(f"\nPaper HD SNR: ~{paper['HD_SNR_MCOS']}")
        print(f"Our HD SNR:   {our['hd_snr_median']:.2f}")
    
    print(f"\nAgreement: {agreement}")
    print(f"\nSaved to {outpath}")
    
    return final


def main():
    print("="*60)
    print("NANOGrav 15-Year GWB Replication Analysis")
    print("="*60)
    
    # Step 1: Posteriors
    print("\n[Step 1/4] Analyzing MCMC posteriors...")
    posterior_results = analyze_posteriors()
    
    # Step 2: Optimal statistic
    print("\n[Step 2/4] Computing optimal statistic...")
    os_results = compute_optimal_statistic()
    
    # Step 3: HD curve plots
    print("\n[Step 3/4] Generating HD correlation figures...")
    plot_hd_curve()
    
    # Step 4: Posterior plots
    print("\n[Step 4/4] Generating posterior figures...")
    plot_posteriors()
    
    # Step 5: Compile
    print("\n[Compile] Final results...")
    final = compile_final_results(posterior_results, os_results)
    
    return final


if __name__ == '__main__':
    main()
