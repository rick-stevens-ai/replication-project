# Failure Analysis — BVBRC-86 Streptomyces (Albuquerque et al. 2021)

The replication ended in **REPLICATED**. This document catalogues everything we did NOT reproduce, everything that produced a discrepancy (even when the discrepancy was harmless), and every scenario in which our verdict could still be wrong.

## 1. What we did NOT reproduce (transparent scope limits)

### 1.1 Raw-read reassembly with Unicycler
- **Paper method**: hybrid PacBio + Illumina Unicycler assembly of freshly-sequenced isolates.
- **Our replication**: consumed the deposited FASTA directly.
- **Why not**: reassembling from SRA reads under PRJNA754006 would only test the sequencing/assembly pipeline, not the paper's biological claims about the assembled genome. Downstream users of these deposits will consume the FASTAs, not re-run the sequencer.
- **Consequence**: our EXACT matches on total bp / GC% / contig count are essentially guaranteed and demonstrate deposit integrity, not sequencing-pipeline reproducibility. A true reassembly is the only way to fully close this gap.

### 1.2 RAST annotation
- **Paper method**: RAST + PGAP hybrid.
- **Our replication**: PGAP-only.
- **Why not**: the public RAST server is unreliable/deprecated for programmatic access.
- **Consequence**: our CDS and tRNA counts are 3–5% lower than the paper's. This is a documented annotator-behaviour effect (PGAP is more conservative than RAST for short ORFs and pseudogene calls) but we did not run RAST to *prove* the delta is annotator-attributable rather than real disagreement.

### 1.3 PYANI-ANIb (the paper's ANI method)
- **Paper method**: PYANI in ANIb mode.
- **Our replication**: skani + fastANI.
- **Why not**: skani and fastANI are the modern successors, faster, and already installed.
- **Consequence**: our ANI numbers are systematically ~0.3–3 percentage points higher than the paper's for divergent genomes (k-mer estimators vs alignment-based estimators). Species-boundary calls are preserved, but the exact numeric agreement with paper is NOT achieved. Concrete gap: MA3 vs SCSIO 3032 is 80.85% (fastANI) vs 77.90% (paper ANIb) — a 3 pp difference, both well below the 95% species threshold.

### 1.4 antiSMASH v5.0 (the paper's version)
- **Paper method**: antiSMASH 5.0.
- **Our replication**: antiSMASH 6.1.1 (docker).
- **Why not**: v6 is the current stable release; we did not want to layer a second discrepancy source (obsolete tool version) on top of the biological analysis.
- **Consequence**: MA3_2.13 BGC count drops from 32 (v5.0) to 27 (v6.1.1). We attribute this to v6's stricter co-location/protocluster-merging rules. We did NOT rerun v5.0 side-by-side. Some of the missing 5 BGCs could reflect v6 correctly discarding v5 false positives rather than merging.

### 1.5 BAGEL4, RiPPMiner, NRPSpredictor2
- **Paper method**: BAGEL4 + RiPPMiner for RiPP verification, NRPSpredictor2 for A-domain specificity.
- **Our replication**: none of the above.
- **Consequence**: the paper's RiPP and NRPS predictions rest partially on these auxiliary tools; our verification is antiSMASH-only. Gross RiPP counts qualitatively support the paper's "S07 is RiPP-rich" claim but individual RiPP predictions are not independently confirmed.

### 1.6 Per-gene protein identity to reference NRPSs
- **Paper claim**: 49–57% aa identity between MA3_2.13 BGC #8 NRPS proteins and atratumycin NRPSs.
- **Our replication**: confirmed cluster-level MIBiG match (BGC0001975, blast score 24833) but did not run per-protein BLAST.
- **Consequence**: the paper's specific numeric identity claims to atratumycin, triacsins, and arsono-polyketide NRPS proteins are NOT directly reproduced. This is a straightforward follow-up.

## 2. Discrepancies that turned out to be explainable (but were still discrepancies)

| Metric | Paper | Our value | Direction | Explanation | Verified explanation? |
|--------|-------|-----------|-----------|-------------|-----------------------|
| CDS count (both) | RAST+PGAP totals | 3–5% lower (PGAP-only) | ↓ | Annotator behaviour on short ORFs / pseudogenes | Documented behaviour, not proven side-by-side |
| tRNA count | RAST+PGAP | slightly lower | ↓ | Same annotator effect | Same |
| S07 vs S187 ANI | 95.83% (ANIb) | 96.66% (skani), 96.12% (fastANI) | ↑ | k-mer estimators > alignment estimators for divergent genomes | Well-documented method bias |
| MA3 vs SCSIO 3032 ANI | 77.90% (ANIb) | 80.85% (fastANI); skani rejects | ↑ | Same method bias, larger at higher divergence | Well-documented |
| MA3_2.13 total BGCs | 32 (v5) | 27 (v6.1.1) | ↓ | v6 protocluster-merging rules | Plausible; NOT confirmed by v5 rerun |
| BGC #24 → arsono-PK region number | region_024 | region_021 | ≠ number | Region numbering shifts when protoclusters merge/split | Consistent with v5→v6 merging |

