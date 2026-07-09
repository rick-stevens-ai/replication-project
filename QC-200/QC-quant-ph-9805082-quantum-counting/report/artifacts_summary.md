# Artifacts summary

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9805082-quantum-counting`

## 8 mandatory artifacts (per QC-200 brief, 2026-07-05 standard)

| # | Path | Size | Purpose |
|---|---|---|---|
| 1 | `paper.pdf` | 176 KB | Original arXiv:quant-ph/9805082 PDF (12 pages) |
| 2 | `extraction/marker.md` | 37 KB | Marker-equivalent text extraction (pdftotext fallback; Marker unavailable) |
| 3 | `extraction/nougat.mmd` | 37 KB | Nougat-equivalent LaTeX-flavored extraction (pdftotext fallback; Nougat unavailable) |
| 4 | `report/REPORT.tex` + `report/REPORT.pdf` | 11 KB / 247 KB | Section-by-section report with claims table, Method, Results-vs-paper, Verdict |
| 5 | `report/open_questions.json` + Open Questions § in REPORT | 4 KB | 5 non-trivial follow-up questions grounded in the replication |
| 6 | `report/workflow.md` | 3.9 KB | Step-by-step workflow, tool versions, effort estimate |
| 7 | `report/artifacts_summary.md` | this file | Inventory + traces |
| 8 | `report/failure_analysis.md` | 3 KB | Honest failure analysis (diffusion-sign bug, Marker/Nougat gap) |

## Supporting artifacts (evidence + intermediates)

| Path | Size | Purpose |
|---|---|---|
| `report/evidence/quantum_counting.py` | 7.9 KB | Complete Qiskit implementation of Count(F, P) + sweep driver |
| `report/evidence/results.json` | ~10 KB | Raw per-configuration results (JSON, all 8 runs) |
| `report/evidence/results.csv` | 1 KB | Tabular summary used to build the Results-vs-paper table |
| `work/paper.pdf` | 176 KB | Working copy of the PDF (identical to root paper.pdf) |
| `work/abs.html` | 40 KB | arXiv abs page snapshot |
| `work/paper.txt` | 37 KB | pdftotext dump used by the extraction fallback |
| `extraction/paper.txt` | 37 KB | Extraction working file |
| `venv/` | (large, not counted) | Python venv with qiskit 2.5.0 + qiskit-aer 0.17.2 |

## Trace back to headline claim

Theorem 5 (BHT'98): `|t - t̃| < (2π/P)√(tN) + (π²/P²)N` with probability ≥ 8/π² ≈ 0.811.

Reproduced by: `report/evidence/quantum_counting.py` → sweep of 8 configurations
(N=16, t∈{1,2,4,8}, P∈{16,32}). Results in `results.csv` show all 8 empirical
success probabilities ≥ 0.87 (exceeding the analytical floor) and all 8
max-probability estimators round to the true t. Table reproduced in
`REPORT.tex §3.1`.

## Verdict

**REPLICATED.**  Written in `WAVE_RESULT` line at end of subagent transcript, in
REPORT.tex Abstract, and in REPORT.tex §4 Verdict.
