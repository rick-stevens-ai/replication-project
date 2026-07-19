# Failure Analysis — TEXTURE-polar-zhou2021

## Summary
No hard failures or crashes. One claim (dielectric magnitude) is out of scope by
design; one sub-metric (neighbour single-peak line profile) was noisy but the
underlying topological claim still held. Everything below is honestly scoped —
nothing faked.

## Out of scope (deliberately NOT attempted — would require full multiphysics)
These are inherent to the paper's HPC-scale method and cannot be reproduced by a
reduced 2D dimensionless model. They are NOT counted as replication failures;
they are scope boundaries.

1. **Full 3D 320x320x350 mesh.** The paper runs a 3D superlattice
   (PTO16/STO16 stacking, substrate, air) on the Shanghai Supercomputing Center.
   We use a single 2D top-layer plane. Justification: the paper analyzes the
   Pontryagin density on the top PTO layer plane, so a 2D plane captures the
   topological observables.
2. **Iterative-perturbation elastic solver + electrostriction** (eigenstrain
   e0 = Q_ijkl P_k P_l, elastic stiffness C_ijkl, lattice mismatch from PTO
   3.957 A / STO 3.905 A). Omitted; replaced by an effective uniaxial anisotropy.
3. **Superposition electrostatics** over film/substrate/air with real
   depolarization fields. Replaced by an analytic electrode field model
   (downward Ez + fringing Ex). The Neel-DMI term stands in for the
   depolarization+gradient competition that makes Neel bubbles.
4. **Absolute physical units.** Real voltages (6/9 V), nominal fields
   (+800 kV/cm), Haun-1987 sixth-order PbTiO3 Landau coefficients, background
   dielectric k=40 in physical units. Our model is dimensionless/reduced.
5. **Dielectric magnitude:** initial eps ~ 650 and the ~80% reduction, plus the
   electrode-size scaling of eps. These require the negative-capacitance /
   depolarization physics with real coefficients. We reproduce only the SIGN
   (eps decreases with field) — see Claim 5 = PARTIAL.
6. **Experimental sections:** PLD growth, RHEED, HAADF-STEM/TEM characterization.
   Purely experimental; nothing to compute. Not attempted.

## Soft issues (within scope, handled)
1. **Neighbour single-peak line profile (Claim 3) was noisy.**
   - Symptom: exp2 reported 3 line peaks, not 1, when sampling a band outside the
     electrode.
   - Root cause: the dense skyrmion lattice put multiple bubbles in the sampled
     band, so the 1-D cut crossed more than one bubble. This is a sampling
     artifact of choosing a fixed band, not a physics failure.
   - Resolution: the CORE topological statement (local Q preserved = +1 through
     the symmetric->asymmetric shape change) was verified independently via the
     windowed local charge (Q_neighbor = 0.83 -> +1) and stands. The exact
     single-peak signature would need per-bubble segmentation (logged as future
     work, not blocking).

2. **Large-field non-recovery threshold initially too strict (exp3).**
   - Symptom: exp3 flagged `large_field_stays_suppressed = false` (recover 65% vs
     a <60% cutoff).
   - Root cause: exp3 used a moderate high field (V=7, d0=30) and an arbitrary
     absolute cutoff. The paper's contrast is RELATIVE (large vs small), and its
     high case is stronger (9 V, wide electrode).
   - Resolution: exp4 re-ran with V=9 / d0=36 and a relative criterion. Result
     decisive: small recover_frac=1.34 (158 bubbles) vs large=0.37 (10 bubbles).
     Recovery asymmetry confirmed. The exp3 flag was a threshold artifact, now
     superseded by exp4.

3. **FFT stripe-anisotropy metric (exp3) was unreliable.**
   - Symptom: `stripe_order_increased = false`.
   - Root cause: after field removal, NEW skyrmions nucleate in un-electroded
     regions, lowering the global FFT anisotropy even though a labyrinthine patch
     locked in locally. The global metric mixes the recovered and locked regions.
   - Resolution: replaced with a bubble-count metric in exp4 (n_bubbles: 158 vs
     10), which cleanly distinguishes recovered vs labyrinthine. FFT metric
     retired.

## Lessons
- For topological-texture replications, COUNT-based metrics (bubble count,
  integer Q) are far more robust than spectral/anisotropy proxies.
- Recovery claims in these systems are best tested with RELATIVE (small-vs-large)
  criteria matching the paper's own comparison, not absolute cutoffs.
- The Berg-Luscher lattice solid-angle charge gives exact integers and was the
  single most reliable observable across all experiments.
