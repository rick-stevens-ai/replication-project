# Artifacts summary — wang2026

**Verdict: PARTIAL** (gap: absolute magnitude / DFT-level material specificity)

**Coverage: 7/10** — Built a complete from-scratch physics surrogate covering all
four mechanism-level claims (orbital>>spin, SOC-required, non-perturbative,
T-odd) plus the chi=tau*D structure. Missing: DFT/Wannier material realism, the
mu-scan and angular-dependence figures, absolute units.

**Agreement: 6/10** — Qualitative/scaling agreement is strong and correct in
sign and hierarchy; the orbital/spin ratio has the right sense and >2-orders
character (ours ~6e3 vs paper ~150, same regime but overshooting), and all
sign/scaling laws match. Absolute magnitude deliberately not reproduced.

## Claim-by-claim
| # | Paper claim | Result | Match |
|---|-------------|--------|-------|
| 1 | chi = tau * D (OBD mechanism) | implemented directly | YES |
| 2 | orbital Hall >> spin Hall (~150x) | ratio ~6.0e3 | YES (qual.) |
| 3 | SOC required (D->0 without SOC) | D^(O): -3.6e-16 -> -3.3e-22 at lambda=0 | YES |
| 4 | non-perturbative weak-SOC enhancement | d log|D^(O)|/d log lambda = -1.1 | YES |
| 5 | T-odd, flips with Neel vector | J->-J flips sign of D^(O) | YES |
| 6 | absolute chi_zzyy = -1.3 (h/e)Ohm^-1V^-1 | model units only | NO (out of scope) |

## Files
- `extraction/marker.md` — INTERIM marker placeholder (pdftotext-backed)
- `extraction/nougat.mmd` — INTERIM pdftotext fallback text layer
- `report/REPORT.tex` — REVTeX writeup
- `report/open_questions.json` — 5 questions + next_steps
- `report/workflow.md` — end-to-end workflow
- `report/artifacts_summary.md` — this file
- `report/failure_analysis.md` — gaps & failure modes
- `report/evidence/wang2026_result.json` — result data (copy)
- `report/evidence/wang2026_replication.py` — code (copy)
- `report/evidence/replication_recipe.json` — original recipe

## Credit
Kernel `gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (itinerant L_z + Kubo/velocity
machinery) adapted and generalized to k-space multiband second-order response.
