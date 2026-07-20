# Failure analysis — nakazawa2024

## Verdict: PARTIAL

## What was reproduced (successes)
1. **Finite uniform M_orb in the triple-Q cLC state.** A purely imaginary NN
   hopping with fixed triangle chirality breaks global TRS and yields a nonzero
   itinerant orbital magnetization (M_orb ~ −5×10⁻⁴ at η=0.01), confirming the
   basic mechanism.
2. **Giant impurity suppression, correct magnitude.** A single unitary-limit
   (I=100 eV) vacancy at ~0.9–1% density suppresses M_orb by 10%→83% depending
   on η, with a mean R ≈ 49% at 1%. This corroborates the headline "R can exceed
   50% with ~1% impurities" — at small η our R is well above 50%.
3. **Independent implementation.** The result comes from a from-scratch real-space
   model + the modern-theory itinerant L_z operator, i.e. the very "nonlocal
   itinerant circulation" the paper credits, not a re-run of the authors' code.

## What failed (honest)
1. **η-insensitivity NOT reproduced.** The paper's central surprise is that R is
   *insensitive* to η (defeating R ∝ πξ_J²). Our model shows R *decreasing*
   monotonically with η (83%→9.5% as η goes 0.005→0.08; relative spread ~0.61).
   Our finite open flake reproduces the *naive* expectation the paper argues
   against — meaning we are capturing the local suppression but NOT the nonlocal
   long-range circulation that flattens R(η) in the full periodic supercell.
2. **Clean M_orb ~ η³ scaling NOT reproduced** (we get exponent ~0.3). The η³ law
   is a momentum-conservation selection rule (b100=b010=b001=0) that requires the
   exact triple-Q sign pattern and precise VHS filling; our distance-based
   chirality assignment and integer filling snap are too coarse.
3. **Size scan is noisy** (R even changes sign at some N). Small flakes with hard
   open boundaries and an integer occupied-state count produce shell-filling
   artifacts, so single-impurity→1% extrapolation is only order-of-magnitude.

## Root causes
- **Open flake vs. periodic folded-BZ supercell.** The paper uses 12-site 2×2
  cells tiled to N≤1200 with a 512² k-mesh and the k-space bulk+edge M_orb formula
  (Eq. 4). A finite open flake truncates exactly the long-range/edge circulation
  that makes R nonlocal and η-insensitive. This is the single biggest gap.
- **cLC sign pattern approximated.** We assign ±iη by sublattice cyclic order, not
  by the paper's explicit Fig-2 up/down-triangle triple-Q geometry.
- **Single-orbital, non-self-consistent.** Only the b3g sector; η is imposed, not
  solved from the density-wave equation; b2g neglected (as in the paper).
- **No finite-T Fermi weighting / VHS resolution.** Integer filling snap misses the
  n=2.55, |μ−μ_vHS|~max(2η,T) satellite structure that shapes M_orb(η).

## What would fix it (see open_questions.json)
Port M_orb to the periodic supercell + Eq.-4 k-space formula with a ≥64² folded-BZ
mesh, encode the exact Fig-2 triple-Q sign pattern, and use a finite-T Fermi
function at μ=0 — this is expected to recover both the η³ clean law and the
η-insensitivity of R.

## Not fabricated
All numbers come from `report/evidence/nakazawa2024_result.json`, produced by
`nakazawa2024_replicate.py`. Where the model disagrees with the paper we report the
disagreement rather than tuning to match.
