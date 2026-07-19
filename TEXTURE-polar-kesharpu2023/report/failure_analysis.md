# Failure Analysis — Kesharpu 2023 Replication

This document records what did **not** work verbatim, the root causes, the
mitigations applied, and the honest scope of the replication.

## 1. Inconsistent lattice-vector / Dirac-point conventions in the source
**Symptom.** First implementation used the paper's printed NN vectors
a_n (|a_n|=1: (√3/2,1/2),(−√3/2,1/2),(0,1)) together with its stated Dirac
point K=(π/√3,0). The NN structure factor `Σ exp(i k·a_n)` did **not** vanish at
that K (|Hx|=0.75 there), so the gap never closed and no topological transition
occurred → claim-1 sign agreement 0.43, zero sign flips.

**Root cause.** The manuscript (as OCR'd) mixes two sublattice conventions: the
a_n listed and the b_n listed are not the NN/NNN sets of a single honeycomb whose
Dirac point is at π/√3. Numerically the a_n structure factor vanishes at
kx≈±2.42, not π/√3. This is a convention/OCR artifact, not physics.

**Fix.** Rebuilt on ONE self-consistent standard-honeycomb convention (NN
vectors of magnitude 1/√3, NNN vectors of magnitude 1, Bravais vectors
a1=(1,0), a2=(1/2,√3/2)). This preserves the paper's *physics* exactly (Dirac
cones from NN hopping; Haldane complex NNN hopping with phase S q2·b_n) and
places the Dirac points at the true honeycomb K/K'. After the fix Hx=Hy=0 at K
and the mass Hz flips sign precisely as q2x crosses 0 → claim-1 agreement 1.00.

## 2. Fragmented OCR of Eq. (2) weight factors w_n, g_n, w'_n, g'_n
**Symptom.** The exact algebraic form of the weights in `extraction/marker.md`
is broken across lines and partly unreadable.

**Root cause.** PDF-to-markdown OCR of dense multi-line equations.

**Mitigation.** Reconstructed the weights as the standard symmetric combination
`w_n = 1/2 + 1/4 cos(q2·b_n) − (1/4 − 1/4 cos(q2·b_n)) cos(q1·b_n)`,
`g_n = (1/4 − 1/4 cos(q2·b_n))/w_n` (and the a_n analogues). Because the band
**topology** is controlled by the *sign* of the Haldane mass `sin(S q2·b)` and by
the always-positive hopping amplitudes, the reconstructed prefactors do not
affect the reproduced sign structure. They *could* shift exact phase-boundary
values (Eq. 10 gap-closing q2x) — flagged in `open_questions.json` #1.

## 3. Sign-flip counter missed the zero-crossing (claim 2)
**Symptom.** Claim-1 clearly showed the Chern number flipping −1→+1 across
q2x=0, yet the claim-2 flip counter returned 0.

**Root cause.** The counter required two *adjacent* nonzero entries of opposite
sign, but the sweep passed through an exact gap-closing point (c=0) at q2x=0
sitting between the −1 and +1 samples.

**Fix.** Count sign changes over the subsequence of nonzero Chern values
(gap-closing zeros are transition points, not separate phases). Claim-2 then
correctly reports 1 flip.

## 4. Claim 3 reframed to match the paper's HONEST conclusion
**Initial framing (rejected).** "For S≥2 the Chern number flips with the polar
angle q1x (absent at S=1)."

**Why rejected.** The numeric Chern is q1x-independent for all S=1,2,3, which at
first looked like a failure. But re-reading Sec. III A shows the paper itself
concludes the polar factor is subdominant: g_n,g'_n are "always positive and
less than unity," so `(1 + S g2/2 cos 2q1x) > 0` and "apart from small
discrepancies … the Chern number depends only on the azimuthal modulating vector
q2x." Reporting a q1x-flip would therefore have been a *misreading of the paper*.

**Fix (honest).** Claim 3 now tests the paper's actual statement: (a) the analytic
polar factor |S g2/2| < 1 in the well-defined lobe (|S q2x|<π; measured max
0.689), and (b) the numeric Chern is q1x-flat. Both hold ⇒ match. We explicitly
note that Eq. (7) formally *contains* a q1x term for S≥2 but the paper deems it
subdominant — exactly what we reproduce. (Over the FULL grid, including
near-boundary points the paper marks as ill-defined, the factor can exceed 1
[max 2.085]; this is scoped out consistent with the paper's Fig. 7 caveats.)

## 5. Terms deliberately not implemented (scope limits)
- **p(k') Fourier coefficient / eps** (Eq. 3, B9): set to 0 per the paper's own
  "p(k')≈0 over the BZ" approximation. Consequently we cannot see the narrow
  large-S sign-flip regions where `2 S eps cos(S q2x)` competes with
  `sin(S q2x)`. (open_questions #2.)
- **Half-integer-spin limiting-case Hamiltonians** (Table I, App. D): not built;
  we use continuous S and rely on the paper's continuity argument.
  (open_questions #3.)
- **S^3 effective-flux scaling**: the quantized Chern is ±1 for all S; we did not
  extract the continuous Berry-curvature magnitude that would show the S^3 trend.
  (open_questions #5.)

## Overall honesty statement
The replication reproduces the **topological structure and sign physics** of the
paper's central results (Eqs. 5, 7, 11 and the THE sign-flip) from an
independent, self-consistent numerical Chern-number computation (FHS). It does
**not** reproduce exact phase-boundary numerical values (Eq. 10) because the
exact weight factors and the p(k')/eps corrections were approximated. Verdict:
**replicated at the level of topology/sign structure (4/4 qualitative claims);
partial at the level of exact phase-boundary values.**
