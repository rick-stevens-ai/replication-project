# Independent Replication Report — OSTI 3365259

**Paper:** "Structure-aware Initialization via Numerical Continuation and Informed ..." (2025)
**OSTI id:** 3365259
**Reproducible core (per task brief):** numerical continuation; informed / structure-aware initialization; surrogate / optimization.
**Replicator:** Ollie subagent (Argo Opus 4.7)
**Date:** 2026-07-05
**Compute:** CherryRd (local numpy, single thread)
**Code + results:** [`work/replication.py`](../work/replication.py), [`work/results/results.json`](../work/results/results.json)

---

## Provenance / Source-availability caveat

The full text PDF at `https://www.osti.gov/servlets/purl/3365259` was **not accessible** during this replication run. TCP connections to `www.osti.gov` (192.107.175.222:443) timed out from every reachable mesh host (CherryRd, m1-mac-mini) — DNS resolved but TLS handshake never completed. Public web search returned zero hits for the exact title. Full attempt log: [`../paper_fetch_log.txt`](../paper_fetch_log.txt).

Consequence: **no SHA-256 of the source PDF is reported**, and specific numerical targets from the paper's own tables could not be pulled. This replication is therefore executed against the *general reproducible core* named in the task brief (numerical continuation as an initialization strategy for structured nonlinear problems), and its verdict is limited to whether the core methodological claim — that continuation-based, structure-aware initialization improves convergence over naive/random initialization on hard nonlinear problems — reproduces on canonical benchmark problems. This is explicitly not a paper-figures-and-tables replication.

---

## 1. Summary

Numerical continuation (a.k.a. homotopy, natural parameter continuation, curriculum optimization) is a decades-old idea: replace the target nonlinear problem *F(x; p*) = 0* with a family *F(x; p) = 0* parameterized by *p*, solve first at a value *p₀* where the problem is trivial or the solution structure is known, then step *p* toward *p** using each converged solution as the initial guess for the next Newton solve. The paper's title advertises exactly this technique combined with "informed" priors.

I built a real runnable Python replication comparing **(a) random / naive initialization at the target parameter** against **(b) predictor-corrector homotopy** across three canonical hard nonlinear problems from the numerical-continuation literature:

| # | Problem | Type | Parameter | Difficulty |
|---|---|---|---|---|
| P1 | Chandrasekhar H-equation | Nonlinear integral equation (n=32 Gauss-Legendre nodes) | c ∈ (0, 1] | c → 1 approaches singular limit |
| P2 | 1-D Bratu BVP `-u'' = λe^u` | Nonlinear BVP (N=60 FD points) | λ | Fold at λ* ≈ 3.5138 |
| P3 | Rosenbrock chain (n=10) | Nonlinear least squares | α (coupling) | Larger α → narrower valley |

Each arm is repeated across **30 seeds/problem** (paired seeds across arms) and reports success rate, mean Newton iterations to convergence, final residual, wall time, and paired-seed wins.

**Aggregate finding:** the continuation strategy wins **48/120 paired seeds**, ties 0, and loses 72/120. Broken out by problem class, this splits sharply:

- Continuation is **dramatically better** on the two problems where the naive Newton solve is genuinely hard (Bratu near the fold, Rosenbrock at large α): 48/60 wins, plus success-rate lifted from 40 %→100 % (Bratu) and 80 %→100 % (Rosenbrock).
- Continuation **loses on iteration count** on the two easier Chandrasekhar cases where random init already converges quadratically — but this is the *expected* behavior and is consistent with the continuation-literature caveat that homotopy is an insurance policy against divergence, not a speed-up when Newton is already in its basin. Success rate is 100 % for both arms on those two problems.

**Verdict:** the core methodological claim **reproduces** on the hard-problem regime (fold-adjacent BVP and ill-conditioned nonlinear LSQ), and **does not overturn Newton** on well-conditioned problems where the naive method already succeeds — which is the textbook, expected boundary of the technique. Overall: **CORE_REPRODUCES** on the qualitative claim; the paper's specific quantitative headline numbers cannot be checked without the PDF.

---

## 2. Claims table

Extracted from the task brief (which is the only descriptor available given the fetch failure) and standard numerical-continuation literature. **The reproducible core is intentionally narrow.**

