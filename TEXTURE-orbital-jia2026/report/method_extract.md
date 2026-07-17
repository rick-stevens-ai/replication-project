# Method Extraction — jia2026

**Paper:** Geometry-Driven Nonlinear Orbital Magnetoelectric Effect (Jia, Qiao, Wang, arXiv:2605.17462)
**Texture class:** orbital (nonlinear orbital magnetoelectric effect, NOME)
**Extraction source:** extraction/marker.md (pdftotext fallback — clean; heavy tensor equations legible)

## 1. Central Claims

| ID | Claim | Testable? | Replicable-with-our-compute? |
|----|-------|-----------|------------------------------|
| C1 | A nonlinear OME exists: δM^c = χ^{c;ab} E_a E_b, rank-3 P-even pseudo-tensor, allowed even in centrosymmetric materials (unlike linear OME). | yes (analytic/symmetry) | **yes** |
| C2 | Intrinsic NOME splits into 3 terms (conventional "od", dipole "d", positional-shift "ic"), all governed by the Hermitian connection; extrinsic NOME has 3 analogous τ-linear terms. Eqs.(3)-(9). | yes | **yes** (model TB numerics) |
| C3 | Symmetry: 41 MPGs support intrinsic NOME, 55 support extrinsic (vs only 10/8 for linear OME) in 2D. Table I constraints. | yes | **yes** (group theory / symmetry enumeration) |
| C4 | Modified Kane-Mele honeycomb model (Eq.11, 6m'm' MPG): only χ^{(0)}_{z;xx}=χ^{(0)}_{z;yy} finite; geometric d+ic terms dominate near band edge; orbital M ≈ 3× spin M, opposite sign; at λ_R=0 retains ~10 μ_B/V² minimum. | yes | **yes** (small TB model) |
| C5 | CuMnAs AFM model (Eq.12, PT-symmetric): only extrinsic χ^{(1)}_{z;xy} finite; Hermitian connection dominates; peak from Dirac points. | yes | **yes** (small TB model) |
| C6 | Magnitude estimates: honeycomb ~10⁻⁵ μ_B/nm², CuMnAs ~10⁻⁶ μ_B/nm² at E=10⁵ V/m — detectable by polar-MOKE. | yes | **yes** |

## 2. Method Class
**Analytic (extended semiclassical wavepacket theory) + model-Hamiltonian tight-binding numerics.** Gauge-invariant Berry-phase / quantum-geometry response formulas evaluated on 2D lattice models. No DFT in the main text (author notes formulation is "suitable for first-principles implementation" but does not do it).

## 3. Computational Recipe
- **Response formulas:** implement Eqs.(3)-(9) — intrinsic (χ^{(0,od)}, χ^{(0,d)}, χ^{(0,ic)}) and extrinsic (χ^{(1,od)}, χ^{(1,ic)}, χ^{(1,d)}) NOME in terms of: interband Berry connection r^a_nm, velocity matrix v^a_nm, orbital-moment matrix L^c_nm = (1/4)ε_cαβ Σ{r^α,v^β}, quantum geometric tensor g^{ab}_nm, Hermitian connection C^{αab}_nm, covariant derivative D^a_mn.
- **Model 1 — modified Kane-Mele** (Eq.11): H = −t Σc†c + iλ_R Σ(σ×d_ij)_z + iλ_so Σv_ij σ_z + λ Σ s_z. Params: **t=0.85 eV, λ_R=20 meV, λ=10 meV, λ_so=10 meV, T=20 K**; μ swept; λ_R swept at μ=50 meV.
- **Model 2 — CuMnAs AFM** (Eq.12): H = −2t τ_x cos(k_x/2)cos(k_y/2) − t'(cos k_x+cos k_y) + λτ_z(σ_y sin k_x − σ_x sin k_y) + J_n τ_z σ_x. Params: **t'=0.08t, J_n=0.6t, λ=0.8t, T=100 K, τ=10 fs.**
- **Codes/packages:** none named. Reproduce with numpy (2-band / 4-band Bloch Hamiltonians, dense k-mesh BZ integration, finite-difference or analytic derivatives for connections). Symmetry table via magnetic point group transformation rule Eq.(10) — can use spglib/custom.
- **Key numerics:** dense 2D k-mesh (e.g. 200×200+ for convergence of geometric integrands near Dirac points), Fermi-Dirac at stated T, relaxation time τ for extrinsic terms.

## 4. Replication Feasibility
- **Fully tractable in hours on CPU.** These are 2-band and 4-band tight-binding models on 2D k-grids. The nontrivial part is *correctly coding the quantum-geometry response tensors* (Hermitian connection, positional shift) — error-prone but well-specified by Eqs.(3)-(9). Convergence near Dirac points needs a fine k-mesh but is cheap.
- Supplemental Material holds the full derivation and MPG enumeration; the two model calculations (C4,C5) and magnitude estimates (C6) are self-contained in the main text.
- Symmetry enumeration (C3: 41/55 MPGs) is pure group theory — a few hours of careful coding.

## 5. Compute Recommendation
- **Host: nuc13 (CPU)** — numpy, dense-k BZ sums for two small models. Multi-core helpful for the k-mesh integration and μ/λ sweeps. Rough ask: 1 node, 8–16 cores, hours.
- No GPU needed. chiatta00/SYCL not relevant.

## Notes / flags
marker.md clean; the dense tensor algebra (Eqs.3-9) survived pdftotext with sub/superscripts mangled but structurally intact — a Nougat pass would give cleaner LaTeX of these equations and would *help* implementation accuracy, but is not strictly required. Model parameters (C4,C5) fully present. **Recommend optional Nougat pass** purely to de-risk transcription of the response-tensor equations.
