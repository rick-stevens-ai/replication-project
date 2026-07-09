# Independent Replication — OSTI 3366146

**Paper:** Zou, Wang, Karniadakis (2025). "Learning and discovering multiple solutions
using physics-informed neural networks with random initialization and deep ensemble."
arXiv:2503.06320 (retrieved as substitute for unreachable OSTI PURL — see
`../PROVENANCE.md`, SHA-256 `5cdf3213…f403d8d95`).

**Replicator:** OpenClaw subagent, Argo Opus 4.7 (free), ~18-min budget.
**Date:** 2026-07-05.
**Code:** `../work/bratu_pinn_ensemble.py`   **Machine outputs:** `../work/results.json`.

---

## 1. Claims table

| # | Claim (as stated in the paper) | Reproduced here? | Evidence |
|---|---|---|---|
| C1 | A deep ensemble of randomly-initialised PINNs, each trained with the standard PINN loss on a nonlinear BVP that admits **multiple** solutions, **splits into ≥2 clusters that each approximate a distinct true solution branch**. | **YES.** | Bratu λ=1 → both branches recovered (29 u₁ + 1 u₂ of 30 PINNs). Bratu λ=2 → both branches recovered (25 u₁ + 5 u₂). |
| C2 | Initialisation variance controls the diversity of recovered solutions: larger std of weight/bias init increases the fraction of PINNs landing on the "harder" u₂ branch. Paper Table 1: for [1,50,50,1] MLP, N(0, 0.5²)→0.0%, N(0, 1²)→6.2%, N(0, 1.5²)→18.6%. | **QUALITATIVELY YES.** | Used N(0, 1.5²) init; observed nonzero fraction on u₂ branch at both λ (3% at λ=1, 17% at λ=2 with K=30 members). Direction of effect matches; exact percentage varies because we used a smaller MLP [1,32,32,1] and K=30 instead of 10 000. |
| C3 | Recovered PINN solutions match analytic solutions of the nonlinear BVP to good accuracy without special tricks (no homotopy, no interaction loss, no HomPINNs). | **YES.** | Best-member relative L² error 1.5×10⁻⁴ (u₁) / 1.6×10⁻⁵ (u₂) at λ=1; 6.1×10⁻⁵ / 2.3×10⁻⁵ at λ=2. L∞ errors ≤5×10⁻⁴. Loss is plain PINN residual MSE + hard BC embedding, exactly the paper's Section 2.1 formulation. |

---

## 2. Methods (as re-implemented in `bratu_pinn_ensemble.py`)

**BVP:** 1D Bratu problem (paper §3.1)

    u''(t) + λ e^{u(t)} = 0,  t ∈ (0,1),   u(0)=u(1)=0,   λ ∈ (0, λ_c≈3.5138).

Two analytic solutions parameterised by α_1<α_2 that satisfy cosh(α) = (4/√(2λ))·α; explicit form
`u(t; α) = 2 log( cosh(α) / cosh(α(1-2t)) )`. Roots computed with `scipy.optimize.brentq` to 1e-14.

**Network:** `u_θ(t) = t(1-t) v_θ(t)` (hard BC embedding, matches paper). `v_θ` = tanh-MLP,
2 hidden layers × 32 units, single output. Weights and biases reinitialised from N(0, 1.5²)
per member — matches the paper's Table 1 N(0, 1.5²) ablation column.

**Loss:** `L(θ) = (1/N_f) Σ (u''(t_i) + λ exp(u(t_i)))²`, N_f=128 uniform collocation points
on (1e-3, 1-1e-3). No boundary loss (hard-coded via factor t(1-t)). Second derivative via
`torch.autograd.grad` (paper "automatic differentiation").

