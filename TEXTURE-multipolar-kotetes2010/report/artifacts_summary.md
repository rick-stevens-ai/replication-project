# Artifacts summary — kotetes2010

Paper: *Magnetic-field-induced chiral hidden order in URu2Si2*, Kotetes, Aperis &
Varelogiannis, Philosophical Magazine (2010), arXiv:1002.2719.

| # | Artifact | Path | Contents |
|---|----------|------|----------|
| 1 | Marker extraction | `extraction/marker.md` | Marker-style header + curated physics extraction (model, gap eqs, params, targets). pdftotext interim (neural marker unavailable — disclosed). |
| 2 | Nougat MMD | `extraction/nougat.mmd` | Full-paper interim in MMD form (pdftotext -layout, header-wrapped; no fabricated OCR). |
| 3 | Report (LaTeX) | `report/REPORT.tex` | Full write-up: model, method, results table, assessment, provenance, verdict. |
| 4 | Open questions | `report/open_questions.json` | 5 questions {question, why_it_matters, next_step} + next_steps summary. |
| 5 | Workflow | `report/workflow.md` | Step-by-step reproduction log incl. debugging. |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file. |
| 7 | Failure analysis | `report/failure_analysis.md` | What didn't replicate and why; scoping. |
| 8 | Evidence | `report/evidence/` | `kotetes2010_result.json` (full numerics + comparison + self_score), `kotetes2010_mft.py` (from-scratch solver), `ollie_multipolar_stevens_landau_kernel.py` (credited shared kernel), `replication_recipe.json`. |

## Headline results
- Zero-field driving gap Delta2(0) = **1.87 meV** (paper 1.55; ratio 1.21).
- Ordering temperature T_HO(0) = **20 K** (paper 17.5; ratio 1.14).
- Landau reduction: Delta1(B=0) = **0** (field-induced, matches paper), To(B) ∝ B²
  (field-enhanced Tc, matches paper mechanism).

## Verdict
**PARTIAL** — Coverage 6/10, Agreement 7/10.

## Provenance
Mean-field/Landau scaffolding reused from `ollie_multipolar_stevens_landau_kernel.py`
(TEXTURES-100 shared kernel). Chiral d-SDW physics implemented from paper Appendices A–D.
