# Extraction marker — nakazawa2024

- **Paper**: Giant impurity effects on charge loop current order states in kagome metals
- **Authors**: Seigo Nakazawa, Rina Tazai, Youichi Yamakawa, Seiichiro Onari, Hiroshi Kontani
- **arXiv**: 2405.12141v3 [cond-mat.str-el], 26 Feb 2025
- **Institutions**: Nagoya University; Yukawa Institute for Theoretical Physics, Kyoto

## Extraction method
- `pdftotext -layout` interim extraction → `extraction/_raw.txt` (710 lines, 68 KB).
- No Nougat GPU model available in this environment; `extraction/nougat.mmd` is a
  faithful hand-normalized markdown header + the abstract/equations copied from the
  pdftotext + pre-supplied `work/*.txt` reflow. Marked interim (NOT machine-Nougat).

## Headline claim (verbatim)
> the suppression ratio R = −ΔM_orb / M_orb^0 can exceed 50% with the introduction
> of 1% impurities. Unexpectedly, the ratio R is qualitatively insensitive to η,
> in high contrast to a naive expectation that R is proportional to the current
> suppression area πξ_J².

## Key model parameters
- Kagome, 3 sublattices A/B/C; NN hopping t = −0.5 eV; 3rd-nearest intra t' = −0.02 eV.
- T = 0.01 eV; VHS filling n = 2.55 / 3-site cell; μ = 0.
- cLC order: purely imaginary NN modulation δt_ij = ±iη; triple-Q, 2×2 (12-site) cell.
- Giant unit cell Mx×My up to 10×10 (N=1200); impurity I=100 eV (unitary/vacancy) on A site.
- k-mesh 512×512 folded BZ.
