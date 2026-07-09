# Artifacts Summary — Davis & LeVeque 2020 Adjoint-AMR Replication

**Paper:** Davis & LeVeque, ACM TOMS 2020, DOI [10.1145/3392775](https://doi.org/10.1145/3392775).
**Replication dir:** `~/Dropbox/REPLICATE-PROJECT/PDE-Davis-LeVeque-adjoint-AMR-2020/`.
**Verdict:** REPLICATED (high confidence).

## Source code (independent build)

| Artifact | Version / SHA | Notes |
|---|---|---|
| Clawpack | v5.9.2 | `git clone --depth 1 -b v5.9.2` |
| amrclaw submodule | 4b50c26 | provides `acoustics_1d_adjoint` + `acoustics_2d_adjoint` examples |
| classic submodule | a27a495 | |
| clawutil submodule | 5aaee22 | |
| geoclaw submodule | 2226769 | not exercised |
| pyclaw submodule | c2b04786 | |
| riemann submodule | c7a9ed0 | |
| visclaw submodule | 32e257c8 | plotting stack |

## Environment

| Item | Value |
|---|---|
| Host | `uicgpu01` (Ubuntu 20.04) |
| Hardware | 8×A100 GPUs (unused), 255 CPU cores, 2 TB RAM |
| Python | 3.8.10 in `~/work/pde-davis-leveque-amr/clawvenv/` |
| numpy / matplotlib / scipy | 1.24.4 / 3.7.5 / 1.10.1 |
| clawpack (PyPI) | 5.9.2 |
| Compiler | gfortran, `FFLAGS="-O2 -fopenmp"` |
| Threads | `OMP_NUM_THREADS=4` (1D), `=8` (2D) |

## Example directories used

- `amrclaw/examples/acoustics_1d_adjoint/` — 1D linear acoustics, constant impedance, target at x=1.5.
- `amrclaw/examples/acoustics_2d_adjoint/` — 2D linear acoustics, piecewise-constant medium (interface at x=0.5), target point-spike at (3.5, 0.5).

Both are paper-authored (README cites Davis+LeVeque 2018).

## 1D run outputs

Reference `J = 2.44403775×10⁻²` (Richardson tol=1e-6, finest available).

| Run tag | Method | tol | L1 | L2 | L3 | Total | J | rel-err |
|---|---|---|---:|---:|---:|---:|---|---:|
| 1d_adj_0.1 | adjoint-magnitude | 0.1 | 2,700 | 13,312 | 63,776 | 79,788 | 8.28e-3 | 6.6e-1 |
| **1d_adj_0.01** | adjoint-magnitude | **0.01** | 2,700 | 24,992 | **129,760** | 157,452 | 2.4465e-2 | **1.01e-3** |
| 1d_adj_0.001 | adjoint-magnitude | 0.001 | 2,700 | 26,240 | 154,016 | 182,956 | 2.4488e-2 | 1.94e-3 |
| 1d_adj_0.0005 | adjoint-magnitude | 0.0005 | 2,700 | 27,200 | 161,792 | 191,692 | 2.4416e-2 | 9.94e-4 |
| **1d_rich_1e-4** | Richardson | **1e-4** | 2,700 | 31,840 | **209,184** | 243,724 | 2.4437e-2 | **1.37e-4** |
| 1d_rich_1e-5 | Richardson | 1e-5 | 2,700 | 32,032 | 224,992 | 259,724 | 2.4440e-2 | 1.85e-5 |
| 1d_rich_1e-6 | Richardson | 1e-6 | 2,700 | 32,224 | 238,368 | 273,292 | 2.4440e-2 | 0 (ref) |

## 2D run outputs

| Run tag | Method | tol | L1 | L2 | L3 | Total | Wall (s) | CPU (s) | Mass at t=7 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2d_adj_0.04 | adjoint-magnitude | 0.04 | 212,500 | 249,008 | 712,912 | **1,174,420** | **0.856** | 4.696 | −0.14886 |
| 2d_rich_1e-3 | Richardson | 1e-3 | 212,500 | 850,400 | 5,574,880 | **6,637,780** | **2.545** | 7.668 | −0.14935 |
| Ratio (Rich/adj) | — | — | 1.00 | 3.42 | **7.82** | **5.65** | **2.97** | 1.63 | <0.4% diff |

## Figures

- `evidence/fig_error_vs_work.png` — 1D J relative error vs. total L3 cell updates, log-log axes; adjoint (blue circles) lies to the left of Richardson (red squares) at the 10⁻³ error band. Confirms C3.
- `evidence/fig_refinement_levels.png` — 1D refinement level along x at t=15; adjoint concentrates L3 around target x=1.5 and approaching wavefronts, Richardson has broader L3 coverage across the domain. Confirms C1.
- `evidence/fig_2d_refinement.png` — 2D refinement heatmap side-by-side at t=7; adjoint L3 is a compact triangular region between origin (initial pulse) and target (3.5, 0.5); Richardson refines every wave crest across the whole domain. Confirms C1 and C4 visually.

## Evidence bundle

- `evidence/llm_judge_verdict.json` — Argo `claude-opus-4.7` per-claim reproduced/not-reproduced verdict; overall REPLICATED.
- `fort.amr` per run — Clawpack per-level cell-update logs (source of the cell-count columns).
- `timing.csv` per 2D run — Clawpack built-in wall/CPU timing (source of the wall/CPU columns).
- `fort.q00xx` frames per run — Clawpack solution snapshots (input to `compute_functional_all.py` and to the 2D mass proxy).

## Scripts

- `work/run_amr_sweep.sh` — driver that patches `setrun.py` and iterates through the (method, tol) sweep.
- `work/compute_functional_all.py` — computes J = ∫ φ(x) · p(x, t_f) dx for each 1D run.
- `work/attempt_log.md` — records the `use_adjoint=False` `free(): invalid pointer` crash and the workaround (keep `use_adjoint=True` even for Richardson-only runs to preserve aux-array bookkeeping).

## Deliverables

- `report/REPORT.md` — full replication report (source of this summary).
- `report/REPORT.tex` — typeset version with dedicated critique section.
- `report/open_questions.json` — 5 genuinely-open follow-up questions.
- `report/workflow.md` — end-to-end reproduction procedure.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — post-mortem of methodological compromises.

## Compute footprint

- Full sweep completes in a single overnight interactive session on `uicgpu`.
- Disk: a few hundred MB in `work/` (dominated by `fort.q*` frames).
- No GPU used, no paid API used for compute; LLM-judge uses free Argo endpoint.
