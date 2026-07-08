# Artifacts Summary — QC-1808.03623

## Directory
`~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1808.03623-mitigating-algorithmic-errors-hamsim/`

## Files

### `report/`
- `REPORT.md` — full narrative (original replication artifact).
- `REPORT.tex` — LaTeX version of the report (backfill).
- `workflow.md` — step-by-step replication workflow (backfill).
- `artifacts_summary.md` — this file (backfill).
- `failure_analysis.md` — honest critique + boundary analysis (backfill).
- `open_questions.json` — 5 open questions with basis + next_steps (backfill).
- `open_questions_section.tex` — LaTeX-formatted open questions (backfill).
- `evidence/results.json` — main Trotter sweep and mitigation numbers.
- `evidence/scaling_curve.json` — polynomial-fit coefficients.
- `evidence/run.log` — raw stdout of both scripts.

### `code/`
- `replicate_algo_error_mitigation.py` — main replication script:
  builds H, exact ref, sweeps N, applies linear + Richardson mitigations.
- `error_scaling_curve.py` — independent 9-point poly fit to
  confirm Trotter-series structure.

### `extraction/`
- `nougat.mmd` — extracted paper markdown (stub if OCR pipeline
  not run; the machine-readable claim mining was done from
  `work/paper.txt` instead).

### `work/`
- `paper.pdf` — arXiv 1808.03623 v-latest.
- `paper.txt` — text extraction for claim mining.

## Environment lockfile (informal)
qiskit 2.5.0
qiskit-aer 0.17.2
numpy 2.4.3
scipy 1.18.0
Python 3 on Darwin 25.3.0.

## Verdict
**REPLICATED** — noise-free algorithmic-error-mitigation core
(C1–C4) reproduces at 18.6× improvement on the paper's own
Fig. 3(a) step triple. Physical-noise portions (C5, C6)
explicitly out of scope.

## Provenance
Wave: QC-100. Replicator: Ollie (subagent). Date: 2026-07-03.
Backfill: 2026-07-06.
