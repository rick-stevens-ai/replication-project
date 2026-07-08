# Workflow — QC-2105.01063 pulse-efficient CR replication

## Environment
- macOS 25.3, Python 3.11.15, CPU only.
- Fresh venv `.venv-legacy`.
- Pinned legacy Qiskit (`qiskit-terra==0.22.4`, `qiskit-aer==0.11.2`,
  `numpy<2.0`, `scipy<1.13`) because Qiskit 2.x removed
  `RZXCalibrationBuilder`, `rzx_templates`, and the `pulse` module
  that the paper's methodology depends on.

## Steps
1. `python3.11 -m venv .venv-legacy && source .venv-legacy/bin/activate`
2. `pip install --upgrade pip setuptools wheel`
3. `pip install "qiskit-terra==0.22.4" "qiskit-aer==0.11.2" "numpy<2.0" "scipy<1.13"`
4. `python code/replicate.py`
   - Runs C1 (RZZ 12-point sweep) and C2 (K4 QAOA, 5×5 grid, 8192 shots)
   - Writes `report/evidence/C1_rzz_sweep.json`,
     `report/evidence/C2_qaoa_sweep.json`,
     `report/evidence/summary.json`
   - Prints console summary of headline metrics
5. Wall time: ~7 s total on 2020-era MacBook.

## Determinism
- `seed_transpiler=42`.
- Only stochastic component: 8192-shot sampling in C2 (expected
  fluctuation ~$1/\sqrt{N}\approx 0.011$, well below the 0.1–0.5
  signal reported).

## Files produced
- `report/REPORT.md` — narrative report (pre-existing).
- `report/REPORT.tex` — LaTeX version with critique + open questions.
- `report/evidence/*.json` — machine-readable per-θ and per-(γ,β)
  tables.
- `report/open_questions.json` + `open_questions_section.tex` — 5
  follow-up questions with concrete next steps.
- `report/workflow.md` (this file).
- `report/artifacts_summary.md` — index of artifacts.
- `report/failure_analysis.md` — honest scope / what was not tested.
- `extraction/nougat.mmd` — extraction stub (paper text not
  re-extracted for backfill; see file).

## Backfill notes (2026-07-06)
- Backfill adds LaTeX report, open-questions JSON+TeX, workflow doc,
  artifacts summary, failure analysis, and nougat stub. Does NOT
  re-run any simulation. Original REPORT.md and evidence JSONs are
  preserved untouched.
