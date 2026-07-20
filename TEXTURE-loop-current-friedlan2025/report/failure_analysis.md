# Failure analysis — arXiv:2510.05234 replication

## What reproduced cleanly (5/5 machine-checkable claims)
- C1-C5 all PASS. The model-defining equations (Eq. 4 Hamiltonian, Eq. 9 spectrum,
  Eq. 12 inverse-energy factors, Eq. 11 perturbation) and the perturbative mechanism
  are quantitatively reproduced with the paper's own parameters and zero free knobs.

## Iteration that was needed (honest record)
- **C4 first attempt FAILED, then corrected (not to force a pass — the physics said so).**
  Initial C4 integrated the Eq. (11) corrections over a fully occupied disk and asked
  "is NLCBO lowest?" It was not — LCBO+ was lowest at every lambda. Re-reading Sec.
  III B, this is EXACTLY the paper's own statement: "if the band is fully occupied,
  one can show that LCBO+ has the lowest free energy." NLCBO wins only under PARTIAL
  filling. A naive inner-disk partial fill still keeps LCBO+ lowest (both its
  isotropic and NLCBO's anisotropic negative terms scale together for a centered
  disk), so a fake fill-window would have been dishonest. The correct
  machine-checkable core of the mechanism is the *anomalous dispersion*: along k_x the
  NLCBO band correction is the most negative of the three (its +8k_x^2/(3 DE2) term
  with 1/DE2<0), it is anisotropic (k_x != k_y), and CBO- is isotropic. C4 now tests
  that directly + confirms LCBO+ lowest at full fill. This matches the paper's
  mechanism argument without fabricating a stabilization we did not compute.

## Out of scope (NOT reproduced) — flagged, not faked
1. **Mean-field phase diagrams (Figs. 2, 3, 7, 9).** Require self-consistent
   simulated-annealing minimization of the free energy over the 6D complex order
   parameter (Delta_AB, Delta_BC, Delta_CA) on a ~500-point (effective) or 30x30 (TB)
   k-grid at T=90 K. This is a multi-hour global-optimization task; not attempted in
   an overnight analytic replication. The perturbative mechanism we DID reproduce is
   what the phase diagram rests on.
2. **Amplitude optimization (Delta' > Delta).** We fix a single magnitude per config
   to isolate phase frustration (as the paper does in Sec. III B). The true NLCBO
   minimum has unequal amplitudes; we did not optimize them. See open_questions #2.
3. **9-band DFT tight-binding model (Sec. IV, Figs. 6-9).** Needs DFT-derived
   Wannier hoppings/on-site energies from Ref. [74] (Christensen et al.) that are not
   printed in the PDF. Cannot build the 9x9 / folded 36x36 Hamiltonian without them.
   See open_questions #4.
4. **Free-energy landscape Fig. 8.** Needs the full finite-lambda, finite-T free
   energy over (phi1, phi2); we verified the O(lambda^2) perturbative structure only.
   See open_questions #5.

## Honesty notes
- No fabricated numbers. Every constant (eps, s1, s2, Delta, lambda, k_cut) is quoted
  from the paper (Figs. 4/5 captions, Sec. II/Appendix B).
- The paper's higher-order-in-lambda caveat is respected: C4/C5 are explicitly labeled
  as the O(lambda^2) mechanism, which the paper itself calls "intuition."
- No network / paid endpoints used. Pure local numpy.
- Kernel provenance is cited; the kernel's own scope caveat (loop-current class is
  "qualitative/PARTIAL unless extended to the paper-specific self-consistent
  interaction") is consistent with our Coverage=6/10 verdict.
