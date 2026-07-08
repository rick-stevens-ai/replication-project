# Artifacts Summary — QC-1909.05074 QNG-for-VQE Replication

## Location
`~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1909.05074-natural-gradient-vqe/`

## Directory layout
```
QC-1909.05074-natural-gradient-vqe/
├── code/
│   └── vqe_h2_natgrad.py         # replication script (statevector, PennyLane)
├── extraction/
│   └── nougat.mmd                # extracted paper text (stub — MathPix/nougat)
├── logs/
│   └── run.log                   # stdout+stderr from `python code/vqe_h2_natgrad.py`
├── report/
│   ├── REPORT.md                 # authoritative narrative report (2026-07-03)
│   ├── REPORT.tex                # LaTeX version with critique + open questions
│   ├── open_questions.json       # 5 open questions, bare JSON list
│   ├── open_questions_section.tex # LaTeX open-questions section (input by REPORT.tex)
│   ├── workflow.md               # step-by-step workflow used
│   ├── artifacts_summary.md      # this file
│   ├── failure_analysis.md       # honest critique of what wasn't done
│   └── evidence/
│       ├── vqe_h2_natgrad.py     # duplicate of code/ script
│       ├── results.json          # machine-readable summary (final energies, iter counts)
│       ├── energy_curves.csv     # per-iteration E_vanilla, E_qng (200 rows)
│       ├── params_vanilla.csv    # per-iteration θ trajectory (vanilla GD)
│       ├── params_qng.csv        # per-iteration θ trajectory (QNG)
│       └── energy_vs_iteration.png  # reproduction of Fig. 5 (bottom)
└── .venv/                        # local venv (Python 3.14 + PennyLane 0.45.1)
```

## Artifact inventory (8 core artifacts)

| # | Artifact | Path | Purpose |
|---|----------|------|---------|
| 1 | Narrative report (MD) | `report/REPORT.md` | Authoritative human-readable replication narrative |
| 2 | Narrative report (LaTeX) | `report/REPORT.tex` | LaTeX version with critique section + open questions input |
| 3 | Open questions (JSON) | `report/open_questions.json` | 5 truly-open questions with concrete next steps |
| 4 | Open questions (LaTeX) | `report/open_questions_section.tex` | Rendered in REPORT.tex via \input |
| 5 | Workflow doc | `report/workflow.md` | Step-by-step reproducibility protocol |
| 6 | Artifacts summary | `report/artifacts_summary.md` | This file — what exists where |
| 7 | Failure analysis | `report/failure_analysis.md` | Honest critique of what wasn't tested |
| 8 | Paper extraction | `extraction/nougat.mmd` | Extracted paper text (stub / placeholder) |

Plus supporting evidence:
- `code/vqe_h2_natgrad.py` — the replication script
- `report/evidence/*.csv, *.json, *.png` — machine-readable results and reproduced figure
- `logs/run.log` — run log

## Headline result (from REPORT.md)
QNG reaches |E − E_exact| < 1e-4 in 44 iterations; vanilla GD requires 77. Speedup 1.75× at that tolerance. Both converge to h₄ = −0.82462 (paper quotes −0.82). Verdict: **REPLICATED** on the headline claim (C3).

## What was NOT done
See `report/failure_analysis.md` for the full honest critique. Highlights:
- No independent hand-implementation of the metric tensor (relied on PennyLane's `QNGOptimizer`)
- Convention/scaling discrepancy in metric-tensor helper not analytically resolved
- Cost accounting in iterations only, not in quantum-circuit-execution count
- Deep-ansatz behavior untested
- Paper's own negative results (Fig. 6, Fig. 7) not exercised
- Shot-noise / hardware-noise regime untested
