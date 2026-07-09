# BVBRC-13: Progress Log
## Paper: He et al. 2018, BMC Genomics - Comparative genomic analysis of E. faecalis

### Step 1: Paper Retrieval & Analysis ✅
- Paper fetched and read in full
- Key claims extracted (see below)

### Key Quantitative Claims from Paper:
1. **78 strains** analyzed (15 newly sequenced + 63 from GenBank)
2. **Pan-genome**: 10,573 gene families
3. **Core-genome**: 1,361 genes (47.2% of avg 2,884 ORFs/genome)
4. **Average genome size**: 2.94 ± 0.15 Mb
5. **Average ORFs**: 2,884 ± 211 per genome
6. **G+C content**: 37.0–38.0%
7. **Phylogenetic tree**: 4 branches (A=19, B=22, C=16, D=21 strains)
8. **Environment-specific genes**: 293 total (143 blood, 66 dairy, 84 water)
9. **Avg antibiotic resistance genes**: 7.5 per genome
10. **5 core AR genes**: lsaA, emeA, efrA, efrB, dfrE
11. **60 putative virulence factors** (23.8 per genome avg)
12. **116 intact prophages** (in 65 of 78 genomes)
13. **Highest VF count**: V583 with 52 virulence factors
14. **Highest AR count**: 18 genes (DAPTO 516, DAPTO 512, S613, R712, TX0104)

### Strain Sources:
- Blood: 20 strains
- Faeces: 16 strains
- Urine: 10 strains
- Dairy: 18 strains (15 new + 3 from GenBank)
- Water: 11 strains
- Oral: 1 strain
- Multiple sites: 2 strains

### Methods Used:
- SiLiX for homologous gene families (80% identity, 80% alignment length)
- MUSCLE for alignment
- Gblocks for removing unreliable alignment regions
- Gubbins for removing recombination
- FastTree 2.1.8 for ML tree (10,000 bootstrap)
- Scoary 1.6.16 for pan-GWAS (1000 permutations, BH correction p<0.05)
- CARD for antibiotic resistance (E-value <1e-15, identity >85%)
- VFDB for virulence factors (E-value <1e-15, identity >95%)
- PHASTER for prophage identification
- RAST 2.0 + COG for functional annotation

### Step 2: Genome Identification & Retrieval
- Status: IN PROGRESS
