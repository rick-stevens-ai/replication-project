# Extraction marker — tazai2025

**Paper:** Tazai et al. (2025), *Chiral d-wave superconductivity under a pure
loop-current phase in kagome metals AV3Sb5* (working title from text).

**Extraction method:** `pdftotext -layout` (interim mechanical extraction; no
Nougat GPU model available on this CPU target). Raw dump in `extraction/_raw.txt`
(832 lines) and the pre-supplied clean text in `work/textures-loop-current-tazai2025.txt`.

## Key extracted quantities
- Model: 12-site (2×2 enlarged-cell) kagome tight-binding, AV3Sb5.
- Hoppings: t = −0.5 eV, t′/t = 0.08; filling n = 11 electrons.
- Loop-current (LC) order: δt^c_ij = i·η·f_ij, f_ij = −f_ji = ±1. **η = 0.014.**
- Bond order (BO): δt^b_ij = φ·g_ij; **φ = 0 for the pure-LC result.**
- On-site attractive pairing g > 0; chiral d-wave for g < 0.5.
- Cutoff Ω = 0.01 eV; example T = 0.1 meV.
- Gap equation: λΔ_m = g Σ_l Γ_ml Δ_l ;
  Γ_ml = (T/N) Σ_{k,n} G_k^{ml}(ε_n) G_{−k}^{ml}(−ε_n) Θ(ε_n;Ω);
  Θ = Ω²/((|ε_n|−πT)² + Ω²).
- Chiral d-wave gap: Δ_μ ∝ (1, ω², ω), ω = e^{i2π/3}, χ_d = −1.

## Headline claim
Under pure LC order η = 0.014 (φ = 0), the chiral d-wave eigenvalue λ_d rises
sharply for T < 5 meV and overtakes the s-wave state, yielding a chiral d-wave
SC state with Tc ≪ 4 meV for g < 0.5. λ_d peaks around η ≈ 0.01–0.016.
