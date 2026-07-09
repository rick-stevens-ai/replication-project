# Artifacts summary — QC-200 replication of quant-ph/9601018

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-9601018-approximate-qft-decoherence/`

## The 8 mandatory artifacts
| # | Artifact | Path | Notes |
|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | 210 KB, 22 pages, SHA256 `d6edeff2d388fc0229cda2d28379fb45336b1eda2df748c2802d21b257f1b556` (fetched from https://arxiv.org/pdf/quant-ph/9601018 on 2026-07-05) |
| 2 | Marker parse | `extraction/marker.md` | Backfill: `pdftotext -layout` fallback with header note (Marker not installed; will backfill from central corpus when available). Convention matches other REPLICATE-PROJECT dirs. |
| 3 | Nougat parse | `extraction/nougat.mmd` | Backfill: plain `pdftotext` fallback with header note. |
| 4 | LaTeX report | `report/REPORT.tex` (+ `report/REPORT.pdf`, 4 pages) | Full section-by-section replication report. Compiled with pdflatex (TeX Live 2026). |
| 5 | Open questions (JSON) | `report/open_questions.json` | 5 non-superficial questions, each `{q, basis, next_steps}`. Mirrored in REPORT.tex's `\section*{Open Questions}`. |
| 6 | Workflow | `report/workflow.md` | Sequence, tool versions (Qiskit 2.5.0, Qiskit-Aer 0.17.2, NumPy 2.4.3, pdflatex TeX Live 2026), work estimate. |
| 7 | Artifacts summary | `report/artifacts_summary.md` | THIS FILE. |
| 8 | Failure analysis | `report/failure_analysis.md` | Honest gaps and friction points. |

## Additional evidence
| Artifact | Path | Notes |
|---|---|---|
| Experiment A + B code | `report/evidence/aqft_fidelity.py` | AQFT builder, 100-sample fidelity sweep, matrix-bound check |
| Experiment C code | `report/evidence/aqft_period_finding.py` | Period-finding on 7^x mod 15 |
| Plotting code | `report/evidence/make_plots.py` | Two-panel PNG |
| Experiment A + B raw JSON | `report/evidence/results_fidelity.json` | All 18 (n,m) rows + phase-bound rows |
| Experiment C raw JSON | `report/evidence/results_period_finding.json` | L∈{6,8} × m∈{1..L} × offset∈{0..3} |
| Figure | `report/evidence/figure_aqft_replication.png` | 150 dpi, 2 panels |
| Working PDF text | `work/paper.txt` | pdftotext dump for skim |
| Venv | `.venv/` | Isolated Python env; NOT under version control |

## Verdict trace
Every headline number in REPORT.tex has a JSON source in `report/evidence/`:
- REPORT.tex "Experiment A" table row (n=8, m=4, mean_fid=0.9903) ← `results_fidelity.json["experiment_A_fidelity"]["8"]["4"]["mean_fidelity"]` = 0.990274 ✔
- REPORT.tex "Experiment B" table row (n=8, m=6, max|ε|=0.0245, bound=0.7854) ← `results_fidelity.json["experiment_B_matrix_epsilon"]["8"]["6"]` ✔
- REPORT.tex "Experiment C" table row (L=8, m=4, success=0.5779) ← `results_period_finding.json["results"]["8"]["4"]["mean_success_prob"]` = 0.577903 ✔

No fabricated numbers.
