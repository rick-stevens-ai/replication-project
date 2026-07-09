# Failure Analysis — s100-026 (honest, no whitewash)

## TL;DR

**Queue label:** REPLICATED
**On-disk substance:** PARTIAL / SPOT-CHECK
**Recommended relabel:** PARTIAL (analytical audit only; MC never re-run; one documented numerical disagreement on wt% claim)

The queue tag "REPLICATED" is not supported by the evidence in this directory.
This document explains why, catalogs the gaps, and marks which claims we did and
did not actually verify.

## What was claimed to be replicated

The paper contains three claim clusters:
1. Quantitative Table 3 (6 species × 6 scenarios = 36 enhancement ratios).
2. Qualitative dose/SB/DSB trends (Figs. 7–9) and indirect ≈ 2× direct SB.
3. Numerical model parameters (17.5 eV threshold, 40% OH→SB, 1.0 ns, 10 bp, 0.225 wt%).

## What was actually done

- Encoded Table 3 verbatim from the paper into Python.
- Recomputed per-species min/max/mean/sign statistics from that encoding.
- Recomputed the AuFeNP wt% claim from stated NP geometry under 6 denominator choices.
- Used OH/H mean ratio as a proxy for the "indirect ≈ 2× direct" claim.

That is an **arithmetic audit of the paper's own numbers**. A "PASS" for e.g.
"OH mean enhancement in [2.0, 2.3]" means "the numbers in Table 3 agree with the
summary statistic reported elsewhere in the paper," not "we regenerated OH counts
independently." The distinction matters.

## What was NOT done (the substance of the PARTIAL verdict)

1. **The Monte Carlo pipeline was never re-run.** No TOPAS run, no Geant4, no
   TOPAS-nBio, no mouse-DNA voxel model compiled, no AuFeNP cloud generated, no
   SDD file produced. Not a single history was simulated in this replication.
2. **No SSB/DSB counts were regenerated.** Figs. 7–9 are entirely untested.
3. **No per-species absolute counts were regenerated.** Fig. 10 is untested.
4. **No independent Table 3.** The 36 enhancement ratios were re-typed from the
   paper, not re-derived from simulation.
5. **The one numerical claim we DID test independently — the 0.225 wt% AuFeNP
   loading — failed.** Under six denominator interpretations, we get 0.014%
   (whole cell), 0.047% (nucleus), 0.96% (100-nm shell around nucleus), and other
   variants. None within a factor of 2 of 0.225%. Closest is off by 4×; the most
   natural interpretation (whole cell) is off by 16×. This is not a rounding issue.

## Why the "R² > 0.99" trap does not apply, but a related trap does

There is no fitted curve here, so no unfalsifiable R². The analogous trap is:
"the audit passes because we're checking the paper's numbers against themselves."
That is what happened for Table 3 and for the qualitative signs — it is a self-
consistency check, not an independent replication.

The one **independent** check we ran (wt%) failed. If you weight the audit results
by "amount of independent-of-the-paper information consumed," the honest verdict
is close to NO-GO on the one thing that was independently checkable, and
UNTESTED on everything else.

## Category-level breakdown

| Category | Verdict | Why |
|---|---|---|
| Table 3 numerical arithmetic | PASS (self-consistency) | Paper's numbers agree with paper's summary stats |
| Table 3 sign of enhancement | PASS (self-consistency) | OH/H2/H/H2O2 > 1; H3O+/e_aq < 1, all as claimed |
| Qualitative dose/SB/DSB trends | UNTESTED | Requires MC engine |
| Indirect ≈ 2× direct SB | INDIRECT PROXY ONLY | OH/H ratio is a very loose surrogate |
| Direct-SB 17.5 eV threshold | UNTESTED | Parameter recorded, not exercised |
| OH → SB 40% probability | UNTESTED | Parameter recorded, not exercised |
| 1.0 ns chemistry stage | UNTESTED | Parameter recorded, not exercised |
| 10-bp DSB window | UNTESTED | Parameter recorded, not exercised |
| **0.225 wt% AuFeNP loading** | **FAIL** | 4×–16× off under every geometry we tried |

## Reproducibility blockers surfaced

- Compute envelope unspecified (no wall-clock, no history counts, no memory).
- RNG seeds not pinned for any of the 12 scenario runs.
- AuFeNP coordinate file not published (only the distribution is fixed).
- Mouse-DNA voxel geometry files not tagged to a git rev.
- Stage-1 and Stage-2 phase-space files not published; forces full upstream re-run
  for any Stage-3 perturbation.

## Recommended action

1. **Reclassify this dir from REPLICATED to PARTIAL** in the LUCID harvest ledger.
2. Open a GitHub issue on `AKlapproth/MultiScale_AuNP_TOPAS` asking (a) the volume
   denominator for the 0.225 wt% claim, (b) whether the intermediate .phsp files
   can be released, (c) whether the AuFeNP coordinate dump can be released.
3. If cluster time on uicgpu/Polaris becomes available, budget a Stage-3-only
   sweep at (200 kVp, Center) with 10 seeds to bound the seed-sensitivity gap
   from open question #2 in `open_questions.json`.

## Meta

This directory is one of ~13 out of 33 sampled LUCID dirs where the queue label
"REPLICATED" is misaligned with on-disk substance (~39% mislabel rate observed
this session; Monte Carlo / track-structure-code papers especially prone).
The correct verdict on the evidence in this dir is PARTIAL.
