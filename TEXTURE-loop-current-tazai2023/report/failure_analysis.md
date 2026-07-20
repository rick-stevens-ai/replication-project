# Failure Analysis --- Tazai-Yamakawa-Kontani replication (PARTIAL)

## Summary
The qualitative headline mechanism reproduces cleanly; the **quantitative** GL
power laws and the bond-order **enhancement** do not. This document lists what
failed, the most likely cause, and the fix.

## F1. Current-only power law: slope 1.31, expected 3.0
- **Observed:** log-log fit of |M_orb| vs eta over eta in [0.005,0.03] gives 1.31.
- **Likely cause:** (a) coarse 24x24 mesh -> M_orb (~1e-4) has k-sampling noise of
  the same order (see F4); (b) our loop-current form factor is a geometric
  triangle-circulation proxy, not the exact TYK f_ij site-by-site assignment, so a
  small spurious lower-order (linear) component leaks in and dominates the fit at
  small eta. The genuine b111 (eta^3) term is subleading in our proxy.
- **Fix:** hard-code the exact f_ij from the paper (sites 1,2,4,5 = +i; 7,8,10,11
  = -i for q1, and the q2,q3 analogues) so that 1Q/2Q band-M_orb vanish exactly;
  then the residual is pure b111 and the slope should approach 3.

## F2. Bond order suppresses M_orb (x0.5) instead of enhancing it
- **Observed:** at eta=0.02, |M_orb| with phi=0.02 is 0.52x the current-only value.
- **Expected:** TYK Fig. 2(d): strong ENHANCEMENT, M_orb becomes linear via
  m1*phi*eta with m1 sizable and the trilinear term dominant.
- **Likely cause:** (a) wrong relative sign/normalization between our even-parity
  bond form factor g_ij and the current f_ij, so the trilinear channel partly
  cancels rather than adds; (b) filling mismatch --- Fig. 2(d) is at n=2.47, we
  evaluated at n=2.55.
- **Fix:** implement the exact star-of-David g_ij (Fig. 1a) and evaluate at n=2.47;
  extract m1 by fitting M_orb = m1 phi eta + m2 eta^3.

## F3. 2Q band-M_orb does not vanish (2Q/3Q = 2.7)
- **Observed:** geometric net flux for 1Q/2Q DOES cancel (1Q ~ 1e-19), but the
  band-theory M_orb for 2Q is larger than 3Q.
- **Likely cause:** the interband M_orb formula is sensitive to the exact
  form-factor parity; our triangle-circulation proxy breaks the exact TRS+
  translation symmetry that forces 2Q -> 0 in the paper. The geometric diagnostic
  (which uses the clean flux definition) behaves correctly, confirming the issue
  is in the band-theory form factor, not the physics.
- **Fix:** same as F1 --- exact f_ij restores the symmetry that zeroes 1Q/2Q.

## F4. Numerical noise ~ signal
- M_orb ~ 1e-4; odd-in-eta residual |M(+eta)+M(-eta)| ~ 1e-4 (same order).
- **Cause:** coarse 24x24 mesh (chosen deliberately for the <3 min perf budget)
  plus finite-mu bisection tolerance. The interband denominator
  |e_a-e_b|^-2 amplifies near-degeneracy k-points.
- **Fix (out of perf budget here):** >=48x48 mesh + mu converged to <1e-6 +
  small broadening of near-degenerate denominators.

## What is NOT a failure (reproduced correctly)
- Finite M_orb ~ 1e-4 mu_B for the 3Q state, matching the paper's magnitude range.
- Geometric flux non-cancellation: 3Q net flux 5.4e-2 vs 1Q ~ 0 (Fig. 2c "J != J' != J''").
- Field coupling dF = -3 h_z M_orb with correct sign; h_z=1e-4 <-> 1 T identification;
  domain-switch gain 6 h_z M_orb ~ 8.2e-8 per 3-site cell -> tiny field aligns chirality.

## Bottom line
Verdict **PARTIAL**. Named gap: the quantitative GL power laws (eta^3 current-only,
linear-with-bond) and the bond-order enhancement coefficient m1 are not
reproduced, traced to a geometric-proxy loop-current form factor + coarse mesh.
The core physical claim --- 3Q chiral current has finite orbital magnetization and
a ~1 T field can switch the chiral domain --- is reproduced qualitatively with the
correct sign and order of magnitude.
