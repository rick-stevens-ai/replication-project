# Artifacts Summary — arXiv:1803.03621

## Report
- `report/REPORT.md` — original hand-written replication report (source of truth for verdict)
- `report/REPORT.tex` — LaTeX version with explicit Critique section, produced during 2026-07-05 backfill
- `report/brief.md` — initial task brief
- `report/attempt_log.md` — chronological attempt notes
- `report/artifact_harvest.md` — provenance / artifact-list
- `report/workflow.md` — reproducible workflow (2026-07-05 backfill)
- `report/artifacts_summary.md` — this file (2026-07-05 backfill)
- `report/failure_analysis.md` — honest critique (2026-07-05 backfill)
- `report/open_questions.json` — 5 open questions, bare JSON list (2026-07-05 backfill)
- `report/open_questions_section.tex` — same 5 questions, LaTeX (2026-07-05 backfill)

## Evidence
- `report/evidence/results_monomial.json` — C1 (Table 1) numeric replication
- `report/evidence/results_clifford.json` — C2 (Table 3) numeric replication
- `report/evidence/results_compare.json` — C3 (Fig 1) three-protocol comparison
- `report/evidence/llm_judge_verdict.md` — Argo GPT-5.2 verdict, verbatim
- `report/evidence/monomial_run.log` — run log for C1
- `report/evidence/clifford_run.log` — run log for C2
- `report/evidence/compare_run.log` — run log for C3
- `report/evidence/rb_three_protocols.png` — survival-curve plot (Fig 1 analogue)
- `report/evidence/monomial_error_vs_d.png` — error-vs-d scaling plot

## Code
- `work/monomial_rb.py` — monomial-unitary group class + Table 1 driver
- `work/clifford_generator_rb.py` — Clifford generator RB + Table 3 driver
- `work/compare_protocols.py` — three-protocol driver
- `work/plot_results.py` — plot generation
- `work/judge.py` — LLM-judge script (Argo endpoint)

## Extraction
- `extraction/nougat.mmd` — Nougat/OCR extraction stub (2026-07-05 backfill; original PDF-to-text was via `pdftotext -layout`, see `work/1803.03621.txt`)

## Paper Source
- `work/1803.03621.pdf` — arXiv PDF (public, open-access)
- `work/1803.03621.txt` — pdftotext extraction

## Backfill Note (2026-07-05)
The 2026-07-04 initial replication produced REPORT.md + evidence + code but not the standardised 8-artifact set. This backfill pass added: REPORT.tex, open_questions.json, open_questions_section.tex, workflow.md, artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd. No re-runs were performed; all numeric results are from the original 2026-07-04 simulation traces.
