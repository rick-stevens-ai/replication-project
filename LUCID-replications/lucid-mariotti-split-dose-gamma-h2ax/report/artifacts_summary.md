# Artifacts summary — Mariotti 2013 split-dose γ-H2AX

Paper: Mariotti et al. 2013, PLoS ONE 8(11):e79541. DOI 10.1371/journal.pone.0079541.
Verdict: **REPLICATED** (coverage 9/11, agreement 8/11). One PARTIAL condition
(20-min-gap Table-S1 anomaly) documented.

## 8-artifact standard status
| # | Artifact | File | Status |
|---|---|---|---|
| 1 | Original PDF | on-disk paper source (CC-BY) | present |
| 2 | Marker text | canonical Marker parse (UICGPU 2026-06-22) + `PARSER_PROVENANCE.md` | present |
| 3 | Nougat text | `extraction/nougat.mmd` | **stub** — no GPU parse; sha256 pointer |
| 4 | LaTeX report | `report/REPORT.tex` (+ `open_questions_section.tex`) | present |
| 5 | Open questions | `report/open_questions.json` (5 × q/basis/next_steps) + `## Open Questions` | present |
| 6 | Workflow | `report/workflow.md` | present |
| 7 | Artifacts summary | this file | present |
| 8 | Failure analysis | `report/failure_analysis.md` | present |

## Headline results (traces)
- Single-acute: 1 Gy peak 21.82 vs 21; 2 Gy peak 37.15 vs 37.
- T-1: 20.1 foci/cell/Gy vs paper ~25 (19.6% rel err) — PASS.
- T-2: 12-h gap peaks 21.82 vs 20.72 (5.0% diff) — PASS.
- T-3: 24-h residual 10.6% (1 Gy) / 15.7% (2 Gy) of peak — PASS.
- T-4: all 5 split-dose B < β=8.011 — PASS.
- T-5: slower decay for 3/4 short gaps — PASS (majority).
- T-6: 20-min single-peak shape OK but height 62.97 vs ~30 — PARTIAL.
- T-7: two peaks at 1/2/5/12 h (4/4) — PASS.
- T-8: net-2nd-foci < single-acute for 4/5 gaps (20-min overshoots) — PASS.
- Full numbers: `results/pass2_claims.json`; Fig-4: `figures/fig4_reproduction.png`.

## Preserved originals (untouched this pass)
REPORT.md, REPORT.pass1.md, PROGRESS.md, README.md, PARSER_PROVENANCE.md,
code/, data/, results/, figures/, extraction/.

## Friction / gaps
Raw foci-count CSV not distributed (blocks direct data confrontation); no 30-kVp or
Fig-8 fit parameters in Table S1 (cross-quality/adaptive strands untested); single
20-min Table-S1 anomaly unresolved.
