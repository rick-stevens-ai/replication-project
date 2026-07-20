# Artifacts summary — Chen 2022 (pyrochlore AF* state) replication

| # | Artifact | Path | Purpose |
|---|----------|------|---------|
| 1 | Extraction marker | `extraction/marker.md` | pdftotext interim extraction note + headline claim |
| 2 | Nougat mirror | `extraction/nougat.mmd` | header-stamped markdown mirror of full paper text |
| 3 | Report (LaTeX) | `report/REPORT.tex` | model, method, results, comparison, verdict |
| 4 | Open questions | `report/open_questions.json` | 5 questions {question, why_it_matters, next_step} + next_steps |
| 5 | Workflow | `report/workflow.md` | end-to-end replication procedure |
| 6 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 7 | Failure analysis | `report/failure_analysis.md` | gaps, non-fabrication statement, scores |
| 8 | Evidence | `report/evidence/chen2022_result.json`, `report/evidence/chen2022_gmft.py` | result JSON + from-scratch code |

## Physics deliverable
- **Code:** `work/chen2022_gmft.py` (also in evidence) — from-scratch bosonic-spinon gMFT
  on the diamond lattice (numpy only).
- **Result:** `work/chen2022_result.json` (also in evidence).

## Key result
- AF* state stabilized at (t1=0.025, t2=0.02, Jx=1): spinon gap ≈ 0.53 (deconfined),
  gapless U(1) photon, nonzero AAO `<Sz>` proxy.
- Phase sequence U(1) QSL → AF* → fragmented AFM (spinon condensation at t2c≈0.07).
- T^3 specific-heat coefficient large (small photon velocity from small exchange scale).

## Verdict
**PARTIAL** — Coverage 8/10, Agreement 8/10.

## Credit
Geometry/utility patterns adapted from the shared TEXTURES-100
`ollie_multipolar_stevens_landau_kernel`.
