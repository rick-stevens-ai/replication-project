# Artifacts summary — QC-2101.05513-local-classical-vs-p2-qaoa

## Report (`report/`)
- `REPORT.md` — narrative replication report (original 2026-07-03 authoring, canonical).
- `REPORT.tex` — LaTeX version with critique section (backfilled 2026-07-05).
- `open_questions.json` — 5 open follow-on questions with basis + concrete next_steps.
- `open_questions_section.tex` — same 5 questions rendered as a LaTeX section.
- `workflow.md` — chronological replication workflow log.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest critique of what was and was not exercised.

## Evidence (`report/evidence/`)
- `qaoa2_aer_heawood_v2.json` — QAOA_2 on Heawood (D=3, n=14): best cut 0.75591 vs paper 0.7559. 5-digit match.
- `qaoa2_aer_heawood_smoke.json`, `qaoa2_aer_heawood_v3.json` — intermediate smoke runs.
- `qaoa2_result.json` — early QAOA_2 test output.
- `qaoa2_pg23.json` — QAOA_2 on PG(2,3) (D=4, n=26 qubits): best cut 0.66773 vs paper 0.6693. 0.24% relative error (short 4-restart budget).
- `thr_heawood.json` — Threshold_1/Threshold_2 Monte Carlo on Heawood, 10k trials.
- `thr_pg23.json` — Threshold_1/Threshold_2 Monte Carlo + full (τ_1,τ_2) sweep on PG(2,3), 30k trials. Best 0.7083 ± 0.0017 at (3,3).
- `judges.json` — 3-model Argo LLM-judge panel raw output (Claude Sonnet 4.6, GPT-5.2, Gemini 2.5 Pro). Majority REPLICATED (2/3).

## Code (`code/`)
- `qaoa2_aer.py` — QAOA_2 statevector on arbitrary graph (Aer, COBYLA, diagonal-Z objective with precomputed sign arrays).
- `threshold_maxcut.py` — n-step threshold algorithm + Monte Carlo estimator.
- `pg23_incidence.py` — projective plane PG(2,3) → Levi incidence graph (the (4,6)-cage).
- `threshold_pg23.py` — Threshold_1/Threshold_2 driver for PG(2,3).
- `qaoa2_pg23_run.py` — 26-qubit QAOA_2 driver for PG(2,3).

## Work-in-progress and inputs (`work/`)
- `paper.pdf` — arXiv:2101.05513 PDF.
- `paper.txt` — pdftotext extraction.

## Extraction (`extraction/`)
- `nougat.mmd` — parser-normalized extraction stub (backfilled 2026-07-05; canonical source is the arXiv LaTeX / PDF; not re-parsed with a heavyweight parser in this replication because the paper is short and reads cleanly).

## Endpoint audit
- Local CPU only for all simulations. Argo (free) used only for the 3-judge LLM panel.
- No paid endpoints touched.

## File count
- 7 backfilled artifacts + pre-existing REPORT.md + 7 evidence JSON + 5 code files + 2 work inputs = 22 files total.
