# Artifacts summary

Inventory of everything produced and pulled during this replication.

## Layout

```
QC-modular-functor-universal-quantum-computation-2000/
├── paper.pdf                              # (1) arXiv PDF, 212 KB
├── extraction/
│   ├── marker.md                          # (2) pdftotext -layout fallback
│   ├── nougat.mmd                         # (3) pdftotext -layout fallback
│   ├── paper.txt                          # raw pdftotext output
│   └── EXTRACTION_NOTE.md                 # notes on the marker/nougat fallback
├── report/
│   ├── REPORT.md                          # detailed markdown report
│   ├── REPORT.tex                         # (4) detailed LaTeX report
│   ├── brief.md                           # 1-paragraph brief
│   ├── attempt_log.md                     # chronological log
│   ├── artifact_harvest.md                # (URLs, sizes, checksums)
│   ├── workflow.md                        # (6) workflow + tools + effort
│   ├── artifacts_summary.md               # (7) this file
│   ├── failure_analysis.md                # (8) failure/friction analysis
│   ├── open_questions.json                # (5) 5 heavy-duty questions
│   └── evidence/
│       ├── fkw_results.json               # results of core replication
│       ├── fkw_extras.json                # results of Haar/hillclimb
│       └── fkw_hadamard_deep.json         # BFS depth-by-depth Hadamard approx
└── work/
    ├── .venv/                             # Python 3.14 venv (numpy 2.5.1, scipy 1.18.0)
    ├── fkw_replication.py                 # 415 LOC, core code
    ├── fkw_extras.py                      # 130 LOC, extras
    ├── fkw_hadamard_deep.py               # 70 LOC, deep BFS
    ├── run_judge.py                       # 90 LOC, LLM-judge caller
    ├── run_judge.sh                       # early bash version (superseded)
    ├── fkw_results.json                   # (mirror of report/evidence/*)
    ├── fkw_extras.json                    # (mirror)
    ├── fkw_hadamard_deep.json             # (mirror)
    ├── judge_input.json                   # 4 141-byte evidence bundle for judge
    ├── judge_response.json                # raw LLM response
    └── judge_verdict.txt                  # judge's JSON verdict
```

## Key traces

| Trace                     | File                                         | Content                                          |
|---------------------------|----------------------------------------------|--------------------------------------------------|
| Numerical evidence        | `report/evidence/fkw_results.json`           | Every C1..C7 check + residuals                    |
| Density stress-test       | `report/evidence/fkw_extras.json`            | Haar-comparison RMS, hillclimb dist               |
| Universality-in-action    | `report/evidence/fkw_hadamard_deep.json`     | best_dist vs braid length (depth 0..15)           |
| LLM-judge input           | `work/judge_input.json`                      | Compact evidence bundle                          |
| LLM-judge output          | `work/judge_verdict.txt`                     | Strict-JSON verdict + reasoning                  |

## SHA-256 checksums (fixed inputs only)

- `paper.pdf` → `81da2bc2c9c7a99f9449493854ab1a6114ad2d4d8594e0ab1fcd95b54d94311e`

## Storage totals

- Source PDF: 212 KB
- Text extraction: 3 × ~60 KB = 180 KB
- Code: ~30 KB
- Results (JSON): ~15 KB
- venv: ~120 MB (numpy+scipy)

Total non-venv footprint: < 500 KB.
