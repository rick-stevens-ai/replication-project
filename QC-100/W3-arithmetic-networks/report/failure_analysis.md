# Failure Analysis / Honest Critique — W3 Arithmetic Networks

Verdict was **REPLICATED**, but a full-honesty accounting requires flagging
the exact things we did *not* verify, and where our replication could still be
wrong.

## 1. Independent Reimplementation Check
- **Claim**: We reimplemented the paper's exact subnetworks gate-by-gate
  (CARRY, SUM, ripple adder, adder-mod-N) using only NOT/CNOT/Toffoli.
- **Honesty**: True. `replicate.py` was written from Figs. 2–4 of the paper
  without inheriting any modern quantum-arithmetic library. This is a genuine
  independent reimplementation, not a wrapper around Qiskit's `qft_add` or
  similar.
- **Residual risk**: We could have accidentally encoded a *different* correct
  reversible adder that happens to give the same input/output map. The
  gate-count-slope-of-8 exactly matches VBE's Fig. 3 structure, which is
  strong circumstantial evidence that it *is* VBE's construction — but we did
  not do a formal circuit-equivalence check against a reference
  implementation of Fig. 3.

## 2. Gate-Count / Correctness Reproduction (Not Just Quotation)
- **Claim**: The paper's asymptotic gate counts (O(n), O(n²), O(n³)) were
  *reproduced*, not merely quoted.
- **Honesty**: Partially. We measured actual emitted gate counts for the
  plain adder at n=2..8 and got slope 8, intercept −2, R² = 1.00000 — this
  is genuine reproduction of the linear scaling. For multiplication O(n²)
  and exponentiation O(n³), the scaling follows *structurally* (n adders
  per mult, n mults per exp) — we did not independently sweep n and fit a
  quadratic/cubic. This is called out as ✓ structural in the results table
  and is a genuine gap.

## 3. Reversibility Overhead vs Classical Arithmetic
- **Claim requirement (Rick's directive)**: Was the comparison against
  classical arithmetic (as a reversibility-overhead check) made?
- **Honesty**: **Not attempted.** The paper's contribution is that arithmetic
  can be made *reversible* in polynomial gates and qubits; a natural probe is
  "how many more gates does the reversible version cost than the classical
  version?" A classical n-bit ripple adder costs ~5n gates (2n XOR + 3n AND);
  our reversible version costs ~8n Toffoli/CNOT-equivalents. This ratio
  (~1.6×) is a meaningful reversibility-overhead metric that we did not
  report because the paper itself does not make this comparison and the
  gate-model choice is not canonical. **Flagged as a genuine gap** — should
  be added in a v2 replication.

## 4. Qubit / Depth Accounting
- **Claim**: The three memory formulas 7n+1, 5n+2, 4n+3 were reproduced
  quantitatively.
- **Honesty**: True for the *qubit* count — we evaluated the formulas for
  N ∈ {15, 21, 35} and matched the paper's "about 20 ions" for N=15 exactly
  (5n+2 = 22 at n=4). **False for depth** — we did not measure circuit depth
  (only gate count). Depth is a separate metric (parallelizable gates can
  reduce depth below total gate count) and is a known optimization target of
  later papers (Draper QFT adder trades gate count for depth). **This is a
  scope gap.**

## 5. Full-Statevector Unitarity of Composed Circuits
- **Claim**: Adder, mod-adder, mult, and exp are all reversible unitaries.
- **Honesty**: Only the plain adder was verified as a full unitary
  (permutation over 2^(3n+1) states at n=2,3). Adder-mod-N was verified as
  classical-reversible only (all (a,b)<N with temp reset), not as a full
  permutation. Controlled mult and modular exp were verified at the
  composition + basis-state level only. This is a standard scope limit
  (dense-state simulation of even a 29-qubit exp circuit is impractical),
  but it means our unitarity claim is *strongest for the plain adder* and
  progressively weaker as we compose upward.

## 6. What Would Break This Replication?
- If a bug in `replicate.py` happened to preserve classical input/output on
  every (a,b) we tested but violated unitarity outside the basis states we
  swept — the mod-adder and mult/exp checks would miss it. The plain-adder
  full-permutation check at n=2,3 is our only defense against this class of
  bug for those n; at higher n we're relying on inductive structure.
- If the paper had a subtle gate-count constant we misread from Fig. 3, our
  measured slope of 8 would differ from the paper's stated constant. We
  believe 8 matches VBE Fig. 3 (2 Toffoli + 1 CNOT for CARRY, similar for
  SUM, over n bits) but a direct-from-figure double-check would strengthen
  this.
- If the paper's "about 20 ions" for N=15 was meant under a different
  memory-reduction scheme (they cite 5n+2), our match (22 at 5n+2) could
  be coincidental. We believe not — the paper's own text supports this
  interpretation — but this is worth flagging.

## Summary
The replication is **honest and reproducible** within its stated scope. The
plain adder is verified to the highest possible standard (full unitary
permutation). Adder-mod-N is verified exhaustively as a classical-reversible
function with temp reset. Mult and exp are verified at composition level.
Gate-count linearity is exact. Memory formulas and the "about 20 ions"
figure are exact.

**Missing / not attempted** (flagged for transparency):
- Depth measurement (only gate count).
- Reversibility-overhead comparison vs classical adder.
- Independent sweep of mult O(n²) and exp O(n³) fits.
- Full-statevector unitarity for adder-mod-N, mult, exp.
- Circuit-equivalence check against a reference Fig. 3 implementation.

None of these gaps invalidates the REPLICATED verdict on the paper's
*headline claims*, but they define the frontier of what a v2 replication
should address.
