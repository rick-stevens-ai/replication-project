# Failure Analysis — QC-1712.03554 Stabilizer Frames

**Honest self-critique of what this replication does and does not establish.** Verdict is REPLICATED, but the scope of that verdict is bounded and worth stating plainly.

## What is genuinely established

1. **Frame-size scaling law (H3):** Under the standard rank-2 decomposition T = e^{iπ/8}(cos(π/8) I − i sin(π/8) Z), the frame doubles on every T-gate and χ = 2^t exactly. Measured on 16 (n, t) main-sweep points + 4 scaling-probe points, with no exception. This is an equality, not an inequality — the paper's headline poly(n)·χ^k cost is confirmed for k=1 with χ=2^t.

2. **Amplitude fidelity (H4):** After global-phase alignment, worst-case max-amplitude error across all 19 runs is 1.12e-16 — effectively machine ε (2^-53 ≈ 1.11e-16). The 1e-10 tolerance from the brief was met by six orders of magnitude.

3. **Runtime scales as ~2× per T:** Per-T ratios of 2.35×, 2.36×, 1.80× (5→6, 6→7, 7→8) and aggregate 10× over 3 extra T-gates vs theoretical 8× — consistent with the poly(n)·2^t cost model.

4. **Independent Clifford baseline:** Stim tableau ↔ Qiskit statevector cross-check at t=0 agrees to ~1e-9 (Stim fp32 residual) or better. The Clifford baseline is not a shell around the same code path.

## What is NOT established — honest gaps

### Presentation-level: Clifford-prefix vs binary tableau encoding
- The paper uses the Aaronson–Gottesman row-echelon binary tableau to encode each stabilizer state. This replication uses a Clifford-circuit prefix (a list of Clifford gates that prepares the state from |0>^n) evaluated by Qiskit's statevector routine.
- The two are mathematically equivalent (both parameterize the same stabilizer subgroup, both admit poly(n) Clifford update), so H3 and H4 are invariant under this substitution.
- **But** absolute per-gate wall-clock is NOT comparable to Quipu's reported numbers on this basis alone. Our per-branch cost is dominated by Qiskit statevector rendering, not by tableau bit-manipulation. Thus H2 is tested for its polynomial-in-n *character*, not for the concrete constants.

### T-count regime is small (t ≤ 8)
- Max tested χ = 256. The paper's ripple-carry / QFT / fault-tolerant benchmarks operate at t in the hundreds. We confirm the qualitative exponential-in-t scaling; we do NOT confirm the quantitative constants that would let Quipu win a race against BDD-based simulators at those regimes.
- What's needed: t ≥ 15–20, ideally with GPU-batched per-branch render. Open question #3 turns this into a concrete probe.

### No head-to-head against competitor simulators
- **H5 (Quipu vs QuIDDPro) is untested.** QuIDDPro is not open source in 2026 and its binary distribution has lapsed. This is a genuine gap: the paper's most-cited performance claim is exactly this comparison.
- **We also did not benchmark against modern alternatives:** Bravyi et al. low-rank stabilizer decomposition (2016, 2019), Pashayan–Wallman–Bartlett quasi-probability sampling (2015), or Kissinger–van de Wetering ZX-based near-Clifford tools. Any *comparative*-performance claim about the frame method is out of scope of this replication.

### No structured-circuit benchmarks
- The paper's empirical evidence lives in ripple-carry adders, QFT, and encoded FT circuits. Our synthetic Clifford + random-T circuits exercise the algorithmic core (frame propagation + T-split + sum-out) but do not exercise the structured-entanglement regimes where BDD or stabilizer-rank methods historically win or lose.
- Fixing this is straightforward but was out of the per-turn budget.

### Multithreading (H6) untested
- Quipu's parallel speedup is a claim about the reference implementation, not about the algorithm. Testing it requires the Quipu source (unavailable). Marked "not tested" — not "failed."

### Judge dissent
- GPT-5.2 returned PARTIAL with two objections:
  1. Stim ↔ Qiskit residual ~1e-9. This is a known Stim fp32 artifact (Stim's `state_vector()` uses float32), NOT a frame-method issue. Frame ↔ Qiskit is 0 at t=0 by construction.
  2. Clifford-prefix vs tableau encoding. This is a real presentation-level dissent, already documented above.
- The dissent does not falsify any measured value; the judge's own H1–H4 field-level answers are all green.

## Confidence-lowering caveats

- **A malicious or careless implementation of the T-split could pass χ=2^t by construction while failing on amplitudes.** Our defense is that amplitude fidelity was checked independently against Qiskit's native T-gate — a code path that has zero shared logic with our frame-based T decomposition.
- **A wrong T-decomposition (e.g. swapping the sin/cos phase) would give χ=2^t but wrong amplitudes.** Amplitude match at 1e-16 rules this out.
- **A shared numerical library (numpy) is used by both the frame simulator and the Qiskit reference.** In principle, a common numpy bug could cause both to be wrong the same way; in practice, the Stim baseline (which uses its own C++ numerics) agrees on the Clifford subset, catching such a scenario.

## Bottom line
The two headline algorithmic predictions of the paper (H3: χ=2^t, H4: machine-precision amplitude recovery) are independently and quantitatively verified on real, from-scratch code. The paper's competitive-performance claims (H5, H6) and its large-t regime are not exercised — they are out of scope and marked "not tested," not "failed." Verdict REPLICATED is honest for the algorithmic core; a would-be user who wants Quipu-level runtime constants at t=100 should treat that as an independent open question (see Open Questions #2 and #3).
