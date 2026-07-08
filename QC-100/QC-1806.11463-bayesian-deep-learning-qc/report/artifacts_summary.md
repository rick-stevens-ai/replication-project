# Artifacts summary — arXiv:1806.11463

All paths relative to the paper working directory
`~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1806.11463-bayesian-deep-learning-qc/`.

## Human-readable reports
| File | Contents |
|---|---|
| `report/REPORT.md` | Full replication report (paper summary, claims table, methods, results vs paper, verdict). Original artifact. |
| `report/REPORT.tex` | LaTeX render of the report with an explicit honest-critique section. Backfilled 2026-07-06. |
| `report/workflow.md` | Chronological end-to-end log of what was done. Backfilled 2026-07-06. |
| `report/failure_analysis.md` | Honest critique of what this replication does and does NOT show. Backfilled 2026-07-06. |
| `report/open_questions.json` | 5 open questions in bare JSON list form (q / basis / next_steps). Backfilled 2026-07-06. |
| `report/open_questions_section.tex` | LaTeX version of the 5 open questions. Backfilled 2026-07-06. |
| `report/artifacts_summary.md` | This file. Backfilled 2026-07-06. |

## Machine-readable evidence
| File | Contents |
|---|---|
| `report/evidence/hhl_circuit.txt` | Qiskit gate listing of the 4-qubit HHL circuit used for the paper's exact 2x2 matrix. |
| `report/evidence/hhl_noiseless.json` | Noiseless HHL post-selected statevector + fidelity 1.000000 vs classical A^{-1}\|b>. |
| `report/evidence/hhl_noisy_sweep.json` | 8-point noisy sweep (gate_noise in {0.000..0.200}, 8192 shots each): HHL success rate + Bhattacharyya-lower-bound fidelity vs classical target. |
| `report/evidence/gp_bayesian_predict.json` | End-to-end quantum -> GP posterior: alpha, predictive mean 0.475, predictive variance 0.6725, all matching classical to 1e-16 / 1e-6. |
| `report/evidence/summary.json` | Machine-readable claim/measurement pairs (C1..C5). |
| `report/evidence/versions.txt` | Reproducibility manifest (Python 3.14.6, Qiskit 2.5.0, Qiskit-Aer 0.17.2, NumPy 2.5.0, SciPy 1.18.0, macOS host). |

## Code
| File | Contents |
|---|---|
| `code/hhl_2x2_paper.py` | Driver: noiseless HHL + 8-point noisy sweep on A = (1/2)*[[3,1],[1,3]]. |
| `code/gp_bayesian_predict.py` | Driver: end-to-end quantum -> Bayesian GP posterior. |

## Extraction
| File | Contents |
|---|---|
| `extraction/nougat.mmd` | Placeholder markdown-math extraction stub. This paper's replication was driven from the arXiv PDF directly; a full Nougat pass over 1806.11463v3 was not needed to reproduce the numerical claims (all math is in the on-disk REPORT.md and the two Python drivers). Backfilled 2026-07-06. |

## Backfill provenance
This directory previously carried the 6 original artifacts
(REPORT.md, hhl_circuit.txt, hhl_noiseless.json, hhl_noisy_sweep.json,
gp_bayesian_predict.json, summary.json, versions.txt, and the two
code drivers). The 2026-07-06 backfill added the 7 files listed above
without re-running any simulation --- all backfilled documents are
derived from and consistent with the pre-existing evidence.

## Verdict (unchanged)
**REPLICATED** for the paper's testable simulation-tier claims
(C1, C2, C3, C5). C4 (IBMQX5 hardware) is out of scope but
bracketed by our noisy sweep.
