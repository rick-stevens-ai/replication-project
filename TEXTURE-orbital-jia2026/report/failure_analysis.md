# Failure Analysis — jia2026 NOME reproduction

**Paper:** Geometry-Driven Nonlinear Orbital Magnetoelectric Effect (Jia, Qiao, Wang, arXiv:2605.17462)
**Verdict:** PARTIAL — validates the symmetry structure, not the flagship magnitude.

## What matched (clean)

1. **Band structure (C4-bands).** 4-band Kane–Mele structure with ~5 eV (≈6t)
   bandwidth and an 18.04 meV central gap — consistent with Fig 1(a).
2. **λ_R-evenness / P-even symmetry (C4-even-λ_R).** χ^{(0,od)}_{z;xx}(+λ_R) =
   χ^{(0,od)}_{z;xx}(−λ_R) to relative error ~9e-16, verified at λ_R = 10, 20,
   30 meV, with a nonzero value (raw ~13.94) at λ_R=0. This is the strongest
   reproduced result and directly confirms the paper's central symmetry claim.
3. **Orbital vs spin sign (part of C4).** Near the gap the orbital "od" response
   is opposite in sign to the spin response — qualitatively as claimed.

## The specific gap: geometric sector not implemented → 3× not reproduced

- **Root cause.** The headline quantitative claim — orbital moment ≈ 3× spin
  moment — is a property of the **total** intrinsic response, which is dominated
  by the geometric "d"+"ic" terms governed by the **Hermitian connection**
  (Eqs. 4–6, 8, 9). This compute pass implemented only the conventional
  matrix-element "od" term (first line of Eq. 3), which is the robustly
  well-defined, gauge-invariant piece.
- **Observed consequence.** The od-only orbital/spin magnitude ratio is
  ~10–100× (near-conduction-edge median ≈ 11.6, peak ≈ −115.6), NOT ≈ 3×. The
  od term alone overshoots because it lacks the geometric contributions that
  rebalance orbital vs spin near the band edge.
- **Why not implemented.** A defensibly gauge-invariant coding of the full
  Hermitian-connection / positional-shift / covariant-derivative tensors
  (C^{a;ab}_nm, N^{a;ab}_nm, L^{a;ab}_nm, D^a_mn) is the error-prone part
  flagged in `method_extract.md` and was out of the compute budget for a
  correct implementation.

## Absolute-magnitude (unit) gap (C6)

- The response is reported in raw/internal geometric units. The claimed
  ~10 μB/V² (and ~1e-5 μB/nm² at E=1e5 V/m) requires the full dimensional
  prefactor of Eq. (1): electron charge, lattice length, ℏ, unit-cell area, and
  the E-field length convention. We reproduce the response **structure**
  (μ-dependence, λ_R-evenness, orbital/spin sign) but did not fix the absolute
  scale, so C6 is neither confirmed nor refuted.

## Not attempted

- **Model 2 (CuMnAs AFM, Eq. 12, extrinsic NOME, C5).** Tractable 4-band,
  τ-linear Fermi-surface model with only χ^{(1)}_{z;xy} allowed. Not coded
  (time budget). Parameters are in `method_extract.md`.
- **MPG symmetry enumeration (C3, 41/55 MPGs).** Pure group theory (Eq. 10
  transformation rule). Not enumerated; only the allowed χ_z;xx component was
  computed, and vanishing of forbidden components was not numerically verified.

## Secondary caveat: mesh sensitivity

- The χ-vs-λ_R curve at fixed μ=50 meV is non-monotonic/noisy because the Fermi
  level crosses band edges as λ_R varies on a fixed 120×120 mesh. The even
  symmetry is exact regardless; only the fine shape is mesh-sensitive. A denser,
  adaptively-refined mesh near K/K′ (≥200×200) would smooth it.

## What a fuller reproduction needs

1. **Code the geometric sector (Eqs. 4–6, 8, 9)** with correct, gauge-invariant
   covariant derivatives (Hermitian connection + positional-shift tensors), then
   recompute the TOTAL orbital and spin χ_z;xx and re-measure the orbital/spin
   ratio near the band edge — testing whether it converges to ≈ 3×.
2. **Fix the dimensional prefactor of Eq. (1)** to convert raw units to μB/V²
   and validate the ~10 μB/V² / ~1e-5 μB/nm² magnitude (C6).
3. **Convergence study** with a dense/adaptive ≥200×200 mesh near the Dirac
   points; sweep T and μ to characterize ratio stability.
4. **Implement Model 2 (CuMnAs)** for the extrinsic NOME (C5).
5. **Enumerate the MPG constraints (C3)** and numerically verify vanishing of
   symmetry-forbidden χ components (C4-onlyxx).
