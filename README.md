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
| 2 | 1565592 | Hempel et al. MSM from short non-equilibrium simulations | Molecular Dynamics | ✅ Complete (9/8 — 1D well + 2D potential + ADP, OOM correction confirmed) |
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
| 13 | 1609039 | Cu₆₄Zr₃₆ Metallic Glass MD (deformation) | Materials Science | ✅ Complete (7/8 + 6/8 — 9 σ-ε runs (3T × 3ε̇); paper ordering reproduced (3.1× drop 10K→600K, rate hardening at 300K/600K); magnitudes 0.51–0.97× paper due to 24× atom-count reduction) |
| 14 | 1484740 | Electronic/Optical Properties of 2D GaN | DFT/Materials | ✅ Complete (9/9 — monolayer + bilayer fully converged on uicgpu QE 7.4.1 GPU; bilayer F_max=0.000598 Ry/Bohr; plasmons ωp ≈ 10 eV match paper Fig 5; PBE-vs-LDA gap discrepancy documented; GW/BSE out of scope) |
| 15 | 1559043 | Ignition Kernel in Turbulent Flow | CFD/Combustion | ✅ Complete (4/5 — PeleC v3, Polaris ensemble 4φ×5 realizations, ignition-propensity curve reproduced, paper Fig.3 analog) |
| 16 | 1275503 | Cosmic Reionization on Computers | Astrophysics | ✅ Complete |
| 17 | 1868518 | Graph-RL for Grid Restoration | ML/Power Systems | ✅ Complete (8/7 — IEEE-33/123 + headline IEEE 8500-Node replicated: 578-cell partition, GCN-DQN 99.67% restored at 2.39s vs paper 100%/2.02s; MLP-DQN collapses to 55% confirming graph structure necessity) |
| 18 | 3003857 | Chaotic Dynamics via Multi-Step Penalty Neural ODEs | ML/Math | ✅ Complete |
| 19 | 2587225 | ScaWL: Scaling k-WL Weisfeiler-Lehman in Distributed Memory | Graph Algorithms / HPC | ✅ Complete (9/10 — independent C++17/MPI/OpenMP 3-WL on chiatta00; 26.4× strong scaling at 128 cores; memory myth busted (8MB actual vs claimed 100GB); multi-node IB at ~10³ ranks parked for Polaris/Aurora) |
| 20 | 1412756 | Chiral Spin Order in Kondo-Heisenberg Systems | Condensed Matter Theory | ✅ Complete (4/5) |
| 21 | 1523841 | Polarization differences ↔ Zone-averaged shift photocurrent | Condensed Matter / Optics | ✅ Complete (4/5) |
| 22 | 1864334 | NN-VMC for A≤4 Nuclei + 3-body forces tier-lift | Nuclear Physics / ML | ✅ Complete (8/9 — V_NN + UIX-inspired V_3N on ³H/³He/⁴He; ³He–³H Coulomb splitting +0.75 vs +0.764 MeV; V_LS = 0 by symmetry on real-valued S-wave ansatz, spinor extension parked) |
| 23 | 1624105 | Clustering huge protein sequence sets in linear time (Linclust) | Bioinformatics / Algorithms | ✅ Complete (9/10) |
| 24 | 2571909 | Physics-based hybrid ML for Critical Heat Flux (CHF) prediction | Nuclear / Thermal Hydraulics / ML | ✅ Complete (7/10) |
| 25 | 1606674 | CMV Reduction in Single-Phase qZSI PV Inverter | Power Electronics / Circuits | ✅ Complete (4/5) |
| 26 | 2439897 | Physics and Chemistry from Parsimonious Representations (rVAE) | ML / Scientific Imaging | ✅ Complete (8/10) |
| 27 | 1981773 | Single-atom Pt doping of La$_2$Ti$_2$O$_7$ for photocatalysis (DFT) | DFT / Materials / Catalysis | ✅ Complete (9/9 — Yambo PBE/RPA optical absorption: 2.40 eV redshift vs paper 2.20 eV (9% diff), 2.91× visible-band enhancement, Pt sub-gap tail at 0.52 eV; facet σ ordering (001)<(010) recovered (13-16% diff vs paper); polar-terminated (100)/(101)/(110) slabs diverged, need symmetric slab gen) |
| 28 | 2469515 | Supervised extraction of near-complete genomes from multiple metagenomes (PATRIC) | Bioinformatics / Metagenomics | ⚠️ Partial (4/10 — baseline MetaBAT2 pipeline reproduced on synthetic 5-species community, 5/5 HQ bins; PATRIC/SEEDtk supervised arm out of scope) |
| 29 | — | Gopal-Trefethen 2019: Lightning Laplace/Helmholtz solvers | Numerical PDE / Spectral | ✅ Complete (8/10) |
| 30 | — | Fortunato-Townsend 2017: Fast Poisson solver for Chebyshev spectral method via ADI | Numerical PDE / Spectral | ✅ Complete (9/10 — spectral convergence to 1.8e-14 by n=24, ADI vs direct crossover at n=1024, O(n² log² n) scaling confirmed up to n=2048) |
| 31 | 1427646 | Deep Learning of Atomically Resolved STEM Images: Chemical ID & Local Transformations | ML / Imaging | ✅ Complete (8/8 — multislice training set, ResNet trained, confusion matrix + peak-detection figs) |
| 32 | 2582579 | Constraining Cosmological Parameters with Needlet Internal Linear Combination Maps | CMB / Cosmology | ✅ Complete (8/8 — pyilc + 6 contributions to Eq.26, <0.2% recovery of reference power spectra at 2≤ℓ≤20) |
| 33 | 2587579 | Mesh-based Super-Resolution of Fluid Flows with Multiscale GNN | PDE / ML | ✅ Complete (8/8 — 4.77× rel-L2 reduction over interp; distributed halo-swap validated bitwise vs single-rank across 3 configs (rel L2 ≤5.4e-9); 3D BFS hex SE mesh runs, 1.11× over trilinear at ep 30) |
| 34 | 2587945 | Spatiotemporal Forecasting of ELMs in Tokamak Plasmas (NN forecaster) | Fusion / ML | ✅ Complete (8/8 — FNO-2D + ConvLSTM-attention + Chronos-T5 + Temporal-VAE on synthetic BES; paper's RNN > FNO ranking triangulated across 5 models; real DIII-D BES not public) |
| 35 | 1861801 | NukeLM: Pre-Trained & Fine-Tuned LMs for Nuclear & Energy Domains | NLP / Domain LMs | ✅ Complete (8/10 — DAPT on RoBERTa-large with 325K OSTI abstracts (114M tokens); MLM loss 0.641 (ppl 1.90) surpasses paper's 0.95; NukeLM Binary F₁=0.710 tops ranking; all paper trends reproduce) |
| 36 | 2475938 | Updated Virophage Taxonomy and Distinction from Polinton-like Viruses | Bioinformatics | ✅ Complete (8/10 — 279-genome NCBI scale-up (21× the 13-genome baseline); 70-taxon 4-marker partitioned ML tree recovers Mavirus/Sputnik/Aquatic-Lavidaviridae clades + Maveriviricetes/Polintoviricetes boundary; IMG/VR uncultivated tail skipped) |
| 37 | 2396968 | Latent Stochastic Differential Equations for Quasar Variability & BH Properties | ML / Astrophysics | ⏳ Data + compute-bound (9/6 — v1_simplified + v2_faithful trained; WeatherBench2 zarr unreachable, 100× retrain budget out of scope) |
| 38 | 1578031 | Joint Emulation of Earth System Model Temperature-Precipitation (fldgen v2.0) | Climate / Stats | ✅ Complete (8/8 — Python re-impl all 8 algorithm steps (pattern scaling, EOF/PCA, Fourier phase randomization, quantile mapping); spatial-rank-corr RMSE 0.056, marginal KS 100% pass, cross-var corr r=0.93; synthetic ESM input not actual CMIP5) |

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
