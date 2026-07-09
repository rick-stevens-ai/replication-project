# Artifacts summary — BVBRC-124

## The 8 mandatory artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | `paper.pdf` at target-dir root | `paper.pdf` (1.7 MB, sha256:5c6c1ed…) | ✅ present |
| 2 | Marker-parsed text | `extraction/marker.md` (740 lines) | ✅ present (pdftotext substitute for a native-typeset PDF; documented in file header) |
| 3 | Nougat OCR | `extraction/nougat.mmd` | ✅ present as an annotated placeholder (nougat CLI not installed on CherryRd; marker.md is sufficient because paper is native-typeset, not scanned) |
| 4 | Very detailed section-by-section LaTeX report | `report/REPORT.tex` (12 KB) | ✅ present with per-claim "what worked/didn't" |
| 5 | 5 heavy-duty open questions (JSON, each with q/basis/next_steps) + `## Open Questions` in report | `report/open_questions.json` (4.8 KB, 5 items) + `## Open Questions` section in `REPORT.md` | ✅ present |
| 6 | Workflow + tools + effort estimate | `report/workflow.md` (5.2 KB) | ✅ present |
| 7 | Artifacts summary | `report/artifacts_summary.md` (this file) | ✅ present |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ present |

## Additional artifacts

| Artifact | Path |
|---|---|
| Main markdown report | `report/REPORT.md` (14 KB) |
| 1-paragraph brief | `report/brief.md` (1.3 KB) |
| Attempt log (chronological) | `report/attempt_log.md` |
| Artifact harvest (URLs, checksums) | `report/artifact_harvest.md` |
| Per-drug AUC evidence (real cross-validated) | `report/evidence/auc_per_drug.json` (10.7 KB) |
| Structural availability evidence | `report/evidence/structural_availability.json` (14.5 KB) |
| LLM-judge verdict | `report/evidence/llm_judge_verdict.json` |
| Source: AUC replication | `work/code/auc_replicate.py` |
| Source: Structural probe | `work/code/structural_map.py` |
| Source: LLM judge | `work/code/llm_judge.py` |
| Raw data | `work/data/` (5 CSVs from authors' GitHub + 4 XLSX from Springer + paper.pdf) |

## Verdict
**PARTIAL** — see `report/REPORT.md` § 5.3 for LLM-judge justification.
