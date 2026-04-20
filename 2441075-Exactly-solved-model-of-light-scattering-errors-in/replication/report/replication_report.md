# Replication Report: OSTI 2441075
## "Exactly-Solved Model of Light-Scattering Errors in Quantum Simulations with Metastable Trapped-Ion Qubits"

### Paper Reference
- **Authors:** Foss-Feig, Vikas, et al.
- **OSTI ID:** 2441075
- **System:** ⁴⁰Ca⁺ metastable optical qubits in Penning trap

---

## 1. Summary of What Was Replicated

### 1.1 Core Model
- **Lindblad master equation** for photon scattering in metastable trapped-ion qubits (²D₅/₂ manifold)
- **Three-level system**: |0⟩ = |D₅/₂, mJ=-3/2⟩, |1⟩ = |D₅/₂, mJ=-5/2⟩, |g⟩ = ²S₁/₂
- **Five jump operators**: elastic (σᶻ), Raman (|0⟩→|1⟩, |1⟩→|0⟩), leakage (|0⟩→|g⟩, |1⟩→|g⟩)
- **Selection rule**: Under π polarization, |1⟩ = |mJ=-5/2⟩ is dark (no scattering), so Γ⁽¹→⁰⁾ = Γ⁽¹→ᵍ⁾ = 0

### 1.2 Exact Analytic Solution (Eqs. 6-10)
Implemented the full m-body correlation function:

⟨∏ⱼ∈M σⱼ^νⱼ⟩ = (e^{-mΓt}/2^m) · ∏ᵢ∉M [I + R + L + B](Jᵢ^{(M,ν)}, t)

with all four components:
- **I**: Ideal Ising evolution (Eq. 7)
- **R**: Raman scattering trajectories (Eq. 8)  
- **L**: Leakage trajectories (Eq. 9) — **new contribution from this paper**
- **B**: Combined Raman+leakage trajectories (Eq. 10) — **new contribution**

### 1.3 Scattering Rates (⁴⁰Ca⁺)
Branching ratios from |0⟩ under π polarization:
| Channel | Fraction |
|---------|----------|
| Leakage (→|g⟩) | 94.5% |
| Raman (→|1⟩) | 3.9% |
| Elastic (→|0⟩) | 1.6% |

### 1.4 Figures Reproduced
- **Figure 1**: Energy level diagrams (schematic)
- **Figure 2**: GHZ state fidelity vs N for B=0.9T and B=4.5T
- **Figure 3**: Correlation functions and leakage probability vs N
- **Figure 4**: Spin squeezing parameter ξ²_R vs N

---

## 2. Validation Results

### 2.1 Analytic vs Numerical Agreement

| Test Case | 1-body error | 2-body error |
|-----------|-------------|-------------|
| N=2, J=5, Γ=2 | 2.7×10⁻¹¹ | 5.2×10⁻¹⁴ |
| N=2, J=2, Γ=5 | 7.9×10⁻¹³ | 5.7×10⁻¹³ |
| N=3, J=3, Γ=1.5 | 1.5×10⁻¹¹ | 1.2×10⁻¹¹ |
| N=3, J=1, Γ=3 | 6.0×10⁻¹³ | 7.4×10⁻¹³ |

**All agree to better than 10⁻¹⁰** — effectively machine precision for the ODE solver tolerance used.

### 2.2 Numerical Solution Properties
- **Trace preservation**: max error 5.5×10⁻¹⁶ (machine epsilon)
- **Positivity**: min eigenvalue -6.2×10⁻¹⁸ (machine epsilon)
- **Convergence**: Error scales linearly with ODE tolerance (rtol=1e-6 → 2e-8 error, rtol=1e-10 → 2e-12)

### 2.3 Component Function Tests
- I(J, 0) = 1, R(J, 0) = L(J, 0) = B(J, 0) = 0 ✓
- No-leakage limit: L = B = 0 ✓
- Permutation-invariant formula matches general formula for uniform coupling ✓
- Scattering rate scaling: linear in Γ for small Γ ✓

---

## 3. What Matched

### 3.1 Perfect Matches
1. **Analytic solution structure** (Eqs. 6-10): Implemented exactly as in the paper with all four terms I, R, L, B
2. **Analytic-numerical agreement**: Machine precision match for all tested N (2, 3) and parameter regimes
3. **Jump operator convention**: Paper uses D(ρ) = 2ΣJ ρ J†, which maps to standard Lindblad via L_k = √2·J_k
4. **Branching ratios**: 94.5% leakage, 3.9% Raman, 1.6% elastic (from Ref. [18])
5. **Selection rules**: |1⟩ dark under π polarization ✓
6. **Initial conditions**: Correct 1/2^m scaling at t=0 for all m-body correlations

