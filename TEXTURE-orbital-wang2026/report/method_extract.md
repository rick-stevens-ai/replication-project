# Method Extraction — wang2026

**Paper:** Magnetic Order in bilayer Ruddlesden-Popper Nickelates (Wang, Duan, Liao, Lin, Yu, Si, arXiv:2607.15228)
**Texture class:** orbital (orbital-selective correlations → magnetic order in La3Ni2O7)
**Extraction source:** extraction/marker.md (pdftotext fallback — clean; main text + full Supplemental Material equations present)

## 1. Central Claims

| ID | Claim | Testable? | Replicable-with-our-compute? |
|----|-------|-----------|------------------------------|
| C1 | Bilayer two-orbital (e_g: d_x²−y², d_z²) Hubbard model for La3Ni2O7 at filling N=3 sits in a bad-metal / orbital-selective-Mott-proximate regime; d_z² → incoherent local moment, d_x²−y² → coherent itinerant. | yes | **yes** (slave-spin mean field) |
| C2 | Effective spin model = superexchange (J^s ∼ 4(1−Z_z)²t²/U) + RKKY (J^r(q) = −j_xz²(q)χ(q)) among d_z² local moments mediated by d_x²−y² carriers. Eq.(3), SM Eqs.(S1-S14). | yes | **yes** (susceptibility + RKKY) |
| C3 | AFM ground state with ordering wavevector Q ≈ (π/2, π/2); at U=0 q≈0.56π, shifting with U (Fig 3); interlayer antiparallel stacking. Consistent with neutron/RIXS. | yes | **yes** (Luttinger-Tisza + variational) |
| C4 | 3rd-neighbor RKKY J3 dominates J1 (J3/J1>1, peak near U~4 eV); leads to frustration driving incommensurate Q. | yes | **yes** |
| C5 | Spin-wave spectrum: acoustic + optical branches, bandwidth ~80 meV, acoustic softening at Q≈(π/2,π/2); params J⊥S=75, J1S=1.9, J3S=4.6, J1'S=1.38 meV. Matches RIXS/INS. | yes | **yes** (linear spin-wave theory) |

## 2. Method Class
**Multi-orbital Hubbard model + slave-spin mean-field (orbital-selective renormalization) + RKKY/superexchange derivation + Luttinger-Tisza / variational classical minimization + linear spin-wave theory.** This is strongly-correlated model condensed-matter theory (NOT DFT+DMFT directly, though hopping/crystal-field taken from a DFT-derived TB in Ref [49]). No cold-atom, no OHE Kubo.

## 3. Computational Recipe
- **TB input (SM Eq.S1):** bilayer two-orbital tight-binding H_TB with hoppings t^{αβ}_{il,jl'} and crystal-field ε_α taken from **Ref [49] (Liao et al. PRB 114, 045112)** — the DFT-derived e_g bilayer parametrization. Interlayer t⊥ ~ 0.6 eV.
- **Interaction (Eq.2):** Hubbard-Kanamori U, U'=U−2J_H, Hund J_H; U swept 0–6 eV, physical U~4 eV.
- **Slave-spin mean field (SM Eq.S2-S4):** solve two-orbital Hubbard via slave-spin (Yu-Si refs [66,67]) → orbital quasiparticle weights Z_α(U), shifts λ_α(U); build renormalized quasiparticle Hamiltonian H_eff with hoppings t̃=√(Z_αZ_β)t.
- **Susceptibility (SM Eq.S5-S8):** Lindhard-type χ_{ab;cd}(q;U) on an N_k×N_k mesh from H_eff eigenvectors; project onto d_x²−y² → χ_ll'(q); even/odd bilayer channels.
- **RKKY (SM Eq.S9-S11):** J^r_ll'(R) = −Σ_q e^{iq·R} (j_xz(q))² Re χ_ll'(q), with j_xz ≈ 1 eV (Hund-dominated). Superexchange J^s ∼ 4(1−Z_z)²t²/U.
- **Magnetic order (Eq.3 → J⊥-J1-J3 model):** Luttinger-Tisza (ref [71]) for candidate Q, then variational optimization (Sunny.jl-style, ref [72]) minimizing classical energy over propagation vector + spin orientation.
- **Spin waves:** linear spin-wave theory (Holstein-Primakoff) on the optimized order → acoustic/optical branches; intensity-weighted S(q,ω).
- **Codes/packages:** none explicitly named; slave-spin (custom, Yu-Si), Luttinger-Tisza (custom), variational + spin-wave likely **Sunny.jl** (ref [72] Dahlbom et al.) or SpinW. χ(q) is custom.
- **Key parameters:** U∈[0,6] eV (focus 4 eV), J_H, N_k×N_k mesh (dense for χ), t⊥~0.6 eV, j_xz~1 eV, exchange values in C5.

## 4. Replication Feasibility
- **Tractable in hours→~1 day on CPU.** No DFT SCF needed (hoppings imported from Ref [49]). Pipeline is: (1) slave-spin solve for Z_α(U) [small self-consistent mean field], (2) Lindhard χ(q) on a dense k-mesh [dominant cost, but modest — 2-orbital×2-layer = 4-band], (3) FT to real-space RKKY, (4) Luttinger-Tisza + variational classical minimization [cheap], (5) linear spin-wave [cheap]. All standard correlated-model techniques.
- Main friction: reproducing the Ref [49] slave-spin Z_α(U) and importing the exact DFT-derived TB hoppings (not tabulated in this paper — need Ref [49]/its SM). χ(q) k-mesh convergence near nesting (π/2,π/2) needs care.
- Spin-wave (C5) is directly reproducible given the stated J values (J⊥S=75, J1S=1.9, J3S=4.6, J1'S=1.38 meV) — one can even start there with Sunny.jl/SpinW to reproduce the ~80 meV bandwidth immediately.

## 5. Compute Recommendation
- **Host: nuc13 (CPU)** — slave-spin + Lindhard χ(q) dense-k (parallel over k), Luttinger-Tisza, spin-wave. Rough ask: 1 node, 8–32 cores, hours to ~1 day (U sweep is the multiplier).
- No GPU required; no SYCL. (χ(q) dense-mesh could use uicgpu if a very fine mesh/large U sweep is wanted, but CPU suffices.)
- **Recommended host: nuc13.**

## Notes / flags
- marker.md is clean and **includes the full Supplemental Material** (slave-spin renormalization Eqs.S1-S4, susceptibility S5-S8, RKKY S9-S14) — highly self-contained recipe. Only external dependency = Ref [49] DFT-derived hoppings + Z_α(U).
- Despite texture_class="orbital", the physics is orbital-*selective correlation*-driven magnetism (not an orbital-Hall/OAM-texture paper). Still on-theme (orbital degree of freedom central) but methodologically it's the odd one out (correlated-electron model, not Berry-curvature transport). Nougat pass unnecessary.
