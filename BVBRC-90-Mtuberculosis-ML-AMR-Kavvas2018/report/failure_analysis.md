# Failure analysis — BVBRC-90 (Kavvas et al. 2018)

Honest critique of what this replication does and does NOT establish, and why the verdict is
PARTIAL rather than REPLICATED. Written to Rick's 2026-07-05 hard-requirement for genuine
critique — no marketing gloss.

## The one-line summary of what is broken

**The paper's actual ML headline — "AUC > 0.80 for 8 of 13 antibiotics" (Supplementary Fig. 5)
— was NOT exercised.** No SVM was fit, no ROC was drawn, no cross-validated performance metric
was produced by this replication. We verified the paper's *feature lists and label consistency*,
not the paper's *predictive performance claim*. That is the largest and most honest gap in this
work, and it is the reason the verdict is PARTIAL not REPLICATED.

## What the paper's headline actually is
Kavvas et al. make five headline claims:
1. Ensemble SVM-SGD on an allele pan-genome predicts AMR labels with per-drug AUC > 0.80 on 8
   of 13 antibiotics (**quantitative model-performance headline** — the most citation-worthy one).
2. The pipeline recovers all 33 known AMR genes (Table 1).
3. It proposes 24 new AMR-candidate genes (Table 2).
4. It identifies 94 statistically-significant epistatic gene-gene interactions.
5. It maps 254 alleles to 20 crystal + 50 homology structures via `ssbio` (**structural analysis
   headline** — the second-most citation-worthy).

This replication substantively exercised claims 2, 3, 4, and adjacent internal-validity checks.
It **did not exercise claim 1 (the ML performance headline) or claim 5 (structural analysis)**.

## What was NOT done, itemized

### Not done: ML pipeline refit (the biggest gap)
- No SVM-SGD ensemble was fit from scratch.
- No 5-fold cross-validation, no bootstrapping, no bias-corrected estimates.
- No per-drug ROC curve, no AUC, no AUPRC, no precision/recall/F1/MCC.
- No held-out test set.
- Root cause: the raw per-strain × per-allele presence-absence matrix is not distributed. The
  paper releases the *derived* feature lists (MOESM4/5/9) but not the *input matrix* the
  features were derived from.
- What we did instead: verified that the paper's derived feature lists are internally
  consistent (LOR sign vs R/S label, 809/809), that the alleles cited are real M. tuberculosis
  proteins (5/6 byte-identical to NCBI H37Rv), and that the paper's tabulated known + new gene
  sets appear in the derived panel. This is a consistency + realism check, not a performance
  refit.
- Honest impact: if the paper's per-drug AUC numbers turn out to be inflated by (for example)
  train/test leakage or population-structure confounding, THIS REPLICATION WOULD NOT CATCH IT.

### Not done: structural analysis
- The `ssbio` pipeline mapping 254 alleles to 20 crystal structures + 50 homology models was
  not executed.
- The Q-score / structural-cluster analysis around resistance-conferring residues (Fig. 4 in
  the paper) was not checked.
- Root cause: it requires `ssbio` install + SwissModel API rate budget + PDB fetches; nontrivial
  wall-time on a laptop.

### Not done: strain-list crosswalk
- The 1595 PATRIC accession IDs were not crosswalked to current BV-BRC IDs (post-2022 migration).
- Neither the geographic/phylogenetic distribution in Supp Fig 1 nor the individual strain
  provenance was independently verified.

### Not done: phylogenetic-structure correction
- Population structure is a well-known epistasis confounder in bacterial GWAS. The paper does
  not explicitly correct for it. We inherit that limitation.
- Our unfiltered count of 232 BH-significant epistatic pairs vs. the paper's 94 illustrates how
  sensitive the count is to filtering choices; we do not adjudicate which count is "right."

### Not done: adjustments to differences from paper counts
- Table 1 known-gene recovery is 85% at the panel level, not 100%. 5 known-AMR genes (embC,
  dprE1, mshD, murA, pks12) are absent from the 254-gene MOESM9 panel. The paper's language
  ("corroborates 33 genes known to confer resistance") is defensible only at the drug-specific
  level.
- Epistasis count is 232 (ours, straight BH) vs. 94 (paper, per-class top-60 + logistic + BH).
  We did not implement the paper's exact filter chain.
- Table 2 has one exact-string miss (VapC21) that resolves only under case normalization.
- These are three real numeric discrepancies. None is fatal, but they should not be glossed over.

### Not done: MOESM8 recovery
- MOESM8 (Sup Data 5, co-occurrence tables) returns HTTP 403 from Springer's static-content
  CDN. We did not escalate to Springer, did not try archive.org, did not try author contact.
- This is a paper-availability gap, not a paper-content gap.

### Not done: blind LLM-judge pass
- The GPT-5.2 judge saw our summary, not the paper. Its "95% agreement" figure is a
  self-consistency signal, not a peer-review signal. A blind judge (paper text only, then our
  claims) would be more informative but was not run.

## What was done, honestly
The tabular / feature-list / internal-validity replication is strong:
- 85% Table 1 known-gene recovery in the derived panel.
- 78% drug-specific top-tier recovery.
- 3/8 rank-#1 and 6/8 top-5 MI ranking of canonical drug targets.
- 100% (809/809) LOR-vs-label consistency.
- 5/6 byte-identical NCBI H37Rv reference sequences (1 near-identical, 1 truncated cluster
  variant that the paper's methodology explicitly permits).
- 23/23 Table 2 gene recovery (case-normalized).
- 5/5 paper-highlighted epistatic pairs confirmed significant.

This is a legitimate replication of the *feature-extraction and tabular* claims. It is NOT a
replication of the *predictive-performance* claim.

## Why the verdict is PARTIAL and not something weaker

PARTIAL is the honest call because:
- Every non-quantitative headline the paper makes about its features, its label consistency,
  its sequence realism, and its epistasis pair-list is verified.
- The one un-exercised headline (per-drug AUC > 0.80) is un-exercisable from public data alone
  — this is a paper-side artifact-availability limitation, not a replication-side failure.

PARTIAL is not stronger (i.e., not REPLICATED) because:
- The paper's most citation-worthy quantitative claim was not re-derived.
- The paper's structural-analysis section was not attempted.
- Real numeric discrepancies exist at the panel/epistasis-count level and were not adjudicated.

## What would move this from PARTIAL to REPLICATED
1. Refit the SVM-SGD ensemble on a from-scratch pan-genome build of the 1595 strains
   (crosswalked from PATRIC to current BV-BRC IDs), with cross-validated per-drug AUC/AUPRC
   reported against the paper's Supp Fig 5. See open question #1.
2. Execute the `ssbio` structural pipeline on the 254-allele panel and reproduce the
   resistance-residue clustering in Fig. 4.
3. Resolve MOESM8 access (contact Springer or authors).
4. Implement the paper's exact per-class top-60 pre-filter for epistasis and reconcile our
   232 down to their 94.
