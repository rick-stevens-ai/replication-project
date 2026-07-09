# Artifacts summary — lucid100-heavy-ion-survival-rf-pide

Independent replication of Debreceni et al. 2024 (Toxics 12(8):545) — heavy-ion cell survival prediction on NB1RGB via LQM, LocReg, and RF trained on the PIDE database.

## Verdict
- **On-disk (deliberated):** PARTIAL (independent Argo judge `argo:gpt-5.2` temp 0 — coverage=8, agreement=6)
- **Queue label:** REPLICATED
- **Cross-check result:** **MISMATCH FLAGGED**, preserved on-disk PARTIAL as the substantiated call. Queue label appears to predate the judge's downgrade.

## On-disk file inventory

### Report artifacts (this backfill)
| Path | Purpose |
|---|---|
| `report/REPORT.md` | Original replication report (2026-07-02; source of truth) |
| `report/REPORT.tex` | LaTeX version with genuine critique + verdict cross-check (backfill) |
| `report/open_questions.json` | 5 open questions, machine-readable (backfill) |
| `report/open_questions_section.tex` | LaTeX open-questions section (backfill) |
| `report/workflow.md` | Reproducible pipeline steps + provenance (backfill) |
| `report/artifacts_summary.md` | This file (backfill) |
| `report/failure_analysis.md` | Where and why the replication falls short (backfill) |

### Extraction stub
| Path | Purpose |
|---|---|
| `extraction/nougat.mmd` | Placeholder — this replication has NO `paper.pdf` on disk. Full text was harvested as JATS XML from Europe PMC (`source/fulltext.xml`) and detagged to plain text (`source/fulltext.txt`). Nougat extraction was neither run nor needed (backfill note). |

### Pipeline artifacts (pre-existing, preserved)
| Path | Purpose |
|---|---|
| `code/build_dataset.py` | Reconstructs NB1RGB-equivalent ensemble from Furusawa (2000) α(LET), β(LET); N=311, 51 experiments, ion mix matches paper |
| `code/run_pipeline.py` | Fits LQM (curve_fit), LocReg (tricube LWR), RF (1000 trees, dose+LET); 100-iter MC-CV; R² and RMSE |
| `code/make_figure.py` | Grouped bar chart of paper vs reproduced R²/RMSE |
| `data/nb1rgb_reconstructed.csv` | 311-row reconstructed NB1RGB ensemble (SUBSTITUTE for gated PIDE) |
| `results/pipeline_results.json` | Mean ± std R² and RMSE for LQM/LocReg/RF over 100 MC-CV iters |
| `results/judge_verdict.json` | Independent Argo judge coverage/agreement/verdict record |
| `figures/model_comparison.png` | Paper vs reproduced comparison figure |
| `source/fulltext.xml` | Europe PMC JATS XML of PMC11359366 |
| `source/fulltext.txt` | Plain-text detagged full text |

## Quantitative headline (from `results/pipeline_results.json`)

| Model | Inputs | Paper R² | Repro R² | Paper RMSE | Repro RMSE | Status |
|---|---|---|---|---|---|---|
| LQM | dose | 0.8843 | 0.844 ± 0.032 | 0.0959 | 0.117 ± 0.012 | ✔ Reproduced |
| LocReg | dose | 0.8986 | 0.832 ± 0.035 | 0.0921 | 0.121 ± 0.011 | ✔ Reproduced |
| RF | dose + LET | 0.9685 | 0.939 ± 0.016 | 0.0196 | 0.073 ± 0.011 | △ R² reproduced, RMSE magnitude did not (see failure_analysis.md) |

## What is (and isn't) reproducible from these artifacts
- ✅ Reproducible **now, from clean clone**: the full pipeline (build_dataset → run_pipeline → make_figure) and the qualitative headline claim (LET-inclusive RF beats dose-only LQM/LocReg).
- ❌ NOT reproducible: exact paper numbers, because the GSI PIDE NB1RGB subset is email-gated. See `failure_analysis.md`.
- ❌ NOT reproducible from paper: **no code was released** by Debreceni et al. This replication is a re-implementation from prose.

## Compliance
- All LLM calls (judge + this backfill) used free Argo endpoints only.
- No sims were re-run in this backfill (HARD REQUIREMENT).
- All pre-existing files preserved; only new artifacts added.
