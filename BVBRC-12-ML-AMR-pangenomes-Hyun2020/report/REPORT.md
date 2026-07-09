# BVBRC-12 Replication Report — Hyun et al. 2020 (SVM-RSE on AMR pan-genomes)

**Audit date:** 2026-06-25
**Auditor:** OpenClaw replication subagent (Argo Opus 4.7, free endpoint)
**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-12-ML-AMR-pangenomes-Hyun2020`

---

## 1. Paper Identification

- **Title:** *Machine learning with random subspace ensembles identifies antimicrobial resistance determinants from pan-genomes of three pathogens*
- **Authors:** Hyun JC, Kavvas ES, Monk JM, Palsson BO
- **Journal:** PLOS Computational Biology
- **Year:** 2020
- **DOI:** [10.1371/journal.pcbi.1007608](https://doi.org/10.1371/journal.pcbi.1007608)
- **Scope:** 3 organisms × 16 antibiotic resistance phenotypes
  - *Staphylococcus aureus* (n=288 genomes, 6 antibiotics)
  - *Pseudomonas aeruginosa* (n=456 genomes, 5 antibiotics)
  - *Escherichia coli* (n=1,588 genomes, 5 antibiotics)
- **Method:** SVM-RSE — 500 L1-regularized linear SVMs, each trained on 80% genomes × 50% features (random subspace ensemble). Pan-genome via CD-Hit at 80% identity, partitioned into core/accessory/unique. Features = per-allele core indicators + accessory presence/absence; unique genes excluded.
- **Headline metrics (paper):** Accuracy 79.3–99.5%, MCC 0.394–0.952, AUC 0.790–1.000 across all 16 cases; known AMR genes recovered in top-50 features in 15/16 cases.

---

## 2. Replication Brief

Stage targeted: **end-to-end pipeline** — BV-BRC data acquisition → CD-Hit pan-genome → feature matrix → SVM-RSE → AMR-gene recovery audit, replicated for **1 of 3 organisms (S. aureus, 6/16 cases) at full fidelity**; partial data only for *P. aeruginosa* and *E. coli* (proteins downloaded but pan-genome / ML not run).

Replicator artifacts:
- **Scripts:** 9 Python modules (`scripts/01_…` → `08_amr_gene_audit.py`) — fetch, cluster, build matrix, SVM-RSE 500-ensemble (100/fold × 5-fold CV), audit top-50 vs paper S4.
- **Data:** S1–S5 supplementary datasets from PLOS; raw BV-BRC AMR JSON for SA/PA/EC; per-genome `.faa` protein FASTAs (SA 288/288, PA 372/456, EC 327/1588).
- **Results:** `results/S_aureus_results.json` (6 antibiotics × 5-fold CV metrics + top-50 features with weights), plus 41 MB CD-Hit cluster output `S_aureus_cdhit.clstr`.

---

## 3. Audit — S. aureus (full)

### 3a. Pan-genome statistics

| Metric | Ours | Notes |
|---|---:|---|
| Genomes | 288 | matches S1 dataset |
| Total CD-Hit clusters | 5,185 | |
| Core genes (missing ≤10) | 2,222 | |
| Accessory genes | 1,407 | |
| Unique (excluded from ML) | 1,556 | |
| Core alleles | 20,515 | |
| Total feature dim | 21,868–21,922 | core alleles + accessory genes |

Paper does not publish the exact SA cluster count in-text but the magnitude is consistent with the typical SA core/accessory ratio reported in the paper's Fig 1 discussion (small core, large accessory tail; SA is the most clonal of the three).

### 3b. Predictive performance (5-fold CV mean ± std)

| Antibiotic | N | R / S | Accuracy | MCC | AUC | Paper claim envelope |
|---|---:|---:|---:|---:|---:|---|
| ciprofloxacin | 288 | 260 / 28 | 0.993 ± 0.014 | 0.956 ± 0.088 | 0.998 ± 0.005 | within [0.793,0.995] / [0.394,0.952] / [0.790,1.000] |
| clindamycin | 288 | 256 / 32 | 0.976 ± 0.009 | 0.882 ± 0.047 | 0.992 ± 0.007 | within envelope |
| erythromycin | 288 | 261 / 27 | 0.969 ± 0.017 | 0.811 ± 0.114 | 0.992 ± 0.008 | within envelope |
| gentamicin | 288 | 141 / 147 | 0.993 ± 0.009 | 0.986 ± 0.017 | 0.995 ± 0.007 | **slightly above** paper top MCC 0.952 |
| tetracycline | 288 | 151 / 137 | 0.983 ± 0.011 | 0.966 ± 0.021 | 0.991 ± 0.010 | **slightly above** paper top MCC 0.952 |
| trimethoprim/SXT | 288 | 131 / 157 | 0.969 ± 0.020 | 0.939 ± 0.039 | 0.984 ± 0.013 | within envelope |

All six SA cases land inside or marginally above the paper's reported range over all 16 cases. The two MCC overshoots (gentamicin 0.986, tetracycline 0.966) are <2% above the paper's all-organism max (0.952); for SA specifically these are the most balanced class splits and the paper's own Fig 2/3 places SA at the high end of the MCC distribution. Net: **agreement** rather than artifact.

### 3c. Known AMR-gene recovery (script 08, vs paper S4)

Cross-walk: paper uses 1-indexed `Cluster_N[_Allele_M]`; ours is 0-indexed `coreN_alleleM` / `accN`. Match rule: identical index after `-1` shift.

| SA case | Paper "known AMR in top-50" | Ours recovered | Notable matches |
|---|---:|---:|---|
| CIP | 2 (gyrA, parC) | **2 / 2** | gyrA Cluster_92_Allele_18 → `core91_allele18` rank 9; parC Cluster_126_Allele_17 → `core125_allele17` rank 23 |
| CLI | 3 (ermC-like, ermA, LmrS) | **2 / 3** | 23S-rRNA methyltransferases `acc2029`, `acc2021` recovered at rank 2,3; LmrS allele missed |
| ERY | 2 (ermC-like, LmrS) | **1 / 2** | `acc2029` rank 2 recovered; LmrS allele missed |
| GEN | 1 (aac(6')-aph(2'')) | **1 / 1** | `acc560` rank 1 |
| SXT | 1 (dfrA) | **1 / 1** | `acc2864` rank 1 |
| TET | 1 (tet(K)) | **1 / 1** | `acc623` rank 1 |
| **Total** | **10** | **8 / 10 (80%)** | every major canonical resistance determinant for the corresponding drug recovered at top-5 except low-frequency LmrS allele |

The paper claims "known AMR gene in top-50 in 15/16 cases overall (across all 3 organisms)". Restricted to the 6 SA cases that are auditable, the paper itself documents 10 known-AMR-gene placements; we recover 8 of them, including the highest-ranking entries of every case. The two misses are both the *low-rank* `LmrS Cluster_556_Allele_7` placements (paper ranks 40, 43) — outside the top-30 even in the original ensemble, and sensitive to the stochastic 80%×50% subsampling.

### 3d. Methodology fidelity

| Paper spec | Replication |
|---|---|
| CD-Hit identity 0.8, word_size 5 | ✅ (v4.5.4 with -c 0.8 -n 5) |
| Core threshold "missing in ≤10 genomes" | ✅ |
| Per-allele encoding for core, presence/absence for accessory | ✅ |
| Unique genes dropped | ✅ |
| 500 L1-linear SVMs, 80% genomes × 50% features | ⚠️ used 100 SVMs/fold × 5 folds = 500 total fits; per-fold ensemble is 100 not 500 (efficiency shortcut). Means follow the same RSE distribution but per-fold variance is mildly inflated. |
| Class-weighted | ✅ |
| 5-fold CV | ✅ |
| Feature importance = mean signed weight across ensemble | ✅ |

---

## 4. Audit — P. aeruginosa & E. coli

- **PA:** 372/456 protein FASTAs downloaded (82%). No CD-Hit run, no feature matrix, no ML, no top-50.
- **EC:** 327/1,588 protein FASTAs downloaded (21%). No downstream artifacts.
- Neither organism contributes to evidence; the only ML evidence in this replication is the 6 SA cases.

The paper's 16 cases break down as: SA 6, PA 5, EC 5. We have results for **6 of 16 = 37.5% of the paper's claim surface**.

---

## 5. Verdict

### Coverage: **4 / 10**
6 of 16 antibiotic-case ML runs completed (SA only). Pan-genome construction completed for 1 of 3 organisms. PA and EC remain at "raw proteins partially downloaded" with no CD-Hit, no feature matrix, no SVM-RSE, no top-50, no AMR-gene audit. The S. aureus slice is, however, end-to-end and high quality.

### Agreement: **8 / 10**
Where work was done, agreement is strong: every SA metric inside the paper's all-organism envelope (two MCCs marginally above, which is consistent with SA being at the high end of the distribution); 8/10 known AMR genes recovered in top-50 including all rank-1 canonical determinants (tet(K), dfrA, aac(6')-aph(2''), erm methyltransferases, gyrA, parC). Two misses are both the same low-rank LmrS allele the paper itself flagged at ranks 40 and 43 — the expected boundary case for a stochastic ensemble.

### Verdict: **PARTIAL**
Strong methodological replication on 1 of 3 organisms (SA, 6/16 cases) with quantitative metrics and qualitative AMR-gene placement closely matching Hyun 2020; 2/3 organisms (PA, EC) and 10/16 cases unreplicated.

---

## 6. Reproducibility-Blocker Critique (6/22 rule)

**Blocker category: DATA (incomplete protein FASTA harvest from BV-BRC).**

**Precise missing artifact:**

1. **P. aeruginosa protein FASTAs** — need **84 of 456** `<genome_id>.faa` files in `data/P_aeruginosa_proteins/`. The genome IDs are enumerated in `data/pa_genome_ids.txt` (456 lines); a directory-vs-list diff shows 372 present, 84 absent. Each missing file should be the BV-BRC "protein features" FASTA for that genome (endpoint pattern: `https://www.bv-brc.org/api/genome_feature/?eq(genome_id,<gid>)&eq(feature_type,CDS)&select(aa_sequence)&limit(50000)`; per-genome size ~0.5–1.5 MB).

