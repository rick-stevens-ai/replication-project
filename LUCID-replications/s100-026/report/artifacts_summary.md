# Artifacts Summary — s100-026

| Path | Purpose | Origin |
|---|---|---|
| `source/paper.pdf` | Original Klapproth et al. 2021 PDF (Cancer Nanotech 12:27) | Springer OA download |
| `ocr/paper.txt` | `pdftotext -layout` dump, 878 lines | pre-existing |
| `extraction/nougat.mmd` | Nougat OCR stub (see file for status) | added 2026-07-05 backfill |
| `code/reproduce_table3_and_audit.py` | Python-only spot-check: Table 3 arithmetic + wt% audit | pre-existing |
| `evidence/spot_check.json` | Machine-readable audit output (per-species stats + wt% audit) | pre-existing |
| `report/REPORT.md` | Human-readable narrative report (canonical body) | pre-existing |
| `report/REPORT.tex` | LaTeX version with honest Critique section + \input open_questions_section.tex | added 2026-07-05 backfill |
| `report/open_questions.json` | 5 open questions with basis and concrete next_steps | added 2026-07-05 backfill |
| `report/open_questions_section.tex` | LaTeX rendering of the 5 open questions | added 2026-07-05 backfill |
| `report/workflow.md` | Method log of what was actually done vs. skipped | added 2026-07-05 backfill |
| `report/artifacts_summary.md` | This file — inventory of every artifact | added 2026-07-05 backfill |
| `report/failure_analysis.md` | HONEST critique + verdict correction (queue REPLICATED → substance PARTIAL) | added 2026-07-05 backfill |

## Standard 8-artifact checklist

1. `source/paper.pdf` ✅
2. `ocr/paper.txt` ✅
3. `extraction/nougat.mmd` ✅ (stub; nougat not run, see file)
4. `code/reproduce_table3_and_audit.py` ✅
5. `evidence/spot_check.json` ✅
6. `report/REPORT.md` + `report/REPORT.tex` ✅
7. `report/open_questions.json` + `open_questions_section.tex` ✅
8. `report/workflow.md` + `artifacts_summary.md` + `failure_analysis.md` ✅

## What is intentionally missing

- No `runs/`, `output/`, `phsp/`, `sdd/`, or any TOPAS artifacts. The MC pipeline was
  not stood up — see `failure_analysis.md`. This replication is an analytical audit,
  not an engine-level rerun.
- No AuFeNP coordinate file (author would have to release one).
- No Stage-1 or Stage-2 phase-space files (author would have to release these).
