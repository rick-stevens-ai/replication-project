# Attempt Log

**Date:** 2026-07-04
**Executor:** subagent (argo/argo:claude-opus-4.7)
**Compute:** local CPU (CherryRd, macOS), pure NumPy — matches paper's own
minimal scalar tests; no GPU needed.

## Chronology

1. Read `WAVE_BRIEF_2026-07-01.md`. Confirmed: free endpoints only (Argo
   127.0.0.1:44497 key=stevens), LLM-judge for verdict, write only inside
   target dir.
2. Recognized paper: Gottlieb & Shu 1998, Math. Comp. — well-established.
   Core numerical objects are eq. (4.1) SSP-RK2 (Heun) and eq. (4.2) SSP-RK3
   (Shu-Osher), both with SSP coefficient c* = 1. Verified formulas from
   memory against the widely-cited canonical form.
3. Created target dir + report skeleton.
4. Wrote `work/ssp_rk_replication.py` — implementations of
     (a) SSP-RK2, SSP-RK3 (paper formulas),
     (b) 1st-order upwind spatial op (forward-Euler TVD at CFL ≤ 1),
     (c) MUSCL+minmod (TVD at CFL ≤ 1/2),
     (d) classical RK4 as non-SSP linear-stability control,
     (e) an explicit non-SSP RK2 with a negative-β downwind stage
         (Shu-Osher counter-example) as TVD-violation control,
     (f) three experiments (C1 order, C2 TVD, C3 empirical SSP CFL).
5. **First run — C1 blew up for SSP-RK2 on periodic linear advection with
   spectral spatial derivative.** Root cause: SSP-RK2's linear stability
   region only touches the imaginary axis at the origin, so *pure*
   advection (purely-imaginary eigenvalues) is unconditionally unstable
   for SSP-RK2 no matter how small the CFL. Fix: switch the C1 order test
   to the scalar ODE u′ = −u (real negative eigenvalue, well inside every
   RK stability region), which is what Gottlieb-Shu themselves use for
   order verification. This is the textbook temporal-order test.
6. **First run — C2 TVD-violation controls (RK4 at CFL ≤ 1) did not
   violate TVD** because RK4's stability region for pure advection extends
   to CFL ≲ 2.83, so RK4 + upwind at CFL = 1 is fine. Replaced with two
   sharper controls:
     - SSP-RK2/3 at CFL = 1.05 (0.05 past the SSP bound) → expected to
       violate TVD per the paper's Prop. 2.
     - An explicit 2-stage RK with a negative β coefficient (a downwind
       Euler stage) at CFL = 0.5 → the Shu-Osher counter-example type,
       expected to blow up.
7. Second run: all three claims reproduced.
     - C1 orders: 2.005 and 3.005 (rates from the last three refinements).
     - C2 TVD: SSP-RK2/3 hold TV to machine zero at CFL = 1; SSP-RK2 at
       CFL = 1.05 blows up (TV × 327); non-SSP neg-β RK2 blows up
       catastrophically (TV × 10⁶) even at CFL = 0.5.
     - C3: empirical SSP CFL = 0.99997 for both schemes, matching c* = 1.
8. LLM-judge (Argo `argo:gpt-4o`, temperature 0) scored the numeric summary
   against the paper's three claims → verdict **REPLICATED**, per-claim all
   "reproduced".
9. Wrote report artifacts.

## What worked
- Paper's formulas are compact and unambiguous; from-scratch NumPy took ~200
  lines, runs in <1 s.
- Scalar ODE u′ = −u is the cleanest way to isolate temporal order.
- The paper's own predictions (SSP bound + Shu-Osher counter-example) make
  strong falsifiable predictions that the code either meets or violates.

## What failed initially
- Testing temporal order on purely-imaginary spectrum (pure advection,
  spectral derivative) — SSP-RK2 is not zero-dissipative there and diverges.
  Standard pitfall; fixed by switching to the real-eigenvalue ODE.
- Non-SSP TVD-violation control needs a scheme whose linear stability region
  and/or CFL is small enough that the given CFL exceeds it. RK4 + upwind at
  CFL = 1 is safe. Fixed by using the negative-β counter-example directly.

## Not attempted (out of minimum scope)
- SSP-RK4 (which the paper shows CANNOT exist with all-positive coefficients
  at optimal CFL — the paper's more subtle 4-stage results).
- Nonlinear tests (Burgers, Euler shock tubes). Not needed to verify the
  three core claims.
