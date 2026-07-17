# Failure / Scope Analysis — oh2026 (arXiv:2605.21124)

## What reproduced perfectly (model headline)
The paper's central theoretical claim — **chirality-locked, spin-free interatomic
OAM** — reproduces to machine precision from a minimal pure-NumPy model:
- **C1:** 3 nondegenerate dispersive bands (bandwidth 4.0 t) from a flux-threaded
  3-site `3_1` helical chain, split over >99% of the BZ, touching only at isolated
  screw-protected crossings.
- **C2a:** `L_Itin_x` locks to `sign(dE/dk)` — per-band sign-match 1.0/1.0/1.0,
  `|corr|` 0.998/0.999/1.000 (mean 0.999).
- **C2b:** OAM flips sign with chirality — RH and LH chains are energy-degenerate but
  `L_L = −L_R` exactly (100% of k-points flip).

Because s-orbitals carry `L_Atom = 0`, the entire OAM in the model is itinerant, so
this is a genuine, clean test of the paper's core concept. No result contradicts the
paper.

## Out of scope (not reproducible with available resources)

### C2/C5 — quantitative DFT+Wannier bulk-Te OAM
- **Why:** needs the Supplemental-Material DFT parameters (plane-wave cutoff, k-mesh,
  SOC/U settings — NOT in the extracted main text), a VASP (or free QE) + Wannier90 +
  `post_wan` toolchain, and the full 3D Te cell.
- **What a full material repro needs:**
  1. Supplemental-Material PDF of arXiv:2605.21124 (exact DFT numerics).
  2. VASP + PAW pseudopotentials (or QuantumESPRESSO free stack), Wannier90, post_wan (Ref [48]).
  3. Materials-Project chiral Te structure (P3_1 21 / P3_2 21, a≈4.46 Å, c≈5.92 Å).
  4. ~1 node / 8–16 CPU cores, a few hours SCF+bands; Wannier90 + post_wan on 1 core.
  5. Compare ACA (→0 for s) vs modern-theory-of-orbital-magnetization L on the
     E−E_F=−9.5 eV iso-energy surface; extract L_Glob_y/z from interchain hopping.

### C3 / C4 — CD-ARPES / SARPES
- **Why:** synchrotron-beamline experiments (circular-dichroism and spin-resolved
  ARPES). Not computable. Their theoretical counterparts (the L_Itin_x sign texture
  and the absence of SAM in s-bands) are what the model half addresses.

## Lesson learned — the chirality-transform bug
A left-handed helix is the **mirror image** of a right-handed one. The FIRST attempt
reversed BOTH the site azimuth (`φ_j → −φ_j`) AND the axial screw phase of the Bloch
term. That combination is just the trivial `k → −k` symmetry: it left `L` unchanged
and produced **no chirality flip** — a false negative on the headline claim.

**Fix:** the correct mirror reverses ONLY the geometric azimuth while keeping the
axial screw-advance direction (hence `H(k)` and `E(k)`) fixed. Then the two
chiralities are energy-degenerate but carry opposite circulating current
(`L_L = −L_R`), exactly matching the paper.

**Takeaway:** when testing a chirality/handedness effect, distinguish a genuine
**mirror** (spatial-inversion of geometry) from a **momentum inversion** (`k → −k`).
They can look identical on a single observable but have opposite physical meaning;
conflating them silently kills the effect you are trying to measure.
