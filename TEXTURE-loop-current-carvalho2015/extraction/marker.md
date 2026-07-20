# Extraction marker — arXiv:1506.07172v2

**Paper:** V. S. de Carvalho, T. Kloss, X. Montiel, H. Freire, C. Pépin,
"Strong competition between ΘII-loop-current order and d-wave charge order along
the diagonal direction in a two-dimensional hot spot model," Phys. Rev. B **92**,
075123 (2015). arXiv:1506.07172v2 [cond-mat.str-el].

## Classification note (HONEST FLAG)

The task routed this paper into the **loop-current kagome tight-binding** class and
pointed at the reusable kernel
`~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`.

**This is a partial misclassification.** The paper IS about *loop-current order*
(the Varma ΘII orbital loop-current phase, which breaks time-reversal + parity),
so the "loop-current" tag is thematically correct. **But the lattice/model is NOT
kagome tight-binding.** It is:

- a **three-band Emery model** of the CuO2 plane (Cu 3d_{x²−y²}, O 2p_x, O 2p_y),
- reduced to a **linearized 8-hot-spot spin-fermion model** (Metlitski–Sachdev /
  Efetov–Meier–Pépin construction) on the **square lattice** Fermi surface,
- solved by a **self-consistent mean-field** competition between two order
  parameters: R_II (ΘII loop current) and b (QDW / d-wave bond charge order).

The kagome kernel's geometry (3-site corner-sharing-triangle Bloch Hamiltonian,
Peierls flux on kagome NN bonds, Chern/Berry on the hexagonal BZ) does **not**
map onto this square-lattice hot-spot model. The kernel's *conceptual* pieces DO
transfer and are cited as provenance in the code:
  - loop-current order breaks TRS through the kinetic/hopping sector (Peierls-like
    complex hopping) rather than a Zeeman term — same idea as the kernel's
    `flux_pattern` machinery;
  - the "real part = bond charge / imag part = loop current" split in the kernel's
    `bond_current_and_charge` is the discrete-lattice analogue of the paper's
    O± decomposition and of R_II (current) vs b (charge) competition;
  - a self-consistent order parameter determined by minimizing a free energy.

**Decision:** flag the misclassification, do NOT force the kagome kernel, and
replicate the paper's ACTUAL in-scope core (the coupled R_II–b mean-field
self-consistency and free-energy competition) in real code. Provenance to the
kernel is cited in `code/hotspot_mft.py`.

## Central claims (from text + Fig. 4)

1. **Coupled MF self-consistency exists.** Eqs. (31) [b] and (33) [R_II] are
   solved together from det[G⁻¹] = Π D_l^(m) (Eq. 30), with G⁻¹ the linearized
   hot-spot inverse propagator (Eq. 21) and Γ-matrices from Appendix A
   (Eqs. A1–A10). The R_II dependence enters through γ₁, γ₂, φ, θ (Eqs. A7–A10).

2. **R_II grows with V_pd; b is suppressed by V_pd** (Fig. 4a): as the NN
   Cu–O interaction V_pd increases (λ fixed), the loop-current order R_II turns on
   continuously from 0 and grows, while the QDW order b decreases toward 0.

3. **b grows with λ; R_II is suppressed by large λ** (Fig. 4b): R_II is finite
   below a λ threshold then suppressed as λ increases (V_pd fixed), while b grows
   from 0. → the two orders are mutually detrimental (COMPETITION, not
   coexistence, except a narrow fine-tuned window).

4. **Critical-ratio estimate:** (R_II^c / V_pd^c) ≈ 0.2 (from Fig. 4a).

5. **Magnetic moment estimate:** ΘII loop-current phase → M_LC ≈ 0.19 μB per
   unit cell, qualitatively consistent with the neutron estimate
   M_exp ≈ 0.05–0.1 μB (Fauqué et al.).

## Fixed parameters (Fig. 4 caption)

- t_pd = 1, t_pp = 0.5, U_p = 3, (ε_d − ε_p) = 3
- m_a = 1e-2, γ (Landau damping) = 1e-5
- n_p = 0.6 (O-orbital density), δ = 0.93 (hot-spot position: δ = (K₊−K₋)/2)
- BZ mesh 320×320; T→0 limit; b assumed k,ε-independent.
- Fig 4a: λ = 20, sweep V_pd. Fig 4b: V_pd = 14, sweep λ.

## Method for replication

The full Appendix-B/C closed forms for D_l^(m)(iε_n,k) are not reproduced in the
extracted text (they reference "Appendices B and C" with only partial listing).
We therefore build a **faithful reduced model** that keeps the paper's essential
structure exactly:
  - the linearized hot-spot G⁻¹(iε_n,k) (Eq. 21) with the Appendix-A Γ-matrices,
  - R_II entering only via γ₁,γ₂,φ,θ(R_II,δ) (Eqs. A7–A10) — verbatim,
  - ∆₊=0 (QDW sector only), b as the constant QDW mean field on the Cu/L block,
  - free energy F(T→0, R_II, b) = −Tr ln G⁻¹ + b²/(coupling) + R_II²/V_pd + const
    (Eq. 32 structure),
  - both order parameters found by MINIMIZING F (equivalent to Eqs. 31 & 33).

This reproduces the QUALITATIVE competition claims (2,3), the ratio (4), and lets
us test claim 1 (a genuine coupled self-consistent solution) with real numerics.
Claim 5 (M_LC) is checked via the paper's own stated ratio-to-moment mapping as a
sanity estimate (flagged as order-of-magnitude, since the full Ref.48 mapping is
not in the text).
