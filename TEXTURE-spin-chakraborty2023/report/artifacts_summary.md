# Artifacts Summary: chakraborty2023 replication package

Paper: Chakraborty & Black-Schaffer, *Zero-field finite-momentum and field-induced
superconductivity in altermagnets*, arXiv:2309.14427v2.

Base dir: `/home/stevens/textures-100/corpus/textures-spin-chakraborty2023/`

## The 8 artifacts
| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Marker extraction (interim) | `extraction/marker.md` | pdftotext fallback dump, header `INTERIM: pdftotext fallback` |
| 2 | Nougat extraction (interim) | `extraction/nougat.mmd` | pdftotext fallback dump, header `INTERIM: pdftotext fallback` |
| 3 | Report | `report/REPORT.tex` | Full LaTeX replication report (model, method, results, verdict) |
| 4 | Open questions | `report/open_questions.json` | 5 Qs {question, why_it_matters, next_step} + top-level next_steps |
| 5 | Workflow | `report/workflow.md` | Step-by-step reproduction workflow |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | Gaps, root cause of timeouts, honesty note |
| 8 | Evidence | `report/evidence/` | Result JSON + code copies |

## Evidence contents
- `report/evidence/chakraborty2023_bdg_ff.py` — from-scratch BdG FF solver
- `report/evidence/chakraborty2023_result.json` — retry-mode result (N=24, 5.6 s)
- `report/evidence/chakraborty2023_result_coarse.json` — prior N=96 result (65 s)
- `report/evidence/replication_recipe.json` — extracted recipe

## Headline result
Zero-field d-wave altermagnet: **BCS (Q=0) → FF (Q*=0.24) transition at t_am=0.44**,
matching the paper's reported lower window edge (0.44 ≲ t_am ≲ 0.56).

## Verdict
**PARTIAL** (gap: upper FF-window edge grid-limited). Coverage 7/10, Agreement 7/10.
Runtime 5.6 s (< 3 min budget). No fabricated values.
