# Marker extraction — Li, Sandhoefner & Kovalev (arXiv:1907.10567v3)

> **Extraction note.** No GPU/marker or nougat binary was available in the
> physics runner environment. This file is the `pdftotext`-based interim
> extraction (poppler `pdftotext`, `/usr/bin/pdftotext`) with a marker-style
> header added for pipeline compatibility. The companion `nougat.mmd` carries
> the same text with the mathematical result equations transcribed to LaTeX.

**Title:** Intrinsic spin Nernst effect of magnons in a noncollinear antiferromagnet
**Authors:** Bo Li, Shane Sandhoefner, Alexey A. Kovalev
**Affiliation:** Dept. of Physics & Astronomy and Nebraska Center for Materials
and Nanoscience, University of Nebraska, Lincoln, NE 68588, USA
**Ref:** arXiv:1907.10567v3 [cond-mat.mes-hall] 24 Oct 2019

## Abstract

We investigate the intrinsic magnon spin current in a noncollinear
antiferromagnetic insulator. We introduce a definition of the magnon spin
current in a noncollinear antiferromagnet and find that it is in general
non-conserved, but for certain symmetries and spin polarizations the averaged
effect of non-conserving terms can vanish. We formulate a general linear
response theory for magnons in noncollinear antiferromagnets subject to a
temperature gradient and analyze the effect of symmetries on the response
tensor. We apply this theory to single-layer potassium iron jarosite
KFe3(OH)6(SO4)2 and predict a measurable spin current response.

## Key physical content (headline claim)

The in-plane Dzyaloshinskii–Moriya interaction (DMI) in the kagome
antiferromagnet KFe3(OH)6(SO4)2 generates a **measurable intrinsic magnon spin
Nernst response**. The out-of-plane DMI, together with the in-plane DMI, forces
a small out-of-plane spin canting (η ≈ 1.9°) of the 120° noncollinear order.

## Model (Eq. 16)

    H = Σ_<ij> J1 S_i·S_j + Σ_<ij> D_ij·(S_i × S_j) + Σ_<<ij>> J2 S_i·S_j

with DMI vector D_ij = Dp n̂_ij + Dz ẑ (in-plane radial + out-of-plane).

Material parameters: J1 = 3.18 meV, J2 = 0.11 meV, |Dp|/J1 = 0.062,
Dz/J1 = −0.062, S = 5/2 (Fe³⁺).

Canting angle:  η = (1/2) tan⁻¹( −2Dp / (√3(J1+J2) − Dz) ) ≈ 1.9°.

Spin order: <S_i> = S(cos η cos φ_i, cos η sin φ_i, sin η),
φ_A = π/2, φ_B = 7π/6, φ_C = −π/6.

## Main result (Eq. 15 / Eq. 1)

Intrinsic magnon spin Nernst response:

    Θ_α = (2 k_B / V) Σ_{n=1..N} Σ_k (Ω^{θα}_{n,k})_β c1[g(ε_{n,k})] ∇_β T

with c1(x) = (1+x)ln(1+x) − x ln(x), g Bose–Einstein, and the generalized
(spin) Berry curvature (Eq. 9)

    (Ω^θ_{n,k})^α_β = Σ_{m≠n} (σ3)_nn (σ3)_mm
                       · 2 Im[(θ_α)_nm (v_β)_mn] / (ε̄_n − ε̄_m)²

for the spin-current operator ĵ^γ_λ = (1/4)(v̂_λ σ3 Ŝ^γ + Ŝ^γ σ3 v̂_λ).

## Reported numerical findings

- Ordinary Berry curvature integrates to Chern numbers **−3, 1, 2** (bottom→top band).
- Spin Nernst conductivity α^y_yx / k_B rises with T to a peak of order **~3.5**
  near k_B T / (J1 S) ≈ 1 (Fig. 3).
- The z-polarized response α^z_yx is **~2 orders of magnitude smaller** than the
  in-plane (y) response, because the canting angle η is small.
- Symmetry (M_x T + C_3z) fixes the tensor shape, Eq. (18).
- Predicted 3D spin current ~10⁻¹¹ J/m² for a 20 K/mm gradient.

---
*Full body text of the paper is available in `work/textures-spin-li2019.txt`
(pdftotext of the same PDF) and the raw interim in `extraction/_pdftotext.txt`.*
