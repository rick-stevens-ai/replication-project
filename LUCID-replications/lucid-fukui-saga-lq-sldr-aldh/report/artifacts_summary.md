# Artifacts Summary — Fukui et al. 2022 Replication

**Target:** Fukui R., Saga R., Matsuya Y., et al. *Tumor radioresistance caused by radiation-induced changes of stem-like cell content and sub-lethal damage repair capability.* Sci Rep 12, 1056 (2022). DOI 10.1038/s41598-022-05172-4.

**Verdict:** PARTIAL (strong). Coverage 9/10, Agreement 9/10.

## Top-level files
| Path | Purpose |
|---|---|
| `REPORT.md` | Original re-pass report (canonical, preserved verbatim) |
| `REPORT.pass1.md` | Original pass-1 report, preserved verbatim |
| `PARSER_PROVENANCE.md` | Pass-1 vs re-pass parser + file hashes |

## `report/` (backfill 2026-07-06)
| Path | Purpose |
|---|---|
| `report/REPORT.tex` | LaTeX writeup with honest critique + `\input{open_questions_section.tex}` |
| `report/open_questions.json` | 5 open questions, `{q, basis, next_steps}` (bare JSON list) |
| `report/open_questions_section.tex` | LaTeX version of the 5 open questions |
| `report/workflow.md` | Step-by-step workflow of pass 1, re-pass, backfill |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Honest critique — done vs not-done, headline exercise status |

## `data/`
| Path | Purpose |
|---|---|
| `data/source-paper.pdf` | Original PDF (md5 `acbb80ecc6f5bfe135a0081aa2be4c9b`) |
| `data/marker_paper.md` | Marker Markdown extract (md5 `f01a1853869d563a72c5c1c06f145e12`) |
| `data/marker_figures/_page_*.jpeg` | Per-page figure rasters from Marker |

## `extraction/`
| Path | Purpose |
|---|---|
| `extraction/nougat.mmd` | Nougat extraction stub (backfill; Marker output is canonical) |

## `code/`
| Path | Purpose |
|---|---|
| `code/imk_model.py` | Pure NumPy implementation of IMK Eqs 1, 2, 4, 6, 7, 12, 13, 14 |
| `code/params_table1.py` | Table 1 verbatim (α₀, β₀, (a+c), f_s per cell line) |
| `code/digitized_fig5.py` | Vision-based Fig 5 point extraction |
| `code/replicate_fig5.py` | Fig 5 forward replication using Table 1 means |
| `code/replicate_fig6.py` | Fig 6 split-dose forward replication |
| `code/refit_mcmc.py` | Independent MCMC refit of w_SLDR from digitized Fig 5 |
| `code/repass/repass_all_claims.py` | Re-pass single script for claims A–G |

## `results/`
| Path | Purpose |
|---|---|
| `results/fig5_replication_summary.md` | Pass-1 Fig 5 R² and residuals |
| `results/fig6_replication_summary.md` | Pass-1 Fig 6 output |
| `results/mcmc_refit_summary.md` | MCMC posterior for w_SLDR |
| `results/mcmc_refit_summary.json` | Same in JSON |
| `results/repass/repass_summary.md` | Re-pass A–G table |
| `results/repass/repass_summary.json` | Same in JSON |

## `figures/`
| Path | Purpose |
|---|---|
| `figures/fig5_replication.png` | Pass-1 Fig 5 replication overlay |
| `figures/fig6_replication.png` | Pass-1 Fig 6 replication overlay |
| `figures/repass/fig6_repass.png` | Re-pass forward-only Fig 6 recovery curves |
| `figures/repass/fig7_repass.png` | Re-pass forward-only Fig 7 dose-rate curves |

## Backfill 8-artifact standard checklist (2026-07-06)
- [x] REPORT.md (top-level, canonical, preserved)
- [x] report/REPORT.tex (LaTeX with honest critique)
- [x] report/open_questions.json (5 bare-list entries)
- [x] report/open_questions_section.tex
- [x] report/workflow.md
- [x] report/artifacts_summary.md
- [x] report/failure_analysis.md
- [x] extraction/nougat.mmd (stub; Marker MD is canonical extraction)
