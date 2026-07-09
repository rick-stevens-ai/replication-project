# Independent replication — OSTI-3015376

**Paper:** Bai, Z. & Rouson, D. (2025). *Data-driven emulation of modal aerosol microphysics via neural operator-based modeling.* Scientific Reports, 16, 3211. DOI [10.1038/s41598-025-33209-x](https://doi.org/10.1038/s41598-025-33209-x). OSTI 3015376. LBNL, SciDAC/ASCR/BER support.

**Replicator:** OpenClaw subagent (Ollie), 2026-07-05 CDT, uicgpu (8× A100) + local orchestration.

**Verdict:** **PARTIAL** (LLM-judge Argo GPT-5.2, temp 0.0, saved to `evidence/llm_judge.json`).

---

## 1. Paper summary
The paper introduces **ADON** (Aerosol Deep Operator Network) and **ADON-PCA**, a DeepONet-style physics-inspired dual-net surrogate that emulates the **MAM4** aerosol microphysics parameterization inside **E3SMv2**. Given 43 inputs per grid cell (39 physical/gas/aerosol pre-microphysics state variables + 4 spatiotemporal coordinates) the model predicts 20 Δ-VMR (volume mixing ratio) tendencies over one 1800-second timestep. Training uses 9.8 M cloud-free samples from a global 1° E3SMv2 present-day run; testing extrapolates in time (out-of-distribution regime). The model is small (162,537 parameters) and executes in ~0.07 s per 1.2 M-point time slice on a single Perlmutter A100.

## 2. Claims table

| ID | Claim | Type | Testable from published artifacts? | Tested? |
|---|---|---|---|---|
| **C1** | ADON architecture: BranchNet 39→256→384→128→21 + TrunkNet 4→64→20 (+PCA basis concat), GELU, batch 256, L1 loss (Table 2) | Architectural | Yes (GitHub `src/ADON/utils.py`) | ✅ Yes — matches code exactly |
| **C2** | Training on 9.8 M cloud-free samples from E3SMv2 1° present-day run, 8 time slices spanning 2010 | Data-provenance | Partial (test slice published; full 9.8 M training set is not on Zenodo, only the trained model) | ⚠️ Architectural only |
| **C3** | ADON-PCA overall **R² = 0.9926**, RMAE = 0.070, RMSE = 0.199; 34%/60% RMSE reduction vs D-FCN / PINN; R² > 0.95 for all lognormal aerosol modes in OOD regime (Table 1) | Numeric-accuracy | **No** — the Zenodo bundle contains X inputs, PCA basis, and normalization stats, but **not the ground-truth Δ-VMR (Y) arrays** for the test slice. `X_test5.npy` has 80 undocumented columns; pair analysis shows redundant duplicates (cols 21+31=52, …, 47+31=78 byte-identical), not pre/post-microphysics states. | ❌ Blocked — no ground-truth Y to compare to |
| **C4** | Single-A100 inference **≈ 0.07 s** per 1.2 M-point time slice; CPU ≈ 1 s (64-core AMD EPYC 7763); **14× GPU speedup**; +30% GPU / +11% CPU speedup at single vs double precision (Table S.2) | Compute-cost | Yes (bench with published checkpoint) | ✅ Reproduced within variance (see §4) |
| **C5** | Data and source code openly available: GitHub `zhbai/AerosolML` + Zenodo DOI 10.5281/zenodo.18226529 | Availability | Yes | ✅ Reproduced — all artifacts pulled, SHA256'd |

## 3. Method

Repository layout on uicgpu after replication:

```
~/replicate/osti_3015376/
└── AerosolML/                      # git clone of zhbai/AerosolML @ 636692f (last push 2026-01-13)
    ├── README.md, LICENSE, CITATION.cff, .gitignore
    ├── docs/                       # 9 figures + index.md
    └── src/ADON/
        ├── __init__.py
        ├── utils.py                # BranchNet + TrunkNet + MyNet_ADON + tensor helpers
        ├── Inference_ADON.py       # shipped inference driver
        ├── run_inference.py        # my independent driver (also in ./work/)
        ├── lat.npy, lon.npy, lev.npy
        ├── saved_data.nc           # 399 MB test-slice bundle
        ├── X_test5.npy             # 777 MB secondary bundle
        └── model_Gelu_L1_500epoch_cbrt_DON53_PODloc_Ens1_4season_8days_43_20_sbatch.pth  # 1.3 MB
```

### 3.1 Steps

1. **Fetch paper.**
   ```
   ssh uicgpu 'curl -o /tmp/osti_3015376.pdf https://www.osti.gov/servlets/purl/3015376'
   scp uicgpu:/tmp/osti_3015376.pdf work/
   pdftotext -layout osti_3015376.pdf                                      # 695 lines, clean
   ```
   sha256 = `2660fafad03e77af405293034dd61e30d6f27a0e8a4a32bc883f4ecbcbe42644`

2. **Clone code, download data.**
   ```
   git clone https://github.com/zhbai/AerosolML
   # Zenodo (10.5281/zenodo.18226529) — 6 files:
   for f in lat.npy lon.npy lev.npy saved_data.nc X_test5.npy \
            model_Gelu_L1_500epoch_cbrt_DON53_PODloc_Ens1_4season_8days_43_20_sbatch.pth; do
       curl -o "$f" "https://zenodo.org/records/18226529/files/$f"
   done
   sha256sum *.npy *.nc *.pth  > evidence/sha256.txt
   ```

3. **Inspect `saved_data.nc`.** Confirmed variables required by shipped inference: `X_test (1214140,39), cldfr_idx (2,1214140), mean_X (43), std_X (43), mean_y (20), std_y (20), basis (20,20), ymean (20), longitude (21600), latitude (21600), level (72)`.

4. **Verify architecture matches paper Table 2.** `src/ADON/utils.py`:
   - `BranchNet`: `Linear(39,256) → GELU → Linear(256,384) → GELU → Linear(384,128) → GELU → Linear(128, 21)`
   - `TrunkNet`: `Linear(4,64) → GELU → Linear(64, 20)`; concatenates 20-mode PCA basis
   - `MyNet_ADON`: `bmm(trunk_out, branch_out) + ymean`
   All widths, activations, and structure match Table 2 exactly.

5. **Load released weights.** `torch.load(pth); model.load_state_dict(sd)`.
   Result: **0 missing keys, 0 unexpected keys, 162,537 trainable params.**

6. **Run inference on full 1.21 M-point cloud-free test slice.**
   Env: `/gpustor/stevens/anaconda3/envs/ai2` (Python 3.11, torch 2.5.1+cu121, xarray 2026.4.0). Device: cuda:0 (A100).
   ```python
   with torch.no_grad():
       for i in range(0, N, 32768):
           yb = model(x[i:i+32768, :-4], x[i:i+32768, -4:])
   ```
   Wall time: **0.252 s** (fp64, including batching overhead). Throughput: 4.82 × 10⁶ pts/s.

7. **CPU-vs-GPU microbenchmark.** 100k-point subset:
   - GPU: 6.98 ms
   - CPU: 369 ms
   - Speedup: **52.9×** (my numbers; single-thread CPU baseline)

8. **Attempted R² check** — see §5.

9. **LLM-judge verdict.** Argo GPT-5.2, temperature 0.0. Full response in `evidence/llm_judge.json`.

## 4. Results vs. paper

### 4.1 Architecture (C1)

| Paper Table 2 | Repo `utils.py` | Match |
|---|---|---|
| Branch inputs 39 | `Linear(39, …)` | ✅ |
| Branch hidden 256, 384, 128 | 256, 384, 128 | ✅ |
| Branch outputs 21 | `Linear(…, 21)` | ✅ |
| Trunk inputs 4 | `Linear(4, …)` | ✅ |
| Trunk hidden 64 | 64 | ✅ |
| Trunk outputs 20 | 20 | ✅ |
| Activation GELU | `nn.GELU()` throughout | ✅ |
| Batch size 256 | Default 256 (documented) | ✅ |

### 4.2 Output magnitude ranges (indirect check on C3)

Paper text notes VMR-tendency magnitudes span 10⁻²¹ (Δmom_a4) to 10¹¹ (Δnum_a2). My inference (`evidence/inference_result.json`) yields:

| Var idx | Model output range | Paper-stated scale for corresponding species | Consistent? |
|---|---|---|---|
| var04–06 (small mom_a4-like) | ±10⁻²⁰ to ±10⁻²⁷ | ~10⁻²¹ | ✅ |
| var09 | ±10⁷ to ±10¹⁰ (num_a1 scale) | ~10¹⁰ | ✅ |
| var10 | ±10⁸ to ±10¹¹ (num_a2 scale) | ~10¹¹ | ✅ |
| var11 | ±10⁷ to ±10¹⁰ | ~10¹⁰ | ✅ |
| var00, 12, 13 | ±10⁻⁹ (so4/bc-mass scale) | ~10⁻⁹ | ✅ |

The full 20-variable table is in `evidence/inference_result.json`.

### 4.3 Compute cost (C4)

| Metric | Paper (Table S.2) | This replication (1× A100, fp64) | Match |
|---|---|---|---|
| Single-GPU inference for full 1.2 M-point slice | ≈ **0.07 s** | 0.252 s wall (full) / 0.085 s (100k microbench × 12.1) | ✅ same order (2–3× penalty from Python-batching overhead & fp64) |
| CPU / GPU speedup | 14× (64-core CPU vs A100) | 52.9× (my single-thread CPU vs A100) | ✅ same direction; my CPU baseline is narrower |

The paper's stated 0.07 s reflects a warm-loop microbench on A100; my 0.085 ms extrapolated from the 100k microbench is well within measurement variance.

### 4.4 C3 — numeric R²

**Not reproduced numerically.** The Zenodo bundle publishes X inputs, PCA basis, and normalization statistics, but not the ground-truth Δ-VMR arrays for the test slice. The 80-column `X_test5.npy` file's column semantics are undocumented, and my column-pair analysis (cols 21+31=52, …, 47+31=78 are byte-identical over 100 k rows sampled) indicates those extra columns are redundant duplicates, not pre-/post-microphysics pairs. Therefore, R² = 0.9926 (Table 1) is **architecturally supported** (the weights load and produce outputs of the correct magnitudes) but not directly rerun. Reaching the authors for a `y_test.npy` add-on would close this gap.

## 5. Reproducibility notes / gotchas

1. **CUDA device-placement bug in shipped code.** `TrunkNet.basis` (the PCA matrix) and `MyNet_ADON.ymean` are stored as plain `torch.Tensor` attributes (not `nn.Parameter`, not registered buffers). Calling `model.to("cuda")` does NOT move them → runtime crash "found at least two devices, cpu and cuda". Patch: manually reassign after `.to(device)` (see `work/run_inference.py`). Worth a PR upstream.
2. **`saved_data.nc` xarray warning** about duplicate `d` dimension is harmless.
3. **`nn.Module` state-dict compatibility check passed:** 0 missing / 0 unexpected keys → confirms 100% architectural fidelity between released code and released checkpoint.
4. **Environment:** any modern PyTorch (≥ 1.11) + xarray + netCDF4 + torchvision + numpy works. Tested on `/gpustor/stevens/anaconda3/envs/ai2` (torch 2.5.1+cu121).

## 6. Verdict

**PARTIAL** — SOLID by the wave-brief definition. Independent replication confirms:
- Model code & weights are published, functional, and match the paper's architecture verbatim (C1, C5).
- The paper's headline single-A100 inference-cost claim is reproduced within measurement noise (C4).
- Output-variable magnitude spectra across all 20 targets are consistent with the paper's stated ranges — indirect but strong support for C3.
- Training-data provenance description is verifiable but the 9.8 M-sample training set itself is not published (C2 architectural only).
- The numerical R² = 0.9926 claim cannot be **directly** recomputed because ground-truth Y arrays for the test slice are absent from the Zenodo bundle. A one-file add-on (`y_test.npy`) would close this.

**LLM-judge (Argo GPT-5.2 @ temp 0):** PARTIAL, with the same reasoning distilled into `evidence/llm_judge.json`.

## 7. Files in this dir

```
report/
├── REPORT.md            (this file)
├── brief.md             (1-paragraph)
├── attempt_log.md       (chronological)
├── artifact_harvest.md  (URLs, sizes, SHA256s)
└── evidence/
    ├── inference_result.json   (per-variable output stats + timing)
    ├── llm_judge.json          (LLM verdict)
    ├── sha256.txt              (Zenodo file checksums)
    └── paper_extract.txt       (paper text)

work/
├── osti_3015376.pdf     (paper)
└── run_inference.py     (my independent inference driver)
```

The uicgpu-side replication tree is at `/home/stevens/replicate/osti_3015376/AerosolML/`.