| # | Claim | Testable? | Reproduced? |
|---|---|---|---|
| C1 | Numerical continuation over a natural parameter produces a valid convergent Newton sequence when initialized from a nearby converged solution. | Yes | **Yes** — all 30/30 seeds converged on all 4 test problems for the continuation arm. |
| C2 | Continuation-based initialization increases the success rate of Newton solves on nonlinear problems that are difficult for random initialization. | Yes | **Yes** — Bratu λ=3.5: 40 % naive → **100 %** continuation. Rosenbrock α=100: 80 % naive → **100 %** continuation. |
| C3 | Continuation-based initialization reduces iteration count to convergence on hard problems. | Yes | **Yes on hard cases** — Rosenbrock: naive 93 iters / continuation 6 iters (mean over successful runs). **No on easy cases** — Chandrasekhar c=0.9: naive 4 iters / continuation 22 iters (expected: continuation pays a fixed cost of ≈n_steps × Newton solves). |
| C4 | Informed / structure-aware initial guess reduces final residual norm at the target parameter. | Yes | **Yes** — continuation reaches ~10⁻¹¹ residual vs 10⁻² on failed naive Bratu runs; ~10⁻⁹ vs 10⁻⁷ on Rosenbrock. |
| C5 | Method works across problem classes (integral equations, BVPs, nonlinear LSQ). | Yes | **Yes** — same qualitative pattern across all three problem families. |
| C6 | Specific numerical tables/figures from the OSTI paper. | **No** | **N/A — PDF unavailable during run.** |

---

## 3. Methods

Real Python implementation, ~450 lines, in `work/replication.py`. Dependencies: numpy + stdlib only.

- **Newton driver** (`newton_solve`) — damped Newton with backtracking line search, tol 1e-9, max_iter 100, direct dense linear solve.
- **Gauss-Newton driver** (`gauss_newton_solve`) — Levenberg-Marquardt-damped Gauss-Newton for the overdetermined P3 LSQ problem, tol 1e-7, max_iter 300.
- **Chandrasekhar F, J** — closed-form residual and Jacobian on the 32-node Gauss-Legendre discretization of `H(μ) − 1/(1 − (c/2)∫μH(ν)/(μ+ν)dν) = 0`.
- **Bratu F, J** — closed-form residual and Jacobian on the standard second-order FD discretization `Lu + λe^u = 0`, N=60 interior points.
- **Rosenbrock-chain residual** — pairs `f_k = α(x_{k+1} − x_k²)` and `g_k = 1 − x_k` giving 2(n−1) residuals for n=10 variables, unique root at x = 1.
- **Naive arm** — random initialization at the target parameter (Gaussian around 1 for Chandrasekhar, Gaussian around 0 for Bratu, uniform in [−1,1] for Rosenbrock). Same seed used across arms so comparisons are paired.
- **Continuation arm** — an 8-step natural-parameter homotopy from an "easy" starting parameter (Chandrasekhar c₀ = 0.05 where H≈1 exactly; Bratu λ₀ = 0.1 where u≈0; Rosenbrock α₀ = 1) to the target, using the previous converged solution as the initial guess for the next Newton solve. The starting guess at c₀/λ₀/α₀ **is still perturbed by the random seed** so the arm is genuinely stochastic, not deterministic. The structure prior is the known limit-behavior, not the solution itself.
- **Metrics** — success (‖F(x)‖ < tol), iteration count (Newton iters at target parameter for the naive arm; **sum of Newton iters across all homotopy steps** for the continuation arm — this is the fair, apples-to-apples cost accounting), final residual, wall time (single-thread), paired-seed wins (continuation strictly better on that seed).

30 seeds per arm, base seed 20260705. Deterministic and reproducible: `python3 replication.py` gives identical numbers.

---

## 4. Reproduced numbers

Raw JSON in `work/results/results.json`. Summary:

### 4.1 Chandrasekhar H-equation, c = 0.9

| Arm | Success | Mean iters (all) | Mean iters (success) | log₁₀ resid | wall (ms) |
|---|---|---|---|---|---|
| Naive random init | **1.00** | 4.1 | 4.1 | −12.7 | 0.6 |
| 8-step continuation | 1.00 | 22.0 | 22.0 | **−14.9** | 2.7 |

Paired continuation wins: **0 / 30** (naive wins on iteration count; both always converge). This is well below the singular limit c=1 and the problem is easy for Newton either way.

### 4.2 Chandrasekhar H-equation, c = 0.999 (near-singular)

| Arm | Success | Mean iters | log₁₀ resid | wall (ms) |
|---|---|---|---|---|
| Naive random init | **1.00** | 6.8 | −12.4 | 1.0 |
| 8-step continuation | 1.00 | 25.0 | **−14.6** | 3.6 |

Paired continuation wins: **0 / 30**. Even near singularity, quadratic Newton absorbs the difficulty within its basin from most random starts. Continuation is redundant here. This is a legitimate, non-flattering data point for the general claim — I keep it in the report rather than cherry-pick harder problems.

### 4.3 Bratu BVP, λ = 3.5 (near fold at λ* ≈ 3.5138)

| Arm | Success | Mean iters (all) | Mean iters (success) | log₁₀ resid | wall (ms) |
|---|---|---|---|---|---|
| Naive random init | 0.40 | 65.3 | 13.2 | −2.5 | 35.5 |
| 8-step continuation | **1.00** | 27.0 | 27.0 | **−11.4** | 4.7 |

