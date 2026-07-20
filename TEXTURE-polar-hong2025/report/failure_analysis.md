# Failure Analysis — hong2025 phase-field replication

## Verdict: REPLICATED (mechanism-level), but with honest scope limits.

## What failed and was fixed (v1 -> v2)
- **v1 electric term was wrong.** The first runner penalized only the
  column-averaged out-of-plane polarization (`eps*<Pz>`). This suppresses net
  Pz but does NOT create the local charge frustration that nucleates vortices.
  Result: a uniform in-plane domain with only 2-7 stray winding defects,
  verdict PARTIAL (3/5).
- **Fix:** replaced with the physically correct bound-charge energy
  `f_elec = 0.5*eps*(div P)^2`, variational derivative `-eps*grad(div P)`. Its
  minimizer is a divergence-free field = closed flux loops = polar vortices.
  Added uniaxial anisotropy `-Kz*Pz` (PTO c-axis) so cores rotate out of plane.
  Result: balanced +21/-21 periodic vortex array, 5/5 checks, REPLICATED.

## Limitations / honest scope
1. **Not a quantitative periodicity match.** Our vortex period (~5 nm at the
   thin-film calibration) is the correct *order of magnitude* but smaller than
   the paper's reported ~14 nm. Coefficients (a, b, g, eps, Kz) are generic,
   not the paper's (unpublished-in-excerpt) PTO/STO Landau set, so absolute
   length scales are not expected to match.
2. **2D cross-section, not full 3D.** The paper simulates 400x200x120 (trilayer)
   and 200x200x250 (superlattice) 3D grids with a 3-component P. We use a 2D
   (x,z) slab with 2-component P. This captures the vortex winding and
   flux-closure mechanism but not the full 3D swirling / toroidal structure or
   the in-plane [100]/[001] vortex orientation seen in DF-TEM.
3. **Only the FIRST half of the claim tested.** The recipe's full headline also
   asserts a *mixed vortex + a1/a2 twin-domain phase* in the [PTO16/STO12]10
   superlattice. That requires anisotropic elastic (strain) energy and a
   superlattice stacking mask, which we did not implement — so the
   trilayer/superlattice contrast is untested (flagged in open_questions).
4. **Simplified energies.** Elastic energy is represented only as thin-film
   confinement (dead-layer mask), not the full iterative-perturbation elastic
   solver with substrate strain and elastic anisotropy the paper uses.
5. **Metastability not ruled out.** Single-seed TDGL from noise; we did not run
   annealing/multi-seed to prove the vortex array is the global minimum
   (though the control run shows it is energetically preferred over uniform
   when the electric energy is on).
6. **The paper's DYNAMICAL headline (field-driven vortex-boundary motion via
   zigzag-core switching) is out of scope** — we replicated the static vortex
   phase that motion acts on, not the motion itself.

## Extraction caveat
`extraction/marker.md` and `extraction/nougat.mmd` are **pdftotext `-layout`
interims** with header notes, not true marker-pdf / nougat OCR output. Equation
glyphs in the PDF (e.g. the TDGL and free-energy equations) are mangled by
pdftotext; the physics was read from context, not the mangled glyphs.

## Bottom line
The core reproducible physical claim — a **pure vortex phase emerges from
Landau+elastic+electric+gradient competition, driven specifically by the
electric/bound-charge energy** — is independently reproduced with correct
topology (balanced ±winding array) and correct regime selectivity. Quantitative
periodicity, the superlattice mixed phase, 3D structure, and field-driven
dynamics remain as documented next steps.
