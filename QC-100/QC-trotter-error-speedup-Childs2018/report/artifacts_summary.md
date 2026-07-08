# Artifacts Summary — QC-trotter-error-speedup-Childs2018

## Directory layout
```
QC-trotter-error-speedup-Childs2018/
├── code/
│   ├── trotter_error.py           # PF1/PF2/PF4 vs exact, slope fit
│   └── bound_vs_empirical.py      # PF1 analytic commutator bound vs empirical
├── results/
│   ├── trotter_results.json       # r, error(PF1,PF2,PF4), fitted slopes
│   └── bound_vs_empirical.json    # r, empirical, bound, ratio
├── extraction/
│   └── nougat.mmd                 # Nougat extraction stub (see note)
└── report/
    ├── REPORT.md                  # narrative report (source of truth)
    ├── REPORT.tex                 # LaTeX version
    ├── workflow.md                # step-by-step protocol
    ├── artifacts_summary.md       # this file
    ├── failure_analysis.md        # honest critique
    ├── open_questions.json        # 5 open questions (structured)
    └── open_questions_section.tex # LaTeX version of Q1-Q5
```

## Artifact roles

| Artifact | Role | Notes |
|---|---|---|
| `code/trotter_error.py` | Executable | Reproduces Claim A slopes |
| `code/bound_vs_empirical.py` | Executable | Reproduces Claim B ratio |
| `results/trotter_results.json` | Data | Raw error(r) for PF1/PF2/PF4 + fitted slopes |
| `results/bound_vs_empirical.json` | Data | Raw empirical + analytic bound values |
| `report/REPORT.md` | Report | Source of truth; markdown narrative |
| `report/REPORT.tex` | Report | LaTeX with `\input{open_questions_section.tex}` |
| `report/workflow.md` | Method | Step-by-step protocol |
| `report/artifacts_summary.md` | Manifest | This file |
| `report/failure_analysis.md` | Critique | Honest gap analysis |
| `report/open_questions.json` | Follow-ups | 5 structured open questions |
| `report/open_questions_section.tex` | Follow-ups | LaTeX rendering |
| `extraction/nougat.mmd` | Extraction | Stub — Nougat not executed on this paper (see file) |

## Headline numbers (single line)
Fitted slopes -0.967 / -1.977 / -4.197 vs theoretical -1 / -2 / -4;
per-doubling error factors ~2x / ~4x / ~16x (PF1 / PF2 / PF4);
bound/empirical ratio ~4x asymptotic for PF1.

## Reproducibility
- Deterministic: seed 20260702 for random-field Heisenberg.
- Runtime: < 5 s on any laptop.
- Dependencies: `numpy`, `scipy` only. Zero paid endpoints (Argo judge is free).

## Verdict
Queue verdict: **REPLICATED** for the scaling-law and bound-gap components
(Claims A, B). The paper's headline resource-estimation output is
**NOT** reproduced. See `failure_analysis.md` for the honest framing.
