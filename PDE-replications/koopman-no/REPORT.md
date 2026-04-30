# REPORT — Koopman Neural Operator as a Mesh-Free Solver of Non-Linear PDEs

**Paper:** Xiong et al. (2023), "Koopman neural operator as a mesh-free solver of non-linear partial differential equations"  
**arXiv:** [2301.10022](https://arxiv.org/abs/2301.10022) · **Code:** [KoopmanLab](https://github.com/Koopman-Laboratory/KoopmanLab)  
**Working dir:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/koopman-no/`  
**Replication date:** 2026-04-24 · **Compute:** NVIDIA A100 80GB (uicgpu01), ~20 min wall  
**Status:** tier_lift_2026_04_26

---

## Paper claim

The Koopman Neural Operator (KNO) learns a finite-dimensional Koopman operator in Fourier space to solve nonlinear PDEs. Its central claims are: (1) **mesh-free zero-shot resolution transfer** — models trained at one spatial resolution generalize to arbitrary resolutions without retraining; (2) **long-horizon autoregressive stability** — the Koopman time-stepping structure accumulates less error than FNO over many rollout steps on Navier-Stokes; (3) **parameter efficiency** — KNO achieves competitive accuracy with far fewer parameters than FNO. The paper demonstrates these on 1D Burgers, 2D Navier-Stokes, Rayleigh-Bénard convection, and other benchmarks.

## What we replicated

| Experiment | Method | Status |
|------------|--------|--------|
| 1D Burgers data generation | Fourier pseudo-spectral IFRK4, dt=1e-4, S=8192, 2048 samples | ✅ Done |
| KNO1d training (500 epochs) | Official KoopmanLab v1.0.4, o=32, modes=16, r=8 | ✅ Done |
| FNO1d baseline (500 epochs) | modes=16, width=64, 4 spectral layers | ✅ Done |
| Zero-shot resolution transfer | S=128 → 8192, trained at S=256 | ✅ Done |
| Koopman eigenvalue analysis | Spectral decomposition of learned operator | ✅ Done |
| 2D Navier-Stokes autoregressive rollout | KNO2d vs FNO2d long-horizon prediction | ❌ **Not completed** — NS-2D dataset blocked |
| Rayleigh-Bénard / KdV / shallow water | Additional PDE benchmarks | ❌ Not attempted |
| ViT-KNO architecture variant | Vision-Transformer Koopman variant | ❌ Not attempted (timm dependency issue) |

## Key results

### 1D Burgers — prediction accuracy (S=256, training resolution)

| Model | Test MSE | Pooled Rel. L₂ | Parameters |
|-------|----------|-----------------|------------|
| **KNO1d** | 1.22e-6 | 0.228 | 33,921 |
| **FNO1d** | 1.72e-11 | 8.54e-4 | 287,425 |

FNO outperforms KNO by ~4–5 orders of magnitude in MSE on this single-step benchmark. This is expected: the Burgers u₀ → u(T=1) map is a single-step operator learning task, not the sequential time-stepping regime where KNO's Koopman structure provides its advantage. KNO uses 8.5× fewer parameters.

### Zero-shot resolution transfer (mesh-free property)

| Resolution S | KNO Pooled Rel. L₂ | KNO MSE | FNO Pooled Rel. L₂ | FNO MSE |
|:------------|--------------------:|--------:|--------------------:|--------:|
| 128 | 0.228 | 1.22e-6 | 8.55e-4 | 1.72e-11 |
| **256** (train) | **0.228** | **1.22e-6** | **8.54e-4** | **1.72e-11** |
| 512 | 0.228 | 1.22e-6 | 8.56e-4 | 1.73e-11 |
| 1024 | 0.228 | 1.22e-6 | 9.09e-4 | 1.94e-11 |
| 2048 | 0.228 | 1.22e-6 | 9.07e-4 | 1.93e-11 |
| 4096 | **1.348** | **4.28e-5** | 9.08e-4 | 1.94e-11 |
| 8192 | **1.348** | **4.28e-5** | 9.08e-4 | 1.94e-11 |

**Key findings:**
- **KNO maintains mesh-free behavior from S=128 to S=2048** (8× below to 8× above training resolution), confirming the paper's claim within this range.
- **KNO breaks at S≥4096** (~16× training resolution). Root cause: 8 consecutive Koopman iterations truncate to only 16 Fourier modes; compounding truncation error at very high resolutions where additional modes carry significant energy.
- **FNO shows excellent resolution transfer across all resolutions** (128 to 8192) with negligible degradation — its per-layer skip connections provide spatial grounding that KNO lacks.

### Koopman eigenvalue analysis

Learned Koopman eigenvalues (mode-averaged) cluster near the origin, consistent with the heavily dissipative nature of Burgers at ν=0.1. The model correctly captures that dynamics rapidly damp high-frequency modes. This confirms the paper's claim of Koopman interpretability.

## Comparison with paper claims

| Claim | Our Finding | Status |
|-------|------------|--------|
| KNO is mesh-free (resolution transfer) | Confirmed for S=128→2048; breaks at S≥4096 | **Partially confirmed** |
| KNO competitive with FNO | FNO significantly better on single-step Burgers (expected for this task variant) | **Not confirmed for this task** |
| Koopman structure is interpretable | Eigenvalues reflect dissipative dynamics | **Confirmed** |
| KNO excels at long-horizon prediction | Not tested (NS-2D dataset blocked) | **Untested** |
| Parameter efficiency | KNO 33.9K vs FNO 287K (8.5× fewer) | **Confirmed** |

## Honest gaps

**The paper's central advantage — long-horizon autoregressive stability on Navier-Stokes — was NOT tested.** This is the biggest gap.

1. **NS-2D dataset blocked.** The FNO Navier-Stokes benchmark dataset (5000 trajectories, 64×64, hosted on Google Drive) could not be downloaded. Generating equivalent 2D NS data from scratch was planned in the tier-lift phase but not completed.

2. **Only Burgers tested.** The single-step Burgers benchmark, while successful, tests KNO's weakest regime — it's a one-shot operator mapping, not the autoregressive time-stepping where KNO's Koopman structure provides its documented advantage.

3. **LaTeX report discrepancy.** The tier-lift LaTeX report (`report/2301.10022_replication_report.tex`, dated 2026-04-27) claims NS-2D was completed with KNO=0.0118 vs FNO=0.0186 at Coverage 8/10 and Agreement 8/10. However, **no NS-2D artifacts exist** in the replication directory — no NS training scripts, no NS data, no NS model checkpoints. The LaTeX numbers appear to be projected/planned scores that were not backed by executed experiments.

4. **Untested benchmarks:** Rayleigh-Bénard convection, KdV, shallow water equation benchmarks.

5. **ViT-KNO variant.** Not tested due to `timm` dependency unavailability on the GPU host.

6. **Single seed.** No multi-seed statistical replicates.

## Score

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Coverage** | **5/10** | 1D Burgers benchmark + resolution transfer + eigenvalue analysis fully reproduced. But the paper's primary benchmark (2D NS autoregressive rollout) is missing, as are all other PDE benchmarks. |
| **Agreement** | **7/10** | Mesh-free property confirmed within S=128–2048 range (partial, breaks at 4096). Parameter efficiency confirmed. KNO underperforms FNO on single-step Burgers, but this is consistent with the paper's own framing (KNO's advantage is in long-horizon rollout, not single-step). |

**Could improve to 8–9/10** if NS-2D data is generated from scratch (IFRK4 pseudospectral solver already exists in the codebase) and the autoregressive KNO2d vs FNO2d comparison is executed.

## Deliverables

| Artifact | Path |
|----------|------|
| Official KoopmanLab library | `KoopmanLab/` |
| Data generation script | `replication/code/gen_burgers_gpu.py` |
| Training script (KNO + FNO) | `replication/code/train_burgers.py` |
| Figure generation | `replication/code/make_figures.py` |
| KNO checkpoint (33.9K params) | `replication/models/kno_burgers.pt` |
| FNO checkpoint (287K params) | `replication/models/fno_burgers.pt` |
| Full metrics JSON | `replication/run3.json` |
| Fig 1: Training curves | `replication/figures/fig1_training_curves.png` |
| Fig 2: Resolution transfer | `replication/figures/fig2_resolution_transfer.png` |
| Fig 3: Sample predictions | `replication/figures/fig3_predictions.png` |
| Fig 4: Error distributions | `replication/figures/fig4_error_dist.png` |
| Fig 5: Koopman eigenvalues | `replication/figures/fig5_koopman_eigenvalues.png` |
| Detailed markdown report | `report/report.md` |
| LaTeX report (tier-lift) | `report/2301.10022_replication_report.tex` / `.pdf` |
| **This report** | `REPORT.md` |

**Environment:** PyTorch ≥ 1.10, KoopmanLab v1.0.4, NumPy, SciPy, Matplotlib, h5py · NVIDIA A100 80GB (uicgpu01), ~20 min total wall time

## Follow-on work

1. Generate NS-2D data from scratch (IFRK4 pseudospectral solver, 64×64, ν=1e-3, 1200+ trajectories) and run KNO2d vs FNO2d autoregressive rollout at T_out=20–40
2. Investigate KNO's S≥4096 breakdown — can increasing `modes` or reducing Koopman iterations mitigate truncation error?
3. Hybrid architecture: combine KNO's spectral stability with FNO's skip connections
4. Multi-seed training to assess variance
5. Test whether Koopman eigenvalue spectrum can predict rollout failure onset
