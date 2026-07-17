# Method Extraction — wang2024

**Paper:** Topological Orbital Hall Effect (Wang, Hung, Lin, Li, He, Bansil, arXiv:2411.00315)
**Texture class:** orbital (topological OHE via feature-spectrum topology, group-IV monolayers)
**Extraction source:** extraction/marker.md (pdftotext fallback — clean; operators + Kubo formulas present)

## 1. Central Claims

| ID | Claim | Testable? | Replicable-with-our-compute? |
|----|-------|-----------|------------------------------|
| C1 | Feature spectrum ⟨P L̂z P⟩ of group-IV monolayer valence states splits into sectors (I: L_z=±1, II: L=0, III: L_z=0) whose Wannier charge centers show topological windings (winding ±2, ±1). | yes | **yes** (TB + WCC) |
| C2 | Orbital Hall conductivity σ^{Lz}_xy forms a **plateau within the band gap**, a consequence of the Chern number carried by the POAM spectrum (despite L_z U(1) being broken). | yes | **yes** (Kubo) |
| C3 | Spin Hall conductivity is near-quantized (−e/2π); slight deviation from U(1)-breaking SOC, explained by perturbation Eq.(4). | yes | **yes** |
| C4 | OHC k-space texture matches Berry curvature of the L̂z feature spectrum (Fukui-Hatsugai), concentrated near K/K' and Γ → topological origin. | yes | **yes** |
| C5 | Bulk-boundary correspondence: zigzag ribbon has orbital-polarized edge states; nonzero edge orbital texture (ARPES-verifiable); OAM sign reverses across Dirac points. | yes | **yes** (ribbon TB) |

## 2. Method Class
**Tight-binding model + feature-spectrum topology (projected-operator / Wannier charge centers) + Kubo linear-response Hall conductivity.** Representative material: germanene (largest SOC of group IV). No self-consistent DFT in main text — uses the Liu-Jiang-Yao TB model (ref [42]); "DFT" only implicitly via that parametrized TB. Wannier-charge-center machinery is the topological analysis.

## 3. Computational Recipe
- **TB model:** four-orbital (|s⟩,|p_x⟩,|p_y⟩,|p_z⟩) per site, honeycomb lattice with buckling, from Liu-Jiang-Yao PRB 84,195430 (ref [42]) — germanene parametrization (SOC gap increases with atomic mass/buckling). Basis includes spin ⊗ sublattice: H = h ⊗ τ ⊗ σ.
- **OAM operator (Eq.1):** ℓ̂_z = iħ [[0,0,0,0],[0,0,−1,0],[0,1,0,0],[0,0,0,0]] in (s,p_x,p_y,p_z); feature operator L̂_z = ℓ̂_z ⊗ τ0 ⊗ σ0.
- **Feature spectrum:** compute ⟨P Ô P⟩ (Ô = Ŝ_z or L̂_z), P = valence-band projector; partition into sectors; build feature-dressed Bloch states Φ_ik = φ_ik ψ_nk.
- **Topology:** Wannier charge center winding per sector (Yu-Qi-Bernevig-Fang-Dai method, ref [43]); Z2 for gapless sector III; Fukui-Hatsugai (ref [45]) for feature Berry curvature.
- **Hall conductivities (Eqs.2-3):** Kubo σ^{Ôη}_μν = (e/…)Σ_n∫d²k f_nk Ω^{Ôη}_μνn(k), with feature Berry curvature Eq.(3) using feature current operator j^{Oη}_μ = (Ô_η v_μ + v_μ Ô_η)/2, v_ν = ħ⁻¹∂H/∂k_ν.
- **Ribbon:** zigzag germanene ribbon for edge states; in-plane B field to gap edge for well-defined feature spectrum.
- **Codes/packages:** none named (custom TB + WannierTools-style WCC + Kubo). Reproduce with PythTB/Kwant + WannierTools or custom numpy. SM has the perturbation-theory details (Eq.4).
- **Key parameters:** germanene TB params from ref [42]; k-mesh dense enough for gap-plateau; chemical-potential sweep across gap.

## 4. Replication Feasibility
- **Tractable in hours on CPU.** Small 4-orbital × 2-spin × 2-sublattice (16-band) TB model; the work is (i) implementing the Liu-Jiang-Yao germanene TB, (ii) the feature-spectrum projection + WCC winding, (iii) Kubo OHC/SHC with the feature Berry curvature. No DFT SCF required (TB is parametrized). The feature-spectrum/WCC machinery is the novel, error-prone part but is well-described and standard tools exist (WannierTools).
- Ribbon edge-state calc is a small 1D-periodic slab — cheap.
- Self-contained in main text except SM perturbation derivation (Eq.4) which only affects the *explanation*, not the numbers.

## 5. Compute Recommendation
- **Host: nuc13 (CPU)** — PythTB/Kwant + custom Kubo/WCC. Dense-k sweeps embarrassingly parallel. Rough ask: 1 node, 8–16 cores, a few hours.
- No GPU/DFT needed. (If one wanted first-principles germanene bands to *regenerate* the TB params, that would add a small uicgpu DFT job, but the paper uses the published TB directly.)

## Notes / flags
marker.md clean; OAM operator matrix (Eq.1) and Kubo/feature-Berry formulas (Eqs.2-4) present and legible. Nougat pass unnecessary for method extraction. Main external dependency = the ref [42] germanene TB parameters (published, retrievable).
