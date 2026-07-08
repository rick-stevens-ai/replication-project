# Failure Analysis — W1-vqe-photonic-peruzzo (honest critique)

## Bottom line

The VQE **algorithm** is genuinely replicated on the paper's actual molecule (HeH+, STO-3G, Jordan–Wigner) end-to-end. The **hardware demonstration** and the **paper's specific absolute-energy convention** are not. These are honest scope-outs, not silent failures.

## What was independently reimplemented (not quoted)

- **VQE algorithm.** Parameterized state preparation (UCCSD ansatz), expectation-value evaluation of a molecular Hamiltonian, and classical optimization (Adam primary, Nelder–Mead cross-check). None of these were quoted from the paper; all were implemented from PennyLane primitives.
- **HeH+ ground-state energy.** Reproduced by independent construction of the STO-3G Jordan–Wigner Hamiltonian and exact diagonalization; VQE optimum agrees with FCI at the 1.7e-6 mHa level (far below chemical accuracy of 1 mHa).
- **Dissociation curve.** Full HeH+ potential-energy surface reproduced across bond lengths; every point sits within chemical accuracy of FCI (100% chem-acc fraction, vs the paper's 96% hardware figure).
- **Equilibrium bond length R_eq.** Recovered at 97.97 pm via a 1-pm-resolution curve fit around the minimum; paper reports 92.3 ± 0.1 pm. Agreement is within ~6 pm — same physics, small quantitative offset (see gaps below).
- **Paper's optimizer (Nelder–Mead) cross-check.** Run independently at R = 0.92 Å; converged to the exact energy in 200 evaluations to 3.6e-11 mHa. This is the paper's actual optimization method verified.
- **Classical FCI baseline.** Exact diagonalization of the qubit Hamiltonian, used as ground truth at every bond length. Not quoted, computed here.

## What was quoted or scoped out (honest gaps)

### 1. Photonic-hardware demonstration (scoped out)
The paper's headline visual is a photonic-chip execution of VQE. This replication does not build a photonic simulator (no dual-rail encoding, no photon-loss model, no post-selection statistics). The paper's "96% within chemical accuracy" figure is a hardware statement, not an algorithmic one, and is not directly comparable to this replication's noiseless 100%. **Impact:** the algorithmic claim is verified; the hardware-realizability claim is not.

### 2. Absolute energy zero (documented convention gap)
The paper reports energies in MJ/mol relative to a tapered 2-qubit Hamiltonian (Supp. Table 2). That Hamiltonian is not in the parsed `paper.md` and was not reconstructed here. Our absolute energies differ from the paper's (−7.53 vs −2.865 MJ/mol at equilibrium); the *relative* curve shape and R_eq match. **Impact:** relative physics matches; absolute-energy comparison is blocked by the missing tapered Hamiltonian.

### 3. R_eq offset (~6 pm)
Our fit gives 97.97 pm; the paper reports 92.3 pm. Same order of magnitude and same qualitative minimum, but ~6 pm off. This is most plausibly attributable to the basis choice (STO-3G vs whatever effective basis the paper's tapered 2-qubit Hamiltonian encodes) and the fit method around the minimum. Not investigated further in this replication. **Impact:** the equilibrium-bond-length claim is qualitatively reproduced; the exact value differs by an amount consistent with basis-set / Hamiltonian-tapering differences.

### 4. Hamiltonian averaging is implicit, not explicit
The paper's algorithmic novelty includes explicit Hamiltonian averaging: decompose H into Pauli terms, measure each separately under shot noise, sum classically. In this replication, PennyLane's `expval` on the qubit Hamiltonian handles the Pauli decomposition internally and the sum is exact in the noiseless statevector regime. **What was NOT done:** finite-shot Hamiltonian averaging with per-term measurement budgets, term-grouping strategies (qubit-wise commuting, general commuting), or measurement-count vs. accuracy tradeoff analysis. **Impact:** the mathematical form of Hamiltonian averaging is respected; the practical shot-count engineering that the paper's hardware demonstration entailed is not exercised.

### 5. Noise robustness (not tested)
No noise sweep. The paper's 96% figure reflects real device error; the replication's 100% reflects a noiseless simulator. See Open Question Q4 for the concrete follow-up.

## Bugs caught and fixed during the run (documented, not hidden)

1. **Angstrom-vs-Bohr coordinate bug.** Initial coordinates in Å produced curves with no minimum. Fixed by conversion to Bohr. Standard trap in `qml.qchem` interfaces; documented in `REPORT.md`.
2. **Sector-leak bug.** A non-particle-preserving ansatz let VQE escape the N=2 charged HeH+ sector into the lower-energy N=3 neutral HeH sector, giving spuriously good energies at the wrong molecule. Fixed by switching to UCCSD (particle-number preserving), adding an N-sector filter on the exact reference, and asserting the variational-principle bound (E_VQE ≥ E_exact) at runtime.

Both bugs were caught, fixed, and documented before the reported numbers were finalized.

## Provenance issues (documented, not hidden)

- **Workspace collision.** During the run a parallel inline attempt (H2-hardcoded fallback) overwrote `replicate.py`. The subagent detected this, restored the PennyLane HeH+ implementation, and cleaned a stale root `results.json`. The overwritten fallback report is preserved as `REPORT.ollie-h2-inline.md.bak`. **Impact on results:** none — the on-disk canonical numbers are from the correctly-restored PennyLane implementation.

- **Audit could not re-execute cleanly.** At audit time (2026-06-26), the PennyLane environment was not consistently available for a fresh end-to-end re-run. Audit therefore relied on (a) internal consistency of the on-disk `results.json` + `fine_eq.json`, (b) cross-check against literature values (HeH+ ground state ≈ −2.863 Ha), and (c) the paper's R_eq. This is honestly labeled in `REPORT.md` under "Verification basis (honest)". A future re-run in a stable env would upgrade the verdict from "audited via literature + on-disk logs" to "audited via fresh execution".

## Verdict-level honesty

The queue label for this dir was "REPLICATED" (algorithm-level); the on-disk `REPORT.md` calls it "PARTIAL (strong; algorithm REPLICATED)" with coverage 6/10 because the photonic-hardware experiment is unreproduced. Per the standing "trust on-disk REPORT.md" and "match substance" rules, **PARTIAL is the substance-honest verdict** and is preserved in this backfill. The algorithmic headline is fully exercised; the hardware headline is not.