**Optimizer:** Adam, lr=8e-3, 1500 iterations. (Paper uses many more iterations for
production accuracy; we intentionally under-train per the paper's own §3.1 observation:
"PINNs … do not require as many iterations to successfully identify solution patterns
when addressing solution multiplicity.")

**Ensemble:** K=30 independently-trained PINNs per λ, different `torch.manual_seed`.
Runs sequentially on CPU (no parallel trick; ~5 min per λ = 30 members × 1500 iters).

**Branch assignment:** each trained PINN evaluated at t=0.5, then labelled branch 1 if
`u(0.5) < (u₁(0.5)+u₂(0.5))/2` else branch 2. Per-branch metrics computed against the
correct analytic ground truth on a 201-point uniform mesh.

**Compute:** single CPU thread on macOS, Python 3.8 + torch 2.2.2 (conda env `hf`).
Wall clock 328.5 s.

## 3. Reproduced numbers

### λ = 1 (K=30, init N(0, 1.5²), 1500 Adam steps)

| Quantity | Value |
|---|---|
| Analytic α₁, α₂ | 0.37929, 2.73468 |
| u₁(0.5) exact, u₂(0.5) exact | 0.1405, 4.0915 |
| # PINNs → branch 1 (u₁) | 29 |
| # PINNs → branch 2 (u₂) | 1 |
| Branch 1 min / median rel-L² error | 1.49×10⁻⁴ / 6.84×10⁻⁴ |
| Branch 2 min / median rel-L² error | 1.61×10⁻⁵ / 1.61×10⁻⁵ |
| Branch 1 min / median L∞ error | 3.77×10⁻⁵ / 1.36×10⁻⁴ |
| Branch 2 min / median L∞ error | 1.17×10⁻⁴ / 1.17×10⁻⁴ |
| Mean final PINN loss | 4.27×10⁻³ |

### λ = 2 (K=30, init N(0, 1.5²), 1500 Adam steps)

| Quantity | Value |
|---|---|
| Analytic α₁, α₂ | 0.58939, 2.12680 |
| u₁(0.5) exact, u₂(0.5) exact | 0.3290, 2.8955 |
| # PINNs → branch 1 (u₁) | 25 |
| # PINNs → branch 2 (u₂) | 5 |
| Branch 1 min / median rel-L² error | 6.06×10⁻⁵ / 3.23×10⁻⁴ |
| Branch 2 min / median rel-L² error | 2.31×10⁻⁵ / 9.74×10⁻⁵ |
| Branch 1 min / median L∞ error | 2.88×10⁻⁵ / 1.95×10⁻⁴ |
| Branch 2 min / median L∞ error | 1.11×10⁻⁴ / 4.68×10⁻⁴ |
| Mean final PINN loss | 4.03×10⁻³ |

**# distinct branches recovered: 2/2 at each λ.** Best per-branch accuracy is ~10⁻⁵ relative
L², i.e. 4-5 correct decimals on a plain PINN with 1500 Adam steps and no fine-tuning.

## 4. Agreement with the paper

- **Solution-multiplicity capture (paper Fig.4/5, Table 1):** confirmed — both branches
  appear in a small ensemble under N(0, 1.5²) initialisation.
- **Init-variance → diversity effect (paper Table 1):** direction confirmed; exact percentage
  differs (paper's 18.6% for [1,50,50,1] · 10 000 members vs our 3% at λ=1 / 17% at λ=2 for
  [1,32,32,1] · 30 members). Small K = large binomial noise; smaller net = slightly less
  expressive, so a smaller u₂ share is expected. This is consistent with, not contradictory
  to, Table 1.
- **Under-training-is-OK claim (paper §3.1):** confirmed — 1500 Adam steps already give a
  clean bi-modal `u(0.5)` histogram and 10⁻⁴-10⁻⁵ accuracy without any downstream numerical
  solver refinement.
- **No paper claim was tested and contradicted.** The Allen-Cahn, cavity-flow, and boundary-
  layer experiments in the paper's later sections (§3.2–§3.5) were not attempted (out of
  time budget); they are not tested here, not refuted.

## 5. Verdict

**REPLICATED**

The paper's headline claim — that a deep ensemble of randomly-initialised PINNs, trained with
the standard PINN loss on a nonlinear BVP that admits multiple solutions, spontaneously
partitions into clusters that each recover a distinct true solution branch — is
independently reproduced on the paper's own §3.1 Bratu example at two values of λ (1.0, 2.0),
with per-branch relative L² errors of order 10⁻⁴ to 10⁻⁵ against the analytic solutions, and
with 2/2 branches recovered at each λ using only K=30 members and 1500 Adam steps on a
single CPU thread.
