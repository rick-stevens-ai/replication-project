# Failure analysis — Osher & Sethian (1988) level-set replication

Verdict is REPLICATED, but the replication has real limitations and
several near-misses worth documenting so downstream work does not
overclaim.

## 1. Untested claims

### 1.1 C4 — higher-order ENO+RK order test (skipped)
- Paper §III.B.2 and Table 1 argue that higher-order ENO in space + RK in
  time gives higher-order accuracy than the first-order Godunov scheme.
- This wave used only first-order upwind Godunov convection + forward
  Euler. The order-of-accuracy claim is therefore inherited from the
  paper, not independently verified here.
- Impact: any downstream user who needs high-order convergence should
  not treat the REPLICATED verdict as evidence that the paper's ENO+RK
  claims specifically hold.

### 1.2 C5 — 3-D / N-D generalization (skipped)
- Paper Sec. I and later sections claim the formulation generalizes to
  3-D surfaces and to N-D. This replication is 2-D only.
- Impact: the "level-set works in N dimensions" story rests on the
  paper alone.

## 2. Convergence-order shortfall in C2 (sub-optimal but documented)

- The MCF grid-refinement study yields observed orders 1.63–1.69 (L²)
  and 1.34–1.93 (L∞), not the clean 2 one would expect from a smooth
  central-difference scheme applied to a smooth problem.
- REPORT.md attributes this to super-first-order behavior for smooth
  solutions that degrades toward first order near the singularity as
  R → 0, consistent with the paper's own discussion in §III.C.
- We did not separate the "smooth-regime order" from the "singularity
  contamination" by restricting the error window to R ≫ 3Δx or by
  stopping earlier. That is a real gap: the reported order is a
  composite that mixes smooth and near-singular behavior.

## 3. Single-resolution merge-time claim in C3

- The C3 numerical merge time (0.1504) matches the analytic value
  (0.1500) to 0.27% at N=251.
- We did not sweep N∈{101, 201, 301, …} for C3, so we cannot show that
  this error shrinks under refinement — only that it is small at one
  resolution.
- Impact: C3 is best read as "consistent at one grid," not as a proven
  convergence to the analytic merge time.

## 4. No external-library cross-check

- The implementation is validated only against analytic solutions of
  highly symmetric problems (single circle, two symmetric disks) and by
  an LLM judge.
- No comparison against an established level-set implementation
  (`scikit-fmm`, `LSMLIB`, or a FMM/FSM-based reference) was performed.
- Impact: a bug that happens to preserve symmetric answers (e.g., a
  sign convention that cancels in the axisymmetric case) would not be
  caught here.

## 5. No reinitialization / |∇φ|-drift instrumentation

- The runs evolve φ directly without periodic Sussman-style
  reinitialization to `|∇φ| = 1`.
- We did not log `||∇φ| − 1|` on a narrow band around the zero set, so
  we cannot say how much of the C2 sub-optimal order (§2) is due to
  drift versus singularity formation.

## 6. Boundary conditions differ from typical practice

- Periodic BCs via `np.roll`. The fronts stay well inside the domain
  in every experiment, so the BCs do not perturb the answers.
- However, real level-set applications typically use outflow / one-sided
  BCs; anyone extending this code to interfaces that touch the domain
  boundary must change the BC handling.

## 7. Explicit forward Euler only — no IMEX / implicit-curvature

- The parabolic CFL `Δt ≲ Δx² / (Cε)` forces very small time steps at
  high resolution: the C2 N=301 run needs 12,500 steps for T=0.4.
- Acceptable at 2-D laptop scale (total wall-clock < 3 min), but this
  would be a real cost in 3-D or in a coupled multiphase flow solver.
- No IMEX or fully implicit treatment of the curvature term was
  implemented or benchmarked.

## 8. LLM judge is not an independent check

- The judge (`argo:gpt-4o`, temperature 0) sees only the paper's claims
  and our own numerical results JSON. It cannot detect an implementation
  bug that returns internally-consistent but physically-wrong numbers.
- Its per-claim `pass` verdicts should be read as "the numbers we
  produced are consistent with the paper's claims," not as independent
  physical validation.

## 9. Data / code near-misses observed during development
- Central-difference curvature is essential: any attempt to mix upwind
  stencils inside K with different stencils inside |∇φ| would blow up
  near |∇φ| ≈ 0 (paper §III.C explicitly warns of this). We followed
  the paper and used all-central; deviating from this is a known trap
  we did not fall into but that future forks might.
- Parabolic CFL `Δt = 0.2·Δx²/ε` was chosen well inside the stability
  bound. A more aggressive Δt would risk instability especially on the
  C2 N=301 run (largest step count).

## 10. What would move this from REPLICATED to STRONGLY REPLICATED

The verdict is not in doubt — the four testable claims match analytic
solutions to ≤ 0.5%. To strengthen it further:

1. Add C4 (ENO+RK order test).
2. Add C5 (3-D shrinking sphere against analytic collapse).
3. Convergence-refine C3 (merge-time vs N).
4. Cross-check against an established level-set library on the same
   inputs.
5. Instrument |∇φ|-drift and add optional reinitialization; rerun C2
   and confirm cleaner order.
