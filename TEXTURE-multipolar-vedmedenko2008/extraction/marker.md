# Extraction marker — vedmedenko2008

- **Paper**: E. Y. Vedmedenko, S. Even-Dar Mandel, R. Lifshitz, "In search of multipolar order on the Penrose tiling", arXiv:0805.1216v1 [cond-mat.mtrl-sci], Phil. Mag. (2008).
- **Source PDF**: `textures-multipolar-vedmedenko2008.pdf`
- **Extraction method**: `pdftotext -layout` (interim), see `nougat.mmd` for the header-normalized markdown interim.
- **Pages**: 11. **Method**: Monte Carlo, classical multipolar rotors on rhombic Penrose tiling.

## Headline claim (extracted)
> For odd-parity multipoles (dipole l=1, octopole l=3; m=0) on the Penrose tiling, the apparent decagonal Hexagon-Boat-Star (HBS) superstructure does **not** indicate true long-range order. All cases studied show only **short-range order**; the observed superstructure arises from short-range head-to-tail attraction along thin-rhombus short diagonals, and long-range orientational order is destroyed by 3-body frustration where chains meet.

## Model
- Hamiltonian: full long-range multipolar interaction in spherical coordinates, Eqs. (1)–(2), no cutoff.
- Rotors: Q_l0, l=1..4, m=0. Odd parity (l=1,3) behave as arrows (head-to-tail); even parity (l=2,4) as double-headed arrows.
- Lattice: vertices of finite rhombic Penrose tiling patches, open BC, up to 1000 moments.
- Algorithm: continuous-angle MC, extremely slow annealing (up to 150 T-steps), local fields updated on accepted moves, two-seed equilibration check.

## Extraction confidence
High for text/claims/model; figures (Figs. 1–3) not machine-parsed (raster). Equations transcribed from text layer.
