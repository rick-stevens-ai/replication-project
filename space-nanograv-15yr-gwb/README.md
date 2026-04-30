# NANOGrav 15-Year GWB Replication

Replication of **Agazie et al. (2023)** — *"The NANOGrav 15 yr Data Set: Evidence for a Gravitational-Wave Background"* — ApJL 951 L8 ([arXiv:2306.16213](https://arxiv.org/abs/2306.16213)).

## Quick Start

```bash
# Create conda environment
conda create -n ng15 -c conda-forge enterprise_extensions la_forge matplotlib numpy scipy pyarrow pytables corner -y
conda activate ng15

# Run the full analysis
cd replication/code
python run_analysis.py
```

## What This Paper Claims

NANOGrav analyzed timing residuals from 67 millisecond pulsars over 15 years and found **2–4σ evidence** for a gravitational-wave background (GWB) through the Hellings-Downs inter-pulsar angular correlation pattern. Key results:
- GWB amplitude A ≈ 2.4 × 10⁻¹⁵ (at fixed γ = 13/3)
- Spectral index γ ≈ 3.2 (varied-gamma analysis; slightly below the SMBHB prediction of 13/3)
- HD signal-to-noise ratio ≈ 3 (noise-marginalized multi-component optimal statistic)

## What We Replicated

| Quantity | Paper | Ours | Match? |
|----------|-------|------|--------|
| γ (varied) | ~3.2 | 3.35 | ✅ <0.5σ |
| log₁₀A (varied) | ~-14.19 | -14.17 | ✅ <0.2σ |
| HD SNR (MCOS) | 2–4 | 2.94 | ✅ |
| n_pulsars | 67 | 67 | ✅ |

## Project Structure

```
space-nanograv-15yr-gwb/
├── README.md                    # This file
├── REPORT.md                    # Detailed replication report
└── replication/
    ├── code/
    │   ├── run_analysis.py      # Master analysis script
    │   ├── analyze_posteriors.py # MCMC posterior extraction
    │   ├── compute_optimal_statistic.py  # HD optimal statistic
    │   ├── plot_hd_curve.py     # HD correlation figures
    │   └── plot_posteriors.py   # Corner plots and comparisons
    ├── data/
    │   └── 15yr_stochastic_analysis/  # NANOGrav data release (git clone)
    │       ├── tutorials/
    │       │   ├── data/
    │       │   │   ├── feathers/          # 67 pulsar feather files
    │       │   │   ├── 15yr_wn_dict.json  # White noise parameters
    │       │   │   ├── curn_14f_pl_vg_os.npz  # Precomputed OS data
    │       │   │   └── optstat_ml_gamma4p33.json  # ML parameters
    │       │   ├── presampled_cores/      # MCMC chains
    │       │   └── optimal_statistic_covariances.py
    │       └── data_release/
    ├── figures/
    │   ├── hd_theory_curve.png           # HD correlation function
    │   ├── mcos_snr_distributions.png    # MCOS SNR histograms
    │   ├── hd_curve_fit.png              # HD curve with recovered amplitude
    │   ├── amplitude_recovery.png        # A² recovery from OS
    │   ├── curn_corner.png               # CURN model corner plot
    │   ├── hd_corner.png                 # HD model corner plot
    │   ├── curn_vs_hd_posteriors.png     # Model comparison
    │   └── free_spectrum.png             # 30-bin free spectrum
    └── results/
        ├── final_results.json            # All numerical results
        ├── posterior_results.json         # MCMC posterior summaries
        └── optimal_statistic_results.json # OS analysis results
```

## Honest Gaps

- Used **presampled MCMC chains** from the NANOGrav data release (full runs take weeks)
- Used **precomputed optimal statistic** results (10,000 noise realizations)
- White noise parameters taken from the published noise dictionary, not independently fit
- Tutorial data may be slightly reduced from full publication data (per NANOGrav README)

See [REPORT.md](REPORT.md) for full details.

## Dependencies

- Python 3.11+
- enterprise 3.4.4
- enterprise_extensions 3.0.3
- la_forge 1.1.0
- numpy, matplotlib, scipy, pyarrow, pytables