### 3.2 Qualitative Matches in Figures
1. **Figure 2 (GHZ fidelity)**: 
   - Fidelity decreases with N ✓
   - Smaller δ (longer gate time) → lower fidelity ✓
   - Higher B field allows more ions ✓
   - Postselection significantly improves fidelity ✓

2. **Figure 3 (Correlations)**:
   - m-body correlations decay faster than exp(-mΓt) ✓ (key paper result)
   - Perpendicular correlations grow from zero ✓ (leakage-induced rotation)
   - Higher-body correlations decay faster ✓
   - Leakage probability approaches 1 for large N ✓

3. **Figure 4 (Squeezing)**:
   - ξ²_R scales as ~N⁻²/³ ideally ✓
   - Scattering adds a floor that limits achievable squeezing ✓

---

## 4. What Didn't Match / Limitations

### 4.1 Quantitative Figure Matching
The paper's figures use **Penning trap mode structure** computed from "zero-temperature simulations of equilibrium ion-crystal configurations" (Ref. [20]), which requires:
- 2D triangular lattice ion positions in a Penning trap
- Full 3D normal mode structure including planar and axial modes
- Specific trap frequencies (ωz, ωr) and magnetic field configuration

We used a **1D chain approximation** for the coupling matrix, which gives qualitatively correct but quantitatively different Jij values. This affects:
- The exact N at which fidelity drops below thresholds in Figure 2
- The coupling variance σ²(Jij) which determines F_unequal

### 4.2 Missing Information
1. **Laser power and beam waist** (P, w₀): Not specified in paper, needed for absolute scattering rates
2. **Trap frequencies** (ωz, ωr): Referenced to Ref. [20] without explicit values
3. **Total scattering rate**: Paper states "< 11 s⁻¹" but doesn't give exact value for each figure
4. **Penning trap mode calculation code**: Would need full 2D crystal simulation

### 4.3 GHZ Fidelity Computation
The GHZ fidelity involves computing ⟨ψ_GHZ|ρ|ψ_GHZ⟩, which requires the full density matrix. For the permutation-invariant case, this reduces to specific correlation functions, but the paper uses a product approximation F ≈ F_unequal × F_scatter that involves fourth-order corrections in δJij. Our implementation captures the dominant physics but may differ in the correction terms.

---

## 5. Code Structure

```
src/
├── __init__.py
├── scattering_rates.py    # Ba+/Ca+ atomic data, branching ratios
├── analytic_solution.py   # Exact solution (Eqs. 6-10)
├── numerical_solution.py  # Full Lindblad ODE integration
├── penning_trap.py        # Coupling matrix computation
└── figures.py             # All figure generation

tests/
├── test_analytic_vs_numerical.py  # Core validation
└── test_convergence.py            # Parameter studies

figures/                           # Generated PNG figures
report/
└── replication_report.md          # This report
```

---

## 6. Key Insights from Replication

1. **The exact solution is genuinely exact**: The quantum trajectory decomposition yields a closed-form expression that agrees with numerical Lindblad integration to machine precision.

2. **Leakage dominates**: For Ca⁺ with π polarization, 94.5% of scattering events cause leakage to |g⟩. The L and B terms (new contributions from this paper) are the most important corrections.

3. **Jump operator normalization matters**: The paper's convention with D(ρ) = 2ΣJρJ† (factor of 2) must be carefully translated to standard Lindblad form.

4. **Permutation invariance is powerful**: For uniform coupling (near COM mode), the N-ion problem factorizes into independent single-ion contributions, enabling computation for N > 300.

5. **Postselection is highly effective**: Since scattering from |1⟩ is forbidden, the residual error after removing leakage events is dominated by elastic and Raman processes, which are only 5.5% of total scattering.

---

## 7. Reproducibility Assessment

| Criterion | Status |
|-----------|--------|
| Analytic solution implemented | ✅ Complete |
| Numerical validation | ✅ Machine precision |
| Scattering rates from atomic data | ✅ Branching ratios match |
| Figure 1 (energy levels) | ✅ Schematic reproduced |
| Figure 2 (GHZ fidelity) | ⚠️ Qualitative match; quantitative requires Penning trap simulation |
| Figure 3 (correlations) | ⚠️ Qualitative match; exact values depend on trap parameters |
| Figure 4 (squeezing) | ⚠️ Qualitative match; scaling behavior correct |
| Test suite | ✅ All tests pass |
| Convergence studies | ✅ Complete |

**Overall**: The core theoretical result (exact analytic solution, Eqs. 6-10) is **fully replicated and validated**. The application figures require Penning trap-specific parameters that are not fully specified in the paper.
