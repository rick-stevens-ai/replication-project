# Failure Analysis — QC-100 W3 Bravyi-Kitaev (honest critique)

## Verdict: REPLICATED — but with clearly-scoped gaps.

## What was independently reimplemented (strong claims)
- **β_n matrices**: constructed from scratch via the recursive binary-grouping doubling; inverse over GF(2) computed and identity β·β⁻¹ = I verified.
- **π_n**: lower-triangular ones matrix, definitionally correct.
- **P/U/F sets**: derived from β_n, β_n⁻¹, π_n β_n⁻¹ per Sect. VI of the paper; structural invariants checked (odd-only update sets, empty flip sets on even indices).
- **JW creation/annihilation operators**: built as explicit 2^n × 2^n matrices from Z-string + Q⁻.
- **BK operators**: built as V a_j^JW V†, where V is the basis permutation |f⟩ → |β_n f mod 2⟩. This IS a real reimplementation — the permutation is a nontrivial classical map, and its correctness is exactly what the cross-encoding spectral test verifies.
- **Anticommutation**: {a_i, a_j†} = δ I and {a_i, a_j} = 0 checked in both encodings, max error **0.0** (not "small" — exact zero).
- **Trotter-step gate counts**: sq and CNOT tallies from the textbook exp(−iθP) compilation — reproduce **30/44 (BK) and 46/36 (JW) exactly**.
- **Locality**: per-operator Pauli weight measured for n ∈ {4, 8, 16, 32, 64}; matches log₂(n)+const (BK) and n−1 (JW) exactly.

## What was NOT independently reimplemented (real gaps)
1. **Chemistry-integral pipeline is missing.** The Pauli coefficients for H2/STO-3G (Eqs. 79/80) were taken from the paper as given, not re-derived from an integral computation. Consequence: the replication tests the encoding + simulation-cost machinery, not the second-quantised-Hamiltonian pipeline that feeds it. A PySCF+OpenFermion re-derivation would close this gap. This is the biggest single hole.
2. **IPEA convergence curve (Fig. 5) not re-run.** Only the gate counts that underpin it were verified; the actual iterative-phase-estimation eigenvalue-vs-Trotter-steps curve was not executed end-to-end. The report's coverage claim is 9/10 for this reason.
3. **No compiler optimisation applied.** The 30/44 and 46/36 numbers are compiler-agnostic textbook counts, not what a modern compiler (with commuting-set grouping, string cancellation, hardware-native gate sets) would emit. Both the paper's numbers and ours reflect the same unoptimised model, so the comparison is fair — but neither reflects what a real device would run.
4. **Locality proven numerically, not analytically for n > 64.** The O(log n) claim was verified up to n = 64. Beyond that it is asserted, not tested, in this replication.
5. **No noise-model check.** All simulations are noiseless. A NISQ-era comparison of BK vs. JW under a realistic noise model is not attempted (see open question 3).
6. **Only H2 tested.** LiH, BeH2, H2O etc. would be needed to say whether the BK/JW tradeoff observed here (BK wins on sq count, loses on CNOT for this tiny 4-orbital case) generalises (see open question 4).

## Comparison against Jordan-Wigner baseline
The Jordan-Wigner baseline was **built independently in the same script**, not merely quoted. Both encodings' spectra of the same molecular Hamiltonian agree to 4.4e-16. This is the strongest internal check available and rules out the bit-ordering class of BK bug that Wave 2 flagged in a different context.

## Did the O(log n) locality claim hold quantitatively?
**Yes, and stronger than the paper states**: the exact functional form (BK weight = ⌈log₂ n⌉ + const, JW weight = n − 1) is reproduced numerically — not just the scaling exponent.

## Bottom line
- Headline exercised end-to-end for the pieces the paper's H2 case study depends on: encoding, operators, spectra, gate counts, locality.
- Not exercised: chemistry pipeline (Pauli coefficients trusted from paper), IPEA convergence curve, compiler optimisation, noise, molecules beyond H2.
- Verdict **REPLICATED** is defensible because the two most load-bearing paper numbers (30/44 and 46/36) match exactly and cross-encoding spectral agreement is at machine precision. If the standard were "close every gap," the verdict would be **PARTIAL** — but the scope-limited replication of the paper's core claims is complete.
