# Failure Analysis — Hotta 2006 replication

## What succeeded (exact matches)
- **Claim 1 (SO split):** Exact. Pure-SO diagonalization gives E(j=5/2)=-0.2,
  E(j=7/2)=+0.15, gap = (7/2)*lambda = 0.35 eV, multiplicities [6,8]. Zero error.
- **Claim 2 (GS flip):** Exact. x=+0.4 -> Gamma67 quartet ground; x=-0.4 -> Gamma5
  doublet ground. Correct multiplicities (4,2) and correct sign-flip behavior
  matching Fig 1(f) / Sec 2.2.
- **Claim 3 (orthonormality):** Exact. Max off-diagonal Tr(Xi Xj) = 2.2e-16.
- **Claim 4 (4u/5u non-mixing):** Exact. All 4u-5u overlaps O(1e-16).
- **Claim 5 (coefficient norms):** norm^2 within 0.995-1.001 of unity, i.e.
  consistent with the paper's 3-significant-figure reporting.

## Discrepancies and their causes
1. **CEF excitation magnitude (n=1 vs many-body n=2).** Our single-electron CEF
   excitation is ~8.3 meV, whereas the paper quotes ~1 meV for PrOs4Sb12 (Fig 1a).
   This is NOT a disagreement: the paper's ~1 meV is an n=2 *many-body* Heff result
   (with Coulomb Racah parameters), while we compute the exact one-body (n=1)
   building block. Different observables; the one-body value is the correct order
   of magnitude. To close this gap requires many-body ED (see open_questions #3).
2. **Coefficient-norm sub-percent deviations.** norm^2 = 0.995 for (0.67,-0.739,0)
   is just rounding of 2-3 sig-fig coefficients, not a modeling error.

## Out-of-scope (marked, not faked)
- Full NRG solution (Lambda=5, 3000 states/shell, Nph=20) -> chi(T), entropy,
  specific-heat curves (Figs 2,3). Requires a dedicated NRG impurity solver.
- Many-body Heff CEF levels for n=2,3,5 (Fig 1a-e) and the (lambda,U) phase
  diagram (Fig 1e). Requires multi-electron ED with Coulomb.
- Dynamical Jahn-Teller phonon dynamics and the 2u->4u+5u dominant-multipole
  crossover (the paper's headline conclusion). NRG-dependent.

## Pitfalls encountered
- **Write-path aliasing:** an early `write` used a path containing `../Dropbox`
  relative to the workspace, which resolved to `~/.openclaw/Dropbox/...` instead
  of `~/Dropbox/...`. Detected immediately (file-not-found on run), moved the file
  to the correct target and switched to absolute paths. No data loss, no writes
  outside the intended project tree (the stray `~/.openclaw/Dropbox` dir was
  removed).
- **Symmetrized (overbar) products:** the Gamma_5g and octupole operators use the
  "all permutations" overbar. Implemented as an explicit average over
  permutations of the cartesian factors; verified by the resulting exact
  orthonormality and 4u/5u decoupling (both would break under a wrong ordering).

## Confidence
High for the replicated (exact-diagonalizable) subset: all five checks pass to
machine precision or rounding. The NRG-dependent headline physics is
untested here and is flagged, not asserted.
