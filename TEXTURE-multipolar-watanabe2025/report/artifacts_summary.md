# Artifacts summary

## Directory layout
```
TEXTURE-multipolar-watanabe2025/
├── paper.pdf                         # arXiv:2507.09237v3
├── extraction/
│   └── marker.md                     # claims, equations, quantitative anchors
├── code/
│   ├── roa_symmetry.py               # Eqs 2,4,5–8: tensor/facet ROA (Claims A/B)
│   ├── roa_tb.py                     # t2g tight-binding H0+Hax (Claim C1)
│   ├── roa_chi_interference.py       # Fig 2/3b: CCχ sign reversal + resonance (Claim C)
│   └── roa_stokes.py                 # Eq 10: θ-parity Stokes/anti-Stokes (Claim D)
├── work/
│   ├── paper.txt                     # extracted text
│   ├── run_all.py                    # master driver
│   ├── results_summary.json          # all numeric results
│   ├── fig_facets.png                # Claim A/B facet ROA bar chart
│   ├── fig_CCchi.png                 # Claim C CCχ(ω) ± t_ax (repro of Fig 3b)
│   └── fig_stokes.png                # Claim D θ-parity discriminator
└── report/
    ├── REPORT.tex / REPORT.pdf       # main report
    ├── open_questions.json           # 5 open questions
    ├── workflow.md                   # how it was run
    ├── artifacts_summary.md          # this file
    └── failure_analysis.md           # what failed / limits
```

## Key result numbers (work/results_summary.json)
| Claim | Quantity | Result | Paper expectation | Verdict |
|---|---|---|---|---|
| A/B | U_CC[1̄11]/U_CC[111] | −1.0000 | −1 (Eq 1, 8) | ✅ exact |
| A/B | I_LR[111] from χ̂⁽¹⁾ only | yes (χ̂⁽²⁾→0) | Eqs 5–6 selection rule | ✅ exact |
| C1 | CCχ(t_ax=0) | 0.000000 | 0 (ROA needs octupolar order) | ✅ exact |
| C1 | CCχ(t_ax=0.1) | −0.520 | nonzero, order-1 | ✅ |
| C | antisymmetry residual CCχ(+t)+CCχ(−t) | 0.0 | 0 (Fig 3b sign reversal) | ✅ exact |
| C | peak |CCχ|, ω_peak | 0.90 @ ω=1.71 | pronounced ω≳1.2, tens of % | ✅ |
| D | θ-even Stokes/anti-Stokes | same sign | symmetric | ✅ |
| D | θ-odd Stokes/anti-Stokes | opposite sign | antisymmetric | ✅ |

## Runtime
- `run_all.py` at Nk=16 ≈ 30 s on CherryRd (single core).
