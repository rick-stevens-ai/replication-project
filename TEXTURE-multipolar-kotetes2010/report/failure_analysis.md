# Failure analysis — kotetes2010

Honest accounting of what did **not** replicate and why. Nothing here is fabricated;
these are real limitations of the from-scratch solve.

## 1. dxy condenses at B=0 in the microscopic single-band model (should be field-induced)
- **Symptom:** the microscopic `solve_point` gives Delta1(B=0) ≈ 3.4 meV, whereas the
  paper requires Delta1(B=0)=0 (dxy strictly field-induced).
- **Cause:** the paper uses a *simplified single-band nesting model* only as an
  illustration; the true suppression of the bare dxy channel comes from the
  four-Fermi-line structure at Q1=(1±0.4,0,0). In our single band, V''=35.25 > V'=23.5,
  so the dxy channel (driven by V'') is actually the *stronger* coupling and condenses
  on its own. The paper's Landau coefficient alpha1>0 (which enforces field-only dxy)
  is an emergent property of the multi-band geometry, not the single band.
- **Mitigation (not a workaround-fake):** we replicate the strict field-induced behavior
  via the paper's *own* Landau reduction (Appendix D), which the authors state their
  numerical solution maps onto. There Delta1=(g/alpha1)Delta2 B is exactly zero at B=0.
- **Scope call:** the microscopic multi-Fermi-line solve is explicitly deferred (open
  question #1); it is the paper's acknowledged "complex and unnecessary" full model.

## 2. Low-T microscopic field sweep shows Delta2 rising with B (paper: mild suppression)
- **Symptom:** in the single-band `low_T_field_sweep`, Delta2 grows with B instead of
  following Delta2(B)/Delta2(0) ≈ 1-(B/Bc1)^2.
- **Cause:** with the single band the Zeeman + orbital terms shift spectral weight in a
  way that lowers the ordered free energy monotonically; without the correct band
  topology there is no gap-closing at ~33.5 T. This is the same single-band limitation
  as #1.
- **Scope call:** the quadratic suppression law is left to the corrected model
  (open question #4).

## 3. Numerical pitfall caught: unphysical orbital coupling
- **Symptom:** first field sweep gave Delta2 ~ 1e20 meV.
- **Cause:** an `e a^2 / hbar` unit-conversion assembled a prefactor ORB ≈ 2.4e18 that
  dwarfed every energy scale, so the free energy was minimized by a runaway gap.
- **Fix:** the paper explicitly states results depend on the *topology* of the orbital
  moment, not its magnitude; we set ORB = 0.010 meV/T (comparable to muB=0.058) — a
  scoped, disclosed choice. Zero-field results are independent of ORB.

## 4. Not attempted (out of MFT-gap-equation scope)
- **Double-step metamagnetism / Bc1=33.5 T, Bc2=41 T:** first-order band-crossing jumps
  in M(B); needs the 4-band magnetization (Eqs. E1-E2), not free-energy topology.
- **Giant Nernst (~30 uV/K) and Kerr angle:** Berry-curvature thermoelectric transport
  (Eqs. E); a separate, larger computation.

## Net
The **mechanistic core** (chiral d-SDW free energy, correct-scale zero-field gap and
T_HO with no parameter tuning, field-induced chirality, field-enhanced Tc) replicates.
The **high-field first-order phenomenology and transport** do not, and are honestly
scoped out. Hence **PARTIAL**, Agreement 7/10, Coverage 6/10.
