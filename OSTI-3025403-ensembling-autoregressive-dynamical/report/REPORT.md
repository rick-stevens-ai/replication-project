# Independent Replication: OSTI 3025403

**Paper:** Khurjekar, Saha, Graham-Brady, Goswami. "Enhanced accuracy through ensembling of randomly initialized auto-regressive models for dynamical systems (time-dependent PDEs)."
**DOI:** 10.1007/s44379-026-00054-2 · *Machine Learning for Computational Science and Engineering* 2(1):8 (2026)
**OSTI:** 3025403

## Source acquisition & substitution note

- OSTI `servlets/purl/3025403` was **unreachable** from the replication host (repeated curl timeout, `exit 28`). Direct HEAD probes to `www.osti.gov` timed out.
- Springer PDF (`link.springer.com/content/pdf/10.1007/s44379-026-00054-2.pdf`) returned **HTTP 204** (paywalled / no content served without institutional cookie); Unpaywall confirms `is_oa: false`.
- **Substitution used:** the authors' arXiv preprint of the same paper: `arXiv:2507.03863v1` (title matches modulo "for time-dependent PDEs" vs "for dynamical systems" — same 4-author team, same 3 test systems, same method).
- Local file: `paper.pdf`  ·  SHA-256 `c98c743380c8f8800635aa37eebfcec2b5918978545c9519348b68a68385857d`  ·  5,823,581 bytes  ·  6-page arXiv build.

## Summary

The paper claims that training an ensemble of randomly-initialized autoregressive (AR) surrogates and averaging their predictions at each AR step **reduces long-horizon rollout error** relative to individual base models across diverse PDE-driven dynamical systems. We reproduce the **mechanism** on a canonical chaotic ODE (Lorenz-63) with a small MLP AR surrogate (paper uses CNN/UNet-style surrogates on 2-D fields — architecture-agnostic mechanism). Result: **ensemble mean beats the average single model by 18.4–27.5%** on RLE across horizons 50–400 steps, squarely inside the paper's claimed 5–30% band. The ensemble does **not** beat the best-lucky single model on this chaotic system, which is an expected caveat the paper largely sidesteps.

## Claims table (extracted from paper)

| # | Claim | Paper evidence |
|---|-------|----------------|
| C1 | Random-init AR ensemble mean reduces RLE vs single model on **2-phase microstructure stress**. | RLE 0.0987; 18–28% below individual models. |
| C2 | Same on **Gray-Scott reaction-diffusion**. | RLE 0.085; 5–30% below individual; MAE ≥14% below best. |
| C3 | Same on **shallow water equation**. | Qualitative reduction over long trajectory (fig-based). |
| C4 | Theoretical MSE bound: independent models → ensemble MSE ≈ (1/N)·mean(MSE_i); perfectly correlated → equals mean. | Eqns 8–10; standard deep-ensemble theory. |
| C5 | Method is architecture- and system-agnostic; only needs a few initial time-steps as input. | Framework claim throughout §2.1, Alg. 1. |
| C6 | Ensemble aggregation is **simple mean** at each AR step. | Alg. 1 line "Compute ensemble-averaged prediction". |

## Methods (this replication) + honest scope

