# Extraction — Wernert et al. 2024 (arXiv:2404.12898v2)

**Title:** Hall mass and transverse Noether spin currents in noncollinear antiferromagnets
**Authors:** Luke Wernert, Bastián Pradenas, Oleg Tchernyshyov, Hua Chen
**Venue:** arXiv:2404.12898v2 [cond-mat.mes-hall], 25 Dec 2024
**Method:** analytic continuum field theory (Noether's theorem on a kagome-AFM σ-model) + linearized-LLG lattice numerics.

## Extraction method
- Interim text layer: `pdftotext` (poppler) → `extraction/_pdftotext_raw.txt` (835 lines, full body + End Matter + references).
- No GPU Nougat/Marker model was invoked in this run; `nougat.mmd` below is the pdftotext-derived Markdown interim with a Nougat-compatible header so downstream tooling can consume it. Marker-quality equation LaTeX was reconstructed by hand from the text layer for the key equations used in replication.

## Key equations extracted (used in replication)
- **Eq.(1)** Continuum Lagrangian: `L = (ρ/4) ∂_t n_α·∂_t n_α − (1/4) Γ_ab^{αβ} ∂_a n_α·∂_b n_β`
- **Eq.(2)** Γ tensor (kagome): `Γ_ab^{αβ} = η (√3/4) J S² (δ_{aα}δ_{bβ} + δ_{aβ}δ_{bα})`, α,β∈{x,y}; zero if α=z or β=z. η=+1 direct; η=+1(αβ=), −1(α≠β) inverse triangular.
- **Eq.(5)** Noether spin current: `J^a = −(1/2) Γ_ab^{αβ} n_α × ∂_b n_β`
- **Static-twist headline** (between Eq.5 and 6): `∂_x n_α = (∂_x φ) n_x × n_α ⟹ J^y = ±(√3/8) J S² (∂_x φ) n_y` (purely transverse).
- **Eq.(7)/(10)** dynamical d.c. response: `⟨J_a^α⟩ = Γ_ab^{αγ} P_b^γ`.
- **Eq.(11)** microscopic Γ from gradient expansion.
- **Eq.(12)** polycrystal isotropic tensor: `Γ̄_ab^{αβ} = g_H(δ_{aα}δ_{bβ}+δ_{aβ}δ_{bα}) + g_0 δ_{ab}δ_{αβ}`.
- **Eq.(13)** magnon velocities: `c_I=√(g_0/ρ̄)`, `c_{II,III}=√((g_0+g_H)/ρ̄)`.

## Headline claim (from recipe)
> A static twist in the noncollinear kagome AFM gives a purely transverse Noether spin current J^y = ±(√3/8) J S² (∂_x φ) n_y, demonstrating a Hall-like spin current response.
