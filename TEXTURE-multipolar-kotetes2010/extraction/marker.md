# Extraction (marker) — kotetes2010

**Paper:** Magnetic-field-induced chiral hidden order in URu₂Si₂
**Authors:** P. Kotetes, A. Aperis, G. Varelogiannis
**Venue:** Philosophical Magazine, Vol. 00 (2010); arXiv:1002.2719v2 [cond-mat.str-el]

## Extraction method

- **Tool:** `pdftotext -layout` (poppler-utils) as the interim extractor. A true
  `marker`/`nougat` neural-layout pass was not available in this environment, so
  this file is the **pdftotext interim** with a marker-style header/section
  scaffold applied by hand. The companion `nougat.mmd` carries the same interim
  content in MMD form. This is disclosed honestly — no OCR/layout model output is
  fabricated here.
- **Source text of record** for the replication physics: `work/textures-multipolar-kotetes2010.txt`
  (pre-extracted full text, 1542 lines), from which all equations and parameters
  below were read.

## Key content extracted (used by the replication)

### Model (Appendix A–B)
- Chiral d-SDW order parameter: Δᶻ_Q(k) = Δ₁ sin kₓ sin k_y − i Δ₂ (cos kₓ − cos k_y)
  - Δ₁ = dₓy (chiral, field-induced), Δ₂ = d_{x²−y²} (driving HO gap).
- Single-band nesting model: ε(k) = −2t(cos kₓ + cos k_y), ε(k+Q) = −ε(k), Q=(π,π).
- 4 quasiparticle bands E^B_{s,ν}(k) = −(s μ_B − m_z(k))B + ν√(ε² + |Δᶻ_Q|²) (Eq. B3).
- Berry curvature Ωᶻ (Eq. B1) → intrinsic orbital moment m_z = eEΩᶻ/ħ (Eq. B2).

### Self-consistency / free energy (Appendix C)
- F = 2v(Δ₁²/4V″ + Δ₂²/V′) − (1/β)Σ_{k,s,ν} ln(1+e^{−βE^B}) (Eq. C1).
- Parameters: t=50 meV, μ=0.69 meV, μ_B=0.058 meV/T, a=5 Å, V′=23.5 meV, V″=35.25 meV.

### Landau reduction (Appendix D)
- F = α₁Δ₁²/2 + α₂(T−T₀)Δ₂²/2 + βΔ₂⁴/4 − gΔ₁Δ₂B_z.
- ∂F/∂Δ₁=0 ⇒ Δ₁ = (g/α₁)Δ₂B_z (**dₓy is field-induced**).
- T₀(B_z) = T₀ + (g²/α₁)B_z² (**field-enhanced Tc** → chiral HO fills the whole B–T diagram).

### Headline numbers (targets)
- T_HO = 17.5 K; Δ₂(B=0)=1.55 meV, Δ₁(B=0)=0.
- MCEP / Bc1 = 33.5 T, T≈3 K; Bc2 ≈ 41 T (double-step metamagnetism).
- Above MCEP: Δ₂(B)/Δ₂(0) ≈ 1 − (B/Bc1)².
- Giant Nernst ≈ 30 μV/K near B≈12 T, T≈3–4 K ("tilted-hill").
