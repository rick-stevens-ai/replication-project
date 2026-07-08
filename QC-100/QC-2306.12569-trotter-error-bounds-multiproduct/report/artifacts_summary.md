# Artifacts summary — QC-2306.12569-trotter-error-bounds-multiproduct

Verdict (preserved from `report/REPORT.md`): **REPLICATED**.

## Pre-existing artifacts (untouched)
| Path | Role |
| --- | --- |
| `report/REPORT.md` | Original replication report (source of truth) |
| `code/mpf_replication.py` | Clean-room implementation: H, S_2, MPF, error metric |
| `code/mpf_scaling_check.py` | Lambda scan + slope fit |
| `report/evidence/mpf_results.json` | Main experiment numbers |
| `report/evidence/scaling_check.json` | Lambda scan + fitted slopes |
| `logs/run1.log` | Raw stdout of main run |
| `logs/scaling.log` | Raw stdout of scaling run |
| `work/paper.pdf` | Source paper (arXiv 2306.12569v2) |
| `work/paper.txt` | pdftotext extract |

## Backfill artifacts (added 2026-07-06)
| Path | Role |
| --- | --- |
| `report/REPORT.tex` | LaTeX archival version of REPORT.md, with genuine critique section |
| `report/open_questions.json` | 5 open questions in canonical JSON schema |
| `report/open_questions_section.tex` | LaTeX rendering of the 5 open questions |
| `report/workflow.md` | Step-by-step pipeline (env, commands, artifacts) |
| `report/artifacts_summary.md` | This inventory |
| `report/failure_analysis.md` | Honest critique of what was NOT independently checked |
| `extraction/nougat.mmd` | Stub — no re-extraction performed |

## Headline exercised
- **C2 (paper's central quantitative claim):** MPF with `k = lambda*(4,13,17)`,
  `c = (0.016088, -1.794934, 2.778846)` yields effective error slope `-4` in `1/lambda`
  on top of `p=2` base Trotter.
- **Measured:** MPF slope `-4.036` (`n=3`) and `-4.055` (`n=4`) at `t=1`;
  Trotter baseline slope `-2.001` / `-2.007`. **Match.**

## Not exercised
- Larger `n` (paper carried numerics to `n=14`).
- Analytical Theorem 1 boundary tests.
- Dynamic MPF (Section VI).
- Minimax MPF (Section VII).
- Hardware / shot noise.
- Trotter-1 and Trotter-4 baselines (only `S_2` compared).
- Sample-cost Pareto with shot-variance overhead.
- Seed variance (single seed = 1 only).
- Alternate Hamiltonians (only Childs-Maslov Heisenberg).
