# Method Extraction — oh2026

**Paper:** Observation of spin-free interatomic orbital angular momentum in a chiral crystal (Oh et al., arXiv:2605.21124)
**Texture class:** orbital (itinerant OAM in chiral Te)
**Extraction source:** extraction/marker.md (pdftotext fallback — clean, fully readable)

## 1. Central Claims

| ID | Claim | Testable? | Replicable-with-our-compute? |
|----|-------|-----------|------------------------------|
| C1 | Chiral Te hosts well-isolated 5s-orbital bands (E−E_F = −15 to −8 eV) separated from the 5p manifold, matching a 3-band tight-binding model of a single helical chain (Fig 1d, 2f). | yes | **yes** (TB + DFT band structure) |
| C2 | These s-orbital bands carry OAM of *purely interatomic* origin (L_Itin), with **no** intra-atomic contribution (L_Atom = 0 for s). ACA gives vanishing L; modern-theory global L is finite. | yes | **yes** (DFT + Wannier + modern theory of orbital magnetization vs ACA) |
| C3 | CD-ARPES shows two bands of opposite CD sign crossing; CD magnitude ∓17% at E−E_F = −9.2 eV, k_x = ±0.4 Å⁻¹, reproducing the CIOS L_Itin_x texture. | yes (experimental) | **no** (ARPES beamline experiment) |
| C4 | SARPES shows no SAM polarization in the s-orbital bands (spin-degenerate) — decisive evidence of spin-free OAM. | yes (experimental) | **no** (spin-resolved ARPES) |
| C5 | First-principles for bulk Te yields finite L_Glob_y, L_Glob_z (beyond single-chain model) from interchain hopping; 3D iso-energy surface at −9.5 eV. | yes | **yes** (DFT) |

The replicable core is the **theory half**: single-chain tight-binding band+OAM, and DFT+Wannier OAM texture of bulk Te comparing ACA vs modern theory. The ARPES/CD-ARPES/SARPES claims (C3,C4) are experimental and out of scope for computational replication (but their theoretical counterparts C2/C5 are directly comparable).

## 2. Method Class
**Hybrid: DFT (VASP) + Wannier90 + tight-binding model + modern theory of orbital magnetization.** (Experimental ARPES is the other half, not replicable.)

## 3. Computational Recipe
- **Tight-binding model:** 3-band model of a single right-handed helical chiral chain with threefold screw-rotation symmetry (Ref [27] Göbel/Schimpf/Mertig analytic model). Bands split by ∂E/∂k sign → ±L_Itin_x. Direct to implement (small analytic TB Hamiltonian).
- **First-principles:** VASP (refs [37,38] Kresse-Furthmüller) with PAW pseudopotentials (refs [39,40]), PBE-GGA (ref [41]), non-collinear magnetism / SOC (refs [42,43]). Structure of chiral Te (trigonal, space group P3₁21 / P3₂21) — from Materials Project (ref [44]).
- **Wannierization:** Wannier90 (refs [45,46,47]) to build MLWFs; OAM computed two ways: (i) atomic-centered approximation (ACA) — L_Atom only; (ii) modern theory of orbital magnetization (Thonhauser/Ceresoli/Vanderbilt/Resta, ref [14]) — global L_Glob incl. itinerant part.
- **Post-processing:** `post_wan` code (ref [48], github.com/philipp-eck/post_wan) for OAM/CD texture on iso-energy surfaces.
- **Key parameters (mostly in Supplemental Material, not in main text):** plane-wave cutoff, k-mesh, U (Te is a p/s-electron system — likely no +U), Te lattice params a≈4.46 Å, c≈5.92 Å. Iso-energy surface at E−E_F = −9.5 eV; s-bands at −8 to −15 eV.

## 4. Replication Feasibility
- **Tight-binding single-chain model (C1 band shape, C2 L_Itin sign):** trivial — analytic 3×3 Hamiltonian, minutes on CPU (nuc13). Fully tractable.
- **DFT + Wannier OAM texture of bulk Te (C2, C5):** Te is a light 3-atom chiral cell; a VASP SOC calculation + Wannier90 is a small job. On uicgpu 8×A100 (or CPU): SCF + non-SCF band + wannierization = **hours**. Main friction: VASP is not GPU-native in older builds (CPU VASP is fine here — small cell), and detailed cutoffs/k-mesh live in the Supplemental Material we don't have parsed. Modern-theory-of-orbital-magnetization post-processing via post_wan needs setup but is CPU-light.
- **Overall: tractable in hours→~1 day** for the theory claims. Experimental claims (C3,C4) infeasible (no beamline).

## 5. Compute Recommendation
- **TB single-chain model:** nuc13 (CPU), Python/numpy, <1 core-hour.
- **DFT+Wannier Te:** uicgpu (if GPU-VASP available) OR nuc13/CPU VASP for the small Te cell (3 atoms). Rough ask: 1 node, ~8–16 cores, a few hours SCF+bands; Wannier90 + post_wan on 1 core. VASP license required (check availability); QuantumESPRESSO+Wannier90 is a free-stack alternative and adequate here.
- **Recommended host: uicgpu** (DFT) with **nuc13** for the TB model.

## Notes / flags
marker.md is clean; equations render as unicode but are legible. Supplemental Material (cutoffs, exact k-mesh, U) is NOT in the extracted text — Nougat pass would not help (it's in a separate SM file). For exact numeric replication, the SM PDF must be pulled separately.
