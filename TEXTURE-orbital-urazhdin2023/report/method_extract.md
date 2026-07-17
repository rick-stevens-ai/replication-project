# Method Extraction — urazhdin2023

**Paper:** Symmetry constraints on the orbital transport in solids (Urazhdin, arXiv:2309.04442)
**Texture class:** orbital (atomic orbital-moment transport / crystal-field torque)
**Extraction source:** extraction/marker.md (pdftotext fallback — clean, fully readable)

## 1. Central Claims

| ID | Claim | Testable? | Replicable-with-our-compute? |
|----|-------|-----------|------------------------------|
| C1 | Continuity relation for orbital angular momentum acquires a **crystal-field torque** term Γ̂ = (i/ħ)[U,L̂] = r×F; conserved only under continuous rotational symmetry (Noether). | yes (analytic) | **yes** (pen-and-paper / symbolic) |
| C2 | In cubic t2g complex oxides (e.g. SrTiO3), orbitally-selective hopping conserves L component **along** the hopping/principal axis but quenches the **normal** component over ~1 lattice constant. TB Hamiltonian Eq.(6)-(8). | yes | **yes** (tiny TB model) |
| C3 | Non-stationary superposition of d_xz/d_yz Bloch states shows **oscillating** ⟨L̂z⟩ = σħ cos[t(ε2−ε1)/ħ] (not precession; ⟨L̂x⟩=⟨L̂y⟩=0). With V=0.2 eV, frequency 0→10¹⁴ Hz across BZ. | yes | **yes** (2-level time evolution) |
| C4 | Triangular 2D lattice (fcc{111}/hcp(0001)): Slater-Koster d-d hopping matrix elements from L_z=2ħ give V22=0.06V_ddσ, V20=−0.36V_ddσ, V2−2=0.73V_ddσ; hopping favors moment **reversal** (~150× more likely than conservation). | yes | **yes** (Slater-Koster algebra) |
| C5 | Orbital moment normal to hopping direction relaxes over a single lattice constant on fcc/hcp → limits OHE accumulation to a few atomic spacings from interfaces. | yes | **yes** (follows from C4) |

## 2. Method Class
**Analytic / model-Hamiltonian tight-binding.** No DFT, no heavy numerics. Slater-Koster two-center integrals, small tight-binding Hamiltonians, elementary quantum time evolution.

## 3. Computational Recipe
- **t2g cubic oxide model:** Ĥ = −V Σ (1−δ_l,m) c†_{n+l,m,s} c_{n,m,s} (orbital-selective hopping, Eq.6). Dispersion ε_m(k) = −2V Σ_{m'≠m} cos(k_{m'} a) (Eq.8). Superposition ψ = (1/√2)(c†_xz + iσ c†_yz)|0⟩; evaluate ⟨L̂z⟩, time evolution Eq.(10)-(11).
- **Triangular lattice:** Slater-Koster parameters V_ddσ, V_ddπ=−2V_ddσ/3, V_ddδ=V_ddσ/6 (Harrison ref [24]); compute V_{L_z L'_z} hopping matrix elements between neighbors; wavepacket dephasing Δt = ħ/(Δk v_g).
- **Codes/packages:** none named (author did it analytically). Reproduce with sympy/numpy (small matrices). Optional: PythTB or Kwant to build the TB models.
- **Key parameters:** V = 0.2 eV (t2g), a = lattice constant, L_z = ħ or 2ħ, Slater-Koster ratios above. No k-mesh/cutoff/U — it's analytic.

## 4. Replication Feasibility
- **Fully tractable in minutes to ~1 hour on a laptop/CPU.** Everything is closed-form or 2×3-orbital matrices. The "computation" is: build the two TB models, compute dispersions, diagonalize, evaluate ⟨L⟩ expectation values and time evolution, reproduce the Slater-Koster hopping-matrix numbers (V22, V20, V2−2) and the ~10¹⁴ Hz oscillation frequency estimate.
- No convergence issues, no data downloads, no GPU. This is the single easiest paper in the set.

## 5. Compute Recommendation
- **Host: nuc13 (CPU)** — trivial Python (numpy/sympy). Sub-core-hour. Could even run on cherryrd directly.
- Rough ask: 1 core, minutes.

## Notes / flags
marker.md clean and complete; all key equations and Slater-Koster numbers are present in the extracted text. No SM dependence for the core results. Nougat pass unnecessary.
