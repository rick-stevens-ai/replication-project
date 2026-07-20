# Artifacts Summary — xie2025

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Extraction marker | `extraction/marker.md` | Bib metadata, extraction method, verbatim key equations (2, 10, 12), headline. |
| 2 | Nougat interim | `extraction/nougat.mmd` | Header-stamped `pdftotext -layout` body (honest interim; Nougat ML-OCR not available — no fabricated reconstruction). |
| 3 | Report (LaTeX) | `report/REPORT.tex` | Full replication write-up: model, method, results table, verdict REPLICATED. |
| 4 | Open questions | `report/open_questions.json` | 5 Q's (question/why_it_matters/next_step) + next_steps list. |
| 5 | Workflow | `report/workflow.md` | Step-by-step method, runner command, pitfalls, key results. |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file. |
| 7 | Failure analysis | `report/failure_analysis.md` | What was/wasn't replicated, limitations, honest scoping. |
| 8 | Evidence | `report/evidence/xie2025_replication.py`, `report/evidence/xie2025_result.json` | From-scratch code + computed results (result also SAVE-EARLY at `work/xie2025_result.json`). |

## Verdict: REPLICATED

## Headline numbers (all computed, none fabricated)
- Eq. (12) mixed-mode spectrum reproduced to **4.4e-16** vs numerical diagonalization.
- iCDW A-channel off-diagonal mixing = **−0.2121** (nonzero); rCDW = **7.8e-17** (zero).
- `mixing_present_in_iCDW_only = true`; `Eq12_reproduced = true`.
- Microscopic kernel cross-check: loop_order(φ=0)=0, loop-current susceptibility=−62.2.

## Credit
Microscopic loop-current cross-check uses `shared-kernels-cache/loop_current_meanfield_kernel.py`
(`ollie_loop_current_meanfield_kernel`).
