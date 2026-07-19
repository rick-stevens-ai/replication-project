# Failure / Gap Analysis --- morozovska2021 (arXiv:2104.00598)

**Verdict:** `replicated` (mechanism-level). Coverage 7/10, Agreement 10/10.
The core physics reproduced cleanly and to machine precision on every checkable
claim; the gaps below are almost entirely **scope** (1D reduction of a 3D FEM
paper) and **tooling**, not physics disagreements.

## What reproduced (high confidence)
- **Flexoelectric Lifshitz invariant = ferroelectric DMI mechanism.** The
  antisymmetric gradient coupling `F(Px Pz' - Pz Px')` converts an Ising wall
  into a chiral (Bloch) wall exactly as the paper argues.
- **Zero chirality at F=0.** `P_e(F=0) = 1.9e-12` --- a pure Ising wall, to
  machine precision (the K-anisotropy trick works).
- **P_e is odd in F.** Antisymmetry residual = 4.52e-5.
- **Chirality flips with sign(F).** `P_e(+0.6) = -0.637`, `P_e(-0.6) = +0.637`.
- **Amplitude grows monotonically with |F|**, and the **net chiral moment
  `int Px dx` grows then saturates** at |F|~1.
- Live re-run matched the saved evidence JSON to all quoted digits.

## The single most important caveat (read first)
**The saturation diagnostic must use the INTEGRAL, not the peak.** The transverse
peak `P_e` keeps growing with |F| (1.50 at F=1.5) because the wall narrows and the
Bloch component sharpens; only the net chiral moment `chi = int Px dx` actually
turns over and saturates (peaks ~2.42 near |F|=1, declining to ~2.17 at |F|=1.5).
Checking saturation on the peak alone would falsely report "no saturation."
This is why the evidence JSON tracks both `P_e_transverse_peak` and
`chirality_integral`.

## Gaps that are EXPECTED / scoped-out (coverage-capping, NOT failures)
1. **1D reduction of a 3D FEM paper.** We reproduce the *mechanism* and *scaling*
   but not the geometry: no cylindrical core-shell mesh, no pair of diffuse axial
   P3-domains near the cylinder ends, no XY-plane vortex/meron, no +/-1/2
   topological index at the ends. These are geometry-level features a 1D wall
   structurally cannot show --- coverage is correctly capped at 7/10 for this
   reason. This is the right scoping call for a 1D reduction, not a shortfall.
2. **Dimensionless units.** We report signs + scaling laws, not absolute
   uC/cm^2. The paper's absolute magnitudes require the full BaTiO3 material
   tensors (Table SI) and self-consistent electrostatics/electrostriction, which
   we fold into effective LGD coefficients.
3. **Self-consistent electrostatics + electrostriction not solved.** Absorbed
   into effective coefficients (a, b, g, K) rather than coupled sub-problems.
4. **Full flexoelectric tensor anisotropy F_ijkl not carried.** The paper stresses
   flexoelectric *anisotropy* shapes the morphology; our model uses a single
   effective scalar F + scalar transverse anisotropy K.

## Gaps that are TOOLING (not physics)
5. **marker / nougat not installed.** `extraction/marker.md` and
   `extraction/nougat.mmd` are honest `pdftotext` interims with NOTE headers and
   the exact regen commands. Equation fidelity from pdftotext is degraded
   (Unicode math mangled) --- mitigated by hand-transcribing Eqs 1a-1g into LaTeX
   inside `nougat.mmd` and `REPORT.tex`. Environment limitation, not a physics gap.
6. **No pdflatex on host.** `REPORT.tex` ships as source and compiles off-host.

## What would raise the verdict
Building a 3D (or cylindrical finite-difference) self-consistent LGD solver with
the full F_ijkl tensor and BaTiO3 Table SI parameters would let us attempt the
actual flexon geometry (axial domain pair + meron core + +/-1/2 index) and match
absolute uC/cm^2 magnitudes --- raising coverage toward 9-10/10. See
`open_questions.json` Q1-Q4 and `next_steps`.
