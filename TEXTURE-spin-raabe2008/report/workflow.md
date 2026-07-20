# Workflow — replication of arXiv:0811.0157 (Raabe et al. 2008, β-Ti alloys)

## 1. Ingest
- `pdftotext -layout paper.pdf paper.txt` → 805-line text layer (no OCR needed).
- Read abstract, methods (Eqs. 1-4), and results §3.1-3.4.

## 2. Theme triage
- Confirmed **off-theme** vs the "texture-spin" batch label: paper is biomedical β-Ti
  DFT+experiment alloy design, not textures/spin. Flagged honestly; proceeded because a
  reproducible computational core exists (closed-form thermo + arithmetic data claims).

## 3. Claim selection (machine-checkable)
- **C1** Ideal-mixing configurational entropy Eq.(2) — closed form, exact.
- **C2** Finite-T free energy Eq.(3) drives β-stabilization threshold DOWN with T.
- **C3** Reported experimental Young's-modulus data claims (min alloy, 37% drop, trends).
- **C4** Table-1 wt%↔at% conversions.

## 4. Implementation (`code/`)
- `composition.py` — wt↔at conversion from standard atomic masses; checks all 8 alloys.
- `thermo.py` — Eq.(2) entropy (verifies S(0.5)=kB·ln2), Eq.(3) free energy with a
  labelled analytic *surrogate* for the DFT energy shape (we lack VASP energies), then
  measures the finite-T threshold shift vs the paper's stated anchors.
- `elastic.py` — arithmetic/trend checks + linear fits on the quoted modulus data.

## 5. Execution (`work/`)
- `python3 code/<x>.py | tee work/out_<x>.txt` for all three.
- No network, no paid endpoints; pure numpy on the local Python.

## 6. Compare & verdict
- C1: PASS (entropy exact). C3: PASS (3/3). C4: PASS (rounding-tolerant, 18/20 rows <0.25 at%).
- C2: PARTIAL — entropy math correct; Ti-Mo threshold reproduced (16.6 vs 14 at%),
  Ti-Nb NOT reproduced (79 vs 25 at%) because the surrogate lacks the true DFT energy shape.
  Reported as honest partial, not tuned to fake a match.

## 7. Report (`report/`)
- REPORT.tex (+ compiled PDF via `pdflatex`), open_questions.json (5), artifacts_summary.md,
  failure_analysis.md, this workflow.md; extraction/marker.md.

## Reproduce
```
cd code && python3 composition.py && python3 thermo.py && python3 elastic.py
cd ../report && pdflatex REPORT.tex
```
