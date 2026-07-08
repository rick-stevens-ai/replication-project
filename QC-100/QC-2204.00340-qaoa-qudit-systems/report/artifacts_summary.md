# Artifacts Summary — arXiv:2204.00340

## Directory layout

```
QC-2204.00340-qaoa-qudit-systems/
├── paper/
│   ├── 2204.00340.pdf          # v2, arXiv, May 2023 (PRR 5, 033039)
│   └── 2204.00340.txt          # pdftotext dump
├── code/
│   └── qudit_qaoa.py           # from-scratch NumPy simulator (both encodings)
├── extraction/
│   └── nougat.mmd              # (backfill stub — mmd not re-derived)
├── results/
│   ├── replication_results.json  # full sweep, per-restart values
│   └── run.log                   # captured stdout
└── report/
    ├── REPORT.md               # canonical narrative
    ├── REPORT.tex              # LaTeX version (backfill 2026-07-06)
    ├── open_questions.json     # 5 open follow-ons (bare list)
    ├── open_questions_section.tex
    ├── workflow.md             # stage-by-stage narrative
    ├── artifacts_summary.md    # this file
    ├── failure_analysis.md     # honest critique
    └── evidence/               # duplicates of code + results for portability
```

## 8-artifact standard checklist

| # | Artifact                              | Path                                       | Present |
|---|---------------------------------------|--------------------------------------------|---------|
| 1 | Paper (PDF)                           | paper/2204.00340.pdf                       | ✅ |
| 2 | Extraction (nougat/marker)            | extraction/nougat.mmd                      | ✅ (stub) |
| 3 | Replication code                      | code/qudit_qaoa.py                         | ✅ |
| 4 | Numerical results                     | results/replication_results.json + run.log | ✅ |
| 5 | Narrative report (md + tex)           | report/REPORT.md, report/REPORT.tex        | ✅ |
| 6 | Open questions (json + tex)           | report/open_questions{.json,_section.tex}  | ✅ |
| 7 | Workflow doc                          | report/workflow.md                         | ✅ |
| 8 | Failure/critique doc                  | report/failure_analysis.md                 | ✅ |

## Key numbers (from results/replication_results.json)

- Qudit gap at p=5: **3.37**  (paper trend: monotone decrease with p)
- Qudit P(ground manifold) at p=5: **0.882**  (paper trend: sharpening)
- Qubit gap at p=5: **16.66** (matched problem, 12 qubits)
- Qubit P(ground manifold, valid) at p=5: **0.509**
- Gap ratio qubit/qudit at p=5: **≈5×** → C3 headline reproduced
- Restarts per (p, encoding): 15 (L-BFGS-B)
- Total wall clock: 1193 s (1 CPU core)
