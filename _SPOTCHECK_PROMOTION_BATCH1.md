# SPOT-CHECK Promotion Assessment — Batch 1 (12 papers)

**Date:** 2026-06-25
**Assessor:** Ollie subagent (depth 1/1)
**Method:** Read each REPORT.md, judge whether realistic additional work
could promote from SPOT-CHECK → PARTIAL or REPLICATED, or whether
SPOT-CHECK is the honest ceiling (review papers, permanently unavailable
raw data, proprietary closed code, etc.).

Verdict tags:
- **PROMOTABLE→PARTIAL** — concrete tractable work would lift to PARTIAL
- **PROMOTABLE→REPLICATED** — concrete tractable work would lift to REPLICATED
- **CEILING-SPOTCHECK** — SPOT-CHECK is the honest ceiling; further work blocked by paper type or permanent data/code unavailability

---

## One-line verdicts (12)

1. **lucid-actinium-lutetium-dose-effect: PROMOTABLE→PARTIAL — already at PARTIAL+ in re-pass (cov 8/10); central α/RBE/MIRD reproduced; raw wet-lab assays permanently blocked.**
   - Note: the report header already self-classifies as PARTIAL/SPOT-CHECK; the re-pass section explicitly upgrades to "PARTIAL+ → MOSTLY REPRODUCED". This is effectively already a PARTIAL; just needs the master ledger to be retagged.

2. **lucid-patra-polbeta-radiosensitivity: PROMOTABLE→PARTIAL — re-run HDOCK/ClusPro server jobs (~days queue) + WebPlotDigitizer on Figs 5–7 would lift to PARTIAL.**
   - Sequence analysis already found a substantive paper-side error (broken cDNA); LQ refit reproduces DMF~1.8. Server docking is technically reproducible but slow. Wet-lab biology permanently blocked.

3. **lucid100-uhdr-plasmid-dna-topas-nbio: PROMOTABLE→PARTIAL — needs TOPAS-nBio v4.0 dev branch + chemistry decks (author-promised "future release") + ~5k CPU-h on Aurora/uicgpu.**
   - Analytic re-derivation already matches every claim to <1%. Full MC blocked by unreleased chemistry deck. Heartbeat-monitor TOPAS-nBio releases per HPC_JOB_PLAN.md.

4. **lucid-brahme-radiobio-optimization-review: CEILING-SPOTCHECK — single-author review/opinion in predatory venue with no data, no code, no parameter tables.**
   - Only Eq.(1) is analytically auditable (already done, 19/19 PASS). Recommended retag from `candidate_curated` to `NO_GO_REVIEW_ONLY`; replication value lives in primary Brahme refs [1-3, 23, 34, 45].

5. **lucid-skin-inflammation-nfkb-cox2: CEILING-SPOTCHECK — wet-lab paper (3D raft culture, IHC, Western, MTT); only Figs 1/2/7 digitizable, already done with 9/10 agreement.**
   - All quantitative digitizable claims reproduced (PGE2 6.5×→6.4×, all 4 Tukey stars recovered, IC50 re-fit added). Remaining content (raft histology, western blots, IHC) requires wet-lab redo. SPOT-CHECK at 3/10 coverage is structural ceiling.

6. **lucid100-nuclear-fragmentation-carbon-rbe: PROMOTABLE→PARTIAL — IF paper full-text access (paywalled BioOne/Allen Press) becomes available; would unlock per-fragment α/β tables.**
   - Currently paywall-blocked (Unpaywall is_oa=false, no preprint, no PMC, no Zenodo). With PDF access could refit MKM/SMKM/RMF/LEM-I against author's tables. Full TOPAS/Geant4-DNA MC re-run requires author macros (don't exist publicly) + HPC.

7. **lucid100-targeted-alpha-single-cell-monte-carlo-dna-damage: PROMOTABLE→PARTIAL — paper is open-access; needs TOPAS-nBio/Geant4-DNA MC campaign on uicgpu/Aurora to reproduce Tables 2-4.**
   - Decay-chain physics + DBSCAN scoring smoke tests pass. Full MC re-run is explicitly feasible (paper documents methods, OA, no proprietary code) but compute-heavy. This is the clearest "just needs HPC time" candidate.

8. **lucid100-zebrafish-brain-chronic-lowdose-transcriptomics: PROMOTABLE→REPLICATED — raw RNA-seq deposited at GEO GSE206573; re-run STAR+DESeq2 pipeline to recover 27/200/530 DEG counts.**
   - The data IS public. Multi-GB download + multi-CPU-hour STAR alignment + DESeq2 DEG calling per paper's stated parameters would directly test the headline claim. Strongest promotion candidate in the batch.

9. **lucid100-fractionated-lowdose-epigenetic-behavior: CEILING-SPOTCHECK — pure wet-lab in-vivo mouse paper (ROPS DPM, Western, HpaII, behavior); zero raw data deposited anywhere.**
   - Verified no GEO/SRA/PRIDE/figshare/Zenodo/Dryad/GitHub. 7 bar-chart figures, 0 supplementary tables. Recommend retag tier A→C, worktype "figure-digitization only". Permanent ceiling.

