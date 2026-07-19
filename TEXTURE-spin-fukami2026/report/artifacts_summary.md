# Artifacts summary — TEXTURE-spin-fukami2026

Paper: Fukami/Sato et al., arXiv:2605.18009 —
"Multi-rotational switching in a noncollinear antiferromagnet by spin-orbit torque".
Replication scope: THEORY dynamical-model only (reduced stochastic LLG for the
noncollinear-AFM order parameter). Not fabrication/measurement.

## Verdict: REPLICATED (theory-model level) — 3/3 claims matched

| # | Artifact | Path | Notes |
|---|----------|------|-------|
| 1 | Replication code | `code/fukami2026_replication.py` | Euler-Maruyama stochastic LLG; both AFM + conventional control; self-scoring. CPU-only. |
| 2 | Results (incremental) | `work/results.json` | Full curves, probability tables, plateau metrics, claim scorecard, summary/verdict. |
| 3 | Figures | `figs/rotations_vs_j.png`, `figs/threshold_vs_duration.png`, `figs/phi_trace_multirotation.png` | (a) rotation growth; (b/c) plateau vs decline; (trace) multiple 2pi rotations. |
| 4 | Report (LaTeX) | `report/REPORT.tex` | Full write-up with model, method, results, honesty notes. |
| 5 | Report (PDF) | `report/REPORT.pdf` | 5 pages, built with pdflatex. |
| 6 | Open questions | `report/open_questions.json` | 5 questions {q, basis, next_steps}. |
| 7 | Workflow | `report/workflow.md` | Steps, modelling decisions, reproduce instructions. |
| 8 | Failure analysis | `report/failure_analysis.md` | The switch-criterion iterations and why each earlier definition failed. |
| + | Artifacts summary | `report/artifacts_summary.md` | This file. |
| + | Metadata | `META.json` | status=replicated, verdict recorded. |

## Reproduced numbers (key)
- Multi-rotation (claim a): max mean ~28 full turns at j=30; correlation of
  turns vs j above depinning = 0.9995. Depinning j_dep = 6*K6 = 6.
- AFM threshold plateau (claim b): P>=0.5 fractional range 0.60, log-log slope
  -0.14 (near-flat). Above j_dep, P=1 switching at *every* duration tested.
- Conventional contrast (claim c): uniaxial fractional range 1.30, slope -0.26;
  conventional decline is 2.18x steeper than AFM plateau.

## How to regenerate
```
python3 code/fukami2026_replication.py         # ~200 s
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```
