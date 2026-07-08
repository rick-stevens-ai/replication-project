# Artifacts summary — QC-2110.13338-efficient-zne-gate-error

Contents of `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2110.13338-efficient-zne-gate-error/`
after 2026-07-06 backfill.

## `report/`
| File | Purpose | Origin |
|------|---------|--------|
| `REPORT.md` | Original replication report (verdict + tables + evidence pointers). | Original run 2026-07-03. |
| `REPORT.tex` | LaTeX version of REPORT with honest Critique section and `\input{open_questions_section.tex}`. | Backfill 2026-07-06. |
| `open_questions.json` | Five open follow-up questions (bare JSON list of `{q, basis, next_steps}`). | Backfill 2026-07-06. |
| `open_questions_section.tex` | LaTeX rendering of the same five questions, `\input`-ed by REPORT.tex. | Backfill 2026-07-06. |
| `workflow.md` | Chronological workflow of the replication. | Backfill 2026-07-06. |
| `artifacts_summary.md` | This file. | Backfill 2026-07-06. |
| `failure_analysis.md` | Honest critique of what was and was NOT demonstrated. | Backfill 2026-07-06. |

## `report/evidence/`
| File | Purpose |
|------|---------|
| `zne_reproduction.py` | CNOT-sweep driver (raw / full ZNE / efficient ZNE). |
| `precision_vs_shots.py` | 30-trial precision study at n_c=10 across shot budgets. |
| `make_plot.py` | Fig 2-style overlay plot generator. |
| `results.json` | Full CNOT-sweep numbers + tool versions. |
| `precision_vs_shots.json` | 30-trial bias/std table. |
| `fig2_replication.png` | Overlay plot vs paper's Fig 2. |
| `run.log` | Stdout of the sweep run. |

## `extraction/`
| File | Purpose |
|------|---------|
| `nougat.mmd` | Stub Nougat-format math markdown of the paper. Not used for the numerical replication (Nougat was not run in the original attempt — see `failure_analysis.md`). |

## `work/`
| File | Purpose |
|------|---------|
| `paper.pdf` | Source paper (arXiv 2110.13338v3). |
| `paper.txt` | `pdftotext -layout` extraction of the paper. |

## `venv/`
Python 3.12 virtual environment used for the replication (mitiq 1.0.0,
qiskit 2.5.0, qiskit-aer 0.17.2, cirq 1.6.1).
Recreate with:
```
python3.12 -m venv venv && source venv/bin/activate && \
  pip install mitiq qiskit qiskit-aer cirq numpy scipy matplotlib ply
```

## Verdict summary
**REPLICATED** on headline C1–C4 of arXiv:2110.13338.
Efficient ZNE (2 scales, random folding, linear extrapolation) matches or
beats full ZNE (3 scales, global folding, Richardson) on both bias and
variance while using 66.7 % of the shot budget, on `mitiq`+`qiskit-aer`
simulation of the paper's Fig 2/3 circuit under ε=1 % depolarising +
T₁=50 µs amplitude damping.
