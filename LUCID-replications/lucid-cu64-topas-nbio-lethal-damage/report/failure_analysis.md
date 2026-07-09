# Failure Analysis — lucid-cu64-topas-nbio-lethal-damage

Honest post-mortem of what this replication did NOT do, and why the verdict is
PARTIAL rather than REPLICATED.

## The single biggest gap: the MC primitive was never re-derived

The paper's original scientific contribution is the number
**0.171 ± 0.003 DSB/decay** for ⁶⁴Cu incorporated on DNA at 0.25 nm from the
axis, computed inside **TOPAS-nBio** with:
- A realistic 9.3 µm spherical nucleus with 6.08 Gbp DNA in 46 chromosomes,
  nucleosomes/chromatin/fractal layout from Zhu et al. 2020.
- Full physical stage (`TsEmDNAPhysics`) + chemical stage (`TsEmDNAChemistry`,
  •OH diffusion and radiolysis).
- `G4RadioactiveDecay` on the ICRP-107 database for the ⁶⁴Cu source.
- 400,000 histories per data point on the "Tochtli-ICN-UNAM" cluster.

**We ran none of this.** Every downstream number in Table 2 anchors on that
primitive; if the primitive is wrong, Table 2 is wrong; and we have contributed
zero independent evidence about the primitive.

## Why we did not rerun (the LUCID MC pattern)

This is the classic LUCID Monte-Carlo cohort pattern, seen across TOPAS,
TOPAS-nBio, PARTRAC, Geant4-DNA papers in this replication set:

1. **License gate.** TOPAS is CC-BY-NC and requires an emailed license key +
   tarball registration. Not fetchable by an unattended subagent.
2. **Build depth.** TOPAS + Geant4 ≥ 10.5 with low-energy EM + nBio extension
   is a multi-hour build even on a well-equipped box.
3. **Compute scale.** 400 k histories × DNA-scale physics + chemistry is a
   parallel-cluster job, not a laptop job.
4. **No public deposit.** No Zenodo/GitHub release of input decks or
   per-event SSB lists. Data-availability = "included in the article."

Any ONE of these could be individually beaten:
- License → email the corresponding author for a research seat;
- Build → keep a pre-built TOPAS-nBio container image on the replication
  cluster;
- Compute → allocate CELS / ALCF Sophia time in advance;
- Deposit → contact author for input decks.

None was beatable in a same-day, unattended subagent run, and we don't
pretend otherwise.

## What our substitute work does and does NOT prove

### R1 (analytic Table 2 rebuild) — strong
Recovers all 5 nuclides in Table 2 to <0.21 % from the paper's own Table 1
DSB/decay values + published half-lives. This is a **genuine** replication of
the analytic chain and would catch any arithmetic error in the paper. It does
NOT catch a systematic error in the MC primitive that feeds it — garbage in,
audited garbage out.

### R2 (DSB scoring rule) — narrow but genuine
Proves the paper's prose ("two opposite-strand SSBs within 10 bp") is
sufficient to reimplement the algorithm from scratch, including edge cases
the paper doesn't explicitly discuss (exactly-10-bp boundary, greedy pairing
under multi-SSB clustering). This constrains the algorithm, not any yield.

### R3 (track-correlated illustration) — indicative only
Fabricated cluster distributions were **hand-tuned** to span the literature
range, not calibrated against any physical model. The resulting DSB:SSB
ratios (0.036, 0.059, 0.161, 0.072) land in the published Nikjoo/Friedland
band, which is a **consistency check on the rule**, not evidence about ⁶⁴Cu.

### R4 (spectrum spot-check) — interpretation-dependent
The paper's "~0.18 e⁻/decay" for ⁶⁴Cu is a **sum over a threshold-dependent
subset** of the Auger cascade. The full ICRP-107 Auger sum is ~1.8 /decay;
the >1 keV subset is ~0.23 /decay; the paper reports ~0.18. All three are
defensible. This flexibility is exactly the sort of thing that makes MC
primitive replication brittle — a factor of ~10 hides in the definition, not
the physics.

## Triage-tag error caught during re-read

Our upstream triage tagged this paper as "DBSCAN clustering for DSB/SSB." It
is not. The paper explicitly uses the Nikjoo/Charlton proximity rule (Methods
§2.2). DBSCAN appears in ref. 34 (the same group's earlier 2020 paper) but
not in this one. We caught this on the Methods re-read. Failure mode:
LLM-driven triage can silently mislabel by neighbourhood.

## What would flip PARTIAL → REPLICATED

Exactly one thing: a from-scratch reproduction of the DSB/decay primitive
that agrees with 0.171 ± 0.003 (at 0.25 nm) and 0.190 ± 0.003 (at 1.15 nm)
within combined stated uncertainty. Best-effort path: open-source Geant4-DNA
build (v11.2+) instead of TOPAS-nBio, per Open Question 1. Expected effort:
1 person-week of build + geometry + 1 cluster-week of compute.

## What would flip PARTIAL → NO-GO
- Discovery that the analytic rebuild (R1) does NOT recover Table 2 at all
  (would indicate paper's arithmetic is off).
- Discovery that the scoring rule as written in Methods is under-specified
  in a way we couldn't work around.
- Neither happened. R1 closed at 0.21 % worst-case; R2 is unit-tested.

## What would flip PARTIAL → SPOT-CHECK
- If we had ONLY done R4 (spectrum spot-check) without R1/R2/R3.
- We did substantially more than that, so SPOT-CHECK understates it.
