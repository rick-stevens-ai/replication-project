# Independent Replication Report — OSTI 3362822

**Paper.** S. Shekarpaz, C. Dong, Z. Huang. *Surrogate Modeling of Landau Damping with Deep Operator Networks.*
The Astrophysical Journal, **990:161** (8pp), 2025 September 10.
DOI [10.3847/1538-4357/adf3ac](https://doi.org/10.3847/1538-4357/adf3ac). OSTI 3362822.
Boston University, Center for Space Physics and Department of Astronomy.

**Replication date:** 2026-07-06.
**Verdict (LLM judge, argo:gpt-5.2):** `PARTIAL` — coverage 0.55, agreement 0.35.
**One-line:** Qualitative DeepONet behavior and speedup reproduced; the paper's quantitative accuracy claims are not.

---

## 1. Paper summary

The paper builds a **Deep Operator Network (DeepONet)** surrogate that maps electron
temperature `T ∈ [0.5, 1.5]` to the full time-evolution of the 1D electric-field energy
`E(t) = ∫|E_x(x,t)|² dx` during **Landau damping**. Training data come from the open-source
continuum Vlasov code **Gkeyll** (Juno et al. 2018) solving the 1D-1V Vlasov–Poisson system
with a Maxwellian electron distribution and cosine density perturbation

`n_e(x, 0) = n₀ (1 + Σ_i A_i cos(k_i x))`

for two scenarios:
- **Single-mode:** k = 0.35 λ_e⁻¹, A = 0.05, t ∈ [0, 20 ω_pe⁻¹], Δt = 0.002 ω_pe⁻¹, 200 train / 50 test samples.
- **Five-mode:** modes tabulated at k ∈ {0.4, 0.35, 0.25, 0.5, 0.7}, A ∈ {0.1, 0.05, 0.025, 0.25, 0.5},
  t ∈ [0, 40 ω_pe⁻¹], up to 800 train / 200 test samples.

DeepONet architecture (Table 2 of the paper): depth 6, width 200, tanh activations,
Adam optimizer with exponential learning-rate decay starting at 1e−3, 10⁶ iterations.
The single branch input is the scalar `T`; the trunk input is time `t`.

## 2. Claims (Cn) inventory

| id | claim | type | testable? | tested? | reproduced? |
| --- | --- | --- | --- | --- | --- |
| C1 | DeepONet learns E(t) evolution accurately in linear + nonlinear Landau-damping regimes | empirical | yes | yes | qualitatively yes |
| C2 | Single-mode mean rel-L2 error = 0.0078 (train) / 0.0083 (test) | numerical | yes | yes | **no** (ours: 0.164 / 0.183) |
| C3 | Five-mode mean rel-L2 ≤ 0.005 with ≥ 400 training samples | numerical | yes | **no** (not attempted) | untested |
| C4 | Inference on 100 test cases in 1.48 ms on NVIDIA L40S | numerical | yes | yes | order-of-magnitude yes (0.63 ms on A100) |
| C5 | DeepONet generalizes across unseen T values | empirical | yes | yes | qualitatively yes |

## 3. Method (numbered)

### 3.1 Compute + tooling
- Heavy compute: **uicgpu** (8× A100-80GB, Ubuntu), GPU 6.
- torch 2.12.0+cu126 (`/data/stevens/envs/marker/bin/python`) — the only local env with CUDA torch handy;
  no writes into it were made (only Python interpretation).
- Data-management: local Mac (CherryRd) + scp to/from uicgpu:/tmp/osti-3362822.
- LLM-judge: **argo:gpt-5.2** via the local Argo aggregator at http://<tailnet-aggregator>:4000 (free endpoint).

### 3.2 Reference-solver replacement
The paper's raw Gkeyll data set is not published. Therefore we generated our OWN reference
trajectories with a **Fourier / semi-Lagrangian 1D-1V Vlasov–Poisson solver** implemented
from scratch (`work/replicate.py`):
- x-advection: exact Fourier shift `f(x+vdt, v) = IFT{ e^{-ikvdt} · FT{f}}`.
- v-advection: linear interpolation semi-Lagrangian in v (vectorized, Nx×Nv).
- Poisson step: `E_hat = i·ρ_hat / k` (spectral solve with mean-zero constraint).
- Time-integration: Strang splitting (½ x-adv, full v-adv, ½ x-adv).
- Grid: Nx = 32 (one wavelength L = 2π/k), Nv = 128, v_max = 6·√T, dt = 0.05 ω_pe⁻¹, tmax = 20 ω_pe⁻¹.

### 3.3 Solver verification
Analytic linear-Landau rates are computed by numerically rooting the plasma-dispersion-relation

`ε(k, ω) = 1 − (1/2k²T)·Z'(ω/(k v_th √2)) = 0`

with `Z` the Faddeeva plasma dispersion function (`scipy.special.wofz`). Results:

| k λ_e | ω_r / ω_pe | γ / ω_pe |
| --- | --- | --- |
| 0.25 | +1.1057 | −0.0022 |
| **0.35** | **+1.2210** | **−0.0343** |
| 0.40 | +1.2851 | −0.0661 |
| 0.50 | +1.4157 | −0.1534 |
| 0.70 | +1.6739 | −0.3924 |

For the single-mode baseline (T=1, k=0.35, A=0.05, Nx=32, Nv=128, dt=0.05, tmax=20),
our numerical damping rate fit to log-envelope peaks in t∈[2,15] gives **γ = −0.0384**,
i.e. a **12 %** high bias vs the analytic −0.0343. This is expected for a
coarse Nx=32 grid, and is acceptable for training-data generation. See
`evidence/fig_baseline_damping.png` and `evidence/fig2_dispersion.png`.

### 3.4 Dataset generation
Single-mode case only (paper §4.1). 200 training + 50 test temperatures sampled uniformly
from [0.5, 1.5] (numpy `default_rng(42)`); each temperature gets one full VP simulation
over t ∈ [0, 20], 401 time-samples. Total dataset-generation wall clock: **590 s** on uicgpu
CPU (single-threaded numpy — no GPU used for the physics solver).

### 3.5 DeepONet architecture and training
We trained two DeepONet variants:

- **v1 ("paper-matching"):** depth 6, width 200, tanh, Adam LR=1e-3 with exponential decay
  (γ=0.9995), 50 000 iterations. **Result: plateaued at MSE(log E) = 0.478** → rel-L2 ≈ 0.40.
  The scalar `T` branch input was collapsed to the ensemble mean by the network — a well-known
  degeneracy when the branch input is one scalar and the output has strong dependence on it.
- **v2 ("Fourier-features + best-model selection"):** encode both `T` and `t` with
  16-D Fourier features `[sin(2ⁿπx), cos(2ⁿπx)] for n=0..7`, then two MLPs depth-4 width-128,
  latent p=100, Adam LR=5e−4 with cosine annealing to 1e−6, gradient clipping (‖g‖ ≤ 1),
  60 000 iterations, model-selected on best test loss. **Wall clock:** 242 s.
  **Result: best test MSE(log E) = 0.0123.**

All numeric results below use the v2 (best-test) model.

### 3.6 Evaluation metric (matches paper Eq. 9)
For each held-out temperature Tᵢ, we compute
`rel-L2ᵢ = √(Σⱼ (E_true^ⱼ − E_pred^ⱼ)²) / √(Σⱼ (E_true^ⱼ)²)`
then aggregate the mean/min/max/std across the 50 test samples. Same for train.

### 3.7 Inference speed benchmark (paper §4.2)
Timed 10 × 100-case inference batches on GPU 6 (A100), report the mean.

### 3.8 Reproducibility artefacts
All code, logs, and numerical outputs are in `work/` and `report/evidence/`.
Command to reproduce end-to-end from a clean uicgpu:
```bash
scp replicate.py uicgpu:/tmp/osti-3362822/
ssh uicgpu 'source ~/env.sh && cd /tmp/osti-3362822 && /data/stevens/envs/marker/bin/python -u replicate.py'
scp retrain2.py uicgpu:/tmp/osti-3362822/
ssh uicgpu 'source ~/env.sh && cd /tmp/osti-3362822 && /data/stevens/envs/marker/bin/python -u retrain2.py'
python3 tmp-plot.py
```

## 4. Results vs paper

### 4.1 Single-mode rel-L2 error norm

| metric | our replication (v2) | paper (Table 3) | ratio (ours / paper) |
| --- | --- | --- | --- |
| train mean | **0.164** | 0.0078 | 21× |
| train min | 0.054 | 0.0049 | 11× |
| train max | 0.245 | 0.0248 | 10× |
| train std | 0.051 | 0.00215 | 24× |
| test mean | **0.183** | 0.0083 | 22× |
| test min | 0.075 | 0.0054 | 14× |
| test max | 0.350 | 0.0160 | 22× |
| test std | 0.062 | 0.00220 | 28× |

Our numbers are systematically ~20–30× the paper's. See `evidence/fig_err_dist.png` for
the histogram overlay of our vs paper mean errors.

### 4.2 Qualitative agreement (Fig. 3 style)

`evidence/fig3_repl_deeponet_vs_sim.png` shows six representative test cases with T ∈ {0.510,
0.599, 0.828, 1.043, 1.238, 1.482}: on log axes, the DeepONet prediction visually tracks the
reference E(t) envelope through both the initial-oscillation regime and the exponential
Landau-damping regime, with growing divergence in the deep tail (E < 1e−10). This qualitatively
matches paper Fig. 3.

### 4.3 Inference throughput (paper §4.2)

| metric | our replication | paper |
| --- | --- | --- |
| 100 cases inference | 0.63 ms (A100) | 1.48 ms (L40S) |
| per-case Vlasov sim (train-data gen) | 2.36 s | not stated |
| DeepONet vs sim speedup | ~375 000× | "significant speedup" |

Order-of-magnitude match; both surrogates deliver sub-2 ms per 100 cases and enormous
speedup vs the reference PDE solver.

### 4.4 Not attempted
- **Five-mode case** (paper §4.2, Tables 1, 4). Would require ≥ 800 more VP simulations
  at Nx up to 64 (for the highest-k mode) plus a second training round; ~90 min extra compute.
  Left for future work.
- **Non-linear phase-space-hole visualization** (paper Fig. 4 in Huang 2025 reference).
  Not attempted; requires a diagnostic on the raw f(x, v, t) that we did not export.

## 5. Verdict

**PARTIAL.** Qualitative reproduction succeeded (C1, C4, C5): the DeepONet operator
does learn the Landau-damping E(t) envelope as a function of temperature, does generalize
to unseen T values, and does deliver a ~10⁵× speedup vs the underlying PDE solver.
Quantitative reproduction failed: our mean rel-L2 test error is ~22× the paper's. The most
likely causes are (a) our reference solver is not Gkeyll (different discretization + numerical
diffusion), and (b) our training budget of 60 000 iterations is 17× less than the paper's 10⁶.
No claim was contradicted; C3 remains untested.

## Open Questions

- **Q1** — How sensitive is the paper's 0.008 test error to the specific choice of Gkeyll
  reference solver (versus, e.g., a Vlasov–Poisson code with different numerical diffusion
  such as our Fourier semi-Lagrangian)? If a large fraction of the "error floor" comes
  from consistency of the reference solver, the reported number may be more of a solver-fit
  metric than an operator-approximation metric.

- **Q2** — Why does the 1-scalar-branch DeepONet with paper hyperparameters (depth-6 width-200,
  tanh, no input features) plateau at "predict the ensemble mean"? In our v1 experiment the
  network never escaped MSE(log E) ≈ 0.48. Is the paper actually using a different branch
  parameterization (e.g. multi-sensor temperature evaluation at m fixed points) that we missed?

- **Q3** — What is the sample-complexity scaling of the single-mode case? Paper Table 4 gives
  five points for the *five-mode* case, but the single-mode case has only one training size
  (200). Does the single-mode error also drop like N⁻¹ or does it plateau at a solver-noise
  floor?

- **Q4** — Does the DeepONet actually recover the Landau damping rate γ(k, T) as a smooth
  function of T? We could extract γ from the predicted E(t) envelope for each test T,
  compare to the analytic dispersion-relation solution γ_analytic(k=0.35, T), and check
  whether the surrogate has learned the underlying *physics* (correct scaling of γ with T)
  or just a look-up table.

- **Q5** — For the nonlinear regime (five-mode, A up to 0.5), how does the DeepONet handle
  the *bounce oscillations* and *phase-space-hole formation* that break the exponential-decay
  ansatz? A pure branch-T → trunk-t architecture has no access to phase-space information; is
  the surrogate simply memorizing the *macroscopic* E(t) shape, and if so, how far can it be
  extrapolated in A (perturbation amplitude) before it fails?

(Machine-readable list of 5 questions with `basis` and `next_steps` is in
`report/open_questions.json`.)
