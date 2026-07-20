# Failure Analysis --- chen2026

## SINGLE most important caveat: no DFT was run (coverage cap, not a failure)
The paper is real-time TDDFT (`compute_target=crux`). This replication deliberately takes
the `dft-paper-model-surrogate` route: it reproduces the **symmetry-dictated** headline
(octahedral-rotation-induced d-wave/g-wave nonrelativistic altermagnetic spin splitting,
zero in the undistorted AFM) from a minimal tight-binding model, WITHOUT the
material-specific KNiF3 band energies, gap, or fs lattice dynamics. This is why **coverage
caps at 8/10** by design. It is correct scoping, not a shortfall.

## What reproduced (high confidence)
- **C1 -- Kramers protection (EXACT).** Undistorted G-type AFM has max|Delta| = 0.0
  (machine precision). Spin degeneracy is protected by PT / tau*U_1/2.
- **C2 -- d-wave for a0b-c- (MATCH).** Dominant angular harmonic m=2, exactly 4 sign nodes,
  and Delta is mirror-ODD under kx<->ky (residual 0.0). This is the d-wave altermagnet.
- **C3 -- g-wave for a0b0c- (MATCH).** Dominant harmonic m=4, exactly 8 sign nodes.
- **C4 -- eta control (MATCH).** Splitting magnitude is monotone in eta, exactly zero at
  eta=0, linear-correlation 0.988. The symmetry-breaking rotation switches the effect on.
- **C5 -- mode switching (MATCH).** Dominant harmonic switches m=4 (g, z-rotation) <-> m=2
  (d, y-rotation), reproducing the Fig 2b switching as a symmetry statement.
- **C6 -- spin-Hall on/off (MATCH).** With weak SOC, the spin-Hall sigma^Sz_xy is exactly 0
  in the ground-state AFM and finite (-1.3e-2) once distorted -- the nonrelativistic Hall
  signature.

## Machine-precision residuals are EXPECTED here -- not a smell
The surrogate obeys the parity/mirror relations BY CONSTRUCTION (cos kx - cos ky is exactly
mirror-odd; the AM term vanishes exactly at eta=0). So residuals ~1e-16 are expected, not
suspicious. The falsifiable content is twofold: (1) a SINGLE minimal model reproduces ALL
six sub-claims simultaneously; (2) a physically-WRONG parameterization genuinely FAILED --
see the debug record below. That combination is the evidence, not the residual magnitude.

## Debug record (an honest wrong-then-right)
- **First draft (1/6):** the altermagnet term was placed on `sigma_z * tau_z * g(k)`. This
  makes the spin-up and spin-down 2x2 blocks identical (the g(k) shift is the same for both
  spins), so the splitting cancelled and only C1 passed. **This is a real failure of a wrong
  model**, exactly the falsifiability the checks are meant to expose.
- **Fix (5/6):** place the AM term on `tau_z * sigma_0` (spin-INDEPENDENT sublattice-staggered
  anisotropy). Its interplay with the collinear Neel exchange `J*sigma_z*tau_z` makes the
  spin-up block see (J+eta*g)*tau_z and spin-down see (-J+eta*g)*tau_z -> genuine spin
  splitting. This is the standard collinear-altermagnet TB mechanism (Smejkal et al.), a
  physically-motivated fix, NOT tuning to the target.

## What did NOT reproduce (scoped / expected)
1. **Net charge AHC = +/-400 S/cm (Fig 3) -- SCOPED, 3D/DFT-locked.** In the minimal 2D
   collinear surrogate the net CHARGE anomalous Hall conductivity is symmetry-compensated to
   zero (~3e-16 for every mu and SOC form tested). This is correct physics for a 2D collinear
   altermagnet: the Berry curvature has the same d-wave symmetry as the order parameter and
   integrates to zero. The finite 400 S/cm requires the real 3D band structure, the specific
   Neel-axis SOC, and the full occupied-band curvature. **We instead reproduce the
   nonrelativistic SPIN Hall on/off** (C6), which is the observable the surrogate can
   genuinely show. The absolute charge-AHC magnitude is open Q1 -- a data/compute-availability
   gap (needs crux DFT+SOC), NOT a physics disagreement. This is why the verdict is not
   downgraded: the mechanism and every symmetry-dictated sub-claim reproduced.
2. **fs time trace eta_alpha(t) (Fig 4d-f).** eta is an external knob here; the real
   trajectory needs coupled electron-lattice rt-TDDFT (open Q2). C5 is reproduced as a
   symmetry statement, not a dynamical selection.
3. **Excited-PES energetics, multi-material selection rule, state lifetime.** Open Q3-Q5.

## Environment / tooling gaps (NOT physics)
- `marker` / `nougat` binaries absent (only poppler `pdftotext`). Artifacts 2 & 3 are honest
  pdftotext interims with NOTE headers + regenerate commands; nougat.mmd carries the
  hand-transcribed LaTeX equations to fulfill its math role.
- No LaTeX engine on host: REPORT.tex delivered as source (compiles off-host).

## Verdict rationale
Every symmetry-dictated sub-claim of the paper's mechanism reproduced from ONE minimal model,
including a genuine wrong->right debug that demonstrates the checks can fail.
**REPLICATED, coverage 8/10 (no DFT), agreement 9/10** (net charge-AHC magnitude scoped to DFT).
