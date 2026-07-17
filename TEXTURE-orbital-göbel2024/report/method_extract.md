# Method Extraction — göbel2024

**Paper:** Topological orbital Hall effect caused by skyrmions and antiferromagnetic skyrmions (Göbel, Schimpf, Mertig, arXiv:2410.00820)
**Texture class:** orbital (topological OHE from real-space skyrmion textures)
**Extraction source:** extraction/marker.md (pdftotext fallback — clean; Methods section with all equations present)

## 1. Central Claims

| ID | Claim | Testable? | Replicable-with-our-compute? |
|----|-------|-----------|------------------------------|
| C1 | Skyrmion crystals produce a **topological orbital Hall effect** (finite σ^{Lz}_xy) even for s electrons without SOC, on top of topological Hall + topological spin Hall. | yes | **yes** (TB + Berry curvature) |
| C2 | Orbital Hall conductivity ≫ spin Hall conductivity; σ^{Lz}_xy scales **quadratically** with skyrmion area while σ_xy and σ^{Sz}_xy scale **linearly** (Fig S2). | yes | **yes** |
| C3 | Simplified transport theory: σ_xy ∝ ±n(E), σ^{Sz} ∝ n(E), σ^{Lz} ∝ [n(E)]²/n'(E) from the zero-field square-lattice DOS (Fig 3). | yes | **yes** |
| C4 | **Antiferromagnetic** skyrmions / bimerons: compensated topological (charge) Hall effect but finite orbital (and spin) Hall — AFM bimeron gives a **pure** orbital Hall effect. | yes | **yes** |
| C5 | Edge states in slab geometry are orbital-polarized (skipping orbits) → bulk-boundary correspondence for OHE. | yes | **yes** (slab TB) |

## 2. Method Class
**Model-Hamiltonian tight-binding + Berry-curvature (Kubo) transport.** s-d model on a square lattice with a real-space skyrmion texture; observables from Berry/orbital-Berry/spin-Berry curvature integrated over the magnetic BZ. No DFT.

## 3. Computational Recipe
- **Hamiltonian (Eq.1):** H = t Σ_⟨ij⟩ c†_i c_j + m Σ_i m_i·(c†_i σ c_i). Single s orbital/site, square lattice a=2.76 Å, nearest-neighbor hopping **t=−1 eV**, Hund coupling **m=5|t|=5 eV** (also m=1 eV weak-coupling, m=900 eV adiabatic limit).
- **Skyrmion texture (Eq.2):** m(r) = [x sin(2πr/λ)/r, y sin(2πr/λ)/r, cos(2πr/λ)] for r<λ/2, else −e_z. Skyrmion sizes **λ = 5a, 8a, 10a**. Magnetic unit cell (λ/a)×(λ/a). Topological charge N_Sk via Eq.(3).
- **AFM skyrmion:** reverse every 2nd moment (checkerboard); use 2nd-neighbor hopping t2=−1 eV (or t1/t2 variants).
- **Observables (Methods Eqs.4-11):**
  - Spin S_z,ν(k) = (ħ/2)⟨νk|σ_z|νk⟩.
  - Orbital moment via modern formula Eq.(5) (off-diagonal, corrected imaginary unit).
  - Hall conductivity Eq.(6) from Berry curvature Eq.(7).
  - Orbital/spin Hall conductivities Eqs.(8,9) from orbital/spin Berry curvatures Eqs.(10,11), with orbital current operator j^{Lz}_x = (1/2){v_x, L_z}.
- **Codes/packages:** none named ("code available on request"; data at DOI:10.5281/zenodo.13919926). Reproduce with numpy/scipy or Kwant/PythTB. Berry curvature via Fukui-Hatsugai or direct Kubo sum.
- **Key parameters:** t=−1 eV, m=5 eV, λ∈{5a,8a,10a}, a=2.76 Å, disorder onsite ±0.2 eV (robustness check), t̃=cos(θ_ij/2)t≈0.9775t for DOS approximation.

## 4. Replication Feasibility
- **Tractable in hours.** The main cost is diagonalizing the s-d Hamiltonian on a magnetic supercell of (λ/a)² sites for each k in the magnetic BZ, then Kubo/Berry-curvature sums. For λ=10a that is a 100-site cell × k-mesh — modest dense linear algebra, easily CPU-parallelized. Slab (10 skyrmions) is a 10·(λ/a)² strip — still small.
- No data download needed (texture is analytic). Zenodo data available for cross-check. The modern-orbital-moment formula (Eq.5) is the error-prone piece.
- Quadratic-vs-linear area scaling (C2) requires a small sweep over λ — cheap.

## 5. Compute Recommendation
- **Host: nuc13 (CPU)** for the model + Berry-curvature sums (embarrassingly parallel over k). Optionally uicgpu if a GPU-accelerated dense-eigensolver is wanted for the λ=10a slab sweeps, but not necessary.
- Rough ask: 1 node, 8–32 cores, a few hours (bulk + slab + λ sweep + AFM variants).

## Notes / flags
marker.md is clean and, unusually, contains the **full Methods section with all transport equations** (Eqs.1-11) — this is the most self-contained recipe in the set. Zenodo data (DOI 10.5281/zenodo.13919926) exists for validation. Nougat pass unnecessary.
