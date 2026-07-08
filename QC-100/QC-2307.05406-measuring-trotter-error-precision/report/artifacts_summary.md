# Artifacts summary — arXiv:2307.05406

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2307.05406-measuring-trotter-error-precision/`

## Report layer (`report/`)
- `REPORT.md` — canonical human-readable report (pre-existing, preserved)
- `REPORT.tex` — LaTeX render of the same, with critique section
- `workflow.md` — this replication's step-by-step method
- `artifacts_summary.md` — this file
- `failure_analysis.md` — honest critique of what did / did not reproduce and why
- `open_questions.json` — 5 truly-open follow-up questions (machine-readable, bare JSON list)
- `open_questions_section.tex` — LaTeX version of the same 5 questions
- `evidence/trotter24_results.json` — raw scan + adaptive results (L=6, L=8)
- `evidence/trotter24_L10.json` — L=10 adaptive results
- `evidence/llm_judge_gpt51.json` — Argo gpt-5.1 verdict JSON (AGREE / REPLICATED, conf 0.86)
- `evidence/llm_judge_gemini.json` — Argo gemini-2.5-pro verdict JSON (AGREE / REPLICATED, conf 0.95)
- `evidence/trotter24.py`, `trotter24_L10.py` — mirrored code

## Work layer (`work/`)
- `trotter24.py` — dense-statevector reimplementation (~200 LOC), L=6/8
- `trotter24_L10.py` — L=10 driver

## Extraction layer (`extraction/`)
- `nougat.mmd` — stub (OCR extraction of the arXiv PDF not attempted for this replication;
  paper was read directly from PDF text)

## Verdict
**REPLICATED** — headline claims C1 (direct-measurement estimator matches true infidelity to 4–5 sig figs)
and C2 (precision-guaranteed adaptive step: 9/9 tolerance hits) both exercised on
mixed-field Ising L=6/8/10. C3 (10× ratio at L=18) only directionally reproduced
(3.4–3.8× at L=6/8/10, monotonically growing).

Two independent LLM judges (gpt-5.1, gemini-2.5-pro) endorse REPLICATED.
