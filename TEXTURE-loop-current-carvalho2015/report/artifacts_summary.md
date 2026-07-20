# Artifacts summary — arXiv:1506.07172 replication

## Directory contents

```
paper.pdf                     source paper (pre-fetched)
paper.txt                     pdftotext -layout extraction (1245 lines)
extraction/marker.md          extraction + misclassification flag + 5 claims + params
code/
  hotspot_mft.py              exact 24x24 Appendix-A linearized-hot-spot G^-1
                              (documents Gamma-matrix structure; independent-gap version)
  hotspot_competition.py      faithful minimal COMPETITION model (main engine)
  run_sweeps.py               Fig. 4 sweeps + checks + plots
work/
  results.json                all sweep data + correlation checks + ratio + M_LC
  sweep_Vpd.csv               R_II, b vs V_pd (lambda=20)
  sweep_lam.csv               R_II, b vs lambda (V_pd=14)
  fig4_replication.png        two-panel reproduction of paper Fig. 4
report/
  REPORT.tex / REPORT.pdf     writeup
  workflow.md                 step-by-step method
  artifacts_summary.md        this file
  failure_analysis.md         what broke, why, and the fixes
  open_questions.json         5 open questions
```

## Key numbers (nk=96 hot-spot mesh)

| Quantity | This work | Paper | Verdict |
|---|---|---|---|
| corr(R_II, V_pd) | +0.997 | R_II grows with V_pd (Fig 4a) | ✓ |
| corr(b, V_pd) | −0.853 | b vanishes as V_pd grows (Fig 4a) | ✓ |
| corr(b, λ) | +0.853 | b grows with λ (Fig 4b) | ✓ |
| corr(R_II, λ) | −0.836 | R_II suppressed by large λ (Fig 4b) | ✓ |
| R_II^c / V_pd^c | 0.171 | ≈ 0.2 | ✓ (~15%) |
| M_LC | 0.162 μB | 0.19 μB | ✓ (qualitative) |

All 5 selected claims reproduced. The mutual-detriment (competition) between the
ΘII-loop-current order and the QDW order — the paper's central result — is
recovered from first principles (anticommuting hot-spot gaps) and is robust to
the hot-spot cutoff (Λ = 0.6–1.5 all give R_II↑, b↓ with V_pd).

## Honesty notes
- Absolute magnitudes of R_II and b are calibration-dependent (the full
  Appendix-B/C D_l^(m) closed forms are not in the extracted text). The
  *trends*, *signs*, *ratio*, and *competition* are calibration-independent and
  are what the paper actually claims physically.
- M_LC is an order-of-magnitude estimate via the paper's own stated linear map
  (M_LC ∝ R_II^c/V_pd^c), not an independent first-principles moment calc.
