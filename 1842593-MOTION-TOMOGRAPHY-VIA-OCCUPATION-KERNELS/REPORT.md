# REPORT — Motion Tomography via Occupation Kernels

**OSTI ID:** 1842593 · **Authors:** Russo, Kamalapurkar, Chang, Rosenfeld · **Year:** 2021  
**Working dir:** ~/Dropbox/REPLICATE-PROJECT/1842593-MOTION-TOMOGRAPHY-VIA-OCCUPATION-KERNELS/  
**Replication date:** 2026-04-19

## Paper claim (one paragraph)

The paper introduces an iterative predictor-corrector algorithm for reconstructing unknown spatially-varying 2D flow fields (e.g., ocean currents) from endpoint observations of mobile sensing vehicles, using *occupation kernels* in a reproducing kernel Hilbert space (RKHS). A trajectory's occupation kernel encodes the integrated effect of the flow field along the path; the algorithm iteratively builds a Gram matrix of these occupation kernels, solves a Tikhonov-regularized linear system for expansion weights, and updates the flow estimate until convergence. The authors prove convergence via the Contraction Mapping Theorem under mild assumptions and validate on three synthetic flow fields (Gaussian bump mixture, linear, constant), reporting max relative error 0.25321 and mean relative error 0.025642 for the Gaussian bump field, with convergence on all three fields within ~10 iterations.

## What we replicated

- **Algorithm 1 (Iterative Motion Tomography):** Full implementation — trajectory generation (RK45), occupation kernel computation (Simpson's rule quadrature), Gram matrix assembly (2D quadrature), Tikhonov-regularized solve, iterative flow estimate update.
- **All three synthetic flow fields:** Gaussian bump mixture (Eq. 14), linear field (f₁=x₂, f₂=−0.2x₁), constant field (f₁=0.2, f₂=0.1).
- **Experiment 1:** Simulated flow field reconstruction (N=25 trajectories, Gaussian RBF kernel, μ=1.0, λ=1e-6, 10 iterations).
- **Convergence study (paper Figure 4):** All three flow fields, N=20 trajectories, 10 iterations each.
- **Parameter sensitivity sweeps:** Kernel width μ, regularization λ, number of trajectories N.
- **26/26 unit tests passing** across kernel properties, flow field correctness, and reconstruction accuracy.
- **Not replicated:** Experiment 2 (Gliderpalooza 2014 real ocean glider data) — no access to the proprietary dataset.

## Key results (table comparing paper vs our values)

### Experiment 1 — Gaussian bump flow field reconstruction

| Metric | Paper (Table 1) | Our replication |
|---|---|---|
| Max relative error | 0.25321 | 0.07746 |
| Mean relative error | 0.025642 | 0.01551 |
| RMSE | — | 0.00710 |
| Relative L² error | — | 0.01741 |

Our errors are *better* than the paper's; this is consistent with different random trajectory placements (paper does not specify seeds, exact N, or initial conditions).

### Convergence (displacement per iteration, Experiment 1)

| Iteration | Mean displacement |
|---|---|
| 1 | 0.2648 |
| 2 | 0.0538 |
| 5 | 7.63e-4 |
| 10 | 5.0e-5 |

Five orders of magnitude reduction confirms algorithmic convergence. ✅

### Convergence study — mean relative error at iteration 10

| Flow field | Our value | Paper trend match? |
|---|---|---|
| Gaussian bump mixture | 0.0354 | ✅ Converges slowest |
| Linear | 0.0276 | ✅ Moderate convergence |
| Constant | 0.0055 | ✅ Converges fastest (~immediate) |

Convergence ordering (constant < linear < Gaussian) matches paper Figure 4. ✅

### Parameter sensitivity

| Sweep | Key finding | Paper match? |
|---|---|---|
| Kernel width μ | U-shaped error curve, optimal μ ≈ 0.5 (error 0.0220) | ✅ |
| Regularization λ | Flat for λ ≤ 1e-8, monotonically increasing beyond; Gram matrix well-conditioned (κ ≈ 3.4) | ✅ (minor: paper may have had ill-conditioned cases) |
| Trajectories N | Error decreases with N; at N=40, mean error < 0.5% (0.0047) | ✅ |

## Honest gaps

1. **Gliderpalooza real-data experiment (Experiment 2)** not replicated — requires proprietary ocean glider dataset from Chang et al. that is not publicly available.
2. **Exact numerical match impossible** — paper does not specify random seeds, exact trajectory count, initial condition distribution, or integration step count for its Table 1 values.
3. **Regularization sweep shape** — our λ sweep is monotonically increasing (well-conditioned Gram matrices, κ ≈ 3.4), while the paper's discussion implies some experiments may have had ill-conditioned matrices where regularization helps. This is a minor difference attributable to different trajectory configurations.
4. **Exponential dot-product kernel** implemented and tested but not exercised in full experiments (paper's main results also use Gaussian RBF).

## Score

**Cov 8/10 · Agr 9/10**

- *Coverage 8/10:* All synthetic experiments (Experiment 1, convergence study, parameter sweeps) fully replicated with matching qualitative and quantitative trends. Deducted for missing real-data Experiment 2 (data unavailable).
- *Agreement 9/10:* Quantitative results in the same range or better than reported. All convergence behaviors, parameter sensitivity trends, and ordering relationships match. Minor difference in regularization sweep shape due to conditioning differences.

## Deliverables (list of important files)

| File | Description |
|---|---|
| `report/motion_tomo_replication_report.pdf` | Full 18-page LaTeX replication report |
| `replication/report/replication_report.md` | Detailed Markdown replication report with all tables and analysis |
| `replication/src/kernels.py` | Gaussian RBF & exponential kernels, occupation kernels, Gram matrix |
| `replication/src/flow_fields.py` | Three synthetic flow fields (Eq. 14, linear, constant) |
| `replication/src/trajectories.py` | Trajectory generation (true, dead-reckoned, estimated) via RK45 |
| `replication/src/reconstruction.py` | FlowReconstructor class implementing Algorithm 1 |
| `replication/src/plotting.py` | Visualization utilities |
| `replication/run_experiment1.py` | Experiment 1 runner |
| `replication/run_convergence.py` | Convergence study runner (Figure 4) |
| `replication/run_sweeps.py` | Parameter sensitivity sweep runner |
| `replication/run_sweep_ntrajs.py` | Trajectory count sweep runner |
| `replication/tests/` | 26 unit tests (kernels, flow fields, reconstruction) |
| `replication/figures/fig1_flow_comparison.png` | True vs estimated flow fields (replicates paper Fig. 1) |
| `replication/figures/fig3_error_field.png` | Error vectors and magnitude map (replicates paper Fig. 3) |
| `replication/figures/fig4_convergence.png` | Convergence curves for three flow fields (replicates paper Fig. 4) |
| `replication/figures/sweep_mu.png` | Error vs kernel width μ |
| `replication/figures/sweep_lambda.png` | Error vs regularization λ |
| `replication/figures/sweep_n_trajs.png` | Error vs number of trajectories N |
| `replication_plan_1842593.pdf` | Detailed replication plan |
| `1842593.pdf` | Original paper |
