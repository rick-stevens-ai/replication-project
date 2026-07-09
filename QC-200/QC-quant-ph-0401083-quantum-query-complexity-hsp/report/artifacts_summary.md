# Artifacts inventory — QC-200/QC-quant-ph-0401083-quantum-query-complexity-hsp

## Top-level (8 required artifacts)
| # | Path | Purpose | Size |
|---|---|---|---|
| 1 | `paper.pdf` | Original PDF, arXiv:quant-ph/0401083 | 109 KB, 8 pp |
| 2 | `extraction/marker.md` | Marker-style parse (pdftotext fallback with header) | ~30 KB |
| 3 | `extraction/nougat.mmd` | Nougat-style parse (pdftotext -layout fallback with header) | ~35 KB |
| 4 | `report/REPORT.tex` | Detailed section-by-section report; compile to REPORT.pdf | ~13 KB |
| 5 | `report/open_questions.json` | 5 heavy-duty q/basis/next_steps triples | ~4.5 KB |
| 6 | `report/workflow.md` | Full step-by-step + tools/versions/time estimate | ~3.5 KB |
| 7 | `report/artifacts_summary.md` | THIS FILE | ~2 KB |
| 8 | `report/failure_analysis.md` | Honest friction / residual gaps | ~4 KB |

## Evidence / code
| Path | Purpose |
|---|---|
| `report/evidence/hsp_query_complexity.py` | Group construction, coset-state density matrices, PGM, confusion matrix, main experiment |
| `report/evidence/fit_scaling.py` | Linear fit of log_2(err_PGM) vs s; slope in bits/query; extrapolated s* |
| `report/evidence/monte_carlo_check.py` | Independent 20k-shot validation of analytic PGM on (D_4, s=3) |
| `report/evidence/results/hsp_query_complexity_results.json` | Full confusion diagonals + timings + paper bound for every (group, s) |
| `report/evidence/results/scaling_analysis.txt` | Human-readable slope table + interpretation |
| `report/evidence/results/scaling_fits.json` | Machine-readable slope fits + extrapolated s* |
| `report/evidence/results/monte_carlo_check.json` | Analytic-vs-empirical diagonals + Hoeffding CI + PASS flag |
| `report/evidence/judge_prompt.md` | The prompt shown to both Argo judges |
| `report/evidence/judge_panel.json` | Both judges' full verdicts + confidences + adjudication rationale |
| `report/evidence/run.log` | Live stdout from `hsp_query_complexity.py` |
| `report/evidence/mc.log` | Live stdout from `monte_carlo_check.py` |
| `work/paper.txt` | `pdftotext -layout` of paper.pdf |

## Traces of every LLM call
- 2 judge calls to `http://localhost:44497/v1/chat/completions` (Argo).
  - Model `argo:gpt-5.2`, temperature default, max_tokens 800.
  - Model `argo:claude-opus-4.7`, temperature default, max_tokens 800.
  - Full prompt archived in `report/evidence/judge_prompt.md`, full responses in `report/evidence/judge_panel.json`.
- No other LLM calls made during this replication.

## Reproducibility hash
- Random seed for MC: `SEED = 20260705` (in `monte_carlo_check.py`).
- Deterministic PGM path: all matrix ops are deterministic given numpy version.
- Group construction is deterministic (fixed permutation generators).
