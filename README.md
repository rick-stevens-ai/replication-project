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
| 13 | 1609039 | Metallic Glass Formation | Materials Science | ⏳ Running |

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
