# Artifacts summary — QC-100 W3

| File | Purpose |
|---|---|
| `REPORT.md`                         | Top-level canonical replication report (verdict, numeric table) — pre-existing, preserved. |
| `paper.md`                          | Source-text extraction of the paper's claims — pre-existing. |
| `replicate.py`                      | Single-file numpy state-vector simulator: DJ / BV / QPE / Shor / Grover — pre-existing. |
| `results.json`                      | Machine-readable numeric results consumed by both `REPORT.md` and `REPORT.tex` — pre-existing. |
| `report/REPORT.tex`                 | LaTeX report with critique + \input of open-questions section (backfill). |
| `report/open_questions.json`        | 5 open questions, structured JSON (bare list) (backfill). |
| `report/open_questions_section.tex` | Same 5 questions as LaTeX section (backfill). |
| `report/workflow.md`                | Reproduction steps + artifact-purpose map (backfill). |
| `report/artifacts_summary.md`       | This file (backfill). |
| `report/failure_analysis.md`        | Honest critique of what was and was not exercised (backfill). |
| `extraction/nougat.mmd`             | Nougat extraction stub — no rerun; semantic capture is in `paper.md` (backfill). |

**Total artifacts:** 11 files (4 pre-existing + 7 backfill).
Backfill count: 7 new files added; 0 files deleted or moved.
Top-level `REPORT.md` was intentionally left in place (not moved into `report/`).
