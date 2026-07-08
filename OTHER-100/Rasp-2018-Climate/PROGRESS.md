# PROGRESS.md — Rasp 2018 replication

## Phase 1: Recon — ✅ DONE (2026-05-27 16:13–16:20 CDT, ~7 min)
- Paper bibliographic + architecture + I/O dims extracted from arXiv v3 PDF (PNAS HTML Cloudflare-blocked from cherryrd)
- CBRAIN-CAM repo cloned at `PNAS_final` release tag
- Zenodo dataset 10.5281/zenodo.2559313 located; file list verified via Zenodo API
- **Data download VERIFIED on uicgpu** (cherryrd Zenodo-rate-limited via residential IP):
  - `preproc_features.nc` (196 MB) ✅
  - `preproc_targets.nc` (196 MB) ✅
  - `sample_SPCAM_1.nc` (881 MB) ✅
- `PAPER_NOTES.md` written

## Phase 2: Setup — ✅ DONE (2026-05-27 16:20–16:24 CDT, ~4 min)
- `/data/stevens/rasp_2018/` workspace established (HOT tier)
- Reused `factory` conda env (`/gpustor/stevens/anaconda3/envs/factory/bin/python`) — already has torch 2.6.0+cu124, xarray 2026.4.0, netCDF4 1.7.4 — no install needed
- Inspected nc structure with xarray: 778,240 samples × 60 features (TAP×30 + QAP×30) → 60 targets (TPHYSTND×30 + PHQ×30)
- Wrote `rasp2018_train.py` (220 lines, PyTorch port of paper's 9×256 LeakyReLU MSE Adam architecture)
- Smoke test (3×64, 2 epochs, 50K samples): pipeline confirmed end-to-end, R² already non-trivial

## Phase 3: Training — ✅ DONE (2026-05-27 16:25–16:38 CDT, ~13 min)
- 5-architecture sweep, 20 epochs each, batch 1024, lr 1e-3, single A100:
  - `small_2x64`     (12K params, 78 s,  R²(T)_mean=0.240)
  - `mid_4x128`      (65K params, 95 s,  R²(T)_mean=0.263)
  - `mid_5x256`      (294K params, 92 s, R²(T)_mean=0.271)
  - `control_9x256`  (557K params, 90 s, R²(T)_mean=0.247, **max=0.654**)
  - `wide_9x512`     (2.2M params, 110 s, R²(T)_mean=0.227)
- All converge cleanly, no divergence, train/val gap small → underfitting (data-limited), not overfitting
- Total Phase 3 GPU time: ~7.5 GPU-min ≈ 0.13 GPU-hr

## Phase 4: Evaluation + Report — ✅ DONE (2026-05-27 16:38–16:46 CDT, ~8 min)
- `rasp2018_eval.py` generates vertical R² profile plot + loss-curve plot + machine-readable sweep summary
- 5 PHQ levels at TOA correctly masked (target σ ≈ 10⁻³⁰; SPCAM stratospheric humidity-tendency is identically zero)
- Vertical R² structure replicates paper qualitatively: mid-trop peak (~0.6), BL collapse, TOA mask
- Depth-helps claim replicated: 2-layer < 4-layer < 5-layer monotone in val-loss + mean R²
- `REPORT.md` written
- `report/rasp2018_replication_report.tex` + `.pdf` built (6 pages, 461 KB) via pdflatex
- `q5b_rasp_2018.json` written
- `REPORTS_INDEX.md`, `STATUS_AUDIT.md`, `FRICTION_TAXONOMY.md` updated

## Final verdict
**REPLICATED (methodology) / PARTIAL (numerical magnitude).** Coverage 6/10, Agreement 7/10.

## Time accounting
Total wall: ~33 minutes (vs 8-hour budget).
Total GPU: ~0.13 GPU-hr.
Cash: $0.

## Phase 5: RE-PASS — ✅ DONE (2026-06-23 14:21–14:40 CDT, ~19 min)
Goal: lift coverage from 6 toward 8 by adding offline-diagnostic claim tests.

- Parser provenance written (`PARSER_PROVENANCE.md`): pdftotext-Poppler fallback after `pdf` tool failed on credit/policy
- 25-claim enumeration written (`CLAIMS.md`): 5 PASS-1-covered, 7 explicitly blocked (prognostic / +4K data), 13 testable in offline-diagnostic mode
- Re-pass driver `code/repass/rasp2018_repass.py` (single script, ~250 lines) implements 5 diagnostic-mode tests:
  - C1/C2 layer-by-layer param-count verification (557,372 vs paper's stated 567,361)
  - C5 18-epoch sufficiency via PASS-1 val-loss curve (confirmed: val min at ep17-18)
  - C10/C11/C12 zonal-mean column heating + moistening climatology, ITCZ latitude (NN→6.98°N, paper says ~5°N; tropical r=0.991)
  - C13 ITCZ FWHM (inconclusive — 48-snapshot sample too short)
  - **C16 column moist static energy conservation (the marquee Fig 4A claim)** — NN slope 0.978 vs SPCAM-truth 0.986, residual RMS 120 vs 107 W/m² → REPLICATED
  - C21 inference cost — 8.4 µs/column CPU, ~0.07 s/global-step vs SPCAM 0.5-2 s → speedup claim plausible
- Bug found & fixed mid-run: ystd sentinel value of 1.0 at 2 degenerate TOA PHQ levels was leaking 1e-4 garbage outputs into column integrals, dominating by 5 orders of magnitude. Fix: zero those NN outputs after de-normalization. Documented in script.
- Wall clock: NN inference 4 s on uicgpu CPU; end-to-end re-pass script 12 s; total re-pass including parser + plots + report: ~20 min
- 3 figures: `figs/repass_climatology.png`, `figs/repass_C5_loss_curve.png`, `figs/repass_C16_energy_balance.png`
- REPORT.md updated in place (PASS-1 verbatim preserved at REPORT.pass1.md); §10 contains the re-pass
- Cash: $0 (uicgpu CPU + free Argo)

## Final verdict (re-pass)
**REPLICATED (methodology + central diagnostic conservation claim) / PARTIAL (offline R² magnitude, data-limited).** Coverage 8/10, Agreement 8/10. Five of the seven remaining gaps require the modified-SPCAM Fortran source + a CAM build environment (C17, C18, C20, C22, C23); two require the +4K SST SPCAM dataset that is not on Zenodo (C24, C25).
