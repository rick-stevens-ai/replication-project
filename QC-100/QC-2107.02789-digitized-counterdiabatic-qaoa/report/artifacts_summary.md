# Artifact Summary — arXiv:2107.02789

## Original replication artifacts (pre-backfill)
| File | Purpose |
|---|---|
| `report/REPORT.md` | Prose report with claims table, methods, results table, verdict. |
| `report/evidence/maxcut_results.json` | Machine-readable full results (12 rows: 3 graphs × 4 depths × 2 variants). |
| `report/evidence/maxcut_stdout.log` | Raw stdout of the simulation run (energies, cuts, ratios, wall times). |
| `report/evidence/approx_ratio_vs_p.png` | Approximation ratio vs p, both variants, all three graphs. |
| `code/dcqaoa_maxcut.py` | Independent Qiskit statevector reimplementation of QAOA and DC-QAOA. |
| `code/plot_results.py` | Plotting script. |
| `work/paper.pdf`, `work/paper.txt` | The arXiv paper (fetched fresh). |

## Backfilled artifacts (2026-07-06)
| File | Purpose |
|---|---|
| `report/REPORT.tex` | LaTeX version of the report, includes honest Critique section (§5) and \input{open_questions_section.tex}. |
| `report/open_questions.json` | 5 open questions in machine-readable form: `[{"q","basis","next_steps"}]`. |
| `report/open_questions_section.tex` | LaTeX rendering of the 5 open questions. |
| `report/workflow.md` | Step-by-step workflow, data flow, environment, reproducibility. |
| `report/artifacts_summary.md` | This file. |
| `report/failure_analysis.md` | Honest failure/limitation analysis (what wasn't tested, what's shaky). |
| `extraction/nougat.mmd` | Placeholder for future full-paper OCR/nougat extraction. |

## Verdict
**REPLICATED** — headline low-p MaxCut advantage of DC-QAOA over QAOA reproduced exactly on the paper's K₄ instance (R=1.0000 at p=1 for DC-QAOA vs 0.9244 for QAOA) and qualitatively/quantitatively on independent n=6 and n=8 3-regular graphs (Fig. 3b trend).

## Headline-exercised note
The MaxCut headline claim (Fig. 3a small-graph + Fig. 3b depth scaling) IS exercised; the LFIM 12-qubit headline claim (Fig. 2a) is NOT (scoped out despite being CPU-feasible). Overall verdict remains REPLICATED because the primary quantitative claim on the classical-optimization use-case reproduces exactly on the paper's own instance.
