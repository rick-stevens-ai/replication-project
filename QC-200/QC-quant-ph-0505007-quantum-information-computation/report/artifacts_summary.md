# Artifacts Summary — quant-ph/0505007 replication

Root: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0505007-quantum-information-computation/`

## The 8 required artifacts

| # | Path | Kind | Source | Notes |
|---|------|------|--------|-------|
| 1 | `paper.pdf` | PDF | arXiv (https://arxiv.org/pdf/quant-ph/0505007) | 189,924 bytes, 12 pages, v3 (22 Mar 2006) |
| 2 | `extraction/marker.md` | Markdown | FALLBACK — pdftotext + hand curation (Marker not installed, no central corpus parse) | Provenance banner in-file |
| 3 | `extraction/nougat.mmd` | Nougat-style .mmd | FALLBACK — pdftotext + hand curation | Math restored from PDF equations |
| 4 | `report/REPORT.tex` | LaTeX report | Written this run | Includes claims table (C1-C7), method, results table, verdict, open questions |
| 5 | `report/open_questions.json` (+ `open_questions_body.tex`) | JSON + LaTeX | Written this run | 5 items, each with `q`/`basis`/`next_steps` |
| 6 | `report/workflow.md` | Markdown | Written this run | Timeline, tools/versions, effort |
| 7 | `report/artifacts_summary.md` | Markdown | This file | Inventory |
| 8 | `report/failure_analysis.md` | Markdown | Written this run | Bookkeeping bug traced + fixed |

## Evidence and code

| Path | Description |
|------|-------------|
| `report/evidence/tulsi_grover_patel_fixed_point.py` | Full numpy statevector simulator (single file, ~185 LOC) |
| `report/evidence/results.json` | Machine-readable sweep results: 12 rows across (n∈{2,3,4}) × (q∈{1,2,3,4}) with `measured_error`, `predicted_error` = ε^(2q+1), `abs_diff`, monotonicity, `verdict: REPLICATED` |
| `work/paper.txt` | pdftotext -layout dump of paper.pdf (600 lines) |

## Traces / logs

- The simulator prints a one-line-per-cell table to stdout when run; a copy of the final passing run is embedded in `report/REPORT.tex` Results section. No separate log file kept (deterministic sub-second run; re-run is the log).
- All numerical values in the report are cross-referenced back to `results.json`.

## Directory layout

```
QC-quant-ph-0505007-quantum-information-computation/
├── paper.pdf
├── extraction/
│   ├── marker.md
│   └── nougat.mmd
├── report/
│   ├── REPORT.tex
│   ├── open_questions.json
│   ├── open_questions_body.tex
│   ├── workflow.md
│   ├── artifacts_summary.md
│   ├── failure_analysis.md
│   └── evidence/
│       ├── tulsi_grover_patel_fixed_point.py
│       └── results.json
└── work/
    └── paper.txt
```

## Reproducibility

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0505007-quantum-information-computation
python3 report/evidence/tulsi_grover_patel_fixed_point.py
# expected: 'VERDICT: REPLICATED' with max abs diff ~ 3e-15
```
