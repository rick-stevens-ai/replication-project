# Failure Analysis — Kassam & Trefethen (2005) ETDRK4 Replication

**Overall verdict:** REPLICATED (strong). This document catalogs failures, near-misses, and legitimate limitations encountered along the way — not to soften the verdict, but so a future reader knows exactly what went wrong, how it was caught, how it was fixed, and what remains untested.

## 1. Silent first-order collapse on KdV (CAUGHT AND FIXED)

**Symptom.** Early implementation of `etdrk4_coeffs` used a HALF-circle contour in the complex plane and then took `real()` of the mean. On KS, Burgers, and Allen–Cahn (dissipative spectra on the negative real axis) this looked correct and gave clean 4th-order convergence. On KdV (pure-imaginary spectrum) ETDRK4 collapsed to **first order** — completely wrong.

**Root cause.** The true ETDRK4 φ-function coefficients on an imaginary-spectrum problem are genuinely complex. Zeroing the imaginary part discards the leading-order phase information; the update stages then no longer satisfy the order conditions and drop to O(h).

**Detection.** Cross-checked convergence order on KdV; the ~1.0 fitted slope was inconsistent with every other benchmark and inconsistent with the paper.

**Fix.** Switched to the FULL unit circle around each `hL` and kept coefficients complex all the way through the update stages.

**Verification post-fix.**
- Cauchy self-convergence on KdV: log₂ ratios 4.09 and 3.85 in the mid-range.
- KdV single-soliton max error 3.28e-9 (spatial-floor limited).
- Mass conserved to 2.8e-16; ∫u² to 4.5e-14 over T=2 at h=5e-4.

**Lesson (durable).** Any future extension of the contour trick — non-normal L, boundary-forced problems, Chebyshev spectra with non-real eigenvalues, or IMEX/split hybrids — inherits the same trap. Full circle + complex arithmetic is not a stylistic choice; it is a correctness requirement.

Logged in `attempt_log.md`.

## 2. Reference-solution slope saturation (NOT A BUG, DOCUMENTED)

**Symptom.** The reference-based convergence table for KdV shows a fitted slope of **2.65**, well below 4. At first glance this could be read as ETDRK4 being sub-fourth-order on dispersive problems.

**Root cause.** At the smallest step sizes (h ≤ 2.5e-3) the temporal error drops below the spatial spectral floor of the reference solution (~4e-11 for KdV at N=512). The log-log fit then averages a true 4th-order slope over the mid-range with a flat "floor" segment at the finest steps, biasing the slope downward.

**Detection / mitigation.**
- Reported the raw reference-based slope alongside a Cauchy self-convergence table that isolates temporal error.
- The self-convergence log₂ ratios (4.09, 3.85 mid-range; 2.17, 0.32 as the floor is hit) show the true 4th-order behavior explicitly.
- Explicit "floor" annotation next to sub-4 entries so the reader is not misled.

**Residual concern.** A skim-only reader looking at the primary reference table without reading the self-convergence addendum could still get the wrong impression. Called out in `REPORT.tex` §Genuine Critique item 1.

## 3. KS "match" is qualitative only (INHERENT, DOCUMENTED)

**What we cannot do.** Kassam & Trefethen Fig. 4 shows a space-time contour of a chaotic KS trajectory. Chaotic trajectories are exponentially sensitive to initial conditions and floating-point noise; pixel-level match to another implementation is impossible in principle.

**What we can (and do) verify.**
- Solution stays finite over T=150 (no blow-up).
- Bound `max|u| = 3.37` (paper qualitatively ~3).
- Mean drift `⟨u⟩_T − ⟨u⟩_0 = 4.4 × 10⁻¹⁷` (numerical mass conservation).
- Final RMS(u) = 1.18 (order-unity, as expected for the KS attractor).
- Space-time contour shows the standard "chaotic soliton" banded pattern.

**Residual.** This is a qualitative match, not a fixed-reference verification. Called out in the REPORT critique.

## 4. Claim C7 (Krogstad ETDRK4-B) not tested (SCOPE CUT)

