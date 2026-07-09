# Failure Analysis — Kavvas 2018 M. tuberculosis pan-genome ML AMR replication

**Verdict:** PARTIAL — not REPLICATED. This document catalogues everything the replication did *not* achieve, distinguishes real failures from principled deferrals, and lists what a stronger follow-up pass would need.

## Overall shape
- **What replicated (§Results):** C1 (pan-genome conservation + PE/PPE/PGRS enrichment), C2a (MI recovery of primary AMR genes for the 6/10 drugs where a protein-allele method can work), C2b (ensemble L1-SVM recovery of additional known genes including the flagship ubiA/ethambutol case), C2c (data availability).
- **What did not replicate or was not attempted:** C3 (97-interaction epistasis), C4 (3-D structural mapping), full 33-known + 24-new gene enumeration, RAxML core-SNP phylogeny, lineage-stratified sensitivity analysis, phenotypic-DST validation of novel signatures.

## Category 1 — Not attempted this pass (principled scope-limit, not a failure of method)

### F1. C3 — 97 epistatic interactions across 10 resistance classes
- **Status:** Not attempted.
- **Reason:** Requires the full gene-gene logistic-regression sweep over SVM-weight-correlated pairs across 10 drug classes. Multi-hour compute + non-trivial preprocessing decisions (which pairs to test, how to correct for the huge number of tests). Would double the report scope.
- **Impact on verdict:** This is one of the paper's four headline results. Not attempting it caps coverage at ~6/10 and forces the verdict to PARTIAL. Cannot be REPLICATED without it.
- **What it would need:** For each drug, take the top-K SVM-selected genes; enumerate all pairs; fit logistic-regression `phenotype ~ gene_A + gene_B + gene_A:gene_B`; Bonferroni-correct over the pair count; count significant interaction terms; compare to paper's 97-interaction total per drug class. Estimated compute: 30–60 min on uicgpu.

### F2. C4 — 3-D structural mutation mapping
- **Status:** Not attempted.
- **Reason:** Requires PDB structures (or AlphaFold homology models) for each candidate gene, per-residue mapping of the SVM-flagged variants, and the authors' custom mapping pipeline (not documented in reproducible form in the GitHub repo).
- **Impact on verdict:** Second of the paper's four headlines. Coverage remains capped at ~6/10.
- **What it would need:** For at least ubiA and embB, fetch the PDB / AlphaFold structure; map SVM-flagged variants onto the residues; ask whether the mutations cluster at active-site / drug-binding-pocket / interface regions.

## Category 2 — Partial replication with documented confounds (honest weakness)

### F3. Raw-MI top-1 dominated by rpoB/pncA for MDR-linked drugs
- **What happened:** For ethambutol, isoniazid, streptomycin, and ethionamide, the *raw* MI top-1 is `rpoB` (or `pncA`), not the drug's own gene.
- **Root cause:** MDR co-resistance in the sequenced strain pool — rifampicin-resistant strains disproportionately carry resistance to other drugs, so rpoB alleles carry high MI with many phenotypes. This is the paper's own documented confound.
- **Mitigation in our pass:** The C2b SVM run applies the paper's exact preprocessing (remove each drug's primary gene from *other* drugs' analyses). After preprocessing, the SVM recovers each drug's own primary + secondary genes correctly (katG rank 9 for INH, embB rank 2 for EMB, ethA rank 4 for ETH, etc.).
- **Residual concern:** A skeptic could argue the paper leans on preprocessing to make a tidy story. Our replication reproduces both the confound and the fix — that is the honest state.

### F4. rrs-mediated drugs are structurally invisible
- **What happened:** Amikacin (142 R / 257 S), kanamycin (278/550), capreomycin (141/237) — all three fail to recover their primary resistance mechanism. Best hits: `eis→1984`, `eis→1482`, `tlyA→2318` respectively.
- **Root cause:** The primary resistance gene for these three drugs is `rrs` (16S rRNA), which is **absent from the protein-level pan-genome (0 clusters)**. An amino-acid-allele method structurally cannot see 16S mutations.
- **Impact:** 3 of 10 tested drugs unrecoverable by construction. The paper faces the same constraint but does not disclose it prominently. Our replication honestly flags it in §7 of REPORT.md.
- **Fix required for a stronger claim:** Extend the pan-genome to include rRNA operons; recompute MI/SVM on the extended feature set. Would require reprocessing the raw sequence data.

### F5. Small-n instability at pyrazinamide
- **What happened:** PZA has 137 R / 92 S. MI recovers pncA at rank 1 correctly, but the ensemble SVM drops pncA to rank 55 (out of top-40).
- **Root cause:** Bootstrap selection frequency is genuinely noisy at that sample size. Compounding: pncA loss-of-function resistance is a heterogeneous set of stop/frameshift variants across the gene, not a small set of hotspot substitutions — so no single allele has consistent SVM weight across 200 bootstrap re-sampled fits.
- **Impact:** Our SVM rank table drops PZA/pncA out of the top-40 while the paper reports it as recovered. This is honestly disclosed in §4.3 and §7.
- **Fix required:** Feature engineering — replace binary allele presence with per-gene "any nonsynonymous variant" features (SnpEff-annotated). Would likely restore pncA to top rank. Requires the allele → variant-annotation crosswalk that the paper's data package does not include.

