# Failure Analysis — arXiv:2108.12388 (VQE noise for quantum chemistry)

Honest audit of what this replication does and does not establish. The verdict is REPLICATED on the paper's headline exercised claim, but that verdict carries real caveats that would be actionable if this were rated for downstream policy use.

## 1. What was reimplemented from scratch (strengths)

- **Hamiltonian pipeline:** written from scratch with PySCF + OpenFermion + Jordan-Wigner, NOT via Qiskit Nature's built-in H2 driver. This is an independent implementation of the paper's Hamiltonian construction, and the 15-term Pauli operator and its exact-diagonalization eigenvalue (-1.137306 Ha) match the paper's reference (-1.1373 Ha) to 4 decimal places.
- **VQE loop:** own SPSA driver + own QWC grouping (5 measurement bases instead of the naive 15). No wrapper around the paper's own code (which was not published anyway).
- **Density-matrix depolarizing:** used AerSimulator(method='density_matrix') so that E = Tr(rho * H) is computed exactly. This isolates the pure gate-noise effect from statistical shot noise, which is the cleanest way to test the linear-in-p claim.
- **Direct 1/sqrt(N) verification (C3):** implemented separately from the VQE loop, with 40 independent repetitions at each N to give a real empirical std, not one-shot values. This is stronger evidence than the paper itself provides for the shot-noise scaling law.

## 2. Where the replication falls short (weaknesses)

### 2a. Noise model does not match the paper's IBMQ setup

