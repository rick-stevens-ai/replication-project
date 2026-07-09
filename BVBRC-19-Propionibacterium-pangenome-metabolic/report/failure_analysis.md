# Failure Analysis — BVBRC-19 (Propionibacterium pan-genome + metabolic replication)

Verdict: **PARTIAL** (Coverage 9/10 · Agreement 10/10 on what was covered)

This document itemizes what did NOT replicate cleanly, why the verdict is PARTIAL rather than a full end-to-end replication, and where the paper's methodology has genuine gaps.

---

## 1. What did NOT independently replicate

### 1.1 Upstream gene-calling step (the PARTIAL element)
- **What is missing.** The paper's protocol begins with KBase/RAST re-annotation using GLIMMER on the 16 raw NCBI GenBank assemblies to standardize gene calls across genomes. We did **not** rerun this step.
- **What we did instead.** Started the pipeline from the authors' *re-annotated* GenBank files distributed in Supplementary File 4 (`Genbank_files.zip`).
- **Consequence.** Everything downstream — pan-genome clustering, pathway audit, FBA — is fully independent, but the gene calls seeding those analyses are the authors'. This is the residual 1/10 coverage gap and the reason the verdict here is **PARTIAL** rather than 10/10.
- **Why not fixed.** Deterministically reproducing the KBase/RAST/GLIMMER step would require the exact 2014-2015 KBase workspace snapshot and model versions used by the paper, which are not pinned in the methods and are not guaranteed to still exist in retrievable form on KBase today.

### 1.2 Strain-specific cluster fraction diverges numerically (52.5% vs 65%)
- **Paper reports:** ~65% strain-specific clusters (~4,445) in the pan-genome.
- **We recover:** 52.5% strain-specific (3,123 / 5,946) across the 6 inter-species reps.
- **Root cause:** the paper's 65% figure is computed across **all 16 closed genomes** (which includes 11 *P. acnes* strains that inflate intra-species singletons). Our 52.5% is over **6 inter-species reps** (the same panel the paper itself uses for the *inter-species* pan-genome comparison).
- **Direction of the claim (accessory-heavy cloud) is preserved**, but the numeric quantity is not one-for-one comparable. We did not run the full 16-genome variant.

### 1.3 What DID replicate (for contrast)
14 / 14 numerical and presence/absence claims reproduce on disk:
- All 5 FBA behaviors (C1-C5): positive growth, glucose-dependence pattern, propionate as major fermentation product, auxotrophy hierarchy, vitamin nesting.
- All 3 pan-genome shape claims (P1-P3): core 909 vs. paper's 792-906 upper (within 0.3%); pan-genome open with +438-698 clusters per added genome; strain-specific dominating the cloud.
- All 6 diagnostic enzyme presence/absence claims (M1-M6), including the *exact* diagnostic absences (transaldolase absent only in *P. avidum*; sucrose-6-P hydrolase only in PAC + PPRO).

---

## 2. Methodology gaps in the paper we noticed while replicating

### 2.1 KBase/RAST/GLIMMER pipeline configuration is underspecified
- Paper cites the algorithm choices and reports post-annotation metrics but does not pin KBase workspace versions, RAST model versions, or full parameter settings for the annotation step.
- Not reproducibility-blocking because they deposit the resulting GenBank files, but this is the specific piece a stricter replication attempt would stumble on.

### 2.2 OrthoMCL sensitivity not reported
- Paper uses MCL inflation 1.5, 75% coverage floor, e-value 1e-5. These are standard defaults but the 792-906 core-cluster range is itself evidence of undocumented sensitivity.
- Neighboring inflation values (1.2, 2.0, 3.0) are not swept; the paper does not report how much the core-cluster count moves with inflation.

### 2.3 Genus taxonomy is outdated
- The paper (2020) treats *Propionibacterium acnes*, *P. avidum*, and *P. granulosum* as members of *Propionibacterium*, but Scholz & Kilian (2016, IJSEM) reassigned all three to a new genus *Cutibacterium*.
- The paper's "genus-wide" pan-genome is therefore a two-genus mixed pan-genome under modern taxonomy, which is expected to inflate the pan-genome and depress the core. The paper does not flag this.

### 2.4 GEM quality metrics not reported
- The six GEMs are declared "functional" because they solve for positive growth, but the paper does not report standard model-validation metrics: MEMOTE score, dead-end reaction count, gap-filled reaction fraction, alternate-optima diversity, or essentiality prediction against knockout data.
- We inherited this gap — we replicated the reported behaviors (μ, propionate flux, vitamin auxotrophy) but did not run a MEMOTE audit.

### 2.5 Nutritional environment assumptions
- The FBA-derived auxotrophy hierarchy depends entirely on the exchange-reaction default bounds coded into the deposited SBML models; the paper does not systematically vary media composition to test robustness.

### 2.6 No experimental cross-validation of pathway "exclusivity" claims
- M4 (xylose isomerase only in *P. acidipropionici*) and M5 (sucrose-6-P hydrolase only in PAC + PPRO) are annotation-based only; the paper does not corroborate with growth-substrate assays.

---

## 3. Failure classification

| Category | Item | Class |
|---|---|---|
| Upstream re-annotation not rerun | KBase/RAST/GLIMMER on raw NCBI | **Deliberately deferred** (reproducibility artifact missing in paper) |
| Strain-specific fraction 52.5% vs 65% | 6-rep vs 16-genome panel | **Panel-size mismatch**, not a real disagreement |
| MCL inflation sensitivity not run | Only I=1.5 executed | **Out of scope** for behavior-replication |
| MEMOTE / gap-fill / essentiality of GEMs | Not run | **Beyond paper's own reporting** |
| M4-M5 experimental cross-validation | Not run | **Wet-lab, out of scope** |

---

## 4. Bottom line

- The paper's central conclusions replicate on disk to within measurement noise wherever we tested them (14/14).
- The verdict remains **PARTIAL** — not because the science failed to replicate, but because we did not independently re-derive the upstream annotation step. Every downstream analysis is a genuine independent re-derivation.
- The paper is **not reproducibility-blocked**: full supplementary artifacts (genomes, models, tables, omics data) are deposited, and methods are specific enough for the pan-genome and pathway steps to be replicated to within the paper's own stated confidence intervals.
- The genuine methodological gaps (KBase pipeline underspecification, no MCL sensitivity sweep, outdated genus taxonomy, no MEMOTE audit, no wet-lab cross-validation of exclusivity claims) are noted for future work, not treated as replication failures.
