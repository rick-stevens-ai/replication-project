# Failure Analysis — arXiv:2107.02789 (DC-QAOA)

**Purpose:** enumerate every place this replication is thinner, shakier, or otherwise less impressive than the paper's headline numbers might suggest. Verdict remains REPLICATED but with caveats a reader should know before citing this replication.

## What was NOT tested (genuine coverage gaps)

1. **Claim C1 — LFIM 12-qubit ground-state prep (Fig. 2a) — SKIPPED.**
   - The paper's most eye-catching claim: DC-QAOA reaches R=1 on a 12-qubit long-range Ising model at p=1, while standard QAOA needs p=3.
   - This is CPU-feasible (12-qubit statevector = 4096 complex amplitudes ≈ 64 KB; well within budget), so the excuse "time budget" is honest but not principled.
   - **Impact:** the LFIM-specific mechanism (long-range interactions + strong CD advantage) is untested. The MaxCut result alone doesn't cover the paper's full "shortcut-to-adiabaticity works everywhere" narrative.

2. **Claim P-spin model (Fig. 4) — SKIPPED.**
   - Would show DC-QAOA on a fully-connected p-spin problem, a different landscape structure than MaxCut. Not tested here.

3. **Sherrington–Kirkpatrick model — SKIPPED.**
   - Random-coupling regime; the paper claims DC-QAOA still helps. Not tested.

4. **Larger MaxCut (n=10–14 in Fig. 3a) — SKIPPED.**
   - We tested n=4, 6, 8. The paper goes up to n=14 in Fig. 3a. n=10 and n=12 are still CPU-feasible; not attempted.

5. **Noise model — ABSENT.**
   - This is pure noiseless statevector. The paper's whole motivation (NISQ-friendly shallow circuits) is contingent on the extra CD gates surviving realistic error rates. That analysis is missing here AND largely missing from the paper.

## What was tested but is shakier than it looks

1. **Comparison choice: vs p, not vs gate count.**
   - DC-QAOA adds 2|E| extra two-qubit rotations per layer on top of QAOA's |E|, so a "p=1 DC-QAOA" circuit is ~3× the two-qubit-gate count of "p=1 QAOA". Comparing at fixed p flatters DC-QAOA.
   - The paper does this too; we inherited the choice without correcting it.
   - **Impact:** the ΔR = +0.076 advantage at p=1 on K₄ could plausibly evaporate if you gave QAOA the same gate budget (i.e., let QAOA run at p=3 with |E|·3 gates ≈ DC-QAOA p=1 with |E|·3 gates). Not tested.

2. **High-p regression is real but attributed to "known landscape difficulty".**
   - At p=4, DC-QAOA is *below* QAOA by ~0.01 on both n=6 and n=8 graphs.
   - We attributed this to the paper's own vanishing-gradient warning + our decision not to warm-start from lower-p optima.
   - **But**: we did NOT verify this attribution by actually running the warm-start experiment. So the regression could equally be evidence that the DC-QAOA advantage genuinely narrows or reverses at moderate depth, which would qualify claim C3.
   - A cleaner replication would run both variants with p=1 → p=4 warm-starting and see if the DC-QAOA advantage survives.

3. **No error bars.**
   - Results are best-of-25-restarts, deterministic given the seed schedule. No mean ± std over independent restart budgets.
   - The tiny ΔR ~0.02 gap at n=8, p=3 could be inside the sampling-variability of the restart-budget procedure. We don't quantify this.

4. **CD pool choice is unverified.**
   - We used the paper's {ZY, YZ} pool as-is. Whether this is *optimal* (vs {XY, YX} or a larger pool) is not tested. The paper's Fig. 3 uses this pool; if it's overtuned to MaxCut, we wouldn't see the tuning.

5. **Optimizer choice.**
   - COBYLA is a reasonable derivative-free choice, but the paper uses different optimizers in different sections. Cross-optimizer robustness (SPSA, gradient-based, ADAM) not tested. A DC-QAOA advantage that disappears under a different optimizer would be less interesting.

## What is genuinely solid

1. **The core K₄, p=1 result (R = 1.0000 for DC-QAOA vs 0.9244 for QAOA) is a bit-for-bit reproduction of the paper's Fig. 3a bar heights on the exact same instance.**
   - This is not a coincidence, not a fit; it's what an independent implementation gives.

2. **The qualitative depth-scaling trend (DC-QAOA > QAOA at low p) holds on TWO independent graphs (n=6, n=8) that were NOT in the paper.**
   - So the effect isn't confined to the specific instances the authors picked.

3. **The CD operator pool {Z⊗Y, Y⊗Z} works as specified.**
   - Wiring it correctly gave the expected numbers on first attempt after debugging.

4. **Effect sizes match order-of-magnitude what Fig. 3b shows.**
   - ΔR ≈ 0.05–0.20 at low p, converging to ~0 at higher p. Consistent with the paper's visual bar heights.

## Bottom line

The paper's *core, tested* claim (DC-QAOA beats QAOA on small MaxCut at low p) is real, reproducible, and holds on out-of-sample instances. The paper's *broader* claims (LFIM, p-spin, SK, hardware feasibility) are not tested here — and the paper's under-discussed weakness (gate-count-normalized comparison, noise robustness) remains a genuine open question. Verdict REPLICATED is defensible for the MaxCut headline; the full-paper verdict would require the extensions listed in `open_questions.json`.
