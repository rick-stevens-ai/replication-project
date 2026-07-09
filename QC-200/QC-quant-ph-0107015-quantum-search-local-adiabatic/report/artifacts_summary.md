# Artifacts Summary

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0107015-quantum-search-local-adiabatic/`

## 8-artifact completion bar (per REPLICATION_DIR_STANDARD_2026-07-05.md)

| # | Required artifact | File | Status |
|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | ✅ 107834 B, 4 pages, arXiv:quant-ph/0107015v1 |
| 2 | Marker parse | `extraction/marker.md` | ✅ pdftotext-based fallback (marker not installed); explicitly noted |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✅ pdftotext-based fallback (nougat not installed); explicitly noted |
| 4 | Detailed LaTeX report | `report/REPORT.tex` (+ `REPORT.pdf`, 6 pages compiled) | ✅ Includes claims table, method, results-vs-paper table, verdict |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` section in REPORT | ✅ 5 non-trivial questions with `q`, `basis`, `next_steps` |
| 6 | Workflow | `report/workflow.md` | ✅ Step-by-step + tool versions + work estimate |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |

## Complete file inventory

```
QC-quant-ph-0107015-quantum-search-local-adiabatic/
├── paper.pdf                          # arXiv:quant-ph/0107015v1 (Roland & Cerf 2001)
├── paper.txt                          # pdftotext dump of paper.pdf
├── code/
│   ├── adiabatic_search.py            # core replication code (2D + full-N sim, bisection, fit)
│   └── plots.py                       # log-log scaling plot + p(T) curve
├── extraction/
│   ├── marker.md                      # marker-style Markdown extraction (fallback: pdftotext)
│   └── nougat.mmd                     # nougat-style .mmd extraction  (fallback: pdftotext)
├── logs/                              # (empty; run log kept in report/evidence/run.log)
└── report/
    ├── REPORT.tex                     # main writeup
    ├── REPORT.pdf                     # compiled, 6 pages
    ├── open_questions.json            # 5 Q with q/basis/next_steps
    ├── workflow.md
    ├── artifacts_summary.md           # (this file)
    ├── failure_analysis.md
    └── evidence/
        ├── results.json               # sanity + T* bisection + fits, structured
        ├── run.log                    # human-readable run log
        ├── scaling.png                # log-log T* vs N (PNG)
        ├── scaling.pdf                # same, PDF for REPORT.tex \includegraphics
        └── p_vs_T_N64.png             # success probability vs T at N=64
```

## Traces

- Full numeric results: `report/evidence/results.json`
- Human-readable log with the sanity table + T* table + fit output: `report/evidence/run.log`
- Circuit/method code (fully self-contained, no ML/inference): `code/adiabatic_search.py`
- Reproducible with: `python3 code/adiabatic_search.py report/evidence && python3 code/plots.py` (~90 s)

## Headline outcome

| schedule | fitted slope | paper prediction | |Δ| | verdict |
|---|---|---|---|---|
| linear | 0.9992 | 1.0 | 0.001 | ✅ within tol |
| local-adiabatic | 0.4756 | 0.5 | 0.024 | ✅ within tol |

**Overall verdict: REPLICATED.**