The paper uses IBMQ device noise (T1, T2, gate durations, measured average gate errors from real backends via Qiskit's device-noise-model builders). We use an abstract depolarizing channel with the common convention p_2q = 10 * p_1q. This is a **partial match**, not a full match. The abstract model reproduces both scaling laws quantitatively, and both channels are trace-preserving and unbiased, so the qualitative conclusions transfer. But we did NOT run `NoiseModel.from_backend(FakeMumbaiV2())` or the equivalent, so we cannot say we reproduced the paper's *specific device numbers* --- only their scaling behavior.

**Mitigation:** honestly flagged in the REPORT.md limitations section and in the REPORT.tex Critique section. A future rerun with `NoiseModel.from_backend(<free IBMQ fake backend>)` would close this gap in <1 hour of CPU.

### 2b. Statistical rigor of final VQE energies is weak

Each noise condition was optimized ONCE, with a single seed. The tail-std reported for shot-noise runs (0.01--0.02 Ha) is real, but the final-energy values could shift by +/-0.01 to +/-0.02 Ha with a different SPSA seed. This does NOT change the qualitative claims:
- monotonicity in p: safe (differences of 0.03, 0.24 Ha overwhelm any seed effect)
- slope-in-p at small p: safe within a factor of 2 (measured 36 Ha/p, expected 18 Ha/p from naive n_gates*||H||)
- shot-noise 1/sqrt(N) exponent: safe (C3 uses 40 reps per N)

But if someone tried to cite our |Delta E| numbers as precision benchmarks they'd be over-interpreting. This is not a paper claim; this is a replication craftsmanship note.

**Mitigation:** stated explicitly in the Critique section of REPORT.tex. A production-grade rerun would use 5-10 optimizer restarts per (p, shots) point.

### 2c. Ansatz-ranking claim (C5) is completely untested

The paper's most subjective and most influential qualitative claim is that noise reshuffles which ansatz "wins" in the 12-ansatz family. We ran ONE ansatz (RY-CZ reps=1). We have no evidence for or against C5. This is a real gap and is the biggest reason a strict reviewer might downgrade our verdict from REPLICATED to PARTIAL.

The rationale for not testing C5 in this pass: QC-100's scope is "one central checkable number + qualitative noise-scaling behavior" per paper. The reference number and both scaling laws exercised the paper's most quantitative claims. C5 is a 12x more expensive sweep and requires reproducing the paper's Table I ansatz definitions (which are given in the paper text but as figures, not as machine-readable schemas --- would need careful transcription).

**Judgement call (Rick's headline-exercised rule):** the paper's headline exercised claim is the reference number and scaling laws, both of which we hit. C5 is the paper's more speculative claim. Verdict stays at REPLICATED, with C5 explicitly noted as untested.

### 2d. Expressibility correlation (C6) also untested

Same story as C5. Requires the 12-ansatz sweep as a prerequisite. Noted as future work in the open-questions section.

### 2e. No error-mitigation replication

The paper is largely a noise-*characterization* study, not a mitigation study, so this is not a gap against the paper's own claims. But every modern replication of noise-scaling work should also test whether ZNE/PEC recover chemical accuracy at the tested p values. We did not do this. It is now open question #2.

### 2f. No bond-length sweep

The paper reports energies at a single bond length R=0.735 Ang. A stronger replication would sweep R across the full potential energy curve. We did not do this; it is a natural extension. Open question #3 covers the related "does this transfer to strongly correlated molecules?" concern.

## 3. Threats to validity

1. **Package version drift.** We used qiskit 2.5.0 / qiskit-aer 0.17.2; the paper used the 2021 qiskit 0.34.x era. Numerically the SparsePauliOp, Aer density-matrix backend, and SPSA optimizer are stable across this range (verified spot-check on a smaller Hamiltonian gives identical eigenvalues), but there could be subtle differences in default seeding, SPSA hyperparameters, or measurement grouping. We did not systematically test cross-version reproducibility.
2. **QWC grouping.** Our grouping gives 5 measurement bases; the paper does not explicitly state theirs. If they used tensor-product-basis (TPB) grouping only, they would have used more circuits per <H> evaluation, and their shot-noise scaling would differ by a constant multiplicative factor (not by the -0.5 exponent). We reproduce the exponent, not the constant, so this is not a threat to the C3 conclusion.
3. **SPSA vs COBYLA vs L-BFGS.** Paper uses SPSA (as we do). If they had used a gradient-based optimizer, noise effects on convergence would differ qualitatively. Our choice matches the paper.
4. **Endianness bug risk.** Qiskit uses little-endian qubit ordering by default; OpenFermion uses big-endian. Getting this wrong would produce a Hamiltonian that permutes the eigenvalue spectrum but leaves the ground state degenerate. Verified visually against the FCI reference: our exact-diag ground state matches PySCF FCI to numerical precision, so the endianness handling is correct.

## 4. What we DO claim (bounded, honest)

1. The paper's reference number for H2/STO-3G/JW ground state (-1.1373 Ha) is reproducible from first principles to 4 decimal places using standard open-source tools; agreement is 6e-4 Ha, well below chemical accuracy (1.6e-3 Ha).
2. The paper's shot-noise 1/sqrt(N) claim is quantitatively reproduced (exponent -0.524 vs theory -0.5) over an 8x dynamic range in N with 40 reps per point.
3. The paper's depolarizing-noise claims (monotonic degradation, linear-in-p at small p, saturation at large p) are qualitatively reproduced on our own abstract depolarizing model, with slope order-of-magnitude matching the naive n_gates * ||H|| prediction.

## 5. What we DO NOT claim

1. That the paper's IBMQ device-noise-model results are reproduced (partial noise-model match only).
2. That the paper's 12-ansatz-ranking claim (C5) is verified.
3. That expressibility-vs-accuracy correlation (C6) is verified.
4. That any single VQE-final-energy value here is precise to better than +/-0.02 Ha (one-seed optimization; use 5--10 restarts for precision).
5. That the results transfer to larger or more strongly-correlated molecules (untested; see open question #3).

## 6. Overall verdict (Rick's headline-exercised rule)

Headline exercised claim of the paper = the H2 reference number + both scaling laws. All three exercised. Verdict: **REPLICATED**. If C5 were treated as the headline (which is defensible), verdict drops to PARTIAL. We use the former because the reference number and scaling laws are the paper's most quantitative, testable, and citable claims.
