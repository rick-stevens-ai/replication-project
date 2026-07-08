# Artifacts summary — QC-2011.10027-contextual-subspace-vqe

## Directory tree
```
QC-2011.10027-contextual-subspace-vqe/
├── work/
│   ├── paper.pdf                # arXiv:2011.10027v2, downloaded via curl
│   └── paper.txt                # pdftotext -layout extraction
├── extraction/
│   └── nougat.mmd               # stub (backfill 2026-07-06): text
│                                #  extraction sufficient for this paper
├── code/
│   ├── csvqe_section24.py       # Sec 2.4 reproduction (10 000 random H)
│   ├── csvqe_h2.py              # H2 single-partition demo
│   ├── csvqe_h2_sweep.py        # H2 fix-generators sweep
│   └── csvqe_h2_smart.py        # H2 exhaustive partition search
├── report/
│   ├── REPORT.md                # original narrative report (2026-07-03)
│   ├── REPORT.tex               # LaTeX version (backfill)
│   ├── open_questions.json      # 5 open questions (backfill)
│   ├── open_questions_section.tex   # LaTeX open-questions section (backfill)
│   ├── workflow.md              # end-to-end workflow (backfill)
│   ├── artifacts_summary.md     # this file (backfill)
│   ├── failure_analysis.md      # honest limitations (backfill)
│   └── evidence/
│       ├── section24_result.json    # C1 raw output
│       ├── h2_csvqe_result.json     # C2 single-partition raw
│       ├── h2_sweep_result.json     # C2 fix-generators raw
│       └── h2_smart_result.json     # C2 exhaustive raw (headline)
└── .venv/                       # Python 3.13 venv (not committed)
```

## Artifact inventory (8-artifact standard)

| # | Artifact                              | Path                                  | Provenance                     |
|---|---------------------------------------|---------------------------------------|--------------------------------|
| 1 | Paper PDF                             | work/paper.pdf                        | arXiv:2011.10027v2             |
| 2 | Text extraction                       | work/paper.txt                        | pdftotext (2026-07-03)          |
| 3 | Nougat MMD (stub)                     | extraction/nougat.mmd                 | backfill 2026-07-06 (n/a here)  |
| 4 | Original narrative report             | report/REPORT.md                      | 2026-07-03                     |
| 5 | LaTeX report                          | report/REPORT.tex                     | backfill 2026-07-06            |
| 6 | Open questions (JSON, 5 items)        | report/open_questions.json            | backfill 2026-07-06            |
| 7 | Open-questions LaTeX section          | report/open_questions_section.tex     | backfill 2026-07-06            |
| 8 | Workflow / artifacts / failure trilogy | report/workflow.md, artifacts_summary.md, failure_analysis.md | backfill 2026-07-06 |

## Evidence artifacts (raw, quantitative)

| File                                    | Content                                          |
|-----------------------------------------|--------------------------------------------------|
| report/evidence/section24_result.json   | Mean/median frac errors over 10 000 samples for nc-only and CS-VQE |
| report/evidence/h2_csvqe_result.json    | Single-partition H2 CS-VQE energy                |
| report/evidence/h2_sweep_result.json    | Fix-generators sweep: (q, best-E) per q          |
| report/evidence/h2_smart_result.json    | Exhaustive: 6 015 nc partitions, best-E per d=2^q |

## Headline numbers (from evidence JSONs)
* Sec 2.4 (n=10 000, seed 20260703):
  * mean frac err, nc only         = 0.2558   (paper: 0.257)
  * mean frac err, CS-VQE          = 0.0267   (paper: 0.0268)
* H2/STO-3G/JW (exhaustive):
  * FCI = -1.13727017 Ha
  * best q=0 partition -> E = -1.13700852 Ha (err 2.6e-4)
  * best q=1 partition -> E = -1.13727017 Ha (err 1.1e-15) [HEADLINE]
  * q >= 2                                    -> exact FCI

## Free-endpoint compliance
All computation on CherryRd CPU. No paid API calls. No HPC.
Total wall time < 10 s.
