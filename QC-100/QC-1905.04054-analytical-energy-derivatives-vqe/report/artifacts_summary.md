# Artifacts Summary — QC-1905.04054 (Analytical VQE Energy Derivatives)

## Directory
`~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1905.04054-analytical-energy-derivatives-vqe/`

## Set / Verdict
- Set: QC-100
- Verdict: **REPLICATED** (headline claim directly exercised)

## Existing artifacts (pre-backfill)
- `report/REPORT.md` — original human-authored replication report (~10 KB).
- `code/vqe_h2_derivatives.py` — full replication script, single file,
  ~200 lines, no external configs. Runs end-to-end in ~5.5 min on a laptop CPU.
- `code/venv/` — pinned Python environment (PennyLane 0.45.1, NumPy 2.5.0,
  SciPy 1.18.0, pennylane_lightning 0.45.0).
- `report/evidence/vqe_h2_derivatives_results.json` — machine-readable
  results dump: E_VQE convergence trace, E_FCI reference, analytical /
  numerical / exact force values, PES scan.
- `logs/run.log` — full stdout capture of the replication run.
- `work/1905.04054.pdf` — arXiv preprint PDF.
- `work/1905.04054.txt` — pdftotext extraction for grep-driven re-reading.

## Backfill artifacts (added 2026-07-06)
- `report/REPORT.tex` — LaTeX version of the report, including a candid
  Critique / Failure Analysis section (Section 6) and `\input`ed
  `open_questions_section.tex` (Section 7).
- `report/open_questions.json` — machine-readable list of exactly 5
  uncertainty-first open questions (bare JSON list of
  `{q, basis, next_steps}` objects — no wrapper dict).
- `report/open_questions_section.tex` — human-readable LaTeX rendering of
  the same 5 open questions.
- `report/workflow.md` — step-by-step methodology + reproduction command +
  environment pins.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — standalone honest critique of scope,
  limits, and things not proven by this replication.
- `extraction/nougat.mmd` — nougat-format extraction stub (no OCR
  re-extraction performed; existing pdftotext extraction in
  `work/1905.04054.txt` is authoritative).

## 8-Artifact Standard Compliance
1. REPORT.md — present (`report/REPORT.md`)
2. REPORT.tex — added
3. open_questions.json — added (bare list of 5 objects)
4. open_questions_section.tex — added
5. workflow.md — added
6. artifacts_summary.md — added (this file)
7. failure_analysis.md — added
8. extraction/nougat.mmd — added (stub; authoritative source is
   `work/1905.04054.txt`)

## Reproducibility Notes
- Deterministic: seed=42, noiseless state-vector simulator (`default.qubit`).
- Environment fully pinned. No paid endpoints. No HPC / GPU / cloud.
- Re-run command in `workflow.md`.
