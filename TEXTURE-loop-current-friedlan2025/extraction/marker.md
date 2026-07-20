# Extraction marker — arXiv:2510.05234

**Paper:** A. Friedlan & H.-Y. Kee, *Emergence of nematic loop-current bond order in
Kagome metals near van Hove singularities*, arXiv:2510.05234v2 (dated 2026-02-12).

**Extraction method:** `pdftotext -layout paper.pdf paper.txt` (poppler 25.x). PDF was
not vision/credit-blocked; text layer clean. Equations transcribed by hand from the
`-layout` dump (LaTeX math renders as unicode-ish ASCII in pdftotext; verified against
figure captions and Appendix A closed forms).

## Central claims / method
- **Effective patch model** near the 3 inequivalent M points, capturing one p-type (vH1)
  and one m-type (vH2) van Hove singularity at each M. Basis
  `{ψ2A, ψ2B, ψ2C, ψ1A, ψ1B, ψ1C}` → **6×6 Bloch Hamiltonian H(k)** (Eq. 4).
- Kinetic patch term `H_patch` (Eq. 1): on-site ±ε splitting between vH2 (+ε) and vH1 (−ε),
  mixing λ k_α between vH1/vH2 blocks. `k1=-kx/2+√3ky/2, k2=-kx/2-√3ky/2, k3=kx`.
- **CBO order parameter** triplet `(Δ_AB, Δ_BC, Δ_CA)` enters via `H_CDW` (Eq. 3) with
  projection factors `s1=-2|b'|²` (vH1) and `s2=+2|b|²` (vH2). For CsV3Sb5: b'≈0.9, b≈0.5
  ⇒ **s1≈-1.62, s2=0.5** (Fig. 5 caption uses exactly these + **ε=0.12 eV**).
- Order-parameter classification by complex phases `Δ_αβ=|Δ|e^{iϕ}`; total phase
  **Φ=ϕ1+ϕ2+ϕ3 (mod 2π)**, always 0 or π. CBO+/LCBO− at Φ=0; CBO−/LCBO+/NLCBO at Φ=π.
- **Unperturbed (λ=0) eigenvalues** (Eq. 9):
  `E_n^(i) = (-1)^i ε - μ + 2 s_i Δ cos((Φ + 2πn)/3)`, n=0,1,2, i=1,2. (Fig. 4 uses Δ=0.2 eV.)
- **Degeneracy** at Φ=0 and Φ=π (Fig. 4): the three cos((Φ+2πn)/3) values collapse to a
  2+1 pattern.
- **Second-order-in-λ perturbation** (Eqs. 10–12) lifts the Φ=π degeneracy among
  CBO−/LCBO+/NLCBO. Inverse-energy factors (Eq. 12):
  `[1/ΔE1] = 1/(2Δ(s1-s2)+2ε) - 2/(Δ(s1+2s2)-2ε)`,
  `[1/ΔE2] = 1/(2Δ(s1-s2)+2ε) + 1/(Δ(s1+2s2)-2ε)`.
  Paper states: for Δ large enough, **1/ΔE1>0 and 1/ΔE2<0** (Fig. 5).
- **Mechanism:** NLCBO uniquely develops an anisotropic (k_x-only) anomalous dispersion
  `+8k_x²/(3ΔE2)` (Eq. 11) that, with 1/ΔE2<0, lowers its band energy below isotropic
  CBO−/LCBO+ for a partially filled band → nematic (C6→C2) stabilization.
- Phase-config choices satisfying Φ=π: CBO− (π,π,π); LCBO+ (π/3,π/3,π/3);
  **NLCBO (0,π/2,π/2)** (breaks rotational symmetry).
- Nine-band tight-binding model (Sec. IV) confirms NLCBO survives with λ≈0.35 eV·a;
  30×30 k-grid. (Full-BZ 9-band DFT-derived model — out of scope for exact reproduction;
  see failure_analysis.)

## Numbers pinned for replication
- ε = 0.12 eV; s1 = -1.62; s2 = 0.5; Δ = 0.2 eV (Fig. 4/5).
- k_cut = 1 (fixed), λ tuned; λ_true ≈ 0.35 eV·a.
- Phase configs: CBO−(π,π,π), LCBO+(π/3,π/3,π/3), NLCBO(0,π/2,π/2), CBO+(0,0,0).
