# Artifacts summary — jiang2023 (arXiv:2311.09290v2)

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Extraction (marker) | `extraction/marker.md` | Interim pdftotext extraction + header |
| 2 | Extraction (nougat) | `extraction/nougat.mmd` | Interim pdftotext extraction + header |
| 3 | Report | `report/REPORT.tex` | RevTeX replication write-up |
| 4 | Open questions | `report/open_questions.json` | 5 Qs + next_steps |
| 5 | Workflow | `report/workflow.md` | Pipeline log |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Scope limits + judge |
| 8 | Evidence | `report/evidence/` | recipe + result JSON + code copy |

## Evidence directory
- `replication_recipe.json` — method + testable headline.
- `jiang2023_result.json` — numeric results (all matches, overall reproduced).
- `replicate_jiang2023.py` — copy of physics runner.

## Result highlights
- s-orbital kagome flat band at E=+2.0 (=2t): **match**.
- BCL counting theorem, 4 configs incl. paper's 3+2 (Nd2=3, Np=2 → 1 flat): **all match**.
- Intra-sublattice A=µI → 1 flat band at E=0.7=µ: **match**.
- `overall_headline_reproduced: true`; runtime 0.03 s.
