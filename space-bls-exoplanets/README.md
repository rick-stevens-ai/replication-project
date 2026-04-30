# BLS Exoplanet Transit Detection — Replication

Replication of the **Box Least Squares (BLS)** algorithm for detecting periodic planetary transits in stellar photometry.

## Papers

- **Kovács, Zucker & Mazeh (2002)** — *A&A 391, 369*: Original BLS algorithm (Signal Residue statistic, SDE)
- **Hartman & Bakos (2016)** — *Astron. Comput. 17, 1*: Fast O(N_bins) phase-binning optimisation

## Quick Start

```bash
# Set up environment
cd ~/Dropbox/REPLICATE-PROJECT/space-bls-exoplanets
source .venv/bin/activate

# Run the synthetic self-test
python replication/code/bls_kovacs2002.py

# Run the full replication on 6 Kepler targets
python replication/code/bls_test.py
```

## Results Summary

All 6 known transiting exoplanets detected, periods recovered to <0.02%:

| Target | Known P (d) | Recovered P (d) | Error | SDE |
|---|---|---|---|---|
| HAT-P-7 b | 2.2047 | 2.2045 | 0.012% | 25.5 |
| TrES-2 b | 2.4706 | 2.4704 | 0.008% | 49.8 |
| Kepler-5 b | 3.5485 | 3.5483 | 0.003% | 23.1 |
| Kepler-6 b | 3.2347 | 3.2345 | 0.008% | 32.0 |
| Kepler-8 b | 3.5225 | 3.5227 | 0.004% | 39.5 |
| Kepler-10 b | 0.8375 | 0.8375 | 0.004% | 24.9 |

## Project Structure

```
space-bls-exoplanets/
├── README.md              # This file
├── REPORT.md              # Detailed replication report
├── .venv/                 # Python 3.12 virtual environment
└── replication/
    ├── code/
    │   ├── bls_kovacs2002.py  # From-scratch BLS implementation
    │   └── bls_test.py        # Test driver (downloads data, runs BLS, plots)
    ├── figures/
    │   ├── HAT-P-7_b.png     # Per-target: lightcurve + BLS spectrum + phase-folded
    │   ├── TrES-2_b.png
    │   ├── Kepler-5_b.png
    │   ├── Kepler-6_b.png
    │   ├── Kepler-8_b.png
    │   ├── Kepler-10_b.png
    │   └── summary_comparison.png  # Period recovery + SDE summary
    └── results/
        └── bls_results.json   # Machine-readable per-target results
```

## Dependencies

- Python 3.12+
- numpy, scipy, matplotlib
- astropy (for comparison BLS implementation)
- lightkurve (for Kepler data download)

## Implementation Details

Our BLS implementation (`bls_kovacs2002.py`) provides:

- `bls_bruteforce()` — Direct implementation of KZM02 eq 3-6 with phase binning
- `bls_fast()` — Optimised version with `np.bincount` and vectorised cumulative-sum sliding windows (Hartman & Bakos approach)
- `phase_fold_lightcurve()` — Utility for phase-folding and plotting

The algorithm searches a 3D parameter space (period × duration × epoch) and returns the Signal Residue (SR) power spectrum plus Signal Detection Efficiency (SDE).

## Known Limitations

- Only 6 targets tested (no blind survey)
- No false-alarm rate characterisation
- Single Kepler quarter per target
- No multi-planet iterative search
- Box model underestimates true transit depths

See `REPORT.md` for full discussion.

---

*Replication performed 2026-04-30 for the REPLICATE project.*
