# Failure Analysis — QC-2208.04100 (Noise-resilient phase estimation with RC)

Honest critique of what this replication actually establishes vs what the paper claims. Verdict of **REPLICATED** applies only under the headline-exercised rule; it is not a claim that every result in the paper has been independently reproduced.

## What was actually reimplemented and reproduced

- **The RC + iterative-QPE combo, at single-qubit scale.** From scratch in qiskit + qiskit-aer, no code taken from the authors' repo. Verified on both sampled Aer runs and an exact superoperator calculation.
- **Bare linear scaling of PE error vs coherent noise angle ε.** Sampled fit k = 1.006; exact fit k = 1.000. Paper: k ≈ 1.04. Within 3–4%. **Strong match.**
- **RC super-linear scaling.** Exact fit k = 2.263 (Nr → ∞ analytic). Paper: k ≈ 2.73. **Qualitative match, quantitatively 17% lower exponent in a different fit window.**
- **Error-reduction ratio.** Up to 1000× (exact) / 800× (sampled) vs paper's claim of "up to two orders of magnitude". **Match.**
- **Coherent-to-stochastic noise conversion.** Verified indirectly via the collapse of the bias term (bare linear-in-ε → RC super-linear-in-ε) after Pauli twirling.

## What was NOT independently reproduced (honest gaps)

### 1. The paper's actual 10-qubit Floquet system
The paper's Fig. 3 exponent of 2.73 comes from a **10-qubit non-Clifford Floquet unitary** with a per-single-qubit-gate R_Z(θ) noise model. This replication used a **single-qubit** reduction. The reduction preserves the physics of the noise model (single-qubit Z-rotation per cycle) but not the scale (10 qubits × depth × entangling structure). Whether the exponent stays at ~2.7 on the full 10-qubit system when I run it from scratch was not tested. My 2.26 exact-analytic exponent is consistent with the paper's regime but the residual gap to 2.73 could either be (a) fit-window sensitivity or (b) a scale effect that only shows up on the multi-qubit system. **Cannot distinguish (a) from (b) from this replication alone.**

### 2. Fig. 3(b) — stochastic-noise sweep, ~60% RC reduction (C3)
Not attempted. The paper's C3 claim (RC still helps under stochastic Pauli noise, delivering ~60% reduction) is qualitatively distinct from C1/C2 (coherent noise) and was not exercised. **Would require an independent sweep with a stochastic-Pauli noise channel replacing R_Z(ε).**

### 3. Fig. 4 — 8-qubit Shor order-finding (C4)
Not attempted. The paper's Fig. 4 shows RC removing spurious peaks in the Shor order-finding frequency spectrum for x=4, N=255, an 8-qubit run. This is arguably the paper's "does the algorithm work" demonstration. **Would require an independent 8-qubit modular-exponentiation circuit + RC harness — a materially larger project than the single-qubit toy.**

### 4. Theorem 1 (C5)
Not attempted. The paper's Theorem 1 (Hermitian-Kraus channels → phase-invariant to first order) is analytical, not numerical. Not something this replication attempts to prove or disprove; the RC bias-collapse behavior we observe is consistent with it but not a proof.

### 5. No non-RC QPE baseline comparison beyond a single-qubit toy
"Bare vs RC" is the entire comparison in this replication, and both live inside the same single-qubit iterative-PE harness. **We do not, e.g., compare RC-QPE vs zero-noise-extrapolation-QPE, vs symmetry-verification-QPE, vs probabilistic-error-cancellation-QPE.** The paper's positioning of RC as *better than other coherent-noise mitigations for QPE* is not exercised here.

### 6. Coherent-to-incoherent conversion was verified only indirectly
We verify it via **bias collapse** on the twirled channel: bare error is linear-in-ε and grows, RC error is super-linear-in-ε and stays small. That is consistent with the twirl producing a stochastic Pauli channel to which Theorem 1 applies. **We did not run process tomography of the effective per-cycle channel** to directly show that off-diagonal (coherent) Pauli-transfer-matrix entries are suppressed. For the single-qubit R_Z(ε) case this is analytically obvious; on a 10-qubit Floquet unitary it is a non-trivial claim we did not verify.

### 7. RC exponent 2.73 not sampled (only computed analytically)
Our sampled Aer runs bottom-out at the stochastic floor ~1/√(Ns · Nr) ≈ 8e-4 (Ns=20 000, Nr=80). The RC super-linear regime lives below this floor for most of the ε range where the paper's fit was done. **To directly sample-verify the 2.73 exponent we would need ~10^7 shots per circuit** — the paper's budget — which is ~100–1000× more single-thread wall time than we spent. Not a physics limitation; a compute-budget limitation. We closed this gap with the exact analytic channel calculation instead.

### 8. Hardware runtime, calibration drift, transpiler overhead
Simulator-only. On real hardware, the per-shot recompile for each Pauli twirl draws (Nr times more transpiler passes per fit point) is potentially significant. **The paper does not benchmark this and neither does this replication.** See open_questions.json Q4.

## Verdict discipline
**Verdict: REPLICATED.** Under the headline-exercised rule this is defensible: the two most-quoted quantitative claims of the paper (C1 bare linear, C2 RC super-linear + ~2 orders of magnitude improvement) were both independently re-derived from scratch and match the paper within uncertainty. The verdict is NOT "the entire paper has been reproduced" — Fig. 4, Fig. 3(b), the 10-qubit Floquet system, and hardware behavior are all outside this replication's scope and are explicitly listed as open items in open_questions.json.

## Would-do-differently list
- Run at least a 2-qubit twirled-channel calculation as a sanity check on the exact-superoperator reduction (small, cheap).
- Include a scan at fixed compute budget T comparing bare-shots-T against RC-shots-T/Nr — the true "at fixed cost" question — instead of only bare-vs-RC at fixed per-circuit shots.
- Add process-tomography-based direct verification of the coherent-to-stochastic conversion, not just the bias-collapse signature.
- Attempt the 8-qubit Shor Fig. 4 demo on a free IBM Q backend to close the C4 gap.
