# Failure Analysis — TEXTURE-spin-sasioglu2026

## Failures encountered and resolved during replication

### F1 — Bloch cross-check spuriously disagreed with analytic (max diff = 2.39)
- **Symptom:** first run reported `analytic vs Bloch spin-split max diff = 2.39e+00`, implying
  the explicit 4×4 sublattice⊗spin Hamiltonian did not reproduce the analytic d-wave splitting.
- **Root cause:** the check function averaged the spin-splitting over BOTH sublattices
  (mean of A and B). Because A and B carry opposite altermagnetic signs (+dwave, −dwave), the
  sublattice average cancels the splitting to zero — a bug in the *diagnostic*, not the physics.
  The Hamiltonian itself was correct.
- **Fix:** compare the sublattice-resolved level `E(A,up) − E(A,dn) = 2·dwave` against the
  analytic `Δ`. New max diff = **0.0** (exact). No change to the physical model.

### F2 — RMS-over-folded-BZ observable was rotation-invariant (isotropic), killing claim c3
- **Symptom:** the "robust across tubes" claim used an RMS of |Δ| over the full folded k-mesh;
  its cos(2θ) fit gave `A ≈ 0, R² = 0.0` — no angular dependence at all.
- **Root cause:** RMS of the d-wave form over a full (rotated) 2D sampling is invariant under
  rotation of the sampling axes — averaging over all k washes out the angular anisotropy. It is
  the wrong observable for a directional (axial) spin splitting.
- **Fix:** switched every tube's observable to the **axial-resolved** splitting — the curvature
  of Δ along the tube axis at the band-edge folded mode. This is the physically relevant 1D
  nanotube spin splitting and folds exactly as cos(2θ). Per-tube fits now give **R² = 1.000**
  for N = 8, 12, 16.

## Lessons
1. When cross-checking a Hamiltonian against an analytic formula, make sure the *diagnostic*
   projects onto the same degree of freedom (here: a single sublattice) — an averaging bug can
   masquerade as a physics discrepancy.
2. Choose an observable that carries the directional information you are testing. An
   rotation-invariant scalar (RMS over full BZ) cannot exhibit an angular law by construction;
   the axial-projected quantity is the correct nanotube observable.

## Not attempted (declared out of scope, NOT failures)
- **First-principles DFT confirmation** of the specific compounds in the paper. This is
  cluster-only and confirmatory; the method extract explicitly recommends the TB core as the
  tractable target. Reported as out of scope.
- **True (n,m) commensurate rolled-lattice** construction with curvature-corrected hoppings —
  captured as open question #2 rather than attempted (continuum zone folding suffices for the
  headline cos(2θ) law).
