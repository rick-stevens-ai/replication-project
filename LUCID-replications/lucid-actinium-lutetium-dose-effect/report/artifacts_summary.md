# Artifacts summary

## Top-level (preserved from original replication — do NOT modify)
- `REPORT.md` — original narrative report (source of truth for verdict).
- `README.md` — orientation.
- `PROGRESS.md` — chronological log.
- `paper.pdf` — local OA CC-BY copy of Ruigrok et al. 2022.
- `paper.txt` — `pdftotext -layout` extraction (re-pass canonical text source).
- `code/replicate_lucid.py` — single-script central pipeline.
- `code/cN_*.py` — one script per claim (C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C19).
- `results/lu177_dose_survival.csv`, `results/ac225_dose_survival.csv` — fit inputs.
- `results/lu177_dose_pipeline_check.csv`, `results/ac225_dose_pipeline_check.csv` — MIRD offset table.
- `results/summary.json` — machine-readable central-pipeline summary.
- `results/cN_*.json` — one JSON per claim in the re-pass.
- `figures/dose_response_replication.png` — dose-response fit figure.
- `figures/dose_pipeline_check.png` — MIRD offset figure.

## `report/` (backfilled 2026-07-06, this pass)
- `REPORT.tex` — full LaTeX synthesis with honest Critique section; `\input{open_questions_section.tex}` at end.
- `open_questions.json` — bare JSON list of 5 open-question objects
  `{q, basis, next_steps}`.
- `open_questions_section.tex` — LaTeX rendering of the 5 open questions.
- `workflow.md` — step-by-step methods trace for both the initial pass and the re-pass.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest critique of what was NOT done, drift risk, and LUCID-corpus PARTIAL pattern.

## `extraction/` (backfilled 2026-07-06, this pass)
- `nougat.mmd` — stub / provenance note. Marker canonical for this DOI is
  not present on uicgpu as of 2026-06-23; canonical text source for the
  re-pass was `pdftotext -layout paper.pdf paper.txt` at the top level.

## Verdict
**PARTIAL** (Coverage 8/10, Agreement 8/10). Re-tiered 2026-06-25 from
SPOT-CHECK after the 12-claim re-pass produced JSON evidence for every
sub-claim. The tier reflects: reproduced central α/RBE/MIRD scaffolding
+ documented multiplicative offset with identified mechanistic origin +
6 precisely-named wet-lab / MC-input artifacts blocking full REPLICATED.

## Artifact count (this backfill pass)
7 new artifacts written by this backfill; 0 pre-existing artifacts modified or moved.
