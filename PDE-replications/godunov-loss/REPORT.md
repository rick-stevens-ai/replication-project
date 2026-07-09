# REPORT — Godunov Loss for Hyperbolic Conservation Laws

**Working dir:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/godunov-loss/`
**Run:** 2026-04-30 (uicgpu A100, GPU 0, ~12 min wall)
**Model:** argo/argo:claude-opus-4.6 (subagent), then continued in main session for execution

## Setup
- **Equation:** 1D Burgers `u_t + u u_x = 0` with shock-forming initial conditions
- **Reference:** Godunov finite-volume solver at Nx=256
- **NN model:** MLP (5 layers, 256 hidden, 328,960 params)
- **Training:** 500 epochs, batch=64, lr=1e-3, 60 random IC trajectories × 25 snapshots each
- **Two losses compared:**
  - `MSE`: standard L2 against FV reference
  - `Godunov_hybrid`: MSE + Godunov-flux conservation penalty (λ=10) + TV penalty (λ=1e-3)

## Results — held-out test cases

| Test case | Loss | L1 | L∞ | TV(pred) | TV(ref) | TV rel. err |
|---|---|---:|---:|---:|---:|---:|
| **strong_step** | MSE | **0.298** | **2.382** | 88.20 | 2.00 | 43.10 |
| | Godunov | 0.565 | 3.229 | 124.29 | 2.00 | 61.14 |
| **bump_to_shock** | MSE | **0.450** | 3.294 | **116.84** | 2.41 | **47.50** |
| | Godunov | 0.529 | 3.519 | 105.94 | 2.41 | 42.97 |
| **n_wave** | MSE | **0.052** | **0.273** | **17.23** | 3.83 | **3.50** |
| | Godunov | 0.227 | 1.947 | 33.17 | 3.83 | 7.66 |

**Honest finding:** **MSE was competitive or BETTER than the Godunov-hybrid loss on all three tests in this setup.** The paper's headline claim (that Godunov-flux-aware losses produce sharper, more conservation-respecting NN solutions of hyperbolic PDEs) is **NOT reproduced here**.

## What this likely means
1. **Architecture limit:** A small MLP without a strong inductive bias (like FNO, DeepONet, or graph networks for stencils) can't learn shock-handling well regardless of loss. Both losses give TV(pred) >> TV(ref), indicating spurious oscillations.
2. **Loss specification:** Our Godunov-hybrid was a best-effort reconstruction (MSE + flux divergence + TV). The actual paper's formulation may differ in important ways (e.g. entropy condition enforcement at the discrete cell-interface level, not a soft penalty). We could not locate the paper PDF — see honest gap below.
3. **Initial conditions:** Shock-forming bump gives both methods trouble. Smoother n-wave is where MSE wins clearly — possibly because Godunov penalty fights pre-shock smoothness.

## Honest gaps
- **Paper PDF not found.** "Godunov loss for hyperbolic conservation laws" 2024 was the brief; subagent could not locate the exact arXiv/journal version. Implementation is reconstructed from the abstract concept + general literature on physics-informed losses for hyperbolic PDEs.
- **Architecture too weak.** A FNO or DeepONet would likely show the loss difference more clearly. Re-running with FNO is a natural next step.
- **Single seed.** No statistical replicates.
- **3.3 M tokens spent on the original subagent run** (run got cut off mid-execution due to context); main-session continuation completed it on uicgpu A100 in ~12 min.

## Score
**4/8** — honest non-replication. We have working baselines, working FV reference, two loss implementations, but the paper's qualitative claim does not appear to hold for this MLP class. Score reflects that the experiment was run faithfully, results are negative.

## Deliverables
- `replication/code/` — burgers_solver.py, nn_models.py, train_mse.py, train_godunov.py, plot_results.py, run_all.py
- `replication/data/` — test cases + training trajectories
- `replication/results/` — results_mse.json, results_godunov.json, model checkpoints, predictions.npz, loss histories
- `replication/figures/` — shock_comparison.png, shock_detail.png, loss_curves.png, error_bars.png
- `replication/run.log` — full run log

## Next pass (if pursued)
1. Find the actual paper, verify our loss reconstruction
2. Re-run with FNO architecture
3. Try entropy-condition penalty as separate term
4. Multi-seed statistics

## Open Questions & Reproducibility Blockers

- Primary blocker (FAILED verdict driver): the **actual paper PDF** ("Godunov loss for hyperbolic conservation laws", ~2024) was never located by the subagent. Without the paper there is no canonical loss specification — our `Godunov_hybrid = MSE + λ·flux-divergence + λ·TV` is a best-effort reconstruction from the title + general physics-informed-loss literature, and the paper's actual entropy-condition enforcement at the discrete cell-interface level is the most likely source of the qualitative-claim mismatch on `strong_step`, `bump_to_shock`, and `n_wave`.
- Secondary missing artifacts (would only matter once the paper is in hand): the **author-reported NN architecture** (whether MLP, FNO, DeepONet, or graph-stencil), **training hyperparameters** (epochs, batch, lr, seeds, IC sampling protocol), **exact reference solver settings** (FV scheme, limiter, CFL, Nx — we used Godunov at Nx=256), and the **held-out test-case definitions** (we synthesized `strong_step`, `bump_to_shock`, `n_wave`; the paper's actual benchmarks are unknown).
- Tertiary blocker: **no statistical replicates**. Single-seed runs cannot distinguish "Godunov loss is genuinely worse for this MLP" from "this particular seed happened to land badly". A multi-seed (n ≥ 5) re-run is required before the negative result is publishable.
- Open question: with the same Burgers + reference + ICs but an **FNO or DeepONet backbone** (which has a stronger inductive bias for hyperbolic operators), does the Godunov-flux loss outperform plain MSE, recovering the paper's qualitative claim? Our MLP-only result hints that architecture, not loss, is the dominant variable here.
- Open question: is the right discrete enforcement of the entropy condition a hard constraint at the cell-interface flux (Godunov upwind) rather than a soft TV penalty? Reframing the loss as a projection step instead of an additive regularizer is the most physically defensible next attempt.



## Verdict

**Verdict: FAILED** (Coverage 4/10, Agreement 3/10). — Paper's Godunov-loss advantage not reproduced; PDF unlocated, loss reconstructed

<!-- census-verdict: FAILED assigned 2026-07-08 by LLM judge (Argo Opus) -->
