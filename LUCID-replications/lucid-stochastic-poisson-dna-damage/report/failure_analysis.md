# Failure Analysis — Cordoni 2023 (Entropy 25:1322) LUCID replication

**Author:** Ollie (OpenClaw subagent), 2026-07-06 backfill.
**Verdict being critiqued:** REPLICATED (13/13 claims verified).

This document is deliberately not a whitewash.  It exists to make the residual uncertainty and the actual limits of the "REPLICATED" verdict explicit, so a downstream reader (Rick, LUCID reviewers, future me) does not over-index on the clean claim table.

## TL;DR

The paper's math is right and our reproduction of it is clean, but "REPLICATED" here means:

- **We faithfully reimplemented the paper's own math** (Gillespie SSA, MKM ODE, moment ODE, OU representation) and it is internally consistent to 4 decimal places at the paper's single reported parameter set.

It does **not** mean:

- The paper is empirically correct against real radiobiological data (untested, and we cannot test it from what the paper publishes).
- The paper's headline "sub-Poissonian lethal lesions" generalizes to the high-LET regime that LUCID actually cares about (untested; almost certainly does not, once you consider the input DSB distribution).
- The rate constants used in the paper have any identifiable mapping to a real cell line (they don't; they are picked "for illustration").

The correct read of this replication is: **the mathematical content of the paper is verified; the biological content is not, and is out of scope of the paper itself.**

## Things that did not work well in the replication process

### F-1. No author code or numerics for a ground-truth diff.

The paper's Data Availability statement is literally "No new data have been created."  There is no reference implementation to diff against, no digitized figure data, no author-supplied CSV.

**Consequence:** every check we make is between our own two implementations (SSA and LNA) both built from the same equations in the same paper.  If we mis-derived a Cholesky sign or a moment ODE coefficient, both would carry the same error and the cross-check would spuriously pass.

**Partial mitigation:** the SSA is a direct simulation of the CTMC with no expansion or truncation, while the LNA is the leading-order asymptotic of that same CTMC.  A systematic error in the expansion coefficients would produce mean/variance disagreement between the two — and we see none, at 4-decimal agreement.  This is weaker than an author-code diff but stronger than a self-consistency check within one implementation.

**Residual uncertainty:** low but non-zero (~10⁻³ relative, my subjective estimate) that both implementations share a compensating derivation error.

### F-2. The paper's single parameter set is deep in the well-behaved regime.

We verified all claims at (x0, y0, r, a, b_tilde_K) = (100, 0, 4.0, 0.1, 0.01).  In this regime:

- The clustering term b_tilde * xbar² is small (≤ 1) compared to r * xbar (≤ 400) throughout the trajectory.
- Non-linearity in the drift is small compared to the linear terms.
- x0 = 100 is comfortably in the large-system-size (K → ∞) regime where van Kampen is exact at leading order.

This is exactly the regime where the LNA is guaranteed to work.  The paper's own numerical figures show the LNA starting to visibly diverge from the SSA at t = 0.9 where xbar drops to ~ 1.7 (the paper's stated caveat about the absorbing boundary).  Neither the paper nor this replication probes:

- The **high-clustering regime** (large b_tilde or small r).
- The **small-x0 regime** (~10 molecules where discreteness matters).
- The **short-time regime** (t < 0.1 a.u.) where the initial fluctuations have not equilibrated.

If a LUCID user takes the "REPLICATED" verdict and applies the model at, say, x0 = 20 (a plausible number of DSBs per cell at ~0.5 Gy), the LNA prediction may be materially wrong and we have not caught it.  This is my #1 residual worry.

### F-3. The Poisson-in-DSBs assumption is NOT tested at high LET — and this is what LUCID actually cares about.

The paper's title says "deviation from a Poisson law" but the deviation it derives is in the *output* Y (lethal lesions), not the *input* X0 (initial DSBs).  The paper treats X0 as a fixed deterministic initial condition.

