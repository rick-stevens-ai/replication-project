# Failure Analysis — Reduced Replication of arXiv:1001.1715

## What was NOT reproduced / limitations

### 1. No literal 3D curved vortex line (fundamental reduced-scope limit)
The paper's headline object is a **single vortex that curves through 3D space,
entering the top surface and exiting the lateral surface**. Our reduced model
solves independent 2D cross-section layers with a fixed external A and no
z-direction gradient coupling. We therefore reproduce the *depth-dependent
winding profile* (a proxy: winding = 6 at top → 1 → 0 at bottom for D=6ξ) but
**not the connected curved line** as a single 3D isosurface. This is a
by-design consequence of Option A (tractable reduction), not a bug. Verdict for
the thick-rod claim is honestly **PARTIAL**.

### 2. First failed run: sample driven fully normal (μ too large)
Initial parameters used μ=55 (reduced units). The point-dipole field ∝ μ/r³ is
extremely peaked under the dot; at μ=55 the field overwhelmed superconductivity
everywhere and Ψ collapsed to |Ψ|²≈1e-6 (essentially the normal state), giving
meaningless winding/core numbers.
- **Root cause:** μ not calibrated to the sample's flux scale; the dipole field's
  strong peak near the dot dominates.
- **Fix:** computed the enclosed dipole flux Φ(μ) through the disk and chose μ so
  Φ/2π ~ a few flux quanta (μ=25 → ~3), keeping SC alive with a few vortices.
- **Prevention:** always calibrate the drive by enclosed flux before a GL run;
  check mean|Ψ|² > 0 as a sanity gate.

### 3. Second failed run: spurious "44 cores" (boundary artifact)
The first core-finder counted local minima of |Ψ| anywhere inside the disk. Since
|Ψ| decays *naturally* to zero at the disk surface (Neumann/masked boundary),
dozens of boundary points registered as false "cores" (44 of them, all on the
rim).
- **Root cause:** amplitude-minimum core detection cannot distinguish a genuine
  vortex core from the natural surface decay of the order parameter.
- **Fix:** replaced with a **gauge-invariant plaquette phase-winding** detector
  (topological charge q = ∮∇θ/2π around each 2×2 cell), restricted to r<0.9R.
  This finds real ±1 phase singularities regardless of amplitude and is immune to
  the boundary decay.
- **Prevention:** for vortex counting always use the topological (phase-winding)
  definition, not an amplitude threshold.

### 4. Regularized (softened) point dipole
The exact point dipole A ∝ 1/r³ is singular directly under the dot and makes the
Peierls link variables blow up on the discrete mesh. We softened |r|³ →
(|r|²+0.05)^{3/2}. This keeps the field strongly peaked (physical) but finite.
- **Consequence:** the absolute μ scale is not identical to the paper's, so our
  winding numbers are illustrative of the regime, not matched to Table 1's exact
  μ/μ0 windows. Documented; flagged in open question #5.

### 5. Quantitative Table-1 matching NOT attempted
We reproduce the *qualitative* giant-vs-multivortex thickness crossover, not the
exact ground-state μ-sequences in Table 1. Matching those requires the precise
dimensionless-unit mapping and the full 3D solver. Honest scope boundary.

## What worked (and why the verdict is a solid PARTIAL, not a failure)
- Thin disk (D=2ξ): winding=2 with both phase singularities piled at r≈0.05ξ
  (RMS radius) = a **giant vortex** — exactly the paper's thin-disk GVS.
- Thick rod (D=6ξ): winding **decreases with depth** (6→1→0) and mean|Ψ|² **grows
  toward the bottom** (0.0 at top → 0.38 at bottom) = **Meissner retained at the
  bottom**, the precise physical statement in the paper's abstract and text
  ("the dipolar field ... may become so dim at the bottom ... unable to sustain
  vortices ... Meissner state is kept at the bottom").
- The two geometries are qualitatively different (giant/uniform vs
  depth-varying), reproducing the headline thickness-dependence mechanism.
