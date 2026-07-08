# Artifacts summary — QC-2107.13470

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2107.13470-unifying-benchmarking-qem/`

## Reports & narrative
- `report/REPORT.md` — canonical Markdown replication report (v1,
  written 2026-07-03; original single source of truth for numbers).
- `report/REPORT.tex` — LaTeX-compilable mirror with an explicit
  honest-critique section and appended open-questions section
  (added 2026-07-06 backfill).
- `report/failure_analysis.md` — honest post-hoc critique of what was
  and was not exercised, with named failure modes (added 2026-07-06).
- `report/workflow.md` — chronological workflow narrative
  (added 2026-07-06).
- `report/artifacts_summary.md` — this file (added 2026-07-06).

## Open questions
- `report/open_questions.json` — five open questions with basis + next
  steps, bare JSON list (added 2026-07-06).
- `report/open_questions_section.tex` — the same five questions
  rendered as a LaTeX `\section`, `\input`-ed by `REPORT.tex`
  (added 2026-07-06).

## Evidence (real Mitiq + Aer runs, 2026-07-03)
- `report/evidence/replication_results.json` — single-seed run
  (seed=2, 2q depth-3): raw / ZNE / PEC / CDR estimates and |err|.
- `report/evidence/replication_results_multi_seed.json` — 5-seed
  ensemble (3 non-null instances) with per-seed and mean |err|.
- `report/evidence/pec_shot_budget.json` — PEC estimate + |err| vs.
  `num_samples ∈ {100, 300, 1000, 3000}`.
- `report/evidence/run5.log`, `run_multi.log`, `pec_budget.log` — raw
  stdout of each run.

## Code (reproducible)
- `code/replicate_qem.py` — single-seed pipeline.
- `code/replicate_multi_seed.py` — 5-seed ensemble driver.
- `code/pec_shot_budget.py` — PEC sample-budget sweep.
- `.venv/` — Python 3.12 venv with pinned Mitiq 1.0.0 + Qiskit 2.5.0 +
  qiskit-aer 0.17.2 + Cirq 1.6.1.

## Paper source
- `work/paper.pdf` — arXiv 2107.13470v2 PDF.
- `work/paper.txt` — `pdftotext` extract for claim-mining.
- `extraction/nougat.mmd` — stub placeholder for nougat MMD extraction
  (added 2026-07-06 as scaffolding; nougat not re-run).

## Verdict
`REPLICATED` — headline C1 (data-driven QEM > raw noisy) reproduced
end-to-end on two paper-relevant methods (ZNE, CDR) with a Qiskit
Aer depolarizing noise model; PEC (not a paper method) fails honestly
in this stack; UNITED- and $10^{10}$-shot-specific claims explicitly
out of scope for laptop replication.