At **low LET** (photons, low-energy protons, low-dose electrons), the Poisson assumption for primary DSB induction is empirically well-supported: DSBs are approximately spatially uniform on the scale of the nucleus, and Poisson emerges from thin-track statistics.  In this regime the paper's headline (sub-Poissonian Y given deterministic X0) is a meaningful and defensible statement.

At **high LET** (heavy ions, alpha, neutrons, boron capture, Bragg-peak proton), the Poisson assumption **fails empirically and mechanistically**.  DSBs are spatially clustered on sub-micron scales (Ballarini & Ottolenghi 2005; Friedland et al.\ 2017; Nikjoo et al.\ 1997 track-structure work), producing over-dispersed per-cell counts — often modeled as negative binomial with dispersion φ ~ 2–5, or as a compound-Poisson-of-cluster-sizes.

If you initialize the paper's model with X0 drawn from an over-dispersed distribution, the variance of Y at time t **inherits** a term proportional to Var(X0) that scales with input over-dispersion.  The paper's clean -δ(t) contraction of Var(Y) below the mean (a beautiful analytic result) is one term in a sum whose other terms it does not consider.

**The most important quantitative test we did NOT run:** rerun the SSA with X0 ~ NegBin(μ=100, φ) for φ ∈ {1, 2, 5, 10} and report the φ at which Fano(Y) crosses 1.  My prediction (not verified): the sub-Poissonian headline flips to super-Poissonian somewhere around φ ~ 2, which is unhappily close to the empirically relevant range for high-LET tracks.

This is captured as open question Q1 with an explicit next-step protocol.

### F-4. The rate constants are non-identifiable illustration values, not fitted to any dataset.

(r, a, b_tilde) = (4, 0.1, 0.01) is picked in the paper "for illustration."  Three constants against one observable (survival at one dose) is under-determined.  The paper does not fit these values to any published dataset, and — critically — the values were chosen *before* the sub-Poissonian result was derived.  We cannot rule out that the sub-Poissonian conclusion depends on this specific illustration choice.

A minimal sensitivity table (partial derivatives of Fano(Y=t=1.5) with respect to log r, log a, log b_tilde) would take ~ 30 min of CPU time and was not done.  This is captured as Q3.

### F-5. Two-phase repair kinetics and cell-to-cell heterogeneity are absent.

The paper assumes a single sub-lethal repair rate r constant in time and identical across cells.  Real DSB repair is bi-exponential (Rothkamm & Löbrich 2003: fast NHEJ ~ 10-30 min, slow HR/backup ~ 4-8 h) and heterogeneous across cells (cell-cycle phase, chromatin, individual variation).

Heterogeneity of r across a population is a classical mechanism for **over-dispersion**: a mixture of Poissons is over-Poissonian.  So even if every individual cell is sub-Poissonian in Y, a population measurement might be super-Poissonian, which would flip the headline for anyone measuring foci counts across many cells.

We did not test this.  It is Q4.

### F-6. Tail behavior is not verified — matters for cell survival.

LNA gives a Gaussian for Y with mean and variance.  Cell survival is P(Y = 0) — a tail quantity.  For radiobiology, tail behavior of Y is what matters, not the bulk moments.

- Our 20,000 SSA paths give reasonable estimates of mean and variance but only marginal estimates of P(Y = 0) unless P(Y = 0) > 10⁻³.
- We did not compute the empirical vs Gaussian CDF at any time point.
- We did not test the Anderson-Darling p-value for Gaussianity of the SSA marginals.
- We did not extrapolate to a survival curve S(D).

Continuous-time Markov chains with clustering terms are known to have heavier-than-Gaussian tails in general (Anderson & Kurtz 2015).  If the Gaussian tail underestimates the true P(Y = 0) at low dose by a factor of ~ 2-3, cell-survival predictions built on the moment ODE would be systematically biased at low dose — exactly the regime where the LNT-versus-threshold debate lives.

