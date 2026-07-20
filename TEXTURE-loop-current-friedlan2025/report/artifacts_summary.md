# Artifacts summary — arXiv:2510.05234 replication

## Directory tree
```
TEXTURE-loop-current-friedlan2025/
├── paper.pdf                     # arXiv:2510.05234v2 (source)
├── paper.txt                     # pdftotext -layout dump
├── PROVENANCE.md                 # kernel reuse + honest scope
├── extraction/
│   └── marker.md                 # extraction method + pinned equations/constants
├── code/
│   ├── patch_model.py            # 6x6 patch H(k), Eqs 1/4/9/11/12 (adapts shared kernel)
│   └── run_checks.py             # C1-C5 driver
├── work/
│   ├── results.json              # machine-readable claim results
│   └── run.log                   # full run log
└── report/
    ├── REPORT.tex                # main report (+ REPORT.pdf if compiled)
    ├── REPORT.pdf                # compiled (if pdflatex available)
    ├── open_questions.json       # exactly 5, {q, basis, next_steps}
    ├── workflow.md               # reproduce-from-scratch steps
    ├── artifacts_summary.md      # this file
    └── failure_analysis.md       # what didn't reproduce + iteration record
```

## Claim results (from work/results.json)
| ID | Claim | Result |
|----|-------|--------|
| C1 | numeric H(k) == analytic Eq.(9); degeneracy at Phi=0,pi | PASS (err 2.5e-16) |
| C2 | Phi/TRSB/nematic classification; NLCBO unique nematic | PASS |
| C3 | 1/DE1>0, 1/DE2<0 at Delta=0.2 (Eq.12/Fig.5) | PASS (+3.85, -4.39) |
| C4 | LCBO+ lowest at full fill; NLCBO anomalous k_x dispersion | PASS |
| C5 | lambda required: Phi=pi degenerate at lambda=0 | PASS (spread 0 -> 0.04) |

**Total: 5/5 machine-checkable claims reproduced.**

## Verdict
- **REPRODUCED (analytic patch-model core).**
- **Coverage: 6/10** — full analytic model + mechanism; not the mean-field
  simulated-annealing phase diagrams or 9-band DFT tight-binding model.
- **Agreement: 9/10** — every reproduced claim matches to machine precision or to the
  paper's stated qualitative outcome (signs, orderings, degeneracies).

## Key parameters (all from paper, none fitted)
eps=0.12 eV, s1=-1.62, s2=0.5, Delta=0.2 eV, lambda~=0.35 eV*a, k_cut=1.