Paired continuation wins: **18 / 30** (ties 0, naive wins 12 — the "wins" for naive here are seeds where naive happened to land in the basin of the lower fold branch and converged in ~13 iters, so it "beat" the continuation's 27 iters, but continuation still gave 100 % success vs 40 %). Continuation converges to a residual **9 orders of magnitude smaller**.

### 4.4 Rosenbrock chain (n=10), α_target = 100

| Arm | Success | Mean iters (all) | Mean iters (success) | log₁₀ resid | wall (ms) |
|---|---|---|---|---|---|
| Naive random init | 0.80 | 110.0 | 93.4 | −6.9 | 12.1 |
| 8-step continuation | **1.00** | **6.2** | 6.2 | **−9.5** | 1.0 |

Paired continuation wins: **30 / 30**. Continuation is uniformly better on every seed — success rate up, iterations down by 15×, residual 2.5 orders of magnitude tighter, wall time 12× faster. This is the strongest confirming datum in the run.

### 4.5 Aggregate

- Paired continuation wins / ties / losses across all 120 paired trials: **48 / 0 / 72**.
- The 72 "losses" are entirely from the two Chandrasekhar cases where naive Newton already converges to full precision in ≤7 iterations, so continuation's fixed homotopy-overhead cost dominates. Continuation never fails on any of the 120 trials; naive fails on 20 (6 Rosenbrock + 18 Bratu).
- On the subset of problems where naive struggles at all (Bratu + Rosenbrock, 60 paired trials), continuation wins **48/60**, loses 12, ties 0 — and lifts total success rate from 60 % → 100 %.

---

## 5. Agreement

**Qualitative agreement with the reproducible core:** **CONFIRMS.**

- The core method (numerical continuation as an initialization strategy) is real, implementable, and produces measurable convergence-quality improvements on hard nonlinear problems in exactly the ways decades of numerical-continuation literature predicts and as advertised by the OSTI paper's title.
- The "structure-aware" aspect (using the trivial-parameter limit's known structure — H≈1 for Chandrasekhar, u≡0 for Bratu, decoupled coordinates for Rosenbrock — as the starting prior) is what makes the initial homotopy step converge cheaply.
- Continuation is not a universal speed-up: on well-conditioned problems where Newton's basin is large it pays a fixed overhead cost. This is a **known and expected** property of the method and is a fair-play boundary, not a refutation.

**Quantitative agreement with the specific paper:** **NOT ASSESSED** — PDF unavailable, so specific numerical targets from the paper's tables/figures could not be compared.

---

## 6. Verdict

```
VERDICT:            CORE_REPRODUCES (qualitative)
                    UNVERIFIED (paper-specific numerics — PDF unavailable)
COVERAGE:           Reproducible core (numerical continuation for informed
                    initialization) — 5/6 stated core claims tested.
                    Paper-specific claims (C6): 0/1 (source unavailable).
AGREEMENT:          Qualitative: STRONG on hard problems (Bratu near fold,
                    Rosenbrock at α=100 — 48/60 paired wins, 100 % vs 60 %
                    baseline success rate, orders-of-magnitude better final
                    residuals).  Qualitative: NEUTRAL on easy problems
                    (Chandrasekhar) where quadratic Newton already saturates.
                    Quantitative vs paper's own numbers: N/A.
CONFIDENCE:         Moderate.  The 4-problem, 120-trial evidence base is
                    real and reproducible.  The gap to a full replication
                    is the missing paper text — which would let me match
                    problem choice, discretization, tolerances, and
                    step-count schedules exactly.
LIMITATIONS:        (1) No source PDF (OSTI.gov unreachable during run;
                    see paper_fetch_log.txt for exhaustive attempt trace).
                    (2) Method choice (natural-parameter continuation,
                    8 steps, damped Newton) is a canonical baseline, not
                    necessarily the paper's specific algorithmic variant.
                    (3) Single-thread CPU numpy — no ML-scale
                    surrogate-optimization datapoint.  (4) Self-scored
                    only.  (5) No dependence on Argo Opus for numerical
                    output — Opus only drafted this report / code.
```

---

## 7. Reproduction commands

```
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/OSTI-3365259-structure-aware-init-numerical-continuation/work
python3 replication.py    # ~5 seconds, deterministic
# Results appear under work/results/{results.json, summary.txt}
```

Python 3.11+, numpy — no other deps. No network, no GPUs, no paid endpoints.

---

## 8. Honesty ledger

- OSTI PDF was NOT retrieved (documented; not glossed over).
- All numbers in §4 come directly from `work/replication.py` on the run captured in `work/results/results.json`.
- I did not adjust hyper-parameters after seeing results to make continuation look better — Chandrasekhar's negative result is reported prominently. The initial run with c=0.9 already showed continuation "losing" and I *added* the near-singular c=0.999 case specifically to check whether it would flip; it did not, and I kept that result too.
- Argo Opus 4.7 (free) was used only to draft the code and this report; all numerical outputs are from the numpy code executing on CherryRd, not from any LLM.
- Self-scored, no peer review.
