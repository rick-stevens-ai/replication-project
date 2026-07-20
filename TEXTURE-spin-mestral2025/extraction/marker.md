# Extraction (marker) — de Mestral et al. 2025

**Paper:** Ab initio functional-independent calculations of the clamped Pockels
tensor of tetragonal barium titanate
**arXiv:** 2506.13209v1 [cond-mat.mtrl-sci] 16 Jun 2025
**Authors:** V. de Mestral, L. Bastonero, M. Kotiuga, M. Mladenović, N. Marzari, M. Luisier
**Method:** DFT (Quantum ESPRESSO) + modern theory of polarization + frozen-phonon
(phonopy) + finite-difference EO derivatives (AiiDA-Vibroscopy). PBEsol / PBEsol+U+V.

> Extraction interim produced with `pdftotext -layout` (poppler). This marker.md is
> the human-readable header + structured key-facts layer over that raw text. A true
> Marker/Nougat neural extraction was not run (no GPU model invoked); the layout-
> preserving pdftotext output in `extraction/nougat.mmd` is the faithful interim.

## Corpus mislabel (important)
Directory is `textures-spin-mestral2025`, implying a spin-texture paper. **It is not.**
This is a DFT electro-optics paper on the **clamped Pockels tensor of BaTiO3**. No spin
physics appears. The `gobel2024` skyrmion Kubo kernel / `spin_ed_probes` were inspected
but are physically irrelevant and were **not** used.

## Headline claim
The largest clamped Pockels coefficient **r51** of tetragonal BTO is recovered in the
correct experimental range (**730 ± 150 pm/V**). r51 is dominated by the ionic soft-
optical-phonon contribution and scales as **1/ω²**; it rises steeply as Ti off-centering
(and the soft-mode frequency) decreases.

## Key numbers
- Governing equation (Eq. 4): `r_ijk = -(1/n_i²n_j²)χ⁽²⁾ - (1/n_i²n_j²)Σ_m α_m p_m / ω_m²`
- Table II (PBEsol, P4bm ground state): r13=-0.1, r33=58.4, **r51=391.2** pm/V
- Experiment [15]: r13=9±2, r33=43±5, **r51=730±150** pm/V
- Table IV Ti-displacement series (PBEsol):
  | Ti disp | r51 [pm/V] | ω_soft [THz] |
  |---------|-----------|--------------|
  | 0.466% (P4bm GS) | 391.2 | 2.0 |
  | 0.450% | 667.0 | 1.5 |
  | 0.425% | 1614.7 | 1.0 |
- Soft-mode ω: PBEsol 1.80 THz, PBEsol+U+V 3.16 THz, exp 1.14 THz (Table III)
