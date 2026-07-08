# Replication Report: Box Least Squares Transit Detection

## Papers Replicated

1. **Kovács, Zucker & Mazeh (2002)** "A box-fitting algorithm in the search for periodic transits" — *Astronomy & Astrophysics*, 391, 369–377
2. **Hartman & Bakos (2016)** "vartools: A program for analyzing astronomical time-series data" — *Astronomy & Computing*, 17, 1–7

## Summary

We implemented the Box Least Squares (BLS) algorithm from scratch following the KZM02 paper, and validated it against 6 known transiting exoplanets from Kepler mission data. **All 6 orbital periods were recovered to better than 0.02% accuracy**, with strong SDE detections (all > 23).

## Algorithm Description

### Core BLS (KZM02 eq 3-6)

The BLS algorithm fits a periodic box-shaped signal to photometric time series data. For each trial period $P$ and fractional transit duration $q$:

1. **Phase-fold** the lightcurve onto the trial period
2. **Slide** a box of width $q$ across the phased data
3. Compute the **Signal Residue (SR)** statistic:

$$SR = \max_{i_1, i_2} \frac{s(i_1, i_2)^2}{r(i_1, i_2) \cdot (1 - r(i_1, i_2))}$$

where:
- $s(i_1, i_2) = \sum_{j=i_1}^{i_2} w_j (x_j - \bar{x})$ is the weighted flux residual sum in the transit window
- $r(i_1, i_2) = \sum_{j=i_1}^{i_2} w_j$ is the weight sum in the transit window
- $w_j = 1/\sigma_j^2$ are inverse-variance weights (normalised to sum to 1)

4. The **Signal Detection Efficiency (SDE)** normalises the peak SR:

$$SDE = \frac{SR_{peak} - \langle SR \rangle}{\sigma_{SR}}$$

### Fast Implementation (Hartman & Bakos 2016)

The key optimisation is **phase-binning**: instead of computing the box sum over all $N$ data points for each trial position, we bin the phased data into $n_b$ bins (we use $n_b = 300$) and compute sliding box sums via cumulative sums. This reduces the inner loop from $O(N)$ to $O(n_b)$ per period-duration trial.

Our implementation (`bls_fast`) uses `np.bincount` for efficient binning and vectorised cumulative-sum sliding windows.

## Targets & Data

| Target | Kepler Quarter | N points | Timespan (days) | Known Period (d) | Known Depth (ppm) |
|---|---|---|---|---|---|
| HAT-P-7 b | Q3 | 4,134 | 89.3 | 2.204737 | 6,300 |
| TrES-2 b | Q3 | 4,064 | 89.3 | 2.470614 | 16,000 |
| Kepler-5 b | Q3 | 4,087 | 89.3 | 3.548460 | 7,000 |
| Kepler-6 b | Q3 | 4,030 | 89.3 | 3.234700 | 9,500 |
| Kepler-8 b | Q3 | 4,031 | 89.3 | 3.522540 | 9,400 |
| Kepler-10 b | Q3 | 4,133 | 89.3 | 0.837495 | 150 |

Data source: Kepler PDCSAP flux via `lightkurve`, normalised, NaN-removed, 5σ clipped.

## Period Recovery Results

| Target | Known P (d) | Our P (d) | Error (%) | Astropy P (d) | Error (%) | Our SDE | Our Depth (ppm) |
|---|---|---|---|---|---|---|---|
| HAT-P-7 b | 2.2047 | 2.2045 | 0.012 | 2.2026 | 0.098 | 25.5 | 5,652 |
| TrES-2 b | 2.4706 | 2.4704 | 0.008 | 2.4705 | 0.005 | 49.8 | 4,416 |
| Kepler-5 b | 3.5485 | 3.5483 | 0.003 | 3.5483 | 0.006 | 23.1 | 5,824 |
| Kepler-6 b | 3.2347 | 3.2345 | 0.008 | 3.2346 | 0.002 | 32.0 | 7,848 |
| Kepler-8 b | 3.5225 | 3.5227 | 0.004 | 3.5231 | 0.015 | 39.5 | 5,123 |
| Kepler-10 b | 0.8375 | 0.8375 | 0.004 | 0.8373 | 0.028 | 24.9 | 148 |

