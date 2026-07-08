# Artifacts summary — QC-2401.11056 GM-QAOA

Files under `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2401.11056-qaoa-grover-mixer/`:

| Path | Purpose |
|---|---|
| `work/paper.pdf` | Paper PDF (arXiv:2401.11056v3). |
| `work/paper.txt` | pdftotext extraction used for method reading. |
| `code/gm_qaoa.py` | Full simulator: GM mixer from rank-1 form, X mixer, cost operator; runs experiments E1/E2/E3 end-to-end (~82s single-core). |
| `report/REPORT.md` | Narrative markdown report (original, preserved). |
| `report/REPORT.tex` | LaTeX version with explicit critique of scope + baseline comparison (backfill). |
| `report/open_questions.json` | 5 truly-open questions (bare JSON list of `{q, basis, next_steps}`). |
| `report/open_questions_section.tex` | LaTeX-formatted version of the 5 open questions for the report appendix. |
| `report/workflow.md` | Environment + reproduction command + experiment layout. |
| `report/artifacts_summary.md` | This file. |
| `report/failure_analysis.md` | Honest critique: what is genuinely reimplemented vs. quoted, coverage gaps, single-instance caveats. |
| `report/evidence/results.json` | Raw per-permutation and per-restart numeric output from `code/gm_qaoa.py`. |
| `extraction/nougat.mmd` | Extraction stub (nougat not run; pdftotext used for method reading — numerical claims come from independent statevector, not from extraction). |

Verdict preserved: **REPLICATED** — C1 (permutation invariance) to 1e-15, C2 (X non-invariance) O(1) deviations, C3 (Eq. 8) to 1e-16, C4 (X > GM on structured MAX-CUT) confirmed with growing gap +0.068 → +0.147 at p=1..3. C5 (asymptotic theorem) explicitly flagged as not tested.
