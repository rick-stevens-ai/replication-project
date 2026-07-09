# Artifacts Summary — AutoFoci Replication

**Paper:** Lengert et al., *Sci. Rep.* **8**:17282 (2018). DOI 10.1038/s41598-018-35660-5.
**Repo:** https://github.com/nleng/AutoFoci (GPL, Java).

## Top-level

| File | Size | Purpose |
|---|---:|---|
| `README.md` | 3 027 B | Overview + quickstart |
| `REPORT.md` | 9 661 B | Original narrative report (paper vs. ours, verdict, tables) |
| `PROGRESS.md` | 1 848 B | Chronology of the 13-minute original run |
| `paper.pdf` | 2 425 148 B | Backfilled 2026-07-06 from https://www.nature.com/articles/s41598-018-35660-5.pdf. sha256 `f9511a7ad59b62c49f303173daa274197c1e4b13e8a90b60e7d35c9655c99c89` |

## `code/`

| File | Size | Purpose |
|---|---:|---|
| `autofoci_reimpl.py` | 15 677 B | Python reimplementation of eqs. 1–4 + all intermediate features per object per channel |
| `evaluate.py` | 7 966 B | Panel-by-panel Spearman ρ, inter-rater agreement, ROC/AUC, bimodality/threshold, figures |

## `results/`

| File | Size | Content |
|---|---:|---|
| `features.csv` | 154 486 B | 473 objects × 22 feature columns (per-channel mean intensity, top-hat, LoG, compactness, OEP variants, ratings) |
| `correlation_summary.json` | 2 291 B | All 9+1 panel Spearman ρ values, inter-experimenter matrix, paper values, deltas |
| `threshold_results.json` | 605 B | Peaks, valley threshold, F1-optimal threshold, confusion matrices, AUC=0.9802, AP=0.9777 |

## `figures/`

| File | Size | Reproduces |
|---|---:|---|
| `channel_check.png` | 80 854 B | R=53BP1 / G=γH2AX / B=DAPI channel-convention validation on a random test image |
| `fig2d_panel_ix_replication.png` | 93 078 B | Paper Fig. 2d panel ix: combined OEP vs. averaged manual rating (ρ = 0.890 vs. paper 0.90) |
| `fig3_oep_histograms.png` | 48 353 B | Paper Fig. 3a/3b: background vs. foci log₁₀(OEP) histograms |
| `fig3_threshold_detection.png` | 75 259 B | Smoothed-histogram valley-finder overlay; auto-threshold @ log₁₀(OEP) ≈ 3.74 |
| `fig_roc.png` | 33 505 B | OEP-as-classifier ROC, AUC = 0.980 |
| `preview_page0.png` | 46 224 B | First-page preview of the source PDF (from pdftotext staging) |

## `report/` (backfill, 2026-07-06)

| File | Size | Purpose |
|---|---:|---|
| `REPORT.tex` | ~19 KB | Detailed LaTeX report with paper summary, claims table, method, results tables, per-claim what-worked/what-didn't, critique, verdict, Open Questions Q1–Q5 |
| `open_questions.json` | ~7 KB | 5 truly-open questions with basis + concrete next_steps (canonical machine-readable rollup source) |
| `workflow.md` | ~7 KB | Comprehensive workflow narrative + tools + versions + LOC + compute estimate |
| `artifacts_summary.md` | this file | Inventory + traces |
| `failure_analysis.md` | ~7 KB | Honest failure analysis + evidence-strength critique |

## `extraction/` (backfill, 2026-07-06)

| File | Purpose |
|---|---|
| `marker.md` | 76 349 B — `pdftotext -layout` extraction of backfilled `paper.pdf`. Not equation-clean but preserves section text, tables, captions. Used as paper re-read source for open questions. |
| `nougat.mmd` | Stub (1 524 B) — GPU Nougat parse pending. Contains paper.pdf sha256 pointer for the future central corpus sweep. |

## `repo/` (external, cloned from https://github.com/nleng/AutoFoci)

| Path | Purpose |
|---|---|
| `AutoFoci/AutoFoci.jar` | Compiled AutoFoci binary (NOT executed during replication — reimpl. was independent) |
| `AutoFoci/src/` | Java source (used only for LoG kernel + inertia disk radius cross-check) |
| `AutoFoci/manual_object_rating.7z` → `manual_data/…/Manual_object_rating_results.xlsx` | Ground truth: 473 objects × 3 raters × 1–9 quality score |
| `AutoFoci/Test_Images_AutoFoci.7z` → `test_images/Test_images_AutoFoci/*.tif` | 804 single-cell TIFFs; we used the 344 with rated objects |
| `AutoFoci/Guidance_to_count_foci_using_AutoFoci.pdf` | User guide (not the paper) |
| `ImageJ/` | Companion ImageJ macros (Cellect pre-processing) — not exercised |
| `ImageJ/Guidance_to_process_images_using_Cellect.pdf` | Cellect user guide (not the paper) |
| `LICENSE` | GPL |
| `README.md` | Upstream README |

## External accessions / URLs

| Item | Locator |
|---|---|
| Paper | https://doi.org/10.1038/s41598-018-35660-5 (Sci. Rep. 8:17282, 2018) |
| Preprint | None (Scientific Reports is not preprinted) |
| Software repo | https://github.com/nleng/AutoFoci (last commit 2018-era, GPL) |
| Ground-truth dataset | Embedded in the same GitHub repo (manual_object_rating.7z) |
| Test image dataset | Embedded in the same GitHub repo (Test_Images_AutoFoci.7z) |

## Provenance / integrity

- No author contact was made.
- No paid endpoints were used.
- AutoFoci.jar was never executed.
- All figures were regenerated from `results/features.csv` by `code/evaluate.py`; the raw features CSV is the single source of truth for every downstream number in the report.
- Backfill (2026-07-06) added items 4–8 without touching any pre-existing file. The original REPORT.md, README.md, PROGRESS.md, code/, figures/, results/, and repo/ are byte-identical to the 2026-05-30 run.