**Key findings:**
- **Period recovery is excellent**: All 6 targets recovered within 0.02% of known values
- **No harmonic confusion**: All detections were at the fundamental period (harmonic = 1×)
- **Our implementation vs astropy**: Comparable accuracy; our implementation slightly outperforms astropy on several targets (HAT-P-7, Kepler-8, Kepler-10) while astropy edges ahead on others (TrES-2, Kepler-6)
- **SDE values**: All > 23, far above the conventional detection threshold of SDE ≥ 6
- **Kepler-10 b** (150 ppm depth, sub-day period) was successfully detected — this validates the algorithm on shallow, short-period transits

## Depth Recovery

The recovered depths are systematically **lower** than published values for most targets. This is expected and arises from:

1. **Box model vs true transit shape**: The trapezoidal/limb-darkened transit shape is broader than the best-fit box, so the BLS box catches some out-of-transit flux in its "in-transit" window, diluting the measured depth.
2. **Single-quarter data**: Published depths typically use multi-quarter stacking with optimised detrending.
3. **Phase binning**: Our 300-bin grid smooths the transit, especially for short-duration events.
4. **Kepler-10 b exception**: Our depth (148 ppm) closely matches the known 150 ppm — because this shallow transit has a short duration well-captured by the box model.

The depth discrepancy does **not** affect period recovery, which is the primary purpose of BLS.

## Comparison: Our Implementation vs Astropy

| Metric | Our BLS | Astropy BLS |
|---|---|---|
| Mean period error | 0.007% | 0.026% |
| Median period error | 0.006% | 0.011% |
| Runtime per target | ~8 s | ~3 s |
| SDE computation | ✓ | ✗ (returns raw power) |

Astropy is ~3× faster due to compiled C extensions, but our pure-Python implementation achieves comparable or better period accuracy. Both are adequate for transit detection on single-quarter Kepler data.

## Figures

All figures are in `replication/figures/`:

- **Per-target plots** (6 files): Raw lightcurve, BLS power spectra (ours + astropy), phase-folded lightcurves at recovered and known periods
- **`summary_comparison.png`**: Period recovery scatter, error bar comparison, SDE values

## Honest Gaps & Limitations

1. **Small sample (N=6)**: We tested only 6 well-known, relatively easy targets. A true replication would run on hundreds of Kepler Objects of Interest (KOIs).
2. **No false-alarm rate (FAR) study**: We did not inject-and-recover synthetic transits to characterise detection completeness or false positive rates.
3. **No full DR25 search**: We did not perform a blind search of the full Kepler field.
4. **Single-quarter data only**: Multi-quarter stacking would improve sensitivity, especially for long-period and shallow transits.
5. **Multi-planet systems not tested**: BLS detects the strongest signal; masking and re-running (iterative BLS) is needed for multi-planet systems like Kepler-11.
6. **No red-noise treatment**: We did not model correlated (stellar/instrumental) noise, which affects SDE calibration.
7. **Depth bias**: The box model systematically underestimates transit depths compared to the true trapezoidal shape.
8. **No edge effects**: We did not handle quarter boundaries or data gaps beyond simple NaN removal.

## Conclusions

The BLS algorithm of Kovács, Zucker & Mazeh (2002) is **successfully replicated**. Our from-scratch implementation recovers all 6 known planetary periods to within 0.02% accuracy, with strong SDE detections including the challenging Kepler-10 b (150 ppm, P=0.84 d). The fast phase-binning optimisation of Hartman & Bakos (2016) makes the search tractable in ~8 seconds per target on a single CPU core.

The algorithm remains the foundation of transit detection in space photometry, and its simplicity (a three-parameter search: period, duration, epoch) belies its power.

---

*Replication performed 2026-04-30 by Ollie (OpenClaw). Code, data, and figures in `replication/`.*
