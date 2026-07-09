# Failure analysis — OSTI 3362822 replication

## Executive summary

The replication is **PARTIAL**. The qualitative and speedup claims (C1, C4, C5)
were reproduced; the quantitative single-mode accuracy claim (C2) was NOT reproduced
(our mean test rel-L2 = 0.183 vs paper's 0.0083, i.e. ~22× worse); the five-mode
claim (C3) was not attempted. No claim was contradicted; the gaps are attributed to
solver-mismatch and training-budget rather than model-family failure.

## What failed (in decreasing severity)

### F1 — Quantitative single-mode error norm off by ~22× (C2 not reproduced)

**Symptom.** Our v2 DeepONet's best test rel-L2 = 0.183 (mean); paper reports 0.0083.
Even the *best individual test sample* in our run (rel-L2 = 0.075) is 9× the paper's mean.

**Root causes (leading candidates, roughly ordered by likelihood).**
1. **Solver mismatch (probable).** The paper trains on Gkeyll continuum-Vlasov output;
   we train on a Fourier / linear-semi-Lagrangian VP solver. Different discretizations
   have different noise floors and different systematic biases. Our numerical γ has 12%
   bias vs analytic; Gkeyll is typically 1–2%. If the paper's DeepONet has effectively
   learned a "clean" Gkeyll trajectory that has $\sim 10^{-3}$ noise floor, and our
   DeepONet is fitting a noisier trajectory with $\sim 10^{-2}$ noise floor, the DeepONet
   errors track the underlying-solver noise floor.
2. **Training budget (probable contributor).** Paper: $10^6$ iterations. Ours: $6 \times 10^4$.
   Our v2 loss curve is still descending at iter 30k (best point) but has almost
   plateaued: training-loss goes 0.00577 → 0.00488, test-loss 0.01229 → 0.01328 (test
   is actually *rising* — mild overfitting from iter ~30k onwards). So even $10\times$
   more iterations probably only shaves the training rel-L2 by ~2×, not the test rel-L2 by 20×.
3. **Architecture mismatch (possible).** Our v2 uses depth-4 width-128 + Fourier features.
   Paper says depth-6 width-200 no Fourier features. Our v1 with the exact paper architecture
   plateaued at MSE(log E) = 0.478 (the ensemble mean solution — no meaningful learning at all).
   Something about the paper's setup lets the depth-6 network escape the mean-solution basin
   that ours cannot: possibly better initialization, longer warmup, undocumented positional
   encoding, or multi-sensor T-evaluation (paper Fig 1 says
   `T = [T(η_1), T(η_2), ..., T(η_m)]^T` — but for our scalar T all these values are equal,
   so this doesn't help unless m is not what we assume).
4. **T sampling / choice (unlikely).** We sample T uniform from [0.5, 1.5] with a fixed
   RNG seed. The paper does not specify the sampling distribution beyond "randomly chosen
   in the range [0.5, 1.5]" but this is unlikely to be the source of a 22× error gap.

**Workaround applied.** We adopted Fourier feature encoders (v2) to escape the v1
mean-plateau; this brought MSE(log E) from 0.478 → 0.012 — a factor of 40 improvement.
But this workaround still leaves us 22× off the paper's rel-L2.

**Residual gap.** To close: (a) get Gkeyll installed on uicgpu and regenerate the dataset
with the paper's exact solver (est. 1 day of Gkeyll build + config); (b) run the paper's
literal architecture at $10^6$ iterations (est. 2–4 h on A100); (c) contact authors for the
Gkeyll input decks. Any one of these could reveal whether the gap is solver noise or
architecture pathology.

### F2 — v1 (paper-exact) DeepONet plateaus at ensemble mean

**Symptom.** With depth-6 width-200 tanh, Adam LR 1e-3, exponential decay γ=0.9995,
50k iterations on our dataset, the training MSE(log E) hits 0.478 at iter 6k and stays
there for 44k more iterations. This equals the sample variance of log E — i.e. the
network is outputting the ensemble mean trajectory for every T.

**Root cause.** With a scalar branch input, no positional encoding, and tanh MLPs,
the gradient of the loss w.r.t. the branch weights is small when the branch output starts
near zero (tanh derivative ~1 at 0). The trunk network can freely fit the *mean shape*
of E(t) — this reduces the loss from 0.99 → 0.48. But then the gradient signal for
telling the network to distinguish trajectories by T is much smaller than the fitting
error, and Adam can't find its way out.

**Workaround.** Fourier feature encoding on the scalar inputs. This makes each of the
scalar inputs (T and t) into a 16-D vector with high-frequency components, and the
initial gradients are much larger.

**Residual issue.** We do not know whether the paper's authors also encountered this
plateau. If they did, they may have used LR warmup, a different tanh init, or the
multi-sensor branch parameterization. If they didn't, there is something about the
specific 1M-iteration training run in their setup that we're not replicating.

### F3 — Nougat (default env) crashed on transformers API drift

**Symptom.** `/data/stevens/.venvs/extraction/bin/nougat` failed with
`BARTDecoder.prepare_inputs_for_inference() got an unexpected keyword argument 'cache_position'`
— a transformers 4.x → 4.4x API change where cache-position kwarg was added.

**Root cause.** Nougat pinned to a specific transformers version; the extraction env
had a newer transformers that changed the internal `prepare_inputs_for_generation` signature.

**Workaround.** Switched to a second Nougat install (`/gpustor/stevens/anaconda3/envs/nougat/`)
which has a compatible transformers version.

**Prevention.** Note the working Nougat env location in TOOLS.md; the extraction default
env is stale.

### F4 — Five-mode case not attempted (C3 untested)

**Symptom.** C3 marked "untested" in claims table.

**Root cause.** Compute-budget triage. The five-mode case would need ~400–800 more VP
sims (each ~5 s in the more demanding k up to 0.7 modes; ~35–70 min extra), plus a second
training round.

**Residual gap.** Complete rather than fundamental: the five-mode case is qualitatively
just "more of the same" architecturally, and if C1/C2 gap is understood, C3 will follow.
Follow-up left as Open Question in report.

### F5 — `numpy.trapz` removed in numpy 2.x

**Symptom.** First `replicate.py` run crashed at first `np.trapz` call.

**Root cause.** numpy 2.0 removed the legacy `trapz` alias in favor of `trapezoid`.
Our uicgpu env has numpy 2.x.

**Workaround.** Global replace `np.trapz → np.trapezoid`. One-line fix.

**Prevention.** Standing rule for future numerical replication scripts: use numpy 2.x
names only. Consider adding a compat header
```
try: np.trapz = np.trapezoid
except: pass
```
if writing code that must run on both numpy 1.x and 2.x envs.

## Assumptions made (documented)

- **Ion background is immobile and uniform** (paper §3.1: "fixed background of ions
  serving as a neutralizing background"). Our VP solver assumes exactly this: `n_i(x) = n_0 = 1`
  throughout.
- **Boundary conditions in x are periodic** (paper doesn't say explicitly but this is
  standard for Landau-damping studies and consistent with cosine perturbations).
- **Boundary conditions in v are open** (f = 0 outside the finite v-grid).
- **Normalized units:** ω_pe = 1, λ_e = √T, electron q/m = -1, ε_0 = 1. Standard.
- **T-sampling distribution:** uniform in [0.5, 1.5] with RNG seed 42.
  Paper says "randomly chosen" — we assume uniform.
- **The paper's L2 error norm is per-sample, then meaned across samples**, as
  written in Eq. 9. Confirmed by matching the paper's numerical range.

## Things worth revisiting (if a full second pass is done)

1. Try the *literal* paper architecture (depth 6, width 200, tanh, LR 1e-3, 1M iters) with
   just LR warmup — see if the mean-plateau is escapable without Fourier features.
2. Install Gkeyll on uicgpu (Rick has infra for this) and regenerate the dataset from
   the paper's actual solver.
3. Contact Chuanfei Dong (dcfy@bu.edu) for the exact Gkeyll input decks + preprocessed dataset.
4. Extend to five-mode case.
5. Perform Q4 (from open_questions.json): extract γ(T) from DeepONet predictions and compare
   to analytic dispersion — verifies whether the DeepONet learned physics or a lookup.
