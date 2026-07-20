# Artifacts Summary — mestral2025

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Marker extraction | `extraction/marker.md` | Header + structured key-facts over pdftotext interim |
| 2 | Nougat mmd | `extraction/nougat.mmd` | Layout-preserving raw text (pdftotext -layout, 962 lines) |
| 3 | Report (LaTeX) | `report/REPORT.tex` | Full replication writeup with equations, results table, verdict |
| 4 | Open questions | `report/open_questions.json` | 5 questions {question, why_it_matters, next_step} + next_steps |
| 5 | Workflow | `report/workflow.md` | Step-by-step replication log |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | What worked / failed / limits |
| 8 | Evidence | `report/evidence/` | result JSON + model code + recipe |

## Evidence contents
- `report/evidence/mestral2025_result.json` — replication result (copy of work JSON)
- `report/evidence/mestral2025_pockels_model.py` — from-scratch physics model
- `report/evidence/replication_recipe.json` — provided recipe

## Headline result
- **r51 (largest clamped Pockels coeff of BTO)** reproduced via 1/ω² soft-mode mode-sum.
- MARE(predicted r51) = 3.68%; r51@0.45% = 695.5 pm/V ∈ experimental 730±150 pm/V.
- **Verdict: PARTIAL** (headline r51 replicated; microscopic ω(off-centering) only qualitative).
- Coverage 7/10, Agreement 8/10.

## Credits
- Reference data: de Mestral et al. 2025 (arXiv:2506.13209).
- gobel2024 skyrmion Kubo kernel: inspected, **not used** (paper has no spin physics).
