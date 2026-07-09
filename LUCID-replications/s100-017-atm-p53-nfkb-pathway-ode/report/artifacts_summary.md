# Artifacts Summary — s100-017 (Jonak et al. 2016)

## Report artifacts (report/)
| File | Bytes | Purpose |
|---|---|---|
| REPORT.md | ~9 KB | Original narrative report (2026-06-22). Verdict, claim table, blockers. |
| REPORT.tex | ~10 KB | LaTeX version with honest Critique section (backfill 2026-07-06). Compiles with `pdflatex REPORT.tex`. |
| open_questions.json | ~7 KB | Bare-list JSON, 5 open questions with q/basis/next_steps. |
| open_questions_section.tex | ~6 KB | LaTeX version of open questions, `\input`'d by REPORT.tex. |
| workflow.md | ~4 KB | Step-by-step replication workflow (phase 1–7). |
| artifacts_summary.md | (this) | Inventory of every artifact and its purpose. |
| failure_analysis.md | ~4 KB | Honest critique: what didn't work, what wasn't tested, what remains uncertain. |

## Code artifacts (code/)
| File | Purpose |
|---|---|
| parameters.py | 133 rate constants from MOESM4 tables 1–5, symbol/value/unit. |
| model.py | 60-state ODE RHS (all MOESM1 Eqs. + mean-field gene-state expressions). |
| initial_conditions.py | 60 ICs × 2 conditions (Ctr-RNAi, Wip1-RNAi) from MOESM3. |
| run_steady.py | 48 h zero-input drift check (<1% on every major species). |
| run_ir.py | 10 Gy IR (1 Gy/min pulse) → Figs. 2 & 3 + claims_10Gy.json. |
| run_dose_response.py | 6-dose sweep × 2 lines + 3-arm TNFα/IR → Fig. 4 + JSONs. |

## Evidence artifacts (evidence/)
| File | Content |
|---|---|
| parameters.json | 133 parameter symbols with values (paper-quoted). |
| claims_10Gy.json | 13 numerical claims scored against the 10 Gy IR run. |
| dose_response.json | 6 doses × 2 conditions × 11 output metrics each. |
| tnf_experiment.json | 3-arm TNFα timing comparison. |
| trajectories_10Gy.npz | Full 60-var × 481-timepoint × 2-condition NumPy array. |

## Figures (figures/)
| File | Reproduces |
|---|---|
| fig2_wip1.png | Paper Fig. 2 — Wip1 kinetics after 10 Gy, Ctr vs Wip1-RNAi. |
| fig3_p53_mdm2_chk2_wip1.png | Paper Fig. 3 — 4-panel p53/Mdm2/Chk2/Wip1 dynamics. |
| fig4_dose_response.png | Paper Fig. 4 — 3-panel dose-response (peak p53, p21, Bax_48h). |
| fig4c_tnf_ir.png | Paper Fig. 4c — TNFα/IR 3-arm comparison. |

## Sources (source/)
| Path | Content |
|---|---|
| paper.pdf | Jonak et al. 2016 primary text (BMC Systems Biology, CC-BY). |
| supplements/MOESM1..10 | All 10 open-access supplementary files. |

## OCR / Extraction (ocr/, extraction/)
| Path | Method | Purpose |
|---|---|---|
| ocr/raw_layout.txt | pdftotext -layout | Primary paper text extraction. |
| ocr/MOESM1..6.txt | pdftotext -layout | Per-supplement OCR (BMC PDFs have text layer, no OCR needed). |
| extraction/nougat.mmd | STUB (see file) | Nougat re-extraction not required; pdftotext -layout was sufficient. |

## Provenance
- All PDFs downloaded from BMC open-access URLs 2026-06-22.
- License CC-BY 4.0; permits redistribution + derivative works.
- No paid inference; all replication runs local CPU with LSODA.
