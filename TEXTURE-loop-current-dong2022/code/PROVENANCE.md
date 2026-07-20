# Code provenance

- `loop_current_meanfield_kernel.py` — VERBATIM copy of the shared TEXTURES-100
  reusable kernel `~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_meanfield_kernel.py`
  (the kernel ASSIGNED for this replication; proven on tazai2022). Provides the
  kagome cluster geometry, the Peierls-flux bond-current operator
  `J_ij = -2 Im[H_ij rho_ji]`, the triangle loop-order parameter, and a
  finite-field loop-current susceptibility probe. Its geometry + current-operator
  concepts are the base that `kagome_tV1V2.py` extends to the paper's 2x2 model.

- `loop_current_kagome_kernel.py` — VERBATIM copy of the shared TEXTURES-100
  reusable kernel `~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`.
  Provides: kagome geometry (A1,A2,sublattice midpoints), 3x3 Bloch H with Peierls
  flux, Fukui-Hatsugai-Suzuki Chern, bond-current/charge operator expectation,
  DOS, and the multipole/patch-channel classifiers. Used here for (a) the baseline
  kagome band-structure/vH cross-check and (b) the FHS Chern algorithm pattern.

- `kagome_tV1V2.py` — THIS paper's model-specific solver, adapted from the kernel.
  The kernel's single-cell 3x3 machinery is INSUFFICIENT for this paper because the
  order is a 2x2 (M-point) complex bond CDW. We therefore extend the kernel with:
    * a 12-site (2x2) supercell enumerator (Supercell class),
    * complex nn + nnn bond order parameters (chi_1,2,3 and chi'_1,2,3 classes),
    * a self-consistent Hartree-Fock loop implementing paper Eq. (20),
    * a finite-T bare bond susceptibility (Lindhard) for the nn/nnn real/imag
      channel selectivity (paper Sec. II / Fig. 1c-d),
    * Fukui-Hatsugai Chern on the folded reduced BZ for the LC-state Chern numbers.
  Geometry conventions (A1,A2, half-bond vectors, FHS link-variable Chern) are
  taken directly from the kernel to preserve provenance.
