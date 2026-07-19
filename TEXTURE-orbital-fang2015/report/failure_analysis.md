# Failure Analysis — TEXTURE-orbital-fang2015

## Scope / honest limits
This is a **review paper**, not a single-result study. A literal replication is
impossible: every concrete example is a plane-wave DFT job (cluster-class,
out of scope here). We replicated the **mechanism** of the OSEP double-well
demonstration (BTO/PTO, Sec 3.1.1) with a tractable model, NOT the DFT itself.
Everything below the DFT line is explicitly out of scope and NOT faked.

## What is a genuine surrogate vs a true reproduction
- **True to the paper:** the physical mechanism (2nd-order Jahn-Teller,
  Ti-3d/O-2p hybridization driving the soft-mode instability; OSEP as an
  orbital-selective on-site shift), the qualitative trends (monotone well
  collapse; ~2 eV quench; Ti-3d >> Pb-6s in PTO).
- **Calibrated, not first-principles:** absolute well depth (10.5 meV) and
  |Q*| (0.12 A) are tuned to physical scales; the lattice stiffness k was chosen
  so the critical shift lands at 2 eV. The paper reports only the 2 eV shift, so
  C2's "pass" partly reflects that calibration (see open_questions #1).

## Implementation failures encountered (and fixes)
1. **First run: no double well at all** (all claims failed). Root cause: initial
   lattice stiffness k=27 eV/A^2 vastly exceeded the vibronic softening
   4g^2/Delta = 6.47 eV/A^2, so curvature at Q=0 stayed positive. Fix: derived
   the analytic instability condition k < 4g^2/Delta and reset k=3.654 so
   s_crit = 4g^2/k - Delta = 2.0 eV exactly.
2. **Wells ran off the grid edge** (|Q*| pinned at 0.3 A). Root cause: the
   two-level lower eigenvalue is asymptotically linear in Q, so without a
   bounding anharmonic term the electronic energy decreases without limit. Fix:
   added a positive quartic k4*Q^4 lattice term to bound the well; tuned k4=45
   for a ~10 meV depth at |Q*|~0.12 A.
3. **JSON serialization TypeError** (numpy bool_ not serializable). Fix: cast all
   pass flags / numeric outputs to native Python bool/float before json.dump.

## Residual discrepancies
- **Grid vs analytic critical shift:** analytic onset = 2.00 eV (curvature sign
  change); grid displacement scan reports the well "gone" by ~1.69 eV because the
  near-onset well is sub-meV and drops below the 0.1 meV detection floor first.
  Both bracket the paper's ~2 eV. Not a failure, a threshold-sensitivity note.
- **Single-channel reduction:** collapsing the full Ti-3d(t2g/eg)+O-2p manifold
  to one bonding channel with one effective g is an approximation; multi-orbital
  effects could renormalize s_crit (open_questions #3).
- **PTO additive channels:** Pb-6s and Ti-3d treated as independent; real
  lone-pair activity involves 6s-6p-O2p cross-coupling (open_questions #4).

## Not attempted (out of scope, flagged not faked)
- Any actual DFT/PDOS calculation (Fig 1a PDOS shape).
- BFO, YMnO3, spin-spiral (gKNB) multiferroics, magnetoelectric interfaces,
  tunnel junctions, EuTiO3/EuO strain predictions — the bulk of the review.
- Absolute DFT double-well energetics for BTO/PTO.

## Reproducibility
Deterministic, no RNG, no network, no external endpoints. `python3
code/osep_model.py` regenerates all artifacts in <1 s. Verified numpy 2.4.3 /
scipy 1.18.0 on Python 3.14 (CherryRd).
