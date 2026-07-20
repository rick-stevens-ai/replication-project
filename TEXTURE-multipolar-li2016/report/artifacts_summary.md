# Artifacts Summary — li2016

**Paper:** Li, Wang & Chen, "Hidden multipolar orders of dipole-octupole doublets
on a triangular lattice", arXiv:1608.07008 (2016).
**Verdict:** REPLICATED | **Coverage:** 9/10 | **Agreement:** 9/10

## Artifacts (8)
| # | Path | Description |
|---|------|-------------|
| 1 | `extraction/marker.md` | Interim marker-style extraction (pdftotext fallback) + metadata, equations, claims |
| 2 | `extraction/nougat.mmd` | Interim nougat-style .mmd with LaTeX-restored equations |
| 3 | `report/REPORT.tex` | Full replication report (model, method, results table, verdict) |
| 4 | `report/open_questions.json` | 5 open questions {question, why_it_matters, next_step} + next_steps |
| 5 | `report/workflow.md` | Step-by-step workflow, provenance, compute, key results |
| 6 | `report/artifacts_summary.md` | This file |
| 7 | `report/failure_analysis.md` | Limits, gaps, honest failure/scope analysis |
| 8 | `report/evidence/` | `li2016_result.json`, `li2016_replication.py`, `ollie_multipolar_stevens_landau_kernel.py`, `replication_recipe.json` |

## Headline claim & outcome
> "For the FO state at (Jx,Jy,Jz)=(-1,-0.2,-0.5), theta=pi/3, the mean-field
> transition occurs at To=1.5|Jx|, with no divergent magnetic susceptibility
> despite time-reversal-breaking octupolar order."

**All 4 sub-claims reproduced independently:**
1. Ground state ferro-octupolar (uniform Tx, S=(0.5,0,0)) ✓
2. To = 1.5|Jx| (exact) ✓
3. chi_zz finite (max 2.5), no divergence ✓
4. Octupolar wave gapped (min gap 1.90) ✓

## Provenance
Kernel `ollie_multipolar_stevens_landau_kernel.py` reused (pseudospin operators,
fluctuation susceptibility, Landau Tc). Credited in code header and REPORT.tex.
