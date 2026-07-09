# Artifacts summary — Osher & Sethian (1988) level-set replication

All paths are relative to
`~/Dropbox/REPLICATE-PROJECT/PDE-Osher-Sethian-levelset-1988/`.

## Source paper
| Artifact | Location | Notes |
|---|---|---|
| Paper PDF | fetched from `http://math.berkeley.edu/~sethian/2006/Papers/sethian.osher.88.pdf` | sha256 `508150b5…`, 38 pages |
| Harvest manifest | `report/artifact_harvest.md` | URL, sha256, page count |

## Independent implementation
| Artifact | Location | Notes |
|---|---|---|
| Level-set code | `work/levelset.py` | single file; upwind Godunov convection + central-difference curvature + forward-Euler time step; every experiment is a function |
| Driver | `python work/levelset.py` | reproduces all 6 runs (C1, C2×3, C2b, C3) end-to-end |
| Virtual environment | `work/venv/` | Python 3.13, NumPy 2.5.1, SciPy 1.18.0, Matplotlib 3.11.0, scikit-image 0.26.0 |

## Numerical evidence (this replication's outputs)
| Artifact | Location | Purpose |
|---|---|---|
| C1 trajectory (radius vs t) | `report/evidence/C1_expanding_circle.csv` | numerical vs exact radius, F=1, N=201 |
| C1 plot | `report/evidence/C1_expanding_circle.png` | radius trajectory |
| C2 trajectory, N=101 | `report/evidence/C2_shrink_N101.csv` | MCF radius under grid refinement |
| C2 trajectory, N=201 | `report/evidence/C2_shrink_N201.csv` | MCF radius under grid refinement |
| C2 trajectory, N=301 | `report/evidence/C2_shrink_N301.csv` | MCF radius under grid refinement |
| C2b star snapshots | `report/evidence/C2b_star_snapshots.png` | corners rounding off; front becomes convex |
| C3 merge snapshots | `report/evidence/C3_merge_snapshots.png` | two disks fuse into one, no re-meshing |
| LLM-judge transcript | `report/evidence/llm_judge.txt` | per-claim scores + one-line summary |

## Report artifacts
| Artifact | Location | Notes |
|---|---|---|
| Canonical report | `report/REPORT.md` | Markdown, section-numbered, verdict = REPLICATED |
| LaTeX report | `report/REPORT.tex` | includes dedicated GENUINE CRITIQUE section |
| Workflow narrative | `report/workflow.md` | step-by-step reproduction procedure |
| Artifacts summary | `report/artifacts_summary.md` | this file |
| Open questions | `report/open_questions.json` | 5 grounded, still-open questions |
| Failure analysis | `report/failure_analysis.md` | limitations, near-misses, negative results |

## Headline numbers (from REPORT.md)
| Metric | Value |
|---|---|
| C1 relative error (F=1 expansion, N=201) | 0.36% |
| C1 max abs error over trajectory | 2.87 × 10⁻³ |
| C2 observed convergence order, L² | 1.63 – 1.69 |
| C2 observed convergence order, L∞ | 1.34 – 1.93 |
| C2b fraction of time steps with perimeter increase | 0.00% (0 of 9 000) |
| C3 merge-time relative error | 0.27% (0.1504 vs 0.1500) |
| Total wall-clock, all experiments | < 3 min on a laptop CPU |
| LLM-judge verdict | REPLICATED |
