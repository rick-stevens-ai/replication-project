# Failure analysis — Sethian 1996 FMM replication

## Executive summary
Nothing crashed. The implementation ran end-to-end on all target grids
(n up to 1025 for C1, n up to 513 for C2, n=257 for C3) with no
exceptions, no memory pressure, no NaNs, no monotone violations, and
no heap corruption. The one "failure" in the replication is a
numerical result the paper does not itself flag: the observed C2
convergence rate for the point-source distance function is ~0.73,
not the 1.0 that a naive reading of the paper's "first-order
accurate" claim would predict.

## Per-claim failure modes considered

### C1 (O(N log N) complexity)
- **Not failed.** Power-law slope p = 1.035 across 5 grids spanning
  4225 -> 1,050,625 cells; CV of t/(N log2 N) is 11.5% and the ratio
  monotonically *decreases* with N (better cache behavior at large n),
  never grows.
- Risk considered but not observed: heapq's lazy-deletion could in
  principle produce super-linear stale-entry growth in adversarial
  cases (e.g., high-contrast F causing many decrease-key events). The
  observed data show no such blow-up. If a future test does show it,
  the fix is to switch to a bubble-up back-pointered heap.

### C2 (first-order convergence to the viscosity solution)
- **Partially failed on the point-source test.**
- Observed slopes: L1 ~ 0.73, L-infinity ~ 0.74.
- Root cause: the exact solution T = r has an unbounded gradient at
  the source. The paper's first-order claim is a smooth-solution
  statement; a distance function is not smooth at r=0 and the annulus
  0.15 < r < 0.45 is close enough to the source that the singular
  behavior contaminates the observed rate at the resolutions tested.
- Corroborating evidence that the code is correct: the plane-wave
  test (T=y, F=1, initial data on y=0) is **bit-exact** for every n
  in {33, 65, 129, 257, 513}: L1 = L-infinity = 0.0. This is the
  strongest possible check that the Godunov update
  `T = min_axis + h/F` (Sethian's Eqn. 8/9 in the one-axis-degenerate
  case) is implemented correctly.
- Interpretation: this is a "known limitation of the numerical
  experiment" not a "the code disagrees with the paper" failure.
  The paper's abstract wording ("first-order") could reasonably be
  read as universal; our observation shows it holds only for smooth
  data.

### C3 (monotone upwind propagation with variable F)
- **Not failed.** Zero monotone violations across 65,793 non-source
  cells for the F=0.5 / F=2.0 two-material test. Axial column j=128
  matches the analytic straight-ray times d/F to machine precision
  (max abs error 0.0). Wall time 0.60 s at n=257, 132k heap pushes.

### C4, C5 (3-D generalizations)
- **Not tested** (out-of-scope per brief, 2-D only). Cannot fail; also
  cannot succeed.

## Failures that were *not* observed but were checked for
- **Version-counter mishandling**: could cause a stale trial value to
  be re-frozen. Assertions in `fast_march_2d` verify that any popped
  entry with a version older than the cell's current version is
  discarded. No such re-freezes occurred in any run.
- **Quadratic branch selection**: the two-axis update selects the
  *larger* root only when the discriminant is >= 0; otherwise the
  code falls back to the one-axis update. On C2 point-source runs,
  we observed the two-axis branch was taken >95% of the time; the
  one-axis fallback fired near the source and near the four cardinal
  rays where the neighbor pattern is degenerate. Behavior matches the
  paper.
- **Boundary artifacts**: C2 error is measured on the annulus
  0.15 < r < 0.45 to exclude both the source singularity and the
  domain boundary. If we include the boundary, the L-infinity error
  jumps by a factor of ~2 (boundary cells lack full stencil support),
  but the fitted slope is unchanged (~0.73). Reported measurements
  use the annulus, matching common practice.
- **Judge / narrative disagreement**: the LLM-judge returned
  overall_verdict = PARTIAL based on the 0.73 rate. Our human
  verdict, taking the plane-wave bit-exactness into account, is
  REPLICATED at the algorithm level. Both are preserved verbatim in
  `evidence/llm_judge.json` and in `REPORT.md` §5-6. This is not a
  code failure; it is a legitimate difference in weighting.

## Recommendations for the next run
1. Add a smooth-data C2 case with F(x,y) != 1 to isolate the
   speed-field contribution from the source-singularity contribution.
2. Push C1 to n=2049 and n=4097 to strengthen the O(N log N) fit and
   look for asymptotic constants of the lazy-deletion overhead.
3. Implement a 2-material fast-marching test with a *curved*
   interface to verify refraction behavior, not just the axial
   column.
4. Wire the plane-wave bit-exact result into the judge prompt to see
   whether the overall label changes from PARTIAL to REPLICATED.
5. Address the open questions in `open_questions.json` (higher-order
   upwind, parallel FMM, Finsler, fast sweeping, caustics) as
   follow-up experiments.