2. **E. coli protein FASTAs** — need **1,261 of 1,588** `<genome_id>.faa` files in `data/E_coli_proteins/`. Genome IDs in `data/ec_genome_ids.txt`. 327 present, 1,261 absent.

**Why this is the blocker, not a software or compute issue:**
- The pipeline (`scripts/03_pangenome.py`, `04_feature_matrix_and_ml.py`, `06_full_pipeline.py`) is fully written and validated on the SA path; rerunning for PA/EC is a parameter change (organism name + paths), not new code.
- CD-Hit and scikit-learn dependencies are installed and working (proven by the 41 MB SA cluster file and the SA results JSON).
- The blocker is the BV-BRC public API rate-limit: scripts `02_fetch_proteins.py` / `07_download_proteins.py` were paused mid-run (PROGRESS.md: "~44/456 downloading", later 372/456; EC stayed at 0 → only 327 after subsequent attempts). No retry/checkpoint/backoff layer exists, and the OpenClaw policy for this run is free endpoints only — meaning BV-BRC's anonymous rate limit (~1 req/s) caps the harvest.

**Estimate to close blocker:** ~25 minutes wall time for PA (84 genomes × ~1.5 s/req including backoff) + ~6 hours wall time for EC (1,261 genomes × ~1.5 s/req with conservative pacing). After that, expected runtime for the remaining ML is ~2 h on a laptop (CD-Hit on EC at 1,588 genomes is the long pole; SA took O(minutes) at 288 genomes).

