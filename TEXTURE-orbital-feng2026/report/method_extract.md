# Method Extraction — feng2026

**Paper:** Nonperturbative Magnetic Orbital Hall Effect in Altermagnets (Feng, Cao, Ang, Yang, Xiao, Xie, arXiv:2602.19076)
**Texture class:** orbital (magnetic orbital Hall effect, MOHE, in altermagnets)
**Extraction source:** extraction/marker.md (pdftotext fallback — clean; model + Kubo formula present, DFT details in SM)

## 1. Central Claims

| ID | Claim | Testable? | Replicable-with-our-compute? |
|----|-------|-----------|------------------------------|
| C1 | MOHE (T-odd orbital Hall) is **forbidden** in conventional AFM (PT or t½T symmetry) but **universally allowed** in all 10 spin-Laue classes of collinear altermagnets. Symmetry table. | yes | **yes** (symmetry) |
| C2 | Perturbative SOC expansion Eq.(3)-(4): linear terms ∝ spin-conserve SOC, quadratic ∝ spin-flip SOC. Verified on a 2D d-wave altermagnet lattice model. | yes | **yes** (TB model) |
| C3 | **Nonperturbative enhancement**: when E_F is near a small SOC-induced gap, σ^{Lz}_xx deviates from quadratic scaling and rises sharply (Fig 2f). | yes | **yes** (TB model) |
| C4 | CrSb (DFT): supports single CPOC component σ^{Lx}_xy ≈ −8703 (ħ/e)Ω⁻¹cm⁻¹ at 300 K (τ~15 fs), ~50× larger than spin counterpart (~176); up to −3.1×10⁴ at 100 K. | yes | **maybe** (DFT + Wannier + Kubo; heavy) |
| C5 | FeSb2 (DFT): σ^{Ly}_yxy ≈ −613 (ħ/e)Ω⁻¹cm⁻¹ at 300 K, *exceeding* nonrelativistic spin Hall (~−552); spin-flip SOC dominates; nodal-surface gap origin. | yes | **maybe** (DFT + Wannier + Kubo; heavy) |
| C6 | Effective orbital Hall angle θ*_L ≈ −37% (CrSb), −15% (FeSb2) with Fe3GaTe2 FM layer. | yes | **maybe** |

## 2. Method Class
**Hybrid: symmetry/spin-group analysis + 2D lattice model (tight-binding) + first-principles DFT (CrSb, FeSb2) with Wannier interpolation and Kubo MOHE.** The model part is analytic/light; the material part is full DFT.

## 3. Computational Recipe
- **Symmetry (C1):** spin-Laue-group / magnetic-point-group analysis of σ^{La}_bc rank-3 pseudotensor; SOC expansion via spin-orbit vectors ζ^α (Eq.2-4). Reproduce by hand / with spin-group tables.
- **2D d-wave altermagnet model (C2,C3):** H = H0 + H_SOC on a square lattice (spin-Laue 2 4/1m2m1m).
  - H0 = 4t1 cos(k_x/2)cos(k_y/2)τ_x + 2t2[cos k_x+cos k_y]τ0 + 2t_s[cos k_x−cos k_y]τ_z + Jτ_z N·σ (Eq.6).
  - Spin-conserve SOC: H^c = 4λ_c sin(k_x/2)sin(k_y/2)τ_y σ_z (Eq.7).
  - Spin-flip SOC: H^f = 4λ_f[sin(k_x/2)cos(k_y/2)τ_yσ_x + cos(k_x/2)sin(k_y/2)τ_yσ_y] (Eq.8).
  - Params: **4t1=0.2, 2t2=−0.08, 2t_d=−0.04, J=0.11 (eV); λ_c=λ_f=0.1t1; μ=−0.04 eV (scaling), μ=0.06 eV (nonperturbative).**
- **MOHE Kubo formula (Eq.9):** σ^{La}_bc = −(e²/ħ)τ Σ_n ∫dk/(2π)^d f0 ⟨j^{La}_b⟩_nk ⟨v_c⟩_nk, with orbital-current ⟨j^{La}_b⟩ = Re Σ_m ⟨v_b⟩_nm⟨L_a⟩_mn and ⟨L⟩_mn the interband orbital-moment matrix (Eq. in text, ieħ²/4μ_B form).
- **DFT (C4,C5):** first-principles band structure of CrSb (hexagonal P6_3/mmc, T_N~700 K, N∥z, spin-Laue 2 6/2m2m1m) and FeSb2 (orthorhombic Pnnm, N∥y, spin-Laue 2 m2m1m). "Calculation details in Ref [50] Supplemental Material" — code (likely VASP/QE) + Wannier90 interpolation + Kubo MOHE on a dense k-mesh, T=100–300 K, τ from experiment (CrSb 15 fs, FeSb2 2.5 fs).

## 4. Replication Feasibility
- **Model claims (C1,C2,C3): tractable in hours on CPU.** 4-band (2 sublattice × 2 spin) Bloch Hamiltonian, dense-k Kubo sums, μ and λ sweeps. The orbital-moment interband matrix is the tricky piece. Straightforward.
- **Material claims (C4,C5,C6): days, heavy.** Requires: (i) DFT SCF + SOC for CrSb (2-atom-ish cell) and FeSb2 (magnetic Pnnm cell); (ii) Wannier90 downfolding to a tight-binding-like model; (iii) dense-k Kubo MOHE integration with orbital-moment matrices at multiple T and μ. Each material = a multi-step DFT+Wannier+transport pipeline. Convergence of the nonperturbative Kubo integrand near SOC gaps needs very fine k-meshes → memory/time heavy. Exact numbers depend on SM-only parameters (cutoffs, U, k-mesh) not in extracted text.
- **Realistic plan:** replicate C1-C3 (model) fully; treat C4-C5 as a stretch DFT goal.

## 5. Compute Recommendation
- **Model (C1-C3):** nuc13 (CPU), numpy, hours.
- **Materials (C4-C5):** **uicgpu 8×A100** for DFT (VASP/QE) + Wannier90 + a custom/Wannier-based Kubo MOHE code. Rough ask: 1 GPU node, DFT SCF+SOC hours each, Wannier + dense-k transport the dominant cost (potentially many core-hours for fine BZ near SOC gaps). Budget ~1–3 days wall for both materials.
- **Recommended host: nuc13 (model) + uicgpu (materials).**

## Notes / flags
marker.md clean; the model Hamiltonian (Eqs.5-9) and all model parameters are present. DFT calculation details (codes, cutoffs, U, k-mesh) are in Supplemental Material [50], NOT in extracted text — Nougat pass on the main PDF would not recover them (separate SM file needed for exact material replication).
