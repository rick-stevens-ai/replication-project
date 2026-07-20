# PROVENANCE — code lineage for the Chatterjee-Sachdev-Scheurer 2017 replication

## Shared kernel considered

`~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`
(SHA of intent: kagome NN tight-binding + Peierls flux + Kubo/Berry/Chern +
`bond_current_and_charge` loop-current order parameter). Built for
Fernandes-Birol-Ye-Vanderbilt, arXiv:2502.16657 (kagome loop-current review).

## Scope decision (honest flag)

The kernel targets the **kagome lattice** flux-phase / staggered-flux physics
(3 sites/cell, Dirac cone at K, Haldane-like Chern insulator from a Peierls
phase). **This paper (arXiv:1705.06289) is a completely different system:** the
**square lattice**, treated by **spin-density-wave mean-field theory** (Appendix
B) plus an **SU(2) gauge theory / CP1** classification of topological order. The
"loop current" here is phase C of the cuprate pseudogap (Varma current loops),
diagnosed through the square-lattice bond bilinear J_ij = 2 Im T_ij (Eq. C14).

Therefore the kagome Bloch Hamiltonian, Chern/Berry machinery, and multi-Q
kagome textures of the kernel are **out of scope** and are NOT used. Reusing them
would be fabrication (kagome Chern numbers say nothing about this paper).

## What IS reused from the kernel (cited in code)

1. **The real=charge / imaginary=loop-current bond-bilinear decomposition.**
   The kernel's `KagomeModel.bond_current_and_charge()` builds the filled-band
   density matrix ρ = Σ_n |V_n><V_n| and reads <c_i^† c_j> off ρ, taking
   Re → bond charge, Im → loop current. This is *exactly* the paper's Eq. (C14)
   (K_ij = -2 Re T_ij, J_ij = 2 Im T_ij). We transplant this idea to the square
   lattice `sdw_bond_current()` in `sdw_meanfield.py`.
2. **The "eigendecompose a tight-binding Bloch matrix on a BZ grid, build the
   filled-band projector, evaluate observables" pattern.** The square-lattice
   2-band SDW Hamiltonian (Eq. B4) is diagonalized on a k-grid the same way.

## What is NEW (written for this paper)

- `sdw_meanfield.py`: square-lattice tp (p=1..4) dispersion ξ_k; the 2×2
  SDW mean-field Hamiltonian h_k (Eq. B4); analytic bands E_{k,±} (Eq. B6);
  filling n(μ), self-consistent gap equation h = 2 U N0, free-energy
  minimization over (h, θ, K); and the Eq.-C14 loop-current bond diagnostic.
- All physics equations transcribed directly from the paper's Appendix B/C.

## Provenance summary

- Kernel reuse: conceptual (bond-bilinear current/charge split; TB+grid pattern).
- Kernel reuse: code-level = NONE copied verbatim (different lattice/Hamiltonian).
- Verdict: kernel is the right *class* (loop-current) but wrong *lattice*; adapted
  the transferable idea, rebuilt the paper-specific core from Eqs. B4–B6, C14.
