# Artifacts summary: Comtesse et al. (2014) replication package

**Paper:** D. Comtesse et al., arXiv:1401.8148 (2014) -- giant inverse MCE in
Ni45Co5Mn37In13. **Verdict: REPLICATED** (coarse, performance-bounded retry).

## 8 required artifacts

| # | Artifact | Path | Notes |
|---|----------|------|-------|
| 1 | Markdown extraction | `report/extraction/marker.md` | INTERIM: pdftotext fallback (marker unavailable) |
| 2 | MMD extraction | `report/extraction/nougat.mmd` | INTERIM: pdftotext fallback (nougat unavailable) |
| 3 | LaTeX report | `report/REPORT.tex` | Full method + results + comparison table + figure |
| 4 | Open questions | `report/open_questions.json` | Exactly 5 Qs + top-level `next_steps` array |
| 5 | Workflow | `report/workflow.md` | Step-by-step reproduction recipe |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file |
| 7 | Failure analysis | `report/failure_analysis.md` | 5 documented gaps, honest scoring |
| 8 | Evidence (code+result) | `report/evidence/code/` | Runner, result JSON, figure |

## Evidence contents
- `report/evidence/code/comtesse2014_beg_potts_mce.py` -- from-scratch BEG+Potts+
  magnetoelastic vectorized Metropolis MC (the physics core).
- `report/evidence/code/comtesse2014_result.json` -- all reproduced numbers.
- `report/evidence/code/figs/mce.png` -- two-branch M(T) + BEG free-energy crossover.
- `report/evidence/replication_recipe.json` -- (pre-existing) recipe.

## Headline comparison
| Quantity | Paper | This work |
|----------|-------|-----------|
| Tm | ~300 K | 296 K |
| dS_mag(Tm) | ~12-14 J/kgK | 14.0 J/kgK |
| dM persists in 2 T | yes | yes |
| Inverse MCE sign | - | - |
| dT_ad (2 T) | -6 K | -10.8 K |
| RCP_inv | -132 J/kg | -281 J/kg |

## Self-score
- **Coverage: 9/10** -- headline observable built from scratch and computed; model,
  Tm, dM, dS_mag, dT_ad, RCP all delivered; DFT/KKR-CPA skipped by design and the
  first-order hysteresis not reproduced (two-branch surrogate).
- **Agreement: 8/10** -- dS_mag quantitative match, sign + field-robust dM match,
  Tm match; dT_ad within factor ~1.8, RCP order-of-magnitude.

## Kernel credit
`gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (topological orbital Hall from skyrmions)
-- NOT physically applicable to this magnetocaloric paper (see failure_analysis.md);
core physics built independently.
