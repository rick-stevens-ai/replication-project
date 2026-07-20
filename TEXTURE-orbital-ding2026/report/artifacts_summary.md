# Artifacts summary — Ding et al. 2026 (Fe2Se2Cl altermagnet)

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Marker extraction | `extraction/marker.md` | Header + `pdftotext -layout` interim body |
| 2 | Nougat extraction | `extraction/nougat.mmd` | Header + interim body (nougat not run this pass) |
| 3 | Report (LaTeX) | `report/REPORT.tex` | Full replication write-up (RevTeX, PRB) |
| 4 | Open questions | `report/open_questions.json` | 5 Qs {question, why_it_matters, next_step} + next_steps |
| 5 | Workflow | `report/workflow.md` | Step-by-step method log |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Limitations, gaps, honest scoring |
| 8 | Evidence | `report/evidence/` | `ding2026_result.json` + `code/ding2026_altermagnet_tb.py` |

## Key numbers
- Max near-Fermi spin splitting: **720 meV** (claim 620 meV; ratio 1.16).
- d-wave fit R^2 = **0.998** vs `cos kx - cos ky`.
- Gamma-M diagonal nodes: |dE| < 1e-12 eV (exact).
- C4z sign reversal Gamma-X vs Gamma-Y: **-1** (confirmed).
- Net magnetic moment: **0** (fully compensated).

## Verdict
**PARTIAL** — altermagnet symmetry fully REPLICATED; 620 meV magnitude
order-of-magnitude confirmed (parameter-tunable, not a DFT-level value).

## Credit
Bloch/lattice patterns adapted from `gobel2024_sd_skyrmion_kubo_Lz_kernel.py`
(Nous Research shared kernels).
