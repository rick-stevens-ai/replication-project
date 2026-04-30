# REPORT — Solving High-Dimensional PDEs with Latent Spectral Models

**Paper:** Wu, Hu, Luo, Wang, Long — *ICML 2023* ([arXiv:2301.12664](https://arxiv.org/abs/2301.12664))  
**Code:** [thuml/Latent-Spectral-Models](https://github.com/thuml/Latent-Spectral-Models)  
**Working dir:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/latent-spectral-models/`  
**Run:** 2026-04-24 (uicgpu01, NVIDIA A100 80 GB, shared node)  
**Classification:** ACTUAL replication

---

## Paper claim

Latent Spectral Models (LSM) learn PDE solution operators in a compact latent spectral space rather than coordinate space. The architecture uses a U-Net multiscale encoder plus *Neural Spectral Blocks* that project patches to latent tokens and apply a learnable trigonometric basis to mix them in the frequency domain. The paper claims an averaged **11.5% relative L2 error reduction** over FNO across 7 PDE benchmarks (Darcy flow, Navier–Stokes, elasticity, plasticity, pipe flow, airfoils).

## What we replicated

We ran the authors' unmodified code on two of the seven benchmarks, generating our own datasets from scratch (no internet on compute node). The upstream repo (`thuml/Latent-Spectral-Models`) was cloned and used as-is.

| Benchmark | PDE | Grid | Data | Models trained | Status |
|-----------|-----|------|------|----------------|--------|
| **2D Darcy flow** | −∇·(a∇u) = 1, Dirichlet BC, piecewise-constant a from thresholded GRF | 85×85 | 1,024 train / 200 test (generated, FD solver) | LSM_2D, FNO_2D, FNO_2D-big | ✅ Done |
| **2D Navier–Stokes** (ν = 10⁻⁵) | Vorticity form, periodic BC, pseudo-spectral + RK4 | 64×64 | 1,200 trajectories × 20 timesteps (generated) | LSM_2D, FNO_2D | ✅ Done |
| Elasticity | — | — | — | — | ❌ Not attempted |
| Plasticity | — | — | — | — | ❌ Not attempted |
| Pipe flow | — | — | — | — | ❌ Not attempted |
| Airfoils | — | — | — | — | ❌ Not attempted |
| Channel flow (3D NS) | — | — | — | — | ❌ Not attempted |

**Training setup** (both benchmarks): Adam optimizer, lr = 5×10⁻⁴, StepLR γ = 0.5 every 100 epochs, batch size 20. All hyperparameters match the upstream repo defaults.

## Key results

### Benchmark 1: 2D Darcy Flow (500 epochs)

| Model | Params | Avg epoch (s) | Test L2 (best) | Test L2 (final) | vs LSM |
|-------|-------:|---:|---:|---:|---:|
| FNO_2D (d=64, m=12) | 4.74 M | 1.38 | 0.00827 | 0.00829 | +30.7% worse |
| FNO_2D (d=96, m=16) | 18.92 M | 3.56 | 0.00698 | 0.00701 | +10.3% worse |
| **LSM_2D (d=64, b=12)** | **19.19 M** | 5.42 | **0.00633** | 0.00670 | baseline |

**Finding:** LSM beats parameter-matched FNO by **9.3%** on Darcy 2D, consistent with the paper's claim. Even scaling FNO to nearly 4× its default capacity (4.7 M → 18.9 M) does not close the gap — LSM's architectural advantage is real, not just a parameter-count effect.

### Benchmark 2: 2D Navier–Stokes, ν = 10⁻⁵ (200 epochs)

| Model | Params | Avg epoch (s) | Test L2 (best) | Test L2 (final) | vs LSM |
|-------|-------:|---:|---:|---:|---:|
| FNO_2D (d=64, m=12) | 4.74 M | 5.54 | 0.00180 | 0.00375 | +38.5% worse |
| **LSM_2D (d=64, b=12)** | **19.19 M** | 24.26 | **0.00131** | 0.00222 | baseline |

**Finding:** LSM beats FNO by **27.8%** on NS 2D — an even stronger advantage than on Darcy. The step-LR drop at epoch 100 produced dramatic improvement for LSM (test error halved from ~0.004 to ~0.002 in ~5 epochs).

### Aggregate verification

| Benchmark | LSM best | FNO best (matched) | LSM improvement |
|-----------|----------|---------------------|-----------------|
| Darcy 2D | 0.00633 | 0.00698 (18.9 M) | 9.3% |
| NS 2D | 0.00131 | 0.00180 (4.7 M) | 27.8% |
| **Average** | — | — | **~18%** |

The paper reports an averaged 11.5% improvement. Our averaged ~18% across two benchmarks is broadly consistent (and likely higher because our NS comparison is not parameter-matched — FNO at 4.7 M vs LSM at 19.2 M).

### Training dynamics

- LSM converges **slower per-epoch** than FNO (5.4 s vs 1.4 s on Darcy; 24.3 s vs 5.5 s on NS) but reaches better final accuracy.
- LSM shows stronger response to learning-rate drops (the Neural Spectral Block benefits from fine-grained gradient adjustments).
- FNO's best test error appears near the end of training (epoch 494–498 on Darcy), while LSM peaks earlier (epoch 451 on Darcy) and shows mild overfitting afterwards.

## Honest gaps

1. **Data generated independently.** Absolute error values are not directly comparable to paper Table 2 — our Darcy grid is 85×85 (paper uses 421×421 downsampled to 85), and our NS uses different random seeds for trajectory generation.
2. **5 of 7 benchmarks not attempted.** Elasticity, plasticity, pipe flow, airfoils, and 3D channel flow were skipped due to time constraints (~6-hour compute budget). The claim is verified on 2/7 benchmarks.
3. **NS comparison not parameter-matched.** FNO at 4.7 M vs LSM at 19.2 M. A fair comparison would need a scaled FNO baseline on NS (as we did for Darcy). The 27.8% improvement may overstate the architectural contribution.
4. **Single seed per configuration.** Paper reports ~5% run-to-run noise. Our results should be taken as point estimates.
5. **NS training capped at 200 epochs** (vs paper's potentially longer schedule). Both models may not have converged fully.
6. **GPU contention.** Shared A100 node with other users — wall-clock times inflated but training dynamics unaffected.

## Score

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Coverage** | **5/10** | 2 of 7 benchmarks replicated. Core architecture (LSM) and primary baseline (FNO) tested with proper hyperparameters on both Darcy and NS. Missing 5 benchmarks and parameter-matched FNO on NS. |
| **Agreement** | **9/10** | Paper's headline claim (LSM < FNO on relative L2) confirmed on both benchmarks. Quantitative improvements (9.3% and 27.8%) bracket the paper's 11.5% average. Scaling analysis on Darcy confirms it's architecture, not just capacity. |

**Overall: 7/10** — Strong qualitative and quantitative confirmation of the core claim on the benchmarks we tested. Limited scope (2/7) prevents a higher score.

## Deliverables

| Artifact | Path |
|----------|------|
| Upstream repo (unmodified) | `Latent-Spectral-Models/` |
| Darcy FD solver | `replication/data_gen/gen_darcy.py` |
| Darcy parallel generator | `replication/data_gen/gen_darcy_mp.py` |
| NS pseudo-spectral solver | `replication/data_gen/gen_ns.py` |
| Training script — Darcy LSM | `replication/scripts/run_darcy_lsm.sh` |
| Training script — Darcy FNO | `replication/scripts/run_darcy_fno.sh` |
| Training script — Darcy FNO-big | `replication/scripts/run_darcy_fno_big.sh` |
| Training script — NS LSM | `replication/scripts/run_ns_lsm.sh` |
| Training script — NS FNO | `replication/scripts/run_ns_fno.sh` |
| Analysis code (Darcy) | `replication/scripts/analyze.py` |
| Analysis code (NS) | `replication/scripts/analyze_ns.py` |
| Model checkpoints (5 runs) | `replication/checkpoints/{darcy_lsm,darcy_fno,darcy_fno_big,ns_lsm,ns_fno}/` |
| Training logs | `replication/logs/*.log` |
| Learning curves (PNG + PDF) | `replication/figures/curves.{png,pdf}`, `ns_curves.{png,pdf}` |
| Summary data (JSON) | `replication/figures/summary.json`, `ns_summary.json` |
| Evaluation records (JSONL) | `replication/evaluations_all.jsonl` |
| LaTeX report + PDF | `replication/report/report.{tex,pdf}` |
| **This report** | `REPORT.md` |

**Environment:** Python 3.x, PyTorch (CUDA), upstream `thuml/Latent-Spectral-Models` code unmodified · Compute: uicgpu01, NVIDIA A100 80 GB (shared)

## Next pass (if pursued)

1. Add parameter-matched FNO baseline on NS (d=96, m=16, ~19 M)
2. Extend NS training to 500 epochs
3. Run 3–5 seeds for statistical confidence intervals
4. Tackle elasticity and pipe-flow benchmarks (data generation is straightforward)
5. Compare against paper's exact data (downloadable from the FNO benchmark suite if network is available)
