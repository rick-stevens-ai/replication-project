# Attempt Log — OSTI 3019881 (CNN-LSTM Norfolk Flood Surrogate)

## 2026-07-02 08:07 CDT — Setup
- Created target dir with report/ + work/ subdirs.
- Attempted `curl` to `https://www.osti.gov/servlets/purl/3019881` from CherryRd — **blocked** (TCP timeout to 192.107.175.222:443). CherryRd home network can't reach osti.gov directly.
- Fallback: fetched via `ssh uicgpu` (proxy internet via `~/env.sh`). ~6.36 MB PDF, MD5 `3fbb8ac27086c58b270ee559d9429738`. Copied to `work/paper.pdf`.

## 08:11 — Paper extraction
- `pdftotext -layout paper.pdf paper.txt` → 946 lines, clean.
- Skipped the `pdf` LLM tool: routes to paid Anthropic/OpenAI (forbidden by FREE-only rule) and returned billing error.
- Grepped for data availability + code: **HydroShare** resource `43244f815e7947e6bac6b6705a9f7941` (Wang 2025). Contains "CNN-LSTM coastal urban flood dataset and source code."
- No GitHub link explicitly given; HydroShare is the canonical release.

## Key paper facts extracted
- Wang, Goodall, Kumar, McSpadden, Barbosa, Roy, Shahabi, Tahvildari — J. Hydrology: Regional Studies 64:103234 (2026).
- Task: surrogate for TUFLOW 2D/1D hydrodynamic model, Norfolk VA, 2.5-m spatial, 15-min temporal, +1 h horizon.
- Architecture: DeepLabv3+ encoder-decoder CNN (spatial: DEM, TWI, past water depth) + LSTM (temporal: rainfall, tide) fused at bottleneck.
- Inputs: 8 past + 4 future timesteps (12 total). 12 AOIs of 128×128 px each.
- Training: Adam, lr=1e-4, MSE loss, batch=4, 200 max epochs, early stop patience=20 min_delta=1e-7, dropout=0.2. K80 GPU, Python 3.10.
- Split: 80/20 train/test.
- **Headline results (Table 5)**: avg MAE 0.024 m, MSE 0.0020 m², RMSE 0.044 m across 12 AOIs. Best RMSE 0.033 m (AOI 4), worst 0.063 m (AOI 7).
- Runtime speedup: TUFLOW 4-6 hours → CNN-LSTM 3.2 min per event.

## 08:14 — HydroShare artifact resolution
- Queried `hsapi/resource/43244f815e7947e6bac6b6705a9f7941/scimeta/` → confirmed public CC BY release by Yidi Wang (UVA).
- Queried `hsapi/resource/43244f815e7947e6bac6b6705a9f7941/files/` → **one** file: `Example Dataset.zip` (108,663,214 B).
- Downloaded to `uicgpu:~/replicate/osti_3019881/work/example_dataset.zip`. MD5 `9bb7a12f1ae2819c2f035bcb198c540c`.
- Unzip: 600 `.npy` files (300 input, 300 output) across 2 events (Aug 29 2017, Sep 30 2022). **No `.py`/`.ipynb`/`.md`/`.txt`** — the "and Source Code" in the HS title is not honored by the released bundle.

## 08:15 — Data inspection
- `input/*.npy` shape (128,128,11) float64 → decoded as [DEM, TWI, past_WD × 8, forcing].
- `output/*.npy` shape (128,128,4) float32 → t+1..t+4 water depth (m).
- 150 samples per event, 15-min stride, matches Table 3 window (8 past + 4 future).

## 08:16 — Model + smoke
- Reconstructed DeepLabv3+ encoder-decoder + LSTM head + upsample decoder from paper description (9.34 M params).
- Smoke: 1 epoch on GPU 3 → 4 s/epoch, val_mse 0.0042. Sanity check passed.

## 08:16–08:24 — Main run seed 42 (GPU 3)
- Full 200 epochs, best_epoch=198, best_val_mse=0.000363, overall test MAE=0.0048 m / MSE=0.00036 / RMSE=0.0191 m.
- Per-future-step RMSE monotone: 0.0186 → 0.0203 m (t+1 → t+4). Matches paper Fig. 5 qualitative pattern.

## 08:26–08:27 — Repeat run seed 7 aborted
- Seed 7 sat at identical loss for 6 epochs (dead-init); killed at 24 s.

## 08:27–08:28 — Repeat run seed 123 (early-stop failure)
- Ran to completion but early-stopped at epoch 1 with val_mse stuck at 0.00432 → dead-init failure mode. Kept as evidence of the seed sensitivity.

## 08:29–08:39 — Repeat runs seeds 1 + 99 (GPUs 4 + 5, parallel)
- Seed 1: best_epoch=156, MAE=0.0040 / RMSE=0.0163 m.
- Seed 99: best_epoch=195, MAE=0.0045 / RMSE=0.0189 m.
- Both reproduce the monotone-in-horizon RMSE growth.

## 08:40 — Verdict
- PARTIAL: released data is real and reproduces same-order errors + qualitative claims, but bundle covers only 2 of 12 AOIs so exact Table 5 per-AOI numbers cannot be re-verified, and no source code was shipped despite the resource title.
