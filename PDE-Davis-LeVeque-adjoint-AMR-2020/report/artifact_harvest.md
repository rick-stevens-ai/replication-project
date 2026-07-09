# Artifact Harvest — PDE-Davis-LeVeque-adjoint-AMR-2020

## Paper / preprint
| Artifact | URL | Notes |
|---|---|---|
| Paper (ACM TOMS 2020) | doi.org/10.1145/3392775 | Paywalled at ACM Digital Library, not fetched |
| arXiv preprint (2018) | https://arxiv.org/pdf/1810.00927 | GREEN open access, 5.1 MB PDF, `work/davis_leveque_2020.pdf` |
| S2 record | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3392775 | paperId 0c583cabcc0faa130145017d665bb983a028d6a8 |

## Code
| Artifact | URL | Notes |
|---|---|---|
| Clawpack v5.9.2 (all submodules) | https://github.com/clawpack/clawpack (tag v5.9.2) | Cloned on uicgpu:~/work/pde-davis-leveque-amr/clawpack. Submodule pins: amrclaw@4b50c26 · classic@a27a495 · clawutil@5aaee22 · geoclaw@2226769 · pyclaw@c2b04786 · riemann@c7a9ed0 · visclaw@32e257c8. |
| acoustics_1d_adjoint example | in clawpack/amrclaw/examples/acoustics_1d_adjoint | Paper-linked example (README explicitly cites Davis+LeVeque 2018) |
| acoustics_2d_adjoint example | in clawpack/amrclaw/examples/acoustics_2d_adjoint | Paper-linked example (Example 3 analog) |
| Python bindings | PyPI clawpack==5.9.2 | Installed in venv |
| Historical paper example archive | github.com/BrisaDavis (referenced in paper abstract) | Not fetched; the shipped `amrclaw/examples/*_adjoint` are the maintained version of the paper's Github artifacts. |

## Runtime environment
| Item | Value |
|---|---|
| Host | uicgpu01 (Ubuntu, 8×A100, 255 cores, 2 TB RAM) |
| Python | 3.8.10 (system) → venv `~/work/pde-davis-leveque-amr/clawvenv` |
| gfortran | (system default on uicgpu) |
| numpy | 1.24.4 |
| matplotlib | 3.7.5 |
| scipy | 1.10.1 |
| Clawpack | 5.9.2 (both PyPI wheel + git source) |
| OpenMP threads | 4 for 1D, 8 for 2D |
| LLM judge | Argo proxy http://localhost:44497/v1, model argo:claude-opus-4.7, key=stevens |

## Outputs archived
Under `report/evidence/` in this dir:
- `fort.amr.1d_adjoint_reference` — full 1D AMRClaw log
- `fort.amr.2d_adjoint` / `fort.amr.2d_richardson` — 2D AMRClaw logs (per-level cell updates + memory + timing)
- `timing.2d_adjoint.csv` / `timing.2d_richardson.csv` — per-frame Clawpack timing
- `results_parsed.csv` — 1D sweep: total cells and per-level updates for 7 runs
- `functional_results.csv` — functional-of-interest J and relative error for 7 1D runs
- `fig_error_vs_work.png` — 1D J-error vs L3 cell updates comparison
- `fig_pressure_snapshots.png` — 1D pressure at t=15
- `fig_refinement_levels.png` — 1D refinement level along x
- `fig_2d_refinement.png` — 2D cell-level side-by-side snapshot
- `fig_2d_pressure.png` — 2D pressure field snapshot
- `llm_judge_verdict.json` — Argo LLM-judge verdict

Under `work/` in this dir:
- `davis_leveque_2020.pdf` — the paper (arXiv preprint)
- `run_amr_sweep.sh` — sweep driver
- `parse_results.py` — fort.amr parser
- `compute_functional*.py` — functional-of-interest J calculators (1D)
- `plot_results.py`, `plot_2d.py` — figure generators

On uicgpu (not archived here to save space; recoverable by rerunning the scripts):
- `~/work/pde-davis-leveque-amr/sweep/*_output/` — full fort.q AMRClaw output for each of 7 1D runs
- `~/work/pde-davis-leveque-amr/clawpack/amrclaw/examples/acoustics_2d_adjoint/_output_*` — 2D outputs
