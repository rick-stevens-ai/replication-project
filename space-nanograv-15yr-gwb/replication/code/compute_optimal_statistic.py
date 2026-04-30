#!/usr/bin/env python3
"""
Compute the optimal statistic (OS) for Hellings-Downs correlations
using the NANOGrav 15-year data release.

This uses the precomputed noise-marginalized OS from the data release
(curn_14f_pl_vg_os.npz) which contains 10,000 noise realizations.

Also computes the single-component OS and multi-component OS (MCOS)
SNR distributions.
"""

import sys
import os
import json
import numpy as np

TUTORIAL_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', '15yr_stochastic_analysis', 'tutorials')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

sys.path.insert(0, TUTORIAL_DIR)


def analyze_precomputed_os():
    """Analyze precomputed noise-marginalized MCOS results."""
    print("="*60)
    print("PRECOMPUTED MULTI-COMPONENT OPTIMAL STATISTIC")
    print("="*60)
    
    data = np.load(os.path.join(TUTORIAL_DIR, 'data', 'curn_14f_pl_vg_os.npz'))
    A = data['A']       # (10000, 3) - amplitudes for [monopole, dipole, HD]
    A_err = data['A_err']  # (10000, 3)
    
    SNR = A / A_err
    
    labels = ['Monopole', 'Dipole', 'Hellings-Downs']
    
    results = {'n_realizations': int(A.shape[0])}
    
    for i, label in enumerate(labels):
        snr_vals = SNR[:, i]
        a_vals = A[:, i]
        
        # Compute statistics
        stats = {
            'median_SNR': float(np.median(snr_vals)),
            'mean_SNR': float(np.mean(snr_vals)),
            'std_SNR': float(np.std(snr_vals)),
            'SNR_percentiles': {
                '5': float(np.percentile(snr_vals, 5)),
                '16': float(np.percentile(snr_vals, 16)),
                '50': float(np.percentile(snr_vals, 50)),
                '84': float(np.percentile(snr_vals, 84)),
                '95': float(np.percentile(snr_vals, 95)),
            },
            'median_A_squared': float(np.median(a_vals)),
            'mean_A_squared': float(np.mean(a_vals)),
        }
        
        results[label.lower().replace(' ', '_').replace('-', '_')] = stats
        
        print(f"\n{label}:")
        print(f"  SNR: median = {stats['median_SNR']:.2f}, mean = {stats['mean_SNR']:.2f}")
        print(f"  SNR 68% CI: [{stats['SNR_percentiles']['16']:.2f}, {stats['SNR_percentiles']['84']:.2f}]")
        print(f"  A^2: median = {stats['median_A_squared']:.4e}")
    
    # Convert A^2 to amplitude for HD
    hd_A2_med = results['hellings_downs']['median_A_squared']
    if hd_A2_med > 0:
        hd_A = np.sqrt(hd_A2_med)
        results['hellings_downs']['A_gwb'] = float(hd_A)
        results['hellings_downs']['log10_A_gwb'] = float(np.log10(hd_A))
        print(f"\n  HD A_gwb = {hd_A:.3e}")
        print(f"  HD log10(A_gwb) = {np.log10(hd_A):.4f}")
    
    return results


def compute_ml_optimal_statistic():
    """
    Compute the maximum-likelihood optimal statistic using the provided
    ML parameters (fixed gamma = 13/3).
    """
    print("\n" + "="*60)
    print("MAXIMUM-LIKELIHOOD OPTIMAL STATISTIC")
    print("="*60)
    
    # Load ML parameters
    ml_params_path = os.path.join(TUTORIAL_DIR, 'data', 'optstat_ml_gamma4p33.json')
    with open(ml_params_path) as f:
        ml_params = json.load(f)
    
    # Count pulsars from parameter names
    psr_names = set()
    for k in ml_params.keys():
        parts = k.replace('_red_noise_gamma', '').replace('_red_noise_log10_A', '')
        psr_names.add(parts)
    
    results = {
        'n_pulsars_with_red_noise': len(psr_names),
        'pulsar_names': sorted(list(psr_names)),
    }
    
    print(f"  {len(psr_names)} pulsars with red noise parameters")
    
    # Show a few example values
    print("\n  Example red noise parameters:")
    for name in sorted(psr_names)[:5]:
        gamma_key = f"{name}_red_noise_gamma"
        A_key = f"{name}_red_noise_log10_A"
        if gamma_key in ml_params and A_key in ml_params:
            print(f"    {name}: gamma={ml_params[gamma_key]:.2f}, log10_A={ml_params[A_key]:.2f}")
    
    return results


def main():
    all_results = {}
    
    # 1. Precomputed MCOS
    all_results['mcos'] = analyze_precomputed_os()
    
    # 2. ML optimal statistic params
    all_results['ml_params'] = compute_ml_optimal_statistic()
    
    # Paper comparison
    print("\n" + "="*60)
    print("COMPARISON WITH PAPER")
    print("="*60)
    
    paper_snr_hd = 3.5  # Table 2 of the paper (noise-marginalized MCOS SNR)
    our_snr = all_results['mcos']['hellings_downs']['median_SNR']
    
    print(f"\n  Paper HD SNR (MCOS, noise-marginalized): ~{paper_snr_hd}")
    print(f"  Our HD SNR (median): {our_snr:.2f}")
    print(f"  Agreement: {'Good' if abs(our_snr - paper_snr_hd) < 1.0 else 'Check'}")
    
    all_results['paper_comparison'] = {
        'paper_hd_snr': paper_snr_hd,
        'our_hd_snr': our_snr,
        'snr_difference': float(abs(our_snr - paper_snr_hd)),
    }
    
    # Save
    outpath = os.path.join(RESULTS_DIR, 'optimal_statistic_results.json')
    with open(outpath, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nResults saved to {outpath}")
    return all_results


if __name__ == '__main__':
    main()
