# Failure Analysis — QC-2302.07395 (Inplace Surface-Code Y Basis)

**Purpose:** enumerate the ways this REPLICATED verdict could still be
subtly wrong, or how it under-supports the paper. Written adversarially.

## 1. What we did NOT independently re-derive

We executed the paper's own released `.stim` circuits (from Zenodo record
7487893). We did **not**:

- Re-derive the twist-defect fusion pattern from first principles.
- Rebuild the stabilizer generators of the fused patch by hand and check
  they match the released circuits' detectors.
- Verify the code-distance claim by direct stabilizer analysis; we only
  observed that the decoder gives sane LERs, which is a *necessary* but
  not *sufficient* distance check.
- Reconstruct the paper's Figures 1–5 illustrations of the fusion procedure.

If the released circuits secretly encode a slightly different construction
than what the paper's prose describes, our replication would not catch it.
Mitigation would be a from-scratch construction pass — out of scope for a
subagent-budget rerun.

## 2. Decoder-gap argument is an *inference*, not a proof

We claim the 1.1–2.6× LER inflation is entirely the correlated-decoder gap,
based on:

- The paper's README explicitly warns pymatching will be worse.
- The inflation grows smoothly with `d`, consistent with more correlated
  errors at higher distances.
- The inflation is **the same pattern across X, Y, Z bases** — not
  Y-specific.

A hostile reviewer could still argue:

- The pattern could equally be a shared detector-error-model construction
  bug in either stim or the released circuits.
- We did not run Google's correlated matching decoder ourselves to close the
  loop; we only compared to their pre-computed LERs.
- Alternative decoders (BeliefMatching, tensor-network) not tried;
  triangulating with a third decoder would harden the claim.

Confidence: high but not airtight.

## 3. Sub-threshold scaling truncated at `d=9`

Paper reports scaling to `d=17`. Distances 11, 13, 15, 17 need
$10^7$–$10^8$ shot budgets. We stopped at `d=9` (worst case
2.3e-4 LER × 500k shots ≈ 115 errors, within budget). The
**large-distance exponent** — which is what a factory design needs —
is therefore only checked at 3 data points on our side.

## 4. Near-threshold regime (`p=0.003`) NOT tested

Paper reports both `p=0.001` and `p=0.003`. Near threshold, sub-extensive
error mechanisms (e.g. hook errors around the twist defect) can dominate,
and the inplace construction concentrates defects along a diagonal.
Not exercised at all → cannot rule out that inplace-Y degrades faster
than expected as `p → p_th`.

## 5. Only SI1000 noise model exercised

- Biased-noise regimes (Z-biased, common in cat-qubit / dual-rail
  architectures) not tested.
- Coherent-error components not tested.
- Leakage not modeled.
- Crosstalk not modeled.

The paper is likewise limited to SI1000, so this is not a *replication*
gap so much as a *scope* limitation both parties share.

## 6. Magic-state distillation end-to-end NOT tested

The paper's motivation (T-factory speedup) is not tested by the paper,
and we did not extend to that regime. Whether the per-Y saving compounds
to real T-state-error-rate savings in a real 15-to-1 or 116-to-12 factory
is an inference from linearity, not an empirical result. This is a real
gap for someone wanting to use this construction to size a superconducting
factory.

## 7. Lattice-surgery composition NOT tested

Related to (6): whether two inplace-Y patches can be merged for a native
$Y_1Y_2$ parity measurement, without XZ-decomposition, is not addressed
in the paper and not tested here. A negative result there would
substantially weaken the practical motivation.

## 8. Hardware-native compilation NOT tested

All work assumes ideal square connectivity + unrestricted CX/CZ. Heavy-hex,
linear-nearest-neighbor, and neutral-atom rearrangement platforms are not
tested. The construction is worst-case if a platform's SWAP overhead
consumes the round-count savings.

## 9. `Y_braid` circuits only exist at `d ≥ 9`

We compared inplace-Y vs braid-Y only at `d=9`. At `d=15` (the paper's
strongest headline plot), we verified qubit counts but did not sample LER
— shot-budget prohibitive. So the "inplace matches braid at scale" claim
is really "inplace matches braid at d=9" in our data.

## 10. `Y_folded` construction discussed but not head-to-head vs `Y_inplace`

The paper compares three Y-basis constructions (inplace, braid, folded).
We sampled folded at `d=3` (Experiment A) and observed it is *worse* than
inplace (9.78e-3 vs 1.376e-2 at d=3, but folded uses `rb=0` while inplace
uses `rb=3` — not a fair head-to-head). A proper folded-vs-inplace
head-to-head at matched `rb` was not run.

## 11. Circuit-integrity chain of custody

We `curl`-fetched `circuits.zip` from Zenodo but did not verify a hash
against a paper-published or independently-recorded SHA. If Zenodo's copy
were ever silently updated (which the DOI mechanism is supposed to
prevent, but is not enforced by us), we would not notice.

## 12. Statistical rigor

Reported LERs use naive Poisson `sqrt(k)/N` error bars, not Wilson or
Jeffreys intervals. At `k ≥ 125` this is fine for `1σ` claims but not for
tight quantitative claims. Not a problem for a REPLICATED headline
verdict; would matter for a PARTIAL / NO-GO adjudication.

---

## Summary

Verdict remains **REPLICATED** — the headline claims are exercised on real
simulations of the paper's own released circuits with an independent open
stack, and the LER offset behaves exactly like the decoder-attributable
gap the paper's README predicts. The residual risks above are almost all
about **scope** (higher distances, other noise models, hardware compilation,
factory composition), not about **correctness** of what we did test.