10. **lucid100-deinococcus-radiodurans-ir-gene-regulation: CEILING-SPOTCHECK — paper is a review with zero primary data; PARTIAL would require re-defining replication target to surrogate GEO datasets.**
    - Could re-run STAR+DESeq2 on GSE17720/22/24 + GSE95658 raw FASTQs (~2-4 CPU-hr on uicgpu) for a deeper panel cross-check, but that tests primary papers (Blanchard/de Groot, Tsai/Contreras), not Wang 2019. Wang has no first-party numbers to reproduce. Ceiling is structural.

11. **lucid100-friedland-stochastic-dsb-photon-ion-slot67: CEILING-SPOTCHECK — paper closed-access + PARTRAC Monte Carlo proprietary (Helmholtz, never released); triple blocker.**
    - (1) PDF behind T&F paywall, no preprint, S2 abstract elided. (2) PARTRAC code never publicly released as of 2026-06-09. (3) Precursor Friedland 2010 RR1965 parameter tables also closed. Even getting one blocker fixed leaves two more. Hard ceiling.

12. **lucid100-topas-proton-cellular-response: PROMOTABLE→PARTIAL — needs TOPAS-nBio physics stage on HPC (~120k thread-hours) to rerun the 12 energies × 100 runs.**
    - Already 19/19 analytic claims verified; Table A2 numerics reproduce to ±5%. MEDRAS repair code is locally available (`lucid-medras-mc`). Full track-structure MC is the explicit blocker, but everything else is in place. Clear HPC-gated promotion path.

---

## Summary tally

| Verdict | Count | Papers |
|---|---|---|
| **PROMOTABLE→REPLICATED** | 1 | zebrafish (GSE206573 re-analysis) |
| **PROMOTABLE→PARTIAL** | 6 | actinium-lutetium (already de-facto), patra-polbeta, uhdr-plasmid, nuclear-fragmentation-carbon, targeted-alpha-single-cell, topas-proton |
| **CEILING-SPOTCHECK** | 5 | brahme-review, skin-inflammation, fractionated-lowdose-epigenetic, deinococcus-review, friedland-PARTRAC |

## Promotion paths by category

### Fastest (data already public, just needs compute)
- **lucid100-zebrafish-brain-chronic-lowdose-transcriptomics** — GSE206573 → STAR + DESeq2 → recover 27/200/530 DEGs. Multi-GB DL + ~CPU-hours.
- **lucid-actinium-lutetium-dose-effect** — already mostly there; just update master ledger tag.

### HPC-gated (open-access papers, MC compute needed)
- **lucid100-targeted-alpha-single-cell-monte-carlo-dna-damage** — TOPAS-nBio campaign on uicgpu/Aurora.
- **lucid100-topas-proton-cellular-response** — ~120k thread-hours on Aurora.
- **lucid100-uhdr-plasmid-dna-topas-nbio** — blocked on author chemistry-deck release + HPC.

### Server-queue-gated
- **lucid-patra-polbeta-radiosensitivity** — re-run 9 ClusPro + HDOCK jobs over days of free-tier queue.

### Paywall-gated (open question)
- **lucid100-nuclear-fragmentation-carbon-rbe** — if Hartzell 2025 PDF becomes accessible (ILL, paid endpoint), can refit α/β.

### Structural ceilings (cannot promote without changing replication target)
- **lucid-brahme-radiobio-optimization-review** — review, no data.
- **lucid-skin-inflammation-nfkb-cox2** — wet-lab, no raw data deposited.
- **lucid100-fractionated-lowdose-epigenetic-behavior** — wet-lab, no raw data deposited anywhere.
- **lucid100-deinococcus-radiodurans-ir-gene-regulation** — review, no primary data.
- **lucid100-friedland-stochastic-dsb-photon-ion-slot67** — closed paper + proprietary PARTRAC code + closed precursor tables.

---

## Notes on judgement calls

- **actinium-lutetium** is genuinely already at PARTIAL per its own re-pass section (cov 8/10, "MOSTLY REPRODUCED"). Flagging as PROMOTABLE→PARTIAL because the master ledger / verdict line still says PARTIAL/SPOT-CHECK; a tag refresh is the work needed.
- **uhdr-plasmid** has 9/10 agreement but 4/10 coverage. The agreement is high because analytic re-derivation matches every reported number to <1%. To get to full PARTIAL with MC reruns requires author's unreleased chemistry deck; this is a soft block (likely future release) rather than a hard ceiling.
- **zebrafish** is the cleanest promotion candidate: data IS deposited, pipeline IS standard (STAR/DESeq2), the question IS quantitative (27/200/530 DEGs). Would likely reach REPLICATED, not just PARTIAL.
- **skin-inflammation** got 9/10 agreement on its 3/10 testable scope. The remaining 7/10 of the paper is wet-lab biology that no amount of computational work can replicate. Honest ceiling.
- **deinococcus** SPOT-CHECK is at cov 7/10 / agree 8/10, which is unusually high for a SPOT-CHECK — but the structural problem is that Wang 2019 is a review with no first-party numbers. Promoting would mean replicating different papers (Blanchard, Tsai). Not a true promotion of *this* slot.
