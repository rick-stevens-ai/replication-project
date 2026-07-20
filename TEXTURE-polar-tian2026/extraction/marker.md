# Extraction — Tian et al. 2026 (arXiv:2607.15009v1)

**Title:** Ridge-Spin-Layer Coupling and Emergent Ridgetronics in 2D Altermagnets
**Authors:** Mu Tian, Run-Wu Zhang, Chaoxi Cui, Zhi-Ming Yu, Yugui Yao
**Venue:** arXiv:2607.15009v1 [cond-mat.mtrl-sci], 16 Jul 2026
**Method:** symmetry (spin layer group) analysis + DFT (monolayer Mg₂Mo₂(PO₅)₂) + tight-binding model + Boltzmann semiclassical transport.

## Extraction method
- Interim text layer: `pdftotext -layout` (poppler) → `extraction/_pdftotext_raw.txt` (400 lines, full body + Table I + references).
- No GPU Nougat/Marker model was invoked in this run; `nougat.mmd` is the pdftotext-derived Markdown interim with a Nougat-compatible header so downstream tooling can consume it. Key-equation LaTeX was reconstructed by hand from the text layer.

## Key equations extracted (used in replication)
- **Eq.(1)** Ridge dispersion: `E(k) = f(k_y)`  — energy independent of k_x (a "ridge").
- **Eq.(2)** Boltzmann conductivity: `σ_αβ ∝ e² τ v_α v_β`, with `v_i = (1/ħ) ∂E/∂k_i`. A ridge along k_x has `v_x=0 ⟹ σ_xx=0`.
- **Eq.(3)** RSLC tight-binding Hamiltonian, basis `{|d_xz,↑⟩₂ , |d_yz,↓⟩₁}`:
  `H = ε_α + diag( π₀ cos k_x + δ cos k_y ,  π₀ cos k_y + δ cos k_x )`.
  Ridge limit `δ ≈ 0`.
- **Eq.(4)** Conductivity spin polarization: `SP_n̂n̂ = (σ_n̂n̂^↑ − σ_n̂n̂^↓)/(σ_n̂n̂^↑ + σ_n̂n̂^↓)`.

## Key symmetry facts
- Two ridges R1, R2 connected by spin group symmetry `{C₂‖O_L}` ⟹ **ridge-spin-layer coupling (RSLC)**.
- Altermagnet requirement: opposite-spin sublattices connected by `{C₂‖O_R}` (proper/improper rotation).
- Realization criteria: 2D square-lattice altermagnet; magnetic atoms on multiplicity-2 Wyckoff positions; out-of-plane moments; 1D band representation along Δ(0,v,0).
- Representative material: monolayer Mg₂Mo₂(PO₅)₂, SSG 3.81.1.1, Mo on 2g, Néel order, μ≈1.6 μ_B, ridges along Γ-X-M and Γ-Y-M connected by `{C₂‖S₄z}`.

## Headline claim (from recipe)
> RSLC enables quasi-1D 100% spin-polarized transport in 2D altermagnets: two orthogonal ridges lock to opposite spins and opposite sublayers, so SP_xx → −1 and SP_yy → +1 within the ridge energy window (Fig. 3c-III).
