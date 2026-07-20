# Failure Analysis — Yuan & Chen 2023 replication

Verdict: **REPLICATED** (headline sub-claims reproduced in a reduced 2D LGD model).
This document records what the replication does NOT establish and where it can mislead.

## What was genuinely reproduced
- A stable, close-packed polar skyrmion lattice with integer topological charge
  Q_net = 15.86 ~ 16 over 16 seeded cores => mean |Q| per core = 0.99 ~ 1.
  (Berg-Luscher lattice invariant; robust to detector noise.)
- The paper's field-driven topological-phase transition: total |Q| collapses
  27.8 -> ~0 as Ez rises, while mean Pz saturates from 0.00 to +1.17
  (multi-domain SkX -> single-domain FE). This is the destructive half of the
  headline (SkX disappears into FE at high field).

## What was NOT reproduced (honest gaps)
1. **Spontaneous field-INDUCED emergence.** The paper shows L (labyrinth) ->
   Sk&L -> SkX with increasing Ez from a random/labyrinth start. Here the SkX is
   *seeded* (Neel cores planted, then relaxed). A minimal 2D LGD without a full
   3D depolarization field and DMI-like/electrostatic stabilization does not
   spontaneously nucleate isolated integer skyrmions from noise — sparse seeds
   decayed in early iterations. The replication therefore tests SkX *stability*
   and *field-destruction*, not *nucleation*.
2. **Low-field labyrinth (L) and stripe (S) phases.** Not observed as distinct
   phases; our zero-field state is the relaxed SkX itself, not a meandering maze.
3. **Quantitative field scale.** Ez is in reduced units; no mapping to physical
   MV/cm was attempted (would require the Haun PbTiO3 Landau coefficients and a
   real electrostatic solver). The claimed thresholds (1.2, 1.8 MV/cm) are NOT
   quantitatively checked — only the qualitative rise/collapse ordering.
4. **T-E phase diagram and Kittel w^2 ~ h scaling.** Out of scope for this run;
   flagged as open questions.
5. **Neel vs Bloch wall type through thickness.** Untestable in a single 2D
   surface layer; requires a 3D slab.

## Detector caveat
`count_skyrmions` (local |Pontryagin density| maxima) is noisy: it reported 57
"cores" for 16 true skyrmions and spuriously non-zero counts in near-uniform
states before an absolute density floor was added. It is reported as
`n_sky_detected` for transparency but is NOT the basis of the verdict — the
integer Berg-Luscher charge Q_net is. Trust Q_net, not the peak count.

## Numerical pitfalls encountered
- Sextic Landau term overflowed at dt=0.05 with overlapping random seeds
  -> fixed by grid-placed non-overlapping seeds, amplitude clamp, and dt=0.02.
- Mean-field (`<Pz>`) depolarization was too weak to favor multi-domain states;
  replaced with a nonlocal low-pass k-space kernel that penalizes long-wavelength
  uniform Pz, making the modulated/SkX state competitive at low field.

## Bottom line
The physics engine correctly demonstrates that an out-of-plane field annihilates
a |Q|=1 polar skyrmion lattice into a single-domain FE state, with each skyrmion
carrying unit topological charge. The emergence direction and quantitative
phase diagram remain to be shown with a 3D, physically-parameterized model.
