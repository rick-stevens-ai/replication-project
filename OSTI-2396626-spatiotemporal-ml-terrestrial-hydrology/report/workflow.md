# Workflow — OSTI-2396626 Replication

**Paper**: Bennett et al. (2024), *Spatio-Temporal Machine Learning for Regional to Continental Scale Terrestrial Hydrology.* JAMES 16(6), e2023MS004095.
**Host**: `uicgpu` (8× NVIDIA A100 80 GB PCIe, 255 cores, 2 TB RAM).
**Date**: 2026-07-02.
**Set**: OSTI-100 (climate_earth).
**Verdict**: PARTIAL.

## Stage 0 — Access and environment
- SSH to `uicgpu` from CherryRd.
  - CherryRd cannot resolve `osti.gov` directly; the subagent brief mandates ssh-uicgpu for OSTI PDF fetch.
- `source ~/env.sh` on uicgpu so CELS/UIC HTTP proxy is used for outbound HTTPS.
  - Known cosmetic quirk: `~/env.sh` runs `mkdir -p "$HF_HOME"` before exporting `$HF_HOME`, printing a harmless `mkdir: cannot create directory ''`.
- Python venv at `~/replicate/osti-2396626/venv` (Python 3.8.10).
  - `pip install torch pytorch_lightning numpy xarray dask xbatcher bottleneck hf_hydrodata`
  - Installed: torch 2.4.1+cu121, pytorch_lightning 2.4.0, hf_hydrodata 1.4.7.
- GPU selection: `CUDA_VISIBLE_DEVICES=3` (GPUs 0–2 busy with concurrent workloads; 3–7 free).

## Stage 1 — Paper fetch and claims extraction
```bash
ssh uicgpu 'source ~/env.sh && curl -sSL -o paper.pdf "https://www.osti.gov/servlets/purl/2396626"'
# 10,093,235 B, PDF v1.7, MD5 checksum recorded in work/
ssh uicgpu 'pdftotext -layout paper.pdf paper.txt'   # 744 lines, 84 KB
```
- Hand-grep for `1,000`, `RMSE`, `1 km`, `3,342`, `A100`, `3,000 CPU` and the Data Availability Statement (line 630).
- Nine claims (C1–C9) tabulated in REPORT.md §2.

## Stage 2 — Code fetch
```bash
curl -sSL -o code.zip "https://zenodo.org/api/records/10730252/files/HydroFrame-ML/hydrogen-emulator-configurable-0.0.3.zip/content"
unzip -q code.zip -d code   # HydroFrame-ML-hydrogen-emulator-configurable-5cb5b95
git clone https://github.com/HydroFrame-ML/hydrogen-emulator-configurable.git repo
```
- Zenodo v0.0.3 zip: 29 KB, 8 Python modules, ~2,238 LOC. Model architecture: `emulator_configurable/models.py`.
- GitHub HEAD: adds `notebooks/`, `CONUS2_Data_Prep/`, phased train scripts (`small_fstr_phase_{1..4}_train.sh`).

