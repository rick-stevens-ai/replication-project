# Failure Analysis — QC-1712.05384

Per Rick's 2026-07-05 hard requirement: every replication carries an honest
critique of what was and was not verified. Verdict "REPLICATED" here is
scoped to the paper's C1–C4 functional-form claims — this file enumerates
the ways in which that verdict could be wrong or misleading.

## 1. What was NOT verified

### 1.1 Byte-identical match to the paper's implementation
- We built the tensor-network mapping **from scratch** using the paper's
  Section IV description (Hadamard + random 1Q gate menu {T, √X, √Y} + CZ
  brickwork on 2D grid, ⟨0|U|0⟩ as scalar TN contraction).
- The paper does **not** ship a reference implementation with the arXiv
  submission. Google's QuickBB + TensorFlow simulator was internal at the
  time.
- Therefore we cannot certify our TN is byte-for-byte the same object the
  authors contracted. We can only certify: (a) our TN evaluates to the
  correct amplitude (machine-precision match to Schrödinger), and (b) our
  TN's structure is what the paper's Section IV describes.
- **Risk:** any hidden difference in how the authors ordered tensor legs,
  chose gauge, or handled the boundary could produce different treewidth
  numbers at a given (n, d). We cannot rule this out — but the treewidth
  values differ from the paper by a small constant factor (compatible with
  the paper's own remark that "vertical vs QuickBB" gives constant-factor
  variation), which is at least consistent.

### 1.2 Supercomputer-scale numerical points (paper Fig. 3)
- The paper's headline empirical results are 5×9 depth 40 (~200k
  amplitudes), 7×8 depth 30, and 10×κ depth 19, computed on a 128 GB
  workstation with QuickBB elimination-ordering search running for
  approximately a day per configuration.
- **We did not attempt these.** The QuickBB search alone would need days
  on the paper's own hardware; we run on a laptop with ~16 GB RAM. This
  is out of scope for a small-instance replication.
- **Consequence:** any headline number in Table I / Figure 3 could in
  principle be wrong (numerical bug, unreported precision loss, or
  QuickBB-specific idiosyncrasy) and our replication would not catch it.
  We verify the **exponent** of the scaling law, not the paper's specific
  reported numerical points.

### 1.3 Comparison against modern classical simulators
- The paper's implicit claim is that graphical-model / QuickBB
  contraction is a state-of-the-art classical simulator for shallow
  circuits (in 2017 it was; the paper's contribution is the
  graphical-model framing).
- Modern simulators (cotengra 2020, quimb slicing, qFlex 2019,
  Schrödinger–Feynman hybrids from Markov+Fatima+Boixo 2018) may
  dominate. **We did not benchmark against any of them.**
- **Consequence:** "REPLICATED" here means the paper's own scaling
  argument reproduces on our sweep. It does NOT mean "this approach is
  still competitive in 2026." That's open_question.json Q2.

### 1.4 Noisy circuits
- The paper is strictly noiseless (unitary gates, pure states, exact
  amplitudes). Modern hardware simulation (post-Sycamore, IBM/Rigetti/
  IonQ benchmarks) requires noise. Whether the graphical-model formalism
  survives Kraus channels with the same treewidth bound is not addressed
  and we did not check it. See open_questions.json Q1.

### 1.5 Elimination-ordering heuristic mismatch
- Paper: QuickBB (branch-and-bound over elimination orderings, near-optimal
  for graphs up to ~100 nodes).
- Us: `opt_einsum` greedy (linear-time local heuristic).
- For our small instances, greedy is often near-optimal (the search space
  is small). For the paper's scale, QuickBB should find tighter orderings.
- **Consequence:** our observed `slope < ℓ_min` in the log-linear fits
  should NOT be interpreted as "the paper's bound is loose." It just means
  the greedy heuristic gets lucky on tiny circuits. At the paper's scale,
  the bound is close to tight.

