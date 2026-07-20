# Artifacts summary — Tazai2022 replication

Paper: Tazai, Yamakawa & Kontani, *"Charge-loop current order and Z3 nematicity
mediated by bond order fluctuations in kagome metals,"* arXiv:2207.08068v4.

## Directory tree
```
TEXTURE-loop-current-tazai2022/
├── paper.pdf                     # source (arXiv v4)
├── paper.txt                     # pdftotext -layout extraction
├── extraction/
│   └── marker.md                 # extraction marker (claims, params, method)
├── code/
│   ├── reused_loop_current_meanfield_kernel.py   # shared kernel (provenance copy)
│   ├── ollie_loop_current_meanfield_kernel.py    # prior-attempt kernel copy
│   └── tazai2022_loop_current_checks.py          # adapted paper-specific checks
├── work/
│   ├── tazai2022_loop_current_checks.py   # runnable checks (source of truth)
│   ├── make_figs.py
│   ├── results.json              # all numeric outputs
│   ├── verification_figures.png  # C1-C4 panels
│   └── gap_scaling.png           # C5 quadrature
└── report/
    ├── REPORT.tex (+ REPORT.pdf if compiled)
    ├── open_questions.json       # exactly 5, schema {q,basis,next_steps}
    ├── workflow.md
    ├── artifacts_summary.md      # this file
    └── failure_analysis.md
```

## 8-artifact bar
1. **REPORT.tex** (+PDF) — report/
2. **open_questions.json** — report/ (exactly 5)
3. **workflow.md** — report/
4. **artifacts_summary.md** — report/ (this)
5. **failure_analysis.md** — report/
6. **extraction/marker.md** — extraction/
7. **code** — code/ + work/ (reused kernel + adapted checks + fig script)
8. **results/figures** — work/results.json + 2 PNGs

## Key results (all from real code, work/results.json)
| Claim | Quantity | Value | Pass |
|-------|----------|-------|------|
| C1 | max\|bond current\| BO / cLC | 0.0 / 0.0476 | YES |
| C2 | up / down triangle loop mean | -0.1075 / +0.1075; net site 6e-16 | YES |
| C3 | sigma_xy at dt^c=0 / dt^c=0.1 | 0.0 / -2.7e-4; flips under TR | YES (qualitative) |
| C4 | chi0 Gamma / M-mean | 0.986 / 1.842 (peak at M) | YES |
| C5 | gap vs 2 sqrt(dtb^2+dtc^2) | rel err 0 (all 6 cases) | YES |

**Reproduced: 5/5 machine-checkable claims** (C3 qualitative only — magnitude and
damping crossover deferred; see failure_analysis.md L1).
