# Artifacts Summary — Yang et al. 2022 (Kagome 3Q iCDW loop-current patterns)

**Paper:** Intertwining orbital current order and superconductivity in Kagome metal,
Yang, Kim, Jeong, Kim, Han & Lee — arXiv:2203.07365v2 (SciPost Physics, 2022).
**Verdict:** REPLICATED · **Coverage: 8/10** · **Agreement: 9/10**

## Headline reproduced
For the 4 possible 3Q iCDW (loop/orbital-current) patterns on the kagome lattice,
with up-spin reference `Phi_up=(i,i,i)`:
- `C_up = +1` for all four (confirmed).
- `C_down = (+1, -1, -1, +1)` for cases (i)-(iv) — **matched 4/4** (Table 1).
- Only case (ii) `(-i,-i,-i)` is helical / time-reversal symmetric; case (i) is the
  chiral flux phase; (iii)/(iv) preserve T*I and T*I*M respectively.
The kernel independently confirms |C|=1 and a TRS-breaking gap for the chiral state.

## Artifact inventory
| # | Artifact | Path | Notes |
|---|----------|------|-------|
| 1 | Marker extraction (interim) | `extraction/marker.md` | pdftotext-based interim + header |
| 2 | Nougat extraction (interim) | `extraction/nougat.mmd` | pdftotext-based interim + Mathpix-style header |
| 3 | Main report | `report/REPORT.tex` | LaTeX; model, method, results table, verdict |
| 4 | Open questions | `report/open_questions.json` | 5 Qs {question, why_it_matters, next_step} + next_steps |
| 5 | Workflow | `report/workflow.md` | reproducible steps + command |
| 6 | Artifacts summary | `report/artifacts_summary.md` | this file |
| 7 | Failure analysis | `report/failure_analysis.md` | limitations, honest scope |
| 8 | Evidence | `report/evidence/` | result JSON + runner + kernel copy |

## Result JSON
`work/yang2022_result.json` (+ copy in `report/evidence/`): per-pattern Chern numbers,
gaps, chirality, symmetry-predicted vs paper C_down, match flags, limitations.

## Self-score rationale
- **Coverage 8/10:** headline topological classification fully covered (all 4 patterns,
  both spins, TRS/helical ID); SC order parameters, LG coefficients (u1,u2), and the
  extended-cell edge spectra were out of scope / not recomputed.
- **Agreement 9/10:** 4/4 Chern numbers reproduce Table 1; magnitude |C|=1 and TRS gap
  are direct numerical results; signs of the two balanced configs are symmetry-derived
  (as the paper itself does), docked 1 point for not being independently FHS-signed.

## Kernel credit
`loop_current_kagome_kernel.py` (`KagomeModel`: kagome tight-binding, Peierls flux,
Fukui-Hatsugai-Suzuki Chern) from `shared-kernels-cache`.
