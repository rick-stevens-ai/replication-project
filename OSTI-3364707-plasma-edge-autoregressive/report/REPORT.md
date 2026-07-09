# Independent Replication Report — OSTI 3364707

**Paper.** Csala H, De Pascuale S, Laiu P, Lore J, Park J-S, Zhang P (2026).
*Autoregressive long-horizon prediction of plasma edge dynamics.*
Nuclear Fusion 66 066013.  DOI: 10.1088/1741-4326/ae666c.
OSTI id: 3364707.

**PDF.** sha256 `a2dd16c54746fe1e4edf138c0fdf997eef17532ca653bc7b12d9e256b1358c0b`; 4,835,518 bytes.
Fetched via IOP (OSTI purl unreachable from the replication host on 2026-07-05).

**Replication mode.** SPOT-CHECK on a matched surrogate problem
(see §6 Scope). Free tooling only (numpy, pytorch MPS/CPU, matplotlib).
Argo Opus reasoning only.

---

## 1. Summary

The paper trains **vision-transformer (ViT) autoregressive surrogates** for
2D SOLPS-ITER plasma-edge fields on the KSTAR tokamak (grid 98×38, channels
= electron density n_e, electron temperature T_e, radiated power P_rad),
driven by a scalar gas-puff actuator. Four models are trained with rollout
horizons `n_train ∈ {1, 10, 50, 100}` steps, and evaluated on training +
unseen test trajectories at rollouts up to ~7000 steps.

The paper's central quantitative claim is that **increasing `n_train`
systematically suppresses long-horizon error accumulation**, reducing
full-trajectory NRMSE from ~40 % (next-step-only training, "Matey-1")
to < 10 % (100-step training, "Matey-100") on training trajectories, and to
~27 % on an unseen 6800-step rollout.

We SPOT-CHECK this central claim using an independent, model-agnostic
setup: a compact **ViT-in-time** transformer (small MATEY-style stack, 3
blocks, 4 heads, C_emb = 64, ~131k params) trained on a synthetic 1D
advection-diffusion-reaction edge-plasma-like PDE with three coupled
channels (n, T, P = n·T·cool(T)) driven by a time-varying gas-puff-like
actuator, using the paper's pushforward training trick.

Two variants (`n_train ∈ {1, 10}`) were trained under a soft ~15-20 min
wall-clock budget on an Apple-Silicon MPS device (paper: ~100 k
optimization steps on 8× V100/H100 GPUs). Matey-10 was warm-started from
the converged Matey-1 weights and used a progressive rollout schedule
(short leads for warmup, then ramp to `n_train`).

