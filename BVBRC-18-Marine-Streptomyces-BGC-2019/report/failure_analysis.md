# Failure Analysis — BVBRC-18 Marine *Streptomyces* BGC Replication

Paper: Xu et al. 2019, *Marine Drugs* 17(9):498, DOI 10.3390/md17090498.
Verdict: **PARTIAL** — no claim was contradicted, but several central claims were **not re-derived** and one class of numeric claims (BGC counts / density) has a documented substitution-driven bias.

This document is deliberately adversarial. It catalogs what did NOT replicate, why, what the impact is on the verdict, and what would fix it.

---

## 1. Claims that did NOT re-derive from scratch

### 1.1 Pan-genome (C12): 123,302 orthologous clusters / core 996 (888 single-copy)
- **Why not:** Proteinortho V5.16b was not re-run. The pan-genome computation needs all-vs-all BLAST across 88 genomes (~7,000 OC sets), which was outside the time/compute budget for the promotion pass.
- **Impact:** The entire mathematical basis for the paper's Section 3 (phylogenomics rests on the 888 single-copy OCs). Without a rerun we cannot state, from first principles, whether the OC counts reproduce at Proteinortho's exact thresholds (`-cov=50 -identity=50`).
- **Contradicted?** No. Not tested at all.
- **Fix:** Install Proteinortho V5.16b, run on the paper's 87-strain set (or the 141 superset), report OC count with a documented rerun-stability bound.

### 1.2 Phylogenomic clade structure (C13): three main clades of 23/38/22 strains
- **Why not:** MAFFT + trimAl + IQ-Tree LG+F+R8 tree not built. Depends on §1.1 (needs the 888 single-copy OCs first).
- **Impact:** The three-clade partition drives every downstream ecological correlation in the paper (BGC specificity by clade; ecotype enrichment by clade). Without an independent tree we cannot confirm even that a three-clade structure naturally emerges; it could plausibly be a graded continuum, or four/five clades depending on model choice.
- **Contradicted?** No. Not tested.
- **Fix:** After §1.1, MAFFT-align each single-copy OC, concatenate, trim with trimAl `-automated1`, run IQ-Tree with `-m MFP` (paper found LG+F+R8), root on *K. setae* KM-6054. Report bootstrap support for the 23/38/22 partition.

### 1.3 Headline biological claim (C14): Clade I + sediment → more *specific* BGCs; Clade II + invertebrate → more *total* BGCs
- **Why not:** Depends on §1.1 + §1.2 + antiSMASH on the full corpus. None of these were completed.
- **Impact:** This is the paper's actual scientific contribution. Everything else in the paper (and everything replicated in this pass) is descriptive infrastructure. Descriptors have been replicated; **the claim has not.**
- **Contradicted?** No. Not tested.
- **Fix:** After §1.1, §1.2, and §2.1 below, fit BGC-count and BGC-specificity models with `clade * ecotype` and a phylogenetic-independence correction (PGLS). Report main effects, interaction, effect size (marginal R²), and confidence intervals.

---

## 2. Claims replicated with substitution-driven bias