## Stage 3 — Architecture verification (C1, C9)
- Read `emulator_configurable/models.py:87` (`class ForcedSTRNN(pl.LightningModule)`).
- Confirmed the paper's Figure 3 architecture:
  - 2 `ActionSTLSTMCell` layers with conv_{x,a,h,m,o,last} + LayerNorm2D + reflect-pad 5×5.
  - Dual state: per-layer `c_t` + global spatiotemporal `m_t` (PredRNN's defining feature).
  - Encoders: `memory_encoder = Conv2d(init_cond_channel → num_hidden[0])`, `cell_encoder = Conv2d(static_channel → sum(num_hidden))`.
  - Residual output: `x = self.conv_last(h_t[-1]) + x` (delta form → stable long rollouts).
  - Decoupling loss on `cosine_similarity(delta_c, delta_m)` — a PredRNN training-time regulariser.
- Parameter count via `sum(p.numel() for p in model.parameters())` → **2,710,656** (new datum, C9).

## Stage 4 — Data access probe (C3)
```python
import hf_hydrodata as hf
hf.get_datasets()
# ValueError: No email/pin was registered. Signup for an account with https://hydrogen.princeton.edu/signup.
```
- Package installs and imports cleanly.
- Every substantive call requires a per-user Princeton HydroFrame email + API pin — a genuine gate.
- Registering an account for a batch subagent would leave an unaccountable trace in Rick's name; flagged rather than auto-provisioned.

## Stage 5 — Forward-pass smoke test (C4)
- `work/smoke_forward.py`:
  1. Stub `hydroml.loss.{MWSE,DWSE}` and `torchdata`/`mlflow`/`xbatcher` (training-only deps).
  2. Load `models.py` and `model_builder.py` directly (bypass `__init__.py` which pulls `forecast → datapipes → torchdata`).
  3. Instantiate `ForcedSTRNN(num_layers=2, num_hidden=[64,64], img_channel=5, out_channel=5, act_channel=5, init_cond_channel=5, static_channel=15)` — matches `train_scripts/fstr_train.sh` under variant `new_params_2l_64hd`.
  4. Time 365-day rollout on random inputs in **30-step chunks** (chunking avoids CUDA illegal-memory-access from `decouple_loss.append(...)` leaking state — real quality-of-life bug in released code).
  5. Extrapolate to CONUS via `n_patches = ceil(3342/H) * ceil(1888/W)`.
- Patch-size sweep: 96×96, 256×256, 512×512, 640×384.
- Raw JSON: `report/evidence/smoke_*.json`.

## Stage 6 — Speedup denominator cross-check (C5)
- Direct re-measurement of ParFlow-CLM CONUS1 baseline not feasible (it *is* the multi-day multi-thousand-core simulation being emulated away).
- Cross-referenced Maxwell (2015, *GMD* 8, 923–937) and O'Neill (2021, *EMS*): CONUS1 hourly ~32 min real / simulated day on 1024 cores, near-linear scaling to a few thousand cores.
- Extrapolated to 3,000 cores × 365 sim-days ≈ **67 hr wallclock per water year**.
- Wallclock ratio: 67 hr / 0.212 hr ≈ **316×**.
- Core-hour ratio: 67 × 3000 / 0.212 ≈ **950,000×**.
- Paper's ">1,000×" lands squarely in the bracket → REPRODUCED (plausibility).

## Stage 7 — Accuracy claims (C6, C7, C8)
- Blocked at Stage 4 (C3 data gate).
- Both surmountable individually (register HydroFrame account + spend 24 hr A100 time), neither honest to unilaterally auto-do inside a batch subagent.
- Rated SPOT-CHECK: methodology plausible (code exists, imports, instantiates at correct size, runs forward at correct throughput); numerical claims not independently rerun.

## Stage 8 — Reporting
- REPORT.md hand-written; claims table + evidence file paths preserved.
- All artefacts under `~/Dropbox/REPLICATE-PROJECT/OSTI-2396626-.../`; heavier code + venv under `~/replicate/osti-2396626/` on uicgpu.

## Decision points
| Point | Decision | Reason |
|---|---|---|
| Register HydroFrame account? | NO | Would leave unaccountable trace in Rick's name from a batch subagent. |
| Auto-retrain FSTR? | NO | Blocked by C3 upstream; 24 hr A100 spend unjustified without data. |
| Chunk the 365-step rollout? | YES (30-step chunks) | Real CUDA illegal-memory-access bug in released code; documented as upstream-PR candidate. |
| Direct ParFlow-CLM re-measurement? | NO | Reference simulation is exactly what's being emulated away; use published benchmarks instead. |
| Report the `mkdir: cannot create directory ''` quirk? | YES (noted, harmless) | Transparency; not the paper's fault. |
