# Artifacts Summary

## Top-level (preserved from original replication)

| Path | Kind | Description |
|---|---|---|
| `REPORT.md` | markdown | Original replication report (verdict, tables, numeric agreements) |
| `README.md` | markdown | How to reproduce |
| `PROGRESS.md` | markdown | Run log during original replication |
| `paper.pdf` | PDF | Local cache of Liew et al. IJMS 23, 6268 (2022) |
| `paper.txt` | text | pdftotext extraction of paper.pdf |
| `code/universe_photon.py` | python | Core photon-side repair-kinetics MC model |
| `code/fig4_left_rtd50.py` | python | R_TD50 reproduction driver (Table 3 col 4 / Fig 4 left) |
| `code/fig12_photon_trend.py` | python | Table 2 photon-only saturation-gain sweep |
| `code/plot_rtd50.py` | python | Overlay plot of R_TD50 curve + 14 paper data points |
| `results/rtd50_results.json` | JSON | Numeric outputs for §3.1 (all 14 conditions) |
| `results/fig4_left_run.log` | log | Run log for R_TD50 reproduction |
| `results/fig12_photon_trend.json` | JSON | Numeric outputs for §3.2 (Table 2 comparison) |
| `results/fig12_photon_run.log` | log | Run log for saturation-gain sweep |
| `figures/fig4_left_RTD50_replication.png` | PNG | R_TD50 curve overlay, 3.75-100 Gy/min |

## Backfill (added 2026-07-06)

| Path | Kind | Description |
|---|---|---|
| `report/REPORT.tex` | LaTeX | LaTeX rendering of the report, verdict, honest critique |
| `report/open_questions.json` | JSON | 5 open questions (q / basis / next_steps) |
| `report/open_questions_section.tex` | LaTeX | Open-questions section, includable |
| `report/workflow.md` | markdown | Stage-by-stage workflow narrative |
| `report/artifacts_summary.md` | markdown | This file |
| `report/failure_analysis.md` | markdown | Honest failure critique |
| `extraction/nougat.mmd` | Nougat MMD stub | Placeholder — full Nougat extraction not run |

## Coverage vs 8-artifact standard

1. REPORT.tex — present (`report/REPORT.tex`)
2. open_questions.json — present (`report/open_questions.json`)
3. open_questions_section.tex — present (`report/open_questions_section.tex`)
4. workflow.md — present (`report/workflow.md`)
5. artifacts_summary.md — present (this file)
6. failure_analysis.md — present (`report/failure_analysis.md`)
7. extraction/nougat.mmd — present (stub; see file for note)
8. Original REPORT.md — preserved at top level (source of truth for verdict)

All simulation-side artifacts (`code/`, `results/`, `figures/`) predate
the backfill and were not modified.
