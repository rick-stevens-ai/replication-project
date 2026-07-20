# Extraction — lund2021 (marker interim)

**Paper:** Lund, Salimath & Hals, *Spin pumping in noncollinear antiferromagnets*, arXiv:2106.15187v2 [cond-mat.mes-hall] (2021).

**Extraction method:** `pdftotext -layout` interim (marker/nougat GPU pipeline not run in this fast-path replication; `extraction/_pdftotext.txt` holds the raw dump, 638 lines). The primary machine-readable text used for physics extraction is `work/textures-spin-lund2021.txt` (1145 lines).

## Key extracted physics (Sec. III, App. A)

- **Model:** kagome monolayer AFM, Heisenberg + anisotropy
  `H = J Σ_<ij> S_i·S_j + Σ_i [ Kz (S_i·ẑ)² − K (S_i·n̂_i)² ]`, with J>0.
- **Ground state:** 120° in-plane order; sublattice easy axes
  n̂₁=[0,1,0], n̂₂=[√3/2,−1/2,0], n̂₃=[−√3/2,−1/2,0].
- **Effective-action constants (App. A):**
  a₁ = 24ℏS/(√3 a²), a₂ = 36S²J/(√3 a²),
  K₁ = 8√3(Kz+K)S²/a³, K₂ = 16√3 K S²/a³.
- **Three k=0 spin-wave resonance frequencies (Eq. after 16):**
  ω₀^(x) = ω₀^(y) = √(4K₁a₂/a₁²), ω₀^(z) = √(4K₂a₂/a₁²).
- **Headline claim:** the three spin-wave bands pump ac spin currents with
  mutually orthogonal spin polarizations (along x, y, z respectively).

## Figures/Tables
- Fig. 1: NM/NCAF bilayer, reciprocal STT ↔ spin-pumping.
- Fig. 2: kagome geometry + orthogonal-polarization schematic.
- No data tables; paper is analytic.
