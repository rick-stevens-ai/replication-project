# Artifacts Summary — W1 qDRIFT Random Compiler

## Top level
- `REPORT.md` — original Markdown replication report (Ollie, 2026-06-26).
  Left in place; the LaTeX version under `report/REPORT.tex` supersedes it
  for citation but does not replace it.

## report/ (added 2026-07-06 backfill)
- `REPORT.tex` — LaTeX replication report with explicit honest Critique
  section and `\input{open_questions_section.tex}` at the end.
- `open_questions.json` — bare JSON list of 5 open-question objects,
  each with `q`, `basis`, `next_steps` (no LaTeX escapes inside string
  bodies; JSON-parseable).
- `open_questions_section.tex` — the 5 questions rendered for LaTeX
  inclusion, matching `open_questions.json` in substance.
- `workflow.md` — end-to-end workflow trace (paper → env → reimpl →
  sweeps → analysis → write-up → verdict).
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest catalog of what was NOT reproduced (in
  addition to what is embedded in the Critique section of REPORT.tex).

## extraction/
- `nougat.mmd` — stub placeholder for the mathpix/nougat markdown-math
  extraction of arXiv:1811.08017. The actual replication drew equations
  from the arXiv LaTeX source directly (transcribed by hand into the
  simulator), so this file is a placeholder rather than a live extraction.

## Run artifacts (from the original 2026-06-26 execution)
The following are referenced by REPORT.md and are expected to live in the
run directory alongside `REPORT.md`; they were produced by
`replicate.py --seed 20260626` and are not regenerated during backfill:

- `replicate.py` — clean-room qDRIFT + Trotter-1 + exact-U driver.
- `results.json` — full sweep results (L-sweep, N-sweep, Trotter sweep).
- `results.csv` — same, flattened.
- `error_vs_gates.png` — log-log plot of measured error vs N for each L,
  with the 2 lambda^2 t^2 / N bound overlaid.
- `run.log` — stdout of the sweep run.

## Absent by design (not part of this replication)
- No molecular Hamiltonian coefficient files (paper's chemistry resource
  estimates were not reproduced; see failure_analysis.md).
- No Suzuki-Trotter-2 / Trotter-4 comparison code (only Trotter-1 was
  implemented; see failure_analysis.md).
- No noisy-channel simulator (open item #4).
- No SDP-based diamond-norm computation (open item raised in Critique).
