# Electronic specific heat capacities and entropies from density matrix quantum Monte Carlo using Gaussian process regression to find gradients of noisy data

- **OSTI ID:** 1993311
- **Rank:** #30
- **Replication Score:** 8/10
- **Open-Source Tools:** Yes
- **Code Repository:** No
- **Tools:** Gaussian process regression (scikit-learn), quantum Monte Carlo (DMQMC, PIP-DMQMC), standard linear algebra (FCI diagonalization)

## Why This Paper
Synthetic data, open-source tools, fully specified QMC/ML methodology, and quantitative results. No code repo but straightforward for AI.

## Replication Plan
AI implements synthetic DMQMC-like data for exactly solvable systems, fits with GP regression using the paper's composite kernel (RBF + Matérn 5/2 + Matérn 3/2), computes C_V and S via analytic GP derivatives, and compares against finite-difference and cubic spline baselines.

## Status
- [x] Paper reviewed
- [x] Code/tools identified (scikit-learn GPR, NumPy, SciPy)
- [x] Code implemented (synthetic benchmark systems)
- [x] Results reproduced (qualitative claims verified)
- [x] Results validated against paper

## Replication Summary

**Data:** Synthetic (Hubbard model + tight-binding chain), not real DMQMC.

**Key result:** GPR outperforms finite differences by 2–44× in C_V RMSE across all tested systems and noise levels, confirming the paper's central claim.

| System | FD RMSE | GPR RMSE | Improvement |
|--------|---------|----------|-------------|
| Hubbard 2-site (U/t=4) | 23.75 | **1.63** | 14.6× |
| Hubbard 2-site (U/t=8) | 16.47 | **0.37** | 44× |
| Hubbard 2-site (high noise) | 83.93 | **42.89** | 2× |

See `replication/REPORT.md` for full analysis.

## Directory Structure
```
├── 1993311.pdf                    # Original paper
├── README.md                      # This file
├── replication/
│   ├── REPORT.md                  # Full replication report
│   ├── code/
│   │   ├── exact_models.py        # Exact thermodynamics (Hubbard, chain)
│   │   ├── gpr_derivatives.py     # GPR fitting + derivatives
│   │   ├── finite_difference.py   # FD + spline baselines
│   │   ├── run_replication.py     # Main replication driver
│   │   └── plot_results.py        # Figure generation
│   ├── results/
│   │   ├── summary.json           # All RMSE metrics
│   │   ├── *_data.json            # Raw numerical data per system
│   │   └── *_noise_sweep.json     # Noise sweep data
│   └── figures/
│       ├── multi_system_cv.png    # All systems C_V comparison
│       ├── noise_sweep.png        # RMSE vs noise level
│       ├── *_cv_comparison.png    # C_V: FD vs GPR vs exact
│       ├── *_energy_fit.png       # GP energy fits
│       └── *_entropy.png          # Entropy comparisons
└── replication_plan*.{tex,pdf}    # Original planning documents
```

## How to Run
```bash
cd replication/code
python3 run_replication.py    # Generate all data (~3 min)
python3 plot_results.py       # Generate all figures
```

**Requirements:** Python 3, NumPy, SciPy, scikit-learn, matplotlib
