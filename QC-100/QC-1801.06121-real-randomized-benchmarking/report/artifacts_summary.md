# Artifacts Summary — QC-1801.06121-real-randomized-benchmarking

## Directory layout
```
QC-1801.06121-real-randomized-benchmarking/
├── report/
│   ├── REPORT.md                       (source-of-truth replication report)
│   ├── REPORT.tex                      (LaTeX version with critique section)
│   ├── open_questions.json             (5 open questions, bare JSON list)
│   ├── open_questions_section.tex      (LaTeX rendering of open questions)
│   ├── workflow.md                     (exact reproduction workflow)
│   ├── artifacts_summary.md            (this file)
│   ├── failure_analysis.md             (honest critique)
│   └── evidence/
│       ├── results.json                (raw survival probs + fits)
│       └── rb_curves.png               (decay curves plot)
├── extraction/
│   └── nougat.mmd                      (nougat MMD stub, see notes)
├── src/
│   ├── real_rb.py                      (main experiment)
│   ├── plot_rb.py                      (plotting)
│   └── theory_check.py                 (analytic cross-check)
└── work/
    ├── 1801.06121.pdf                  (paper)
    ├── 1801.06121.txt                  (pdftotext)
    ├── run1.log                        (execution log)
    └── theory_check.log                (analytic cross-check log)
```

## Artifact roster (8-artifact standard)
| # | Artifact                              | Path                                          | Status |
|---|---------------------------------------|-----------------------------------------------|--------|
| 1 | Source-of-truth report                | `report/REPORT.md`                            | pre-existing |
| 2 | LaTeX report                          | `report/REPORT.tex`                           | added (backfill) |
| 3 | Open questions (JSON)                 | `report/open_questions.json`                  | added |
| 4 | Open questions (LaTeX section)        | `report/open_questions_section.tex`           | added |
| 5 | Workflow                              | `report/workflow.md`                          | added |
| 6 | Artifacts summary                     | `report/artifacts_summary.md`                 | added (this file) |
| 7 | Failure / critique analysis           | `report/failure_analysis.md`                  | added |
| 8 | Extraction (nougat MMD)               | `extraction/nougat.mmd`                       | added (stub) |

## Verdict
`REPLICATED` — see `REPORT.md` and `REPORT.tex` §Verdict.

## Evidence provenance
- `report/evidence/results.json` — raw per-length survival probabilities,
  per-sequence samples (mean + SEM), fit parameters $(A, B, f\ \text{or}\ b)$
  with covariances, and analytic predictions. Written by
  `src/real_rb.py`.
- `report/evidence/rb_curves.png` — three RB decay curves overlaid:
  standard Clifford RB ($M=30$), real Clifford RB ($M=30$), real Clifford
  RB reduced ($M=10$). Written by `src/plot_rb.py`.
- `work/run1.log`, `work/theory_check.log` — captured stdout of the two
  runs.

## Cost
- Local CPU only. No paid API calls. Free endpoints only.
