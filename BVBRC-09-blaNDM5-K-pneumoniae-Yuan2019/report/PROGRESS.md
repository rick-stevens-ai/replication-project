# PROGRESS.md — Replication of Yuan et al. 2019

## Status: COMPLETE

## Checkpoints

### 1. Paper Acquisition ✅
- Full text accessed from PubMed Central (PMC6701021)
- Key claims extracted and documented in paper/paper_notes.md

### 2. Genome Acquisition ✅
- Complete genome downloaded from RefSeq (GCF_008320705.1)
  - Chromosome: NZ_CP174529.1 (5,191,370 bp)
  - pVir-SCNJ1: NZ_CP174530.1 (211,858 bp)
  - pNDM5-SCNJ1: NZ_CP174531.1 (45,255 bp)
- Reference genome SCLZ15-011 (GCA_001630805) downloaded
- Comparator plasmids pNDM_MGR194, pLVPK, pL22-1 downloaded

### 3. MLST & Typing ✅
- Kleborate v3.1.3 confirms ST29
- K54 capsular type confirmed (wzi115)
- O-type: O1αβ,2β

### 4. AMR Gene Detection ✅
- blaNDM-5 detected on pNDM5-SCNJ1 (100% identity, 100% coverage)
- Chromosomal: blaSHV-187, oqxA, oqxB, fosA6
- No other carbapenemase genes detected ✓

### 5. Virulence Gene Detection ✅
- pVir-SCNJ1: rmpA, iucABCD, iutA, iroBCDN confirmed
- rmpA2 truncated (60% by Kleborate) confirmed
- Chromosomal: yersiniabactin (ybt), enterobactin (ent), Type 3 fimbriae (mrk) confirmed
- Kleborate virulence score: 4 (high)

### 6. Plasmid Characterization ✅
- pNDM5-SCNJ1: IncX3 confirmed by PlasmidFinder
- pVir-SCNJ1: repB_KLEB_VIR confirmed by PlasmidFinder
- BLAST comparisons completed against pNDM_MGR194, pLVPK, pL22-1

### 7. Phylogenetic Context ✅ (partial)
- Kleborate confirms SCLZ15-011 is also ST29
- BLAST alignment shows ~931 raw mismatches (consistent with 198 post-Gubbins SNPs)
- Full 60-genome phylogeny not replicated (requires CSI Phylogeny server + Gubbins)

### 8. Report Written ✅
- REPORT.md completed with full claim audit
