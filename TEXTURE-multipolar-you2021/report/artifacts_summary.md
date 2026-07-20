# Artifacts Summary — You et al. 2021

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Marker extraction | `extraction/marker.md` | Structured Markdown extraction + header (title, claim, params, reproducibility note) |
| 2 | Nougat extraction | `extraction/nougat.mmd` | Math-flavored interim capture (Eq.1, torque terms, Kittel, ST-FMR line-shape) |
| 3 | Report | `report/REPORT.tex` | Full LaTeX replication report (model, results table, verdict, physics summary) |
| 4 | Open questions | `report/open_questions.json` | 5 questions {question, why_it_matters, next_step} + next_steps |
| 5 | Workflow | `report/workflow.md` | Step-by-step method + reproduce commands |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Limits, assumptions, what was NOT reproduced |
| 8 | Evidence | `report/evidence/you2021_result.json`, `report/evidence/you2021_llg.py`, `report/evidence/replication_recipe.json` | Result JSON + simulation code |

## Verdict
**PARTIAL** — core mechanistic theory claim reproduced from scratch via macrospin LLG;
experimental bulk (growth, ST-FMR, MOKE) not reproducible without samples.

- **Coverage: 6/10**
- **Agreement: 8/10**

## Key result
- Case A (σz present, J‖T): deterministic field-free switching; final state set by current
  sign (both init states → same final). Threshold C_crit ≈ 12 (reduced units).
- Case B (σz absent, J⊥T): no deterministic switching; final state tracks initial state.
- Reproduces the paper's [001] (switch) vs [110] (no switch) control (Fig.4c vs 4f).
