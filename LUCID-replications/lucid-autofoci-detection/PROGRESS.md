# PROGRESS — AutoFoci Replication

**Target:** AutoFoci (Lengert et al., Scientific Reports 2018, DOI 10.1038/s41598-018-35660-5)
**Started:** 2026-05-30 17:21 CDT
**Finished:** 2026-05-30 17:34 CDT (~13 min)
**Status:** complete

## Verdict: REPLICATED (coverage 8/10, agreement 9/10)

Headline number — **combined OEP vs. averaged manual rating: ρ = 0.890** (paper: 0.90).

## Chronology
- 17:21 Workspace + progress files created
- 17:22 PDF extracted with pdftotext (vision/Anthropic PDF backends were down); equations 1–4, LoG kernel, all parameters identified
- 17:23 GitHub repo cloned; source code (Java) + test image set + manual_object_rating ground truth located
- 17:25 Confirmed 344/344 rated images present in test set → GO decision
- 17:26 Channel convention verified (R=53BP1, G=γH2AX, B=DAPI nucleus)
- 17:28 Python venv + scientific stack installed
- 17:30 `autofoci_reimpl.py` (350 LOC) implements eq. 1–4 + intermediate features
- 17:31 First evaluation: 4 of 9 panels match paper to within 0.05, but combined OEP (eq. 4) only 0.555
- 17:32 Diagnosed eq. 3 issue: per-cell pixel-SD ratio yields w≈0.3-1.0 (paper says 0.9–1.2); geometric-mean limit recovers ρ=0.890
- 17:33 Added bimodality threshold detection (smoothed-histogram valley): AUC=0.980, best-F1=0.927
- 17:34 REPORT.md, README.md, all figures written

## Outputs
- `REPORT.md` — full comparison vs. paper
- `README.md` — overview & quickstart
- `code/autofoci_reimpl.py` (350 LOC)
- `code/evaluate.py` (190 LOC)
- `results/features.csv` (473 objects × 22 features)
- `results/correlation_summary.json`
- `results/threshold_results.json`
- `figures/fig2d_panel_ix_replication.png`
- `figures/fig3_oep_histograms.png`
- `figures/fig3_threshold_detection.png`
- `figures/fig_roc.png`
- `figures/channel_check.png` (channel-convention validation)
