# Extraction — Malashevich, Souza, Coh & Vanderbilt (2010)

**Title:** Theory of orbital magnetoelectric response
**Authors:** A. Malashevich, I. Souza, S. Coh, D. Vanderbilt
**Ref:** New J. Phys. 12, 053032 (2010); arXiv:1002.0300v2
**PACS:** 75.85.+t, 03.65.Vf, 71.15.Rf

## Method
Interim extraction via `pdftotext` (layout) of the paper PDF into
`work/textures-orbital-malashevich2010.txt`. This markdown is the human-curated
header + key-equation digest; `nougat.mmd` holds the machine-formatted body dump.

## Headline claim
The linear (orbital) magnetoelectric (ME) susceptibility
**α_da = ∂M_a/∂E_d = ∂B_a/∂P_d** of a 3-D tight-binding *ordinary* ME insulator,
computed under **periodic boundary conditions** (k-space Berry-phase /
Chern-Simons "axion" OMP), is in **excellent agreement** with **bounded-sample**
(open-boundary, finite-field) calculations.

## Physics decomposition (orbital magnetoelectric polarizability, OMP)
- OMP α = "frozen-ion orbital" ME response (the one term lacking prior framework).
- Isotropic part ↔ dimensionless axion angle θ:  α_da^θ = (θ e²/2πhc) δ_da.
- Three gauge-invariant contributions:
  1. **Chern-Simons OMP (CSOMP)** — eq (47a): θ_CS = −(1/4π)∫d³k ε_ijk tr[A_i ∂_j A_k − (2i/3) A_i A_j A_k], with non-Abelian Berry connection A over occupied bands. Purely isotropic; the only term surviving for Z₂ TIs (quantized θ=π).
  2. **α̃^LC** (local circulation, Kubo-like) — eq (47b).
  3. **α̃^IC** (itinerant circulation, Kubo-like) — eq (47c).
- For ordinary insulators all terms contribute (θ = θ_CS + θ_Kubo).

## Model (Appendix A, table A1)
- Spinless simple-cubic lattice, primitive cell doubled to **2×2×2 = 8 sites/cell**.
- H₀ = Σ_i E_i c†_i c_i + Σ_⟨ij⟩ e^{iφ_j→i} c†_i c_j, hopping magnitude t=1.
- On-site energies E_i = {−6.5, 0.9, 1.4, 1.2, −6.0, 1.5, 0.8, 1.2}.
- Complex NN hopping phases (φ_x, φ_y, φ_z) per site in table A1; one x-phase is the scanned parameter φ ∈ [0, 2π].
- **Two lowest bands treated as occupied** (valence); gap to the other six.
- Breaks time-reversal and inversion (required, else α ≡ 0). r taken diagonal in TB basis.

## Numerics (paper)
- PBC: 80×80×80 k-mesh; smooth gauge via projection of delta trial orbitals at the two lowest-on-site sites.
- Open BC: cubes of L×L×L cells (2L+1 sites/edge), L=4,5,6,7; extrapolate M(L)=M+a/L+b/L²+c/L³.
- Reported cross-method differences: ~1e-7 e²/ħc.
