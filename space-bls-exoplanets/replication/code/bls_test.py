#!/usr/bin/env python3
"""
BLS replication test driver.

Downloads Kepler/TESS lightcurves for known transiting exoplanets,
runs our from-scratch BLS implementation + astropy.timeseries.BoxLeastSquares,
and compares recovered periods/depths to published values.

Targets (known transiting planets):
  1. Kepler-10 b   — P = 0.8375 d, depth ~150 ppm (hard: short period, shallow)
  2. HAT-P-7 b     — P = 2.2047 d, depth ~6300 ppm (easy: deep transit)
  3. TrES-2 b      — P = 2.4706 d, depth ~16000 ppm (easy: very deep)
  4. Kepler-5 b    — P = 3.5485 d, depth ~7000 ppm
  5. Kepler-8 b    — P = 3.5225 d, depth ~9400 ppm
  6. Kepler-6 b    — P = 3.2347 d, depth ~9500 ppm

We use single-quarter Kepler data to keep downloads fast.

Author: Ollie (OpenClaw subagent), 2026-04-30
"""

import sys
import os
import json
import time as pytime
import warnings
import numpy as np

# Suppress noisy warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*oktopus.*")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Our BLS implementation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bls_kovacs2002 import bls_fast, phase_fold_lightcurve, BLSResult

# Astropy BLS for comparison
from astropy.timeseries import BoxLeastSquares
import astropy.units as u

import lightkurve as lk


# ─── Target definitions ───────────────────────────────────────────────────────
TARGETS = [
    {
        "name": "HAT-P-7 b",
        "search_name": "HAT-P-7",
        "mission": "Kepler",
        "quarter": 3,
        "known_period": 2.204737,    # days
        "known_depth": 6300e-6,      # fractional (ppm / 1e6)
        "period_min": 0.5,
        "period_max": 10.0,
    },
    {
        "name": "TrES-2 b",
        "search_name": "TrES-2",
        "mission": "Kepler",
        "quarter": 3,
        "known_period": 2.470614,
        "known_depth": 16000e-6,
        "period_min": 0.5,
        "period_max": 10.0,
    },
    {
        "name": "Kepler-5 b",
        "search_name": "Kepler-5",
        "mission": "Kepler",
        "quarter": 3,
        "known_period": 3.54846,
        "known_depth": 7000e-6,
        "period_min": 1.0,
        "period_max": 15.0,
    },
    {
        "name": "Kepler-6 b",
        "search_name": "Kepler-6",
        "mission": "Kepler",
        "quarter": 3,
        "known_period": 3.23470,
        "known_depth": 9500e-6,
        "period_min": 1.0,
        "period_max": 15.0,
    },
    {
        "name": "Kepler-8 b",
        "search_name": "Kepler-8",
        "mission": "Kepler",
        "quarter": 3,
        "known_period": 3.52254,
        "known_depth": 9400e-6,
        "period_min": 1.0,
        "period_max": 15.0,
    },
    {
        "name": "Kepler-10 b",
        "search_name": "Kepler-10",
        "mission": "Kepler",
        "quarter": 3,
        "known_period": 0.837495,
        "known_depth": 150e-6,
        "period_min": 0.3,
        "period_max": 5.0,
    },
]


def download_lightcurve(target):
    """Download and clean a Kepler lightcurve."""
    print(f"  Downloading {target['search_name']} Q{target['quarter']}...")
    search = lk.search_lightcurve(
        target["search_name"],
        mission=target["mission"],
        quarter=target["quarter"],
        author="Kepler",
        cadence="long",
    )
    if len(search) == 0:
        # Try without specifying quarter
        print(f"    No Q{target['quarter']} data, trying any quarter...")
        search = lk.search_lightcurve(
            target["search_name"],
            mission=target["mission"],
            author="Kepler",
            cadence="long",
        )
        if len(search) == 0:
            raise RuntimeError(f"No data found for {target['search_name']}")
        # Take first available
        lc = search[0].download()
    else:
        lc = search[0].download()

    # Use PDCSAP flux, normalise, remove NaNs
    lc = lc.remove_nans().normalize()

    time = lc.time.value
    flux = lc.flux.value
    flux_err = lc.flux_err.value if hasattr(lc, 'flux_err') and lc.flux_err is not None else None

    # Sigma clip
    median = np.median(flux)
    std = np.std(flux)
    mask = np.abs(flux - median) < 5 * std
    time = time[mask]
    flux = flux[mask]
    if flux_err is not None:
        flux_err = flux_err[mask]

    print(f"    Got {len(time)} points over {time[-1]-time[0]:.1f} days")
    return time, flux, flux_err


