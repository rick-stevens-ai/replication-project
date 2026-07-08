# Artifacts Summary — QC-1611.04542-grover-analog-coherence

## Standard 8-artifact set (post-backfill)

| # | Artifact | Path | Purpose |
|---|----------|------|---------|
| 1 | REPORT.md (narrative) | `report/REPORT.md` | Original replication write-up, verdict, quantitative tables. |
| 2 | REPORT.tex (LaTeX, honest critique) | `report/REPORT.tex` | Compilable LaTeX version, includes explicit Critique section and `\input{open_questions_section.tex}`. |
| 3 | open_questions.json | `report/open_questions.json` | Bare JSON list of 5 open-question objects `{q, basis, next_steps}`. |
| 4 | open_questions_section.tex | `report/open_questions_section.tex` | LaTeX rendering of the 5 open questions (for REPORT.tex include). |
| 5 | workflow.md | `report/workflow.md` | Step-by-step reproduction recipe + compute budget + non-goals. |
| 6 | artifacts_summary.md | `report/artifacts_summary.md` | This file. Index of the 8-artifact set. |
| 7 | failure_analysis.md (honest critique) | `report/failure_analysis.md` | What this replication does NOT establish, per-claim honesty audit. |
| 8 | extraction/nougat.mmd | `extraction/nougat.mmd` | Stub / marker for OCR-extracted paper text (see file). |

## Pre-existing artifacts preserved (not modified in backfill)

- `report/REPORT.md` — the original replicator report (READ-only in this backfill wave).
- `code/grover_coherence.py` — the Qiskit simulation source.
- `code/plot_tradeoff.py` — plotting source.
- `report/evidence/grover_coherence_n3.json` — per-k records, n=3.
- `report/evidence/grover_coherence_n4.json` — per-k records, n=4.
- `report/evidence/grover_coherence_n5.json` — per-k records, n=5.
- `report/evidence/summary.json` — top-line summary.
- `report/evidence/coherence_success_tradeoff.png` — three-panel plot.
- `work/paper.pdf`, `work/paper.txt` — paper source + extracted text.
- `.venv/` — Python environment.

## Verdict
**REPLICATED** — C1 (Grover k_opt), C2 (C_l1 collapse-at-peak), C3 (C_r collapse-at-peak) all quantitatively reproduced on Qiskit statevector at n=3,4,5. C4/C5 out of scope.
