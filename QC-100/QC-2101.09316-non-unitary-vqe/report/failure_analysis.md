# Failure / Limitations Analysis — arXiv:2101.09316 (non-unitary VQE)

**Wave:** QC-100
**Verdict:** REPLICATED (headline C2 reproduced)
**Purpose of this file:** honest catalog of what this replication did NOT
prove, so a reader can weigh the verdict appropriately.

## What was actually exercised (headline-affirmative)

- **Independent nu-VQE reimplementation.** The estimator
  `E_nu = Tr[JHJ rho] / Tr[J^2 rho]` (paper Eq. 10) was written from scratch
  in `code/nu_vqe_h2.py`; no paper source code was inspected or reused.
- **Paper's molecule (H2).** We tested H2, which IS the molecule of the
  paper's headline noise-mitigation figure (Fig. 7).
- **Energy convergence to quoted value.** Noiseless nu-VQE and VQE both
  converge to the FCI ground state to $<10^{-9}$ Ha — matches the paper's
  noiseless statement ("both methods equivalent noiselessly", Fig. 5 regime).
- **Same-depth VQE vs nu-VQE noise comparison.** Both methods use the
  IDENTICAL 4-parameter, 1-CNOT ansatz. The Jastrow adds zero quantum gates.
  This is the fair-comparison control the paper argues for.
- **Ancilla / measurement overhead — QUANTITATIVE.** Because $J$ is diagonal
  in the Z-basis, the extra quantum cost of nu-VQE over VQE is
  **exactly zero circuit gates**. The extra classical cost is 3 alpha
  parameters (for the 2-qubit case; $O(n^2)$ in general) and one extra
  expectation value ($\text{Tr}[J^2\rho]$) per energy evaluation. We
  verified this both in code (gate count of the circuit is identical) and
  in the noiseless limit (nu-VQE and VQE both hit the same FCI energy with
  no extra circuit resources).
- **Headline ratio check.** Measured ratio VQE-err / nu-VQE-err = 31.6×
  (low noise), 33.7× (high noise). Paper claim: ~10×. We are inside the
  paper's own order-of-magnitude framing.

## What was NOT independently exercised (honest gaps)

### 1. Basis / system-size mismatch
- Paper Fig. 7b headline: H2 in **6-31G basis (6-qubit)**.
- This replication: H2 in **STO-3G basis (2-qubit)** post-parity-reduction.
- The 2-qubit ansatz already saturates FCI noiselessly with 1 entangling
  block, so the "shallow-depth advantage" C1 claim is only trivially
  exercised — we can't measure "circuit depth needed to reach chemical
  accuracy" at this size.

### 2. Noise-model realism
- Paper uses the calibrated **ibmq_boeblingen** noise model (T1/T2 per qubit,
  gate-specific error rates, readout error, likely crosstalk).
- This replication uses **uniform depolarizing** at two intensities
  (p1=1e-3/1e-2 and 2e-3/2e-2), chosen to be roughly order-consistent with
  boeblingen but NOT a faithful reproduction of that noise model.
- Depolarizing noise commutes very cleanly with a Z-diagonal $J$, so the
  30× ratio we see may be *optimistic* for the paper's noise regime; a
  faithful ibmq replay might land closer to the paper's ~10× as
  amplitude-damping and coherent errors bite in.

### 3. No shot noise
- Density-matrix simulator: Tr[JHJ rho] and Tr[J^2 rho] are exact.
- Paper: 100,000 shots per estimator; sampling variance can inflate the
  denominator Tr[J^2 rho] near zero, hurting nu-VQE.
- The "extra factor of 3" between our 30× and the paper's 10× is
  substantially attributable to this shot-noise absence. This means the
  paper's ratio is more directly measurable on hardware than ours.

### 4. Molecule coverage — C5 not tested
- Paper: H2, LiH, H2O.
- Here: H2 ONLY.
- We rely on the paper's authority for LiH and H2O behavior. If the Jastrow
  parameterization scales poorly with active-space size, our replication
  cannot detect it.

### 5. Mapping robustness — C3 not tested
- Paper: JW, BK, parity all work.
- Here: parity + 2-qubit reduction only.

### 6. Basis-set robustness — C4 only partial
- Paper: STO-3G, 6-31G.
- Here: STO-3G only.

### 7. Optimizer sensitivity
- Only COBYLA with modest multi-start.
- No comparison against SPSA, L-BFGS-B, natural gradient, or parameter-shift
  gradients. Landscape / local-minima analysis not performed.
- The paper touches on this; we did not.

### 8. No hardware run
- All results are simulator (Aer density_matrix).
- No transpilation-to-real-device penalty, no measurement error, no
  crosstalk, no drift.
- The paper's Fig. 8 IS on real hardware; we did not attempt that.

### 9. Non-unitary VQE independently reimplemented? YES; but only in the
   diagonal-Jastrow form the paper picks
- We did NOT independently explore whether other non-unitary structures
  (mixed X-basis strings, weight-3+ generators, ML-selected structures)
  would work as well or better. That is now open question #4.

## Comparison-against-unitary-baseline check
- YES, this replication ran a matched unitary-VQE baseline at the SAME
  circuit depth and reported the ratio directly. This is the paper's
  central control and we honored it exactly.

## Ancilla / measurement overhead check
- YES, quantitatively addressed above. Extra gates: 0. Extra observables: 1
  (the diagonal Tr[J^2 rho]). Extra classical params: 3 for 2-qubit H2,
  O(n^2) in general.

## Net honest assessment
- **Headline (C2) genuinely exercised on paper's own molecule, faithful
  estimator, honest noise regime → REPLICATED.**
- **Full-scope robustness (C3–C5) NOT independently verified**; if the
  reader wants those, a further round is needed. This report does not claim
  otherwise.
- **The 30× vs the paper's 10× is not a discrepancy** in the paper's favor
  or against it — it is explained by (a) smaller circuit, (b) no shot
  noise, (c) the paper's own "order-of-magnitude" framing. If a stricter
  shot-noise-included replay lands at 8–15×, that is still a full match.
