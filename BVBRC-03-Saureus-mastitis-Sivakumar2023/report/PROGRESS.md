# PROGRESS.md — Sivakumar et al. 2023 Replication

## Checkpoints

### CP1: Paper acquired & claims extracted
- **Time:** 2026-05-05T14:30 CDT
- **Status:** Paper HTML downloaded, text extracted (62K chars)
- **41 NCBI accessions identified** from Data Availability section
- **Key quantitative claims identified** (see REPORT.md)
- **Next:** Query BV-BRC for genome availability, retrieve/annotate

### CP2: Genomes retrieved from BV-BRC
- **Time:** 2026-05-05T14:35 CDT
- **Status:** All 41/41 genomes found in BV-BRC via GenBank accession search
- Genome IDs saved to data/bvbrc_genomes.json
- Full metadata (size, GC, contigs, MLST) saved to data/bvbrc_genomes_detail.json
- Initial stats verified: mean=2.71 Mbp, GC=32.7%, contigs 24-132

### CP3: MLST analysis complete
- **Time:** 2026-05-05T14:38 CDT
- 15 unique STs confirmed (exact match)
- ST2454:17, ST2459:5, ST4968:4, ST5:2, ST672:2, ST4967:2, plus 8 singletons
- 5 CCs confirmed: CC8(21), CC97(10), CC5(3), CC1(2), CC30(1)

### CP4: AMR gene analysis complete
- **Time:** 2026-05-05T14:42 CDT
- 3,047 AMR specialty gene records retrieved
- All 41 MSSA confirmed (0/41 methicillin resistant)
- blaZ: 14/41 (exact match)
- Core efflux pumps (norA, arlR, mgrA, lmrS): all 41/41
- AMR gene matrix saved to analysis/amr_gene_matrix.tsv

### CP5: Virulence factor analysis complete
- **Time:** 2026-05-05T14:45 CDT
- 5,695 VFDB records retrieved across 41 genomes
- 131 unique VF genes (paper: 108)
- Key VFs verified: hemolysins, ica operon, PVL, sak, tsst
- VF gene matrix saved to analysis/vf_gene_matrix.tsv

### CP6: Pangenome & phylogeny complete
- **Time:** 2026-05-05T14:50 CDT
- PLFam pangenome: 3,412 total (core:2089, soft-core:137, shell:449, cloud:737)
- UPGMA tree from PLFam distances reproduces 6 clade structure
- Distance matrix and Newick tree saved to analysis/

### CP7: REPORT.md written
- **Time:** 2026-05-05T14:55 CDT
- 33 testable claims identified, 31 tested (94%)
- 23 verified, 6 partially verified, 0 contradicted, 2 not tested
- Verdict: **REPLICATED**

### Key Paper Claims (extracted for testing)
1. 41 strains sequenced
2. Mean genome size 2.7 Mbp, avg GC 32.7%
3. Pan-genome: 4,360 total genes
4. Core genome: 1,878 genes (shared by >99% strains)
5. Soft-core: 215, Shell: 717, Cloud: 1,550 genes
6. 15 sequence types (STs) identified
7. 5 clonal complexes (CCs)
8. CC8 largest (21/41), CC97 second (10/41)
9. ST2454 most common (n=17), ST2459 (n=5), ST4968 (n=4)
10. 6 major phylogenetic clades
11. 16 different spa types, 8 untypeable
12. 17 different AMR genes identified
13. All 41 strains MSSA (no mecA/mecC)
14. 108 virulence factors detected
15. 2,293,099 variant positions with 84.4% coverage (SNP analysis)
16. tsst found in 14 genomes
17. PVL (lukF-PV, lukS-PV) in only 1 strain (A3.1)
18. ica operon in all strains (>98%)
19. Pan-genome almost closed (power-law b=0.0817389)
