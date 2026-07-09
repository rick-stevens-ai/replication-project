# Artifacts summary

## Directory tree
```
QC-quant-ph-0211140-quantum-algorithms-hidden-shift-vandam/
├── paper.pdf                                    # (1) 214 KB, 12 pages
├── extraction/
│   ├── marker.md                                # (2) pdftotext fallback + disclosure header
│   ├── nougat.mmd                               # (3) pdftotext fallback + disclosure header
│   └── paper_layout.txt                         # (aux) pdftotext -layout output
├── report/
│   ├── REPORT.tex                               # (4) full LaTeX report
│   ├── open_questions.json                      # (5) 5 deep open questions with next_steps
│   ├── workflow.md                              # (6) narrative + tools + effort
│   ├── artifacts_summary.md                     # (7) this file
│   ├── failure_analysis.md                      # (8) honest failure log
│   └── evidence/
│       ├── hidden_shift_zn.py                   # core replication code (~300 LOC)
│       └── hidden_shift_results.json            # every trial + summary stats
└── work/
    ├── paper.pdf                                # arXiv PDF (source)
    └── paper.txt                                # pdftotext reading-order output
```

## Files (with sizes)

| Artifact | Path | Size | Kind | Origin |
|---|---|---|---|---|
| Paper PDF | `paper.pdf` | 214 KB | binary | arxiv.org/pdf/quant-ph/0211140 |
| Paper PDF (copy) | `work/paper.pdf` | 214 KB | binary | curl |
| pdftotext | `work/paper.txt` | ~40 KB | text | pdftotext v22.02 |
| pdftotext layout | `extraction/paper_layout.txt` | ~35 KB | text | pdftotext -layout |
| Marker fallback | `extraction/marker.md` | ~40 KB | text | pdftotext + disclosure header |
| Nougat fallback | `extraction/nougat.mmd` | ~40 KB | text | pdftotext + disclosure header |
| LaTeX report | `report/REPORT.tex` | 14 KB | LaTeX | this replication |
| Open questions | `report/open_questions.json` | 5 KB | JSON | this replication |
| Workflow | `report/workflow.md` | 5 KB | Markdown | this replication |
| Failure analysis | `report/failure_analysis.md` | (this pass) | Markdown | this replication |
| Simulation code | `report/evidence/hidden_shift_zn.py` | 15 KB | Python | this replication |
| Results | `report/evidence/hidden_shift_results.json` | ~20 KB | JSON | numpy run of hidden_shift_zn.py |

## Traces / logs

- Stdout of the main run is reproducible via `python report/evidence/hidden_shift_zn.py` (< 5 s).
- Summary from that run (also embedded in `hidden_shift_results.json`):
  ```
  Z_8   chirp g: 10/10 exact recoveries, mean p=1.0000
  Z_16  chirp g: 10/10 exact recoveries, mean p=1.0000
  Z_32  chirp g: 10/10 exact recoveries, mean p=1.0000
  Z_8   boolean g: 10/10 recoveries (argmax), mean p=0.7286
  Z_16  boolean g: 10/10 recoveries (argmax), mean p=0.6988
  Z_32  boolean g: 10/10 recoveries (argmax), mean p=0.8038
  Legendre F_13:  10/10 recoveries, mean p=0.9231, theory (1-1/p)^2=0.8521
  classical query lower bound Z_8/16/32: 3/4/5 queries (info-theoretic ceil log2 N)
  ```

## Provenance / accessions

- arXiv: `quant-ph/0211140` (van Dam, Hallgren, Ip — verified from PDF header + author affiliations).
- No external dataset accessions (this paper is pure algorithms; the "data" is the oracle function chosen by the reproducer).
- No external services used (Argo etc. not needed for a numpy-only replication).
