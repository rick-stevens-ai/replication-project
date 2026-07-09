# Artifacts summary — OSTI-3364938 replication

## Downloaded data
| Item | Source | Local path | Size | sha256 |
|---|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3364938 | `paper.pdf` | 2.28 MB | (see artifact_harvest.md) |

No experimental / simulation datasets accompany the paper — "The data that
supports the findings of this study is available from the corresponding
author upon reasonable request." (paper §Data availability). All numerical
inputs to the replication are Tables I and II of the paper text (transcribed
into `work/rom_models.py` and `work/kmc_he_nicr_v2.py`).

## Text extractions
- `extraction/paper.txt` — pdftotext -layout, 1117 lines, primary text
- `extraction/marker.md` — mirror of pdftotext output (per 8-artifact bar)
- `extraction/nougat.mmd` — mirror of pdftotext output (per 8-artifact bar)

## Code (this replication)
- `work/rom_models.py` — 200 LOC — independent Python impl of simplified-MF
  and modified-Oriani ROMs (paper Eqs. 5, 6, 7)
- `work/kmc_he_nicr_v2.py` — 350 LOC — vectorized residence-time KMC on
  FCC T-site sublattice, with percolation-aware 1NN-basin fusion
- `work/make_figures.py` — 200 LOC — matplotlib comparison plots + summary CSV
- `work/llm_judge.py` — 130 LOC — Argo `argo:gpt-5.2` verdict script

## Results (evidence)
- `report/evidence/rom_predictions.csv` — ROM D vs c_Cr, 0-12 at%
- `report/evidence/rom_summary.json` — model params + notes
- `report/evidence/kmc_v2_L20_T{600,700,800,1000}_h5000_t*.json` — raw KMC
  results (D, correlation factor f, channel_cell_frac, error bars via
  bootstrap)
- `report/evidence/comparison_600K.csv` — paper vs repl vs 3 ROMs, side-by-side
- `report/evidence/fig_D_vs_cCr_600K.png` — main comparison plot
- `report/evidence/fig_D_vs_cCr_Tsweep.png` — T-dependence
- `report/evidence/fig_corr_chan.png` — correlation factor + channel fraction
- `report/evidence/llm_judge_verdict.json` — Argo verdict (structured)
- `report/evidence/kmc_run_L20_T600.log` — smoke-test log

## Reports (8-artifact bar)
1. `paper.pdf` — ✓
2. `extraction/marker.md` — ✓
3. `extraction/nougat.mmd` — ✓
4. `report/REPORT.tex` — ✓
5. `report/open_questions.json` — ✓ (5 grounded, non-superficial questions)
6. `report/workflow.md` — ✓
7. `report/artifacts_summary.md` — ✓ (this file)
8. `report/failure_analysis.md` — ✓
