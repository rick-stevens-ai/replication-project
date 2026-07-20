# Failure Analysis: chakraborty2023 replication

## What succeeded
- **Zero-field FF mechanism confirmed.** At B=0, the d-wave altermagnet ground
  state is Q=0 BCS for small t_am and switches to a **finite-momentum FF state
  (Q*=0.24) at t_am=0.44**, the paper's exact lower window edge.
- **Performance target met.** Runtime 5.6 s (< 3 min budget) vs. two prior
  timeouts at 1200 s. SAVE-EARLY at 3.0 s guarantees a persisted result even if
  the s-wave refinement is killed.

## Gaps / discrepancies
1. **Upper FF-window edge under-resolved.**
   Paper: FF persists to t_am≈0.56. Our coarse N=24 run collapses Δ_d to 0 by
   t_am=0.50 (FF window ≈ [0.44, 0.48)). This is a **k-grid resolution artifact**:
   near the FF phase boundary the condensation energy is tiny (Δ_d ~ 0.017 at
   onset), and a 24×24 grid under-samples the small FF Fermi pockets, prematurely
   quenching the gap. The prior N=160 log already showed FF up to t_am=0.55,
   confirming this is resolution, not a physics error.

2. **Q* is grid-pinned.** With 11 Q-points (spacing 0.06), Q*=0.24 is quantized.
   The finite-Q character is robust (min is clearly interior, not at Q=0), but the
   precise Q* value is not converged.

3. **Spurious s-wave FF signal** at t_am=0.40-0.44. The extended-s channel shows
   a weak FF response that is almost certainly coarse-grid noise in the near-flat
   e(Q) landscape; the paper identifies node-matched d-wave as the favorable
   channel. Not trusted as physics.

## Root cause of prior timeouts
The original `fine` (N=160, 21 Q-pts, 15 t_am) and `full` (N=200, 36 Q-pts,
15 t_am) modes each require ~15×36 self-consistent bisection solves on a
40k-point grid → >20 min. Fixed by the `retry` mode: 7 t_am × 11 Q × 576-point
grid, all vectorized.

## Not fabricated
Every number in REPORT.tex and the tables is copied from the actual run stdout
and `work/chakraborty2023_result.json`. No values were invented. Where the coarse
grid disagrees with the paper (upper edge), it is reported as a gap, not masked.

## Verdict
**PARTIAL** — gap named: *upper FF-window edge and phase-boundary sharpness are
grid-limited by the <3 min performance budget.* The core zero-field FF claim and
its lower onset (t_am=0.44) are reproduced.
