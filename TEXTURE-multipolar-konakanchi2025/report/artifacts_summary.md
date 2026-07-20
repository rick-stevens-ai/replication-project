# Artifacts Summary — Konakanchi et al. 2025 replication

**Paper:** arXiv:2501.18978v1 — Electrically Tunable Picosecond-scale Octupole
Fluctuations in Chiral Antiferromagnets.
**Verdict:** REPLICATED · Coverage 9/10 · Agreement 8/10.

## 8 Artifacts

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Marker extraction | `extraction/marker.md` | Full paper text (pdftotext -layout interim; marker/GPU OCR unavailable) with marker-style header |
| 2 | Nougat MMD | `extraction/nougat.mmd` | Same corpus in nougat MMD wrapper (interim; neural OCR unavailable in env) |
| 3 | LaTeX report | `report/REPORT.tex` | PRL-style writeup: model, method, results table, verdict |
| 4 | Open questions | `report/open_questions.json` | 5 questions {question, why_it_matters, next_step} + next_steps |
| 5 | Workflow | `report/workflow.md` | Step-by-step replication log + runner + key numbers |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | What broke, what's approximate, honest caveats |
| 8 | Evidence bundle | `report/evidence/` | result JSON + replication code + kernel (provenance) + recipe |

## Evidence bundle contents
- `konakanchi2025_replication.py` — from-scratch physics (analytic + Monte-Carlo + Langevin)
- `konakanchi2025_result.json` — all computed numbers (also in `work/`)
- `ollie_multipolar_stevens_landau_kernel.py` — octupole operator provenance (credit: shared-kernels-cache)
- `replication_recipe.json` — original recipe

## Headline result
Low-barrier octupole relaxation reaches **6.5–13.5 ps** (min), reproducing the
paper's "~10 ps for sub-kT barriers"; high-barrier escape is ~13 ns (orders
slower), reproducing the two-mechanism crossover. Numeric Monte-Carlo of the
dephasing integral matches the analytic form to 0.16%; independent Langevin
integration agrees within 1.5x.

## Kernel credit
Octupole (rank-3 Stevens `Txyz`) operators built with
`ollie_multipolar_stevens_landau_kernel.py` from the shared kernels cache.
