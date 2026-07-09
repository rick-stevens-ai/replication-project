# BVBRC-91 — Brief

**Paper:** Tekedar HC, Kumru S, Blom J, Perkins AD, Griffin MJ, Abdelhamed H, Karsi A, Lawrence ML.
*Comparative genomics of Aeromonas veronii: Identification of a pathotype impacting aquaculture globally.*
**PLoS ONE** 14(8):e0221018 (2019).
**DOI:** [10.1371/journal.pone.0221018](https://doi.org/10.1371/journal.pone.0221018) — **PMID:** 31465454 — **PMCID:** PMC6715197.
Open access (CC BY 4.0).

## Core claims
1. **Data**: 41 publicly available *A. veronii* genomes (as of 2018-02-21) support a comparative-genomics study; ML09-123 (U.S. catfish, this study) is deposited as GenBank PPUW00000000.
2. **Pathotype**: The U.S. catfish isolate *A. veronii* ML09-123 is nearly identical to the Chinese yellowhead-catfish isolate TH0426, suggesting a shared aquaculture-impacting pathotype (ANI values in the conserved cluster > **99.91%**).
3. **Secretion-system distribution**: T1SS / T2SS / T4P / flagellum core components are conserved in *all* 41 genomes; T3SS / T5SS / T6SS / TAD are **variably** present. In particular, human isolates (AVNIH1/AVNIH2/AMC35/AER397/CECT4257/CCM 4359) and B565 lack T3SS.
4. **Virulence-gene tally**: 207 putative virulence genes identified across the 41-strain panel (29 categories), dominated by secretion systems (68) and adherence (56).
5. **Pan/core genome**: 8,710 total genes in the pan-genome, 2,855 in the core (predicted extrapolated core ≈ 2,791).

## Replication scope (this pass)
- Confirm data availability of all 41 paper strains in BV-BRC / NCBI Datasets today.
- **Directly reproduce the pathotype ANI claim** by downloading the actual ML09-123 (GCA_002906945.1) and TH0426 (GCA_001593245.1) assemblies and running fastANI + skani independently.
- Verify genome-statistic reproducibility (length, contigs, GC%) matches paper Table 1 for both strains.
- Cross-check BV-BRC Specialty Genes (VFDB + Victors + PATRIC_VF) against paper's secretion-system-distribution claim for ML09-123, TH0426 (T3SS+/T6SS+) and AVNIH1 (T3SS-/T6SS-).
- Note that full 41-genome pan/core-genome rerun (EDGAR 2.0 / MUSCLE / RAxML on 2.9 Mb concatenated alignment) is outside the scope of a single-analyst quick replication.
