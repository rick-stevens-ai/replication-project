# Failure analysis — TEXTURE-polar-wang2026

## 1. First-iteration failure (killed at 13 s)

**Symptom.** The initial run with `J=0.35` and a minimum-filter core detector
produced:
- Interlayer correlation saturated at ~1.000 across ALL temperatures (no
  crossover visible; supposed to be the headline signature).
- "Skyrmion count" ~72-77 per LAYER on a 32×32 grid — physically impossible;
  the smallest core radius is ~4, so at most ~6-10 fit.
- χ(T) noisy with no clear peak.

**Root causes.**
1. **`J` too strong.** With J=0.35 the two layers are locked into
   ferromagnetic-like alignment from the very first equilibration step, so the
   interlayer correlation is enforced by construction, not emergent. Fixing
   the crossover requires J that is small compared to the intra-layer
   gradient/Landau scale — J was reduced to 0.05 (roughly 3% of the gradient
   coefficient `g=1.2`).
2. **Core detector was a minimum filter on raw Pz.** Every local pixel dip in
   a noisy Pz map registered as a "skyrmion", inflating the count 10×. Fix:
   detect NMS maxima on the Gaussian-smoothed
   `|P_xy| · max(-Pz, 0)` score with an adaptive threshold. This drops the
   count to a physical 3-8 per layer.
3. **Sample noise on χ.** `sample_every=2` and `n_meas=1000` were too tight
   given the noise level; extended to `sample_every=1`, `n_meas=1200`, plus
   longer equilibration `n_eq=1000`.

**Fix applied and validated.** The second iteration produced a clean
correlation crossover 0.14 → 0.97 and a well-formed χ(T) peak at T≈0.95.

## 2. Post-run honest downgrade of Claim 3

**Symptom.** The auto-scorer initially marked Claim 3 as PASS because
`argmax(|χ'(T)|)` was 1.30 for all three ω tested, satisfying the naïve
"peak_T(ω_max) ≥ peak_T(ω_min)" criterion.

**Why that PASS was wrong.** T=1.30 was the *highest* temperature sampled in
the AC block, and for all three ω the χ'(T) profile monotonically decreased
from 1.30 downward. That means the true peak sits AT OR ABOVE the top of our
sampled range — its position vs ω cannot be measured. A "tie at the endpoint"
is not evidence of a shift; it is evidence that the shift cannot be resolved.

**Fix.** Manually rewrote the Claim 3 record in `work/results.json`:
- `pass: false`
- `observation`: amplitude dispersion (|χ'| shrinks with ω) IS present at
  every T — a necessary but not sufficient condition for relaxor behavior.
- Verdict downgraded from "all-3-PASS" to "Claims 1 & 2 reproduced;
  Claim 3 unresolved".

**Lesson for future subagent runs.** Any peak-shift criterion of the form
"argmax vs ω" MUST reject the case where all argmax values equal a boundary
index. Added this rule mentally; if this replication pattern recurs, promote it
to the skill.

## 3. Known scope limitations (not "failures" — declared up-front)

- 2D grid, mean-field depolarization instead of a 3D Poisson solve.
- Skyrmion "cores" are Pz-down NMS maxima, not verified topological charges.
- No elastic energy, no Sr/Pb layer chemistry, no strain.
- Landau parameters are dimensionless / arbitrary, not fitted to PbTiO3.

These are why the verdict caps at "PARTIAL (mechanism-only)" even with all
claims passed — a full quantitative match to the paper's superlattice would
require the 3D machinery listed above.

## 4. What did NOT go wrong (worth noting)

- FFT Laplacian was stable throughout; no CFL blowup at dt=0.02.
- No NaNs, no runtime errors, no dependency issues.
- Runtime came in at 114 s, well inside the 500 s target and the 1200 s cap.
- Incremental JSON save pattern worked as designed — the first-iteration kill
  left a partial results.json on disk that was cleanly overwritten by the
  successful run.
