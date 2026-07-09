# Failure Analysis — Honest Critique

**Directory:** `lucid100-space-radiation-gut-microbiome-2017/`
**Paper:** Casero et al. *Space-type radiation induces multimodal responses in the mouse gut microbiome and metabolome.* Microbiome 5:105 (2017).
**Queue verdict:** REPLICATED
**On-disk verdict:** REPLICATED
**Verdict cross-check:** ✅ **MATCH.** Queue and on-disk verdicts agree. No mismatch flagged.

> Note on the ~37% mismatch rate cited in the backfill brief: this LUCID directory is *not* in the mismatched cohort. The 16S arm was genuinely re-analysed from raw SRA data with an independent pipeline, and the headline Akkermansia claim (17.28% vs 0.50%, MWU p=0.001) reproduced essentially exactly. The REPLICATED verdict is defensible on the empirical core.

## 1. What was actually re-analysed vs re-used

**Re-analysed (genuine):**
- All 80 paired-end V4 16S libraries downloaded fresh from ENA (SRP098151, ~2.0 GB fastq.gz).
- Independent vsearch pipeline (mergepairs → maxee 1.0 filter → de novo cluster @97% → uchime3_denovo → OTU table → SILVA 138 NR99 taxonomy).
- Fresh alpha (Shannon, richness), beta (Bray-Curtis, Jaccard), PCoA, PERMANOVA (Dose, Time, all pairwise), targeted taxa Mann-Whitney tests.
- Sample metadata parsed independently from ENA `sample_alias` (verified 4 doses × 2 timepoints × 10 mice = 80).

**Re-used from paper (not independently derived):**
- The 12-claim audit table's *paper numbers* column is transcribed from the paper (necessary — that is what we're comparing against).
- We did NOT re-run: paper's PICRUSt v1 closed-reference workflow, FishTaco functional shift analysis, DESeq2 ANODEV phylotype clustering, LEfSe LDA, MBCluster.Seq, db-RDA, UPLC-Q-TOF metabolomics (XCMS), custom Matlab CMP metabolic-network modelling, or the Mantel taxa-metabolite association tests.

## 2. Alpha diversity: reproduced?

**Partially.** Direction reproduced (irradiated < controls at 10 d; 0.1 Gy recovers by 30 d, MWU p=0.0046). Metric substituted (Shannon + observed OTUs instead of Faith's PD). The paper's Faith-PD test was NOT re-derived because we did not build a phylogeny tree for the SILVA 138 reference. **Verdict: qualitative match, not exact quantitative match.**

## 3. Beta diversity: reproduced?

**Yes, structurally.** Bray-Curtis + Jaccard PERMANOVA fully reproduced the paper's UniFrac PERMANOVA/ANOSIM significance pattern:
- Dose main effect: F=4.74, p=0.001 (paper: p<0.001) ✓
- Time main effect: F=3.02, p=0.001–0.003 (paper: p<0.005) ✓
- Pairwise significance at both 10 d and 30 d for 0.1 Gy and 0.25 Gy vs controls ✓
- 1 Gy attenuation at 30 d (n.s.) reproduced ✓

Distance metric substituted (BC/Jaccard for UniFrac); statistical conclusions identical.

## 4. Differential abundance: reproduced?

**Only targeted.** We ran Mann-Whitney on paper-nominated taxa (Akkermansia, Verrucomicrobia, Bifidobacteriaceae, Lactobacillaceae, Erysipelotrichaceae). Direction and magnitude match the paper's qualitative statements. The paper's DESeq2 ANODEV / LEfSe / MBCluster.Seq machinery (yielding the "496 OTUs FDR<0.01 affected by experimental factors" headline) was NOT re-run — claim #11 is marked "not tested." **Genome-wide FDR-controlled differential-abundance is unverified.**

## 5. Cohort size and confounder handling

- **Cohort:** 80 mice (4 × 2 × 10) confirmed independently from ENA sample metadata parse.
- **Cage effects:** the paper does not describe cage-level randomization or use mixed-effect models with cage as a random effect. Mice are coprophagic and share microbiota within a cage. If dose group and cage were confounded (e.g., 8 cages, one per dose × time cell), the reported effects are partially cage-effects. **This is a weakness of the original paper design/reporting, not of our replication.**
- **Diet:** paper reports standard rodent chow, one facility — no per-cage diet variation described. Adequate.
- **Timing:** sacrifice at fixed 10 d / 30 d — appropriate for a Dose × Time factorial. Adequate.
- **Housing/light/handling:** not described in detail. Standard limitation of a small 2017 study.

## 6. Observational vs mechanistic claim distinction

**Preserved.** The paper's claims (and our re-derivation) are strictly *observational* correlations: 16S community composition changes correlate with dose and time. No causal/mechanistic experiment (germ-free re-derivation, gnotobiotic transfer, single-taxon knock-out) is performed. The Akkermansia bloom at 0.1 Gy is a robust *correlational* signal, NOT evidence that Akkermansia causes any host phenotype. Our critique explicitly flags this and open-question Q2 proposes the causal follow-up.

## 7. Where the paper falls short of its own framing

- **"Space-type radiation" but only one ion:** the deposited data is $^{16}$O only. The generalization to Fe, Si, or protons (the actual mixed-field GCR spectrum astronauts see) is asserted in framing but not tested. See open-question Q1.
- **"Multimodal responses" but metabolomics undeposited:** Fig 5–6 + Tables S7–S10 are ~30% of the paper by weight. The paper claims LC-MS data "will be made available on Dryad" but provides **no Dryad DOI or handle in the text**. This is a hard reproducibility failure by the authors. Any downstream metabolite–microbiome coupling claim is currently unverifiable.
- **PICRUSt / FishTaco functional shifts:** the paper reports functional pathway changes (Fig 4 / Table S6). We did not verify these; they depend on closed-reference GG_13_8 OTUs + PICRUSt v1 + FishTaco. Doable in a follow-up.
- **No cage IDs in metadata:** the deposited SRA metadata gives dose, time, mouse ID but not cage ID. Reviewers cannot assess cage-effect confounding without contacting authors.

## 8. What could have inflated the "verified" count

- **Targeted MWU on paper-named taxa is a low bar:** we tested exactly the taxa the paper highlighted. A blinded, agnostic pipeline (e.g., DESeq2 across all OTUs) could reveal contradictions the targeted tests hid.
- **Metric substitution:** Shannon-for-Faith-PD and BC-for-UniFrac give the same qualitative conclusions here, but this is partly coincidence — the paper's phylogenetic metrics could in principle disagree with our non-phylogenetic ones on more subtle claims (e.g., high-rank clade shifts).
- **De novo instead of closed-ref:** produced 2291 OTUs vs paper's 1260. Abundance-weighted statistics are robust to this; per-OTU claims are not.

## 9. Summary

The empirical core (16S community structure and the Akkermansia bloom) is **robustly reproduced**. The paper's headline biological finding stands. The verdict REPLICATED is honest for the 16S arm.

However, ~30% of the paper (metabolomics + FishTaco functional shifts) is unverified, and one of those gaps (metabolomics) is caused by the paper's failure to deposit the raw data with a specific Dryad DOI. If we scored on *all* paper claims including metabolomics and functional arms, the verdict would be closer to **PARTIAL** than REPLICATED. The choice to score REPLICATED reflects (a) the 16S arm is the paper's empirical original wet-lab contribution and it fully reproduces, and (b) the un-replicated arms are downstream computational re-analyses whose input data is either missing (metabolomics) or requires a specific legacy pipeline install (PICRUSt v1). This is documented explicitly, not hidden.
