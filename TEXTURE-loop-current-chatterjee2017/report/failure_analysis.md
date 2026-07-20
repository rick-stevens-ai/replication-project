# Failure analysis — arXiv:1705.06289 replication

## Scope mismatch (the big one — flagged, not faked)
- **Shared kernel is kagome; paper is square-lattice.** The provided
  `loop_current_kagome_kernel.py` implements kagome Peierls-flux tight-binding
  (Chern insulator, Dirac cones, Berry curvature). This paper is a
  square-lattice SDW mean-field / SU(2) gauge theory. The kagome Bloch
  Hamiltonian, Chern numbers, and multi-Q kagome textures are **physically
  irrelevant** to this paper — reporting kagome Chern numbers as a "replication"
  would be fabrication.
- **Resolution:** reused only the transferable concept (real=charge /
  imag=loop-current bond-bilinear decomposition) and rebuilt the paper-specific
  core (Eqs. B4-B6, C14). Documented in `code/PROVENANCE.md`.

## Paper has no numeric tables to hit
- 1705.06289 is a theory/symmetry PLL: its "results" are phase diagrams (Figs.
  2,3) and symmetry tables (I, II), not tabulated numbers. So the replication
  targets **structural/qualitative claims with quantitative internal checks**
  (analytic gap = h; self-consistent h(U) asymptotics; energy ordering; current
  vanishing for collinear order) rather than matching a printed value.
- The paper does **not tabulate the tp hopping values** used for Figs. 2/3 in
  the extracted text; a cuprate-like stand-in set was used for the energetic
  checks (C2, C4). This weakens C2/C4 from "exact match" to "correct ordering
  with a physically reasonable band". Logged as open questions 1 & 2.

## Bugs hit and fixed during the run
1. **numpy-bool not JSON serializable** (Python 3.14 / numpy 2.4): `results`
   dict contained `np.bool_` from comparisons -> `json.dump` TypeError. Fixed
   with a `_san()` recursive sanitizer casting np scalars to python types.
   (Checks themselves had already completed and printed 5/5 before the crash.)

## Soft / partial results (honest)
- **C4 electron side:** the single-cut (Kx, pi) fixed-h scan returned a mildly
  incommensurate best-K on the electron-doped side too, whereas the paper says
  the electron side stays coplanar/commensurate. The hole-side claim (the
  paper's actual particle-hole-asymmetry point) is clean; the electron-side
  artifact is attributed to not co-optimizing theta and full 2D K. Open q. 5.
- **C5 non-collinear current is small** (6.5e-4): finite and nonzero (the
  qualitative claim), but the magnitude depends on the chargon Zij
  renormalization we did not implement. We assert only the robust,
  model-independent part: collinear -> exactly zero, non-collinear -> nonzero.

## No fabrication statement
Every number in `work/results.json` is produced by running `sdw_meanfield.py`.
No values were hand-tuned to pass. Out-of-scope kernel machinery was excluded
rather than repurposed to manufacture agreement.
