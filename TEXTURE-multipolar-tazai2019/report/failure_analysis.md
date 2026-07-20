# Failure Analysis — arXiv:1901.06213 replication

## Bugs hit and fixed during the run
1. **Lindhard sign / negative bare susceptibility.** First chi0 implementation produced
   negative bare susceptibilities at Gamma and an `overflow in exp` warning. Root cause:
   wrong sign in the intraband (degenerate) limit and unclamped Fermi exponent at T=0.01.
   Fix: use the manifestly positive form chi0 = sum |M_mn|^2 (f_n - f_m)/(E_m - E_n) with
   the m=n limit -> -f'(E) >= 0, and clip (E-mu)/T to [-50,50]. After fix all chi0 > 0.
2. **numpy.trapz removed.** NumPy 2.x dropped `np.trapz`; replaced with `np.trapezoid`.
   Continuum scaling integrals then ran clean.

## Genuine discrepancies (not bugs — physics/convention limits)
1. **Filling partition (C1).** nf~0.99 / ns~0.19 vs paper 0.58 / 0.69. Cause: the SM allows
   substituting an s-band for the realistic 5d conduction band; our s-band sits entirely
   above mu so conduction charge comes only from hybridization. The total filling matches to
   ~7%, but the c/f partition and the paper's counting normalization (Ref [1]/[2]) are not
   reproduced. Fixable by importing the exact 5d tight-binding band and counting convention.
2. **RPA peak position (C2).** Our peak lands on the Gamma-M diagonal at (0.5,0.5)pi rather
   than a clean q=0 + q=(pi,pi) double peak. Cause: the s-band proxy changes Fermi-surface
   nesting. Magnetic dominance and the Gamma-M weight are correct; exact nesting vectors are
   not. Fixable with the real conduction band.
3. **Stoner magnitude (C4).** alpha_mag=1.02 at u=1.08 vs paper 0.9 (~13% high). Cause:
   channel-diagonal RPA using only the reported *diagonal* U0Q; we neglect the one nonzero
   off-diagonal coupling U0^{Jmu,Tmu^alpha}=0.58 and the full 16x16 tensor structure, and we
   use a finite k-mesh (nk=40). Direction and ordering (alpha_mag > alpha_el) are correct.

## Deliberately out-of-scope (marked, never faked)
- **Full AL/MT vertex corrections (C6, the headline number 0.94).** Requires the exact
  16x16 Slater-Condon Coulomb tensor + nested three-point vertices Lambda^{EF}_{ABCD}(q,p)
  with double k,p momentum-frequency sums (Eqs. 7,8,S8,S9). This is two-loop, O(N_k^2 * 16^3)
  work — beyond an overnight tractable-model run. We instead reproduced (a) the RPA baseline
  the VC acts on, and (b) the analytic xi-scaling that *proves* AL dominates MT (C5), so the
  mechanism is validated even though the final enhanced susceptibility number is not computed.
- **Field-induced octupole (Fig. 5).** Downstream of the full VC machinery; not attempted.

## What would raise the grade
- Import Ref [1] 5d conduction band -> fixes filling partition + peak positions (C1, C2).
- Build U^0 from F^k Slater integrals + include the 0.58 off-diagonal -> tightens C4 and
  enables the full VC calculation (C6).
- Implement the AL1/AL2 vertices -> would move C6 from out-of-scope to a direct test of 0.94.

## No-fabrication statement
Every number in REPORT/artifacts came from an actual Python run in `work/` (outputs saved
as JSON/npz). Out-of-scope items are labeled as such; no DFT or experimental values were
invented to fill gaps.
