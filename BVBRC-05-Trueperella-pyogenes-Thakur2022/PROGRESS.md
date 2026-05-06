# PROGRESS — Thakur et al. 2022 Replication

## Status: COMPLETE ✅

### Step 1: Paper Fetch ✅
- PDF saved to paper/thakur2022.pdf
- All quantitative claims extracted

### Step 2: Strain Identification ✅
- 19 strains identified with NCBI RefSeq accessions
- Saved to data/strain_accessions.tsv

### Step 3: Genome Download ✅
- 19/19 genomes downloaded from NCBI FTP
- All verified by size comparison

### Step 4: Annotation ✅
- Prokka v1.14.6 annotation complete for all 19 strains
- CDS counts match paper exactly

### Step 5: Analyses ✅
- Pan-genome: Roary 3.13.0 (substitute for EDGAR 3.0)
- ANI: FastANI 1.34 (all pairs ≥97.83%)
- Phylogeny: FastTree (core genome, GTR model)
- VF: BLASTN for plo, nanH (both universal)
- AMR: abricate + CARD database

### Step 6: Claims Testing ✅
- 15 quantitative claims tested
- 11 verified, 4 partially verified (tool differences), 0 contradicted

### Step 7: Report ✅
- report/REPORT.md written per AUDIT_PROTOCOL.md
- Verdict: REPLICATED

## Conda Environment
- Name: tpyo
- Tools: prokka, roary, fasttree, fastani, pyani, blast, abricate, biopython, pandas, scipy
