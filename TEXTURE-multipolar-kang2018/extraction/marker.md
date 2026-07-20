# Extraction — Kang, Shiozaki, Cho (2018/2019)

**Paper:** "Many-Body Order Parameters for Multipoles in Solids"
**arXiv:** 1812.06999 (v4, 10 Mar 2019)
**Journal:** Phys. Rev. B **100**, 245134 (2019)
**Authors:** Byungmin Kang (KIAS), Ken Shiozaki (YITP Kyoto), Gil Young Cho (POSTECH)
**Subject:** cond-mat.str-el (higher-order topological insulators, multipole moments)

> Source note: Text extracted with `pdftotext -layout` from the arXiv v4 PDF.
> The `pdf` vision tool was unavailable (no API credits / plugin disabled), so
> equations were transcribed from the layout text. Figures were not OCR'd.

---

## 1. Central claims

1. **Many-body order parameters for bulk multipoles.** The authors generalize
   Resta's many-body polarization to define gauge-invariant, real-space
   order parameters for the **dipole**, **quadrupole**, and **octupole**
   moments of a crystalline insulator, as expectation values of a single
   many-body *unitary* built from the position operator.

2. **They equal the corner charge.** Via an effective-field-theory argument
   they show `⟨Û_a⟩ = exp(2πi q_c)`, i.e. the phase of the order parameter
   equals the physical corner charge `q_c` (= physical multipole moment
   `Q^ph`), even when the quantizing symmetries are broken.

3. **They outperform the nested Wilson loop.** The nested-Wilson-loop index
   `Q^ω_xy = 2 p^ω_x p^ω_y` only equals the physical moment when quantizing
   symmetries are present. The many-body order parameter tracks the physical
   moment / corner charge even when symmetries are broken (and in "anomalous"
   quadrupole insulators where the nested Wilson loop fails entirely).

4. **Numerical proof** on the non-interacting Benalcazar–Bernevig–Hughes (BBH)
   quadrupole model reproduces the quantized quadrupole (0 vs 1/2), the sharp
   phase boundaries at the Wannier-gap closings, and (via Thouless pumping)
   the continuous agreement of `Im ln⟨Û₂⟩/2π` with `q_c`.

---

## 2. Order-parameter definitions

**Dipole (Resta):**
```
P_x = (1/2π) Im ln ⟨Û₁⟩ ,   Û₁ = exp( 2πi Σ_x x n̂(x) / L_x )      (Eq. 1)
```
`n̂(x)` = electron-number operator at site x; L_x = system length along x;
periodic BC x ~ x + L_x. Expectation is over the many-body ground state.

**Quadrupole:**
```
Q_xy = (1/2π) Im ln ⟨Û₂⟩ ,  Û₂ = exp( 2πi Σ_r (x y / (L_x L_y)) n̂(r) )   (Eq. 2)
```
sum over (x,y) ∈ (0,L_x] × (0,L_y].

**Octupole:**
```
O_xyz = (1/2π) Im ln ⟨Û₃⟩ , Û₃ = exp( 2πi Σ_r (x y z /(L_x L_y L_z)) n̂(r) )  (Eq. 3)
```

**Well-definedness:** Q_xy is well-defined (invariant mod 1) only when the
total polarization vanishes (P_x = P_y = 0). Under mirrors {M_x, M_y}:
`Û₂ → Û₂*`, so `Q_xy → −Q_xy`, quantizing it to 0 or 1/2 mod 1.

**Generalized (partial-region) operators** V̂₁(l), V̂₂(l) (Eqs. 6,7) restrict
the exponent to a sub-region r ∈ (0,l]×(0,l] and give the same information.

---

## 3. Model (numerical proof) — BBH quadrupole insulator

Bloch Hamiltonian (Eq. 8 = Eq. D5), 4 orbitals/cell on a square lattice with
π-flux per plaquette:
```
h(k) = [γ_x + λ_x cos k_x] Γ4 + λ_x sin(k_x) Γ3
     + [γ_y + λ_y cos k_y] Γ2 + λ_y sin(k_y) Γ1 + δ Γ0        (Eq. 8 / D5)
```
Gamma matrices (τ_i = Pauli, τ_0 = 2×2 identity; Kronecker order τ⊗τ):
```
Γ0 = τ3 ⊗ τ0
Γi = −τ2 ⊗ τi   (i = 1,2,3)
Γ4 = τ1 ⊗ τ0
```
- `γ` = intra-cell hopping, `λ` = inter-cell hopping, `δ` = on-site
  dimerization/mass that breaks mirror & C4 but keeps C2.
- **Half filling** (2 of 4 bands occupied).
- **Physical energy gap** closes only when `|γ_x/λ_x| = 1` AND `|γ_y/λ_y| = 1`.
- **Wannier gap** closes when `|γ_x/λ_x| = 1` OR `|γ_y/λ_y| = 1`.
- Topological quadrupole (q_xy = 1/2) when δ=0, `|γ_x/λ_x| < 1`, `|γ_y/λ_y| < 1`.
- Symmetries at δ=0: mirrors M_x=iτ1⊗τ3, M_y=iτ1⊗τ1 (anticommute due to π-flux);
  C4 = [[0, τ0],[−iτ2, 0]] when γ_x=γ_y, λ_x=λ_y; C2 = −iτ0⊗τ2 (keeps P=0 even δ≠0).

**Thouless pumping paths** (θ ∈ [0,2π]):
- Isotropic (Eq. 9): γ_x=γ_y=1−0.6 sinθ, λ_x=λ_y=1+0.6 sinθ, δ=0.6 cosθ.
- Anisotropic (Eq. 10): γ_x=1−0.6 sinθ, γ_y=1−0.5 sinθ, λ_x=1+0.6 sinθ,
  λ_y=1+0.5 sinθ, δ=0.6 cosθ.

---

## 4. Key numerical results

- **Phase diagram (Fig 1a):** with δ=0, λ_x=λ_y=1, shaded (topological,
  q_xy=0.5) region for γ_x,γ_y < 1; gap-closing dots on the boundary.
- **Cuts (Fig 1b,c):** `Im ln⟨Û₂⟩/2π` jumps sharply 0 ↔ 0.5 at γ_y = 1.
- `|⟨Û₂⟩|` vanishes exactly at the phase boundary (Wannier-gap closing),
  `|γ/λ| = 1`.
- **Thouless pumping (Fig 2):** phase of ⟨Û₂⟩ and corner charge q_c coincide
  (no discernible difference) along the full pump; nested-Wilson `Q^ω` agrees
  only at the quantized points θ = π/2, 3π/2 (δ=0).
- **Anomalous quadrupole insulator (Fig 1d):** ⟨Û₂⟩ captures the topological
  transition at V_2z / √(Δ²+µ'²) = 1 where the nested Wilson loop fails.

---

## 5. Free-fermion evaluation (implementation note)

For a Slater-determinant ground state the many-body expectation of a
single-body exponential unitary reduces to a determinant over the occupied
single-particle subspace:
```
⟨Ψ| exp( i Σ_r φ(r) n̂_r ) |Ψ⟩ = det( P† · diag(e^{iφ(r)}) · P )
```
where P is the (N_sites·orb × N_occ) matrix whose columns are the occupied
single-particle eigenvectors, and φ(r) is the phase field (2π x/L_x for the
dipole; 2π x y /(L_x L_y) for the quadrupole). This is the standard
Resta/Wilczek–Zee determinant identity used to make Eqs. (1)–(2) computable.
Q_xy = (1/2π) Im ln det(...).