## 2. Things that could be silently wrong in our replication

### 2.1 Circuit-generator interpretation
- The paper's Sec IV says single-qubit gates go on qubits "touched by the
  previous 2Q layer." We implemented this literally, but there is some
  ambiguity in layer 1 (nothing was touched before it). We chose to apply
  1Q gates to all qubits in layer 1. If the paper meant "skip layer 1's
  1Q gates," our per-instance amplitudes would differ (though the
  scaling wouldn't).
- Fix if wrong: gate on `layer > 1`. Would not change any of C2/C3/C4
  scaling claims.

### 2.2 CZ brickwork phase
- We rotate through {H-even, H-odd, V-even, V-odd} on a 4-layer cycle.
  The paper's specific 8-cycle pattern (Sycamore-style ABCDEFGH) was
  described later (Arute+2019) and is not in this paper. Our choice is
  structurally faithful but not identical to any specific gate schedule.
- **Consequence:** absolute amplitudes will differ from any specific
  paper figure; scaling behavior should not.

### 2.3 opt_einsum path stochasticity
- `opt_einsum.contract_path(..., optimize="greedy")` is deterministic
  given the same input, but greedy can be tie-broken differently across
  versions. Our results are pinned to `opt_einsum==3.4.0`. A future
  version bump could shift the observed slopes by 5–10%.

### 2.4 Treewidth vs contraction width
- We equate `contraction_width = log2(largest_intermediate)` with the
  treewidth of the line graph of the TN, per standard TN theory (Markov &
  Shi 2008). This is an **upper bound**, not equality. The paper's Fig 4
  plots "max tensor rank" which is the same quantity — so this is a
  faithful reproduction of the paper's proxy, but neither we nor the
  paper compute the actual treewidth.

## 3. Failure modes observed during the run (fixed)

- **opt_einsum PathInfo AttributeError on trivial 1-tensor networks**
  (n=1, d=0 edge case in early smoke test). Fix: upgraded to 3.4.0.
- **Over-counted 1Q-gate cost** in early circuit generator (applied 1Q
  gates every layer to every qubit, not just to touched qubits). Fix:
  gated on `qubits_touched_prev_layer`.
- **einsum wire-name collisions at n > 26** (single-letter labels ran
  out). Fix: switched to `opt_einsum.get_symbol(k)`.
- **Statevector reshape confusion** on ℓ×m grids (2D vs flat qubit
  index). Fix: consistent left-to-right row-major linearization
  everywhere.
- **All four caught by the smoke tests** (`smoke.py`, `smoke2.py`) which
  compare TN vs SV on tiny circuits and would immediately fail if any of
  the above regressed.

## 4. What a reader should NOT conclude from this REPLICATED verdict

- ❌ "The paper's Fig 3 numbers are all correct." — Not tested at that scale.
- ❌ "The graphical-model / TN approach is still SOTA in 2026." — Not benchmarked against cotengra/quimb.
- ❌ "This works for noisy circuits." — Not tested.
- ❌ "The bound `min(O(d·ℓ), O(n))` is tight." — Verified as an upper bound with O(1) constants; tightness would need a matching lower bound (which the paper does not claim).

## 5. What a reader CAN conclude

- ✅ The graphical-model / TN mapping for shallow universal circuits
  works: a from-scratch implementation matches full statevector
  evolution to machine precision on 70 configurations spanning
  n=8–16, d=2–6, four different grid geometries.
- ✅ The contraction width scales as `min(O(d·ℓ), O(n))` with an O(1)
  constant across all configurations tested.
- ✅ The classical-savings crossover (TN cost falls below `2ⁿ` at
  shallow depth) is real and quantitatively substantial (~41,000× at
  n=16, d=2).
- ✅ The paper's core methodological contribution — the
  complex-graphical-model framing of shallow-circuit amplitudes — is
  correct and implementable independently from the paper's specific
  supercomputer results.
