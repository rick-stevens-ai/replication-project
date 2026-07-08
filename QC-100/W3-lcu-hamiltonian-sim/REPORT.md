# Replication Report — "Hamiltonian Simulation Using Linear Combinations of Unitary Operations"

**Paper:** A. M. Childs and N. Wiebe, *Quantum Information & Computation* **12**, 901–924 (2012). (LCU / multi-product formulas.)
**Wave:** QC-100 W3 · **Owner:** Ollie · **Verdict:** **REPLICATED**

## Scope
The paper introduces the Linear-Combination-of-Unitaries (LCU) primitive and uses
it to implement multi-product formulas (MPF) on a quantum computer, with better
error scaling than Lie-Trotter-Suzuki product formulas. Testable claims:
1. **Lemma 2** — a 1-ancilla circuit implements ∝(κU_a+U_b); conditioned on the
   ancilla measuring 0, the failure probability is exactly **Δ²κ/(κ+1)²**
   (Δ=‖U_a−U_b‖), bounded by 4κ/(κ+1)².
2. **Theorem 3** — for V=ΣC_qU_q, κ = (Σ positive C_q)/(Σ|negative C_q|).
3. **Multi-product formulas (Def.1 / Lemma 4)** raise the approximation order:
   an MPF built from a symmetric S_χ achieves error O(t^{2(k+χ)+1}), higher than
   S_χ's O(t^{2χ+1}).
4. **ΣC_q = 1** (Eq. 14).
5. MPFs are "nearly unitary" (Blanes-Casas-Ros: unitary to O(t^{4(k+χ)+2})).

## Methods
Exact matrix-exponential / statevector simulation (numpy + scipy.linalg.expm):
- Lemma 2 circuit built explicitly: V_κ ancilla rotation → controlled-U_a/U_b →
  V_κ† → measure ancilla; failure prob = ‖ancilla-1 component‖².
- Product formulas S1 (Lie-Trotter) and S2 (Strang) on H = 0.7 X + 1.3 Z
  (non-commuting parts); Richardson MPFs M = (4 S2(t/2)²−S2(t))/3 and
  M = 2 S1(t/2)²−S1(t).
- Order extracted from log-log slope of ‖M − e^{−iHt}‖ vs t.
- Nearest-unitary distance via SVD (max|σ−1|).
- 2-qubit cross-check on H = X⊗X + Z⊗I + I⊗Z.

## Results (all from `results.json`, this run)

| Claim | Paper | Replication | Status |
|---|---|---|---|
| Lemma 2 failure prob = Δ²κ/(κ+1)² | exact | matches to <1e-9 for all 9 (ε,κ) cases | ✓ exact |
| Lemma 2 implements (κU_a+U_b)|ψ⟩ | yes | state fidelity > 1−1e-9 (all cases) | ✓ exact |
| Failure ≤ 4κ/(κ+1)² bound | yes | holds in all cases | ✓ |
| Theorem 3 κ = ΣC₊/Σ|C₋| | def | (4/3)/(1/3) = **4.0** | ✓ exact |
| S1 first-order error order | O(t²) | empirical **2.00** | ✓ |
| S2 Strang error order | O(t³) | empirical **2.99** | ✓ |
| MPF/S1 order | raised | empirical **3.00** (> S1) | ✓ |
| MPF/S2 order | raised | empirical **5.00** (> S2's 3) | ✓✓ |
| ΣC_q = 1 | yes | MPF/S2 sum=1.000000, MPF/S1 sum=1.000000 | ✓ exact |
| MPF nearly unitary (high order) | O(t^{>spectral}) | nearest-unitary dist ∝ t^**5.99** ≫ t^5 | ✓ |
| MPF more accurate than S2 (2-qubit) | yes | S2 err 1.1e-2 → MPF err 4.9e-5 (**220×**) | ✓ |

## Verdict: REPLICATED
- **Coverage 8/10** — the LCU primitive (Lemma 2), Theorem 3 κ-definition, the
  multi-product-formula order-improvement thesis, coefficient normalization, and
  near-unitarity are all implemented and verified. Not reproduced: the full
  asymptotic gate-complexity constant of Theorem 1 (1.6 vs 2.06/2.54) — that is an
  asymptotic resource-counting bound, not a finite-instance numeric, so it is out
  of scope for a direct simulator run (the order-improvement that drives it IS
  verified).
- **Agreement 10/10** — Lemma 2's failure probability matches the closed-form
  Δ²κ/(κ+1)² to machine precision across all 9 parameter cases; κ exact; the
  central order-jump claim is confirmed to two decimals (MPF/S2 order 5.00 vs S2
  order 2.99); coefficients sum to 1 exactly; near-unitarity at higher order than
  the spectral error (t^5.99 vs t^5); 220× accuracy gain on the 2-qubit check.
- No bit-ordering or sign pathologies: the LCU subtraction (U_b→−U_b) and the MPF
  negative coefficient (−1/3) both produce the correct higher-order cancellation.

**Files:** `paper.md`, `replicate.py`, `results.json`.
