# Failure Analysis — OSTI-3364673

## What partially failed

**Symptom:** 4 of 105 dimension tests disagree with the paper's Theorem I.1.

**Concrete cases:**

| Graph | Paper prediction | Numerical (both methods) | Ratio |
|---|---:|---:|---:|
| a_14 on K_{1,3}   (n=4) | 20   = 2·sp(4)  | 72   = 2·sp(8)  | 3.60x |
| a_14 on K_{3,3}   (n=6) | 272  = 2·sp(16) | 1056 = 2·sp(32) | 3.88x |
| a_14 on K_{1,5}   (n=6) | 272  = 2·sp(16) | 1056 = 2·sp(32) | 3.88x |
| a_14 on H-graph   (n=6) | 272  = 2·sp(16) | 1056 = 2·sp(32) | 3.88x |

All four are in the same branch: `a_14, G bipartite, l and m both odd`.

## Root-cause analysis performed

1. **First hypothesis: OCR / extraction error.** Solution: cross-check with `pdftotext -raw`, which preserves line breaks for super/subscripts. Result: raw text unambiguously reads `sp(2^{n-2})⊕2, l,m odd` — the paper does state `n-2`.

2. **Second hypothesis: generator-set mismatch.** The paper gives two equivalent generator sets for a_14: `{XX, YY, XY, YX}` (symmetric) and `{XX, YY, ZI, IZ}` (with 1-local Z's). Both should generate the same Lie algebra. Verified numerically: both variants give dim 6 on 2 qubits, dim 72 on K_{1,3}, identical closures.

3. **Third hypothesis: my bit-symplectic DLA closure is wrong.** Solution: rewrite with explicit 2ⁿ × 2ⁿ complex matrices and SVD-based R-linear-independence tracking (`dla_matrix.py`). Result: gives dim 72 on K_{1,3} for a_14. Independent method, same answer.

4. **Fourth hypothesis: subgraph inclusion violated.** Since K_{1,3} ⊂ K_4, we must have dim(a_14^{K_{1,3}}) ≤ dim(a_14^{K_4}) = 126. Numerically 72 ≤ 126 ✓. Also verified `closure(K_{1,3}) ⊂ closure(K_4)` as sets. Consistent.

5. **Fifth hypothesis: paper's Lemma IV.5 upper bound applies but is not tight for l=1 or m=1.** The paper's Lemma IV.5 says the upper bound in (14) is tight for **k=4, 14**. Its proof does induction from K_{1,1}. Numerically, dim(a_14^{K_{1,1}}) = 6 (which is dim su(4) fully) — but for the theorem's own scheme, K_{1,1} = K_2 which is treated separately in reference [1]. The a_14^{K_2} row in Appendix B of [1] would tell us what the paper *expects* the base case to be; that is not directly checkable from this paper alone.

## Best current explanation

Most likely a **typo in the exponent** of the theorem statement (n-2 → n-1) for the `a_14, BP, l,m odd` branch. Evidence:
- Every other subcase of Theorem I.1 matches numerically (101 of 105).
- The numerical dim matches a clean closed form `sp(2^{n-1})^{⊕ 2}` across four distinct graph topologies at two different n values (4 and 6).
- The structural (k-equivalence) claim of the theorem is corroborated: H-graph and K_{3,3} give the *same* wrong-per-paper dim 1056, so the equivalence holds — only the dimension formula is off in that branch.
- Alternative causes are less parsimonious: an implementation bug would likely spread across other branches, and a genuine deep contradiction in the theorem's proof would be a much bigger deal.

## What did not fail (highlights)

- All 27 complete-graph K_n dimensions (k ∈ {0,2,4,6,7,14,16,20,22}) matched exactly.
- All 9 tests on the H-graph matched the K_{l,m} predictions (except a_14 BP-odd-odd) — confirms Theorem III.12's k-equivalence claim.
- The triangle-plus-pendant graph (NBP, single vertex of degree 3) matched K_4 for all 9 k-values — confirms Theorem III.4/III.9.
- All 6 b-type tests matched.
- Two independent DLA implementations agreed on every case, including all 4 anomalies.

## What we did not attempt

- **Explicit commutator-word reproduction** (Lemma III.6, III.7 equations (4)-(7)): these are constructive proofs that specific nested-commutator words produce specific new-edge Pauli operators. We verified the *existence* of such words indirectly via closure equivalence, but did not reproduce them symbolically.
- **Killing form / Cartan-type invariants** to distinguish e.g. sp(d) from so(d+1) at the same dimension — the paper's claim is more specific than dimension.
- **Larger n (n ≥ 7)**: our bit-symplectic closure would still be fast (4^n ≤ 16 384 for n=7), but the paper's classification is fully determined by n, l, m alone, so a positive check at n=6 is representative.
- **Random / Erdős-Rényi graph sweep**: only a small hand-picked battery was run. The paper's theorem is a universal quantifier; a random-graph sweep would strengthen confidence at the cost of time (see Open Questions Q4/Q5).
- **Reaching out to the authors** for confirmation of the suspected typo. Left as follow-up.
