# Artifacts Summary — TEXTURE-orbital-gmitra2013

Paper: Gmitra et al., PRL 111, 036603 (2013), arXiv:1303.2510.
Texture class: orbital. Method class: first-principles DFT (Fe/GaAs slabs).

## 8-Artifact Bar

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Paper source | `paper.pdf`, `extraction/marker.md` | present |
| 2 | Method extract | `report/method_extract.md` | present (pre-existing) |
| 3 | Code (model) | `code/sof_model.py`, `code/run_analysis.py` | written, runs |
| 4 | Work run | `work/` (scripts + execution) | executed |
| 5 | Results | `results/metrics.json` | 6/6 claims PASS |
| 6 | Figures | `figs/fig2_sof_butterflies.png`, `figs/fig2_polar_wk.png`, `figs/fig3_soc_vs_theta.png` | generated |
| 7 | Report | `report/REPORT.tex` | written (section-by-section) |
| 8 | Meta artifacts | `report/open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md` | written |

## Machine-checkable claims (results/metrics.json)

| ID | Claim | Result |
|----|-------|--------|
| C1 | Symmetry extraction Eqs.(4-9) round-trips alpha,beta,w_xy exactly | PASS (err <1e-6) |
| C2 | alpha_1(theta) changes sign (magnetic control) | PASS ([-6.68,+5.84] meV.A) |
| C3 | alpha_1*beta_1 flips sign [1-10]->[110]; band 2 does not | PASS (+46.8 -> -91.3; band2 +2419 -> +2502) |
| C4 | linear-in-k regime + anisotropic butterfly | PASS (|w|/k const; max/min 42.6 vs 2.19) |
| C5 | pure cos(2theta) C2v; band1 >> band2 sensitivity | PASS (|B/A| 14.9 vs 0.043) |

## What is reproduced vs not

**Reproduced (analytic core):** C2v Hamiltonian, alpha/beta angular
parametrization, symmetry extraction method (Eqs. 4-9), Fig. 2 butterflies,
Fig. 3 structure, and every qualitative magnetic-control claim.

**Not reproduced (out of scope, marked):** relativistic FLAPW DFT band
structure of the Fe/GaAs slab; independent computation of Table I coefficients;
electric-field sweep beyond the given points; out-of-plane <s>/Delta_xc maps.

## Verdict
Partial-to-strong replication of the paper's symmetry framework.
**Coverage: 6/10. Agreement: 9/10.**
