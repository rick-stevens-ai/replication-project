# INTERIM: pdftotext fallback

> **Note.** This is a `pdftotext -layout` interim extraction standing in for a
> Marker (PDF→markdown) run. Layout, equation typesetting, and figure captions
> are approximate. The companion `nougat.mmd` is the same interim source. Use
> `work/textures-loop-current-tazai2023.txt` for the authoritative plain text.

## Bibliographic record

- **Title:** Drastic magnetic-field-induced chiral current order and emergent
  current–bond–field interplay in kagome metal AV₃Sb₅ (A = Cs, Rb, K)
- **Authors:** Rina Tazai, Youichi Yamakawa, Hiroshi Kontani
- **Affiliations:** Yukawa Institute for Theoretical Physics, Kyoto University;
  Department of Physics, Nagoya University
- **Ref:** arXiv:2303.00623v4 [cond-mat.str-el], 4 Apr 2024
- **System:** kagome metal AV₃Sb₅ loop-current (chiral current) order

## Abstract (extracted)

In kagome metals, the chiral current order parameter η with
time-reversal-symmetry-breaking (TRSB) is the source of various exotic
electronic states, while the method of controlling the current order and its
interplay with the star-of-David bond order φ are still unsolved. Here, the
authors reveal that a tiny uniform orbital magnetization M_orb[η, φ] is induced
by the chiral current order, and its magnitude is prominently enlarged in the
presence of the bond order. They derive the magnetic-field (h_z)-induced
Ginzburg–Landau (GL) free energy ΔF[h_z, η, φ] ∝ −h_z M_orb[η, φ], which
governs field-induced current–bond phase transitions. An emergent
current–bond–h_z **trilinear** coupling term, −3 m₁ h_z η·φ, explains the
field-sensitive electronic states (field-induced current order; strong
bond/current interplay) and the strain-induced increment of T_c.

## Key model parameters (Section: Model Hamiltonian)

| Quantity | Value |
|---|---|
| Orbital | single effective 3d_XZ (b3g) per sublattice A/B/C |
| NN hopping t | −0.5 eV |
| Intra-sublattice hopping t′ | −0.02 eV |
| Filling n_vHS | 2.55 electrons / 3-site cell |
| Temperature | 1 meV |
| Lattice constant a = |a_AB| | 0.275 nm |
| E₀ = ħ²/(a² m_e) | 1.0 eV |
| Supercell | 2×2 = 4×3 sites (12 sites), folded BZ |
| Current order | δt^c_ij = η · f_ij (imaginary, odd parity) |
| Bond order | δt^b_ij = φ · g_ij (real, even parity) |
| Field scale | h_z = 1×10⁻⁴ ↔ ≈ 1 Tesla |

## Central equations (as extracted)

- **Eq. 1** δt^c_ij = η · f_ij  (current order; f_ij = −f_ji, odd)
- **Eq. 2** δt^b_ij = φ · g_ij  (bond order; g_ij = +g_ji, even)
- **Eq. 3** M_orb = (μ_B / E₀ N_uc N) Σ_{k,σ} m(k)
- **Eq. 6** T=0 form: M_orb = (μ_B/E₀N_ucN) Σ_{k,α<β}
  Im{V^x_βα V^y_αβ − (α↔β)} (ε_α+ε_β−2μ)(n₀(ε_α)−n₀(ε_β)),
  with V_αβk = ⟨α|∇_k h_k|β⟩/(ε_α−ε_β)
- **Eq. 7** ΔF = −3 h_z M_orb  (free energy per 3-site cell)
- **Expansion** M_orb[η] = Σ_pqr b_pqr η₁^p η₂^q η₃^r, p+q+r = odd;
  leading allowed term b₁₁₁ (needs q₁+q₂+q₃ = 0). ⇒ M_orb ∝ η₁η₂η₃ ⇒
  M_orb ∝ η³ for the 3Q state (η,η,η)/√3; M_orb = 0 for 1Q and 2Q.
- **With bond order** M̄_orb = m₁ φ·η + m₂ η₁η₂η₃ ⇒ becomes **linear** in η.

## Headline claim

A tiny magnetic field of order **~1 T** (h_z = 10⁻⁴ in the paper's units) can
align/switch the chiral loop-current domain, because the 3Q chiral current
carries a finite uniform orbital magnetization M_orb that couples to h_z via
ΔF = −3 h_z M_orb; M_orb is strongly enhanced (and made linear in η) by
coexisting 3Q bond order through the trilinear term −3 m₁ h_z η·φ.

_(Full interim body: see `nougat.mmd`.)_
