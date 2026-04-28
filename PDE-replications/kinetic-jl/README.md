# Kinetic.jl Replication

**Paper:** Xiao, T. (2021). "Kinetic.jl: A portable finite volume toolbox for scientific and neural computing." *Journal of Open Source Software*, 6(62), 3060.  
**DOI:** [10.21105/joss.03060](https://doi.org/10.21105/joss.03060)

## Overview

Replication of three core examples from Kinetic.jl — a Julia-based finite volume framework for kinetic equations (Boltzmann, BGK, Vlasov, MHD) with machine learning integration.

## Replicated Examples

| # | Example | Method | Status | Runtime |
|---|---------|--------|--------|---------|
| 1 | Sod shock tube | 1D BGK kinetic (KFVS) | ✅ Pass | ~14s |
| 2 | Homogeneous relaxation | BGK / Shakhov / ES-BGK | ✅ Pass | ~5s |
| 3 | Brio-Wu MHD shock | Two-species plasma kinetic | ✅ Pass | ~134s |

## Key Results

- **Sod shock tube:** Correct wave structure (rarefaction, contact, shock) matching exact Riemann solution. Smooth-region L² error < 10⁻³.
- **Homogeneous relaxation:** All three collision operators converge correctly — BGK to Maxwellian (7 orders), ES-BGK (3 orders), Shakhov to its own equilibrium M+S.
- **Brio-Wu MHD:** Full MHD wave structure (5 waves) captured via two-species kinetic formulation. Boundary states preserved to machine precision.

## Self-Score: 8.5/10

Successful replication across gas dynamics, collision operators, and plasma MHD. Deductions: no direct quantitative MHD reference solver comparison; neural closure example not attempted.

## How to Run

```bash
# Requires Julia 1.10+
cd kinetic-jl
julia --project=. -e 'using Pkg; Pkg.instantiate()'

# Run individual examples
julia --project=. replication/01_sod_shock_tube.jl
julia --project=. replication/02_homogeneous_relaxation.jl
julia --project=. replication/03_briowu_plasma.jl
```

## Structure

```
kinetic-jl/
├── README.md
├── Project.toml          # Julia project dependencies
├── replication/
│   ├── 01_sod_shock_tube.jl
│   ├── 02_homogeneous_relaxation.jl
│   ├── 03_briowu_plasma.jl
│   └── data/             # CSV output data
└── report/
    ├── report.md
    ├── report.pdf
    └── figures/           # 15 PNG plots
```

## Environment

- Julia 1.12.6
- Kinetic.jl 0.7.10 / KitBase 0.9.31 / KitML 0.4.11
- macOS x86_64 (CherryRd)
- Replicated: 2026-04-24
