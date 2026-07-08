#!/usr/bin/env python3
"""
fldgen v2.0 Replication — Main Script
======================================
Trains the emulator on synthetic ESM data, generates realizations,
and validates against the training data using the metrics described
in the fldgen v2.0 paper.

Produces:
- Comparison figures (spatial correlation, variance, distributions)
- Saved data (training data, generated realizations)
- Diagnostic statistics
"""

import sys
import os
import json
import numpy as np
from pathlib import Path

# Add code directory to path
CODEDIR = Path(__file__).parent
sys.path.insert(0, str(CODEDIR))

from fldgen import (train_tp, generate_resids, generate_fullgrids,
                    pscl_apply, normalize_resids, unnormalize_resids)
from synthetic_esm import generate_synthetic_esm

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy import stats as sp_stats


def setup_dirs():
    """Create output directories."""
    base = CODEDIR.parent
    (base / 'data').mkdir(exist_ok=True)
    (base / 'figures').mkdir(exist_ok=True)
    return base / 'data', base / 'figures'


def compute_spatial_correlation_matrix(fields, ngrid, sample_cells=50):
    """
    Compute pairwise Spearman rank correlation between a subset of grid cells
    across time (for one variable).
    """
    ntime = fields.shape[0]
    rng = np.random.default_rng(99)
    cells = rng.choice(ngrid, size=min(sample_cells, ngrid), replace=False)
    cells.sort()
    
    subset = fields[:, cells]
    corr = np.zeros((len(cells), len(cells)))
    for i in range(len(cells)):
        for j in range(i, len(cells)):
            r, _ = sp_stats.spearmanr(subset[:, i], subset[:, j])
            corr[i, j] = r
            corr[j, i] = r
    return corr, cells


def compute_variance_ratio(training_resids, gen_resids_list, ngrid):
    """Variance per grid cell: generated / training."""
    train_var = np.var(training_resids, axis=0)
    
    gen_vars = []
    for g in gen_resids_list:
        gen_vars.append(np.var(g, axis=0))
    gen_var_mean = np.mean(gen_vars, axis=0)
    
    ratio = gen_var_mean / np.maximum(train_var, 1e-20)
    return ratio, train_var, gen_var_mean


def compute_autocorrelation(ts, maxlag=10):
    """Compute autocorrelation function for a time series."""
    n = len(ts)
    ts_centered = ts - np.mean(ts)
    var = np.var(ts)
    if var < 1e-20:
        return np.zeros(maxlag + 1)
    acf = np.correlate(ts_centered, ts_centered, mode='full')
    acf = acf[n-1:]  # positive lags only
    acf = acf / (var * n)
    return acf[:maxlag + 1]


