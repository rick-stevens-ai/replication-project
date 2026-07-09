# Artifact harvest

## Primary paper
| Item | URL | Size | SHA-256 |
|---|---|---|---|
| Chorin (1968) PDF | `https://www.ams.org/journals/mcom/1968-22-104/S0025-5718-1968-0242392-2/S0025-5718-1968-0242392-2.pdf` | 1.59 MB (10 pp) | `94c4a22f71ab16675207a1b44daa42e2e517896175a2061d2f6dfcfdfcf1dcef` |

## Reference benchmark data (embedded in source, not downloaded)
| Item | Source | Notes |
|---|---|---|
| Ghia, Ghia, Shin (1982) centerline u(y), v(x) at Re=100, Re=400 | J. Comput. Phys. 48, 387–411, Table I & II | 17 points per profile, transcribed as constants in `work/chorin_projection.py`. Same table is reproduced across many textbooks (e.g. Ferziger–Perić, 4th ed., Table 8.2). |

## Code (all our own, MIT-style, no external NS solver imports)
| File | Purpose |
|---|---|
| `work/chorin_projection.py` | MAC-staggered Chorin projection solver (vectorized NumPy). |
| `work/run_cavity_experiments.py` | Lid-driven cavity Re=100 (nx=32,64,128) and Re=400 (nx=64,128). |
| `work/pearson_test.py` | Chorin's own Section-5 test problem (Pearson exact soln). |
| `work/convergence_study.py` | Spatial 2nd-order + divergence-free audit. |
| `work/temporal_convergence.py` | Cauchy self-refinement O(dt) test. |
| `work/make_plots.py` | Summary PNGs. |
| `work/llm_judge.py` | Argo LLM-judge (never regex) over evidence JSON. |

## Dependencies
- Python 3.14.6
- NumPy 2.4.3
- SciPy 1.18.0 (only `scipy.sparse` + `scipy.sparse.linalg.splu` for pressure Poisson)
- Matplotlib 3.x (plotting only)

## Compute
All runs on `CherryRd` (macOS, local CPU). Total wall time for all experiments
under 8 minutes. No GPU, no external cluster, no paid endpoints. LLM judge
was called via free Argo proxy at `127.0.0.1:44497` (`argo:claude-sonnet-4.6`,
one call).
