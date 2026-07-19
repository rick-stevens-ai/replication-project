# Failure Analysis — Hayashi et al. 2005 vortex-in-NCS replication

## What is reproduced (high confidence)
- **Same core radius** for Psi(r) and Delta(r) (paper's stated finding) — by
  construction (both tanh), so this is a qualitative match, not an independent test.
- **Zero-bias LDOS core peak**: N(E=0,r) maximal at r=0 and core LDOS peaked at E=0.
- **Two-gap bulk DOS**: fully-gapped sheet I strongly suppressed at E=0, line-node
  sheet II with finite zero-energy DOS — the paper's central spectroscopic signature.
- **Supercurrent** ~0 at core, peaking near r~xi0, from g_I+g_II.
- **Distinctive radial magnetization** |M|~(g_I-g_II): peaks near the core, →0 far,
  and **exactly vanishes** in the equal-sheet control — the mechanism (broken
  inversion symmetry / FS splitting) is cleanly isolated.

## Key correction made during this replication
An earlier draft computed the magnetization as a scalar `g_z`-weighted DOS
*deviation* (`m_z`), which is **not** the paper's construction and produced an
unphysical far-field value larger than the core value (`textured=false`,
`reproduced=false`). The paper's Eqs.7-9 define the magnetization from the sheet
**difference** `g_I - g_II` with in-plane (radial) direction and `M_z=0`. The
solver was rewritten to use `g_I - g_II` exactly; the far field then →0 and the
equal-sheet control →0 identically, as physics requires. **Lesson: read the
paper's observable equations verbatim before coding; a plausible-looking proxy
gave the wrong sign structure and a false verdict.**

## Limitations / what is NOT fully reproduced
1. **No self-consistency.** Psi(r), Delta(r) are imposed tanh profiles, not solved
   from the gap equations. So absolute magnitudes and the precise core shape are
   model inputs, not outputs → PARTIAL, not full REPLICATED.
2. **Absolute scales not matched.** |M| and |j| are in arbitrary/normalization-
   dependent units; only spatial textures, core localization, sign *structure*,
   and the control are claimed.
3. **Modest LDOS core/far ratio (1.60).** The paper's zero-bias peak is very large
   (truncated in its Fig.3). Finite smearing eta=0.05 and coarse radial binning
   dilute the peak; smaller eta + finer bins would sharpen it (see open questions).
4. **Radial magnitude only for M.** We verified |M(r)| from g_I-g_II but did not
   separately confirm the azimuthal-component cancellation via the full
   (-k~_y, k~_x) angular integral, nor the sign (paper: M points inward).
5. **1/r tail not fit.** The paper confirms ~1/r decay of |j| and |M|; we did not
   fit the far-field exponent.
6. **FS anisotropy ignored** (spherical FS, equal vI/vII and DOS) — same
   assumption the paper makes, so not a discrepancy.

## What would break it / pitfalls for re-runners
- Forgetting `|Delta|>|Psi|` collapses the two-gap structure (sheet II must be able
  to node) — set Delta>Psi.
- Seeding the Riccati integration from the wrong (growing) side causes blow-up;
  keep a-forward / b-backward.
- Setting Delta=0 is the control (identical sheets) — M must be 0; if it is not,
  a binning/normalization asymmetry between sheets is present.
- Numerical az. current at r=0 is ~1e-33 (floating-point zero), correct.
