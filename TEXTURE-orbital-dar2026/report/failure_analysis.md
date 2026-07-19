# Failure / gap analysis — dar2026

**Verdict: PARTIAL.** The proximity-induced triplet-generation mechanism
reproduces; the paper's defining altermagnet signature does not.

## SINGLE most important caveat (verdict-capping)
**The discriminating headline claim — a fourfold angular hotspot modulation that
is UNIQUE to the altermagnet and VANISHES in the antiferromagnetic limit
(rho_z=0) — is NOT reproduced.** Our on-wall angular modulation is 0.119 (AM) vs
0.122 (AFM), and the fourfold (l=4) Fourier power is 2.88e-11 (AM) vs 3.00e-11
(AFM). These are essentially identical, i.e. the AM and AFM triplet angular
patterns look the same in this implementation. The paper's Fig. 4(a) vs 4(b)
requires the fourfold pattern to appear ONLY when rho_z != 0.

Physical read: in our discretized effective Hamiltonian the on-wall angular
structure is dominated by the emergent SOC alpha ~ rho_3 * phi'(r) * r_hat, which
is present in BOTH the AM and AFM limits (it survives at rho_z=0). The
altermagnet-ONLY emergent Zeeman field V_z ~ rho_z * phi'(r)^2 * cos(2*chi) — the
term that is supposed to imprint the d-wave fourfold pattern — contributes a
change of <=3% and does not rise above the SOC-induced background. So we see the
common (SOC) part of the physics but not the distinguishing (V_z) part.

## Compounding caveat: difference of small numbers
The equal-spin triplet is only ~0.4% of the singlet amplitude
(sqrt(I_t)/psi_s ≈ 0.0038). The AM-vs-AFM contrast the paper hangs its headline
on is therefore a difference of two very small, nearly equal quantities
(replication-skill pitfall 8). Even if a genuine fourfold AM component exists, at
this dynamic range we cannot cleanly separate it from numerical/discretization
background. Any quantitative AM signature must be established with far more
triplet-channel dynamic range before it can be trusted.

## What reproduced (high confidence)
1. **Wall localization of triplets** — I_t localization fraction 0.99 (both AM and
   AFM). Matches Eq. (15): alpha_p ~ phi'(R) vanishes off the wall, so triplet
   generation is confined to the wall. Clean, unambiguous.
2. **Spin-resolved angular anisotropy** — I_t_up peaks near chi=+/-pi/2, I_t_dn
   near chi=0,pi (evidence keys `angular_It_up_AM`, `angular_It_dn_AM`), matching
   the paper's Fig. 4(c) description.
3. **Sanity/physics checks** — hermiticity residual exactly 0.0; BdG spectrum
   gapped at min|E| = 5.1e-4 eV ~ Delta_0; finite singlet (2.44e-3). The model is
   built and diagonalized correctly.

## What did NOT reproduce / not attempted
- **Fourfold AM-only modulation** (the discriminator): FAIL — see above. This is a
  real shortfall of the current implementation, not merely scoped out.
- **Supercurrent-induced quadrupolar torque (Sec. VII):** NOT ATTEMPTED. Requires
  the finite-Cooper-pair-momentum BdG (Eq. 17, Delta -> exp(iQ.R)Delta) and the
  torque functional tau = <dH/dn>.J_s. EXPECTED scoped-out gap — coverage-capping,
  not a failure of what was built.
- **Momentum-resolved node structure (Fig. 3):** NOT ATTEMPTED. Our real-space
  bond-correlator proxy for Eq. (16) integrates over p and cannot show the
  circle->ellipse node deformation that actually carries the hotspot pattern. This
  is likely WHY claim 2 fails here: we measured the wrong (p-integrated) object to
  see a p-space anisotropy effect.
- **Nodal <-> fully-gapped transitions around the wall:** NOT ATTEMPTED (single
  global min|E| only).

## Likely root cause (best current hypothesis)
The fourfold pattern is a MOMENTUM-SPACE anisotropy (spin-dependent elliptical
node condition, paper Eq. after 15) that becomes an angular real-space pattern
only through the p-integral in Eq. (16). Our nearest-neighbor bond intensity is a
crude, p-averaged proxy that washes out the ellipse-vs-circle distinction, and the
chosen rho_z=0.1 (vs rho_0=1.0) puts V_z's effect at the few-percent level. Both
push the AM signature below the resolution floor.

## Environment/tooling gaps (NOT physics)
- `marker` / `nougat` not installed → extraction artifacts are honest `pdftotext`
  interims with NOTE headers + regenerate commands; key equations hand-transcribed.
- `pdflatex` not installed → REPORT.tex ships as source.

## What would raise the verdict
1. Compute the momentum-resolved F_sigma-sigma(R,p) (Eq. 15) and integrate Eq. (16)
   exactly, recovering the node ellipse — the object that carries the fourfold pattern.
2. Sweep rho_z upward (toward exchange-dominated) and check the l=4 power separates
   from the AFM baseline monotonically.
3. Self-consistent Delta + finer grid to give the triplet channel dynamic range.
If (1)+(2) show a clean AM-only fourfold pattern, the verdict goes to REPLICATED.
