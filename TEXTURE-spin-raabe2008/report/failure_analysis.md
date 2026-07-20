# Failure analysis — arXiv:0811.0157 replication

## Scope verdict: OFF-THEME but PARTIALLY REPRODUCIBLE (not NO-GO)

The paper is a DFT + experiment progress report on biomedical β-Ti alloys, mislabelled into a
"texture-spin" batch. It has a reproducible computational core (closed-form thermodynamics +
quantitative data claims), so we replicated those rather than declaring it non-reproducible.

## What could NOT be reproduced, and why

### 1. The DFT total energies (the paper's actual "ab initio" engine)
- Eqs.(1),(4) require plane-wave DFT (GGA-PBE96, VASP) total energies of ordered bcc/hcp
  Ti-X supercells with volume relaxation. This is an HPC-scale calculation, out of scope for an
  overnight, free-endpoint, laptop replication. **Not attempted; not faked.**
- Consequence: we cannot independently produce Figs. 1a/1b, Fig. 6 simulated curves, or the
  Gibbs-construction β volume fractions from first principles.

### 2. Ti-Nb finite-T β-stabilization threshold (C2, partial FAIL)
- With the exact ideal-mixing entropy (verified: S(0.5)=kB·ln2) and a *symmetric parabolic
  surrogate* for the DFT energy anchored to the paper's stated T=0 root (~93 at% Nb), Eq.(3)
  at the hcp↔bcc transition temperature (~1155 K) lowers the threshold only to ~79 at% Nb —
  far above the paper's stated ~25 at%.
- **Root cause:** the true DFT Ef(x) for Ti-Nb is strongly asymmetric/skewed toward the
  dilute side (positive but small over a wide range), so a modest T·S term can zero it out at
  low Nb. A symmetric parabola with a 93 at% root has too large a positive hump at low Nb for
  the entropy to overcome. This is a limitation of the *surrogate*, not of Eq.(3) — and it is
  reported honestly rather than tuned away.
- Ti-Mo, whose T=0 root (~25 at%) is already at low solute, reproduces well (16.6 vs 14 at%),
  confirming the entropy machinery itself is correct.

### 3. Experimental data
- We can only *check arithmetic/trend claims* on the quoted moduli and volume fractions; we
  cannot reproduce the ultrasonic Grindo-Sonic measurements or XRD phase fractions (physical
  experiments).

## Honest negatives retained
- C4 max mismatch 1.02 at% on the roughest-rounded wt% row (Ti20Nb) — kept and explained as a
  rounding artifact rather than hidden.
- C3 Ti-Nb experimental modulus DECREASES with Nb (opposite the simulated linear increase) —
  kept and cross-referenced to the paper's own α/ω-contamination caveat.

## No fabrication statement
All numbers in REPORT come from either (a) verbatim paper text or (b) real executions of the
scripts in `code/` (outputs saved in `work/`). The DFT energies were never invented; where the
true energy curve is unavailable it is explicitly labelled a surrogate.
