# Failure Analysis / Honest Critique

**Paper:** Maciejewski, Baccari, Zimborás, Oszmaniec (2021), arXiv:2101.02331.
**Verdict:** REPLICATED (reproducible core). This document catalogs the gaps
between what the paper claims and what this replication actually established.

## 1. Was the crosstalk-readout-error model independently reconstructed from the paper's specific hardware calibration data?

**No.** The noise model here is a *synthetic textbook instance* of the paper's
noise class:

- Asymmetric per-qubit measurement matrices `A_i` with `p01=[0.02..0.04]`,
  `p10=[0.06..0.09]` — plausible IBM-era numbers but not extracted from Melbourne
  or Aspen calibration snapshots.
- Cluster `C = {q1, q2}` with an ad-hoc 5-percentage-point crosstalk term.
- 4-qubit system, not 15q Melbourne or 23q Aspen.

**Implication.** Our absolute numbers (30.8x reduction) are *upper bounds* on
what the paper's method can achieve in a clean, well-characterized cluster
regime — they should NOT be compared to Table 1 of the paper on a per-qubit
basis. Only the *qualitative* correlated-vs-TP ordering and the
*order-of-magnitude* reduction factor are directly comparable.

**What a stronger replication would do.** Pull historical IBM Melbourne
calibration data (may still be recoverable from IBM Quantum archives) and
reconstruct a per-qubit `A_i` + cluster response from those numbers. Also
run DDOT circuits on a modern IBM device to characterize a fresh 15q sub-block
and compare. Neither was done.

## 2. Was the correction verified vs the paper's quoted reduction factor?

**Partially.**

- Paper quotes >22x on IBM 15q Melbourne (real hardware, ground-state energy).
- This replication gets 30.8x on |ΔE| in a synthetic 4-qubit cluster.
- Same order of magnitude, same direction, expected to be slightly better than
  IBM because we have perfect `R_true` and no non-cluster noise (leakage,
  drift, T1-during-readout).

**What is NOT verified:** the paper's Rigetti 23q Aspen >5.5x number; the
per-qubit breakdown of where the mitigation gain comes from; whether the
factor grows or plateaus with N.

## 3. Was a comparison against uncorrelated (tensor-product) readout mitigation made?

**Yes** — this is the central comparison, and it is directly exercised.

- Raw noisy: |ΔE| = 0.1721
- Tensor-product mitigation: |ΔE| = 0.0505 (3.4x vs raw)
- Correlated mitigation: |ΔE| = 0.00558 (30.8x vs raw, ~9x vs TP)

The 9x advantage of correlated over TP is the substance of Claims C2 and C3
and matches the paper's qualitative story ("correlated model beats
uncorrelated by a large factor").

**Caveat.** Our synthetic noise model was *designed* with a cluster
crosstalk term (δ=0.05) that TP mitigation cannot capture — so of course
correlated wins. On a hypothetical noise model where crosstalk is
sub-dominant, the correlated advantage would shrink. We did not sweep δ.

## 4. Was the calibration overhead quantitatively addressed?

**No.** This is the biggest single gap in this replication.

- Paper's DDOT protocol: `O(k·2^k·log N)` circuits — the whole scalability
  argument depends on this number.
- This replication: assumes perfect characterization (`R_true` known
  exactly), bypassing the entire characterization cost.
- Consequence: our 30.8x number is the *perfect-characterization limit*.
  Real DDOT introduces a residual that both mitigation strategies inherit;
  the correlated one inherits more of it because it has more parameters to
  estimate.

**What a stronger replication would do.** (a) Implement DDOT circuit
generation with k=2. (b) Vary the number of DDOT shots and record how the
estimated `R_hat` converges to `R_true`. (c) Plot the mitigation quality as
a function of characterization budget. (d) Verify the paper's claim that
`O(k·2^k·log N)` circuits are enough. Not done.

## 5. Other omissions

- **N=4 only.** No scaling sweep. The paper's advantage grows with N because
  `|R_true - ⊗ A_i|` grows.
- **No error bars.** 25-seed averages reported as means only.
- **No comparison to M3, PEC, PEA, or Twirled-Readout-Error-eXtinction
  (TREX).** All of these post-date the 2021 paper but are the current
  competitive baselines.
- **QAOA landscape is qualitative.** Single line-4 MaxCut instance at p=1.
  Paper studies random MAX-2-SAT and SK-model at multiple p.

## 6. Bottom line

- **Headline exercised:** YES. The paper's central claim — that correlated
  response-matrix mitigation beats tensor-product mitigation by a large
  factor on a chip with cluster-structured readout crosstalk — is
  reproduced with the correct sign, correct rough magnitude, and correct
  ordering (correlated > TP > raw).
- **Full hardware numbers reproduced:** NO. Requires access to IBM
  Melbourne or Rigetti Aspen (retired) or a full DDOT run on a current
  device.
- **Calibration cost side of the claim:** NOT reproduced.
- **Scaling side of the claim:** NOT reproduced.

The verdict of REPLICATED is justified under the "reproducible-core"
reading of the wave brief. It would NOT be justified under a
"full-paper-with-hardware" reading — for that, at minimum a fresh DDOT run
on a supported IBM device is needed.
