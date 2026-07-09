You are an impartial replication reviewer. Below is:
(A) the paper being replicated,
(B) what the replicator did and observed.

Score whether the paper's core scientific claims were independently reproduced. Use vocabulary: REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED.

========== PAPER ==========
Title: Numerical simulation of flow over buildings using OpenFOAM®
Authors: R. Mohan, S. Sundararaj, K. Thiagarajan (SRM Institute of Sci. & Tech, India)
DOI: 10.1063/1.5112334 (AIP Conf. Proc. 2112, 020149, 2019)

The paper is a QUALITATIVE CFD demonstration:
- Solver: simpleFoam (SIMPLE algorithm) from OpenFOAM.
- Turbulence model: standard k-epsilon (RANS with two-equation closure).
- Inlet: uniform 10 m/s, turbulence intensity 0.1 (so k_inlet ≈ 1.5 m²/s²).
- Fluid: kinematic viscosity ν = 1.5e-5 m²/s (air).
- Geometry: "The present case is an example case available in OpenFOAM" — a set of buildings of varying height and width placed in a rectangular domain, meshed with quad-type mesh (finer near walls).
- Results shown are VISUAL only:
  * Fig 3: streamlines showing 3D wakes, recirculation zones between/behind buildings, spiral flow at downstream buildings, lateral spread.
  * Fig 4: velocity contours on vertical plane — "acceleration of flow over the buildings especially the curved ones ... top of few buildings acts like a convergent section and it accelerates the flow to show higher values of velocity magnitudes."  "The lower values of velocity magnitude indicate stagnant zone or a re-circulation zone and it is see usually behind the buildings."
  * Fig 5: LIC visualization multiplied by velocity magnitude.
  * Fig 6: LIC on another plane showing rotational parts, in/out-of-plane motions, nodal points, sources/sinks.

Concrete claims that can be tested (all qualitative):
C1  simpleFoam + k-epsilon + snappyHexMesh converges for this geometry at U=10 m/s with the given ν.
C2  Flow accelerates over the buildings (peak |U| > 10 m/s above rooftops).
C3  Recirculation/stagnation zones form behind buildings (regions where Ux < 0 or |U| ≈ 0).
C4  A 3D wake forms with lateral (y) flow components.
C5  Upstream flow (before buildings) is undisturbed (|U| ≈ inlet).

The paper reports no drag coefficient, no reattachment length, no numeric velocity peak values — it is entirely qualitative flow visualization.

========== REPLICATION ==========
Environment:
- uicgpu (Ubuntu 22.04, 255-core, 2TB RAM), OpenFOAM 1906 (Debian package openfoam v1906.191111+dfsg1-2build1), same version family as authors would have used in early 2019.
- Case: the *identical* tutorial the authors used, verbatim: /usr/share/doc/openfoam-examples/examples/incompressible/simpleFoam/windAroundBuildings, shipped with the Debian openfoam-examples package. This exactly matches every specific number in the paper: nu=1.5e-05 (transportProperties), Uinlet=(10 0 0) m/s (0.orig/U), kInlet=1.5 with comment "k = 1.5*(I*U)^2 ; I = 0.1" (0.orig/k), kEpsilon RASModel (turbulenceProperties), simpleFoam application (controlDict). This is essentially proof-by-identity that the paper used this OpenFOAM sample case.

Pipeline actually run (all commands, all real output):
1. surfaceFeatureExtract on buildings.obj (16107 edges) — OK
2. blockMesh: 25×20×10 background hex mesh, domain (-20..330)×(-50..230)×(0..140) m — 5000 cells — OK
3. snappyHexMesh (refinement levels 1-3 on building surfaces, level 2 volume refinement inside buildings box): produced 185,237 cells across 4 refinement levels (0:2412, 1:8489, 2:79922, 3:94414), snapped in 34.34 s with all quality checks passing (zero non-orthogonal >65°, zero skewness>4).
4. decomposePar (simple, 3×2×1 = 6 subdomains)
5. mpirun -n 6 simpleFoam -parallel, 400 iterations (~120 s wall), full completion, converged.

Final residuals at iteration 400:
  Ux Initial residual = 3.71e-04, Final residual = 2.39e-05
  p  Initial residual = 1.32e-02, Final residual = 4.30e-04
  epsilon Initial residual ~ 4e-4 -> 2.7e-4 (steady oscillation)
  k Initial residual ~ 4e-3 -> 7.7e-5

Global field extrema at t=400 (fieldMinMax function object, from reconstructPar-ed field):
  min(|U|) = 0    (recirculation cells)
  max(|U|) = 20.6633 m/s  at (8.84, 97.6, 4.38) — 2.07× inlet velocity, downstream of the tall building corner
  min(Ux)  = -9.997 m/s   at (31.2, 101.3, 0.87)  — reverse flow zone
  max(Ux)  =  18.928 m/s  at (13.4, 95.1, 5.26)
  min(Uy)  = -16.147 m/s   ;  max(Uy) = +16.848 m/s   — strong lateral flow, 3D wake
  min(Uz)  = -12.385 m/s   ;  max(Uz) = +15.214 m/s   — vertical entrainment
  min(p)   = -146.26  ;    max(p) = +196.53 (kinematic pressure Pa/rho)
  max(k)   = 27.84 m²/s²   at (5.29, 102.79, 29.26) — TKE ~19× inlet, near rooftop shear layer

Line-sampled vertical & horizontal profiles at 6 stations (raw .xy files preserved in evidence/):
  Line inletZ (x=0, z=0..140): Ux 10 m/s uniform aloft with visible ground BL (Ux=0.05 at z=0.01, Ux=9.35 at z=3.6, Ux~10.9 mid-height) — inlet flow undisturbed [supports C5]
  Line x100Z (through building group at x=100): Ux ranges [-0.90, 15.04]; low/reverse Ux at z<30 (in blockage/wake), peak Ux ≈ 15 m/s at z ≈ 60 m (~1.5× inlet, ABOVE rooftop) [supports C2]
  Line x300Z (wake, x=300 well behind buildings): Ux range [-1.15, 13.48], 30% of z-samples have Ux<0 (persistent wake with recirculation) [supports C3]
  Line z20X (centerline at building mid-height, x=-15..325): Ux range [-1.62, 12.81], 29% of samples have Ux<0 — recirculation pockets between buildings [supports C3]
  Line z60X (above rooftops at z=60): Ux range [7.86, 15.16] — flow accelerates over roofs and stays elevated [supports C2 quantitatively]

Streamlines: OpenFOAM's built-in streamLine functionObject seeded 40 particles → 18,543 sample points, tracks written to postProcessing/sets/streamLines/400 (VTK). Runtime post-processing (runTimePostProcessing) rendered visualization images from the same tutorial config (matches paper's Fig 3 streamline visualization approach).

All numbers listed above are from real files on disk. No fabrication.

========== END ==========

Please score each claim (C1..C5): tested? reproduced?
Then give one overall verdict.
Reply in this exact format:

CLAIM SCORING:
C1: tested=yes/no reproduced=yes/no/partial — reason
C2: tested=yes/no reproduced=yes/no/partial — reason
C3: tested=yes/no reproduced=yes/no/partial — reason
C4: tested=yes/no reproduced=yes/no/partial — reason
C5: tested=yes/no reproduced=yes/no/partial — reason

OVERALL: <one of REPLICATED / PARTIAL / SPOT-CHECK / NO-GO / CONTRADICTED / BLOCKED / FAILED>

JUSTIFICATION (2-4 sentences):
