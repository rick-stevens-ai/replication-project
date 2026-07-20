# Artifacts summary — nakazawa2024

| # | Artifact | Path | Description |
|---|----------|------|-------------|
| 1 | Extraction marker | `extraction/marker.md` | Bibliographic header, method note, verbatim headline claim, key params |
| 2 | Nougat markdown | `extraction/nougat.mmd` | Interim (pdftotext + hand-normalized) header, abstract, model & M_orb equations |
| 3 | Report (LaTeX) | `report/REPORT.tex` | Full replication report: model, modern-theory M_orb, results table, verdict |
| 4 | Open questions | `report/open_questions.json` | 5 Qs (question/why_it_matters/next_step) + prioritized next_steps |
| 5 | Workflow | `report/workflow.md` | End-to-end steps from read → build → run → compare → package |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | What matched, what didn't, and why |
| 8 | Evidence bundle | `report/evidence/` | result JSON + replication code + both credited kernels + recipe |

## Evidence bundle contents (`report/evidence/`)
- `nakazawa2024_result.json` — computed R, η-scan, size-scan, headline evaluation.
- `nakazawa2024_replicate.py` — from-scratch physics code.
- `gobel2024_sd_skyrmion_kubo_Lz_kernel.py` — credited (itinerant L_z operator).
- `loop_current_kagome_kernel.py` — credited (kagome loop-current conventions).
- `replication_recipe.json` — original recipe.

## Headline numbers (from result JSON)
- R at 1% impurity, mean over η: **~48.7%** (range 9.5%→82.6% single-imp @ ~0.93%).
- claim_exceeds_50pct: partially (yes for η ≤ 0.01; mean just under 50%).
- claim_R_insensitive_to_eta: **False** (relative spread ~0.61).
- Clean M_orb(η) exponent: **~0.3** (paper: ~3).

## Verdict: PARTIAL
Giant impurity suppression of M_orb (magnitude ~50% at 1%) reproduced from an
independent implementation; η-insensitivity and clean η³ scaling not reproduced.
