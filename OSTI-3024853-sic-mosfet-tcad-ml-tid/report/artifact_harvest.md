# Artifact Harvest — OSTI 3024853 (Gao et al. 2026, ACM TODAES 31:4:76)

Pulled 2026-07-05.

## Paper / preprint

| Artifact | URL | Size | Notes |
|---|---|---|---|
| Full PDF (v2, ACM published) | https://www.osti.gov/servlets/purl/3024853 | 3,064,916 B | Retrieved via `uicgpu` (needs proxied internet). 36 pages, ACM v1.4. Report number SAND2026-19093J. |
| ACM DL landing | https://dl.acm.org/doi/10.1145/3766551 | HTML | CC-BY 4.0 open access. |
| Sandia companion conf. paper (SAND2024-01114A) | https://www.sandia.gov/app/uploads/sites/203/2024/03/sand2024-01114A.pdf | 2,038,704 B | Same authors, IEEE NSREC-style short paper on the same coupling approach. Confirms constants (rho_ox, t_ox, E_form). |

## Public tools referenced by the paper

| Artifact | URL | Size / status | Notes |
|---|---|---|---|
| Charon (TCAD) source | https://github.com/tcadsoftware/charon | GitHub, C++, 164 MB, 14 stars, last push 2022-07-29 | Public. Sandia's open-source drift-diffusion TCAD code the paper uses for ALL simulations. Depends on Trilinos. |
| Charon project page | https://charon.sandia.gov/ | HTTP 200 | Documentation & user manual (PDF). |
| Dakota (UQ/optimization) | https://dakota.sandia.gov/ | HTTP 200 | Sandia's UQ/optimization framework. Public. |
| Trilinos | https://github.com/trilinos/Trilinos | Public, C++, 1.4k stars | Nonlinear/linear solvers Charon builds on. |
| Cubit (meshing) | https://cubit.sandia.gov/ | Gated (Sandia-licensed) | Not fully open — used for device geometry meshing. |
| R `randomForest` | https://CRAN.R-project.org/package=randomForest | CRAN | Random-forest surrogate. |
| R `FME` (Metropolis-Gibbs) | https://CRAN.R-project.org/package=FME | CRAN | DRAM MCMC sampler used for Bayesian calibration. |
| R `mcgibbsit` | https://CRAN.R-project.org/package=mcgibbsit | CRAN | MCMC convergence diagnostic. |
| R `randtoolbox` | https://CRAN.R-project.org/package=randtoolbox | CRAN | Halton space-filling design. |

## NOT publicly available (blocks full replication)

| Artifact | Status | Impact |
|---|---|---|
| Experimental TID dataset (SAND2023-00940 — Hughart et al. 2022) | Sandia internal technical report; NOT on OSTI, sandia.gov, or elsewhere via search + OSTI API. | Cannot re-fit the Bayesian inverse problem to the true IBL / ACRR / LINAC ΔV_th vs dose measurements (nearly 80 device samples across three facilities). |
| GeneSiC 3.3 kV SiC MOSFET SEM cross-sections, SIMS doping profile | Proprietary Sandia measurements on GeneSiC datasheet-only device. Datasheet [23] itself is a manufacturer specification, not the SEM/SIMS data. | Cannot construct the exact Charon simulation geometry. |
| The 10,000-run Charon simulation training corpus 𝒯 | Not published in any repository the paper points to. | Cannot rerun the random-forest surrogate fit. |
| Trained random-forest surrogate ℳ_RF and DRAM chains | Not published. | Cannot rerun the posterior predictive tests. |
| Charon input decks / Dakota input files for this specific study | Not linked from paper. | Even with Charon installed, the exact 5-parameter TID sweep is not reproducible without them. |
| Kimpton model Charon plugin | Paper says "when we implemented the Kimpton model in Charon" — implementation likely in a Sandia branch/fork, not visible in the public `tcadsoftware/charon` repo (last push 2022, paper is 2026). | Even the modified TID kernel is not in the public Charon. |

## Independent-replication compute cost estimate

- 10,000 Charon runs × 448 cores × 0.5 h = 2,240,000 CPU-core-hours.
- On `uicgpu` (255 CPU cores) that is ~1.0 year of wall-clock, ignoring the fact that we do not have the input decks.
- Full re-execution is out of scope for this wave; the assigned "solid where evidence supports" verdict for this paper is SPOT-CHECK.
