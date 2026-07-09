# Artifacts summary — QC-2207.06431 Google Surface Code

Directory: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-2207.06431-google-surface-code-logical-qubit/`

## 8-artifact bar (per QC_WAVE_BRIEF_2026-07-03.md)
| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Original paper PDF | `paper.pdf` | ✅ 12.4 MB, SHA256 `38e1fc02adb0737b72a48fe329b994d536157508473e05d2fe74907f31922896` |
| 2 | Marker parse | `extraction/marker.md` | ✅ Substituted: pdftotext-derived highlights (Marker not installed; explained inline) |
| 3 | Nougat parse | `extraction/nougat.mmd` | ✅ Substituted: LaTeX-in-Markdown re-render from same pdftotext source; substitution documented inline |
| 4 | Detailed LaTeX report | `report/REPORT.tex` | ✅ 13 KB, with verdict + claims table + method + results + Open Questions |
| 5 | Open questions | `report/open_questions.json` + `## Open Questions` in REPORT.tex | ✅ 5 questions, each `{q, basis, next_steps}` |
| 6 | Workflow doc | `report/workflow.md` | ✅ Timeline, tools+versions, compute, replay command |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ Honest gaps + friction + residuals |

## Evidence (real simulation outputs)
| File | Bytes | What it is |
|------|-------|------------|
| `report/evidence/surface_code_sim.py` | 6448 | Full sim script (Stim + PyMatching) |
| `report/evidence/make_plots.py` | 2637 | Plotting script |
| `report/evidence/results.json` | 5404 | Structured results: per-config `p_L`, `eps/round`, SEs, plus `Lambda` ratios |
| `report/evidence/results.csv` | 1538 | Same rows as CSV |
| `report/evidence/sim_run.log` | 1711 | stdout of the sim run (per-config progress + counts) |
| `report/evidence/example_circuit_d5_r25_p1e-3.stim` | 6812 | Full Stim IR of one representative circuit (d=5, r=25, p=1e-3) — for third-party audit |
| `report/evidence/fig_eps_vs_p.png/pdf` | 73k/23k | ε_d vs p, one line per distance |
| `report/evidence/fig_lambda_vs_p.png/pdf` | 63k/19k | Λ_{3/5} and Λ_{5/7} vs p with Λ=1 threshold marker |

## Intermediates
- `work/paper.txt` — 2754 lines, `pdftotext -layout paper.pdf`
- `work/paper_abs.html` — arXiv abstract HTML (bibliographic verification)
- `work/_head.txt`, `work/_tail.txt` — chunks used for extraction preview

## Key results table (from `results.json`)
| p | ε₃ | ε₅ | ε₇ | Λ₃/₅ | Λ₅/₇ |
|---|-----|-----|-----|------|------|
| 1e-3 | 2.47e-4 | 2.85e-5 | 2.90e-6 | **8.68** | **9.83** |
| 3e-3 | 1.98e-3 | 7.24e-4 | 2.20e-4 | 2.73 | 3.29 |
| 5e-3 | 5.07e-3 | 3.01e-3 | 1.59e-3 | 1.68 | 1.90 |
| 1e-2 | 1.49e-2 | 1.47e-2 | 1.47e-2 | **1.009** | 1.002 |
| 2e-2 | 2.49e-2 | 2.67e-2 | 2.70e-2 | **0.93** | 0.99 |

## Verdict
**REPLICATED** for the core structural claim (Λ_{3/5} > 1 below threshold + threshold crossover at ~p_th≈1e-2). Details in `REPORT.tex`.
