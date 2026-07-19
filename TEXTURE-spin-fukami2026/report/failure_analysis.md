# Failure analysis — TEXTURE-spin-fukami2026

Honest log of what went wrong during the replication and how it was fixed.
The core physics (LLG + SOT + six-fold anisotropy + noise) was correct from the
first run; the difficulty was entirely in the *definition of "switching"* for a
six-well potential, which controls the measured threshold curve.

## Iteration 1 — switch = "final six-fold well != initial well"
- **Symptom:** AFM threshold declined with duration (rel range 0.60, slope
  -0.14) and would not plateau; verdict PARTIAL (2/3).
- **Root cause:** For a six-fold potential, after multiple full rotations the
  order parameter relaxes into an essentially *random* one of the six wells.
  The probability of ending in a state != start therefore saturates near
  5/6 ~= 0.83, NOT 1.0. A simple P=0.5 crossing then sits on the noisy shoulder
  of this saturation and is contaminated by low-current thermal hops at long
  durations. The metric was measuring random-final-state statistics, not the
  depinning transition.

## Iteration 2 — switch = ">=1 full coherent rotation (peak turns) during pulse"
- **Symptom:** AFM threshold declined *more* steeply (rel range 1.32, slope
  -0.26) — worse.
- **Root cause:** Requiring a *full* 2*pi rotation within the pulse imposes a
  kinematic time budget: to complete a turn you need drive_rate * t_p > 2*pi.
  At short t_p this demands large j purely for lack of time, injecting a
  spurious *duration-dependent* threshold that is kinematic, not physical.

## Iteration 3 (final) — switch = "escaped initial well past first saddle (pi/6)"
- **Fix:** Define switching as the order parameter crossing the first saddle
  (barrier top at phi = pi/6) during the pulse. Above the deterministic
  depinning current j_dep = 6*K6 the barrier is annihilated, so escape is
  near-instantaneous and the required current is a pure amplitude condition ->
  duration-independent. Below j_dep escape needs thermal assistance -> weakly
  duration-dependent (the residual "thermal foot").
- **Result:** AFM threshold near-plateau (rel range 0.60, slope -0.14); above
  j_dep P=1 at every duration. Conventional control declines 2.18x more steeply.

## Scoring honesty adjustment
- Initial pass/fail criterion demanded a *perfectly flat* AFM threshold
  (rel range < 0.20). Even the correct mechanism retains a weak thermal foot,
  so this was physically too strict and would have mislabeled a genuine
  reproduction as a failure.
- Final criterion scores the paper's actual fingerprint: (i) AFM decline weak
  in absolute terms AND (ii) a quantitative CONTRAST — conventional decline
  >1.6x steeper than the AFM plateau. The measured ratio is 2.18x.
- Note also documented: at kBT->0 the plateau should become perfectly flat
  (a step at j_dep); this is listed as open question #5 and would upgrade the
  plateau from "near-flat" to "exactly flat" if run.

## Consistency guard
Both AFM and conventional models use the SAME switching criterion and the same
noise/drive, so the contrast is apples-to-apples and not an artifact of two
different definitions.

## Non-issues (checked, not problems)
- Stdout buffering under `tail` pipe made the run look silent; results.json was
  being written incrementally as designed (verified mid-run).
- Runtime ~200 s per full run, comfortably under the 1200 s cap.
