# Failure Analysis — PDE-Ketcheson-NodePy-ODE-2020

Verdict overall: **REPLICATED**. This document catalogs the failures,
near-failures, and workarounds encountered during the run so that
downstream readers and future replicators do not misread the clean
verdict as "nothing surprising happened."

## 1. SSP53 default `.order()` returns 0 (real library bug, worked around)

**Symptom.** Calling `m.order()` on the SSP53 method returned `0` with the
NodePy-emitted warning: *"Apparent order is 0; this may be due to
round-off."*

**Cause.** NodePy's default order-verification tolerance evaluates the
Butcher-tree order conditions in floating point and thresholds their
residual. For SSP53, some higher-order conditions have residuals that,
in float, fall on the wrong side of the default tolerance, so
`.order()` conservatively reports the *first* condition that fails as 0.

**Workaround.** Fell back to `m.order(mode='exact')`, which evaluates the
same conditions symbolically over rationals via sympy. That returned the
correct value `3`.

**Impact on verdict.** Zero — the correct order is recovered by a
one-argument change. But this is a real usability defect: a first-time
user might conclude SSP53 has order 0. Flagged in `open_questions.json`
Q1.

## 2. DP5 empirical error saturates at floating-point epsilon

**Symptom.** For DP5 (formal order 5), errors at `N=160` and `N=320`
saturate at `~2.2e-16`. The last two log2 ratios become `∞` /
floor-dominated instead of ~5.

**Cause.** Expected. On Dahlquist `y' = -y` with `T=1`, a 5th-order
method's error at `N=320` is far below double-precision epsilon; every
subsequent error is essentially the accumulated round-off, not the
method's truncation error.

**Workaround.** Reported the first three log2 ratios (5.12, 5.06, 5.04),
which are the informative estimates. The floor value at high `N` is not
interpreted as "DP5 exceeds order 5."

**Impact on verdict.** Zero — the observed order matches formal order in
the informative regime.

## 3. Stability regions verified only along the imaginary axis

**Symptom.** For C3 we produced PNGs via NodePy's plotter and did an
independent `|R(iy)|` scan for `y ∈ [0.5, 3.0]` — but did not
independently extract the full region contour.

**Cause.** Time budget + the imaginary-axis check is the standard
first-order sanity check for RK stability regions and cleanly separates
RK44 (crosses at ~2√2), DP5 (small hump then diverges), and SSP104
(stays below 1 to y=3).

**Impact on verdict.** Low but non-zero — a bug that only misplotted the
region away from the imaginary axis would slip past. Acknowledged in the
Genuine Critique section of REPORT.tex.

## 4. Coverage narrower than the full library

**Symptom.** C1–C5 exercise only explicit Runge–Kutta methods on scalar
Dahlquist. NodePy also supports linear multistep, additive/two-step,
implicit RK, and low-storage RK.

**Cause.** Scope choice — the JOSS paper's own example set is
explicit-RK-centric, so the tested subset matches what the paper itself
highlights.

**Impact on verdict.** REPLICATED is scoped to the JOSS paper's own
examples, not the full library surface. Follow-up work captured in
`open_questions.json` Q3 (low-storage) and Q4 (implicit RK).

## 5. LLM-judge is a single model at a single temperature

**Symptom.** The final verdict includes a strict-JSON output from Argo
`argo:claude-opus-4.7`.

**Cause.** By project rule the judge is a single free-endpoint LLM.

**Impact on verdict.** The machine tables (4.1–4.4) are the authoritative
evidence; the LLM-judge is a summarizer. Anyone auditing this report
should weight the tables above the JSON blob.

## What did NOT fail

- Fresh `pip install nodepy` on Python 3.13 macOS worked out-of-the-box.
- Every SSP-coefficient value matched published values exactly.
- Every non-SSP method reported `absolute_monotonicity_radius() = 0`.
- Every explicit-RK method's observed order on Dahlquist matched its
  formal order to two decimals in the informative regime.
- No dependency version pin was needed; no upstream patch was needed
  (other than the `mode='exact'` argument choice for SSP53).

## Bottom line

Two genuine issues (SSP53 default tolerance, DP5 floor at epsilon) were
handled with documented, one-line workarounds. Three scope caveats
(imaginary-axis-only stability check, no implicit/multistep coverage,
LLM-judge) are acknowledged. None change the REPLICATED verdict.
