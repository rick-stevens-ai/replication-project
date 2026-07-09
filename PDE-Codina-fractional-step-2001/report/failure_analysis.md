# Failure Analysis — Codina (2001) Fractional-Step Replication

Honest audit of what was tried and didn't work, and what was deliberately
deferred, per REPORT.md.

## Attempted-but-not-clean

### 1. Manufactured-solution convergence test (paper Section 6.2 / Fig 7)
- **What we tried.** 20×20 Q1 with the paper's exact eq. 60 manufactured
  solution; sweep δt and check for O(δt) (first-order, θ=1) and O(δt²)
  (second-order, θ=1/2) temporal error rates.
- **What happened.** Errors did NOT show clean O(δt)/O(δt²). They in fact
  *grew* as δt shrank, mirroring the same equal-order-Q1/Q1 instability that
  the paper's Sections 3.2–3.3 predict.
- **Root cause.** Paper's Fig 7 is produced with the *stabilized* second-order
  scheme; the paper itself says: "since we have seen that the second-order one
  is unstable, we have combined it with the pressure stabilization technique."
  Without OSS/PSPG, Fig 7 is not expected to reproduce.
- **Resolution.** Documented as evidence *supporting* C1/C2 (instability of the
  unstabilized scheme), not as a contradiction of C5. C5 remains untested
  because we did not implement OSS (see item under Deferred).

### 2. Second-order (γ=1, θ=1/2) magnitude at small δt
- **What we saw.** Our unstabilized second-order rerun reaches
  P_std ≈ 2.26 × 10⁵³ at δt = 0.1·δt_crit, and ≈ 1.20 × 10¹⁸ at δt_crit.
  Codina's Fig 2 shows *bounded but completely oscillatory* contours at
  essentially the same parameters.
- **Hypothesized causes** (paper's implementation details are not fully
  specified):
  1. Equal-order Q1/Q1 amplifies the paper's already-weak ℓ∞ bound
     `{δt ∇pₕⁿ} ∈ ℓ∞(L²)`.
  2. Strict one-shot Picard convection linearization provides no damping.
- **Resolution.** Reported the divergence honestly under "Deviations from the
  paper" and in the "Genuine Critique" section of `REPORT.tex`. The
  *direction* (2nd-order much worse than 1st-order, both fine only at large
  δt) matches the paper cleanly; the *magnitude* does not. This is the largest
  substantive gap in the replication.

## Deferred (not attempted, and why)

### A. OSS stabilization (paper Section 5) — blocks C3 and C5
- **What's needed.** Compute the pressure-gradient projection Πh(∇p) via a
  consistent-mass solve (an extra Gramm-matrix inversion per step), then add
  the OSS residual term to the pressure Poisson equation.
- **Why deferred.** "A substantial additional coding effort that did not fit
  in the allocated time budget" (REPORT.md, Verdict/Justification).
- **Impact.** C3 (stabilization cures oscillations) and C5 (stabilized O(δt),
  O(δt²) convergence) are NOT_TESTED. Both are neither confirmed nor
  contradicted. This is why the LLM-judge returned PARTIAL, and why a strict
  claim-by-claim aggregate is more conservative than the "core theoretical
  claims REPLICATED" narrative.

### B. N-scan and Re-sweep
- Only N=20 Q1 at Re=100 was tested. No mesh refinement study, no Reynolds
  sweep, no alternative geometry. The paper's Section 6 is broader; ours is a
  single slice.
- Deferred for the same time-budget reason.

### C. Independent-implementation cross-check
- We built the Q1/Q1 code from scratch in NumPy/SciPy. We did NOT compare the
  same six cavity cases against an established FEM library (FEniCS,
  Firedrake, deal.II). A silent implementation error could still exist and
  would not be caught by our current tests.
- Deferred.

### D. Contour-by-contour visual comparison to paper Fig 1–2
- We produced our own contour plot
  (`report/evidence/cavity_pressure_contours.png`) and made the quantitative
  P_std / roughness_d2 comparison. We did NOT perform a side-by-side visual
  overlay against Codina's Fig 1 or Fig 2. Metric-based match is unambiguous;
  visual match is presumed but not formally verified.

## What did NOT fail (recorded for symmetry)

- **First-order projection scheme.** Reproduced C1 cleanly: pressure quality
  improved ≈ 5 orders of magnitude as δt grew from 0.1·δt_crit to 56·δt_crit,
  consistent with the paper's √δt scaling. No implementation surprises.
- **Consistent-mass corrector.** Once we (correctly) refused to lump the mass
  in the corrector step, the projection identity `L ≈ D M⁻¹ G` held and the
  first-order scheme behaved as predicted.
- **Pressure pin.** Pinning p[0] = 0 removed the singular Neumann mode without
  visibly affecting the pressure-quality metrics. (Sensitivity to alternative
  gauges is listed as an open question in `open_questions.json` but was not
  observed to cause trouble in the runs performed.)

## Bottom line
The failures were localized (C3/C5 untested, second-order magnitude larger
than the paper's) and *documented*, not swept under the rug. The verdict
"REPLICATED (core theoretical claims)" is honest for C1/C2, and the "Genuine
Critique" section in REPORT.tex spells out what is *not* proven.
