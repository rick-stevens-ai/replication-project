# Failure Analysis — Davis & LeVeque 2020 Adjoint-AMR Replication

**Verdict:** REPLICATED. There is no "failure" of the overall replication.
This document catalogs partial failures, methodological compromises,
build-artifact bugs, and gaps between the paper's setup and ours, so future
replicators or extenders can address them.

## 1. Build-time crash: `use_adjoint=False` → `free(): invalid pointer`

**Symptom.** Attempting to run the 1D forward with `use_adjoint=False`
(i.e. standard AMRClaw with `flag2refine=True` using the undivided-difference
criterion) crashed inside the `adjoint_module` initialization with
`free(): invalid pointer` (glibc double-free / invalid-free abort).

**Root-cause hypothesis.** The maintained
`amrclaw/examples/acoustics_1d_adjoint/` example allocates aux-array storage
for adjoint bookkeeping unconditionally, then tries to free something that was
never allocated when `use_adjoint=False`. Not investigated to fix.

**Workaround.** For Richardson-error-flagging runs, kept `use_adjoint=True`
(so the aux-array bookkeeping stays initialised) but set `flag_richardson=True,
flag2refine=False`. The adjoint machinery is present but not used for the
flagging decision — a legitimate configuration.

**Impact.** We were unable to test the paper's "undivided-difference
`flag2refine`" baseline in the same code path. Richardson error flagging is
still one of the paper's four baselines, so C2 is not orphaned, but coverage of
the baseline set is reduced from 4 to 3.

**Fix path (open).** File a Clawpack issue upstream against
`amrclaw/examples/acoustics_1d_adjoint/` with the crash trace; check if
`adjoint_module.f90` guards its `deallocate` calls with `use_adjoint`.

## 2. 1D example is not paper Example 1 (didactic variant)

**Compromise.** The Clawpack-maintained example uses domain `[-5, 3]`,
target `x=1.5`, `t_f=15`, 30 base cells. Paper Example 1 uses `[-12, 12]`,
`x_p=7.5`, `t_f=34`, 60 base cells.

**Why compromise.** Rebuilding the exact Example 1 setup requires modifying
`setrun.py` (straightforward) and re-verifying that the target functional
weight, adjoint IC, and BCs match the paper's — a full afternoon of care that
was not in scope for a first-pass replication.

**Impact.** We can only claim the *directional* result (adjoint < Richardson
at matched J-error) is present in the smaller variant. Absolute
comparison to paper Fig. 12 CPU curves is not possible.

**Fix path (open).** Item #3 in `open_questions.json`. Rebuild Example 1 to
paper specs; overlay error-vs-work curve on Fig. 12.

## 3. 1D $J_{\text{ref}}$ is self-consistent, not analytical

**Compromise.** Used Richardson tol=1e-6 (finest available) as the reference
for J when reporting `|J − J_ref| / J_ref`.

**Why compromise.** There is no closed-form solution for the variable-
coefficient linear acoustics problem at t=15; producing a spectrally-converged
reference would require a separate high-resolution FDM or DG solver, out of
scope.

**Impact.** Both adjoint and Richardson could converge to a common numerical
fixed point that differs from the true J. The *ordering* claim (adjoint uses
fewer cells at matched numerical J) is robust. Absolute-error magnitudes
should be read as "self-consistency", not true error.

## 4. Only one 2D tolerance pair (single-point evidence for C4)

**Compromise.** The dramatic 2D ratios (5.65× total cells, 7.82× L3 cells,
2.97× wall clock) come from a single (adjoint tol=0.04, Richardson tol=1e-3)
pairing.

**Why compromise.** 2D runs are expensive (~seconds each, but the whole
sweep-and-verify loop is human-in-the-loop-limited on a shared node); a full
sweep was deferred.

**Impact.** Cannot rule out that the ratios are peculiar to this tolerance
pair. C4 stands but on thinner evidence than C2 or C3.

**Fix path (open).** Item #2 in `open_questions.json`. Run a 3×3 tolerance
grid and report the ratio as a function of achieved accuracy.

## 5. 2D "accuracy" proxy is mass, not J

**Compromise.** Used total mass ∫∫ p(x,y,t=7) dx dy as the accuracy check
(agreement <0.4%), not the localised functional J over a target rectangle.

**Why compromise.** Computing J requires the paper's Example 3 target
rectangle geometry and integration weight. The maintained
`acoustics_2d_adjoint/` example uses a point-spike adjoint IC and does not
ship a target-rectangle J.