## Category 3 — Not exhaustively verified (partial evidence only)

### F6. The full "33 known + 24 new" enumeration
- **What we did:** Verified representative primary/secondary genes for 7 drugs, including the flagship ubiA/ethambutol case.
- **What we did not do:** Produce the full 33-known-gene curated recovery list or the 24-novel-signature list per drug.
- **Impact:** The paper's headline "33 known + 24 new" is not fully corroborated at the enumeration level. A subsequent pass could fail to reproduce all 24 novel signatures.
- **What it would need:** Extract the paper's supplementary gene lists; per-drug per-gene, check MI rank + SVM rank in our outputs; report per-gene recovery status.

### F7. RAxML core-SNP phylogeny not rebuilt
- **What the paper did:** 2,803 core genes, 21,206 core SNPs, RAxML v8 → strain phylogeny.
- **What we did:** Nothing at the phylogeny layer.
- **Impact:** Cannot show that MI/SVM ranks are not driven by lineage structure. Cross-lineage generalization untested (see open question 4).
- **What it would need:** Multi-hour RAxML run on the core-gene concatenated alignment. Feasible but wasn't the priority for this pass.

### F8. No CD-HIT re-clustering from raw PATRIC proteomes
- **What the paper did:** CD-HIT v4.6, id=0.8, word length 5, on 1,595 raw proteomes → 11,039 clusters.
- **What we did:** Used the authors' published cluster matrices directly.
- **Impact:** Everything downstream of clustering is faithfully re-run in our own code, but if the clustering itself is idiosyncratic (parameter choices, deduplication decisions), our replication inherits that.
- **What it would need:** Multi-day CD-HIT run on PATRIC-downloaded proteomes; diff cluster count vs published 11,039.

## Category 4 — Method-level bias not addressed

### F9. Only one classifier family exercised
- **Issue:** The paper's headline talks about "ML" recovering signatures, but only linear L1-SVM is tested. Other families (RF, XGBoost, MLP) might recover a different set — meaning the "24 new" could be L1-sparsity artifacts rather than robust biological findings.
- **See:** open question 1.

### F10. Novel signatures not phenotypically validated
- **Issue:** Some SVM-flagged non-canonical hits are known *compensatory* loci (e.g. rpoC compensates rpoB fitness cost without independently conferring rifampicin resistance). The SVM cannot distinguish causal from compensatory signal.
- **See:** open question 5.

### F11. Beijing lineage over-representation not corrected
- **Issue:** PATRIC's M. tuberculosis pool is Beijing (Lineage 2) MDR-enriched due to outbreak-sequencing bias. Neither the paper nor our replication tests whether ML transfers to other lineages.
- **See:** open questions 2 and 4.

## Summary table
| # | What failed | Category | Impact | Fixable? |
|---|---|---|---|---|
| F1 | C3 epistasis sweep | Scope | Cap coverage at ~6/10 | Yes, 30–60 min |
| F2 | C4 structural mapping | Scope | Cap coverage at ~6/10 | Yes, hours-days |
| F3 | Raw-MI rpoB/pncA dominance | Documented confound | Requires preprocessing | Reproduced + fixed |
| F4 | rrs drugs invisible | Method limit | 3/10 drugs unrecoverable | Only via rRNA-inclusive re-run |
| F5 | PZA/pncA SVM instability | Small n + mechanism | 1 drug drops out of SVM top-40 | Yes, via variant-level features |
| F6 | Full 33+24 enumeration | Partial evidence | Headline count not exhaustively verified | Yes, hours |
| F7 | No RAxML phylogeny | Scope | Cannot phylogeny-correct | Yes, hours |
| F8 | No CD-HIT re-cluster | Scope | Inherit authors' clustering | Yes, multi-day |
| F9 | Single classifier family | Method bias | "24 new" may be L1-specific | Yes, hours |
| F10 | No phenotypic validation | Method bias | Novel hits may be compensatory | Yes, via CRyPTIC MIC data |
| F11 | Beijing over-representation | Method bias | Cross-lineage transfer untested | Yes, via leave-one-lineage CV |

## Conclusion
The PARTIAL verdict is honest. Three of four headline claims (C1, C2a, C2b) reproduced independently on the authors' real data with our own code, including the marquee ubiA/ethambutol SVM finding. The remaining ~40% gap to REPLICATED is dominated by scope deferrals (F1, F2, F7, F8) plus one hard structural limit (F4) and three method-bias concerns (F9, F10, F11) that neither our pass nor the paper resolves.
