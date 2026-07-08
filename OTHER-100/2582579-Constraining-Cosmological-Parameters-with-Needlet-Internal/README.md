# Constraining Cosmological Parameters with Needlet Internal Linear Combination Maps I: Analytic Power Spectrum Formalism

- **OSTI ID:** 2582579
- **Authors:** K. Surrao & J. C. Hill (2024), arXiv:2302.05436
- **Rank:** #14
- **Replication Score (stated):** 9/10
- **Open-Source Tools:** Yes — `NILC-PS-Model`, `pyilc`, WebSky mocks

## What Paper I actually does
Paper I is **not** a cosmological parameter-inference paper. It derives and
validates a single analytic formula (their Eq. 26) that predicts the
auto- and cross-power spectra of NILC component-separated maps, including
bispectrum and trispectrum corrections from the spatial locality of the
ILC weights. Validation is against a deliberately minimal MC simulation:
- Nside = 32, ellmax = 20
- 2 channels: 90 and 150 GHz
- CMB + amplified tSZ (×1000) + white noise (3×10⁴ μK·arcmin, 1.4′ beam)
- 3 Gaussian-difference needlet scales (FWHM 1000, 800 arcmin)

Cosmological parameter constraints (MCMC, Fisher, posteriors) are
**explicitly deferred to Paper II** (Surrao & Hill, "to appear" at the
time this replication was executed).

## Replication result (this run)

**Analytic NILC power spectrum (Eq. 26) vs simulation: ≤ 0.2 %
agreement** across all four component→NILC-map propagations and all
multipoles 2 ≤ ℓ ≤ 20. Reproduces Fig. 3 of the paper.

Full 8-page LaTeX writeup: `replication/report/report.pdf`.

## Layout

- `replication/` — main pipeline matching Paper I exactly
  - `NILC-PS-Model/` — cloned from the authors' repo (2-line compat patch documented in report §2.3)
  - `pyilc/` — cloned from jcolinhill/pyilc
  - `inputs/` — WebSky `lensed_alm.fits` (2 GB) and `tsz_2048.fits` (400 MB)
  - `nilc_ps_config.yaml` — matches paper's specification exactly
  - `prep_websky.py` — convert WebSky alms to Kelvin map and degrade tSZ
  - `make_paper_plots.py` — generate Figures 1–3 analogs
  - `outputs/` — pyilc weight maps, n-point-function pickles, `data_vecs/`
  - `report/report.pdf` — writeup with numerical validation table
- `replication/extended/` — bonus from-scratch pipeline (7-channel
  Planck-like sky with dust/sync foregrounds, 3-parameter emcee MCMC on
  CAMB spectrum). Not part of Paper I validation.

## Runtime
- Full pipeline wall time: **~2 h 10 min** on CherryRd (iMac, num_parallel=2).
- Dominant cost: pixel-space trispectrum estimator (~1 h 50 min).
- Compute: Python 3.11 (conda), numba-JIT inner loops in pyilc.

## Status
- [x] Paper reviewed (PDF read carefully; scope clarified vs replication plan)
- [x] Code/tools identified (kmsurrao/NILC-PS-Model + jcolinhill/pyilc + WebSky)
- [x] Code implemented/cloned + made runnable (2-line patch to pyilc_interface.py)
- [x] Results reproduced (Eq. 26 analytic vs direct NILC Cl, 4 panels)
- [x] Results validated against paper (match at <0.2% level, consistent with paper's sub-percent claim)
