# Workflow — BVBRC-12 Replication (Hyun et al. 2020)

Reconstructed from the artifacts and scripts described in `REPORT.md`. Verdict: **PARTIAL** — full end-to-end for *S. aureus* (6/6 cases), partial for *P. aeruginosa* / *E. coli*.

---

## Stage 0 — Paper & supplementary acquisition

- Retrieve the paper (DOI `10.1371/journal.pcbi.1007608`).
- Download PLOS supplementary datasets **S1–S5** into `data/`:
  - S1: genome list per organism (used to define n=288 SA, n=456 PA, n=1,588 EC).
  - S4: known-AMR gene annotations per (organism, antibiotic) → the ground-truth crosswalk for the top-50 audit.
  - S5: figure data — cross-checked against per-organism R/S counts.

**Artifacts produced:** `data/S1..S5_*.{xlsx,zip}`

---

## Stage 1 — BV-BRC data acquisition (script `01_*`, `02_fetch_proteins.py`, `07_download_proteins.py`)

- Pull AMR phenotype JSON per organism from BV-BRC.
- For each genome ID in the paper's cohort, fetch its protein CDS FASTA via the BV-BRC public API:
  `https://www.bv-brc.org/api/genome_feature/?eq(genome_id,<gid>)&eq(feature_type,CDS)&select(aa_sequence)&limit(50000)`.
- Write per-genome `.faa` files to `data/<organism>_proteins/`.

**Coverage achieved:**
| Organism | Target | Got | % |
|---|---:|---:|---:|
| S. aureus | 288 | 288 | 100 |
| P. aeruginosa | 456 | 372 | 82 |
| E. coli | 1,588 | 327 | 21 |

**Rate-limit note:** BV-BRC anonymous API ~1 req/s. Fetch scripts have no retry/checkpoint/backoff layer, so partial runs are the observed failure mode.

**Artifacts produced:** `data/{S_aureus,P_aeruginosa,E_coli}_amr_raw.json`, per-genome `.faa` files, `data/{sa,pa,ec}_genome_ids.txt`.

---

## Stage 2 — Pan-genome construction (script `03_pangenome.py`)

Executed for **S. aureus only.** PA / EC skipped due to Stage 1 gap.

- Concatenate all per-genome `.faa` into a single organism-level input.
- Run CD-Hit: `-c 0.8 -n 5` (80% identity, word size 5), matching paper spec.
- Partition clusters:
  - **Core** = present in `n_genomes - 10` or more genomes (paper rule: "missing in ≤ 10").
  - **Accessory** = present in >1 and <core threshold.
  - **Unique** = present in exactly 1 genome — **dropped from ML**.

**SA pan-genome stats:**
| | count |
|---|---:|
| Total CD-Hit clusters | 5,185 |
| Core genes | 2,222 |
| Accessory genes | 1,407 |
| Unique (dropped) | 1,556 |
| Core alleles | 20,515 |

**Artifacts produced:** `results/S_aureus_cdhit{,.clstr,.bak.clstr}` (41 MB cluster file is the main artifact).

---

## Stage 3 — Feature matrix construction (script `04_feature_matrix_and_ml.py`)

- **Core encoding:** per-allele indicator. Each distinct allele within a core cluster becomes its own feature — a genome carrying that specific allele → 1.
- **Accessory encoding:** presence/absence per cluster.
- **Unique clusters:** excluded (paper rule).
- **Feature dim (SA):** 21,868–21,922 (varies slightly per antibiotic subset).

**Label:** binary R / S from BV-BRC AMR JSON per (genome, antibiotic).

**Artifacts produced:** in-memory feature matrix per (organism, antibiotic) → consumed directly by the ML step; not persisted separately.

---

## Stage 4 — SVM-RSE training + 5-fold CV (script `04_feature_matrix_and_ml.py`, `06_full_pipeline.py`)

Per antibiotic:
- **5-fold stratified CV** on the 288 SA genomes.
- **Per fold: 100 L1-linear SVMs**, each trained on 80% of the training-fold genomes × 50% of features (random subspace).
- **Total fits per antibiotic:** 100 × 5 = 500 (paper spec: 500 per fold; ours is 500 total — a documented efficiency shortcut).
- **Class-weighted** SVMs (paper spec).
- **Feature importance:** mean signed weight across the ensemble.
- **Metrics:** Accuracy, MCC, AUC — mean ± std across folds.

**Artifacts produced:** `results/S_aureus_results.json` with, per antibiotic:
- fold-level and mean ± std Accuracy / MCC / AUC,
- top-50 features by mean signed weight.

---

## Stage 5 — Known-AMR-gene recovery audit (script `08_amr_gene_audit.py`)

- Load paper S4 known-AMR annotations (1-indexed `Cluster_N[_Allele_M]`).
- Crosswalk to our 0-indexed `coreN_alleleM` / `accN` naming via `-1` shift.
- For each SA antibiotic, count top-50 hits and record the highest-ranking match.

**Re-executed 2026-06-25** to populate report §3c.

**Result:** 8 / 10 known-AMR placements recovered across the 6 SA cases (all rank-1 canonical determinants matched; 2 low-rank LmrS placements missed).

---

## Stage 6 — Report & audit assembly

- `report/PROGRESS.md`: progress log (populated during Stage 1 to mark harvest checkpoints).
- `report/REPORT.md`: final audit, verdict, blocker analysis.
- This file (`workflow.md`): reconstruction of the pipeline for reproducibility.

---

## Reproduce (SA only, from a clean checkout)

```bash
cd BVBRC-12-ML-AMR-pangenomes-Hyun2020/

# 0. Supplementary data
#    (S1..S5 must be present in data/ from PLOS)

# 1. Fetch S. aureus proteins from BV-BRC
python scripts/01_fetch_amr_json.py --organism S_aureus
python scripts/02_fetch_proteins.py --organism S_aureus

# 2. Build S. aureus pan-genome
python scripts/03_pangenome.py --organism S_aureus

# 3+4. Feature matrix + SVM-RSE 5-fold CV per antibiotic
python scripts/04_feature_matrix_and_ml.py --organism S_aureus

# 5. AMR-gene recovery audit
python scripts/08_amr_gene_audit.py --organism S_aureus \
    --paper-s4 data/S4_Dataset_annotations.xlsx
```

For **PA / EC**, the same commands with `--organism P_aeruginosa` / `--organism E_coli` are the intended path once Stage 1 protein FASTAs are complete (Stage 1 is the blocker).

---

## What is deliberately NOT part of this workflow

- No SNP-only or k-mer-only baseline (Hyun 2020 does not build one; our replication does not add one).
- No MIC-regression variant — binary S/R only, matching paper.
- No cross-species transfer of trained SA models to PA / EC.
- No wet-lab validation of any recovered top-50 feature.

These are surfaced as open questions in `open_questions.json`.
