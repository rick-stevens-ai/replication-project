# Artifacts Summary — lucid-medras-mc

## Top-level
- `REPORT.md` — canonical narrative report (2026-05-28, Ollie). **Preserved as-is.**
- `PROGRESS.md` — phase log (referenced in original REPORT.md).
- `logs/` — raw run output from the 2026-05-28 execution.
- `results/fidelity_summary.csv` — tidy per-condition table extracted from Fidelity log.
- `figures/` — three publication-ready PNGs:
  - `misrepair_vs_LET.png` (Fig 5 shape reproduction)
  - `repair_kinetics.png` (Fig 2C shape reproduction)
  - `misrepair_vs_dose_xray.png` (Fig 3A shape reproduction)
- `scripts/parse_and_plot.py` — parser + plot generator.
- `artifacts/pide_hunt/` — cached PIDE documentation (NASA THREE overview, GSI page snapshot).

## report/ (this backfill, 2026-07-06)
- `REPORT.tex` — LaTeX version of the report with an explicit **Critique** section
  (what was and was not exercised vs the paper's headline), preserving the
  original 7/7 mechanistic reproduction table and PARTIAL verdict.
- `open_questions.json` — 5 open questions as a bare JSON list.
- `open_questions_section.tex` — LaTeX-formatted 5 open questions,
  \\input from REPORT.tex.
- `workflow.md` — 5-stage execution workflow.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest analysis of the ~65% coverage gap and the
  PARTIAL verdict rationale.

## extraction/ (this backfill)
- `nougat.mmd` — stub for downstream Nougat extraction (not actually run;
  paper text and figures were read directly from Frontiers in Oncology
  open-access HTML).

## What is NOT in this dir (out of scope)
- No Paganetti proton-survival table.
- No PIDE 3.4 ion-survival data (registration wall).
- No Lehmann/Newman dose-rate raw.
- No cell-line-specific alpha/beta fits.
- No survival-curve overlay figures.
- No re-implementation of MEDRAS analytic equations independent of shipped code.

## Verdict artifact
See `../QUEUE.md` (LUCID batch) for the entry: **PARTIAL** (MC backbone
reproduced; headline survival/RBE/dose-rate overlays not reconstructed).
