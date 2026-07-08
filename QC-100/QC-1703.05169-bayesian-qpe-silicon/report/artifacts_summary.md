# Artifacts summary — arXiv:1703.05169 replication

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1703.05169-bayesian-qpe-silicon/`

## Report artifacts (this backfill)
| File | Purpose |
|------|---------|
| `report/REPORT.md` | Original narrative report (preserved). |
| `report/REPORT.tex` | LaTeX version of the report with §Critique. |
| `report/open_questions.json` | 5 open questions (bare JSON list). |
| `report/open_questions_section.tex` | LaTeX version of the 5 open questions. |
| `report/workflow.md` | Chronological workflow + reproduce recipe + checklist. |
| `report/artifacts_summary.md` | This manifest. |
| `report/failure_analysis.md` | Honest self-critique / limitations audit. |
| `extraction/nougat.mmd` | Nougat-extraction stub (see file for rationale). |

## Evidence artifacts (from original run, preserved)
| File | Purpose |
|------|---------|
| `report/evidence/rfpe_sim.py` | Archived canonical simulation driver. |
| `report/evidence/experimentA_fig2a.json` | Seed-38 single-run trajectory (μ, σ, M, Θ, outcome per step). |
| `report/evidence/experimentB_scaling.json` | 200-trial RFPE + 400-trial SQL scaling data. |
| `report/evidence/experimentC_distribution.json` | 100-seed final-error distribution. |
| `report/evidence/fig2a_replication.png` | Fig. 2a-style plot with paper's two horizontal lines. |
| `report/evidence/scaling_rfpe_vs_sql.png` | Heisenberg-vs-SQL scaling plot. |
| `report/evidence/final_err_distribution.png` | Histogram (log scale) of 100-seed final errors. |

## Working directory (preserved, not edited during backfill)
| File | Purpose |
|------|---------|
| `work/1703.05169.pdf` | Source paper. |
| `work/1703.05169.txt` | `pdftotext -layout` extraction. |
| `work/rfpe_sim.py` | Canonical driver (mirror in `report/evidence/`). |
| `work/debug*.py` | Diagnostic scripts kept for provenance (esp. `debug3_grid.py` — grid-Bayes reference that revealed the Θ=μ symmetry bug). |
| `work/pick_seed.py` | 50-seed sweep used to select seed 38. |
| `work/venv/` | Python 3.13.11 venv (qiskit 2.5.0, numpy 2.5.0, scipy 1.18.0, matplotlib 3.11.0). |

## Reproduction cost
- Local CPU. No GPU. No paid API.
- Full experiment suite wallclock: ~14 s.
- Disk footprint: ~30 MB (dominated by venv and the 100-seed distribution JSON).

## Verdict cross-check
`verdict_preserved = REPLICATED` — matches (i) queue directive,
(ii) REPORT.md §6 verdict, (iii) evidence in `experimentA_fig2a.json`
(final-step |err| = 1.87e-4 rad ≤ paper's 2.4e-4 headline) and
`experimentB_scaling.json` (1.12× Heisenberg bound saturation).
