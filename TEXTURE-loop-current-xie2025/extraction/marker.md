# Extraction Marker — xie2025

- **Paper:** Ying-Ming Xie & Naoto Nagaosa, *Probing Loop Currents and Collective Modes of Charge Density Waves in Kagome Materials with NV Centers*
- **arXiv:** 2504.14166v1 [cond-mat.str-el], 19 Apr 2025
- **Affiliation:** RIKEN Center for Emergent Matter Science (CEMS), Wako, Japan
- **Extraction method:** `pdftotext -layout` (interim) → `extraction/pdftotext_raw.txt` (733 lines); reference text `work/textures-loop-current-xie2025.txt`
- **Nougat:** not run in this environment; `extraction/nougat.mmd` is a header-stamped interim built from the pdftotext layout pass (honest placeholder — no fabricated LaTeX/ML-OCR reconstruction).

## Key extracted equations (verbatim, as parsed)
- **Eq. (2)** Mean-field free energy:
  `F ≈ Σ_α (b cos 2θ_α − λ1') |Δ_Qα|² + λ2 |Δ_Q1||Δ_Q2||Δ_Q3| cos(θ1+θ2+θ3) + λ3 |Δ_Q1||Δ_Q2||Δ_Q3| cos θ1 cos θ2 cos θ3 + u1 Σ_α |Δ_Qα|⁴ + u2 Σ_{α≠β} |Δ_Qα|²|Δ_Qβ|²`
- **Eq. (10)** Fluctuation Lagrangian (A and E channels); contains A-channel cross term `∝ (3/2) λ2 sin(3θ0) |Δ_Q| (A^(A) θ^(A) + A^(A) θ^(A))`.
- **Eq. (12)** Mixed phase-amplitude A-channel q=0 modes:
  `κ0 (ω±^(A))² = |b| + 2(u1+2u2)|Δ_Q|² ± sqrt[ (|b| − 2(u1+2u2)|Δ_Q|²)² + (9/4) λ2² |Δ_Q|² ]`

## Headline
In the **iCDW** phase (b>0, θ0 = ±π/2) the amplitude (Higgs) and phase collective modes **mix** in the A irrep (off-diagonal `∝ sin(3θ0) ≠ 0`); in the **rCDW** phase (b<0, θ0 = 0/π) they **decouple** (`sin(3θ0)=0`). Phase-mode dynamics of the iCDW generate a time-dependent stray field detectable by NV centers.

## Figure-3 example parameters (recipe + paper)
`b=1, λ1'=5, λ2=0.1, λ3=0, u1=0.5, u2=0.5`
