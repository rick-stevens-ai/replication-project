# Artifacts Summary — LUCID Slot 040

Every file in this replication directory, with purpose and provenance.

## `report/` (primary deliverable)
- **REPORT.md** — Original human-readable report (2026-06-22).
  Verdict, claim-by-claim table, bug discovery, reproducibility blockers.
- **REPORT.tex** — LaTeX equivalent with explicit critique section
  (backfill 2026-07-05).
- **open_questions.json** — 5 truly-open questions in structured JSON
  (bare list of {q, basis, next_steps}).
- **open_questions_section.tex** — Same 5 questions in LaTeX prose.
- **workflow.md** — What was actually executed and how to re-run.
- **artifacts_summary.md** — This file (pointer index).
- **failure_analysis.md** — Honest critique of paper AND this replication.

## `code/`
- **reproduce_damage_model.py** — Single Python file, ~200 LOC, stdlib +
  numpy + matplotlib. Reproduces every analytically tractable claim in
  the paper. Runs in < 2 s on one CPU core. No GPU, no network, no MC.

## `evidence/`
- **numbers.json** — Machine-readable dump of every reproduced quantity
  (bead radii, Morse+LJ per-bond, McMahon residual, back-fit μ/φ,
  Eq. 8 cross-check).
- **log.txt** — Human-readable execution log with intermediate values
  and paper-vs-reproduction deltas.

## `figures/`
- **cg_potentials.png** — Morse + LJ curves for all five bond types
  (P-OP1, P=OP2, P-O5', OP1-OP2, OP1-O5', OP2-O5').
- **mcmahon_fits.png** — SC(D), OC(D), L(D) curves for ⁶⁰Co γ and
  1-MeV e⁻ with recovered μ, φ.
- **table3_threshold_ranges.png** — Bar plot of prior-work threshold
  ranges (5-37.5 eV) with this work's values (12.4 and 30.5 eV)
  marked as inclusion checks.

## `ocr/`
- **raw_layout.txt** — pdftotext -layout extraction of the source PDF.
  Used as text source for the analytical reproduction. (Nougat not run
  this session; born-digital PDF, pdftotext sufficient.)

## `extraction/`
- **nougat.mmd** — Stub file. Nougat OCR not applicable here (see
  file for rationale).

## Files intentionally NOT present
- No Geant4-DNA source code (blocker #1, not released).
- No CG geometry file / DNAFabric format (blocker #1).
- No SSB/DSB clustering algorithm (blocker #1).
- No Supplementary Fig. S1 / S2 figures (blocker #2, not retrieved).
- No wet-lab gel-band CSV (blocker #3, not released).
- No G4EmDNAPhysics_option2 macro cards (blocker #5).
- No `runs/` directory — no simulations were run.

## Re-run
```bash
python3 code/reproduce_damage_model.py
```
Regenerates `evidence/` and `figures/` from scratch in < 2 s.