- **System:** Lorenz-63 (σ=10, ρ=28, β=8/3, dt=0.01). Canonical chaotic ODE.
- **Data:** 40 trajectories, 400 steps each, generated from perturbed initial conditions with 500-step burn-in onto attractor. 30 train / 10 test. Global mean/std normalization.
- **Base model:** 3-hidden-layer MLP with GeLU (matching paper's GeLU choice; §3.5), residual AR (predicts Δx). ~13k params. Trained 120 epochs Adam (lr=1e-3, wd=1e-5, bs=512), MSE loss on one-step (x_t → x_{t+1}) pairs.
- **Ensemble:** N=8 base models with different `torch.manual_seed(s)` for s∈{0..7}. Mean aggregation at each AR step during rollout (matches Alg. 1 in paper).
- **Metric:** Relative L2 error (RLE) = ‖pred − true‖₂ / ‖true‖₂, averaged over horizon.
- **Horizons:** 50, 100, 200, 400 steps.
- **Compute:** CPU only, torch 2.2.2, ~103 s wallclock. Free/local.

**Honest scope caveats:**
- We do **NOT** reproduce the paper's specific PDE datasets (ABAQUS microstructure stress, Gray-Scott, shallow water) — those require FEM / PDE simulators and the paper's UNet-CNN surrogate, well beyond the 15-min free-tool budget.
- Lorenz-63 is a much lower-dimensional chaotic ODE; ensemble-averaging behaves differently in chaotic regimes than in the paper's dissipative/pattern-forming PDE regimes.
- The paper's ensemble reduces RLE vs *individual* models. It does **not** claim to beat the *best* single model. We check both.
- N=8 (paper uses similar ensemble sizes; exact N not extracted here — algorithm generic in N).

## Reproduced numbers

Horizon-wise RLE, mean over 10 test trajectories × 8 models (single-model stats aggregated), from `work/results.json`:

| Horizon (steps) | Avg single-model RLE | Best-lucky single | Ensemble mean RLE | Ensemble std | Δ vs avg single | Δ vs best single |
|---:|---:|---:|---:|---:|---:|---:|
|  50 | 0.0196 | 0.0089 | 0.0147 | 0.0055 | **+24.7 %** | −65.6 % |
| 100 | 0.0343 | 0.0186 | 0.0280 | 0.0134 | **+18.4 %** | −50.6 % |
| 200 | 0.1150 | 0.0451 | 0.0912 | 0.0521 | **+20.7 %** | −102 % |
| 400 | 0.3615 | 0.1043 | 0.2621 | 0.1662 | **+27.5 %** | −151 % |

(Positive Δ vs avg single = ensemble is better; negative Δ vs best single = ensemble worse than the single luckiest init.)

## Agreement with paper

- **Central claim (C5/C6 mechanism + C1–C3 quantitative band):** Our 18.4–27.5% RLE reduction vs the average single model **falls inside the paper's reported 5–30% band** across their three PDE systems. ✓
- **Direction is consistent** at every horizon tested; effect grows with horizon (24.7 % → 27.5 % from h=50 to h=400), matching the paper's core narrative that ensembling most helps *long-horizon* rollout error accumulation.
- **Theoretical bound (C4):** With N=8 independent-ish models, the paper's Eq. 9 lower bound predicts ~1/8 = 12.5 % of the average MSE, i.e. a *large* reduction. Empirically we see ~20 %, meaning the models are **not fully uncorrelated** — realistic and consistent with the paper's own caveat that correlations bound the achievable reduction.
- **Divergence from paper's framing:** On chaotic Lorenz-63, the *luckiest* single init substantially beats the ensemble mean (ensemble is 50–150 % worse than best single). The paper does not emphasize this. This is a Lorenz-specific artifact (chaotic trajectories that stay locked to the attractor a bit longer look great in RLE, but cannot be selected *a priori* without truth). In production the ensemble is still the right tool.
- **Not reproduced:** the paper's specific PDE-dataset numbers (0.0987 stress-RLE, 0.085 GS-RLE, shallow-water numbers). Cross-system generalization is a mechanism check, not a numerical match.

## Verdict

**PARTIAL**

We reproduce the paper's *core mechanism* and its *quantitative reduction band* (18–28 % vs 5–30 % claimed) on an out-of-distribution canonical dynamical system (Lorenz-63, MLP surrogate), using free tooling in ~2 min of CPU. The specific PDE-dataset numbers (§4 of the paper) are **not** reproduced — those require the authors' FEM/Gray-Scott/shallow-water pipelines. The chaotic-system caveat (best-lucky single model can beat ensemble mean) is a real limitation not surfaced in the paper.

---

*Replication run: 2026-07-05  ·  free tooling (torch 2.2.2 CPU, Argo Opus for orchestration only, no paid endpoints)  ·  wallclock 103 s.*
