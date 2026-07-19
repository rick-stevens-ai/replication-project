# Failure Analysis — Chatterjee 2019 Replication

## Bugs encountered and fixed (development)

### 1. `np.trapz` removed in numpy 2.x
- **Symptom:** `AttributeError: module 'numpy' has no attribute 'trapz'`.
- **Root cause:** numpy 2.x renamed `trapz` → `trapezoid`.
- **Fix:** `sed s/np.trapz/np.trapezoid/`. No physics impact.

### 2. Factor-of-2 error in the Belavin-Polyakov baseline (IMPORTANT)
- **Symptom:** BP baseline energy came out ≈ 25.1 while the topological target
  is 4πρ_s ≈ 12.566 — off by exactly 2×. The scan over skyrmion scale λ was
  correctly FLAT (≈25 for all λ), proving scale-invariance was right but the
  normalization was wrong.
- **Root cause:** the O(3) sigma-model energy density is **(ρ_s/2)(∂n)²**, i.e.
  `(ρ_s/2)(θ'² + sin²θ/r²)`. The first draft used `ρ_s(θ'²+sin²θ/r²)` (no 1/2),
  doubling every gradient energy and giving 8πρ_s instead of 4πρ_s.
- **Fix:** added the 1/2. BP baseline → 12.537 (0.24 % from 4π). This is the
  single most diagnostic check in the whole replication: the topological bound
  is exact, so hitting 4π to <1 % validates the functional AND the numerics.
- **Lesson:** when a scale-invariant quantity is off by an exact integer/simple
  ratio and flat across the free scale, suspect a normalization/convention
  factor, not a convergence problem.

### 3. First non-monotonicity construction was unphysical
- **Symptom:** an early version of the observable gap went strongly NEGATIVE
  (−29) because it stacked an arbitrary offset + an `alpha/size` "correction"
  onto a shifted skyrmion energy — an ad-hoc fudge that produced numbers
  without physical meaning.
- **Root cause:** trying to force a non-monotonic dip by hand instead of letting
  the relaxed sigma-model energy provide it.
- **Fix:** rewrote the mechanism honestly: (a) the RELAXED skyrmion energy
  Δ_sk(b) genuinely has an interior minimum (gradient-vs-Zeeman size balance),
  and (b) the observable gap is the min-envelope of Δ_sk vs a linearly-rising
  bare-electron channel. Removed the arbitrary offsets. All reported energies
  are now positive and physical.

## Honest limitations of the accepted result

1. **No absolute units.** ρ_s=1 normalization; K, b, T, and the electron-channel
   coefficients (c_e, E_e0) are effective parameters chosen to place the crossing
   in a visible range. The NON-MONOTONIC TREND is robust; the exact peak field is
   not predicted (needs HF inputs). This is why Claim 2 is scored PARTIAL, not
   full quantitative replication.

2. **Radial ansatz.** Winding-1 radial hedgehog only. No 2D relaxation, no
   skyrmion-antiskyrmion pairs, no CP¹/valley sector.

3. **Bare-electron channel is a model.** Δ_e = E_e0 + c_e·b is the standard
   spin-Zeeman quasiparticle cost, not derived from HF here. The non-monotonic
   min-envelope depends on this channel existing and rising with b — physically
   sound, but its slope is a parameter.

4. **Grid edge effects.** The BP scan shows a mild downward drift at very large
   λ=40 (12.44) because the skyrmion tail approaches r_max=400; this is a finite-
   box artifact, not physics. It does not affect the relaxed finite-size
   skyrmions (size ≈ 3–5 ≪ 400).

## What WOULD falsify the replication
- If the relaxed Δ_sk(b) had NO interior minimum (monotone in b), the
  non-monotonic magnetoresistance mechanism would not follow from the sigma
  model and the replication would fail. It does have one (min at b≈0.125).
- If the BP baseline missed 4πρ_s by more than a few %, the energy functional
  would be wrong. It hits it to 0.24 %.
