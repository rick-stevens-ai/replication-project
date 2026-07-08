#!/usr/bin/env python3
"""
Analyze presampled MCMC posteriors from NG15 data release.
Extract GWB amplitude (A_GWB), spectral index (gamma), and model comparison (Bayes factor).

Corresponds to NANOGrav 15yr GWB paper (Agazie et al. 2023, ApJL 951 L8).
Paper values:
  - A_GWB ≈ 2.4e-15 (at f_ref = 1 yr^-1)
  - gamma ≈ 13/3 ≈ 4.33 (for SMBHB prediction)
  - Recovered median gamma ~3.2 (slightly below 13/3 but consistent within ~1σ)
"""

import sys
import os
import json
import numpy as np

# Paths
TUTORIAL_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', '15yr_stochastic_analysis', 'tutorials')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

sys.path.insert(0, TUTORIAL_DIR)

from la_forge import core


def analyze_chain(corepath, name, gw_params_map):
    """Analyze a single MCMC chain."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {name}")
    print(f"{'='*60}")
    
    c = core.Core(corepath=corepath)
    print(f"  Chain shape: {c.chain.shape}")
    print(f"  N_samples (post-burn): {c.chain.shape[0]}")
    
    results = {'name': name, 'n_samples': int(c.chain.shape[0])}
    
    for label, param_name in gw_params_map.items():
        if param_name in c.params:
            idx = c.params.index(param_name)
            vals = c.chain[:, idx]
            pct = np.percentile(vals, [5, 16, 50, 84, 95])
            results[label] = {
                'median': float(pct[2]),
                'mean': float(np.mean(vals)),
                'std': float(np.std(vals)),
                'ci_68': [float(pct[1]), float(pct[3])],
                'ci_90': [float(pct[0]), float(pct[4])],
            }
            print(f"  {label} ({param_name}):")
            print(f"    median = {pct[2]:.4f}")
            print(f"    68% CI = [{pct[1]:.4f}, {pct[3]:.4f}]")
            print(f"    90% CI = [{pct[0]:.4f}, {pct[4]:.4f}]")
            
            if 'log10_A' in param_name:
                A_med = 10**pct[2]
                A_lo = 10**pct[1]
                A_hi = 10**pct[3]
                results[label]['A_linear'] = float(A_med)
                results[label]['A_linear_68'] = [float(A_lo), float(A_hi)]
                print(f"    A (linear) = {A_med:.3e}")
                print(f"    A 68% CI = [{A_lo:.3e}, {A_hi:.3e}]")
    
    # Bayes factor from nmodel if available
    if 'nmodel' in c.params:
        idx = c.params.index('nmodel')
        nmodel = c.chain[:, idx]
        # nmodel=0 is CURN, nmodel=1 is HD (or alternative)
        n0 = np.sum(nmodel < 0.5)
        n1 = np.sum(nmodel >= 0.5)
        if n0 > 0 and n1 > 0:
            bf = n1 / n0
            results['bayes_factor'] = float(bf)
            results['log10_bf'] = float(np.log10(bf))
            print(f"  Bayes factor (model1/model0): {bf:.2f}")
            print(f"  log10(BF): {np.log10(bf):.2f}")
    
    return results


def analyze_free_spectrum(corepath, name):
    """Analyze free-spectrum chain to get per-frequency power."""
    print(f"\n{'='*60}")
    print(f"Analyzing free spectrum: {name}")
    print(f"{'='*60}")
    
    c = core.Core(corepath=corepath)
    
    # Get free-spectrum parameters
    rho_params = sorted([p for p in c.params if 'log10_rho' in p])
    print(f"  Found {len(rho_params)} frequency bins")
    
    results = {'name': name, 'n_freqs': len(rho_params), 'n_samples': int(c.chain.shape[0])}
    
    freqs = []
    medians = []
    ci_lo = []
    ci_hi = []
    
    for p in rho_params:
        idx = c.params.index(p)
        vals = c.chain[:, idx]
        pct = np.percentile(vals, [16, 50, 84])
        freq_idx = int(p.split('_')[-1])
        freqs.append(freq_idx)
        medians.append(float(pct[1]))
        ci_lo.append(float(pct[0]))
        ci_hi.append(float(pct[1]))
        
    results['freq_indices'] = freqs
    results['log10_rho_medians'] = medians
    results['log10_rho_ci_lo'] = ci_lo
    results['log10_rho_ci_hi'] = ci_hi
    
    return results


def analyze_spline_orf(corepath, name):
    """Analyze spline ORF chain to extract spatial correlation pattern."""
    print(f"\n{'='*60}")
    print(f"Analyzing spline ORF: {name}")
    print(f"{'='*60}")
    
    c = core.Core(corepath=corepath)
    
    orf_params = sorted([p for p in c.params if 'orf_spline' in p])
    crn_params = {p: c.params.index(p) for p in c.params if 'gw_crn' in p}
    
    results = {'name': name, 'n_samples': int(c.chain.shape[0])}
    
    print(f"  Spline ORF parameters: {orf_params}")
    
    spline_vals = {}
    for p in orf_params:
        idx = c.params.index(p)
        vals = c.chain[:, idx]
        pct = np.percentile(vals, [16, 50, 84])
        spline_vals[p] = {
            'median': float(pct[1]),
            'ci_68': [float(pct[0]), float(pct[2])]
        }
        print(f"  {p}: median={pct[1]:.4f}, 68%CI=[{pct[0]:.4f}, {pct[2]:.4f}]")
    
    results['spline_orf'] = spline_vals
    
    # CRN amplitude/gamma
    for p, idx in crn_params.items():
        vals = c.chain[:, idx]
        pct = np.percentile(vals, [16, 50, 84])
        results[p] = {'median': float(pct[1]), 'ci_68': [float(pct[0]), float(pct[2])]}
        print(f"  {p}: median={pct[1]:.4f}")
    
    return results


def main():
    presampled = os.path.join(TUTORIAL_DIR, 'presampled_cores')
    
    all_results = {}
    
    # 1. CURN (common uncorrelated red noise) — baseline model
    all_results['curn'] = analyze_chain(
        os.path.join(presampled, 'curn_14f_pl_vg.core'),
        'CURN 14-freq power-law varied-gamma',
        {'gamma': 'gw_gamma', 'log10_A': 'gw_log10_A'}
    )
    
    # 2. HD (Hellings-Downs correlated) — GWB model
    all_results['hd'] = analyze_chain(
        os.path.join(presampled, 'hd_14f_pl_vg.core'),
        'HD 14-freq power-law varied-gamma',
        {'gamma': 'gw__gamma', 'log10_A': 'gw__log10_A'}
    )
    
    # 3. CURN vs HD hypermodel comparison
    all_results['curn_vs_hd'] = analyze_chain(
        os.path.join(presampled, 'curn_hd.core'),
        'CURN vs HD hypermodel',
        {'crn_log10_A': 'gw_crn_log10_A', 'hd_log10_A': 'gw_hd_log10_A'}
    )
    
    # 4. Free spectrum (30 freq bins)
    all_results['free_spectrum'] = analyze_free_spectrum(
        os.path.join(presampled, 'hd_30f_fs.core'),
        'HD 30-freq free-spectrum'
    )
    
    # 5. Spline ORF
    all_results['spline_orf'] = analyze_spline_orf(
        os.path.join(presampled, 'spline_orf_vg.core'),
        'Spline ORF varied-gamma'
    )
    
    # Summary comparison with paper
    print("\n" + "="*60)
    print("COMPARISON WITH PAPER VALUES")
    print("="*60)
    
    paper_vals = {
        'A_GWB': 2.4e-15,
        'log10_A': np.log10(2.4e-15),
        'gamma_SMBHB': 13/3,
        'note': 'Paper Table 1 values (varied-gamma CURN model)'
    }
    
    print(f"\nPaper: A_GWB = {paper_vals['A_GWB']:.2e}, log10(A) = {paper_vals['log10_A']:.4f}")
    print(f"Paper: gamma (SMBHB prediction) = {paper_vals['gamma_SMBHB']:.4f}")
    
    if 'log10_A' in all_results['curn']:
        our_A = all_results['curn']['log10_A']['median']
        our_gamma = all_results['curn']['gamma']['median']
        print(f"\nOur CURN: log10(A) = {our_A:.4f}, A = {10**our_A:.3e}")
        print(f"Our CURN: gamma = {our_gamma:.4f}")
        
        # Agreement check
        delta_A = abs(our_A - paper_vals['log10_A'])
        delta_gamma = abs(our_gamma - paper_vals['gamma_SMBHB'])
        sigma_A = all_results['curn']['log10_A']['std']
        sigma_gamma = all_results['curn']['gamma']['std']
        print(f"\nlog10(A) offset: {delta_A:.4f} ({delta_A/sigma_A:.1f}σ)")
        print(f"gamma offset: {delta_gamma:.4f} ({delta_gamma/sigma_gamma:.1f}σ)")
    
    if 'log10_A' in all_results['hd']:
        our_A_hd = all_results['hd']['log10_A']['median']
        our_gamma_hd = all_results['hd']['gamma']['median']
        print(f"\nOur HD: log10(A) = {our_A_hd:.4f}, A = {10**our_A_hd:.3e}")
        print(f"Our HD: gamma = {our_gamma_hd:.4f}")
    
    # Save results
    all_results['paper_reference'] = paper_vals
    
    outpath = os.path.join(RESULTS_DIR, 'posterior_results.json')
    
    # Convert numpy types for JSON serialization
    def convert(obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    with open(outpath, 'w') as f:
        json.dump(all_results, f, indent=2, default=convert)
    
    print(f"\nResults saved to {outpath}")
    return all_results


if __name__ == '__main__':
    main()
