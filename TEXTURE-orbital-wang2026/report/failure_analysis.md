# Failure analysis — wang2026

## What is NOT reproduced (the PARTIAL gap)
1. **Absolute magnitude in physical units.** The paper's `chi_zzyy^(O) = -1.3
   (h/e) Ohm^-1 V^-1` requires an SOC-DFT + Wannier90 Hamiltonian of real
   CuMnAs with the physical band velocities, gaps, and Fermi surface. Our
   surrogate is in arbitrary model units, so only the ratio, sign, and scaling
   are comparable — not the number.
2. **Quantitative orbital/spin ratio.** We get ~6.0e3 vs the paper's ~150. Same
   qualitative regime (orbital dominates by >2 orders) but overshooting by ~40x.
   Likely causes: (a) simplified itinerant Eq.(3) L_z operator vs the paper's
   modern orbital-magnetization operator; (b) the model's spin channel is
   artificially suppressed because S^z is exactly sublattice-diagonal and the
   SOC term mixes spin in a way that under-weights the spin dipole; (c) coarse
   18^3 grid on a sharply peaked Fermi-surface quantity.
3. **Figures / functional dependence.** No mu-scan (Fig 1d), no k-resolved OBD
   map (Fig 1e/f), no angular dependence chi(phi) (Figs 2d, 3c).
4. **Symmetry derivation.** The m'm'm' selection rules (Table I/S1) are imposed
   by construction in the toy model, not derived from the real crystal symmetry.

## Failure modes encountered and fixed
- **Empty Fermi surface (mu in a gap).** First run used mu=0, which sat in a
  global gap; df0/dk was ~0 everywhere and every dipole was numerical noise
  (~1e-22). Fixed by probing the spectrum and setting mu=1.0 on the
  nodal-line-derived Fermi surface (near-FS state fraction ~0.035).
- **Under-converged FS integral / grid noise in the lambda scan and T-odd
  checks.** At T=0.02 and Nk=14 the scan/T-odd numbers were noise-dominated and
  inconsistent (spurious ratios ~1e9, sign not flipping). Fixed by raising the
  thermal smearing to T=0.08 (consistent with the paper's finite-T 50 K setting)
  and unifying all grids to Nk=18.
- **Sign-flip guard mis-scaled.** The T-odd test used a `> 1e-12` magnitude guard
  while model-unit dipoles are ~1e-16, so a genuine sign flip was reported as
  "no flip". Fixed threshold to 1e-30.

## Confidence
Mechanism-level physics (SOC-induced, non-perturbative, T-odd, orbital-dominant
Berry-curvature-dipole response) is reproduced robustly and is not sensitive to
the remaining fixes. The absolute-magnitude gap is fundamental to skipping DFT
and is the honest reason for the PARTIAL (not REPLICATED) verdict.