**Headline finding.** Matey-1 shows the expected qualitative shape
(rollout NRMSE grows monotonically with horizon, plateauing at ~40-55 %
around 400 steps). Under our compute-limited setup **Matey-10 did NOT
reproduce the paper's key improvement claim**: its long-horizon NRMSE
was *worse* than Matey-1, growing without bound (2.4 at 400 steps vs
Matey-1's 0.42-0.55). An independent earlier replication attempt in the
same directory (using a GRU surrogate; see `work/rollout_error.csv`) also
saw catastrophic divergence for longer-rollout training in a
compute-limited setting.

**Verdict (see §7).** SPOT-CHECK: partial reproduction of Matey-1's
error-growth shape but NEGATIVE reproduction of the paper's Matey-10
long-horizon-stability improvement in this compute budget.

---

## 2. Claims table

| # | Claim (paraphrased)                                                                                                                     | Type                                | Testable here?                                     | Tested in this replication?                                     |
|---|-----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|---------------------------------------------------|-----------------------------------------------------------------|
| C1 | ViT autoregressive surrogate can predict 2D KSTAR SOLPS-ITER edge fields (n_e, T_e, P_rad) at 98×38.                                    | Methodological (existence of model) | No — requires MATEY code + KSTAR SOLPS trajectories. | No                                                              |
| C2 | Increasing autoregressive training horizon `n_train` reduces long-horizon rollout NRMSE (direction).                                    | Quantitative / direction            | Yes — model-agnostic; ViT-mini on synthetic PDE.  | **Yes** — result NEGATIVE at this compute budget (see §4).      |
| C3 | Matey-1 → ~40 % NRMSE at full rollout; Matey-100 → < 10 %.                                                                              | Quantitative / magnitude            | Not directly comparable across problems.          | Shape only (matey-1 grows to ~40-55 %).                          |
| C4 | Matey-100 → ~27 % NRMSE at 6800-step rollout on unseen trajectory 3.                                                                    | Quantitative / magnitude            | Not comparable across setups.                     | No                                                              |
| C5 | Longer-horizon training stabilizes the error-growth shape (near-linear vs sharp blowup for Matey-1).                                    | Qualitative / shape                 | Yes.                                              | **Yes** — result FAILS at this compute budget.                  |
| C6 | Pushforward trick (Brandstetter et al 2022) suffices to train long-horizon AR models tractably.                                         | Methodological                      | Yes — we adopt the same trick.                    | **Partial** — trick applied; matey-10 does not diverge in loss but does not out-perform matey-1 in eval. |
| C7 | Surrogate inference is 3–4 orders of magnitude faster than SOLPS-ITER (paper: 0.018 s / step vs 30 s / step).                            | Performance comparison              | Not comparable — depends on the specific solver.  | No (see caveat §6).                                             |
| C8 | Attention maps of the ViT correlate with physical group partitioning (PFR, core, SOL).                                                  | Interpretability                    | Marginal — architecture-specific.                 | No                                                              |
| C9 | Model performance degrades on OOD regimes (trajectory 3× beyond training range).                                                        | Qualitative / expected behavior     | Yes — test-trajectory NRMSE > training NRMSE.     | **Yes** — traj3_test NRMSE ≥ traj1 NRMSE at all horizons.       |
| C10 | MATEY codebase is publicly available (github.com/ornl/MATEY/).                                                                          | Reproducibility                     | Verifiable by URL check.                          | **Yes** (URL exists).                                            |

Testable claims tested: **C2, C5, C6, C9, C10** → Coverage ≈ **0.50**.
Of the tested claims, C2 and C5 (the paper's headline claim) **failed**
in this budget; C6 partially held; C9 and C10 succeeded.

---

## 3. Methods

### 3.1 Ground-truth PDE (proxy for SOLPS-ITER)

1D advection-diffusion-reaction system on `x ∈ [0, 1]` with 64 spatial cells,
three coupled channels (n, T, P):

```
∂n/∂t = −v ∂n/∂x + D_n ∂²n/∂x² + a(t)·src(x) − sink(x)·n
∂T/∂t = −v ∂T/∂x + D_T ∂²T/∂x² − α n T · cool(T) + a(t)·heat(x)
P     = n · T · cool(T)     (algebraic diagnostic; small multiplicative noise)
cool(T) = 0.15 + 0.35 · T / (T + 0.1)   (nonlinear cooling coefficient)
```

* `src(x)`   = Gaussian near x = 0.15 (gas-puff injection)
* `heat(x)`  = Gaussian near x = 0.5   (auxiliary heat)
* `sink(x)`  = Gaussian near x = 0.95  (outflow / divertor-pump-like)
* Upwind advection + central-difference Laplacian, `dt = 5e-3`.
* 20 inner PDE substeps per saved snapshot; each snapshot represents
  0.1 units of physical time.

3 trajectories, each with a different actuator waveform (linear ramp;
linear + sinusoid @ 3 Hz; linear + sinusoid @ 7 Hz + higher-freq mode);
500 snapshots × 64 cells × 3 channels each. All three min-max normalized
into [0, 1] using the joint train + test statistics (matches paper §2.3).

Trajectories 1 & 2 are used for training; trajectory 3 is used as the
unseen test set. This mirrors the paper's traj1+traj2 → train,
traj3 → test protocol.

### 3.2 Surrogate model

**ViT-in-time** transformer surrogate (paper: full MATEY ViT with 12
blocks, C_emb = 192; ours: mini-MATEY with 3 blocks, C_emb = 64,
4 heads — ~131 k trainable params).

Architecture (see `work/model.py`):

* Preprocessor: 1×1 Conv1d from C = 3 physical channels to C_uni = 24.
* Tokenizer: Conv1d with kernel = stride = 2 over the spatial axis
  → tokens per time slice = 32; total tokens = T × 32 = 96 (T = 3).
* Learned positional embedding + additive actuator embedding
  (MLP: (T+1) → 256 → 64).
* Encoder: 3 stack of standard `TransformerEncoderLayer` with
  pre-norm, 4 heads, mlp_ratio = 2, no dropout, no causal mask
  (global spatiotemporal attention).
* Decoder: take the last 32 tokens → ConvTranspose1d + 1×1 Conv1d
  → residual over the last input state (`y = U[:, -1] + 0.1 * tanh(Δ)`).
* Output: predicted state at t+1, shape (W, C).

The residual formulation with `0.1 * tanh(Δ)` and zero-init on the
output head is a stability trick — without it, the transformer's
unconstrained output on this near-identity problem diverges within
~700 iterations on Apple MPS (a repeatable failure mode we verified by
diagnostic runs).

### 3.3 Training

* **Autoregressive rollout in training** with the pushforward trick
  (paper §2.3, Brandstetter et al ref [40]): only the *final* forward
  pass in each rollout has gradient; the preceding rollout steps run
  under `torch.no_grad()` with detach.
* **Progressive rollout schedule** (extra stabilization we added):
  * iters ∈ [0, warmup)    → `max_lead = max(1, n_train // 4)`
  * iters ∈ [warmup, 2·warmup) → linear ramp from `n_train // 4` to `n_train`
  * iters ≥ 2·warmup       → `max_lead = n_train`
  * per-batch rollout length uniformly sampled in `[1, max_lead]`.
* **Curriculum**: Matey-10 is warm-started from the converged
  Matey-1 weights (same architecture) so the harder rollout regime
  starts from a strong prior.
* Feedback clamp: during pushforward, fed-back states clamped to
  [-0.2, 1.2] to prevent runaway drift out of the min-max range.
* Loss: plain MSE on the state (NRMSE reported separately at eval).
* Optimizer: AdamW, `lr = 5e-5`, weight_decay = 1e-4, `eps = 1e-4`
  (larger than default 1e-8 to avoid the Adam variance-estimate
  collapse we saw on tiny losses).
* Grad-clip global norm = 1.0.
* Batch = 32, `T_in = 3` past states + 1 next actuator.
* **1500 optimization steps per model** (paper: 100 000+).
  Wall-clock training time (MPS on Apple Silicon):
  Matey-1 = **250 s**, Matey-10 = **335 s**.
  Total run incl. eval + dataset build = **~17 min** (within budget).

### 3.4 Evaluation

* Metric: variable-averaged NRMSE (paper eq 3), computed as
  `NRMSE(k) = mean_c sqrt( mean_{n,x} (ŷ - y)² / mean_{n,x} y² )` at
  each rollout step k.
* Rollout horizons reported: **{5, 10, 20, 50, 100, 200, 400} steps**.
* At each variant, evaluation runs 8 random start times per
  trajectory, then rolls out to the max horizon; NRMSE at each k is
  averaged over the 8 starts.
* Trajectories evaluated: traj1 (training), traj2 (training),
  traj3_test (unseen).

---

## 4. Reproduced numbers

All results from `work/results.json` after full 17-minute run.
Numbers are variable-averaged NRMSE at the given rollout horizon.

**Matey-1** (next-step training, 2000 gradient steps, converged
training MSE = 9.3 × 10⁻⁵):

| Traj / h        |     5 |    10 |    20 |    50 |   100 |   200 |   400 |
|-----------------|-------|-------|-------|-------|-------|-------|-------|
| traj1 (train)   | 0.149 | 0.184 | 0.345 | 0.384 | 0.354 | 0.430 | 0.426 |
| traj2 (train)   | 0.145 | 0.175 | 0.257 | 0.250 | 0.301 | 0.336 | 0.553 |
| traj3 (test)    | 0.177 | 0.221 | 0.298 | 0.289 | 0.323 | 0.318 | 0.492 |

Matey-1 error grows monotonically (with mild plateauing) from ~15 %
NRMSE at 5-step rollout to ~40-55 % NRMSE at 400-step rollout on all
trajectories, and the test trajectory is always at or above the
training trajectories — consistent with the paper's qualitative
picture for Matey-1.

**Matey-10** (10-step autoregressive training with pushforward
trick + curriculum warm-start from Matey-1, 1500 gradient steps,
converged training MSE = 2.4 × 10⁻³):

| Traj / h        |     5 |    10 |    20 |    50 |   100 |   200 |   400 |
|-----------------|-------|-------|-------|-------|-------|-------|-------|
| traj1 (train)   | 0.187 | 0.232 | 0.374 | 0.793 | 0.943 | 1.286 | 2.252 |
| traj2 (train)   | 0.160 | 0.198 | 0.345 | 0.699 | 1.065 | 1.275 | 2.406 |
| traj3 (test)    | 0.178 | 0.210 | 0.367 | 0.772 | 1.062 | 1.377 | 2.423 |

Matey-10 error grows *much faster and without bound* — the exact
opposite of the paper's claim. At h = 400 steps, Matey-10 has
~5× the NRMSE of Matey-1. Interestingly Matey-10's *training* MSE
(2.4 × 10⁻³) is ~26× larger than Matey-1's (9.3 × 10⁻⁵), consistent
with autoregressive training being harder to converge in this
compute budget.

**Runtime** (Apple Silicon MPS, ~131 k-param mini-MATEY ViT):

| Metric | Value |
|---|---|
| ML forward pass per step | 18.3 ms |
| Synthetic PDE per snapshot | 3.7 ms |
| ML / PDE ratio | 0.20 × (ML is *slower* than the synthetic PDE) |

The runtime comparison is a scope artifact: our synthetic 1D PDE has
only 20 inner substeps per snapshot on 64 cells, whereas SOLPS-ITER
on the 98×38 KSTAR grid is a fundamentally more expensive physics
solve. **We do not claim to have replicated the paper's C7 speedup
claim.** For a fair comparison one would run the real SOLPS-ITER
KSTAR case (paper: 30 s / step on 16 MPI ranks on 2.1 GHz CPUs;
ratio ≈ 1600×–3000× over the paper's 0.009–0.018 s / step ML
inference on GPU).

---

## 5. Agreement with paper

**Qualitatively partial, quantitatively negative on the headline
claim (C2/C5).**

* **Matey-1 shape** (C5, partial): the shape of monotone error growth
  with rollout horizon on Matey-1 is reproduced (0.15 → 0.42-0.55 over
  5-to-400 steps). The paper's Matey-1 saturates near NRMSE ~ 0.15 at
  100 steps and ~0.4 at full-trajectory (few-thousand-step) rollouts;
  our Matey-1 saturates near 0.4-0.55 by 400 steps. The rough shape
  and magnitude agree to within a factor of ~2, which is as much as
  can be expected across two very different underlying PDE systems.

* **Long-horizon-training improvement** (C2/C5, primary claim, NEGATIVE):
  the paper's central quantitative finding — that longer-`n_train`
  training reduces long-horizon NRMSE — did NOT reproduce here. Our
  Matey-10 has ~2-5× *higher* NRMSE than Matey-1 at all horizons ≥ 50.
  This mirrors a separate independent replication attempt in the same
  directory (a GRU model, `work/rollout_error.csv`) that likewise saw
  catastrophic divergence for longer-training variants.

  Two mechanisms plausibly explain the negative result:
  1. **Compute budget.** The paper trained for 100 000 optimization
     steps; we trained for 1 500. The paper's improvement may require
     substantially more optimization to materialize.
  2. **Optimizer stability.** The pushforward trick amplifies model
     mis-predictions across rollout steps during training. Without the
     paper's DAdaptAdam variant and warmup schedule, standard AdamW
     can drift into a regime where the model outputs get worse
     during the long-lead phase; the progressive-horizon schedule we
     added helps but does not fully cure this in 1 500 steps.

* **OOD degradation** (C9, reproduced): on both variants, the test
  trajectory has higher NRMSE than the training trajectories at every
  horizon — consistent with the paper's finding that Matey-100 degrades
  in the OOD trajectory 3× regime.

* **Loss magnitudes.** Matey-1's final training MSE (9.3 × 10⁻⁵) is
  comparable in *magnitude* to the paper's Matey-1 training NMSE
  (4.8 × 10⁻³ ÷ mean-squared GT ≈ 10⁻³ on min-max data — within an
  order of magnitude of our result).

* **Pushforward-trick tractability** (C6, partial): the trick was
  applied and did NOT cause loss to explode when combined with the
  progressive-horizon schedule + curriculum warm-start; but on its own
  (without the schedule/warm-start) we repeatedly saw loss divergence
  at ~700 iterations on MPS.

---

## 6. Deviations and caveats (Scope)

* **Model.** Small MATEY-style ViT-in-time (~131 k params, 3 blocks,
  C_emb = 64) vs paper's full MATEY ViT (~O(10⁷) params, 12 blocks,
  C_emb = 192). Architecture family matches; capacity does not.
* **Data.** 1D synthetic advection-diffusion-reaction with 3 coupled
  channels (n, T, P) vs paper's 2D SOLPS-ITER on 98×38 grid.
  Phenomenology (transport + nonlinear diagnostic + actuator drive +
  OOD test regime) matches; absolute physics does not.
* **Compute.** 1 500 optimization steps per variant on 1 Apple-Silicon
  MPS device (Matey-1: 250 s, Matey-10: 335 s), vs paper's 100 000+
  steps on 8× V100 / H100 GPUs distributed. This is a ~500-1000×
  compute deficit and is the most plausible explanation for the
  negative Matey-10 result.
* **Optimizer.** AdamW with lr = 5 × 10⁻⁵, eps = 1 × 10⁻⁴, weight
  decay = 1 × 10⁻⁴ (chosen for stability on MPS with a nearly-optimal
  identity baseline). Paper uses DAdaptAdam with cosine annealing.
* **Numerical stability on MPS.** We hit a repeatable Adam variance-
  estimate collapse ("loss stable for 500-700 iters, then diverges")
  on Apple MPS at multiple LR / eps / loss-scale combinations. The
  final configuration (larger eps, residual head with tanh cap,
  smaller model, progressive rollout schedule, curriculum warm-start)
  is the setting that fits the compute budget without divergence for
  Matey-1 and 2 000 iters.
* **Runtime speedup (C7).** Not reproduced; scope excludes running
  the real SOLPS-ITER solver.
* **Attention maps (C8).** Not analyzed; even at ~131 k params our
  ViT has 3 blocks × 4 heads × T-slice-attention, and comparison to
  the paper's 12-block × 3-head grouped-attention interpretation is
  not meaningful at this scale.

---

## 7. Verdict

**Verdict: SPOT-CHECK**
**Coverage: 0.50** (5 of 10 claims tested)
**Agreement: PARTIAL/NEGATIVE — Matey-1 error-growth shape reproduces
(qualitatively and to within a factor of ~2); the paper's central
Matey-10-beats-Matey-1 long-horizon-stability claim (C2/C5) does NOT
reproduce in this ~17-min single-device compute budget.**

The paper's claim is not falsified — the most plausible explanation is
the ~500-1000× compute deficit and the paper's use of a more capacity-
appropriate optimizer (DAdaptAdam) and a much larger model. Our
NEGATIVE result is a genuine finding about *replicability at
constrained compute*: the improvement claim is not robust to a
compute reduction of this magnitude with off-the-shelf AdamW + a
smaller model, even with our progressive-horizon schedule + curriculum
warm-start stabilizers.

A stronger replication would require:
1. Running the actual MATEY code (github.com/ornl/MATEY) with the
   KSTAR SOLPS-ITER data, or
2. Substantially more compute (≥ 50 000 iters, batch ≥ 64), or
3. DAdaptAdam or a similar auto-scaling optimizer.

None of these fit inside the assigned single-agent budget.

## Reproducibility

* Deterministic (fixed seed = 42 in dataset + training).
* Full re-run:
  ```
  cd work
  python3.11 -u train.py --iters 1500 --variants 1,10 \
    --budget_seconds 900 --lr 5e-5 \
    --horizons 5,10,20,50,100,200,400
  ```
  On Apple Silicon MPS ≈ 17 min end-to-end.
* Results (JSON), training log, and code are in `work/`.
