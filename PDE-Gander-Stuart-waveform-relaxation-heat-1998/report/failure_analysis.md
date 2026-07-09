# Failure Analysis — Gander & Stuart 1998 Replication

Overall verdict: **REPLICATED** (unanimous 3/3 judge panel, C1 and C2 numeric agreement
to ~0.1% or better). This file honestly catalogues everything that did *not* go smoothly,
plus scope gaps the reader should know about before extending the work.

---

## 1. Non-hard failures (operational hiccups that were worked around)

### 1.1 Publisher PDF paywalled
- **What:** The SIAM canonical PDF for DOI `10.1137/S1064827596305337` is behind a
  paywall; no free institutional route was used.
- **Impact:** None on the numerics. We fell back to the author's copy at
  `stuart.caltech.edu/publications/pdf/stuart39.pdf`
  (MD5 `a5aebcbf1b51887995c676f3bbf44439`).
- **Residual risk:** Author preprints occasionally differ from the published version in
  minor typography. The test problem (eq 4.1) and the analytic contraction formula
  `ρ = α(1−β)/(β(1−α))` are structural and would be extremely noticeable if edited;
  we detected no such discrepancy.

### 1.2 Claude referees hit an Argo serialization quirk
- **What:** `argo:claude-opus-4.8` and `argo:claude-opus-4.7` were attempted as judges but
  hit an Argo chat-endpoint response-serialization issue; they did not produce clean
  scorable outputs.
- **Workaround:** Substituted `argo:gpt-5.2`, `argo:gemini-2.5-pro`, `argo:gpt-4.1`
  (all free endpoints), which returned clean per-claim verdicts.
- **Impact:** The judge panel is still 3-of-3 unanimous, all free-tier, so the substitution
  is cost-neutral and evidence-neutral. It does slightly reduce model diversity (no
  Anthropic-family judge).

## 2. Hard scope limitations (things we deliberately did not test)

### 2.1 C3 tested at only one (N, r) point
- **What:** For claim C3 (`rate ≤ 1 − 4r(1−r)sin²(π/(2(N+1)))` and initial stagnation),
  we ran only `N=8`, `r=0.35`. Measured decay 0.9327 lies below the upper bound 0.9726
  and the stagnation phase (~4 iterations) matches the paper's qualitative description,
  so the tested point is consistent with the theorem, but this is not a stress test.
- **Impact:** C3 is confirmed *for one configuration*. We do not know from our runs how
  tight the bound is across (N, r), or whether it becomes vacuous in any regime
  (e.g. r → 0).
- **Follow-up:** See `open_questions.json` Q1.

### 2.2 Only one discretization tested for C2
- **What:** The mesh-robustness sweep uses centered second-order FD in space and backward
  Euler in time (matching the paper's §4). Crank–Nicolson, BDF2, higher-order FD, and
  spectral discretizations were not tried.
- **Impact:** Our C2 confirmation is discretization-specific in the sense that only one
  discretization was tested — but the space-time continuous theory predicts the same
  contraction factor for any reasonable discretization in the limit, so this is a scope
  gap rather than evidence of a problem.
- **Follow-up:** See `open_questions.json` Q3.

### 2.3 Only Jacobi-style sweep implemented
- **What:** All SWR sweeps use the parallel (Jacobi) update — every subdomain updates
  from the previous iterate's neighbor traces. A Gauss–Seidel (sequential) variant was
  not implemented.
- **Impact:** The paper's Theorem 2.4/2.8 asymptotic rate is the same for both flavors,
  so C1's asymptotic factor is not compromised. However, we cannot say anything about
  a potential pre-asymptotic superlinear phase on bounded time intervals that G-S would
  expose.
- **Follow-up:** See `open_questions.json` Q2.

### 2.4 Contraction factor fit from a scalar per-iteration summary
- **What:** For C1 and C2 the per-double-iteration factor is fit from the interface error
  at grid point `b` (a single spatial location, scalar summary per iteration); for C3 the
  fit uses the `∞`-norm across interfaces. The paper's theorem is a bound on an
  `L^∞`-in-time maximum-principle quantity.
- **Impact:** The metric we used is a defensible scalar proxy and matches how the paper
  presents §4, but a strict functional check (contraction of `sup_{t∈[0,T]} |error(b,t)|`
  across iterations) was not performed.
- **Follow-up:** Would be straightforward: swap the scalar peak-value fit for a
  time-supremum contraction check in `swr_heat.py`.

### 2.5 No comparison against algebraic-splitting WR
- **What:** The paper motivates its result by contrast with classical algebraic-splitting
  WR, whose rate degrades with mesh refinement. We did not implement algebraic-splitting
  WR and did not measure the comparative claim.
- **Impact:** Our C2 numerics confirm the *positive* claim (physical-space overlap gives
  mesh-robust rates). The *comparative* claim relies on well-established literature
  outside this paper; we take it as given but did not re-verify it.

### 2.6 Stagnation-phase length not characterised beyond one initial guess
- **What:** The ~4-iteration stagnation observed in the 8-subdomain experiment uses the
  constant-in-time initial guess prescribed by the paper. We did not sweep alternative
  initial guesses (linear-in-t interpolants, warm starts from coarser solves, random
  perturbations) to see how the stagnation length varies.
- **Impact:** The qualitative claim ("information has to propagate across domains") is
  confirmed at the tested initial guess but not characterised as a function of the start.
- **Follow-up:** See `open_questions.json` Q4.

### 2.7 1D only
- **What:** All experiments are 1D on `Ω = [0, 1]` with strip subdomains — exactly matching
  the paper's setting. Whether the same physical-overlap mesh-robustness story extends to
  2D/3D with cross-points and non-strip geometries is neither addressed by the paper nor
  probed by our replication.
- **Follow-up:** See `open_questions.json` Q5 (2D unit-square with 2×2 overlapping
  decomposition and cross-point).

## 3. Non-failures worth calling out honestly

- The C1 and C2 numeric agreement is very tight (~0.1% or better on the contraction factor;
  invariance to 4 sig-figs across 8× mesh refinement). No systematic deviation was detected
  that we then papered over. If the numbers had disagreed, we would have flagged it.
- The referees are three closed-source large models and may share priors; unanimous
  verdicts are corroborative evidence, not three independent expert reviews. The core
  weight of the replication is the numeric tables, not the LLM verdicts.

## 4. Reproducibility status

- Every numeric table entry traces to `evidence/results.json` or `evidence/mesh_robust.json`.
- No numbers were manually entered or estimated; the run scripts are the source of truth.
- Total runtime is seconds on a laptop; no GPU / HPC required.
- Reproduce with the block in `workflow.md`.

## 5. Bottom line

No hard technical failure. Two operational hiccups (paywalled publisher PDF, Claude judge
serialization) were routed around with no impact on evidence quality. Every remaining
weakness is a *scope* gap (single (N, r) for C3, single discretization, only Jacobi, only
1D, only one initial guess), each of which is either logged as an open question or is
outside the paper's own claim boundary. The paper's two headline results reproduce
quantitatively with essentially zero slop.
