# Artifact Harvest — WoSt Replication

## Paper
| item | URL | size | checksum |
|------|-----|------|----------|
| arXiv PDF `2302.11815v3` | https://arxiv.org/pdf/2302.11815 | 28,672,972 B (28 MB) | md5 `fa1fc3332930ede62a931b400c56be28` |
| DOI landing (ACM TOG 42(4), Art. 1) | https://doi.org/10.1145/3592398 | metadata only | — |
| arXiv abstract page | https://arxiv.org/abs/2302.11815 | metadata only | title/DOI/author verified |

## Reference implementation (NOT used for independent replication)
| repo | URL | stars | language | notes |
|------|-----|-------|----------|-------|
| CMU `zombie` — Sawhney's grid-free MC library | https://github.com/rohan-sawhney/zombie | 296 | C++ | contains WoSt reference; deliberately NOT used to keep this an independent implementation. |
| `fcpw` (bounding-volume-hierarchy library the paper cites) | https://github.com/rohan-sawhney/fcpw | (cited) | C++ | not needed for our 2D disk replication (analytic geometry). |

## Own implementation artifacts
| file | purpose |
|------|---------|
| `work/wost2d.py` | 2D WoSt (Algorithm 1) + WoS + naive multi-intersect + reflecting-SDE, from-scratch in Python. |
| `work/run_experiments.py` | Drives C1 (convergence) + C2 (correctness) experiments. |
| `work/run_C3.py` | Drives C3 (WoSt vs SDE) comparison. |
| `work/make_plot.py` | Log-log convergence figure. |

## Experimental evidence
| file | claim | summary |
|------|-------|---------|
| `report/evidence/C1_convergence.json` | C1 | RMSE vs N=32..2048 at Neumann fractions {0, 0.25π, 0.5π, 0.75π}; log-log slopes fitted. |
| `report/evidence/C1_convergence.png` | C1 | Log-log convergence plot. |
| `report/evidence/C2_correctness.json` | C2 | WoSt vs naive multi-intersection RMSE at 5 Neumann fractions. |
| `report/evidence/C3_wost_vs_sde_dt*e*.json` | C3 | Fixed-N comparison: WoSt vs reflecting-SDE Euler-Maruyama at dt∈{1e-3, 5e-4}. |
| `report/evidence/experiment_run.log` | audit | Raw stdout of C1+C2 runs. |
| `report/evidence/C3_run.log` | audit | Raw stdout of C3 run. |
