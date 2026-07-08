# Artifacts Summary — QC-2208.04100

Root: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2208.04100-noise-resilient-phase-est-rc/`

## Top-level
- `report/` — everything user-facing (see below).
- `work/` — paper.pdf + pdftotext dump.
- `extraction/` — parser output stubs (nougat.mmd).
- `venv/` — local Python 3.14 venv (qiskit 2.5, qiskit-aer 0.17.2, numpy 2.5).

## report/
- `REPORT.md` — original narrative report (preserved, source of truth for §1–§8).
- `REPORT.tex` — LaTeX version of the same report with the verdict, headline tables, and honest critique.
- `open_questions.json` — 5-object bare JSON list of truly-open follow-ups with basis + concrete next_steps.
- `open_questions_section.tex` — human-readable LaTeX rendering of the same 5 questions.
- `workflow.md` — pipeline, environment, timings, reproducibility, provenance.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest critique of what this replication did and did NOT establish.

## report/evidence/
- `rpe_rc.py` — main Qiskit-Aer iterative-PE + RC implementation (wide sweep).
- `rpe_rc_strong.py` — strong-noise diagnostic (identified aliasing at ε·Lmax ≈ π).
- `rpe_rc_final.py` — final well-designed sweep (Lmax=32, Ns=20 000, Nr=80).
- `rc_exact_check.py` — shot-noise-free exact superoperator computation of the RC-twirled channel M^L.
- `run.log`, `run_strong.log`, `run_final.log`, `exact_run.log`, `exact_run_v2.log` — raw stdout logs.
- `results.json` — machine-readable final-sweep results.

## extraction/
- `nougat.mmd` — Nougat OCR stub (not run; qiskit-aer replication did not need OCR).

## Verdict
**REPLICATED** — both quantitative headlines (C1 bare linear scaling k≈1.00 vs paper 1.04; C2 RC super-linear scaling k≈2.26 (exact) vs paper 2.73; up to 1000× error reduction vs paper's "two orders of magnitude") are independently verified via a from-scratch Qiskit-Aer implementation plus an exact-superoperator analytic cross-check.

## Non-goals (explicitly not attempted)
- 10-qubit Floquet demo of Fig. 3(a) (paper's actual system).
- 8-qubit Shor order-finding of Fig. 4.
- Stochastic-noise sweep of Fig. 3(b) (~60% RC reduction claim).
- Theorem 1 formal verification.
- Hardware execution.

## File-count sanity
```
report/REPORT.md
report/REPORT.tex
report/open_questions.json
report/open_questions_section.tex
report/workflow.md
report/artifacts_summary.md
report/failure_analysis.md
report/evidence/*.py   (4 scripts)
report/evidence/*.log  (5 logs)
report/evidence/results.json
extraction/nougat.mmd
work/paper.pdf
work/paper.txt
```
