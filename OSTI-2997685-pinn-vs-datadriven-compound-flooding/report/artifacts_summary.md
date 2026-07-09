# Artifacts summary — OSTI-2997685

## 1. Source paper
- `paper.pdf` — 5.77 MB, OSTI-2997685, https://www.osti.gov/servlets/purl/2997685
- DOI: 10.1029/2025JH000758 (JGR-MLC 2(4), e2025JH000758, 2025)

## 2. Extractions
| File | Size | Tool | Note |
|------|------|------|------|
| `extraction/marker.md` | 137 385 B (577 lines) | marker_single (`/data/stevens/envs/marker`) | markdown parse |
| `extraction/nougat.mmd` | 113 079 B (385 lines) | nougat (`/gpustor/stevens/anaconda3/envs/nougat`) | .mmd + tables |
| `extraction/pdftotext_raw.txt` | 165 843 B (1473 lines) | poppler pdftotext -layout | keeps column layout |

## 3. Author artifact bundle
- URL: https://api.figshare.com/v2/articles/28890083
- DOI: 10.6084/m9.figshare.28890083.v2 (Feng, 2025)
- Bundle: 295 files, 1.53 GB total
- Local copy: 212 small files + 3 PINN training logs in `work/figshare_code/` (17.3 MB)
- Full bundle staged on uicgpu at `/data/stevens/scratch/tmp/osti2997685/`

Key sub-artifacts in `work/figshare_code/`:
| Group | Files | Purpose |
|-------|-------|---------|
| PINN source | `SVE_module_dynamic_uh_mff_ts_l2_new.py` (33 kB), `..._FDM.py` (37 kB), `PINN_test_bnd_uh_Telemac{,_FDM,_FDM_backward}.py` | vanilla + FD PINN training + drivers |
| Data-driven training | `train_CNN.py`, `train_CNN_conv.py`, `train_CNN_LSTM.py`, `train_GRU.py`, `train_LSTM.py`, `train_UNet.py`, `train_UNet_tiny.py` | one per architecture |
| Data-driven predict | matching `predict_*.py` |  |
| Metrics tables | `PINN_metrics.csv`, `PINN_FDM_metrics.csv`, `PINN_FDM_backward_metrics.csv` | R^2, MSE, MAE, L2 by observational-noise level |
| Metrics (Irene) | `metrics_CNN_Irene.csv`, `metrics_CNN_conv_Irene.csv`, `metrics_CNN_LSTM_Irene.csv`, `metrics_GRU_Irene.csv`, `metrics_LSTM_Irene.csv`, `metrics_UNet_Irene.csv`, `metrics_UNet_tiny_Irene.csv` | Irene held-out event, Ne=100..800 |
| Timing | `time_CNN{,_conv,_LSTM}.csv`, `time_GRU.csv`, `time_LSTM.csv`, `time_UNet.csv` | wall-clock per Ne size |
| PINN logs | `PINN_uh_Telemac.out` (6.7 MB), `PINN_uh_Telemac_FDM.out` (4.6 MB), `PINN_uh_Telemac_FDM_backward.out` (4.6 MB) | contain `PINN Time elapsed:` ground truth for C1 |
| Per-Ne arrays | `CNN_Ne{100..800}_array.npy`, `CNN_time_Ne{100..800}_array.npy`, ...| raw per-sample metric arrays |
| Requirements | `requirement_tf1.txt` (PINN), `requirement_tf2.txt` (data-driven) | conda env specs |
| README | `README.md` (1.5 kB) | training/prediction instructions |

Large binaries staged on uicgpu only (not needed for numerical claim verification):
| Path | Size | Purpose |
|------|------|---------|
| `Telemac_output_ensemble_rp.nc` | 545 MB | training-ensemble reference solutions |
| `output_high.slf` | 142 MB | high-resolution Telemac hindcast |
| `DR_1D_5cells.p01.hdf` | 12 MB | HEC-RAS comparison output |
| `output_10days_hotstart.slf` | 36 MB | Telemac 10-day hotstart |
| `mesh_1D_channel_dx100.exo` / `mesh_1D_channel_dx100_update.slf` / `mesh_1D_channel_hourly.liq` | ~350 kB total | 1-D river mesh + BC |
| `PINN_uh_Telemac_*.pickle` / `PINN_uh_weights_*.out` / `PINN_uh_mff_*.out` | ~34 MB total across 6 noise x 3 variants | trained PINN weights, hopefully re-loadable |

## 4. Replication evidence
| File | Purpose |
|------|---------|
| `report/evidence/verified_claims.json` | Machine-readable summary of C1..C5 verification |
| `report/evidence/verify_output.txt` | Text dump of verify_claims.py stdout |
| `report/evidence/pinn_speedup.png` | Bar chart: vanilla vs FD vs FD-back PINN training time |
| `report/evidence/irene_r2_vs_samplesize.png` | Line plot: Irene R^2 vs training-ensemble size for six data-driven models, with PINN and FD-PINN reference lines |

## 5. Verification script
- `work/verify_claims.py` (~150 LOC) — parses `.out` logs, computes speedup, parses `metrics_*.csv`
  for R^2 rankings and sequence-aware means. Idempotent, no GPU needed.

## 6. Meta
- `work/figshare_meta.json` — full Figshare API response (all 295 file records with md5, size, url).
- `attempt_log.md` — chronological run log.

## 7. Provenance
| Origin | Files | How obtained |
|--------|-------|--------------|
| OSTI | `paper.pdf` | `curl https://www.osti.gov/servlets/purl/2997685` |
| Figshare | 215 code + metrics + log files | Figshare v2 API |
| self | verification driver + 2 regenerated plots | Python 3.13 + numpy + matplotlib |
| uicgpu (marker env) | `extraction/marker.md` | marker_single, disable-image-extraction |
| uicgpu (nougat env) | `extraction/nougat.mmd` | nougat default model 0.1.0-small |
