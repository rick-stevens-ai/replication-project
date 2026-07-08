# Artifacts Summary — QC-2110.15958-hybrid-hhl-plusplus

## Layout

```
QC-2110.15958-hybrid-hhl-plusplus/
├── code/
│   └── hhl_replication.py         # Baseline + Hybrid HHL circuits, run + evidence writer
├── report/
│   ├── REPORT.md                  # Full replication report (markdown, original 2026-07-03)
│   ├── REPORT.tex                 # LaTeX version with critique section (backfill)
│   ├── open_questions.json        # 5 truly-open questions (bare JSON list)
│   ├── open_questions_section.tex # Same 5 questions rendered as LaTeX section
│   ├── workflow.md                # Pipeline / time budget / endpoints used
│   ├── artifacts_summary.md       # This file
│   ├── failure_analysis.md        # Honest critique of what wasn't tested
│   └── evidence/
│       ├── replication_results.json  # A, b, x_classical, per-variant metrics
│       └── verdict_summary.json      # Gate/qubit/fidelity comparison + booleans
├── extraction/
│   └── nougat.mmd                 # Nougat-mode text extract stub (backfill)
├── logs/
│   └── run1.log                   # Full stdout of the reproducing run
└── work/
    ├── paper.pdf                  # arXiv:2110.15958 v6 (2.1 MB)
    ├── paper.txt                  # pdftotext of paper
    └── abs.html                   # arXiv abstract page
```

## Artifact roles

| artifact | role | when created |
|---|---|---|
| `work/paper.pdf` | canonical source (arXiv v6) | 2026-07-03 |
| `work/paper.txt` | grep/section-nav | 2026-07-03 |
| `code/hhl_replication.py` | reproducing script | 2026-07-03 |
| `logs/run1.log` | full stdout of the run | 2026-07-03 |
| `report/evidence/replication_results.json` | raw per-variant metrics | 2026-07-03 |
| `report/evidence/verdict_summary.json` | headline comparison + verdict booleans | 2026-07-03 |
| `report/REPORT.md` | primary report | 2026-07-03 |
| `report/REPORT.tex` | LaTeX report + critique | 2026-07-06 (backfill) |
| `report/open_questions.json` | 5 open questions, bare list | 2026-07-06 (backfill) |
| `report/open_questions_section.tex` | LaTeX render of open questions | 2026-07-06 (backfill) |
| `report/workflow.md` | pipeline / time budget | 2026-07-06 (backfill) |
| `report/artifacts_summary.md` | this file | 2026-07-06 (backfill) |
| `report/failure_analysis.md` | honest critique | 2026-07-06 (backfill) |
| `extraction/nougat.mmd` | Nougat extract stub | 2026-07-06 (backfill) |

## Evidence pointers

- **Headline numbers** — `report/evidence/verdict_summary.json`:
  - CNOT reduction 92.0% (50 → 4), qubit reduction 50.0% (4 → 2),
    depth reduction 88.8% (89 → 10), fidelity 1.0000 preserved.
- **Per-variant raw metrics** — `report/evidence/replication_results.json`
  (baseline at n_clock=2/3/4 + hybrid).
- **Reproducer** — `code/hhl_replication.py`, one-liner in REPORT.md §7.

## Preservation note

All artifacts from the original 2026-07-03 run were preserved verbatim
during the 2026-07-06 backfill. Backfill only added new files; no
existing files were edited or overwritten.