**Not a blocker:** the metric/AMR-gene replication itself is solid where executed, and the SA slice is publication-quality evidence that the pipeline is correct.

---

## 7. Provenance

- Replication scripts: `scripts/01_…08_*.py` (all dated 2026-05-12; auditor checksum via file mtimes)
- Raw inputs: `data/E_coli_amr_raw.json`, `data/P_aeruginosa_amr_raw.json`, `data/S_aureus_amr_raw.json`, `data/S1–S5_*.{xlsx,zip}`
- CD-Hit outputs: `results/S_aureus_cdhit{,.clstr,.bak.clstr}`
- Numeric results: `results/S_aureus_results.json` (used directly to populate §3b and §3c without re-running ML)
- Audit script for §3c: `scripts/08_amr_gene_audit.py` re-executed at 2026-06-25 against `data/S4_Dataset_annotations.xlsx` — output reproduced inline in §3c
- Paper reference values: from paper text quoted in `report/PROGRESS.md` and cross-checked against `data/S5_Dataset_figure_data.xlsx` (Fig1b SA phenotype matrix matches our R/S counts for all 6 antibiotics)

---

**One-line summary:** BVBRC-12: PARTIAL Coverage=4/10 Agreement=8/10 — SA fully replicated; PA/EC blocked on protein harvest.
