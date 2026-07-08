# Artifacts summary — arXiv:2305.04954 replication

**Set:** QC-100
**Dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2305.04954-xeb-phase-transition/`
**Verdict:** REPLICATED (finite-size, qualitative)

## Directory layout

```
QC-2305.04954-xeb-phase-transition/
├── paper/
│   ├── 2305.04954.pdf                  # arXiv PDF (fetched 2026-07-03)
│   └── 2305.04954.txt                  # pdftotext output
├── extraction/
│   └── nougat.mmd                      # stub (see file)
├── code/
│   ├── xeb_replication.py              # main simulation (~326.6 s wall)
│   └── plot_results.py                 # matplotlib plotting
├── results/
│   ├── xeb_sweep.json                  # raw numeric outputs (N x epsilon grid)
│   ├── fig_F_and_chi_vs_epsN.png       # F, chi, chi/F vs epsilonN
│   └── fig_log_chi_vs_epsN.png         # log-scale, showing slope change
├── notes/                              # scratch notes (pre-existing)
├── venv/                               # Python 3.12.13 venv (pre-existing)
└── report/
    ├── REPORT.md                       # canonical prose report
    ├── REPORT.tex                      # LaTeX version (this backfill)
    ├── open_questions.json             # 5 open questions, machine-readable
    ├── open_questions_section.tex      # LaTeX rendering, \input into REPORT.tex
    ├── workflow.md                     # reproducible workflow
    ├── artifacts_summary.md            # this file
    ├── failure_analysis.md             # honest critique / limits
    ├── fig_F_and_chi_vs_epsN.png       # figure copy
    ├── fig_log_chi_vs_epsN.png         # figure copy
    └── evidence/                       # sim code + JSON copies
```

## Artifact roll-call (8-artifact standard)

| # | Artifact | Path | Status |
|---|---|---|---|
| 1 | Paper PDF | `paper/2305.04954.pdf` | Present |
| 2 | Simulation code | `code/xeb_replication.py`, `code/plot_results.py` | Present |
| 3 | Raw numeric results | `results/xeb_sweep.json` | Present |
| 4 | Figures | `results/fig_*.png` + `report/fig_*.png` copies | Present |
| 5 | Prose report | `report/REPORT.md` (canonical) + `report/REPORT.tex` | Present |
| 6 | Reproducible workflow | `report/workflow.md` | Present (this backfill) |
| 7 | Open-questions JSON + LaTeX | `report/open_questions.json`, `report/open_questions_section.tex` | Present (this backfill) |
| 8 | Honest failure analysis | `report/failure_analysis.md` | Present (this backfill) |

## Provenance

- **Simulation:** exact Cirq statevector / density-matrix, 1D brickwork, N in {4,6,8,10},
  d=8, epsilon sweep with 11 points crossing epsilonN = ln(5/2). Wall time 326.6 s
  on CherryRd, 2026-07-03.
- **No LLM inference used in physics pipeline.** Free endpoints only for report
  authoring / backfill.
- **All numeric rows in report** were regenerated from `results/xeb_sweep.json`; no
  filled-in cells.

## Headline exercised

The paper's central qualitative claim (XEB tracks F below a critical epsilonN, then breaks
away sharply above) is reproduced on real Cirq simulation: chi/F grows from ~1 to ~20 as
epsilonN crosses the theoretical Haar all-to-all threshold ln(5/2) ~ 0.916 at N=10, d=8.
The paper's Fig.~2c quantitative asymptote (-0.92/layer at N=40) is not fully reproduced;
this is a stated instance-size limit of CPU statevector, not a contradiction.
