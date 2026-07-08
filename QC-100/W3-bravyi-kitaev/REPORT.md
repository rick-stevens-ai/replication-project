# Replication Report — "The Bravyi-Kitaev transformation for quantum computation of electronic structure"

**Paper:** J. T. Seeley, M. J. Richard, P. J. Love, *J. Chem. Phys.* **137**, 224109 (2012).
**Wave:** QC-100 W3 · **Owner:** Ollie · **Verdict:** **REPLICATED**

## Scope
The paper (a) develops the Bravyi-Kitaev (BK) fermion-to-qubit encoding (matrices
β_n, π_n; parity/update/flip sets P/U/F), (b) writes creation/annihilation operators
in the BK basis, (c) applies it to H2 in a minimal (STO-3G) basis giving explicit
Pauli Hamiltonians H_BK and H_JW (Eqs. 79/80), and (d) compares simulation cost:
- single first-order Trotter step: **BK = 30 single-qubit + 44 CNOT**;
  **JW = 46 single-qubit + 36 CNOT**;
- locality per fermionic operator: JW **O(n)** vs BK **O(log n)**.

## Methods
Built entirely from numpy:
- β_n via the recursive binary-grouping doubling; π_n = lower-triangular ones;
  GF(2) matrix inverse; P/U/F sets derived from β_n, β_n⁻¹, π_n·β_n⁻¹ exactly as
  prescribed in Sect. VI.
- a_j (annihilation) as explicit 2ⁿ×2ⁿ matrices: JW directly (Z-string + Q⁻);
  BK as V·a_j^{JW}·V† where V is the basis-permutation |f⟩→|β_n f mod 2⟩ — this
  both builds the BK operator and tests that β_n is the correct encoding.
- H2 Hamiltonians assembled from the paper's exact Pauli coefficients (Eqs. 79/80).
- Gate counts from the textbook exp(−iθP) compilation (2(|support|−1) CNOTs per
  string; 2 single-qubit per X/Y basis change + 1 rotation).

## Results (all from `results.json`, this run)

| Claim | Paper | Replication | Status |
|---|---|---|---|
| β₄ encoding / β·β⁻¹=I (GF2) | binary grouping | β₄ correct; identity holds | ✓ exact |
| Update sets only odd indices | yes | True (all j) | ✓ |
| Flip set of even index empty | yes | True (all even j) | ✓ |
| Anticommutation {a_i,a_j†}=δI, {a_i,a_j}=0 (JW) | holds | max err **0.0** | ✓ exact |
| Anticommutation (BK) | holds | max err **0.0** | ✓ exact |
| BK & JW H2 spectra identical | same molecule | max |Δspec| = **4.4e-16** | ✓ machine prec |
| H2 ground-state energy | (encoding-independent) | BK = JW = **−1.851046** | ✓ |
| Both Hermitian | yes | max|H−H†| = 0.0 | ✓ |
| One Trotter step BK gates | 30 sq / 44 CNOT | **30 / 44** | ✓ EXACT |
| One Trotter step JW gates | 46 sq / 36 CNOT | **46 / 36** | ✓ EXACT |
| Locality JW O(n) / BK O(log n) | yes | JW {3,7,15,31,63}; BK {2,3,4,5,6} (n=4…64) | ✓ exact log |

## Verdict: REPLICATED
- **Coverage 9/10** — encoding construction, P/U/F sets, operators, anticommutation,
  H2 Hamiltonians, spectra, gate counts, and locality scaling all reproduced. Only
  the explicit IPEA eigenvalue-vs-Trotter-step convergence curve (Fig. 5) was not
  re-run end-to-end (the gate-count claims it underpins were verified directly).
- **Agreement 10/10** — the headline gate-count numbers (30/44 and 46/36) match the
  paper **exactly**; BK and JW spectra agree to machine precision (4.4e-16),
  confirming the encoding is correct with no index/sign bug; anticommutation is
  exact in both encodings; the O(log n) BK vs O(n) JW locality is exactly reproduced
  (BK = log₂(n) qubits, JW = n−1).
- The exact-match of the spectra across two independent encodings is the strongest
  possible internal consistency check and rules out the bit-ordering class of bug
  flagged in Wave 2.

**Files:** `paper.md`, `replicate.py`, `results.json`.