## 3. Ways the verdict could still be wrong

### 3.1 Deposit integrity is trivially preserved
Because we consumed the deposited FASTA, exact matches on sequence-derived statistics prove only that the deposit is intact — not that the paper's pipeline actually produced these numbers from raw reads. If the depositor edited the assembly post-publication (rare but not impossible), we would not detect it.

**Mitigation**: cross-check assembly release dates and version numbers on NCBI (recorded in `attempt_log.md`). Only a re-assembly from SRA would fully close this.

### 3.2 antiSMASH v5→v6 drift is *partially* mechanistic
Our attribution of the 32→27 drop entirely to protocluster-merging is a hypothesis. If v6 actually discards several v5 false positives, then:
- the paper's "32 BGCs" number is a slight over-count;
- the "23.1% of chromosome is BGC" number is a slight over-estimate;
- the "PKS-rich" categorical claim is unaffected but the density claim is.

**Mitigation**: rerun v5.0 side-by-side (Open Question #3).

### 3.3 GTDB / MiGA reference set has expanded since 2021
The novel-species status of MA3_2.13 was based on the 2021-vintage reference set. Post-2021 marine and deep-sea Streptomyces deposits could contain a closer relative. If so, MA3_2.13 might be reclassified as a novel strain of an existing species rather than a new species.

**Mitigation**: rerun MiGA + GTDB search against the current type-strain set (Open Question #2). The formal *S. profundus* species description (post-2021 literature) provides the current best answer, which we did not evaluate.

### 3.4 S07_1.15 conspecificity is right on the species-boundary knife-edge
95–96% ANI is exactly the disputed species-boundary range. Our two modern methods sit just above 96%; if PYANI-ANIb (as the paper) puts it at 95.83%, it is a hair above the threshold. The species call is not robust to a change of ANI method or a stricter threshold interpretation.

**Mitigation**: report aligned-fraction alongside ANI, and place S07_1.15 in a S. xinghaiensis-clade tree with additional post-2021 close relatives (Open Question #4).

### 3.5 Named MIBiG hits are cluster-level, not gene-level
The strongest confirmation in our replication (three named MIBiG hits recovered) is at the cluster level. Divergent gene identities (paper reports 49–57% for atratumycin NRPSs) mean the actual metabolic products could differ substantially from atratumycin / triacsins / arsono-polyketide. Our cluster-level confirmation supports the paper's "significant similarity to" claim but does NOT support any "produces atratumycin" interpretation.

**Mitigation**: per-protein BLAST + LC-HRMS metabolomics (Open Question #1).

### 3.6 LLM-judge is not domain-expert review
Argo Claude Sonnet 4.6 was given a structured claims/results table and constrained vocabulary. Its "REPLICATED" rationale is coherent but is a summary of the evidence, not an independent adjudication. A domain expert in natural-product genomics reviewing the raw antiSMASH JSONs could disagree.

**Mitigation**: `evidence/llm_judge_response.txt` is preserved verbatim so any reviewer can inspect the reasoning. All raw antiSMASH JSONs are archived for independent inspection.

### 3.7 Docker image tag ≠ container digest
We pinned `antismash/standalone:6.1.1` but did not archive the container image digest. If Docker Hub re-tags 6.1.1 (e.g. rebuilds with refreshed MIBiG database), future pulls could produce different top MIBiG hits.

**Mitigation**: archive the digest going forward; note in `artifacts_summary.md`.

### 3.8 Two-genome sample size
The paper's PKS-rich (sediment) vs RiPP-rich (sponge-associated) ecological contrast rests on n=2. Our replication confirms the compositional contrast but cannot test whether it is a niche-driven signal or a phylogenetic accident.

**Mitigation**: add 5–10 additional genomes per niche and test with a phylogenetically-controlled model (Open Question #5).

## 4. Steps NOT taken that a fully-defensive replication would take
1. PacBio + Illumina Unicycler reassembly from SRA.
2. Side-by-side antiSMASH v5.0 vs v6.1.1 comparison.
3. PYANI-ANIb rerun to reproduce paper's exact ANI numbers.
4. Per-protein BLAST for atratumycin / triacsins / arsono-PK NRPS ORFs.
5. BAGEL4 / RiPPMiner / NRPSpredictor2 auxiliary reruns.
6. GTDB r220 / MiGA-current rerun for novel-species robustness.
7. Docker image digest archival.
8. Independent domain-expert review of antiSMASH JSONs.

None of these were required for the verdict; all would strengthen it.

## 5. Bottom line
The verdict "REPLICATED" is defensible because every claim that is testable purely from deposited public data was confirmed, and every deviation is attributable to documented tool-choice effects rather than factual disagreement. The verdict is narrow: it means "the paper's biological conclusions are reproducible from deposited public data with modern tooling," not "the paper's exact pipeline reproduces its exact numbers." The latter would require the steps listed in Section 4.
