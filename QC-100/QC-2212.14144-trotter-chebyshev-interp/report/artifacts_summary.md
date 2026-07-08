# Artifacts summary — QC-2212.14144-trotter-chebyshev-interp

All paths relative to the replication root
`~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2212.14144-trotter-chebyshev-interp/`.

## Source paper
- `paper/2212.14144.pdf` — original PDF (arXiv v4).
- `paper/2212.14144.txt` — text extraction.

## Code (preserved verbatim from initial run)
- `code/find_params.py` — spectrum sweep on TFIM (J, g) — pinned J=1, g=0.3.
- `code/trotter_chebyshev.py` — v1 driver: baseline S_1/S_2/S_4 +
  real Qiskit `QuantumCircuit` sanity check (|Δ|_F = 1.55e-16), first-
  pass Chebyshev interpolation in s.
- `code/trotter_chebyshev_v2.py` — v2 driver (**canonical**):
  interpolation in u = s^2 (reflection-symmetry trick), barycentric
  Lagrange with Salzer weights, cost accounting, head-to-head at
  matched budget. Produces canonical results.

## Numeric evidence
- `report/evidence/results.json` — v1 raw numbers.
- `report/evidence/results_v2.json` — v2 raw numbers (canonical).
- `report/evidence/fig_scaling.png` — two-panel: (left) err vs r/n,
  (right) err vs cost. Reproduces paper Figs 4 & 5 qualitatively.

## Report (top-level)
- `report/REPORT.md` — narrative markdown replication report (preserved).
- `report/REPORT.tex` — LaTeX mirror with explicit Critique section and
  `\input{open_questions_section.tex}` at end.
- `report/workflow.md` — chronological workflow log.
- `report/artifacts_summary.md` — this file.
- `report/failure_analysis.md` — honest critique + what was NOT done.
- `report/open_questions.json` — 5 open questions (bare JSON list).
- `report/open_questions_section.tex` — LaTeX rendering of the same.

## Extraction stub
- `extraction/nougat.mmd` — placeholder for future full-paper Nougat
  extraction (see file for details).

## What backs the verdict
- **REPLICATED verdict** rests on:
  - Real Qiskit unitary matches numpy S_2 to `1.55e-16`.
  - Baseline S_2 log-log slope ≈ −2.0; S_4 ≈ −4.0 (textbook).
  - Cheb+S_2 error decays 9.02e-6 → 1.66e-8 → 2.60e-11 → 3.48e-13 →
    **4.44e-16** for n=2..6 (per-node ratio ~500-1000×, hitting
    double-precision floor at n=6).
  - At cost ≤100 exponentials: Cheb+S_2 (n=4) = 2.60e-11 beats single
    S_2 (r=32, cost 96) = 5.03e-5 by ~2e6×; beats single S_4 = 2.74e-7
    by ~10^4× at comparable cost.

## Headline exercised?
YES. C4 (spectral-convergence-in-n headline of the paper) is
quantitatively reproduced end-to-end on the paper's own Sec-5 testbed
using a real Qiskit circuit backbone. Also C5 (matched-cost
head-to-head win) is reproduced.
