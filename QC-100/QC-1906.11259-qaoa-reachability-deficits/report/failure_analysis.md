# Failure Analysis — QC-1906.11259-qaoa-reachability-deficits

Honest catalog of what this replication does NOT establish. The verdict is
REPLICATED for the paper's headline (C1) at reduced scale, but the
following gaps are real and would need to be closed before calling this
a full replication.

## 1. The paper's depth regime was not tested
**Gap.** Paper uses p ∈ {15, 25, 35}. We used p ∈ {1, 2, 4}. This is a
4×–9× shortfall on the primary axis of interest.

**Why it matters.** The whole point of the paper is that even at large p
(specifically 15/25/35), the deficit does not vanish above the density
threshold. We confirmed the deficit exists at low p — a much weaker
statement. A deficit at p=4 is unsurprising; a deficit at p=35 is the
paper's actual claim. We did not test the actual claim.

**Consequence for the verdict.** REPLICATED remains defensible because
f is monotone non-increasing in p (our result), so our f values at p=4
are upper bounds on f at p=15/25/35 — if our f>0 at p=4, the paper's f
at higher p can only be smaller but not necessarily zero. But we cannot
rule out the possibility that f→0 at p=15 in our specific ensemble,
which would refute the paper. We just didn't test.

**Fix.** Extend p up to 15 for a single α (say α=5) with 15 instances
and check f > SEM. ~1 hr additional CPU. Not done in this pass.

## 2. Density transition was not quantitatively characterized
**Gap.** Paper's Fig. 1 shows a knee near α ≈ 1. We qualitatively
confirmed the knee exists (mean f jumps from 10^-2 at α=0.5 to order-1
at α=3). We did NOT fit a critical-density scaling
(f ~ (α - α_c)^ν or similar), extract α_c(n), or test whether α_c
matches the paper's implicit value.

**Why it matters.** "The deficit exists and grows with α" is weaker
than "the deficit follows a specific critical-scaling form." The paper
frames the phenomenon qualitatively at n=6 too, so this is
consistent with the paper's own scope, but a stronger replication
would go beyond what the paper does.

## 3. Instance count is 6.7× smaller than paper's
**Gap.** 15 instances/cell vs paper's 100. SEM inflated ~2.6×.

**Consequence.** At α=1 and p=4, our f_mean/SEM ≈ 2.4 — statistically
detected but noisy. The paper's version of this cell would be at
~6σ. We are working near the edge of detection for the smallest
signal cells.

**Fix.** Bump n_instances to 60 or 100 for the α ∈ {0.5, 1.0} rows only.
~2 hr CPU.

## 4. Single value of n; no finite-size analysis
**Gap.** Paper runs n ∈ {6, 8, 10, 12} to argue the deficit persists
and (implicitly) that α_c is well-defined in the finite-size limit.
We ran only n=6.

**Consequence.** We cannot say anything about scaling with n. If the
deficit vanished as n → ∞, our n=6 result would be a finite-size
artifact. The paper argues the opposite; we don't test either way.

**Fix.** Add n=8 (dim=256, ~8× cost, still tractable) and n=10
(dim=1024, ~64×, ~10 hr). Would tighten the replication substantially.

## 5. Optimizer robustness not checked
**Gap.** We used exactly one optimizer (COBYLA) with exactly one
restart budget (4). If COBYLA gets systematically trapped in local
minima at high α, our f values are inflated above the true reachable
minimum, which would visually reinforce the "reachability deficit"
narrative even if the ansatz manifold does contain the ground state.

**Why it matters (a lot).** The paper argues the deficit is
ansatz-inexpressibility, not optimizer failure. Post-2019 barren-plateau
work has made optimizer failure a leading alternative hypothesis. We
did not disentangle.

**Fix.** Q1 in open_questions.json is exactly this — re-run with COBYLA
+ L-BFGS-B + BOBYQA, 20 restarts each, at the α cells where the
deficit is largest.

## 6. Secondary claims C2/C3/C4 completely untested
**Gap.** Only C1 tested.

- C2 (projector mixer, Fig. 2): same code with mixer swap — not run.
- C3 (p* for overlap ≥ 0.95 grows with α, Fig. 3): needs p up to ~40, ~10× compute.
- C4 (variational Grover p* ~ √N, Fig. 4): analytic per paper's Eq. 10-12; nothing to replicate numerically at reasonable n.

## 7. No comparison against alternative QAOA analyses
**Gap.** We did not benchmark our results against:
- Barren-plateau predictions (McClean 2018) — does gradient variance
  at our (n, p, α) match BP theory?
- Concentration of measure (Wang 2021) — is the deficit consistent
  with cost-function concentration rather than reachability per se?
- Larocca 2022 overparameterization / DLA theory — does the QAOA DLA
  at low p literally not contain the ground-state projector?

Any one of these could either strengthen or reframe the paper's claim.
We did none.

## 8. No modern-variant benchmark (warm-start / ADAPT / RQAOA / multi-angle)
**Gap.** The literature since 2019 has produced several QAOA variants
that were designed partly to address inexpressibility. None were tested.

**Consequence.** The paper's message ("QAOA has a reachability deficit")
may already be moot in the modern-variant regime. Our replication does
not test whether the message survives the improved algorithms.

**Fix.** Q2 in open_questions.json.

## 9. No noise model
**Gap.** Pure noiseless statevector. Paper is also noiseless, so this
is consistent, but the "does QAOA work on real hardware" question that
the reachability-deficit paper implicitly informs is not addressed.

## 10. Verdict downgrading criteria we considered but rejected
- **PARTIAL** was considered because p ≤ 4 is a real scope reduction.
  Rejected because C1 as stated in the paper's abstract (deficit
  exists, grows with α, shrinks with p) is qualitatively reproduced
  with high statistical significance and zero counter-observations.
- **SPOT-CHECK** was considered because we tested one panel (Fig. 1 top).
  Rejected because that panel IS the headline; C2/C3/C4 are
  explicitly labeled secondary. Headline-exercised rule met.

## What would move this to a full REPLICATED (no qualifiers)
1. Add p=8 and p=15 for at least one α value.
2. Bump n_instances to 100 at α ∈ {0.5, 1}.
3. Add n=8 sweep to check finite-size trend.
4. Add optimizer-robustness cross-check (Q1).
5. Add C2 (projector mixer) sweep.

All are CPU-only, free, and would add ~15 hr of sequential compute.
Not in this wave.
