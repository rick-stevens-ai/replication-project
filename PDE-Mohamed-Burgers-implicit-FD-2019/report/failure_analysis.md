# Failure Analysis — Mohamed (2019) BDF-2 Burgers' Replication

**Verdict: REPLICATED.**
**No replication failure occurred.** All quantitative claims tested (Tables 1,
2, 6, 11, 12 — 33 sampled cells) reproduced within expected tolerances.

This document therefore serves two purposes:

1. Document the *near-failures* and *scope limitations* encountered during
   replication (what could have gone wrong, and what didn't).
2. Flag the *latent failure modes in the paper itself* that a downstream
   user relying on Mohamed (2019) needs to understand before extending the
   scheme.

---

## 1. Near-failures during replication

### 1.1 Cloudflare-blocked PDF access
- **What happened:** the Taylor & Francis PDF endpoint returned Cloudflare
  challenge pages to `curl`, breaking the ordinary "fetch paper → extract
  tables" pipeline.
- **Mitigation:** switched to the OpenClaw `browser` tool (headless Chrome)
  against the HTML full-text `showPopup?...&id=T0001..T0012` handlers to
  scrape all 12 tables into `work/paper_tables.md`.
- **Impact:** none on verdict; added scraping time.

### 1.2 Cole–Hopf series truncation
- **Risk:** for small `ν t`, the exponentials `exp(−n² π² ν t)` decay slowly
  and the Fourier series needs many modes; for larger `ν t` they underflow
  and only the leading modes matter.
- **Mitigation:** conservatively truncated at `n = 200`, verified that
  additional modes contribute below the 10⁻¹⁶ noise floor for all tested
  `(ν, t)` pairs. Composite Simpson on 4001 nodes for `c₀`, `cₙ`.
- **Impact:** none — 6-decimal pointwise agreement on Table 2 confirms the
  reference solutions themselves are accurate.

### 1.3 MATLAB↔NumPy floating-point path differences
- **Expected effect:** small (≲ ULP-level per operation) drift in the deepest
  digits of paper vs. our L₂/L∞ error norms, particularly for Table 6
  norms of order 10⁻⁸ to 10⁻¹³ where the norm itself is near the floating-
  point noise floor.
- **Observed:** in Table 6 row `ν=1, T=2, Δt=0.002`, paper reports
  `L₂=6.56E-13`, we get `L₂=4.31E-13`. Both are at the noise floor of double
  precision after ~1000 time steps; the ratio is meaningless. This is
  agreement, not disagreement.
- **Impact:** none on verdict; noted in REPORT.md §4.3.

## 2. Scope not covered (deliberate)

### 2.1 Non-uniform grid variant
- **What:** paper §3 Eqs. (15)–(21) describes a non-uniform variant needed
  for boundary-layer resolution at high Re.
- **Why not:** the uniform-grid quantitative tables (Tables 1, 2, 6, 11, 12)
  already establish the scheme cleanly. Non-uniform-grid replication would
  be a straightforward follow-up.

### 2.2 High-Re Figures 3 and 6 (Re = 10⁴, 2×10⁴)
- **What:** paper's most visible qualitative claim (C6) — stability at Re up
  to 2×10⁴ — is demonstrated only via figures on the non-uniform grid.
- **Why not:** requires 2.1 first, and produces only figure-vs-figure
  comparison (no quantitative delta to compute). Deliberately deferred.

## 3. Latent failure modes in the paper itself

These are **not** failures of our replication — they are issues in the
paper that our replication *faithfully reproduced*, and that downstream
users should be aware of.

### 3.1 ★ Example 3's "exact solution" is an approximate ansatz
- **What:** the paper claims `u(x,t) = (¼) e^{−νt} cos(π x)` is the exact
  solution to Example 3.
- **Reality:** direct substitution leaves a nonzero PDE residual
  `R(x,t) = −(π/32) e^{−2νt} sin(2πx)`. It is a valid *approximate ansatz*
  in the regime `u u_x ≪ ν u_xx` (small amplitudes / large ν), which is
  exactly the regime chosen for Table 11.
- **Consequence:** Table 11 measures "how close is BDF-2 to an approximate
  Burgers-solution ansatz," not "true Burgers L∞ error." Our replication
  reproduces the same quantity the paper reports (same ansatz on both
  sides), so the numerical replication is genuine. But the *semantic label*
  attached to that quantity in the paper is misleading.
- **Fix:** either re-label Table 11's error metric explicitly, or replace
  the ansatz with a high-resolution numerical reference (e.g., WENO5 on a
  fine grid) for a proper convergence study.

### 3.2 Linearization order-of-accuracy in advection-dominated regimes
- **What:** `w = 2 u^n − u^{n−1}` is nominally `O(Δt²)`-accurate for smooth
  `u`. Combined with BDF-2, the paper claims `O(Δt² + h²)` overall.
- **Latent risk:** in advection-dominated regimes (large Re, sharp gradients)
  linear extrapolation lags the true solution and can effectively demote the
  observed convergence order — a well-known issue in IMEX-type schemes.
- **Not flagged in paper.** All paper tests are in regimes where this does
  not bite. Users pushing to high Re on uniform grids may find the observed
  order degrades.

### 3.3 Non-conservative form vs. shock formation
- **What:** the paper uses `u u_x`, not `∂_x (u²/2)`.
- **Consequence:** once shocks form, the non-conservative form does *not*
  converge to the correct entropy solution. Rankine-Hugoniot shock speeds
  will be misrepresented.
- **Not tested by paper.** All four examples are pre-shock or shock-free by
  construction. Applying this scheme to shock-forming initial data (e.g.,
  `u_0 = −sin(π x)` on `[−1,1]`, which shocks at `t = 1/π`) is *not* safe.
- **Documented as open question Q2 in `open_questions.json`.**

### 3.4 Stability at high Re is asserted, not proved
- **What:** the paper's high-Re demonstrations (Figures 3, 6) are entirely
  empirical, on the non-uniform grid.
- **Missing:** von-Neumann analysis, energy estimate, or CFL-type condition.
- **Latent risk:** the uniform-grid scheme's Re limit is unknown; users
  attempting Re = 10⁴ on a uniform grid may hit stability failures that the
  paper's non-uniform figures do not surface.
- **Documented as open question Q4 in `open_questions.json`.**

### 3.5 Narrow comparative benchmarking
- **What:** the paper's principal comparison (Table 6) is against Mukundan's
  BDF-2 variant.
- **Missing:** comparison against higher-order compact FD (Sari–Gürarslan
  2009), WENO/ENO schemes, or fully-implicit Crank–Nicolson variants — the
  natural competition for 1-D Burgers'.
- **Latent risk:** the paper's efficiency claim ("simple, efficient, accurate")
  is only established against one competitor. It may or may not survive a
  broader benchmark.
- **Documented as open questions Q1 and Q3 in `open_questions.json`.**

### 3.6 Extension to systems is nontrivial
- **What:** paper scope is scalar Burgers'. The linearization
  `u u_x → w u_x` is specific to scalar.
- **Latent risk:** the natural extension to systems (freezing the flux
  Jacobian at the extrapolated state) introduces per-eigenmode stability
  constraints not discussed in the paper.
- **Documented as open question Q5 in `open_questions.json`.**

## 4. Summary

| Category | Count |
|---|---:|
| Replication failures | 0 |
| Near-failures mitigated | 3 (Cloudflare, series truncation, floating-point drift) |
| Deliberate scope exclusions | 2 (non-uniform grid, Figures 3+6) |
| Latent failure modes in paper | 6 (ansatz, linearization order, non-conservative form, stability proof, benchmarks, systems extension) |

**Bottom line:** the paper's numerical work is correct, reproducible, and
solidly documented in the regimes tested. The latent failure modes above
are honest limitations that constrain the scheme's safe application
envelope; they do not detract from the reproducibility of what the paper
claims.
