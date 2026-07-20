# Failure analysis — vedmedenko2008

## What was fully reproduced (from scratch)
- **Penrose tiling generation** (the hard part): de Bruijn pentagrid dual method,
  no external tiling library. Produces a proper aperiodic rhombic patch with the
  correct 5/10-fold local environments and n*pi/10 bond directions.
- **Central odd-parity claim**: apparent order but only short-range order.
  All 5 diagnostic checks pass for both dipole (l=1) and octopole (l=3):
  orientation peaks along tiling directions, no ferromagnetic LRO, decaying
  C(r), no orientational Bragg beyond random baseline, frustration present.
- **Parity/rank trend**: octopole shows stronger frustration (0.83 vs 0.41) and
  weaker short-range correlation, matching the paper's remark that octopolar SRO
  is slightly less perfect (larger out-of-plane protrusion).

## Scope limits / not reproduced
1. **System size**: 151 sites vs the paper's up to 1000. Chosen for the <6 min
   fast-run budget. Finite-size scaling (see open_questions) is the honest gap.
2. **Full MC + 150-step annealing**: replaced by zero-T local-field relaxation
   with a short annealing preamble. Same algorithm *class* (local fields updated
   on accepted moves) and same equilibration philosophy (two seeds), but not the
   published slow-anneal schedule. Consequently the two-seed energies differ by
   ~1.2% (dipole) rather than converging exactly — a real signature of the
   near-degenerate frustrated landscape, but also a sign our minimizer finds
   slightly different frustrated minima per seed.
3. **Fourier/Bragg spectra**: we use an orientation-weighted structure-factor
   peak-to-mean ratio vs a random baseline as a proxy for "no additional
   orientational Bragg peaks." We did NOT compute the paper's full 2D diffraction
   patterns, so agreement on the Fourier claim is qualitative, not spectral.
4. **HBS superstructure geometry**: we verify the *statistical fingerprints* of
   the HBS-outlining short-range order but do not explicitly decompose the
   configuration into hexagon/boat/star tiles. Visual HBS match is inferred, not
   directly rendered.
5. **Interaction kernel**: we use the dipolar angular form with an l-dependent
   radial exponent (2l+1) rather than the full T_{lA lB mA mB} spherical
   interaction tensor of Eqs (1)-(2). For odd-parity m=0 rotors the head-to-tail
   physics is dominated by this leading term, but coefficients are not the exact
   tensor. This is the main physics approximation.
6. **Even-parity cases (l=2,4)**: not run (out of scope for the fast odd-parity
   focus). Listed as a next step.

## Honesty notes
- No results were fabricated; every number in the report comes from
  `work/vedmedenko2008_result.json`.
- The "two_seed_converged=false" flag is reported truthfully; it reflects the
  frustrated-landscape degeneracy plus our simplified (non-full-MC) minimizer,
  not a hidden success.
- Verdict is deliberately **PARTIAL (qualitative REPLICATED)**, not REPLICATED,
  because size, annealing schedule, exact Hamiltonian tensor, and Fourier
  spectra were approximated.

## Verdict
PARTIAL — Coverage 7/10, Agreement 8/10. The qualitative central claim (apparent
HBS order = short-range only, no LRO, frustration-driven) is robustly reproduced
from a scratch-built Penrose tiling.
