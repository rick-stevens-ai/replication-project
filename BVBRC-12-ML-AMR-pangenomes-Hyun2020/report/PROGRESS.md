# BVBRC-12 Replication Progress

## Paper
Hyun et al. (2020) "Machine learning with random subspace ensembles identifies antimicrobial resistance determinants from pan-genomes of three pathogens"
DOI: 10.1371/journal.pcbi.1007608

## Status: IN PROGRESS

### Step 1: Paper Analysis ✅
- Fetched and read full paper from PLOS Computational Biology
- Identified 3 organisms, 16 antibiotic cases, methodology
- Key method: SVM-RSE (500 SVMs, 80% genomes, 50% features, L1 regularization)
- Pan-genome: CD-Hit clustering at 80% identity, core/accessory/unique classification

### Step 2: Data Acquisition ✅ (S. aureus), IN PROGRESS (PA, EC)
- Downloaded supplementary datasets S1-S5 from PLOS
- Retrieved genome IDs: SA=288, PA=456, EC=1588
- Fetched AMR phenotype data from BV-BRC API
- Protein sequences:
  - S. aureus: 288/288 complete (810,770 proteins)
  - P. aeruginosa: ~44/456 downloading...
  - E. coli: 0/1588 pending

### Step 3: Pan-genome Construction ✅ (S. aureus)
- CD-Hit v4.5.4 run with identity=0.8, word_length=5
- S. aureus results:
  - Total clusters: 5,185
  - Core genes (missing ≤10): 2,222 (20,515 alleles)
  - Accessory genes: 1,407
  - Unique genes: 1,556 (excluded from ML)
  - Total features: 21,922

### Step 4: Feature Matrix & ML ✅ (S. aureus)
- Built binary feature matrix (288 × 21,922)
- Core allele + non-core gene presence/absence encoding
- Trained SVM-RSE (500 SVMs, L1 linear SVC, class-weighted)
- 5-fold cross validation (100 SVMs per fold for efficiency)

### Step 5: S. aureus Results ✅

| Antibiotic | N | R | S | Accuracy | MCC | AUC |
|---|---|---|---|---|---|---|
| ciprofloxacin | 288 | 260 | 28 | 0.993 | 0.956 | 0.998 |
| clindamycin | 288 | 256 | 32 | 0.979 | 0.900 | 0.992 |
| erythromycin | 288 | 261 | 27 | 0.972 | 0.839 | 0.990 |
| gentamicin | 288 | 141 | 147 | 0.993 | 0.986 | 0.995 |
| tetracycline | 288 | 151 | 137 | 0.983 | 0.966 | 0.993 |
| trimethoprim/SXT | 288 | 131 | 157 | 0.969 | 0.939 | 0.985 |

Paper's reported ranges (all 16 cases): Accuracy 79.3-99.5%, MCC 0.394-0.952, AUC 0.790-1.0

Our S. aureus results fall within or slightly above the paper's ranges.

### Step 6: P. aeruginosa & E. coli — PENDING
- Protein downloads in progress (rate-limited by BV-BRC API)
- Will run same pipeline when data is available

### Step 7: Report — PENDING
- Will write REPORT.md following AUDIT_PROTOCOL.md
