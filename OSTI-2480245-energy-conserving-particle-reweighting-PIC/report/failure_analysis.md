# Failure Analysis — OSTI 2480245

Honest critique of where this replication is strong, where it is weak, and where the claim of PARTIAL could reasonably be contested in either direction.

## What went right

1. **Every declared mathematical invariant of the novel operators was verified to machine precision** on tens of thousands of random events. This is not a small thing: the paper's central contribution is *correctness* (energy conservation of the split, momentum conservation of the merge with a bounded ΔKE loss), and every such claim was reproduced independently from the equations alone.
2. **The paper's headline accuracy feature — imaginary-velocity-split rejection** — was exercised: 0 leaks across 20,000 attempts, with the polar-π/2 fallback firing correctly on inaccessible geometries.
3. **The Test-4.2 structural claim** (real-electron growth rate independent of computational count N_c, computational count bounded N_c…1.1·N_c) reproduces at both the qualitative and quantitative level: β = 3.0507 s⁻¹ for every N_c ∈ {10, 100, 1000, 10000}, matching the paper's ~3.06 s⁻¹.
4. **Cutoff behavior was measured, not assumed**: 1388 of 18,612 candidate merges were rejected by the Eq-9 cutoffs (Δv < v_thermal at T=5 eV; α < 30°), confirming that the gating logic is active and not vacuous. Median ΔKE loss 0.062 %, 95th percentile 0.587 % of pair KE — matches the paper's qualitative "small" claim.
5. **The LLM-judge (free Argo gpt-5.2) independently returned PARTIAL** with coverage 0.78 and agreement 0.80, aligning with our own honest self-assessment.

## What went wrong / what was not exercised

1. **Aleph itself was never run.** Sandia's PIC-DSMC code is proprietary and no public code/data package accompanies the paper. This is the single biggest gap: everything downstream of the operator-level reimplementation is either (a) an abstraction we built, or (b) not tested.
2. **The paper's headline figures were not reproduced.** Figs 4–10 (VDFs from Test 4.1, wall-time curves, EEDF shapes from Test 4.2, Bolsig+ comparison) exist only in the paper; we did not attempt to reproduce them numerically or pictorially. A stricter reviewer would say: "you replicated the *specification*, not the *demonstration*."
3. **Test 4.1 (coupled sheath with bump-on-tail beam) was not attempted.** This is the paper's showcase test that reweighting does not visibly perturb the coupled PIC self-consistent field. We have no independent evidence that this claim holds — only that the *operators* preserve their invariants at the level of individual events. It is logically possible (though unlikely) that operator-level correctness fails to propagate to whole-system correctness through some accumulated bias we did not measure.
4. **Test 4.2 was abstracted to a 0D bookkeeping model** — no cross-sections, no EEDF evolution, no Bolsig+ comparison. Our "growth-rate independence" result is therefore a *structural* claim about the reweighting control loop, not a physics-faithful reproduction of the H₂ swarm.
5. **C7 (precision improves with N_c) is not isolable in our harness.** Our abstract 0D bookkeeping model recovers β to floating-point precision at *every* N_c, because it lacks Aleph's stochastic DSMC event noise (the source of the precision limitation at small N_c). We flagged this honestly rather than claiming C7 reproduces (which would be false-positive) or claiming C7 fails (which would be false-negative).
6. **The reimplementation was single-cell / single-element.** AMR-adjacent behavior, boundary-crossing children, and cross-rank / cross-GPU migration are all untested. If Aleph relies on any subtle inter-cell fix-up that the paper did not spell out, our reimplementation does not exercise it.
7. **No relativistic / electromagnetic extension probed** — the paper is explicitly electrostatic and non-relativistic. Any downstream user of these operators in an EM PIC context is on their own.

## Why PARTIAL is the honest label (not REPLICATED, not SPOT-CHECK)

- **Not REPLICATED**, because "REPLICATED" (in this project's rubric) implies numerical reproduction of the paper's headline demonstrations. We did not run Test 4.1's coupled sheath and did not reproduce Figs 4–10.
- **Not SPOT-CHECK**, because a spot-check implies cursory verification. We performed a full operator reimplementation from equations, ran ~40k conservation events with quantitative error tables, and executed a 4-decade N_c scaling sweep. This is substantially more than a spot-check.
- **PARTIAL** captures: the mathematical core of the method is fully vindicated independently, but the whole-code simulation demonstrations remain out of independent reach. Both the operator-level fidelity (fully passed) and the demonstration-level gap (untested) are documented quantitatively.

## Risks of over-claim (if a reviewer pushed us to REPLICATED)

- The operator invariants passing does not, by itself, prove that thousands of operator applications in a coupled simulation do not accumulate systematic bias. That would require running the full Aleph problem.
- Our 0D abstraction of Test 4.2 could be masking a physics issue that only appears with real cross-sections and EEDF feedback.
- Judge coverage 0.78 (not 1.0) and agreement 0.80 (not 1.0) both signal that a nontrivial fraction of the paper's claims remain untested.

## Risks of under-claim (if a reviewer pushed us to NO-GO)

- The paper's central contribution *is* the operator design and its invariants. Those are 100% reproduced.
- The Test-4.2 structural scaling result is nontrivial (β independent across 4 decades of N_c to 1e-15 relative spread) and matches the paper's absolute value.
- Absent Aleph, there is no obviously stronger independent test we could have run.

**Net:** PARTIAL is the tightest honest label. The method is correct; the deployed system is out of reach.