def main():
    print("=" * 70)
    print("fldgen v2.0 Replication")
    print("Python implementation of joint T-P field generation")
    print("=" * 70)
    
    datadir, figdir = setup_dirs()
    
    # =====================================================================
    # Step 1: Generate synthetic ESM data
    # =====================================================================
    print("\n[1] Generating synthetic ESM data...")
    esm = generate_synthetic_esm(nlat=24, nlon=48, nyears=95, seed=42)
    
    print(f"    Grid: {esm['nlat']}x{esm['nlon']} = {esm['ngrid']} cells")
    print(f"    Time: {esm['years'][0]}-{esm['years'][-1]} ({len(esm['years'])} yr)")
    print(f"    T range: {esm['tas'].min():.1f} - {esm['tas'].max():.1f} K")
    print(f"    P range: {esm['pr'].min():.2e} - {esm['pr'].max():.2e} kg/m2/s")
    print(f"    Tgav: {esm['tgav'][0]:.2f} -> {esm['tgav'][-1]:.2f} K")
    
    # Save training data
    np.savez_compressed(str(datadir / 'training_data.npz'),
                        tas=esm['tas'], pr=esm['pr'], tgav=esm['tgav'],
                        lat=esm['lat'], lon=esm['lon'], years=esm['years'])
    
    # =====================================================================
    # Step 2: Train the emulator
    # =====================================================================
    print("\n[2] Training fldgen v2.0 emulator...")
    emulator = train_tp(
        tdata=esm['tas'],
        pdata=esm['pr'],
        lat=esm['lat'],
        lon=esm['lon'],
        tgav=esm['tgav'],
        p_transform=np.log,
        p_floor=1e-9
    )
    
    print(f"    EOF components: {emulator.reof.rotation.shape[1]}")
    print(f"    Variance explained (top 5): " + 
          ", ".join([f"{v:.4f}" for v in emulator.reof.sdev[:5]**2 / 
                     np.sum(emulator.reof.sdev**2)]))
    
    # =====================================================================
    # Step 3: Generate new realizations
    # =====================================================================
    NGEN = 10
    print(f"\n[3] Generating {NGEN} new realizations...")
    
    np.random.seed(123)
    resid_grids = generate_resids(emulator, ngen=NGEN, method=1)
    full_grids, mf_t, mf_p = generate_fullgrids(
        emulator, resid_grids, tgav=esm['tgav'], p_inverse=np.exp)
    
    print(f"    Generated {len(full_grids)} realizations")
    for i, fg in enumerate(full_grids[:3]):
        print(f"    Realization {i}: T [{fg['tas'].min():.1f}, {fg['tas'].max():.1f}] K, "
              f"P [{fg['pr'].min():.2e}, {fg['pr'].max():.2e}] kg/m2/s")
    
    # Save generated data
    for i, fg in enumerate(full_grids):
        np.savez_compressed(str(datadir / f'realization_{i:02d}.npz'),
                            tas=fg['tas'], pr=fg['pr'])
    
    # =====================================================================
    # Step 4: Validation
    # =====================================================================
    print("\n[4] Validation...")
    ngrid = emulator.ngrid
    nlat, nlon = esm['nlat'], esm['nlon']
    
    # --- 4a: Spatial correlation preservation ---
    print("    Computing spatial rank correlations...")
    
    # Training data residuals (in T space)
    train_t_resid = emulator.meanfld_t.r
    gen_t_resids = [rg[:, :ngrid] for rg in resid_grids]
    
    train_corr, sample_cells = compute_spatial_correlation_matrix(
        train_t_resid, ngrid, sample_cells=40)
    
    gen_corrs = []
    for rg in gen_t_resids[:5]:
        gc, _ = compute_spatial_correlation_matrix(rg, ngrid, sample_cells=40)
        gen_corrs.append(gc)
    gen_corr_mean = np.mean(gen_corrs, axis=0)
    
    # --- 4b: Variance ratio ---
    print("    Computing variance ratios...")
    var_ratio_t, train_var_t, gen_var_t = compute_variance_ratio(
        train_t_resid, gen_t_resids, ngrid)
    
    train_p_resid = emulator.meanfld_p.r  # log(P) residuals
    gen_p_resids = [rg[:, ngrid:] for rg in resid_grids]
    var_ratio_p, train_var_p, gen_var_p = compute_variance_ratio(
        train_p_resid, gen_p_resids, ngrid)
    
    # --- 4c: Autocorrelation ---
    print("    Computing temporal autocorrelation...")
    maxlag = 10
    
    # Pick a few representative grid cells
    cells_acf = [ngrid//4, ngrid//2, 3*ngrid//4]
    train_acfs = []
    gen_acfs_all = []
    for c in cells_acf:
        tacf = compute_autocorrelation(train_t_resid[:, c], maxlag)
        train_acfs.append(tacf)
        
        gacfs = []
        for rg in gen_t_resids:
            gacf = compute_autocorrelation(rg[:, c], maxlag)
            gacfs.append(gacf)
        gen_acfs_all.append(np.mean(gacfs, axis=0))
    
    # --- 4d: Cross-variable correlation ---
    print("    Computing cross-variable correlations...")
    train_cross = []
    gen_cross = []
    for c in range(min(ngrid, 200)):
        r, _ = sp_stats.spearmanr(train_t_resid[:, c], train_p_resid[:, c])
        train_cross.append(r)
        
        gc = []
        for k in range(len(gen_t_resids)):
            rg, _ = sp_stats.spearmanr(gen_t_resids[k][:, c], gen_p_resids[k][:, c])
            gc.append(rg)
        gen_cross.append(np.mean(gc))
    
    train_cross = np.array(train_cross)
    gen_cross = np.array(gen_cross)
    
    # --- 4e: Marginal distribution check ---
    print("    Checking marginal distributions...")
    ks_pvalues_t = []
    ks_pvalues_p = []
    for c in range(min(ngrid, 200)):
        # KS test: training vs mean of generated for each cell
        combined_gen = np.concatenate([rg[:, c] for rg in gen_t_resids])
        ks_stat, ks_p = sp_stats.ks_2samp(train_t_resid[:, c], combined_gen)
        ks_pvalues_t.append(ks_p)
        
        combined_gen_p = np.concatenate([rg[:, c] for rg in gen_p_resids])
        ks_stat_p, ks_p_p = sp_stats.ks_2samp(train_p_resid[:, c], combined_gen_p)
        ks_pvalues_p.append(ks_p_p)
    
    ks_pvalues_t = np.array(ks_pvalues_t)
    ks_pvalues_p = np.array(ks_pvalues_p)
    
    # =====================================================================
    # Step 5: Generate Figures
    # =====================================================================
    print("\n[5] Generating figures...")
    
    # ---- Figure 1: Overview (6-panel) ----
    fig = plt.figure(figsize=(18, 24))
    gs = GridSpec(4, 2, hspace=0.35, wspace=0.3)
    
    # 1a: Training vs Generated T field (one time slice)
    ax1 = fig.add_subplot(gs[0, 0])
    t_slice = 47  # mid-century
    im1 = ax1.imshow(esm['tas'][t_slice].reshape(nlat, nlon),
                     cmap='RdBu_r', aspect='auto',
                     extent=[0, 360, -90, 90])
    ax1.set_title(f'Training: T field (year {esm["years"][t_slice]})', fontsize=12)
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    plt.colorbar(im1, ax=ax1, label='T (K)')
    
    ax2 = fig.add_subplot(gs[0, 1])
    im2 = ax2.imshow(full_grids[0]['tas'][t_slice].reshape(nlat, nlon),
                     cmap='RdBu_r', aspect='auto',
                     extent=[0, 360, -90, 90])
    ax2.set_title(f'Generated: T field (realization 1, year {esm["years"][t_slice]})', fontsize=12)
    ax2.set_xlabel('Longitude')
    ax2.set_ylabel('Latitude')
    plt.colorbar(im2, ax=ax2, label='T (K)')
    
    # 1b: Spatial correlation matrices
    ax3 = fig.add_subplot(gs[1, 0])
    im3 = ax3.imshow(train_corr, cmap='RdBu_r', vmin=-1, vmax=1, aspect='equal')
    ax3.set_title('Training: T spatial rank correlation', fontsize=12)
    ax3.set_xlabel('Grid cell index')
    ax3.set_ylabel('Grid cell index')
    plt.colorbar(im3, ax=ax3)
    
    ax4 = fig.add_subplot(gs[1, 1])
    im4 = ax4.imshow(gen_corr_mean, cmap='RdBu_r', vmin=-1, vmax=1, aspect='equal')
    ax4.set_title('Generated (mean): T spatial rank correlation', fontsize=12)
    ax4.set_xlabel('Grid cell index')
    ax4.set_ylabel('Grid cell index')
    plt.colorbar(im4, ax=ax4)
    
    # 1c: Variance ratio histograms
    ax5 = fig.add_subplot(gs[2, 0])
    ax5.hist(var_ratio_t, bins=40, alpha=0.7, color='steelblue', edgecolor='black')
    ax5.axvline(1.0, color='red', linestyle='--', linewidth=2, label='Perfect (1.0)')
    ax5.set_xlabel('Variance Ratio (Generated / Training)')
    ax5.set_ylabel('Count')
    ax5.set_title(f'T Variance Ratio (median={np.median(var_ratio_t):.3f})', fontsize=12)
    ax5.legend()
    ax5.set_xlim(0, 3)
    
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.hist(var_ratio_p, bins=40, alpha=0.7, color='forestgreen', edgecolor='black')
    ax6.axvline(1.0, color='red', linestyle='--', linewidth=2, label='Perfect (1.0)')
    ax6.set_xlabel('Variance Ratio (Generated / Training)')
    ax6.set_ylabel('Count')
    ax6.set_title(f'log(P) Variance Ratio (median={np.median(var_ratio_p):.3f})', fontsize=12)
    ax6.legend()
    ax6.set_xlim(0, 3)
    
    # 1d: Cross-variable correlation
    ax7 = fig.add_subplot(gs[3, 0])
    ax7.scatter(train_cross, gen_cross, alpha=0.4, s=10, c='purple')
    lims = [min(train_cross.min(), gen_cross.min()) - 0.1,
            max(train_cross.max(), gen_cross.max()) + 0.1]
    ax7.plot(lims, lims, 'r--', linewidth=1.5, label='1:1 line')
    ax7.set_xlabel('Training: Spearman(T, log(P))')
    ax7.set_ylabel('Generated: Spearman(T, log(P))')
    ax7.set_title('Cross-Variable Rank Correlation', fontsize=12)
    ax7.legend()
    ax7.set_xlim(lims)
    ax7.set_ylim(lims)
    
    # 1e: Temporal autocorrelation
    ax8 = fig.add_subplot(gs[3, 1])
    lags = np.arange(maxlag + 1)
    colors_acf = ['steelblue', 'coral', 'forestgreen']
    for idx, c in enumerate(cells_acf):
        ax8.plot(lags, train_acfs[idx], 'o-', color=colors_acf[idx],
                label=f'Training (cell {c})', markersize=4)
        ax8.plot(lags, gen_acfs_all[idx], 's--', color=colors_acf[idx],
                alpha=0.7, label=f'Generated (cell {c})', markersize=4)
    ax8.set_xlabel('Lag (years)')
    ax8.set_ylabel('Autocorrelation')
    ax8.set_title('T Residual Temporal Autocorrelation', fontsize=12)
    ax8.legend(fontsize=8, ncol=2)
    ax8.axhline(0, color='gray', linewidth=0.5)
    
    plt.savefig(str(figdir / 'fig1_overview.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    Saved fig1_overview.png")
    
    # ---- Figure 2: Marginal distributions ----
    fig2, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    # Pick 3 representative cells
    repr_cells = [ngrid//6, ngrid//2, 5*ngrid//6]
    
    for idx, c in enumerate(repr_cells):
        # Temperature
        ax = axes[0, idx]
        ax.hist(train_t_resid[:, c], bins=20, density=True, alpha=0.6,
               color='steelblue', edgecolor='black', label='Training')
        combined = np.concatenate([rg[:, c] for rg in gen_t_resids])
        ax.hist(combined, bins=20, density=True, alpha=0.4,
               color='coral', edgecolor='black', label='Generated')
        lat_idx = c // nlon
        lon_idx = c % nlon
        ax.set_title(f'T residual (lat={esm["lat"][lat_idx]:.0f}°, lon={esm["lon"][lon_idx]:.0f}°)',
                    fontsize=10)
        ax.set_xlabel('T residual (K)')
        ax.set_ylabel('Density')
        ax.legend(fontsize=8)
        
        # Precipitation
        ax = axes[1, idx]
        ax.hist(train_p_resid[:, c], bins=20, density=True, alpha=0.6,
               color='forestgreen', edgecolor='black', label='Training')
        combined_p = np.concatenate([rg[:, c] for rg in gen_p_resids])
        ax.hist(combined_p, bins=20, density=True, alpha=0.4,
               color='coral', edgecolor='black', label='Generated')
        ax.set_title(f'log(P) residual (lat={esm["lat"][lat_idx]:.0f}°, lon={esm["lon"][lon_idx]:.0f}°)',
                    fontsize=10)
        ax.set_xlabel('log(P) residual')
        ax.set_ylabel('Density')
        ax.legend(fontsize=8)
    
    fig2.suptitle('Marginal Distributions: Training vs Generated', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(str(figdir / 'fig2_marginals.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    Saved fig2_marginals.png")
    
    # ---- Figure 3: Global mean T and time series ----
    fig3, axes3 = plt.subplots(2, 1, figsize=(14, 8))
    
    # 3a: Global mean T
    ax = axes3[0]
    ax.plot(esm['years'], esm['tgav'], 'k-', linewidth=2, label='Training Tgav')
    
    cos_weights = np.cos(np.deg2rad(np.repeat(esm['lat'], nlon)))
    cos_weights = cos_weights / cos_weights.sum()
    
    for i in range(min(5, NGEN)):
        gen_tgav = full_grids[i]['tas'] @ cos_weights
        ax.plot(esm['years'], gen_tgav, '-', alpha=0.5, linewidth=1,
               label=f'Generated #{i}' if i < 3 else None)
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Global Mean T (K)')
    ax.set_title('Global Mean Temperature: Training vs Generated', fontsize=12)
    ax.legend(fontsize=9)
    
    # 3b: Time series at a single grid cell
    ax = axes3[1]
    mid_cell = ngrid // 2
    lat_idx = mid_cell // nlon
    lon_idx = mid_cell % nlon
    
    ax.plot(esm['years'], esm['tas'][:, mid_cell], 'k-', linewidth=2, label='Training')
    for i in range(min(5, NGEN)):
        ax.plot(esm['years'], full_grids[i]['tas'][:, mid_cell], '-', alpha=0.5, linewidth=1,
               label=f'Generated #{i}' if i < 3 else None)
    
    ax.set_xlabel('Year')
    ax.set_ylabel('T (K)')
    ax.set_title(f'T at ({esm["lat"][lat_idx]:.0f}°N, {esm["lon"][lon_idx]:.0f}°E)', fontsize=12)
    ax.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(str(figdir / 'fig3_timeseries.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    Saved fig3_timeseries.png")
    
    # ---- Figure 4: Spatial correlation scatter (training vs generated) ----
    fig4, ax4 = plt.subplots(1, 1, figsize=(8, 8))
    
    # Extract upper triangle of both correlation matrices
    mask = np.triu(np.ones_like(train_corr, dtype=bool), k=1)
    train_vals = train_corr[mask]
    gen_vals = gen_corr_mean[mask]
    
    ax4.scatter(train_vals, gen_vals, alpha=0.3, s=8, c='steelblue')
    ax4.plot([-1, 1], [-1, 1], 'r--', linewidth=1.5)
    ax4.set_xlabel('Training Spearman Correlation')
    ax4.set_ylabel('Generated Spearman Correlation (mean)')
    ax4.set_title('Spatial Rank Correlation: Training vs Generated\n(T residuals, pairwise between 40 grid cells)')
    
    corr_rmse = np.sqrt(np.mean((train_vals - gen_vals)**2))
    corr_r, _ = sp_stats.pearsonr(train_vals, gen_vals)
    ax4.text(0.05, 0.95, f'RMSE = {corr_rmse:.4f}\nPearson r = {corr_r:.4f}',
            transform=ax4.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(str(figdir / 'fig4_spatial_corr_scatter.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    Saved fig4_spatial_corr_scatter.png")
    
    # =====================================================================
    # Step 6: Summary Statistics
    # =====================================================================
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    results = {}
    
    # Spatial correlation
    results['spatial_corr_rmse'] = float(corr_rmse)
    results['spatial_corr_pearsonr'] = float(corr_r)
    print(f"\nSpatial Rank Correlation Preservation:")
    print(f"  RMSE between training and generated: {corr_rmse:.4f}")
    print(f"  Pearson r: {corr_r:.4f}")
    
    # Variance ratio
    results['var_ratio_t_median'] = float(np.median(var_ratio_t))
    results['var_ratio_t_iqr'] = [float(np.percentile(var_ratio_t, 25)),
                                    float(np.percentile(var_ratio_t, 75))]
    results['var_ratio_p_median'] = float(np.median(var_ratio_p))
    results['var_ratio_p_iqr'] = [float(np.percentile(var_ratio_p, 25)),
                                    float(np.percentile(var_ratio_p, 75))]
    print(f"\nVariance Ratio (Generated / Training):")
    print(f"  T: median = {results['var_ratio_t_median']:.3f}, "
          f"IQR = [{results['var_ratio_t_iqr'][0]:.3f}, {results['var_ratio_t_iqr'][1]:.3f}]")
    print(f"  P: median = {results['var_ratio_p_median']:.3f}, "
          f"IQR = [{results['var_ratio_p_iqr'][0]:.3f}, {results['var_ratio_p_iqr'][1]:.3f}]")
    
    # Cross-variable correlation
    cross_rmse = np.sqrt(np.mean((train_cross - gen_cross)**2))
    cross_r, _ = sp_stats.pearsonr(train_cross, gen_cross)
    results['cross_var_corr_rmse'] = float(cross_rmse)
    results['cross_var_corr_pearsonr'] = float(cross_r)
    print(f"\nCross-Variable Correlation (T vs log(P)):")
    print(f"  RMSE: {cross_rmse:.4f}")
    print(f"  Pearson r: {cross_r:.4f}")
    
    # Marginal distribution preservation
    frac_pass_t = np.mean(ks_pvalues_t > 0.05)
    frac_pass_p = np.mean(ks_pvalues_p > 0.05)
    results['ks_test_t_frac_pass'] = float(frac_pass_t)
    results['ks_test_p_frac_pass'] = float(frac_pass_p)
    print(f"\nMarginal Distribution (KS test, p>0.05 = pass):")
    print(f"  T: {frac_pass_t*100:.1f}% of grid cells pass")
    print(f"  P: {frac_pass_p*100:.1f}% of grid cells pass")
    
    # ACF comparison
    acf_errors = []
    for idx in range(len(cells_acf)):
        ae = np.mean(np.abs(train_acfs[idx] - gen_acfs_all[idx]))
        acf_errors.append(ae)
    results['acf_mean_abs_error'] = float(np.mean(acf_errors))
    print(f"\nTemporal Autocorrelation:")
    print(f"  Mean absolute error (ACF): {np.mean(acf_errors):.4f}")
    
    # EOF explained variance
    eof_var = emulator.reof.sdev**2
    eof_var_frac = eof_var / eof_var.sum()
    cumvar = np.cumsum(eof_var_frac)
    n90 = np.searchsorted(cumvar, 0.9) + 1
    results['eof_components_total'] = int(len(eof_var))
    results['eof_components_90pct'] = int(n90)
    results['eof_top5_variance_frac'] = [float(v) for v in eof_var_frac[:5]]
    print(f"\nEOF Decomposition:")
    print(f"  Total components: {len(eof_var)}")
    print(f"  Components for 90% variance: {n90}")
    print(f"  Top 5 variance fractions: {[f'{v:.4f}' for v in eof_var_frac[:5]]}")
    
    # Physical consistency
    for i in range(min(3, NGEN)):
        neg_pr = np.sum(full_grids[i]['pr'] < 0)
        results[f'neg_pr_realization_{i}'] = int(neg_pr)
        if neg_pr > 0:
            print(f"\n  WARNING: Realization {i} has {neg_pr} negative precipitation values")
    
    print(f"\n  All realizations have non-negative precipitation: ",
          all(np.all(fg['pr'] >= 0) for fg in full_grids))
    
    # Save results
    with open(str(datadir / 'validation_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'=' * 70}")
    print(f"Results saved to: {datadir / 'validation_results.json'}")
    print(f"Figures saved to: {figdir}")
    print(f"{'=' * 70}")
    
    return results


if __name__ == '__main__':
    results = main()
