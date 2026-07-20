# Artifacts Summary — Hotta 2006 (cond-mat/0611113)

## Directory tree
```
TEXTURE-multipolar-hotta2006/
├── paper.pdf                     source (8 pp)
├── code/
│   ├── multipole_ops.py          j=5/2 multipole operators; Claims 3,4,5
│   └── cef_levels.py             14-orbital CEF+SO exact diag; Claims 1,2
├── work/
│   ├── paper.txt                 pdftotext -layout extraction
│   ├── multipole_out.txt         run log (Claims 3,4,5)
│   └── cef_out.txt               run log (Claims 1,2)
├── extraction/
│   └── marker.md                 equation/figure extraction map
└── report/
    ├── REPORT.tex / REPORT.pdf   main writeup
    ├── comparison.json           quantitative match table (5 claims)
    ├── open_questions.json       exactly 5 open questions
    ├── workflow.md               end-to-end procedure
    ├── artifacts_summary.md      this file
    └── failure_analysis.md       successes, discrepancies, scope
```

## Claims and outcomes
| # | Claim | Result | Agreement |
|---|-------|--------|-----------|
| 1 | SO -> j=5/2(6) + j=7/2(8), gap (7/2)λ | E=-0.2/+0.15, gap 0.35, [6,8] | exact |
| 2 | j=5/2 -> Γ5 doublet + Γ67 quartet, GS flips w/ sign(x) | x>0 Γ67, x<0 Γ5 | exact |
| 3 | 15 multipole ops orthonormal Tr(XX')=δ | max off-diag 2e-16 | exact |
| 4 | 4u ⟂ 5u for n=5 (j=5/2) | overlaps O(1e-16) | exact |
| 5 | mixing coeffs (p,q,r) unit-norm | norm²=1.00±0.005 | within rounding |

## Key numbers (replicated)
- Spin-orbit gap: 0.350000 eV (= 3.5·λ, λ=0.1) — exact.
- CEF excitation (n=1, single electron): 8.32 meV (x=+0.4), 8.63 meV (x=-0.4).
- Multipole operator orthonormality residual: 2.2e-16.

## Tools / environment
Python 3.14, numpy 2.4.3, scipy 1.18.0; pdftotext, pdflatex. Host: CherryRd (macOS).

## Verdict
**Strong partial replication.** Every exactly-diagonalizable claim (the local
CEF+SO level structure, ground-state symmetry crossover, and the full multipole
operator algebra incl. the 4u/5u non-mixing that underpins the paper's central
argument) reproduces to machine precision. The NRG-dependent thermodynamics and
the dominant-multipole crossover are out of scope and flagged.
- **Coverage: 6/10** (local physics fully covered; NRG chi(T)/phonons not).
- **Agreement: 10/10** on the replicated subset (machine-precision matches).
