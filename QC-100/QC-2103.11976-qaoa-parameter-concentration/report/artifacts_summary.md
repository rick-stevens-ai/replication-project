# Artifacts Summary — QC-2103.11976 QAOA Parameter Concentration

## Layout
```
QC-2103.11976-qaoa-parameter-concentration/
├── work/
│   ├── paper.pdf              # arXiv:2103.11976v1 (fetched)
│   └── paper.txt              # pdftotext canonical text
├── extraction/
│   └── nougat.mmd             # stub (see note below)
├── code/
│   ├── qaoa_state_prep.py     # main sweep + Qiskit statevector cross-check
│   └── analyze.py             # folding, fits, concentration exponent
└── report/
    ├── REPORT.md              # narrative report (primary, was pre-existing)
    ├── REPORT.tex             # LaTeX submission version (added 2026-07-06)
    ├── open_questions.json    # 5 truly-open questions with basis + next_steps
    ├── open_questions_section.tex  # LaTeX open-questions section
    ├── workflow.md            # end-to-end pipeline
    ├── artifacts_summary.md   # this file
    ├── failure_analysis.md    # honest critique of the replication
    └── evidence/              # all JSON/CSV/log artefacts (pre-existing)
        ├── p1_sweep.{json,csv}
        ├── p2_sweep.{json,csv}
        ├── qiskit_crosscheck.{json,csv}
        ├── p1_concentration.{json,csv}
        ├── p1_analysis.json
        ├── p1_concentration_fit.json
        ├── p1_large_n.json
        ├── run.log
        ├── analyze.log
        └── large_n.log
```

## Evidence highlights (all measured, none quoted)
| Artifact | What it proves |
|----------|----------------|
| `evidence/qiskit_crosscheck.csv` | Qiskit statevector overlap == paper eq.5 to 10^-16 at n=4,6,8 → C1 |
| `evidence/p1_sweep.csv` | 17 optima (n=4..20) for p=1 → basis for C2, C3, C4 fits |
| `evidence/p2_sweep.csv` | 12 optima (n=4..15) for p=2 → C5 |
| `evidence/p1_large_n.json` | Extended sweep to n=40; β_opt matches π/(n+2) to 6 digits |
| `evidence/p1_analysis.json` | Fit γ = 1.0003π − 2.0023β (paper: γ = π − 2β) → C2 |
| `evidence/p1_concentration_fit.json` | Power-law l ≈ 3.5 in n≤40 window (paper: l=4 asymptotic) → C4 |

## Backfilled artifacts (2026-07-06)
| File | Purpose |
|------|---------|
| `report/REPORT.tex` | LaTeX version of narrative report |
| `report/open_questions.json` | 5 open questions, JSON list format |
| `report/open_questions_section.tex` | LaTeX section for the 5 open questions |
| `report/workflow.md` | End-to-end pipeline for third-party reproduction |
| `report/artifacts_summary.md` | This inventory |
| `report/failure_analysis.md` | Honest critique |
| `extraction/nougat.mmd` | Stub retrieved-text file |

## Note on extraction/nougat.mmd
The paper is a theory paper (arXiv) with clean LaTeX-rendered PDF; the
canonical machine-readable text is already `work/paper.txt` (`pdftotext`
output). A full Nougat OCR pass on a native-LaTeX PDF is redundant. The
stub records this decision and points at the canonical text.

## Provenance
- Replicator: Ollie (OpenClaw subagent, model `argo/argo:claude-opus-4.7`).
- Original run: 2026-07-03.
- Backfill (this pass): 2026-07-06 subagent, model `argo/argo:claude-opus-4.7`.
- No paid endpoints used at any stage.
- No pre-existing files modified in the backfill (only the 7 new files listed above).
