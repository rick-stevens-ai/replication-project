# Artifacts Summary — Acheva et al. 2017 Replication

## On-Disk Artifacts

| Artifact | Location | Provenance |
|---|---|---|
| Source PDF | `paper/` (or repo root, per LUCID convention) | Frontiers open-access, doi:10.3389/fimmu.2017.00082 |
| Top-level REPORT.md | `REPORT.md` | Original detailed narrative report |
| Digitized bar-chart inputs (Figs 1, 2, 7A) | `code/digitized_figures.py` | Multimodal-LLM read (Argo Claude Sonnet 4.6, free endpoint) |
| Digitized bar-chart inputs (Figs 3, 4B, 5, 6, 7B) | `code/digitized_figures_extra.py` | Multimodal-LLM read (Argo Claude Sonnet 4.6, free endpoint) |
| Spot-check statistical routines | `code/replicate_stats.py` | Tukey HSD on Figs 1, 2A, 2B, 7A |
| Extended statistical routines | `code/replicate_extended.py` | 2^-ΔΔCT identity + PDF deposit scan |
| Promo-2 extended routines | `code/replicate_promo2.py` | Tukey + trend audit on Figs 3, 4B, 5B/C, 6, 7B |
| Figure regeneration | `code/make_figures.py` | Regenerates PNGs from same digitized inputs |
| Spot-check results | `results/spotcheck_results.json` | Fig 1, 2A, 2B, 7A p-values |
| Extended results | `results/extended_results.json` | 2^-ΔΔCT + deposit-scan results |
| Promo-2 results | `results/promo2_results.json` | Fig 3, 4B, 5B/C, 6, 7B p-values + trend checks |

## Backfill Artifacts (this pass)

| Artifact | Location | Purpose |
|---|---|---|
| LaTeX report | `report/REPORT.tex` | LaTeX render of the audit narrative + critique |
| Open questions (JSON) | `report/open_questions.json` | 5 open questions with basis + next steps (structured) |
| Open questions (LaTeX) | `report/open_questions_section.tex` | Same 5 questions in LaTeX for REPORT.tex `\input` |
| Workflow diagram | `report/workflow.md` | End-to-end data flow, endpoints, reproduction command |
| Artifacts summary | `report/artifacts_summary.md` | This file |
| Failure analysis | `report/failure_analysis.md` | What worked, what broke, honest PARTIAL justification |
| Extraction stub | `extraction/nougat.mmd` | Nougat MMD extraction placeholder (equations + text) |

## Quantitative Headline Numbers Recovered

| Quantity | Paper claim | Recomputed | Match |
|---|---:|---:|---|
| 2^-ΔΔCT identity (2.4× synthetic) | 2.4× | 2.3999999998× | ✓ (< 1e-9) |
| COX-2 mRNA ">2.5× at 4h" | > 2.5× | 2.40× | ✓ (digitization slop) |
| sc-236 rescue "< 0.5× CTRL" | < 0.5× | 0.50× | ✓ (at boundary) |
| PGE2 fold-change at 72h/2Gy | 6.5× | 6.4× | ✓ (within 2%) |
| PGE2 72h 2Gy vs CTRL 72h Tukey | *** | p = 2.4e-04 → *** | ✓ exact |
| sc-236 IC50 (not in paper) | — | 16.8 µM | new |
| Bay 11-7085 IC50 (not in paper) | — | 3.8 µM | new |
| Bay 1 µM working-dose vs CTRL | ns | p = 0.28 → ns | ✓ |

## Cumulative Asterisk Audit

| Metric | Value |
|---|---:|
| Total printed asterisks audited | 27 |
| Qualitative agreement | 19/27 = 70% |
| Core-stats agreement (Fig 1, 2A, 2B, 7A) | 12/12 = 100% |
| Extended-digitization agreement (Fig 3, 6, 7B) | 7/15 = 47% |
| Trend/dose-response pass (Fig 4B, 5B, 5C) | 3/4 |

## Deposits Searched (All Zero Hits)
GEO, SRA, ArrayExpress, ENA, BioProject, PRIDE, Zenodo, Dryad, FigShare, Mendeley Data, GitHub, GitLab, Bitbucket. Scan scope: 68,135 chars of PDF text.

## Free-Endpoint Compliance
- Argo Claude Sonnet 4.6 (free) for bar-chart digitization
- scipy for all statistics
- No paid APIs, no author contact, no closed data, no nested subagents
