INTERIM: pdftotext fallback

# Marker extraction (INTERIM)

**Status:** INTERIM placeholder. A full `marker` (marker-pdf) conversion was not run in
this budget; this file documents the intended marker output and carries the
`pdftotext` text as the working substitute (see `extraction/nougat.mmd` and
`extraction/_pdftotext.txt` for the raw text layer).

- **Source PDF:** `textures-orbital-wang2026.pdf`
- **Title:** Nonlinear Magnetic Orbital Hall Effect Induced by Spin-Orbit Coupling
- **Authors:** Hui Wang, Huiying Liu, Yanfeng Ge, Xukun Feng, Jiaojiao Zhu, Jin Cao,
  Cong Xiao, Shengyuan A. Yang, Lay Kee Ang
- **arXiv:** 2604.02636v1 [cond-mat.mtrl-sci], 3 Apr 2026

## Key extracted content (via pdftotext)
- Proposes a **second-order nonlinear magnetic orbital Hall effect (nonlinear MOHE)**
  in PT-symmetric collinear antiferromagnets, mechanism = **orbital Berry-curvature
  dipole (OBD)**, response `δj^d_a = χ_dabc E_b E_c`, `χ_dabc = τ D_dabc`.
- **Material:** orthorhombic CuMnAs (space group Pnma, point group D2h; magnetic
  point group m'm'm' for n||[001]).
- **Headline number:** at T = 50 K, τ = 1.4 ps, near E_F:
  `χ_zzyy^(O) = -1.3` vs `χ_zzyy^(S) = -0.0087` (ℏ/e Ω⁻¹V⁻¹) →
  **orbital exceeds spin by > 2 orders of magnitude**. Also `χ_xxyy^(O)=1.4` vs `(S)=-0.0026`.
- **Mechanism detail:** SOC-required (odd in Néel vector, T-odd); nodal line in ky=0
  plane near X gapped by weak SOC (local gaps < 20 meV) → **non-perturbative**
  amplification of OBD.
- Effect flips sign under 180° Néel reversal → readout of AFM order.

> Tables/figures (Fig 1 band structure + χ(μ); Fig 1e/f k-resolved OBD; Figs 2–3
> angular dependence) are not reconstructed here; consult the PDF directly.
