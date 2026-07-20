# Extraction — jaubert2016 (Marker interim)

**Paper:** *Monopole holes in a partially ordered spin liquid*, L. D. C. Jaubert, arXiv:1602.02707v1 [cond-mat.str-el], 8 Feb 2016 (OIST).

**Extraction status:** Marker/Nougat GPU pipelines not invoked in this fast-path run.
This is a `pdftotext -layout` interim extraction (1004 lines) plus a curated header of
the physics that drives the replication. The clean working text used for replication is
`work/textures-spin-jaubert2016.txt` (1626 lines).

## Headline claim (replication target)
Dipolar interactions in the Fragmented Coulomb Spin Liquid (FCSL) produce an **effective
magnetic Coulomb interaction** between topological defects with dimensionless form

> V/D = -(8√2 / 3√3) (r_d / r)  ≈ -2.17732 (r_d/r)

with nearest-neighbour value V_nn = -(8/3)√(2/3) D.

## Core physics
- **Lattice:** Ising spins on the pyrochlore lattice (corner-sharing tetrahedra); local
  <111> easy axes; each spin shared by one "up" and one "down" tetrahedron.
- **FCSL:** all tetrahedra are single monopoles crystallized in a **zinc-blende** pattern
  on the dual diamond lattice — "3-in-1-out" on one sublattice, "3-out-1-in" on the other.
- **Moment fragmentation (Helmholtz decomposition):** the 3-in-1-out moment splits into a
  **divergence-full** part (long-range all-in-all-out charge order → Bragg peaks) plus a
  **divergence-free** part (Coulomb spin liquid → pinch-point diffuse scattering).
- **Pseudo-magnetization** ρ = (1/N)Σ Sᵢ·eᵢ takes the ladder values {0, 1/2, 1} for
  spin-ice (2-2) / FCSL (3-1) / all-in-all-out (4-0).
- **Defects:** "2-in-2-out" (monopole holes, break divergence-full order) and "4-in/4-out"
  (monopoles, break divergence-free Coulomb field) are excitations out of the FCSL.
- **Dumbbell energetics (Eqs. 12-13):** ΔE_hh ≈ -2p_h - 4.73D, ΔE_mm ≈ -2p_m + 19.75D;
  Monte-Carlo -4.34D and +19.70D.
- **Structure factor (Fig. 10):** Bragg peaks (Spin-Flip channel, charge order) coexist with
  pinch points (Non-Spin-Flip / total, Coulomb fragment) down to the ordering transition.

See `_pdftotext.txt` for the raw layout extraction.
