# Failure Analysis — Honest Critique

## Executive summary
Within scope, this replication is unusually clean: DEG counts unit-exact, %upregulated unit-exact to 2 decimals, top-12 genes overlap 11/12 in each of three groups, all 7 interaction genes recovered exactly, and the paper's central biological narrative independently confirmed by open-source ORA. Nevertheless, the verdict is deliberately kept at **PARTIAL** (not upgraded to REPLICATED) because a substantial and important portion of the paper's pipeline is fundamentally unreachable. This document catalogs what was NOT done and why the PARTIAL label is the honest one.

## Category A — Genuinely unreachable (blocks REPLICATED verdict)

### A1. Raw FASTQ → count matrix
- **Paper does:** Illumina PE reads → Trimmomatic → STAR alignment → featureCounts quantification against a GRCh38-based annotation.
- **We do:** Nothing. No FASTQ, no BAM, no counts.
- **Why blocked:** Authors did not deposit raw reads. The Data Availability statement ("All data generated or analyzed during this study are included in this published article and its additional information files") is technically accurate about the DEG *tables* but is inadequate by 2026 norms for a 156-donor bulk RNA-seq study. No GEO, SRA, or ENA accession is provided.
- **Consequence:** Aligner choice, read-count normalization, low-count-filter thresholds, and gene-annotation version are all taken on trust. We cannot test whether swapping STAR → salmon, or featureCounts → HTSeq, would perturb downstream results.

### A2. Independent voom/limma re-execution
- **Paper does:** Model 1 (per-dose within-group) and Model 2 (interaction across groups) via voom + limma.
- **We do:** Consume the paper's already-computed logFC / adj.P.Val columns from AF1.
- **Why blocked:** Requires the count matrix (A1).
- **Consequence:** Cannot re-derive p-values from scratch, cannot test alternative DE frameworks (DESeq2, edgeR-glmQLF, NOISeq), cannot check method-sensitivity of the p53 fold-enrichment difference between groups.

### A3. IPA proprietary re-run
- **Paper does:** Ingenuity Pathway Analysis for canonical pathways, upstream regulators (E2F1, JUN, MYBL2, TP53, etc.), diseases-and-functions, and network causal-inference z-scores.
- **We do:** Open-source Fisher's-exact over-representation against MSigDB Hallmark, KEGG, and Reactome gene sets.
- **Why blocked:** IPA is proprietary; the QIAGEN knowledge base (curated causal edges) is not freely reproducible.
- **Consequence:** We can match the *biological direction* (p53 is the top hit, DNA-repair only in N0, E2F strongest in N2+) but not the exact IPA z-scores or causal-network scores. The upstream-regulator claim in particular is a claim about IPA's proprietary edge database, not about a computation we can independently reproduce.

### A4. qPCR wet-lab validation of MDM2, CDKN1A, MSH6
- **Paper does:** RT-qPCR validation on a subset of donors (Fig 8).
- **We do:** Nothing.
- **Why blocked:** Wet-lab data. Cannot be replicated in silico by design.
- **Consequence:** Cannot cross-check the qPCR fold-change against the RNA-seq LFC.

## Category B — In-scope but deliberately deferred

### B1. Total expressed-gene count (14,756)
- **Status:** NOT VERIFIED but PLAUSIBLE.
- **Reason:** AF1 stores the union of *significant* DEG rows across combos (8,134 unique genes). The 14,756 figure requires the pre-filter or post-filter count matrix.
- **Assessment:** The number is plausible for a typical human RNA-seq experiment after low-count filtering, but we did not verify it. If the paper's authors ever deposit the count matrix, this is trivially checkable.

### B2. ConsensusPathDB GO clustering
- **Status:** SPOT-CHECK only.
- **Reason:** AF5 contains the paper's GO clustering result table; we did not independently re-run ConsensusPathDB.
- **Assessment:** Low-value target — GO clustering results are consistent with the pathway ORA we did run, and the specific clustering algorithm choices would affect the exact result even in an honest re-run.

### B3. Choice of MSigDB collection version
- **Reason:** We used the MSigDB Hallmark annotations embedded in AF1's "In Geneset" column (i.e., MSigDB version at time the paper's authors curated AF1). If MSigDB Hallmark v7.5 (post-paper) reclassifies a gene into/out of HALLMARK_P53_PATHWAY, the ORA fold-enrichment would drift. We did not test this sensitivity.

## Category C — Sanity checks passed

- No red flags in DEG count unit-matching (three groups × two doses = 6 combos, all six exact).
- The 11/12 vs 12/12 top-gene discrepancy is fully explained by the paper's curation preference for canonical p53-axis genes over raw |LFC| ranking; the discordant genes at rank 12 (FAS, HSPA4L, BBC3) are themselves p53 targets.
- Union of two interaction contrasts (N2+/N1 vs N0, N1 vs N0) produces exactly the paper's 7-gene set — a non-trivial coincidence that would fail if AF1b had been miscurated.

## Why PARTIAL, not REPLICATED
The 8-of-10 coverage / 9-of-10 agreement is genuinely strong, but the two coverage misses (A1 raw pipeline, A2 DE re-execution) are *large* — they cover the entire upstream computational stack. A REPLICATED verdict would imply "we could rebuild this paper from scratch given only the source materials," which is manifestly not true here (we could not; we could only rebuild it from the paper's own already-processed outputs). The strong-PARTIAL label is honest and calibrated.

## What would move this to REPLICATED
1. Author deposits FASTQ to SRA/GEO. Then A1, A2 become tractable.
2. Independent re-run of alignment + DE + downstream produces the same DEG counts (or numerically-close approximation given method drift).
3. Method-sensitivity analysis shows the group-difference biological signal (N0 vs N2+ low-dose p53 gap) survives DESeq2 and edgeR re-runs.

## What would move this to NO-GO
Discovery that the deposited DEG tables (AF1) contain errors or inconsistencies with the paper's main-text numbers. We looked and found none.
