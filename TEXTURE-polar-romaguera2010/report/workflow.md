# Workflow — Reduced Replication of Romaguera, Doria & Peeters (arXiv:1001.1715)

## Goal
Reproduce the **essential mechanism** of the paper: the vortex morphology in a
superconducting rod with a magnetic dot on top depends *qualitatively* on the rod
thickness D — thin rods (disk, D~ξ) give **giant vortex** states; thick rods
(D≫ξ) give **curved / top-to-side multivortex** states with the Meissner state
retained at the bottom.

## Reduced-scope decision
The full paper is a 3D Ginzburg-Landau simulated-annealing calculation (heavy).
We chose the recommended tractable path (Option A):

1. **2D GL on the disk cross-section**, solved via TDGL gradient-flow relaxation
   in a **fixed external vector potential** (London/lowest-Landau-style), with the
   inhomogeneous field of a **point dipole** located 2ξ above the top surface,
   oriented along the rod axis (paper's geometry, A = (μ×r)/r³).
2. **Thin disk (D=2ξ):** one representative cross-section layer.
3. **Thick rod (D=6ξ):** a **stack of z-layers** (top→bottom). Because the dipole
   field decays with distance, each deeper layer sees a weaker field. Tracking the
   per-layer vortex configuration is the reduced proxy for the true 3D curved
   vortex line.

## Steps executed
1. Read `report/method_extract.md` + `extraction/marker.md` → extracted GL free
   energy (dimensionless), dipole A, geometry, and Table 1 state sequences.
2. Wrote `code/romaguera2010_replication.py`:
   - Cartesian cross-section mesh restricted to the disk (r≤R).
   - Peierls/link-variable **covariant Laplacian** for the gauge-covariant kinetic
     term (correct GL kinetic operator with fixed A).
   - **TDGL relaxation** dΨ/dt = Ψ − |Ψ|²Ψ + (∇−iA)²Ψ, multiple seed windings,
     lowest-free-energy state selected per geometry.
   - Diagnostics: boundary **phase-circulation winding**, **plaquette
     phase-singularity** vortex-core finder (gauge-invariant topological charge),
     core RMS radius (giant vs spread), mean |Ψ|².
3. **Calibration:** computed enclosed dipole flux vs μ to pick μ in the few-vortex
   regime (μ=25 reduced units → ~3 flux quanta at the top layer). Early μ=55 run
   drove the whole sample normal (mean|Ψ|²≈1e-6) — corrected.
4. Ran full experiment (137 s): thin disk + 5-layer thick stack.
5. Saved `work/results.json` incrementally; generated 3 figures.
6. Scored each claim honestly (expectation / observed / reproduced / match / note).

## Reproducibility
- CPU-only, `numpy` + `scipy` + `matplotlib`. Deterministic seeds.
- Rerun: `python3 code/romaguera2010_replication.py` (~140 s).
