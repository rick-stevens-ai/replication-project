# Replication Project

Systematic replication of computational science papers using AI-assisted reproducibility methods.

## Overview

This project contains independent replications of published computational science papers across multiple domains. Each replication includes:

- **Code**: Independent implementation (not copied from original authors)
- **Data**: Generated results and comparisons
- **Figures**: Reproduced plots from the papers
- **Report**: Analysis of reproducibility, discrepancies, and lessons learned

## Completed Replications

| # | OSTI ID | Paper | Domain | Status |
|---|---------|-------|--------|--------|
| 1 | — | Fajar et al. (2026) PVMol-Gen | Materials/ML | ✅ Complete |
| 2 | — | Hempel et al. MSM | Molecular Dynamics | ✅ Complete |
| 3 | 1997354 | Hausdorff Integer Sequences | Mathematics | ✅ Complete |
| 4 | 2571540 | BayesOpt qHSRI | Optimization | ✅ Complete |
| 5 | 1983793 | CPW Resonator | Quantum Devices | ✅ Complete |
| 6 | 1475143 | FDTD Delay PDE | Numerical Methods | ✅ Complete |
| 7 | 1461824 | Photo-z PDFs | Astrophysics | ✅ Complete |
| 8 | 1379592 | GraphBLAS Foundations | Graph Algorithms | ✅ Complete |
| 9 | 2441075 | Trapped-Ion Qubits | Quantum Computing | ✅ Complete |
| 10 | 1842593 | Motion Tomography | Signal Processing | ✅ Complete |
| 11 | 2217719 | SCALE MSRE Depletion | Nuclear Engineering | ✅ Complete |
| 12 | 3014512 | Dark Matter SD Scattering | Particle Physics | ✅ Complete |
| 13 | 1609039 | Metallic Glass Formation | Materials Science | ⏳ Running (76%) |
| 14 | 1484740 | Electronic/Optical Properties of 2D GaN | DFT/Materials | ✅ Complete |
| 15 | 1559043 | Ignition Kernel in Turbulent Flow | CFD/Combustion | ✅ Complete (4/5 — PeleC v3, Polaris ensemble 4φ×5 realizations, ignition-propensity curve reproduced, paper Fig.3 analog) |
| 16 | 1275503 | Cosmic Reionization on Computers | Astrophysics | ✅ Complete |
| 17 | 1868518 | Graph-RL for Grid Restoration | ML/Power Systems | ✅ Complete |
| 18 | 3003857 | Chaotic Dynamics via Multi-Step Penalty Neural ODEs | ML/Math | ✅ Complete |
| 19 | 2587225 | ScaWL: Scaling k-WL in Distributed-Memory | Graph Algorithms / HPC | ✅ Complete |
| 20 | 1412756 | Chiral Spin Order in Kondo-Heisenberg Systems | Condensed Matter Theory | ✅ Complete (4/5) |
| 21 | 1523841 | Polarization differences ↔ Zone-averaged shift photocurrent | Condensed Matter / Optics | ✅ Complete (4/5) |
| 22 | 1864334 | NN-VMC for A≤4 Nuclei (ANN correlator ansatz) | Nuclear Physics / ML | ✅ Complete (3/5) |
| 23 | 1624105 | Clustering huge protein sequence sets in linear time (Linclust) | Bioinformatics / Algorithms | ✅ Complete (9/10) |
| 24 | 2571909 | Physics-based hybrid ML for Critical Heat Flux (CHF) prediction | Nuclear / Thermal Hydraulics / ML | ✅ Complete (7/10) |
| 25 | 1606674 | CMV Reduction in Single-Phase qZSI PV Inverter | Power Electronics / Circuits | ✅ Complete (4/5) |
| 26 | 2439897 | Physics and Chemistry from Parsimonious Representations (rVAE) | ML / Scientific Imaging | ✅ Complete (8/10) |
| 27 | 1981773 | Single-atom Pt doping of La$_2$Ti$_2$O$_7$ for photocatalysis (DFT) | DFT / Materials / Catalysis | ✅ Complete (6/10) |
| 28 | 2469515 | Supervised extraction of near-complete genomes from multiple metagenomes (PATRIC) | Bioinformatics / Metagenomics | ⚠️ Partial (4/10 — baseline MetaBAT2 pipeline reproduced on synthetic 5-species community, 5/5 HQ bins; PATRIC/SEEDtk supervised arm out of scope) |
| 29 | — | Gopal-Trefethen 2019: Lightning Laplace/Helmholtz solvers | Numerical PDE / Spectral | ✅ Complete (8/10) |
| 30 | — | Fortunato-Townsend 2017: Fast Poisson solver for Chebyshev spectral method via ADI | Numerical PDE / Spectral | ✅ Complete (9/10 — spectral convergence to 1.8e-14 by n=24, ADI vs direct crossover at n=1024, O(n² log² n) scaling confirmed up to n=2048) |

### PDE Replication Series

| # | Paper | Domain | Status |
|---|-------|--------|--------|
| P1 | Grossmann et al. 2023: Can PINNs Beat the Finite Element Method? | Numerical PDE / ML | ✅ Complete (7/10 — 1D Poisson full sweep, 2D Poisson + 1D Allen-Cahn partial PINN sweeps; FEM dominance confirmed across all problems; 3D Poisson & Schrödinger skipped due to missing eval data in repo) |

## OSTI Publication Analysis

Analysis of Argonne's full OSTI publication record (2016-2025, ~30,000 papers) shows:
- **~400 papers/year** are computationally replicable without experimental facilities
- **~3,500 papers** over the last 10 years form the replicable corpus
- 70% discovery science, 23% applied science/engineering, 6% facility/methods
- This project has replicated papers spanning 15 of Argonne's OSTI subject categories

## Methodology

Each replication follows a standard process:
1. Read and analyze the original paper
2. Implement the methods independently (from equations, not source code)
3. Reproduce key results (figures, tables, numerical values)
4. Document discrepancies and assess reproducibility
5. Write a structured report

Replications are performed using a mix of Python, Fortran, LAMMPS, OpenMC, and other domain-specific tools, running on GPU clusters (NVIDIA A100, Intel PVC) and workstations.

## Tools & Infrastructure

- **AI Assistant**: Ollie (OpenClaw + Claude Opus)
- **Compute**: Argonne ALCF (Polaris, Aurora), UIC GPU cluster (8× A100), DGX Spark
- **Languages**: Python, C++, Fortran
- **Domain codes**: OpenMC, LAMMPS, DarkELF, OpenMM, MDAnalysis

## Author

Rick Stevens, Argonne National Laboratory  
AI-assisted by Ollie (OpenClaw)

## License

Research use. Individual replications may reference GPL/MIT/BSD licensed tools.
