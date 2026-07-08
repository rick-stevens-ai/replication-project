"""
Box Least Squares (BLS) — from-scratch implementation.

Reference:
  Kovács, Zucker & Mazeh (2002) A&A 391, 369–377
  "A box-fitting algorithm in the search for periodic transits"

  Hartman & Bakos (2016) Astronomy & Computing 17, 1–7
  "vartools: A program for analyzing astronomical time-series data"
  (describes the fast O(N) binning approach)

This module implements:
  1. The brute-force BLS statistic (eq 3–6 of KZM02)
  2. The Signal Detection Efficiency (SDE) statistic
  3. A phase-binned fast BLS following the Hartman & Bakos optimisation

Author: Ollie (OpenClaw subagent), 2026-04-30
"""

import numpy as np
from typing import NamedTuple, Optional


class BLSResult(NamedTuple):
    """Container for BLS search results."""
    periods: np.ndarray          # trial periods
    power: np.ndarray            # BLS power (SR statistic) at each period
    best_period: float           # period of maximum power
    best_duration: float         # best-fit transit duration
    best_t0: float               # best-fit epoch (mid-transit)
    best_depth: float            # best-fit transit depth (positive = dimming)
    sde: float                   # Signal Detection Efficiency at best period
    sde_spectrum: np.ndarray     # SDE at each trial period


def _phase_fold(time, period, t0=0.0):
    """Phase-fold time array to [0, 1)."""
    return ((time - t0) / period) % 1.0


