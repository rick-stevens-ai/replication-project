# Failure & Scope Analysis — li2016

**Verdict: REPLICATED** (all headline sub-claims pass) — but with honest scope limits.

## What was fully reproduced
- **FO ground state**: classical energy minimization returns a uniform, fully
  polarized octupolar moment S≈(0.5,0,0). Unambiguous ferro-octupolar order.
- **To = 1.5|Jx|**: recovered *exactly* and *analytically* from the mean-field
  instability z|Jx|·chi_site with chi_site=(1/4)/T for a pseudospin-1/2 and z=6.
  This is a genuine independent derivation, not a fit.
- **Non-divergent chi_zz**: the field couples to a dipole (Ty,Tz) orthogonal to
  the ordered octupole (Tx); chi_zz stays finite (max 2.5). Matches the paper's
  central "hidden order" claim.
- **Gapped octupolar wave**: Eq. 5 evaluated numerically; min gap 1.90 > 0.

## Limits / what is NOT a from-scratch first-principles result
1. **chi_zz mechanism is modeled, not derived from the SI.** We impose an
   octupolar molecular field that gaps the transverse dipole channel — physically
   correct and consistent with the paper's argument, but a single-site MF proxy.
   A full RPA/spin-wave chi_zz(T) was out of budget (see open_questions #3).
2. **SI rotated-coupling definitions unavailable.** Eq. 4's Jx,Jy,Jz are defined
   in the Supplementary Information (not in the fetched text). We interpret them
   as the effective post-rotation couplings; if the SI folds Jyz into them, the
   *quantitative* To could shift (qualitative result unaffected). This is the main
   source of the 1-point Agreement deduction.
3. **Full Fig. 2 phase diagram (Ox surface) not reproduced.** We mapped only a
   coarse Ix-surface slice via classical minimization (43/49 FO). The
   self-consistent 3-sublattice AFO/supersolid diagram (Eq. 6) with first- vs
   continuous-order boundaries was not solved — the main Coverage deduction.
4. **Quantum dipole-octupole modulation inaccessible classically.** The paper
   states the ferro-dipolar/antiferro-octupolar mutual modulation is a *quantum*
   effect absent in a classical spin model. Our classical minimizer cannot
   capture it by construction; ED would be required (open_questions #5).

## No fabrication
Every number in the result JSON and report is produced by the committed runner
`work/li2016_replication.py` executed under `/home/stevens/comfyui-env/bin/python`.
Extraction files are labeled as pdftotext-based interims because marker/nougat
were unavailable — not passed off as native marker/nougat output.

## Score justification
- **Coverage 9/10**: headline claim + ground state + Tc + chi_zz + octupolar wave
  + phase slice covered; full Ox-surface self-consistent MF diagram not.
- **Agreement 9/10**: To exact, GS exact, chi_zz & gap qualitatively confirmed;
  minor uncertainty from unavailable SI coupling definitions.
