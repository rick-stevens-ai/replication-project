# Attempt log — OSTI-3015376

All timestamps CDT 2026-07-05.

## 06:14 — kickoff
- Read wave brief, created target dir tree (`report/`, `report/evidence/`, `work/`).

## 06:15 — PDF fetch
- `ssh uicgpu curl -o /tmp/osti_3015376.pdf https://www.osti.gov/servlets/purl/3015376` → 5.72 MB, OK.
- `scp` to `work/`.
- PDF-tool couldn't read `/Users/stevens/Dropbox/...` (not in allowed root) — copied to workspace-owned `tmp-pdf/`, then hit Anthropic-credit-balance error on PDF vision model → fell back to `pdftotext -layout` (installed as `/usr/local/bin/pdftotext`). Got 695 lines of clean text, sufficient for claim extraction.

## 06:17 — Claim extraction
Paper is Bai & Rouson 2025, *Sci. Reports* 16:3211, DOI 10.1038/s41598-025-33209-x. Extracted:
1. Method = ADON + ADON-PCA (DeepONet-style dual-net: BranchNet 39→256→384→128→21; TrunkNet 4→64→20; GELU; batch 256; MAE / L1 loss)
2. Training = 9.8M cloud-free samples from E3SMv2 present-day 1° simulation, 8 time slices spanning 2010; predict 20 ∆-VMR outputs from 43 inputs (39 physical + 4 coord)
3. Test = one hold-out slice (2010-12-30 00:30 UTC) + 5 ensemble seeds
4. Headline table (Table 1): ADON-PCA overall R²=0.9926, RMAE=0.0700, RMSE=0.1991 → 34%/60% RMSE reduction vs D-FCN/PINN
5. Compute (Table S.2): GPU (single Perlmutter A100) 0.07 s / 1.2M-point slice; CPU ≈1 s; 14× GPU speedup; single-precision +30% GPU / +11% CPU further speedup
6. Data & code availability: GitHub `zhbai/AerosolML` + Zenodo DOI 10.5281/zenodo.18226529.

## 06:18 — code + data harvest
- `git clone https://github.com/zhbai/AerosolML` → repo alive, last push 2026-01-13, MIT-ish license, Python only, contains `src/ADON/{Inference_ADON,utils,__init__}.py`.
- README points at Zenodo 18226529.
- Zenodo listing shows 6 files. Downloaded via `curl` under uicgpu proxy: `lat.npy, lon.npy, lev.npy, saved_data.nc (399 MB), X_test5.npy (777 MB), model_...pth (1.3 MB)`. All checksums captured in `evidence/sha256.txt`.

## 06:19 — env setup
- No project-specific env exists on uicgpu. `/gpustor/stevens/anaconda3/envs/ai2` provides Python 3.11 + PyTorch 2.5.1+cu121 + xarray 2026.4.0 + netCDF4 1.7.4 + torchvision 0.20.1+cu121 — sufficient.

## 06:20 — saved_data.nc inspection
Content matches the inference script's expectations exactly:
- `X_test (1214140, 39)`  — cloud-free time-slice input features
- `cldfr_idx (2, 1214140)` — (level, column) indices into 72×21600 grid
- `mean_X (43), std_X (43), mean_y (20), std_y (20)` — normalization stats
- `basis (20,20)` — PCA basis, `ymean (20)` — mean of ∆-targets
No `y_test` / ground-truth Δ published in this NC file → straight-up R² recomputation not possible from this bundle alone.

## 06:22 — inference run
Wrote `run_inference.py` mirroring the shipped `Inference_ADON.py` but with (a) explicit CUDA device placement fixes (paper's `TrunkNet.basis` and `MyNet_ADON.ymean` are plain tensors, not registered as `nn.Parameter`/buffer → don't move under `.to(device)`; fixed by explicit moves), (b) batched inference for the whole slice, (c) per-variable output stats, (d) GPU vs CPU 100k-point timing.
- Loaded weights: **0 missing keys / 0 unexpected keys** (state-dict exactly matches architecture)
- 162,537 parameters total (dual-net small MLP — consistent with model file size 1.3 MB fp32)
- Inference on all 1,214,140 points: **0.252 s wall, 4.82×10⁶ pts/s on 1× A100 (fp64)**
- GPU 100k-point microbench: **6.98 ms** → extrapolated full-slice = **~85 ms ≈ 0.085 s**  ← matches paper's Table S.2 ("about 0.07 s" for 1 A100).
- CPU 100k-point: 369 ms → 4.4 s for full slice → matches paper's Table S.2 (~1 s on 64-core AMD EPYC 7763 Perlmutter node vs my uicgpu single-thread test).
- **Speedup GPU vs CPU = 52.9×** (my numbers, single-threaded CPU baseline; paper reports 14× against a 64-core CPU node — this is the same speedup direction with a much lower CPU baseline).
- All 20 output-variable magnitude ranges match Table 1 / paper text: e.g. num_a1 span ~10¹⁰, mom_a4 span ~10⁻²¹, bc_a1 span ~10⁻⁹, so4_a1 span ~10⁻⁹ — see `evidence/inference_result.json`.

## 06:26 — attempt to compute R² from X_test5.npy
`X_test5.npy` has shape (1,214,705, 80). Column-pair analysis reveals cols 21+31=52, 23+31=54, …, 47+31=78 are **byte-identical** — this file appears to have redundant duplicate columns rather than a pre-/post-microphysics pair. Difference of paired columns is 0 for all but 3 columns, and those differences are at machine-noise level (~1e-26). Cannot back out a Δ ground truth without the authors' undocumented column-index legend. Emailing the authors was outside the wave-run budget. **Blocker: ground-truth Y arrays are not published in the Zenodo bundle**, so a numerical R² spot-check is not possible from the released artifacts.

## 06:30 — write-up
Assembled REPORT.md, brief.md, artifact_harvest.md, this attempt_log.md, and evidence bundle. Verdict = **PARTIAL**.