def bls_bruteforce(time, flux, flux_err=None,
                   periods=None, durations=None,
                   period_min=0.5, period_max=None,
                   n_periods=5000, n_durations=20,
                   duration_min_fraction=0.005,
                   duration_max_fraction=0.15,
                   n_phase=200):
    """
    Brute-force BLS following Kovács, Zucker & Mazeh (2002), equations 3-6.

    For each trial period P and fractional transit duration q:
      - Phase-fold the lightcurve
      - Slide a box of width q across the phase
      - Compute the SR statistic (signal residue)

    The SR statistic (eq 5 of KZM02) is:
        SR = max over (i1,i2) of  s(i1,i2)^2 / [r(i1,i2) * (1 - r(i1,i2))]

    where s and r are the weighted flux sum and weight sum in the transit box.

    Parameters
    ----------
    time : array-like
        Observation times (BJD or similar).
    flux : array-like
        Normalised flux (1.0 = out of transit).
    flux_err : array-like, optional
        Per-point uncertainties. Uniform weights if None.
    periods : array-like, optional
        Explicit trial periods. Overrides period_min/max/n_periods.
    durations : array-like, optional
        Explicit trial durations (in units of period fraction).
    period_min, period_max : float
        Range for automatic period grid (days).
    n_periods : int
        Number of trial periods.
    n_durations : int
        Number of trial durations.
    duration_min_fraction, duration_max_fraction : float
        Min/max fractional transit duration.
    n_phase : int
        Number of phase bins for the fast approach.

    Returns
    -------
    BLSResult
    """
    time = np.asarray(time, dtype=np.float64)
    flux = np.asarray(flux, dtype=np.float64)

    if flux_err is not None:
        flux_err = np.asarray(flux_err, dtype=np.float64)
        weights = 1.0 / flux_err**2
    else:
        weights = np.ones_like(flux)

    # Normalise weights so sum = 1 (KZM02 convention)
    weights = weights / np.sum(weights)

    # Weighted mean subtraction (work with residuals from weighted mean)
    wmean = np.sum(weights * flux)
    flux_res = flux - wmean

    # Period grid
    if periods is None:
        if period_max is None:
            period_max = (time[-1] - time[0]) / 2.0
        # Uniform in frequency for even sampling
        freq_min = 1.0 / period_max
        freq_max = 1.0 / period_min
        freqs = np.linspace(freq_min, freq_max, n_periods)
        periods = 1.0 / freqs
    else:
        periods = np.asarray(periods, dtype=np.float64)

    # Duration fractions
    if durations is None:
        durations = np.linspace(duration_min_fraction, duration_max_fraction, n_durations)
    else:
        durations = np.asarray(durations, dtype=np.float64)

    n_p = len(periods)
    power = np.zeros(n_p)
    best_duration_arr = np.zeros(n_p)
    best_t0_arr = np.zeros(n_p)
    best_depth_arr = np.zeros(n_p)

    for ip, period in enumerate(periods):
        best_sr = -np.inf
        best_dur = durations[0]
        best_phase0 = 0.0
        best_dep = 0.0

        # Phase-fold and bin (Hartman & Bakos fast approach)
        phases = _phase_fold(time, period, t0=time[0])

        # Bin the data
        bin_edges = np.linspace(0, 1, n_phase + 1)
        bin_s = np.zeros(n_phase)    # sum of w*flux_res in each bin
        bin_r = np.zeros(n_phase)    # sum of w in each bin

        bin_idx = np.clip(np.digitize(phases, bin_edges) - 1, 0, n_phase - 1)
        for ib in range(n_phase):
            mask = bin_idx == ib
            bin_s[ib] = np.sum(weights[mask] * flux_res[mask])
            bin_r[ib] = np.sum(weights[mask])

        # Extended bins for wrap-around
        bin_s_ext = np.concatenate([bin_s, bin_s])
        bin_r_ext = np.concatenate([bin_r, bin_r])

        for q in durations:
            # Number of bins in the transit box
            n_box = max(1, int(round(q * n_phase)))
            if n_box >= n_phase:
                continue

            # Sliding box using cumulative sums
            cum_s = np.cumsum(bin_s_ext)
            cum_r = np.cumsum(bin_r_ext)

            # s(i, i+n_box) and r(i, i+n_box) for each starting bin
            s_box = cum_s[n_box:n_box + n_phase] - np.concatenate([[0], cum_s[:n_phase - 1]])
            r_box = cum_r[n_box:n_box + n_phase] - np.concatenate([[0], cum_r[:n_phase - 1]])

            # Correct the first element
            s_box[0] = cum_s[n_box - 1]
            r_box[0] = cum_r[n_box - 1]

            # Actually recompute cleanly to avoid off-by-one
            s_box2 = np.zeros(n_phase)
            r_box2 = np.zeros(n_phase)
            for start in range(n_phase):
                idx_range = np.arange(start, start + n_box) % n_phase
                s_box2[start] = np.sum(bin_s[idx_range])
                r_box2[start] = np.sum(bin_r[idx_range])

            # SR statistic: s^2 / (r * (1 - r))  [KZM02 eq 5]
            valid = (r_box2 > 0) & (r_box2 < 1)
            if not np.any(valid):
                continue

            sr = np.full(n_phase, -np.inf)
            sr[valid] = s_box2[valid]**2 / (r_box2[valid] * (1.0 - r_box2[valid]))

            imax = np.argmax(sr)
            if sr[imax] > best_sr:
                best_sr = sr[imax]
                best_dur = q * period  # convert to days
                best_phase0 = imax / n_phase
                # Transit depth = s / r  (mean flux deficit in transit)
                if r_box2[imax] > 0:
                    best_dep = -s_box2[imax] / r_box2[imax]  # positive = dimming
                else:
                    best_dep = 0.0

        power[ip] = best_sr if best_sr > -np.inf else 0.0
        best_duration_arr[ip] = best_dur
        best_t0_arr[ip] = time[0] + best_phase0 * period
        best_depth_arr[ip] = best_dep

    # Signal Detection Efficiency (SDE)
    # SDE = (SR_peak - mean(SR)) / std(SR)   [KZM02 eq 6]
    mean_sr = np.mean(power)
    std_sr = np.std(power)
    if std_sr > 0:
        sde_spectrum = (power - mean_sr) / std_sr
    else:
        sde_spectrum = np.zeros_like(power)

    ibest = np.argmax(power)
    best_period = periods[ibest]
    best_duration = best_duration_arr[ibest]
    best_t0 = best_t0_arr[ibest]
    best_depth = best_depth_arr[ibest]
    sde = sde_spectrum[ibest]

    return BLSResult(
        periods=periods,
        power=power,
        best_period=best_period,
        best_duration=best_duration,
        best_t0=best_t0,
        best_depth=best_depth,
        sde=sde,
        sde_spectrum=sde_spectrum,
    )