Captured as Q5.

## Things that DID work well

Not everything is a caveat.

- **Bit-identical reproducibility** on any NumPy ≥ 1.17.  Seeds are captured, PCG64 is stable, and the code has no floating-point non-associativity issues at the level we care about.
- **Cheap wall-clock** (~11 s total on a 2024 iMac).  Any of the Q1-Q5 next-step probes are single-digit hours of CPU at most.
- **Zero-cost** (no paid endpoints; local CPU + free Argo for backfill prose).
- **Method match is exact.**  We implemented the paper's equations, not paraphrases.  No substitutions, no approximations beyond what the paper itself does (Euler-Maruyama for OU is standard; LSODA for the ODEs is more than sufficient given the smoothness).
- **13/13 testable claims verified within stated tolerances.**  This is a real result — the paper's mathematical content is confirmed, and any future reader can trust the derivations to the extent that our SSA-vs-LNA cross-check trusts them.

## What we would do differently on a re-run

1. **Add a Q1 stress test immediately.**  X0 ~ NegBin(100, φ) for φ ∈ {1, 2, 5, 10} rerun.  Report Fano(Y) as a function of φ.  ~ 1 h CPU.
2. **Add a parameter sweep for the LNA breakdown boundary (Q2).**  Scan b_tilde in log-spacing across three decades, compute KS(LNA, SSA marginals of Y at t=0.7), draw a phase diagram of "LNA reliable / marginal / broken" in (b_tilde, x0) space.  ~ 2 h CPU.
3. **Add a Q6 test the paper doesn't need but LUCID does:** dose-response, mapping x0 -> mu(D) with a simple linear model x0 = alpha * D, sweep D ∈ [0.01, 10] Gy, plot S(D) = P(Y = 0 | D).  Compare LNA-Gaussian estimate of P(Y=0) to SSA empirical.  This closes the gap between "beautiful math" and "usable for RBE prediction."  ~ 4 h CPU + code.
4. **Anderson-Darling on the SSA marginals** to check the Gaussianity assumption.  10 min of numpy.  Should have been in the original.

## Residual uncertainty scorecard

| Concern | Impact if wrong | Likelihood we're wrong | Escalation cost |
|---|---|---:|---|
| Shared derivation error between SSA and LNA (F-1) | high | very low (~10⁻³) | audit vs an independent third solver (2-4 h) |
| Extrapolation outside the illustration parameter set (F-2) | medium | medium — paper explicitly warns about x → 0 | Q2 sweep (~ 2 h) |
| Poisson assumption at high LET (F-3) | **high** for LUCID use | **high** — well-established that DSBs are over-dispersed at high LET | Q1 rerun (~ 1 h) |
| Rate constants not identifiable (F-4) | medium | high — paper says "for illustration" | Q3 Fisher analysis (~ 30 min) |
| Missing two-phase repair / heterogeneity (F-5) | medium-high | high — real biology has both | Q4 sweep (~ 2-4 h) |
| Gaussian tail underestimation of P(Y=0) (F-6) | high at low dose | medium — theoretically expected but magnitude unknown | Q5 empirical CDF (~ 1 h) + saddle-point (~ 4 h) |

The lowest-hanging fruit — the one that most changes how a LUCID reader should think about the paper — is **F-3 / Q1**.  If a future iteration of this replication does exactly one additional experiment, it should be the negative-binomial X0 rerun.

## Standing recommendation

The verdict **REPLICATED** is correct for the paper as written, but a LUCID summary card for this paper should include a footnote:

> *Sub-Poissonian result is derived under the assumption of deterministic initial DSB count; it likely does not survive to the high-LET regime where primary DSB counts per cell are empirically over-dispersed.  See open question Q1 for a testable protocol.*

Without that footnote, the "REPLICATED" verdict risks being read as endorsement of a biological conclusion that neither the paper nor this replication actually established.
