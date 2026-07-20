# Method Extraction — Bhowal & Spaldin, arXiv:2212.03756 (PRX 14, 011019 (2024))

**Title:** Magnetic octupoles as the order parameter for unconventional antiferromagnetism
**Authors:** Sayantika Bhowal, Nicola A. Spaldin (ETH Zurich)
**System:** rutile MnF2, space group P4_2/mnm (D4h), magnetic space group P4_2'/mnm', T_N=67 K, spins along [001].

## Central claims
1. T-broken, centrosymmetric AFMs with non-relativistic spin splitting (NRSS / altermagnets) are described by **ferroic ordering of magnetic octupoles** — the lowest-order ferroically ordered magnetic quantity → the natural order parameter.
2. For MnF2 the relevant ferro-ordered octupole is **O_{32}^- with real-space form `xy·m_z`**, belonging to B1g. The O_{30} (`(3z²−r²)m_z`) octupole is antiferro-ordered (cancels).
3. Reciprocal-space rep obtained by r→k: O_{32}^- ↔ **`k_x k_y m_z`**, giving **d-wave NRSS**: splitting ∝ sin(kx a) sin(ky a), symmetric in k [ΔEs(k)=ΔEs(−k)], sign flip under (kx,ky)→(kx,−ky); vanishes along kx=0 or ky=0; maximal along Γ→M ([110]).
4. Minimal 4-band tight-binding model reproduces the DFT spin splitting; splitting ∝ t3·t4 (inter-sublattice hoppings) × J (exchange).
5. Piezomagnetism of MnF2 (Λxyz=Λyxz≠Λzxy) is the direct consequence of the ferro O_{32}^- octupole; predict a new **anti-piezomagnetic** effect from antiferro O_{30}.
6. Non-zero **magnetic Compton profile (MCP)** despite zero net magnetization — direct probe of the octupole; symmetric in p, sign flips [110]→[1-10].

## Tight-binding model (Sec III.D, Eqs 2–6; Appendix B)
Basis order: {Mn1-dxz, Mn1-dyz, Mn2-dxz, Mn2-dyz}.
Σ = Pauli in sublattice (Mn1/Mn2) space; σ = Pauli in orbital (dxz/dyz) space; σ0 orbital identity.

Eq(2):  Ht = α(k) I + β(k) Σz⊗σx + γ(k) Σx⊗σ0 + δ(k) Σx⊗σx

Eq(3):
  α(k) = ε1 + 2 t1 cos(kz c)
  β(k) = ε2 + 2 t2 cos(kz c)
  γ(k) = 8 t3 cos(kx a/2) cos(ky a/2) cos(kz c/2)
  δ(k) = −8 t4 sin(kx a/2) sin(ky a/2) cos(kz c/2)

Eq(4) eigenvalues (no exchange):
  E±^-(k) = α − { β² + (δ ± γ)² }^{1/2}
  E±^+(k) = α + { β² + (δ ± γ)² }^{1/2}

Eq(5) full 8×8 with AFM exchange: H = S0⊗Ht + J Sz⊗(Σz⊗σ0).
With exchange the top valence pair eigenvalues are Eq(4) but with β → J+β.

Eq(6) spin splitting of top two spin-polarized bands:
  ΔEs = E↑ − E↓
      = { (J+β)² + (δ−γ)² }^{1/2} − { (J+β)² + (δ+γ)² }^{1/2}
      ≈ (32/ε) t3 t4 sin(kx a) sin(ky a),   with ε ≡ J+β ≈ J+ε2+2t2.
Exact in kz=0 plane.

## Realistic parameters (Table I, NMTO; units Ry)
t1 = 0.0036, t2 = −0.0038, t3 = 0.0040, t4 = 0.0034, ε1 = −0.1385, ε2 = −0.0339.
Exchange splitting 2J ≈ 5 eV → J ≈ 2.5 eV. (1 Ry = 13.6057 eV.)
Lattice: rutile a ≈ 4.87 Å, c ≈ 3.31 Å (standard MnF2; used only via products kx·a etc.).

## Piezomagnetism (Eq 7)
Mx = Λxyz σyz, My = Λyxz σxz, Mz = Λzxy σxy, with Λxyz=Λyxz≠Λzxy (ferro O_{32}^-).
Anti-piezomagnetic (predicted): Λxxz=Λyyz, Λzxx=Λzyy, Λzzz from antiferro O_{30}, t_z^(τ).
NOTE: piezo/antipiezo magnitudes are RELATIVISTIC (SOC) DFT results → out of scope for TB reproduction (symmetry structure IS checkable).

## Magnetic Compton profile (Eq 9)
Jmag(pz) = ∫∫ [ρ↑(p) − ρ↓(p)] dpx dpy. DFT/Elk result → out of scope numerically; symmetry (symmetric in p, C4 sign flip, zero integral) is model-checkable via the TB spin density.

## What is DFT-only vs model/analytic
- DFT-only (Elk/VASP): octupole magnitudes vs λr (Fig 2), piezo/antipiezo moment magnitudes (Fig 4), MCP magnitudes (Fig 5), absolute band energies.
- Model/analytic (REPRODUCIBLE here): TB Hamiltonian Eqs 2–5, eigenvalues Eq 4, spin-splitting Eq 6 & its d-wave symmetry, agreement of Eq(6) analytic vs full 8×8 diagonalization (Fig 3d), reciprocal-space octupole form factor kx ky mz, symmetry selection rules (which multipoles ferro vs antiferro), piezomagnetic tensor nonzero-element structure.
