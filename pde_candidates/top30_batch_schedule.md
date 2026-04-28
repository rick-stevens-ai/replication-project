# PDE Top-30 Replication Batch Schedule

**Generated:** 2026-04-24
**Source:** `top30_deep_read.jsonl` (Stage 5 LLM deep-read)

## Tier Summary

- **Priority A (start today, 11 papers):** low friction, code exists, clear benchmarks
- **Priority B (plan for next 1–2 weeks, 10 papers):** some friction — older, heavier deps, or partial code
- **Priority C (aspirational / deferred, 9 papers):** no public code or theory-only; need reimplementation

---

## Batch 1 — "Start Today" (A tier, parallel-safe)

These 11 can be spawned as **parallel sub-agents** now. Grouped by dependency stack for efficient environment reuse.

### Batch 1a: PyTorch-only (parallel, 1 GPU each)
| # | Title | Repo | Est. hrs |
|---|---|---|---|
| 1 | FEM vs PINNs (Grossmann+ 2023) | github.com/TamaraGrossmann/FEM-vs-PINNs | 4 |
| 2 | ML-accelerated CFD (Kochkov+ 2021) | github.com/google/jax-cfd | 6 |
| 3 | Latent Spectral Models (Wu+ 2023) | github.com/thuml/Latent-Spectral-Models | 6 |
| 4 | Koopman Neural Operator (Xiong+ 2023) | github.com/Koopman-Laboratory/KoopmanLab | 6 |
| 5 | Laplace Neural Operator (Cao+ 2023) | github.com/qianyingcao/Laplace-Neural-Operator | 4 |

### Batch 1b: C++/Julia/MATLAB (parallel, CPU-heavy)
| # | Title | Repo | Est. hrs |
|---|---|---|---|
| 6 | Walk on Stars (Sawhney+ 2023) | github.com/GeometryCollective/wost-simple | 5 |
| 7 | Fast Poisson (Fortunato+Townsend 2017) | github.com/danfortunato/fast-poisson-solvers | 4 |
| 8 | New Laplace/Helmholtz (Gopal+Trefethen 2019) | trefethen/lightning.m | 3 |
| 9 | Kinetic.jl (Xiao 2021) | github.com/vavrines/Kinetic.jl | 4 |
| 10 | APBS electrostatics (Jurrus+ 2017) | github.com/Electrostatics/apbs | 6 |

### Batch 1c: Framework-level (standalone, can run alongside 1a/1b)
| # | Title | Repo | Est. hrs |
|---|---|---|---|
| 11 | Dedalus spectral framework (Burns+ 2019) | github.com/DedalusProject/dedalus | 4 |

**Total wallclock for Batch 1 in parallel (4-way):** ~8 hours
**Total compute:** ~52 CPU/GPU-hours

---

## Batch 2 — "Next 1–2 weeks" (B tier)

Spawn after Batch 1 mostly completes. These need more setup or partial reimplementation.

| # | Title | Issue | Est. hrs |
|---|---|---|---|
| 12 | lifex-cfd (Africa+ 2023) | deal.II build heavy | 10 |
| 13 | PINN RANS (Eivazi+ 2021) | no public code; DeepXDE reimpl | 8 |
| 14 | Elman+Silvester preconditioner (1996) | use IFISS | 5 |
| 15 | Poisson Flow Generative (Xu+ 2022) | off-PDE-topic but code good | 10 |
| 16 | Kernel Active Subspaces (Romor+ 2020) | ATHENA + HopeFOAM | 6 |
| 17 | FLUPS (Caprace+ 2020) | MPI/HPC scaling | 8 |
| 18 | Optimized Schwarz Helmholtz (Gander 2002) | reimpl in FreeFem++ | 5 |
| 19 | AMR vs MR (Deiterding+ 2015) | Carmen + AMROC build | 8 |
| 20 | Godunov loss (Cassia+Kerswell 2024) | reimpl in PyTorch | 8 |
| 21 | IMEX-SAV NS (Huang+Shen 2021) | reimpl | 8 |

---

## Batch 3 — "Aspirational" (C tier)

Defer unless we get budget for full reimplementations or authors release code.

| # | Title | Blocker |
|---|---|---|
| 22 | PINN DD preconditioner (Kopaničáková+ 2023) | code "upon acceptance" only |
| 23 | Stochastic DO/BO PINN (Zhang+Karniadakis 2019) | no code |
| 24 | Deep RL AMR (Foucart+ 2022) | github repo dead 404 |
| 25 | Plane-wave DG Helmholtz (Hiptmair+ 2011) | theory-only |
| 26 | Stochastic Burgers Galerkin (Blömker+Jentzen 2013) | theory-only |
| 27 | DG-Hermite Vlasov-Poisson (Bessemoulin+Filbet 2022) | theory-only |
| 28 | Rate-optimal AFEM (Gantner+ 2020) | theory + no code |
| 29 | Fractional Allen-Cahn (Hou+Xu 2021) | no code |
| 30 | Modified PNP (Ma+ 2020) | no code |

---

## Recommended Spawning Order (if replicating 15)

Pick the 15 with best expected-value per unit time:

### Wave 1 (parallel, run simultaneously): 5 papers, ~6-8h wallclock
1. FEM vs PINNs (#1) — A, 4h
2. Walk on Stars (#6) — A, 5h
3. Fast Poisson Spectral (#7) — A, 4h
4. Lightning Laplace/Helmholtz (#8) — A, 3h
5. Kinetic.jl (#9) — A, 4h

### Wave 2 (parallel): 5 papers, ~6-10h wallclock
6. ML-accelerated CFD / jax-cfd (#2) — A, 6h
7. Latent Spectral Models (#3) — A, 6h
8. Koopman Neural Operator (#4) — A, 6h
9. Laplace Neural Operator (#5) — A, 4h
10. Dedalus framework (#11) — A, 4h

### Wave 3 (parallel): 5 papers, ~6-10h wallclock
11. APBS electrostatics (#10) — A, 6h
12. lifex-cfd (#12) — B, 10h
13. Elman+Silvester + IFISS (#14) — B, 5h
14. Optimized Schwarz Helmholtz (#18) — B, 5h
15. FLUPS Poisson library (#17) — B, 8h

**Total wallclock (3 waves, 5-way parallel):** ~24–30 hours
**Total compute:** ~85–100 core-hours + ~30 GPU-hours

---

## Cross-check vs existing replications

None of the 30 overlap with the existing REPLICATE-PROJECT subdirectories. All are genuinely new candidates.

## Domain / method distribution (top-30)

- **ML-operator / PINN:** 10 papers (#1,2,3,4,5,6,11,13,17,24 — by original rank)
- **Classical spectral / FD / FV:** 8 papers
- **Preconditioning / DD / multigrid:** 4 papers
- **Stochastic / kinetic / fractional PDEs:** 5 papers
- **Monte Carlo / grid-free:** 2 papers (Walk on Stars, and MC refs in FLUPS)
- **AMR / adaptivity:** 3 papers

Roughly 40% ML-forward, 60% classical — a healthy mix.