def bls_fast(time, flux, flux_err=None,
             periods=None, period_min=0.5, period_max=None,
             n_periods=10000, n_bins=300,
             duration_min_fraction=0.005, duration_max_fraction=0.15,
             n_durations=30):
    """
    Fast BLS using the phase-binning approach of Hartman & Bakos (2016).

    Key optimisation: bin data once per period, then slide the box over bins
    using cumulative sums → O(n_bins * n_durations) per period instead of O(N).

    Parameters are similar to bls_bruteforce but with higher defaults for
    n_periods and n_bins.

    Returns
    -------
    BLSResult
    """
    # This is essentially the same algorithm as bls_bruteforce with the
    # binning optimisation already built in. The brute-force version above
    # already uses binning. The difference here is we use more bins and
    # vectorise the sliding-box computation more aggressively.

    time = np.asarray(time, dtype=np.float64)
    flux = np.asarray(flux, dtype=np.float64)

    if flux_err is not None:
        flux_err = np.asarray(flux_err, dtype=np.float64)
        weights = 1.0 / flux_err**2
    else:
        weights = np.ones_like(flux)

    weights = weights / np.sum(weights)
    wmean = np.sum(weights * flux)
    flux_res = flux - wmean

    if periods is None:
        if period_max is None:
            period_max = (time[-1] - time[0]) / 2.0
        freq_min = 1.0 / period_max
        freq_max = 1.0 / period_min
        freqs = np.linspace(freq_min, freq_max, n_periods)
        periods = 1.0 / freqs
    else:
        periods = np.asarray(periods, dtype=np.float64)

    durations = np.linspace(duration_min_fraction, duration_max_fraction, n_durations)

    n_p = len(periods)
    power = np.zeros(n_p)
    best_duration_arr = np.zeros(n_p)
    best_t0_arr = np.zeros(n_p)
    best_depth_arr = np.zeros(n_p)

    for ip, period in enumerate(periods):
        phases = _phase_fold(time, period, t0=time[0])

        # Bin
        bin_idx = np.clip((phases * n_bins).astype(int), 0, n_bins - 1)

        # Use np.bincount for speed
        bin_s = np.bincount(bin_idx, weights=weights * flux_res, minlength=n_bins)
        bin_r = np.bincount(bin_idx, weights=weights, minlength=n_bins)

        best_sr = -np.inf
        best_dur = durations[0]
        best_phase0 = 0.0
        best_dep = 0.0

        # Double the bins for wrap-around handling
        bin_s2 = np.concatenate([bin_s, bin_s])
        bin_r2 = np.concatenate([bin_r, bin_r])
        cum_s = np.concatenate([[0], np.cumsum(bin_s2)])
        cum_r = np.concatenate([[0], np.cumsum(bin_r2)])

        for q in durations:
            n_box = max(1, int(round(q * n_bins)))
            if n_box >= n_bins:
                continue

            # Vectorised sliding box
            starts = np.arange(n_bins)
            ends = starts + n_box
            s_box = cum_s[ends] - cum_s[starts]
            r_box = cum_r[ends] - cum_r[starts]

            valid = (r_box > 1e-15) & (r_box < 1.0 - 1e-15)
            sr = np.full(n_bins, -np.inf)
            sr[valid] = s_box[valid]**2 / (r_box[valid] * (1.0 - r_box[valid]))

            imax = np.argmax(sr)
            if sr[imax] > best_sr:
                best_sr = sr[imax]
                best_dur = q * period
                best_phase0 = imax / n_bins
                if r_box[imax] > 1e-15:
                    best_dep = -s_box[imax] / r_box[imax]
                else:
                    best_dep = 0.0

        power[ip] = best_sr if best_sr > -np.inf else 0.0
        best_duration_arr[ip] = best_dur
        best_t0_arr[ip] = time[0] + best_phase0 * period
        best_depth_arr[ip] = best_dep

    mean_sr = np.mean(power)
    std_sr = np.std(power)
    if std_sr > 0:
        sde_spectrum = (power - mean_sr) / std_sr
    else:
        sde_spectrum = np.zeros_like(power)

    ibest = np.argmax(power)

    return BLSResult(
        periods=periods,
        power=power,
        best_period=periods[ibest],
        best_duration=best_duration_arr[ibest],
        best_t0=best_t0_arr[ibest],
        best_depth=best_depth_arr[ibest],
        sde=sde_spectrum[ibest],
        sde_spectrum=sde_spectrum,
    )


def phase_fold_lightcurve(time, flux, period, t0):
    """Phase-fold a lightcurve for plotting."""
    phase = _phase_fold(time, period, t0)
    # Centre on transit (phase 0.5 → 0.0)
    phase = (phase - 0.5) % 1.0 - 0.5
    sort_idx = np.argsort(phase)
    return phase[sort_idx], flux[sort_idx]


if __name__ == "__main__":
    # Quick synthetic test
    np.random.seed(42)
    N = 5000
    time = np.sort(np.random.uniform(0, 90, N))  # 90 days of obs
    true_period = 3.5
    true_depth = 0.005
    true_duration = 0.1  # days
    true_t0 = 1.0

    flux = np.ones(N)
    phase = ((time - true_t0) / true_period) % 1.0
    in_transit = phase < (true_duration / true_period)
    flux[in_transit] -= true_depth
    flux += np.random.normal(0, 0.001, N)

    print("Running BLS on synthetic data...")
    print(f"  True period={true_period}, depth={true_depth}, duration={true_duration}")

    result = bls_fast(time, flux, period_min=1.0, period_max=10.0, n_periods=5000)
    print(f"  Recovered: period={result.best_period:.4f}, "
          f"depth={result.best_depth:.5f}, "
          f"duration={result.best_duration:.4f}, "
          f"SDE={result.sde:.1f}")
    print(f"  Period error: {abs(result.best_period - true_period):.4f} days "
          f"({abs(result.best_period - true_period)/true_period*100:.2f}%)")
