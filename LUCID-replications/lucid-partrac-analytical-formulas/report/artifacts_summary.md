# Artifacts Summary — PARTRAC Analytical Formulas

## Source
- `source-paper.md` — cached paper text (Kundrát et al., *Sci Rep* 10:15775, 2020,
  DOI `10.1038/s41598-020-72857-z`). Task queue DOI mismatch logged (F8).

## Code (implemented from paper text alone)
| File | Purpose |
|---|---|
| `code/formulas.py` | Eq. 1 (SB/SSB) and Eq. 2 (DSB family) with `N.A.` handling. |
| `code/parameters.py` | Verbatim Tables 1–2 transcription, keyed by (ion, class). |
| `code/run_replication.py` | Driver: sweeps LET, evaluates both equations, writes results + figures. |

## Results
| File | Contents |
|---|---|
| `results/summary.json` | Low-LET headline baselines (SB≈170, SSB≈156, DSB≈6.90 at H, LET=0.5). |
| `results/yield_grid.csv` | Log-spaced LET grid × ion × damage class → yield (Gy⁻¹ Gbp⁻¹). |
| `results/table_excerpts.txt` | Selected paper-text excerpts used for cross-checks. |

## Figures (fit-line only — no PARTRAC symbols; MC points unpublished)
| File | Corresponds to |
|---|---|
| `figures/fig1_sb_total_yields.png` | Paper Fig. 1 (SB vs LET). |
| `figures/fig2_dsb_total_yields.png` | Paper Fig. 2 (DSB vs LET). |
| `figures/fig3_dsb_sites_total_yields.png` | Paper Fig. 3 (DSB sites vs LET). |
| `figures/fig4_dsb_sites_effect_components.png` | Paper Fig. 4 (component decomposition). |

## Report bundle
| File | Purpose |
|---|---|
| `REPORT.md` (top level) | Original narrative replication report. |
| `report/REPORT.tex` | LaTeX replication report (verdict, audit, honest critique, `\input{open_questions_section.tex}`). |
| `report/open_questions.json` | 5 truly-open reproducibility/extension questions with next steps. |
| `report/open_questions_section.tex` | Same 5 questions rendered as a LaTeX section. |
| `report/workflow.md` | Step-by-step replication workflow, inputs, non-goals. |
| `report/artifacts_summary.md` | This file — index of everything on disk. |
| `report/failure_analysis.md` | What was tried, what worked, what did not, why. |
| `extraction/nougat.mmd` | Stub — MMD extraction was not run; markdown source used directly. |

## Not produced (with reasons)
| Missing | Reason |
|---|---|
| Independent MC yield points | PARTRAC not public/runnable; no Geant4-DNA re-run in this pass. |
| Refitted coefficients | Requires raw MC points, which are not deposited anywhere accessible. |
| Cross-code comparison (Geant4-DNA / TOPAS-nBio) | Out of scope for backfill (compute budget); listed as Q1. |
| RMS-vs-PARTRAC validation | Blocked by absence of raw simulation points. |

## Verdict
**PARTIAL** — retained from the queue. Rationale in `REPORT.tex` §Critique.
