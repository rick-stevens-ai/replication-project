# Failure Analysis — xie2025

## Verdict: REPLICATED (with honestly-scoped limitations)

## What was fully replicated
- **Free-energy minimization (Eq. 2):** equilibrium |Δ_Q| matches the analytic
  iCDW value √((b+λ1')/2(u1+2u2)) = 1.41421 to 7 sig figs; phase selection
  θ0=±π/2 (iCDW) vs 0/π (rCDW) confirmed.
- **Mode mixing (Eq. 10):** the A-channel off-diagonal coefficient
  (3/2)λ2 sin(3θ0)|Δ_Q| is nonzero (−0.2121) for iCDW and exactly zero
  (~1e-17 float noise) for rCDW — the paper's central qualitative claim.
- **Closed-form spectrum (Eq. 12):** numerical diagonalization of the dynamical
  matrix reproduces Eq. (12) to **4.4e-16** — quantitative agreement at machine
  precision.
- **Microscopic picture:** shared kagome kernel confirms zero net loop order at
  real hopping (φ=0) and finite loop-current susceptibility to imaginary flux.

## What was NOT attempted (and why)
- **NV-center T1 / stray-field estimate (Eqs. 13–15):** requires unspecified
  material geometry, NV standoff distance, and absolute loop-current magnitude.
  The paper itself gives only a qualitative Fermi-golden-rule scaling, so a
  faithful quantitative number is not derivable from the excerpt. Flagged as
  open question #1 rather than fabricated.
- **Finite-q dispersion:** we reproduced the q=0 (M-point) result the paper
  states; the schematic Fig. 3(b) dispersion at finite q was not mapped
  (open question #2).
- **E-channel modes:** the paper notes E1/E2 modes remain decoupled by C3; we
  verified the A-channel mixing (the headline) but did not separately diagonalize
  the E sector.
- **Landau damping / RPA electron dressing:** the phenomenological modes are
  undamped; coupling to the VHS particle-hole continuum (open question #3) was
  not included.

## Sources of residual numeric error
- rCDW off-diagonal (~7.8e-17) and cross susceptibility (~2.9e-18) are pure
  floating-point round-off; analytically they are exactly zero because
  sin(3θ0)=sin(3π)=0. This is the *correct* symmetry-protected result, not a
  discrepancy.
- iCDW |Δ_Q| differs from analytic by ~2e-8 (grid refinement tolerance);
  negligible.

## Honest assessment
The theoretical headline — phase–amplitude mode mixing in iCDW, decoupling in
rCDW, with the Eq. (12) spectrum — is a self-contained algebraic/mean-field
result and is **fully and quantitatively reproduced**. The experimental
NV-detection proposal is a separate, less-specified layer that is scoped out
rather than guessed.
