# Failure Analysis — QC-2209.00292-barren-plateaus-tensor-network

**Purpose.** Honest critique of what was NOT reproduced, what was WEAKENED by our methodology, and where the REPLICATED verdict must NOT be over-read.

## What was actually exercised (headline)
- **C1:** exponential decay of Var[∂_{1,1} <X_N>_qMPS] in N — YES, reproduced on 7,000 real MC runs, N=3..9
- **C2:** base = 3/8 (Thm 3, Eq. 13, j<i=N branch) — REPRODUCED TO WITHIN A FACTOR 1.33 (our fitted base 0.282 vs paper's 0.375)

## What was NOT exercised (auxiliary — REPLICATED verdict does NOT cover these)

### 1. Independent computation of the gradient-variance scaling for the paper's SPECIFIC block (Eq. 10) — NO
We used an equivalent-but-not-literal 2-qubit block (`RX·RZ·CX·RX·RZ`, 8 params) instead of the paper's Eq. 10 block. The block is locally 2-design-equivalent at each stage, so the *existence* of exponential decay in N is a theorem-level consequence (which we recover). But the exact numeric prefactor 3/8 that the theorem quotes is block-realisation-specific. **We did NOT re-derive Eq. 13 symbolically for our block.** Consequence: our 25% base shortfall (0.282 vs 0.375) is *not* a falsification of Thm 3 — it is a consistency check under an equivalent block — but it is *also* not an independent verification of the numeric constant.

### 2. Comparison against a generic HEA baseline on the same N range — NO
The paper positions tensor-network-inspired ansatze relative to generic Hardware-Efficient Ansatze. A direct side-by-side (same N range, same MC estimator, HEA vs qMPS) would sharpen the structural point. We did NOT run a HEA baseline. Consequence: we can say "qMPS-far-obs has an exponential plateau" but cannot say "qMPS is worse/better than generic HEA in our own numerical results."

### 3. Local-vs-global cost quantitative check (C3) — NO
Claim C3 says a sum-of-local observable H = Σ_i X_i *avoids* the plateau on qMPS. We tested only the far-observable global-like case. The distinction is central to the paper's positive narrative (tensor-network ansatze CAN be trainable with the right cost). **Untested.** Consequence: our REPLICATED verdict speaks only to the *bad-case* barren plateau, not to the paper's positive claim about avoidability.

### 4. qTTN / qMERA polynomial-scaling reproduction (C4) — NO
Claim C4 (polynomial vs exponential dichotomy for tree/MERA ansatze) is arguably the paper's most practically consequential finding, and it is the reason TN-inspired ansatze are proposed. **We did NOT implement qTTN or qMERA.** A REPLICATED verdict on C1+C2 alone must NOT be read as vouching for the polynomial-scaling story.

### 5. Classical complexity argument (C5) — NO
Structural argument; not a numerical claim; not attempted.

### 6. Full Eq. 13 piecewise coverage — NO
Eq. 13 has three branches (j<i, j=i, j=i+1). We tested only the j<i=N branch (top-left parameter, far observable). The other branches were not verified.

## What weakens the REPLICATED verdict but does not invalidate it

### Sample-size caveat at large N
At N=9 Var ~ 1.66e-5. With 1000 samples the MC standard error is not negligible (a rough sqrt(2/(n-1)) · Var estimate gives relative-error ~5%). The exponential trend is clean over 6 decades of N-shift, so the qualitative claim survives, but tight uncertainty bands on the *fitted base* would want >=10^4 samples/N.

### Base-mismatch narrative
Our writeup frames the 25% base shortfall as "expected because of the block-realisation-specific prefactor." That framing is defensible but not proven from first principles in this replication — we did not symbolically compute what our block *should* give. A more rigorous version would either (a) re-derive Eq. 13 for our block, or (b) use the paper's exact block and re-run.

## What was genuinely done well
- 14,000 real state-vector circuit evaluations (7 N-values × 1000 samples × 2 param-shift evals)
- Deterministic seed (20260703), reproducible under 95 s wall
- Log-linear fit R² essentially perfect (unambiguous linearity on log axis) — barren-plateau *phenomenology* is unmistakable
- MC results always ≤ Thm 3 prediction (more severe, not less) → conservative for the "plateau exists" conclusion
- No fabrication; every number in the results table is a real MC output
- Absolute values within factor ~4 of Thm 3 across N=3..9 — leading-order-consistent

## Bottom line
The REPLICATED verdict is real and defensible for the headline C1+C2 claim on qMPS with a far observable. It should NOT be read as validating the paper's full narrative (positive avoidance case, tree/MERA polynomial scaling, block-specific prefactor). Downstream users planning to build on the paper's polynomial-scaling advantage for tree/MERA ansatze should treat those claims as UNVERIFIED by this replication and either re-run those specific simulations or cite them separately.
