# Artifacts Summary — arXiv:2402.04000 replication

## Required 8 artifacts (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Size | Present |
|---|----------|------|------|---------|
| 1 | Paper PDF | `paper.pdf` | 748 KB | ✔ |
| 2 | Marker extraction | `extraction/marker.md` (pdftotext-layout fallback) | 96 KB | ✔ |
| 3 | Nougat extraction | `extraction/nougat.mmd` (pdftotext-raw fallback) | 59 KB | ✔ |
| 4 | REPORT.tex | `report/REPORT.tex` | 12 KB | ✔ |
| 5 | Open questions (5) | `report/open_questions.json` + `## Open Questions` in REPORT.tex | 4.4 KB | ✔ |
| 6 | Workflow | `report/workflow.md` | 3.2 KB | ✔ |
| 7 | Artifacts summary | `report/artifacts_summary.md` (this file) | -- | ✔ |
| 8 | Failure analysis | `report/failure_analysis.md` | -- | ✔ |

## Evidence directory (`report/evidence/`)

| File | Purpose |
|------|---------|
| `lre_replication.py` | Independent implementation of global RE + LRE from scratch (multivariate Lagrange coefficients, standard-basis specialisation, d=1 linear extrapolation). ~260 lines. |
| `plot_results.py` | Matplotlib plotter for results JSON files. |
| `smoke.json` | Quick n=2,3, 100k shots x 3 trials smoke test. |
| `results_gamma0.02.json` | Full sweep n=2..6, 1e6 shots x 5 trials, gamma=0.02. Verdict evidence. |
| `results_gamma0.06.json` | Full sweep n=2..8, 1e6 shots x 10 trials, gamma=0.06. Directly comparable to paper Table I regime. |
| `results_gamma0.02.png` | Log-scale plot: LRE << RE << unmit across widths. |
| `results_gamma0.06.png` | Same plot at higher noise; RE saturates, LRE keeps a gap. |

## Work directory (`work/`)

| File | Purpose |
|------|---------|
| `paper.pdf` | Duplicate of top-level `paper.pdf` (also lives in work/ per convention). |
| `paper.txt` | Original pdftotext dump used during skim. |
| `paper_layout.txt` | pdftotext -layout dump (basis for marker.md fallback). |
| `paper_raw.txt` | pdftotext -raw dump (basis for nougat.mmd fallback). |

## Traces

* All Python invocations logged in the subagent transcript (single continuous session `agent:main:subagent:0883a247`).
* Each JSON result file contains `meta.runtime_sec`, exact shot budget, gamma, trial count, and scale-factor choice — enough to re-derive the plots and tables bit-for-bit.
* No external network calls after the initial `curl` to arXiv.
