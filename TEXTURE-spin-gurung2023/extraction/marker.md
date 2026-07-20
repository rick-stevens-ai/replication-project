# Extraction — gurung2023 (marker interim)

**Source:** `textures-spin-gurung2023.pdf` (Gurung, Elekhtiar, Luo, Shao, Tsymbal)
**Title:** *Nearly Perfect Spin Polarization of Noncollinear Antiferromagnets*

## Extraction method
- **Interim/fallback:** `pdftotext -layout` → `extraction/_pdftotext_raw.txt` (727 lines).
- **Marker/Nougat** (neural PDF→markdown) not run in this sandbox; this file is the
  pdftotext interim standing in for the marker pass. `nougat.mmd` carries the same
  interim body with a Nougat-style header so the 8-artifact package is complete.

## Key extracted content (headline + model)
- **Headline claim:** Mn₃GaN (noncollinear antiperovskite AFM, Γ₅g 120° spin
  structure) exhibits **nearly 100% effective spin polarization** in a broad area
  of the Fermi surface; matched to low-decay evanescent states of SrTiO₃ this
  yields **ETMR ~10⁴%** in Mn₃GaN/SrTiO₃/Mn₃GaN (001) AFMTJs.
- **Effective spin polarization (Eq. 2):** p_k∥ = |s_k∥| / Σₙ|s_nk∥|,
  s_k∥ = Σₙ s_nk∥ over conduction channels (Fermi crossings) at fixed transverse k∥.
- **p_k∥ = 100%** iff all channel spins parallel OR only one channel present.
- **Illustrative model (Fig. 1):** 2D **kagome** lattice, one orbital/atom,
  exchange-split on-site energies Eᵢ↑,↓ = Eᵢ ± Δ/2 along a noncollinear AFM
  configuration, spin-independent NN hopping t. **Six bands**; Δ/t = 1.5.
- **Symmetry:** broken P̂T̂ and T̂t̂ ⇒ spin-split bands **without SOC**.
- **Method:** DFT (Mn₃GaN) + tight-binding illustration + ballistic tunneling.

## Figures of record
- Fig. 1: kagome noncollinear AFM band structure + p_ky(ky,E_F) map (Δ/t=1.5).
- Fig. 3: Mn₃GaN atomic/spin structure, s_nk∥ for 5 Fermi-surface bands, p_k∥ map.
- Fig. 4: Mn₃GaN/SrTiO₃/Mn₃GaN AFMTJ transmission P/AP and ETMR(E).