**Decision.** Explicit scope cut: the paper's headline is about Cox–Matthews ETDRK4 vs IFRK4 and the cancellation cure. Krogstad ETDRK4-B is a secondary variant. Implementing and testing it would not change the verdict on the primary claims.

**What is missing.** No independent evidence that ETDRK4-B behaves similarly on our benchmarks. Would take a few extra hours to add.

**Impact on verdict.** None on C1–C6; C7 remains untested and is reported as such.

## 5. Endpoint saturation on KdV soliton error (INHERENT, DOCUMENTED)

**Observation.** `max|u − u_exact|` at T=2 is essentially constant (3.28e-9) across h ∈ {2e-3, 1e-3, 5e-4} — i.e. it does not decrease when the step size is halved.

**Explanation.** The spatial spectral error (N=512 grid, domain L=40) is already at ~3e-9 at these h values; temporal error at h=2e-3 is already below the spatial floor. The invariant test (mass and ∫u²) is the sharper diagnostic here and shows machine-precision drift.

**Not a failure.** This is the expected behavior of a well-behaved spectral + high-order-time scheme on an exact-solution problem. Documented in `REPORT.md` §C5.

## 6. Underspecified initial conditions (COMPENSATED, DOCUMENTED)

**Gap.** The paper does not fully pin down every IC (e.g. exact phase / normalization). We used:
- KS: Trefethen `kursiv.m` IC `cos(x/16)(1+sin(x/16))`.
- KdV: single soliton (paper also shows a two-soliton case with A=25).

**Impact.** Cannot claim pixel-level KdV match to the paper's two-soliton plot. Single-soliton was chosen for a cleaner order fit (two-soliton at A=25 needs dealiasing and much smaller steps).

**Documented.** `REPORT.md` §7 and `REPORT.tex` §Genuine Critique item 5.

## 7. Untested: cost / competitiveness axis (SCOPE CUT)

**Gap.** We show ETDRK4 wins vs IFRK4 in **error at equal h** (1.4×–5.14× ratio). We do not report wall-clock, RHS-eval count, or FFT count. Therefore we do not close the loop on "which integrator is faster to a given tolerance."

**Impact on verdict.** None on C1–C6 as stated by the paper (which are accuracy claims). But a reader who wants a practical recommendation between ETDRK4, IMEX-RK, and split-step needs a work-precision study that we did not do.

Reflected in `open_questions.json` Q2 as a legitimate open item for future work.

## 8. Untested: fp64 wall / Chebyshev / non-normal L (SCOPE CUT)

- All runs in fp64. Contour coefficient error floors at ~1e-15 (near the fp64 wall); we did not confirm the contour approach continues to give ~machine-precision accuracy in extended precision.
- Only Fourier discretizations. The paper also mentions Chebyshev spectra (non-normal L, non-uniform eigenvalues). Not tested here.

Reflected in `open_questions.json` Q1 and Q5.

## 9. Judge is single-source (ACKNOWLEDGED)

`report/judge_result.txt` is a single-pass Argo LLM sanity read of the initial draft. It is a useful sanity check, not a peer review. The strong-REPLICATED verdict rests on the numerics, not on the judge.

## Summary of what is bulletproof vs what is a documented limitation

**Bulletproof (numerically clean, multi-line evidence):**
- C1 direct-coefficient cancellation (6+ digits lost at |hL|=1e-3).
- C2 contour cure (uniform ~1e-15 across the sweep).
- C3 4th-order in time on KS / Burgers / Allen–Cahn (fitted 3.80 / 3.88 / 4.05).
- C3 for KdV via Cauchy self-convergence (4.09, 3.85 mid-range).
- C4 ETDRK4 > IFRK4 at equal h (1.4×–5.14× error ratio).
- C5 KdV soliton (spatial-floor limited error; machine-precision invariants).
- C6 long-time KS bounded, correct pattern, mean drift ~1e-17.

**Documented limitations (no impact on verdict):**
- C7 Krogstad not tested (scope cut).
- KdV reference-based slope saturated by spatial floor (mitigated by self-convergence).
- KS chaotic match is qualitative (inherent).
- Only fp64; only Fourier; no wall-clock competitiveness axis; single-source LLM judge.

**Verdict:** REPLICATED (strong). See `REPORT.md` §6.