def run_astropy_bls(time, flux, flux_err, target):
    """Run astropy's BoxLeastSquares for comparison."""
    if flux_err is not None:
        model = BoxLeastSquares(time * u.day, flux, dy=flux_err)
    else:
        model = BoxLeastSquares(time * u.day, flux)

    periods = np.linspace(target["period_min"], target["period_max"], 10000) * u.day
    # Ensure max duration < min period (astropy requirement)
    max_dur = min(0.3, target["period_min"] * 0.4)
    durations = np.linspace(0.01, max_dur, 20) * u.day

    result = model.power(periods, durations)

    best_idx = np.argmax(result.power)
    best_period = result.period[best_idx].value
    best_depth = result.depth[best_idx]
    # depth may be a Quantity
    if hasattr(best_depth, 'value'):
        best_depth = best_depth.value

    return {
        "best_period": best_period,
        "best_depth": float(best_depth),
        "periods": result.period.value,
        "power": result.power,
    }


def run_one_target(target, fig_dir, n_periods=10000):
    """Process a single target: download, run BLS, compare, plot."""
    print(f"\n{'='*60}")
    print(f"  TARGET: {target['name']}")
    print(f"  Known period: {target['known_period']:.6f} d")
    print(f"  Known depth:  {target['known_depth']*1e6:.0f} ppm")
    print(f"{'='*60}")

    # Download
    time, flux, flux_err = download_lightcurve(target)

    # Run our BLS
    t0 = pytime.time()
    our_result = bls_fast(
        time, flux, flux_err,
        period_min=target["period_min"],
        period_max=target["period_max"],
        n_periods=n_periods,
        n_bins=300,
        n_durations=30,
    )
    our_time = pytime.time() - t0
    print(f"  Our BLS: period={our_result.best_period:.6f} d, "
          f"depth={our_result.best_depth*1e6:.0f} ppm, "
          f"SDE={our_result.sde:.1f}, "
          f"time={our_time:.1f}s")

    # Run astropy BLS
    t0 = pytime.time()
    astropy_result = run_astropy_bls(time, flux, flux_err, target)
    astropy_time = pytime.time() - t0
    print(f"  Astropy BLS: period={astropy_result['best_period']:.6f} d, "
          f"depth={astropy_result['best_depth']*1e6:.0f} ppm, "
          f"time={astropy_time:.1f}s")

    # Period recovery metrics
    known_p = target["known_period"]
    our_p = our_result.best_period
    astropy_p = astropy_result["best_period"]

    # Check for harmonic aliases (P/2, 2P, P/3, 3P)
    def best_harmonic_match(recovered, known):
        """Check if recovered period matches known or a harmonic."""
        harmonics = [1, 2, 3, 0.5, 1/3]
        best_frac_err = abs(recovered - known) / known
        best_mult = 1
        for h in harmonics:
            err = abs(recovered - known * h) / (known * h)
            if err < best_frac_err:
                best_frac_err = err
                best_mult = h
        return best_frac_err, best_mult

    our_frac_err, our_harmonic = best_harmonic_match(our_p, known_p)
    astropy_frac_err, astropy_harmonic = best_harmonic_match(astropy_p, known_p)

    our_depth_err = abs(our_result.best_depth - target["known_depth"]) / target["known_depth"] if target["known_depth"] > 0 else 0

    print(f"  Our period error: {our_frac_err*100:.3f}% "
          f"(harmonic: {our_harmonic}x)")
    print(f"  Astropy period error: {astropy_frac_err*100:.3f}% "
          f"(harmonic: {astropy_harmonic}x)")

    # ─── Plot ──────────────────────────────────────────────────────────────
    safe_name = target["name"].replace(" ", "_")
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)
    fig.suptitle(f"{target['name']} — BLS Transit Search", fontsize=14, fontweight='bold')

    # 1. Raw lightcurve
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(time, flux, '.', ms=0.5, alpha=0.5, color='gray')
    ax1.set_xlabel("Time (BJD - 2454833)")
    ax1.set_ylabel("Normalised Flux")
    ax1.set_title("Raw PDCSAP Lightcurve")

    # 2. Our BLS power spectrum
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(our_result.periods, our_result.sde_spectrum, 'b-', lw=0.5)
    ax2.axvline(known_p, color='r', ls='--', alpha=0.7, label=f"Known P={known_p:.4f}")
    ax2.axvline(our_result.best_period, color='g', ls=':', alpha=0.7,
                label=f"Found P={our_result.best_period:.4f}")
    ax2.set_xlabel("Period (days)")
    ax2.set_ylabel("SDE")
    ax2.set_title("Our BLS (KZM02)")
    ax2.legend(fontsize=8)

    # 3. Astropy BLS power spectrum
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(astropy_result["periods"], astropy_result["power"], 'b-', lw=0.5)
    ax3.axvline(known_p, color='r', ls='--', alpha=0.7, label=f"Known P={known_p:.4f}")
    ax3.axvline(astropy_result["best_period"], color='g', ls=':', alpha=0.7,
                label=f"Found P={astropy_result['best_period']:.4f}")
    ax3.set_xlabel("Period (days)")
    ax3.set_ylabel("Power")
    ax3.set_title("Astropy BLS")
    ax3.legend(fontsize=8)

    # 4. Phase-folded lightcurve (our result)
    phase_our, flux_our = phase_fold_lightcurve(time, flux, our_result.best_period, our_result.best_t0)
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.plot(phase_our, flux_our, '.', ms=0.5, alpha=0.3, color='gray')
    # Bin for clarity
    n_show_bins = 100
    phase_bins = np.linspace(-0.5, 0.5, n_show_bins + 1)
    bin_centers = 0.5 * (phase_bins[:-1] + phase_bins[1:])
    bin_flux = np.array([np.median(flux_our[(phase_our >= phase_bins[i]) & (phase_our < phase_bins[i+1])])
                         if np.sum((phase_our >= phase_bins[i]) & (phase_our < phase_bins[i+1])) > 0
                         else np.nan
                         for i in range(n_show_bins)])
    ax4.plot(bin_centers, bin_flux, 'r-', lw=1.5)
    ax4.set_xlabel("Phase")
    ax4.set_ylabel("Flux")
    ax4.set_title(f"Phase-folded (our P={our_result.best_period:.4f} d)")
    ax4.set_xlim(-0.2, 0.2)

    # 5. Phase-folded at known period
    phase_known, flux_known = phase_fold_lightcurve(time, flux, known_p, our_result.best_t0)
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.plot(phase_known, flux_known, '.', ms=0.5, alpha=0.3, color='gray')
    bin_flux_known = np.array([np.median(flux_known[(phase_known >= phase_bins[i]) & (phase_known < phase_bins[i+1])])
                               if np.sum((phase_known >= phase_bins[i]) & (phase_known < phase_bins[i+1])) > 0
                               else np.nan
                               for i in range(n_show_bins)])
    ax5.plot(bin_centers, bin_flux_known, 'r-', lw=1.5)
    ax5.set_xlabel("Phase")
    ax5.set_ylabel("Flux")
    ax5.set_title(f"Phase-folded (known P={known_p:.4f} d)")
    ax5.set_xlim(-0.2, 0.2)

    plt.savefig(os.path.join(fig_dir, f"{safe_name}.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved figure: {safe_name}.png")

    return {
        "name": target["name"],
        "known_period": known_p,
        "known_depth_ppm": target["known_depth"] * 1e6,
        "our_period": float(our_result.best_period),
        "our_depth_ppm": float(our_result.best_depth * 1e6),
        "our_sde": float(our_result.sde),
        "our_duration": float(our_result.best_duration),
        "our_period_error_pct": float(our_frac_err * 100),
        "our_harmonic": float(our_harmonic),
        "our_time_s": float(our_time),
        "astropy_period": float(astropy_p),
        "astropy_depth_ppm": float(astropy_result["best_depth"] * 1e6),
        "astropy_period_error_pct": float(astropy_frac_err * 100),
        "astropy_harmonic": float(astropy_harmonic),
        "astropy_time_s": float(astropy_time),
        "n_datapoints": len(time),
        "timespan_days": float(time[-1] - time[0]),
    }


def make_summary_plot(results, fig_dir):
    """Create summary comparison plot."""
    names = [r["name"] for r in results]
    known_p = [r["known_period"] for r in results]
    our_p = [r["our_period"] for r in results]
    astropy_p = [r["astropy_period"] for r in results]
    our_err = [r["our_period_error_pct"] for r in results]
    astropy_err = [r["astropy_period_error_pct"] for r in results]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # 1. Period recovery scatter
    ax = axes[0]
    pmin = min(known_p) * 0.8
    pmax = max(known_p) * 1.2
    ax.plot([pmin, pmax], [pmin, pmax], 'k--', alpha=0.3)
    ax.scatter(known_p, our_p, c='blue', marker='o', s=80, label='Our BLS', zorder=5)
    ax.scatter(known_p, astropy_p, c='red', marker='s', s=60, label='Astropy BLS', zorder=5, alpha=0.7)
    for i, name in enumerate(names):
        ax.annotate(name.split()[0], (known_p[i], our_p[i]),
                    textcoords="offset points", xytext=(5, 5), fontsize=7)
    ax.set_xlabel("Known Period (days)")
    ax.set_ylabel("Recovered Period (days)")
    ax.set_title("Period Recovery")
    ax.legend(fontsize=9)
    ax.set_aspect('equal', adjustable='box')

    # 2. Error bars
    ax = axes[1]
    x = np.arange(len(names))
    ax.bar(x - 0.15, our_err, 0.3, label='Our BLS', color='steelblue')
    ax.bar(x + 0.15, astropy_err, 0.3, label='Astropy', color='salmon')
    ax.set_xticks(x)
    ax.set_xticklabels([n.replace(" b", "") for n in names], rotation=45, ha='right', fontsize=8)
    ax.set_ylabel("Period Error (%)")
    ax.set_title("Period Recovery Error")
    ax.legend(fontsize=9)
    ax.set_yscale("log")
    ax.set_ylim(bottom=0.001)

    # 3. SDE values
    ax = axes[2]
    sde_vals = [r["our_sde"] for r in results]
    colors = ['green' if s > 6 else 'orange' if s > 3 else 'red' for s in sde_vals]
    ax.barh(x, sde_vals, color=colors)
    ax.axvline(6, color='green', ls='--', alpha=0.5, label='SDE=6 threshold')
    ax.set_yticks(x)
    ax.set_yticklabels([n.replace(" b", "") for n in names], fontsize=8)
    ax.set_xlabel("SDE")
    ax.set_title("Signal Detection Efficiency")
    ax.legend(fontsize=9)

    plt.suptitle("BLS Replication — Period Recovery Summary", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "summary_comparison.png"), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n  Saved summary figure: summary_comparison.png")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fig_dir = os.path.join(base_dir, "figures")
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    results = []
    for target in TARGETS:
        try:
            r = run_one_target(target, fig_dir, n_periods=10000)
            results.append(r)
        except Exception as e:
            print(f"\n  *** FAILED: {target['name']}: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                "name": target["name"],
                "known_period": target["known_period"],
                "known_depth_ppm": target["known_depth"] * 1e6,
                "error": str(e),
            })

    # Save JSON results
    results_path = os.path.join(results_dir, "bls_results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to {results_path}")

    # Summary plot (only for successful results)
    good = [r for r in results if "error" not in r]
    if good:
        make_summary_plot(good, fig_dir)

    # Print summary table
    print(f"\n{'='*80}")
    print(f"  SUMMARY TABLE")
    print(f"{'='*80}")
    print(f"  {'Target':<14} {'Known P':>8} {'Our P':>8} {'Err%':>7} "
          f"{'Astropy P':>9} {'Err%':>7} {'SDE':>6} {'Depth(ppm)':>10}")
    print(f"  {'-'*14} {'-'*8} {'-'*8} {'-'*7} {'-'*9} {'-'*7} {'-'*6} {'-'*10}")
    for r in results:
        if "error" in r:
            print(f"  {r['name']:<14} {r['known_period']:>8.4f}  FAILED: {r['error'][:40]}")
        else:
            print(f"  {r['name']:<14} {r['known_period']:>8.4f} {r['our_period']:>8.4f} "
                  f"{r['our_period_error_pct']:>6.3f}% "
                  f"{r['astropy_period']:>9.4f} {r['astropy_period_error_pct']:>6.3f}% "
                  f"{r['our_sde']:>6.1f} {r['our_depth_ppm']:>10.0f}")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
