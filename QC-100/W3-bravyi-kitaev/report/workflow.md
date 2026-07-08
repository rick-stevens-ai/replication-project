# Workflow — QC-100 W3 Bravyi-Kitaev

## Paper
Seeley, Richard, Love, *J. Chem. Phys.* **137**, 224109 (2012) — "The Bravyi-Kitaev transformation for quantum computation of electronic structure." Extends and applies the original Bravyi & Kitaev 2002 fermion-to-qubit mapping to a full chemistry benchmark (H2 / STO-3G).

## Environment
- Language: Python 3, numpy only (no chemistry stack — Pauli coefficients taken from paper Eqs. 79/80).
- Host: m1 (paper.md + replicate.py + results.json produced there in the original W3 run).
- Free endpoints only for any follow-up questions; no re-simulation was performed in this backfill.

## Steps executed
1. Read paper (Sects. II–VI: BK encoding, matrices β_n, π_n; parity/update/flip sets; a_j in the BK basis; H2 Hamiltonians).
2. Implement β_n by recursive binary-grouping doubling; invert over GF(2); build π_n = lower-triangular ones matrix.
3. Derive P_j, U_j, F_j from β_n, β_n⁻¹, π_n β_n⁻¹ per Sect. VI. Assert:
   - update sets U_j non-empty only for odd j;
   - flip sets F_j empty for even j.
4. Build a_j^JW as 2^n × 2^n matrix directly (Z-string + Q⁻).
5. Build a_j^BK = V a_j^JW V†, V being the basis permutation |f⟩ → |β_n f mod 2⟩.
6. Verify {a_i, a_j†} = δ I and {a_i, a_j} = 0 in both encodings.
7. Assemble H2 Pauli Hamiltonians H_BK, H_JW using the paper's exact coefficients.
8. Diagonalise both; compare eigenvalues (must agree — encoding-independent physics).
9. Compile one first-order Trotter step per Pauli string via textbook rule (2(|supp|−1) CNOT, 2 sq per X/Y basis change, 1 rotation). Sum sq and CNOT across all strings.
10. Measure per-fermionic-operator Pauli weight (locality) for n ∈ {4, 8, 16, 32, 64} in both encodings.
11. Dump all measured numbers to `results.json`.

## Files produced (original W3 run, preserved)
- `paper.md` — reading notes / Pauli-coefficient tables.
- `replicate.py` — numpy-only reimplementation described above.
- `results.json` — every numerical claim in the report is a field here.
- `REPORT.md` — top-level replication report (original artifact — preserved).

## Files produced (this backfill, 2026-07-06)
- `report/REPORT.tex` — TeX version of the report with genuine critique section.
- `report/open_questions.json` — 5 open questions (bare list).
- `report/open_questions_section.tex` — TeX version of the same.
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — inventory of artifacts and what each proves.
- `report/failure_analysis.md` — honest critique of what was and was not exercised.
- `extraction/nougat.mmd` — extraction stub (no full nougat pass performed).

## What was NOT done (documented in failure_analysis.md)
- Chemistry-integral pipeline (PySCF/OpenFermion) was not re-run; Pauli coefficients were taken from the paper as given.
- IPEA eigenvalue-vs-Trotter-steps convergence curve (Fig. 5) was not re-run end-to-end.
- No compiler optimisation (string cancellation, commuting-set grouping) applied to the gate counts.
- Locality was checked numerically, not proven analytically for n > 64.
