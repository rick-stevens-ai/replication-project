# Artifacts Summary — hong2026

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Marker extraction | `extraction/marker.md` | Interim text extraction (pdftotext -layout fallback + provenance header). |
| 2 | Nougat extraction | `extraction/nougat.mmd` | Interim .mmd extraction (pdftotext body + nougat-format header). |
| 3 | Report (LaTeX) | `report/REPORT.tex` | Full replication write-up: method, results table, verdict, scoring. |
| 4 | Open questions | `report/open_questions.json` | 5 questions {question, why_it_matters, next_step} + next_steps list. |
| 5 | Workflow | `report/workflow.md` | Step-by-step replication procedure + provenance credit. |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file. |
| 7 | Failure analysis | `report/failure_analysis.md` | Bug caught/fixed, scope limits, sensitivity, reproducibility. |
| 8 | Evidence | `report/evidence/` | `hong2026_result.json` (results) + `hong2026_runner.py` (from-scratch code) + `replication_recipe.json`. |

## Headline claim under test
2π-skyrmions have the widest thermal stability window (up to ~600 K); order
sequence solitons → 1π → 2π → 3π → 4π with alternating topological charge parity.

## Result at a glance
- **Verdict: REPLICATED** (mechanism-level).
- Q parity: 1π=−1.0, 2π≈0, 3π=−1.0, 4π≈0 (odd→|Q|1, even→0). ✓
- Stability windows (model K): 1π=917, **2π=1100**, 3π=917, 4π=917 → 2π widest. ✓
- Runtime ~4 s, 64×64 grid, CPU.

## Provenance / credit
- `ollie_tdgl_phasefield_polar_skyrmion_kernel.py` — TDGL phase-field + Langevin noise.
- `ollie_berg_luscher_topological_charge_kernel.py` — Berg-Luscher topological charge.