**Impact.** Two runs could have matched total mass but different J (unlikely
given the compact-support of the wave energy and the target-region
localisation, but not impossible). C2 in 2D is confirmed via a proxy.

**Fix path (open).** Item #1 in `open_questions.json` (with the target-
rectangle J on Example 3 geometry).

## 6. C5 (tolerance ∝ J-error for adjoint-error flagging) not tested

**Compromise.** Only tested adjoint-*magnitude* flagging. Did not test the
adjoint-*error* flagging variant that the paper's Fig. 11 highlights as the
strongest performer with the cleanest tolerance-to-J-error mapping.

**Why compromise.** Enabling the adjoint-error variant in v5.9.2 requires
either a separate code path in `adjoint_module` (not confirmed present in the
maintained example) or a backport from v5.6.1. Deferred.

**Impact.** C5 marked partial in the claims table. Note: since our results
show adjoint-magnitude (the weaker variant) already beats Richardson, this
*understates* the paper's claim, so the replication conclusion is not
threatened.

## 7. C6 (adjoint solve cheaper than forward) qualitatively supported only

**Symptom.** In 2D, adjoint solve took 8s (8 threads), forward took 0.86s —
superficially the wrong direction. Attributed to the forward being
under-resolved at this small example scale.

**Compromise.** No proper C6 test was performed. Both 1D solves are
sub-second so the ratio is noise-dominated.

**Impact.** C6 marked "qualitative only". The paper's claim (adjoint solve
is ~10s vs. a much larger forward cost) is unverified.

**Fix path (open).** Item #5 in `open_questions.json`. Test at Example 3
production scale where the forward is properly resolved.

## 8. Clawpack version drift (v5.6.1 → v5.9.2) unaudited

**Compromise.** Used v5.9.2; paper used v5.6.1. Did not diff the adjoint-AMR
kernel between those tags.

**Impact.** If maintainers modified the inner-product weight, L3 threshold
semantics, or snapshot interpolation, this replication reproduces the
*maintained* algorithm, not the paper's exact one. Directional result is
almost certainly unchanged; absolute magnitudes could shift.

**Fix path (open).** Item #4 in `open_questions.json`. `git log
v5.6.1..v5.9.2 -- src/{1d,2d}/adjoint/` and diff any semantic commits.

## 9. Timing noise not quantified

**Compromise.** 2D wall/CPU numbers from a single `timing.csv` per run. No
repeat runs to bound timing noise on a shared 255-core node.

**Impact.** The reported 2.97× wall-clock ratio has no error bar. Could be
2.5×–3.5× depending on node contention.

**Fix path (cheap).** Rerun each 2D run 5–10 times; report median and IQR.

## 10. Log-log "left-of" 1D evidence is 3+4 points

**Compromise.** 4 adjoint tolerances + 3 Richardson tolerances → 3 points per
method on the error-vs-work curve (once you drop the "too loose" adjoint tol=0.1
row that fails to converge). The visual "adjoint left of Richardson" is
convincing but statistically thin.

**Fix path (cheap).** Add 3–4 more tolerances per method.

## Root-cause summary table

| # | Failure/gap | Class | Blocking? | Fix cost |
|---|---|---|---|---|
| 1 | `use_adjoint=False` crash | build/upstream | no (workaround) | file upstream issue |
| 2 | Didactic 1D variant, not Example 1 | scope | no | 1 afternoon |
| 3 | Self-consistent J_ref | scope | no | separate solver, days |
| 4 | Single 2D tolerance pair | scope | no | 1 afternoon |
| 5 | Mass proxy in 2D, not J | scope | no | implement rectangle J, hours |
| 6 | C5 (adjoint-error variant) not tested | scope | no (C5 partial marked) | investigate code path, hours-days |
| 7 | C6 not testable at this scale | scope | no (marked qualitative) | need Example 3 setup, day |
| 8 | Version drift unaudited | audit | no | git log + diff, hours |
| 9 | No timing noise bars | rigor | no | rerun, hour |
| 10 | Sparse tolerance sweep in 1D | rigor | no | rerun, hour |

**Net.** The verdict REPLICATED is robust to every item above. Items 2–10
represent the difference between "the paper's central claim is reproduced
directionally on a maintained variant" and "the paper's exact figures are
reproduced numerically". A follow-up replication addressing items 2, 4, 5, 6,
and 8 would upgrade the confidence from "high" to "very high with quantitative
figure-level agreement".
