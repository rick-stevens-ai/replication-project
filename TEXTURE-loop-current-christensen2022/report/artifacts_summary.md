# Artifacts summary — christensen2022

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Marker extraction | `extraction/marker.md` | pdftotext interim + header/title/abstract |
| 2 | Nougat extraction | `extraction/nougat.mmd` | pdftotext fallback (.mmd), full text |
| 3 | Report | `report/REPORT.tex` | Full LaTeX writeup: model, method, results, verdict |
| 4 | Open questions | `report/open_questions.json` | 5 questions {question, why_it_matters, next_step} + next_steps |
| 5 | Workflow | `report/workflow.md` | Reproducible step-by-step procedure |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | What was skipped, limitations, honest gaps |
| 8 | Evidence | `report/evidence/` | result JSON + runner code + kernel + recipe |

## Evidence contents
- `christensen2022_result.json` — minimization output (both scenarios, counts, deep-cool minima, TRS check, pure-iCDW test)
- `christensen2022_landau.py` — from-scratch free-energy minimizer
- `loop_current_meanfield_kernel.py` — shared kernel (credited)
- `replication_recipe.json` — original recipe

## Verdict
**REPLICATED** (Landau-theory core). Coverage 7/10, Agreement 9/10.

## Key result
Two generic mixed iCDW-rCDW phases confirmed as global free-energy minima:
- **3Q-3Q**: N=(−0.89,−0.89,−0.89), Φ=(0.91,0.91,0.91) — C3-preserving, magnetic.
- **2Q-1Q**: N=(0,0,−1.41), Φ=(1.01,1.01,0) — C3-breaking, orthorhombic.
Pure iCDW is never a stand-alone minimum (requires rCDW), exactly per the paper.
