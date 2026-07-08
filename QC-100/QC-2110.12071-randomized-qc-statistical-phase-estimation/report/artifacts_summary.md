# Artifacts Summary — QC-2110.12071

Directory: `QC-100/QC-2110.12071-randomized-qc-statistical-phase-estimation/`

## Paper/source artifacts (`work/`)
| File | Purpose |
|---|---|
| `work/abs.html` | arXiv abstract page (author/DOI/version anchor) |
| `work/paper.pdf` | arXiv PDF v2 (13 Jul 2022), authoritative source text |
| `work/paper.txt` | `pdftotext -layout` dump for `grep`/`awk` pipelines |

## Extraction (`extraction/`)
| File | Purpose |
|---|---|
| `extraction/nougat.mmd` | Nougat markdown-math extraction stub (see file for reproduction command; content is the pdftotext-derived equivalent as this backfill did not re-run OCR) |

## Code (`code/`)
| File | Purpose |
|---|---|
| `code/statistical_pe.py` | Main replication — builds 2q TFIM, samples $j\sim\|F_j\|/A$, runs simulated Hadamard tests on exact $U_j=e^{i\hat H t_j}$, accumulates $\tilde C(x)$, writes JSON evidence. Supports `--n-samples`, `--d`, `--scaling`, `--scan-reps`. |
| `code/make_plots.py` | Renders `fig_cdf.png` and `fig_scaling.png` from JSON evidence. |

## Evidence (`report/evidence/`)
| File | Purpose |
|---|---|
| `report/evidence/spe_run.json` | Single-run log ($N=40{,}000$): Hamiltonian spectrum, overlaps, Fourier weights, $\tau E_\text{gs}^\text{est}=-1.0707$, energy $-1.4088$ (error 0.0053). |
| `report/evidence/spe_scaling.json` | 8-$N$ × 24-rep scan: per-$N$ std of $\tilde C(x_0)$, bias, RMS energy error. |
| `report/evidence/fig_cdf.png` | Analytic $\tilde C(x)$ vs.\ sampled estimator; vertical lines at true $\tau E_k$; jumps visible only at non-zero-overlap eigenvalues. |
| `report/evidence/fig_scaling.png` | Left: $\log$std vs.\ $\log N$, slope $-0.451$ vs.\ paper $-0.500$. Right: RMS energy error vs.\ $N$. |

## Report (`report/`)
| File | Purpose |
|---|---|
| `report/REPORT.md` | Original replication report (2026-07-03). |
| `report/REPORT.tex` | LaTeX version with genuine critique + headline-exercised judgment (backfill). |
| `report/open_questions.json` | 5-item bare JSON list of open questions (backfill). |
| `report/open_questions_section.tex` | LaTeX-typeset version of the 5 open questions (backfill). |
| `report/workflow.md` | Reproduction workflow (backfill). |
| `report/artifacts_summary.md` | This file (backfill). |
| `report/failure_analysis.md` | Honest gap/failure critique of the replication (backfill). |

## Environment
- `.venv/` — Python 3.14.6 sandbox; NumPy 2.5.0, SciPy 1.18.0, Qiskit 2.5.0, Matplotlib.

## Cost/endpoint tally
- Compute: local CherryRd M2 CPU only (~15 s wall).
- External endpoints: none (paper PDF + arXiv abstract only, both free).
- Paid endpoints touched: **none**.

## 8-artifact standard checklist
- [x] REPORT.md (original)
- [x] REPORT.tex (backfill)
- [x] open_questions.json (backfill, bare 5-item list)
- [x] open_questions_section.tex (backfill)
- [x] workflow.md (backfill)
- [x] artifacts_summary.md (backfill, this file)
- [x] failure_analysis.md (backfill)
- [x] extraction/nougat.mmd (backfill stub)
