# Failure Analysis — arXiv:1803.03621 replication

Honest critique of what this replication did NOT verify and where its verdict could be legitimately challenged.

## What we DID verify (strengths)
- **C1 (MU RB fidelity extraction)**: at d ∈ {4, 8, 16}, our fits recover the analytic ground-truth fidelity to 4-5 significant digits, with mean errors 0.04-0.48 × 10⁻³ — TIGHTER than the paper's 4.5-9.2 × 10⁻³ (the paper's larger d and single-m estimator explains the gap). The order-of-magnitude methodological claim is genuinely replicated.
- **C2 (Clifford generator RB)**: at n=2, p ∈ {0.99, 0.98, 0.95}, our fits give 0.4-0.6 × 10⁻³ errors, safely below the paper's Table 3 best cell (1.44 × 10⁻³). Replicated in the high-fidelity regime.
- **C4 (analytic F(T))**: the depolarising-to-fixed-state formula was rederived and used consistently as ground truth; the numeric fits match to 4-5 digits.
- **C6 (O(d) structural claim)**: confirmed by construction — our `Monomial.__matmul__` uses fancy-indexing and never expands to a dense matrix during composition.

## What we did NOT verify (weaknesses)

### 1. Paper's exact Table 1 cells not reproduced
The paper's cells are d ∈ {64, 128, 1024} with M ∈ {100, 1000} and 100 channels/cell. We ran d ∈ {4, 8, 16} with 20 channels/cell. Our replication demonstrates the SAME method at SMALLER scale; it does not reproduce THE SAME NUMBERS. A strict reviewer could legitimately say "you didn't replicate Table 1, you demonstrated a smaller-scale analogue." The reason: we used dense d×d matrices for readout clarity even though our `Monomial` class supports O(d) sparse operations. Running the paper's exact cells requires keeping density matrices sparse throughout — engineering work, not new science, but not done here.

### 2. Approximate-2-design fitting formula NOT independently reimplemented for a non-Clifford group
Rick's hard-requirement asks specifically: was the approximate-2-design fitting formula independently reimplemented and behavior verified for a specific non-Clifford group vs quoted?  
**Answer: NO.** We used a SINGLE-EXPONENTIAL fit `A + B·f^m` throughout. The paper's genuine theoretical contribution is a K-TERM exponential fit whose degree K equals the number of inequivalent irreps of G appearing in the representation. For MU(d, 8) with the specific noise channels we chose, a single exponential happens to work (because the relevant representation is close to irreducible in the sense that matters). But we did NOT stress-test the framework on a group where the single-exponential fit provably fails and the multi-term fit provably succeeds. This is the paper's DISTINCTIVE NOVEL CLAIM and it is untested by this replication.

### 3. Concentration bounds NOT empirically tested
The paper gives Hoeffding-style upper bounds on Pr[|P̂_m − P_m| > ε]. We report point-estimator errors only. Whether those bounds are empirically tight, or whether the true tail decays faster/slower than the bound, is not addressed. This matters for practical resource planning of lab RB campaigns.

### 4. NO comparison against exact Clifford RB
A rigorous cross-check would run a canonical exact-Clifford RB implementation (qiskit-experiments or stim) on the same noise channel and compare the two estimates. We did NOT do this. Our ground truth is the analytic formula for F(T) (which is straightforward for the specific channels used). This means our "replication" is really a self-consistency check: fit ≈ analytic formula. If the paper's method had a systematic bias that also appeared in the analytic formula derivation (unlikely but not ruled out), we would not catch it.

### 5. C5 (graceful degradation at low p) UNTESTED
Paper Table 4 reports a 27 × 10⁻² error at p=0.6, illustrating that the framework degrades gracefully as noise breaks the δ-covariance assumption. We only tested p ∈ {0.9, 0.95, 0.98, 0.99}. The low-p regime — where the framework's failure mode is most interesting — was not exercised.

### 6. C3 (three-protocol equivalence) shows P2 fails at small b
Our P2 (generator-based, b=3) gives 2.3 × 10⁻³ error — an order of magnitude worse than P1 and P3. The paper's Fig 1 caption implies indistinguishability without a b-qualifier. Our data shows the equivalence is TRUE for b ≥ 15 (well beyond the mixing time of the 11-generator random walk on MU(4,8)), but FALSE at b=3. This is honest and reported as PARTIAL for C3, but a reader of the paper alone would not know that a specific b-choice is load-bearing.

### 7. LLM judge is single-source
We queried one judge (Argo GPT-5.2, free). A robust verdict would combine at least 2-3 judges (e.g., Claude Opus 4.7, Nemotron-3-Ultra, GPT-5.4) with a consensus rule. This was deferred.

## Verdict-preservation reasoning
The queue verdict is REPLICATED. The on-disk REPORT.md verdict is PARTIAL, and the report author (also this replicator) explicitly enumerates why PARTIAL is the honest label:
- C1, C2 replicated (fidelity extraction works)
- C3 partial (b-qualifier missing from paper's claim)
- Paper's distinctive novel claim (multi-term irrep fit) untested
- Paper's exact numeric cells (d=1024, n=5) not reached

Given the honesty requirements from Rick 2026-07-05, we preserve **PARTIAL** — matching the on-disk substance, not the queue label. Upgrading to REPLICATED would require running the exact paper cells at d ∈ {64, 128, 1024} with the sparse-simulator path AND stress-testing the multi-term irrep fit on a group where single-exponential fits fail. Neither is expensive; both are deferred as "engineering not science" work items that would move the verdict.

A stricter reviewer might further downgrade to SPOT-CHECK on the grounds that only 2 of 7 claims were empirically tested (C1, C2), 1 partially (C3), 2 confirmed structurally (C6, C7), 1 confirmed analytically (C4), and 1 not tested at all (C5). We choose PARTIAL as the middle-ground honest label.

## What would move the verdict
- **To REPLICATED**: rerun C1 at paper's exact (d, M, channels) cells using the sparse-simulator path; run n=5 Clifford generator RB with stim; ADD a multi-term irrep fit test on a reducible-representation group to exercise the paper's distinctive contribution.
- **To NO-GO**: nothing observed; no claim was contradicted, no simulator bug found, no failure to reproduce order-of-magnitude behaviour.
