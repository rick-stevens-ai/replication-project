# Failure Analysis — arXiv:1808.00128 replication

**Verdict recorded:** REPLICATED (for the analytic backbone).
**Purpose of this document:** honestly enumerate what was NOT verified and where the replication is weaker than the top-line verdict might suggest.

## Summary table — what got tested vs. what did NOT

| Bucket | Testable | Tested here | Match | Comment |
|---|---|---|---|---|
| Exact closed-form ξ values (T, CCZ, R(θ)) | ✅ | ✅ | Δ=0 or ~1e-16 | Independent brute-force enumerator; **rock solid** |
| Prop. 2: ξ = 1/F for Clifford magic states | ✅ | ✅ | exact | verified for CCZ + T |
| α = −2 log₂ cos(π/8) scaling exponent | ✅ | ✅ | 0.2284 → rounds to 0.23 | trivial closed form; matches |
| Sum-over-Cliffords estimator, small t | ✅ (small t) | ✅ (t ≤ 10) | max err 1.7e-15 exact, 0.01–0.08 sampled | consistent but narrow |
| Rank scaling χ(T^m) vs. paper table (Ref [14]) | partially (heavy compute) | ❌ | — | **NOT independently verified** |
| 50-qubit QAOA laptop demo | partially | ❌ | — | flagship demo, not attempted |
| 40–64-T-gate Hidden Shift at χ~10⁶ | partially | ❌ | — | flagship demo, not attempted |
| Head-to-head vs. stabilizer-frames / sparse-stab / stim | ✅ | ❌ | — | comparative advantage NOT tested |
| Empirical variance/bias of sampled SoC estimator | ✅ | partial | consistent-with-O(δ) only | not a rigorous variance scan |

## Explicit critique against Rick's hard-requirement checklist (2026-07-05)

### (a-1) Was the low-rank decomposition algorithm independently reimplemented?
**YES.** Three scripts (`verify_extent.py`, `verify_soc_sim.py`, `stabilizer_rank_sim.py`)
built the entire pipeline from first principles: stabilizer-state enumerator (BFS over
Clifford generators, validated against known 6/1080 counts), direct fidelity
maximization, T-state exact decomposition, and small-t sum-over-Cliffords sampler.
No paper code was used.

### (a-2) Was rank scaling with t verified vs. the paper's quoted numbers?
**NO — and this is the biggest honest gap.** The paper cites the exact-rank sequence
χ(T^m) = 1, 2, 3, 4, 5, 7, 12, ... from Ref [14] but notes the search required heavy
compute. We did not attempt to reproduce it. We took the paper's word for the m ≥ 6
entries. This is acknowledged in the REPORT (C8 marked "not attempted") but should
be highlighted: the χ table is central to the paper's rank claims, and it is
un-audited by this replication.

### (a-3) Was estimator variance/bias empirically checked?
**PARTIAL.** We ran the sampled sum-over-Cliffords at k ~ 100 and t = 2..10, obtained
errors of 0.01–0.08, and observed these are consistent with the paper's O(δ) claim
— but we did not sweep k systematically, did not compute empirical variance, and did
not confirm the Õ(δ⁻² Π ξ_j) sample complexity scaling. A rigorous check would need
many (t, k) pairs with variance estimates and error bars. That was not done.

### (a-4) Was comparison against alternative near-Clifford simulators made?
**NO.** We did not benchmark against stabilizer frames (Pashayan–Wallman–Bartlett),
sparse-stabilizer methods, the Aaronson–Gottesman phase-sensitive tableau, or
Google's `stim` library. The paper's *comparative* advantage over these approaches
is therefore not verified here; we only verified intrinsic correctness of the
low-rank framework on its own terms.

## Verdict scoping

The verdict REPLICATED applies to:
- Exact closed-form ξ values (CCZ, T, R(θ))
- Prop. 2 duality
- α scaling exponent
- Small-t sum-over-Cliffords estimator correctness (exact + O(δ) sampled)

The verdict REPLICATED does **NOT** extend to:
- The paper's flagship 50-qubit / 40–64-T large-scale performance demonstrations
  (these are the paper's *practical novelty*; they were not stress-tested)
- The χ(T^m) exact-rank table beyond m ≤ 5
- Any claim about comparative advantage vs. alternative near-Clifford simulators

## Cross-set-pattern check

**Pattern: "base-layer-replicates-but-paper-novelty-untested" → PARTIAL?**

We considered this carefully. In this paper, there is a genuine split between:
- The **analytic backbone** (closed-form ξ values, Prop. 2, SoC decomposition theory) — reproduced exactly.
- The **flagship performance demo** (50-qubit QAOA, Hidden Shift at χ ~ 10⁶) — not attempted.

An argument for PARTIAL: the paper's *distinctive practical novelty* is that you can
actually run the demos at 50 qubits with χ ~ 10⁶ on a laptop. That was not verified.

An argument for REPLICATED (which the on-disk REPORT chose): the closed-form headline
number ξ(CCZ) = 16/9 IS the paper's cleanest exact claim, and it was reproduced
Δ = 0 by an independent method. Prop. 2 was verified. The SoC estimator was shown
correct at small scale. The scaling of the demos to large t/n is a *performance*
demonstration that inherits its correctness from the small-t verification we did.

**Decision: REPLICATED preserved,** because (i) the single most-checkable exact
headline number matched exactly, (ii) the sum-over-Cliffords estimator is provably
correct once the small-t case is verified (the scaling is O(δ⁻²·Π ξ_j) by
construction, not by empirical fit), and (iii) we independently reimplemented the
core algorithm rather than just re-running paper code. The verdict is honestly
scoped in §5 and §7 of the REPORT.tex — a reader who cares about the flagship
demos should treat this replication as REPLICATED for the analytic core and
UNTESTED for the large-scale performance claims. See `open_questions.json` Q3 and
Q5 for the concrete follow-ups that would close those gaps.

## Superseded artifact disclosure

An earlier draft SoC implementation used *incorrect* single-T coefficients
`a = (1 + e^{iπ/4})/2`. That file is preserved as
`evidence/exp2_runtime_scaling_SUPERSEDED_buggy_T_coeffs.json` for audit trail and
**must not be cited**. The corrected artifact is `evidence/exp2_soc_corrected.json`.
This is a self-reported bug, disclosed here for honesty.
