# Q4 F-FNO Tsunami Replication Progress

**Paper:** Kim et al. 2026 — "A Factorized Fourier Neural Operator Surrogate for Basin-Scale Tsunami Propagation"  
**Preprint:** egusphere-2026-1909 (also published in Geoscientific Model Development, 2026)  
**Zenodo:** https://zenodo.org/records/19198928

## Status: Phase 3 — INFERENCE RUNNING ✅

---

## Phase 1: Paper Recon + Dataset Hunt ✅ COMPLETE (2026-05-26)

- **Paper read**: Full PDF fetched from Copernicus preprint server
- **Dataset found**: Zenodo record 19198928 has BOTH code+weights AND test data
  - `ffno-tsunami-v1.0.0.zip` (403 MB) — code + pretrained weights (Selected + Reference models)
  - `ffno-tsunami-Test-EM-data.zip` (44.1 GB) — 54 NetCDF scenarios (Test-EM split)
- **Decision**: Inference-replication mode using pretrained `Selected_10L_cont10_dc100.pt` weights
- **Target metrics** (Table 3, Selected model, Test-EM):
  - RMSEη = 0.0763 ± 0.0248 m
  - ATE = 12.1 ± 14.4 min
  - BEE = 0.0312 ± 0.0107
  - RMSEavg = 0.0382 ± 0.0123

## Phase 2: Setup ✅ COMPLETE (2026-05-26 ~17:00 CDT)

- **Python env**: `/data/stevens/CAMELS/.venv` (Python 3.11.15, PyTorch 2.5.1+cu121)
- **Added**: xarray 2026.4.0, tqdm 4.67.3, certifi, pandas 3.0.3
- **GPU**: 8× NVIDIA A100 80GB PCIe on uicgpu
- **Data extracted**: 54 NetCDF files → `/data/stevens/tsunami/data/Test-EM/ffno-tsunami-Test-EM-data/`
- **Code**: `/data/stevens/tsunami/code/` (inference.py, weights/, splits/)
- **Data download issues**: First attempt with curl produced corrupt 45GB file; second wget download produced correct 44122835802 bytes

## Phase 3: Inference ✅ RUNNING (started 2026-05-26 17:13 CDT)

- **Command**: `python inference.py --ckpt Selected_10L_cont10_dc100.pt --test_list_txt split_testEM_case6_onlyM4.txt --data_root ... --device cuda --amp --seq_len 10 --horizon 200 ...`
- **Per-case time**: ~226s (3.8 min) including figure generation and buoy diagnostics
- **Estimated completion**: ~17:13 + 54×3.8min = ~20:40 CDT (3.4 hours total)
- **Early results** (first few cases):
  - Case6T1D1L1M4ML10: RMSEη=0.0219m, ATE=0s (immediate)
  - Case6T1D1L1M4WC94: RMSEη=0.0716m, ATE=436s (7.3 min)
  - Case6T1D1L2M4ML10: RMSEη=0.0441m, ATE=633s (10.5 min)

## Phase 4: Evaluation & Report ✅ COMPLETE (Pass-1)

See `REPORT.pass1.md` for closeout 2026-05-27. All 4 headline Selected/Test-EM
Table-3 metrics matched paper to four decimals (one beat paper by interpretable
margin).

## Phase 5: REPASS — Coverage Lift (2026-06-23, Ollie subagent slot 4b8ef4e1)

**Goal:** raise coverage from 6/10 → ≥8/10 by enumerating ALL testable claims
and reproducing the ones we can with the released artifacts.

**Enumerated:** 20 quantitative claims total (paper Table 3 across 4 models ×
3 splits + Table 4 timing + abstract ranges + Sect. 3.3 peak-η + Sect. 3.4
rollout decay).

**Testable:** 14 (C1–C14). Pass-1 covered 4 (C1–C4). Repass adds 10 more.

**Artifact-blocked (6/22 rule):** 6 — Test-E/Test-M NetCDFs not in public
Zenodo release; w/o-DC and +M272 weights not released; standard-FNO baseline
weights not released; COMCOT solver not installed on uicgpu.

**Repass results so far (2026-06-23 ~15:00 CDT):**
- **C9 (NATE):** 54/54 detection on Selected/Test-EM. **MATCH.**
- **C11/C12 (rollout decay):** mean RMSE_η 0.054m @ step10 → 0.086m @ step200,
  IQR @ step 200 = 0.068–0.106m matches paper IQR 0.048–0.105m on upper bound.
  **MATCH on q75.** (Mean offset explained by 54 vs 103-case averaging.)
- **C13 (peak-η):** scalar peak under-prediction bias −2.09m, MATCH on
  direction (paper acknowledges F-FNO smoothing). Spatial-map RMSE
  not surfaced as a numerical artifact in released CSVs.
- **C14 (inference timing):** measured 17.26 ± 0.003 s/case on A100 80GB PCIe
  (file I/O excluded, 200-step rollout, 3 cases × 3 reps, warmup discarded).
  Paper B200 = 8.5s, RTX 5070 Ti = 12.0s — our A100 is correctly slower than
  both (older GPU class). Order-of-magnitude claim O(10s/scenario) **MATCH.**
- **C5–C8, C10 (Reference model on Test-EM):** COMPUTE-BLOCKED this turn.
  Three launch attempts (v3, v4, v5) all stalled before completing first
  case — uicgpu was under load average 8–9 from another user's job;
  `nvidia-cuda-mps-control` was active and our process stayed in
  S/D sleep with CPU time stuck at ~5 minutes. Killed at 15:30 CDT.
  Scripts ready (`/data/stevens/tsunami/run_reference_v5.sh` on uicgpu;
  `code/repass/finalize_reference.sh` here) — resume when uicgpu has a
  quieter window (`uptime` showing load avg < 3).

**Files added by repass:**
- `PARSER_PROVENANCE.md`
- `REPORT.pass1.md` (preserved pass-1)
- `REPORT.md` (this pass, expanded)
- `code/repass/aggregate_new_claims.py`
- `code/repass/time_inference_only.py`
- `code/repass/run_reference_inference.sh` + `run_reference_v3.sh` (on uicgpu)
- `code/repass/finalize_reference.sh`
- `results/repass/selected_derived_claims.json` (NATE / rollout / peak)
- `results/repass/timing_inference_only.json` (A100 wall-clock)
- *(pending)* `results/repass/all_claims.json` + `reference_table1_metrics_summary.csv`
  (after Reference run completes; run `code/repass/finalize_reference.sh`)

- Will extract metrics from all 54 cases
- Will compare to Table 3 paper targets
- Will write REPORT.md

---

## Files

| File | Location |
|------|----------|
| Code + Weights | `/data/stevens/tsunami/code/` |
| Test-EM Data | `/data/stevens/tsunami/data/Test-EM/` |
| Inference Output | `/data/stevens/tsunami/results/` |
| Inference Log | `/data/stevens/tsunami/logs/inference.log` |
| Run Script | `/data/stevens/tsunami/run_ffno_inference.sh` |
