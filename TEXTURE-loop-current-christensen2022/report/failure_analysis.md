# Failure analysis — christensen2022

## What was replicated (the reproducible core)
The coupled iCDW–rCDW Landau free energy (Eqs. 10–13) constructed from scratch,
minimized numerically, phase diagram mapped. Both generic mixed phases (3Q-3Q,
2Q-1Q) reproduced as global minima; pure-iCDW exclusion and 2Q-1Q orthorhombicity
confirmed. This is the paper's central phenomenological claim and it holds.

## What was deliberately skipped (out of scope / time budget)
1. **DFT electronic structure of CsV3Sb5.** The VHS band structure at M
   (p-type/m-type sublattice polarization, dz2/dxz/dyz orbital character) was not
   computed. We take the *existence* of the M-point order parameters as given and
   test only the Landau energetics — as instructed (skip DFT).
2. **Group-theory derivation of the seven iCDW irreps.** We use the free-energy
   form the paper derives (mM2+/mM3+/mM4+ all reduce to the same F), but did not
   independently classify the Bloch-state symmetry content. Hence the "seven
   distinct iCDW types" and the ferro/octupolar/toroidal/monopolar subsidiary
   orders are cited, not re-derived.
3. **SOC-induced SDW back-reaction** not included in the minimized F.
4. **Out-of-plane (kz) modulation / interlayer coupling** not modeled.

## Limitations of the Landau minimization
- Higher-order coefficients (u, λ, γ, κ) are **chosen**, not derived from a
  microscopic model. We demonstrate that *disjoint regions of coefficient space*
  give the two generic phases (Scenario A → 3Q-3Q, Scenario B → 2Q-1Q), which is
  the paper's qualitative statement; we do NOT claim the physical AV3Sb5 point.
- First tuning attempt: Scenario A initially still landed in 2Q-1Q (biquadratics
  too strong). Fixed by lowering λr, λi, λ_ir(1) and raising γ_ir, γ_r — the
  physically correct lever (trilinear reward vs biquadratic co-location penalty).
  This is documented, not hidden.
- Nelder–Mead multistart: global minimum found by seeding all candidate phases;
  no continuation/annealing. Robust here (clean, low-D landscape) but not proven
  exhaustive.

## No fabrication
All numbers in the result JSON and report come from actual execution of
`christensen2022_landau.py` (runtime ~28 s). No DFT numbers, band energies, or
experimental values were invented.

## Net verdict
**REPLICATED** for the Landau-theory core; **PARTIAL** if the full paper
(DFT + group theory + magneto-response tensors) is the yardstick.