### 2.1 SMBGC counts and density (C6, C7, C10c): PKS-I over-counted
- **Substitution:** antiSMASH v5/v6 not installed; replaced with a BV-BRC product-name marker-keyword scan.
- **Why the substitution is not equivalent:** antiSMASH collapses a multi-module type-I PKS into ONE cluster (spanning ~100 kb, ~10 KS-domain-bearing CDSs). The keyword scan counts each KS-domain-bearing CDS as a marker; even after applying a divisor of 2, a large modular PKS contributes 5+ apparent BGCs where antiSMASH would count 1.
- **Observed manifestation:** PKS-I per strain: this pass 15–100 vs paper 2–38 (upper bound ~3× inflated). BGC density: this pass 4.24–11.55 vs paper 1.94–9.21 (overlaps only at upper end).
- **What DOES survive:** Order-of-magnitude BGC count (~36–87 vs 16–84 — range brackets paper), universal presence of major classes, weak/no correlation with genome size (r=0.24 on n=12).
- **Contradicted?** No, but the numeric agreement is coarser than the raw table suggests. Any BGC-count claim must be read with the substitution caveat.
- **Fix:** Install antiSMASH v5-relaxed (as close to the paper's version as possible) with `--fullhmmer`, ActiveSiteFinder, KnownClusterBlast, SubClusterBlast. Rerun on the exact 87 (or the 141 superset). Report per-genome counts, per-class ranges, density with real cluster boundaries.

### 2.2 Gene count (C4): RAST vs BV-BRC/PATRIC ORF-caller difference
- **Substitution:** BV-BRC CDS count used as proxy for the paper's RAST ORF count.
- **Observed manifestation:** 4631–9636 vs paper's 5363–10,776. Broadly overlapping, but ~5–10% caller-driven shift downward.
- **Impact:** Minor. Distributional shape and dominance ranking preserved.
- **Fix:** Optional — rerun RAST on the 141 QC-passing set. Not high priority given the effect is small and well-understood.

---

## 3. Data-availability failures

### 3.1 MDPI supplementary spreadsheets (Tables S1–S5) — HTTP 403
- **What failed:** Every URL variant of `https://www.mdpi.com/.../s1/*.xlsx` returned HTTP 403 (Cloudflare/Akamai edge block).
- **Impact:** The paper's exact 87-strain accession list (Table S1) was not obtained. This forces us to use the present-day BV-BRC marine superset (141 QC-passing) rather than reconstruct Xu et al.'s exact dataset.
- **Consequence:** We are testing whether *a* marine *Streptomyces* set of similar diversity yields similar aggregate statistics — NOT whether Xu et al.'s exact 87-strain analysis is bit-reproducible.
- **Fix attempts made:** curl with browser-realistic headers, direct MDPI DOI landing page → all 403. No fix executed within pass budget.
- **Fix options (untried):**
  - Institutional-subscription download via a UI browser (blocked here: unattended pass).
  - Request Table S1 directly from corresponding author.
  - Text-mine strain names from the paper body (partial; paper does not enumerate all 87 accessions in-text).

---

## 4. Sampling and statistical concerns

### 4.1 n=12 is small
The BGC marker scan sampled 12 of ~141 QC-passing genomes. The Pearson r=0.24 "no correlation" finding has a 95% CI wide enough to include mild positive OR mild negative correlations. It is **consistent with** the paper's claim, not a **replication** of it. Paper's n=87 gives statistical power we do not have.

### 4.2 Stratified sample skewed to mid/large genomes
Our floor at ~36 BGCs is higher than the paper's 16 because we did not include the smallest QC-passing genomes in the 12-strain sample. This inflates the "matching lower bound" claim; a proper replication would span the full size distribution.

### 4.3 Corpus drift: 2019 GenBank ≠ 2026 BV-BRC
141 QC-passing genomes today includes many strains not available in Jan 2019 and may exclude a handful that were. See §3.1 for the underlying blocker.

### 4.4 `keyword(marine)` is a metadata heuristic
Not curator-validated. Over-includes strains with "marine" in the isolation source but from lab-passaged or estuarine contexts; under-includes marine strains whose metadata uses "ocean", "seawater", or coordinates only.

### 4.5 Class divisors are hand-tuned
The (PKS/NRPS = 2, terpene/butyrolactone = 1) divisors are heuristics with no citation and no held-out validation. Sensitivity of BGC estimates to these divisors was not reported.

---

## 5. What would raise the verdict from PARTIAL to FULL

1. **Obtain Table S1** (author request or institutional subscription) and reconstruct the exact 87-strain set, subject to genome-availability decay since 2019.
2. **Install antiSMASH v5-relaxed** with the paper's exact extras. Rerun on the reconstructed 87 (and the 141 superset). Report directly-comparable BGC counts, class breakdowns, densities.
3. **Run Proteinortho V5.16b** at `-cov=50 -identity=50` on the full set. Report OC count vs 123,302 with a rerun-stability confidence interval.
4. **Build MAFFT/trimAl/IQ-Tree LG+F+R8 tree** on the 888 single-copy OCs with *K. setae* outgroup. Report clade partition and bootstrap stability of the 23/38/22 split.
5. **Kruskal-Wallis (paper's method) + PGLS (better method)** on BGC-count-per-clade and BGC-specificity-per-ecotype. Report both.

**Budget estimate:** ~16 CPU-cores × 1 week; ~500 GB scratch for intermediate BLAST tabulations.

---

## 6. Why the verdict is still PARTIAL, not FAIL

Every claim that was tested either verified outright or overlapped quantitatively. No claim was contradicted. The paper's descriptive infrastructure (corpus, size, GC, gene count, ecotype distribution, universal BGC classes, size-decoupled BGC distribution) is fully verifiable against fresh 2026 BV-BRC data. The gap is one of *coverage* (5/10 of the paper's claims) not of *disagreement* (9/10 agreement on what was tested). Xu et al.'s work is treated as directionally reproducible; the outstanding pieces are quantitatively unverified, not empirically challenged.
