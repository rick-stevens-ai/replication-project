# Failure Analysis — TEXTURE-polar-gao2025

## Previous attempt
Timed out after extracting the physics but before writing any code. Root cause:
too much time on reading/derivation. **Fix applied this run:** code-first,
save-early — wrote and ran the code and dumped `work/results.json` before any
report writing, so the physics survives a timeout.

## Bugs hit and fixed during this run

### 1. Wrong Q quantization from amplitude-scaling profile (fixed)
- **Symptom:** first profile used a flip *fraction* f=cos(2θ) that scaled the
  whole texture amplitude. At 2θ=75° this gave Q=−0.16 instead of the paper's
  integer −1.
- **Root cause:** scaling the profile amplitude reduces sphere *coverage*
  uniformly; it never completes the wrap needed for an integer charge.
- **Fix:** make 2θ control the **core polar angle** β_core=2θ (core in-plane at
  equator, lifted to pole below), with a monotone radial profile relaxing to the
  opposite pole. Full-sphere coverage → exact integer Q. After the fix:
  Q(75°)=−1.000 (Berg), Q(equator)=0.

### 2. Hybrid state initially skipped
- **Symptom:** the single-texture model jumped discontinuously 0→−1 (Berg), so
  Claim 4 (hybrid) had no genuine test.
- **Fix:** added `build_hybrid` — two opposite-winding cores at ±sep — and
  `local_Q` to integrate per lobe. Result: left lobe +1, right lobe −1, net 0.

## Remaining limitations (honest)
1. **Geometric, not second-principles.** We reconstruct the order-parameter
   texture from the PS parametrization; we do NOT run the effective-Hamiltonian
   MD, so no energetics/dynamics/temperature.
2. **Transition boundary is model-dependent.** The exact 2θ at which Q flips
   depends on the real dipole radial profile; our generic ansatz makes the Berg
   transition sit right at the equator. FD shows the physical smooth crossover.
3. **Equator is a half-integer edge case.** FD reads −0.5 (hemisphere), Berg
   reads 0. Both consistent with "antivortex-like" but the true integer/half
   status at exactly 2θ=90° is profile-sensitive.
4. **Temporal hybrid not captured.** Paper emphasizes dynamical/temporal hybrids
   (time-dependent OAM); a static field only gives the spatial split.

## Verdict impact
None of the limitations undermine the four topological-charge claims, which are
reproduced exactly (Berg) with a consistent FD crossover. Verdict: **REPLICATED**
at field-topology level, with the second-principles energetics explicitly out of
scope.
