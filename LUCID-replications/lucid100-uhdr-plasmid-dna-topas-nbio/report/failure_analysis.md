# Failure Analysis — Honest Critique

**Slot:** `lucid100-uhdr-plasmid-dna-topas-nbio`
**Paper:** Masilela et al., Phys. Med. Biol. 71 (2026) 095013
**On-disk verdict:** SPOT-CHECK (analytic), Coverage 4/10, Agreement 9/10
**Queue tag:** REPLICATED
**Backfill date:** 2026-07-06

## Verdict mismatch — flagged

**The upstream queue tagged this slot REPLICATED. The on-disk `REPORT.md` says SPOT-CHECK (analytic). The on-disk verdict is the correct one and is preserved by this backfill.**

Reclassifying this to REPLICATED would misrepresent the level of independent computation performed. No Monte-Carlo track-structure simulation was run. Every "verified" absolute G-value in the report is a *read-through* of the paper's own Table 2 — the tabulated numbers were used as *inputs* to analytic checks (ratios, reductions, monotonicity), not independently computed.

## Primary failure mode: "analytical reduction only, MC never re-run"

This is the exact anti-pattern the backfill brief flagged for TOPAS-nBio family papers. The pattern here is:

1. Paper reports absolute G-values (SSB and DSB, per Gy per Da, at 4 σ points × 2 dose-rate regimes × 2 damage models).
2. Paper also states the mechanism analytically (Eq. 4: `k_obs = 1.32e7 · σ^0.29`) plus the intertrack condition (τ_·OH > ⟨Δt⟩).
3. This replication implemented (2) in Python and confirmed that (2) → the ratios, reductions, and crossovers reported in (1) with <1% error.
4. This replication did NOT re-derive (1). The absolute numbers were consumed as inputs.

**What this proves:** the paper's arithmetic is internally consistent, and its mechanism explains its own numbers.

**What this does NOT prove:**
- That the reported absolute G-values themselves are correct (an independent MC could disagree).
- That the choice of physics list, chemistry deck, geometry, and pulse implementation in TOPAS-nBio was executed as claimed.
- That an alternative simulator (Geant4-DNA opt-4, PARTRAC) would produce the same numbers.
- That the code, if released, would actually reproduce the paper on rerun.

## Specific gaps and their severity

### Severity: **critical** (prevents true replication)

1. **No TOPAS-nBio MC was run.** The condensed-history 225 kVp beam, volumetric e⁻ track-structure stage, IRT chemistry propagation, and per-strand DSB scoring were all skipped. This is not a shortcut — it is the entire core of the paper.
2. **Chemistry decks unavailable.** The paper's Models 1 & 2 `TsChemistry` `.topas` decks are unreleased ("will be released as an example in a future version of TOPAS-nBio"). Without them, even having the TOPAS-nBio binary would not permit reproduction.
3. **Physics-list patches unreleased.** The paper uses TsEmDNAPhysics + ELSEPA elastic scattering + Meesungnoen thermalization, but the specific dev-branch patches on top of TOPAS-nBio v2.0 base are not tagged publicly.

### Severity: **significant** (limits interpretation)

4. **FLASH-vs-conventional comparison partially reproduced.** The UHDR/CONV *ratio* was re-derived from Eq. 4; the underlying absolute G-values on both sides of the ratio come from the paper. So the claim "UHDR reduces DSB by 73.5%" is confirmed to *be consistent with the paper's own arithmetic and its stated mechanism* — but is not independently derived.
5. **Plasmid-to-chromatin extrapolation not addressed.** The paper is pUC19-only. Whether the FLASH sparing signature translates to cellular chromatin (where endogenous σ ≈ 3-7×10⁸ s⁻¹ puts the system *outside* the paper's own predicted-sparing regime) is not tested. This is a fundamental limitation on the paper's biological/clinical relevance, not a defect of this replication — but the replication did not surface or resolve it either.
6. **No cross-code corroboration.** Geant4-DNA standalone and PARTRAC exist and could in principle be driven from the same chemistry list; no such cross-check was attempted. Bertolet 2022 documented 20-30% inter-physics-list variance in DSB yields, so a same-code within-1% agreement is weaker evidence than a cross-code within-15%.

### Severity: **modest** (context-limiting)

7. **11 experimental comparator studies (Table 2) not independently re-verified.** The paper's agreement with experiment relies on percent-reduction values quoted from 11 published works; those primary plasmid-gel datasets were not re-extracted or re-derived.
8. **No Fig. 3 (time-resolved species) reproduction.** Requires IRT chemistry trajectory dumps that only TOPAS-nBio produces.
9. **Bonus 2×10⁹ Gy/s data point not tested.** Read-through only.
10. **Range-cut and DNA-concentration sensitivity sweeps not run.** Read-through only.

### Severity: **minor** (paper-side issues, not this replication's fault)

11. **Two apparent paper-side text errata flagged.** Claim 12 (§3.2 DSB(UHDR) at 1e-3 M DMSO reads 1.62×10⁻⁹ against CONV 1.68×10⁻¹⁰ — inconsistent with "no significant difference" narrative; probable missing exponent). Claim 24 (Eq. 3 oxygen Henry's-law algebra is off by ~5 orders of magnitude while the *value used* is correct). Neither changes the conclusions; both are worth flagging to authors upstream. Not corrected in the replication.

## What a genuinely REPLICATED verdict would require

To upgrade this from SPOT-CHECK to REPLICATED honestly, the following would need to be done:

1. Obtain (or independently reconstruct) the TOPAS-nBio dev-branch physics-list patches.
2. Obtain (or reconstruct from Table 1) the Models 1 & 2 chemistry decks in `.topas` format.
3. Rebuild the 225 kVp SARRP beam vertex spectrum from Miles 2023.
4. Run at minimum a 4-cell matrix (2 dose rates × 2 σ endpoints) on Aurora-class hardware (~50k CPU-h).
5. Re-derive absolute G-values (SSB & DSB) at those 4 conditions.
6. Compare independently-computed G-values to paper Table 2; if within statistical uncertainty (paper reports 2% 1-SD), verdict → REPLICATED.

The full 16-cell matrix at ~1M CPU-h would upgrade to REPLICATED+ but is not required for the verdict change.

## Why this is still worth having on disk

Even without an MC rerun, the analytic pass:
- Confirms the paper's arithmetic is internally consistent (17/18 tested claims within <1%).
- Confirms the stated mechanism (Eq. 4 + intertrack condition) actually explains the reported numerical pattern.
- Catches two paper-side typographical errata worth reporting upstream.
- Provides a fully-scripted, seed-fixed, in-process-assertion-guarded reproduction package that anyone with 30 seconds and Python 3 can rerun.
- Documents the exact blockers (physics patches, chemistry decks, HPC) so a future full replication can pick up cleanly.

That is a legitimate SPOT-CHECK. It is not a REPLICATED, and this backfill will not relabel it.

## Recommended action

- Preserve verdict `SPOT-CHECK (analytic), Coverage 4/10, Agreement 9/10` in the on-disk record.
- Update the upstream queue label from `REPLICATED` → `SPOT-CHECK` (queue-side correction).
- Heartbeat-monitor `topas-nbio/TOPAS-nBio-v2.0` GitHub releases for chemistry deck landing.
- On chemistry deck release, escalate to full MC rerun per `notes/HPC_JOB_PLAN.md` and re-audit for a REPLICATED verdict.
