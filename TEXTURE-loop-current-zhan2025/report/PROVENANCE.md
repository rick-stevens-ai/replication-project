# PROVENANCE — TEXTURE-loop-current-zhan2025

## Paper
Jun Zhan et al., "Loop Current Order on the Kagome Lattice",
arXiv:2506.01648v2 [cond-mat.str-el], 27 Mar 2026.

## Reused shared kernel
`~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`
(the FIRST loop-current kernel of the Textures-100 set; originally built for
Fernandes-Birol-Ye-Vanderbilt, "Loop-current order through the kagome looking
glass", arXiv:2502.16657).

### Directly reused (unmodified, imported by path)
- `KagomeModel` geometry: primitive vectors A1,A2,A3; sublattice offsets TAU;
  reciprocal vectors B1,B2; high-symmetry points Gamma, M, K.
- Closed-form 3x3 NN Bloch Hamiltonian + Peierls-flux machinery
  (`hamiltonian`, `eig_grid`, `bands`, `dos`, `all_eigvals`).
- `gap()` — direct gap between the two lower bands.
- `chern_number()` — single-band Fukui–Hatsugai–Suzuki plaquette method.
- `bond_current_and_charge()` — Re = bond charge (CBO), Im = loop current (LCO).
- `triangle_flux_from_config()` — 3Q vs 2Q vs 1Q magnetic-multipole classification.

### Added for Zhan2025 (in `code/replicate_zhan2025.py`)
- `FoldedKagomeLCO`: a 12-site (2×2 supercell) kagome tight-binding model that
  carries an **imaginary (loop-current) bond order** on both 1nn and 2nn bonds
  in the 3Q pattern, reproducing Fig 3(d) (Δ_1nn=0.1t, Δ_2nn=0.15t → full gap,
  total Chern C=1). Includes a non-abelian multiband FHS Chern routine for the
  occupied subspace and a folded-BZ gap scan.
- Landau-quartic minimizer for Eq.(2) (`claim_D_landau_3Q`).

## Out of scope (honestly not reproduced)
The paper's central methodological result — the **unbiased FRG phase diagram**
(Fig 2) obtained from a truncated-unity FRG code on HPC (NHR@FAU) — is NOT
reproduced. It requires a dedicated FRG implementation and large compute. We
replicate the paper's **downstream single-particle electronic-model claims**,
which are its concrete falsifiable outputs (spectrum, gap, Chern number, Landau
selection, TRS breaking). See extraction/marker.md and failure_analysis.md.

## Environment
- python3 /usr/local/bin/python3, numpy 2.4.3, macOS (CherryRd).
- No network, no paid endpoints. Full run ~ seconds.
