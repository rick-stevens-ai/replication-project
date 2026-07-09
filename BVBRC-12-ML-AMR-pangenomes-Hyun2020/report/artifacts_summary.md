# Artifacts Summary — BVBRC-12 Replication (Hyun et al. 2020)

Root: `~/Dropbox/REPLICATE-PROJECT/BVBRC-12-ML-AMR-pangenomes-Hyun2020/`

All entries below are grounded in `report/REPORT.md`; nothing here is fabricated beyond what REPORT.md states.

---

## Scripts (`scripts/`)

Nine Python modules, all dated 2026-05-12. Together they cover: fetch → cluster → matrix → SVM-RSE → audit.

| Script | Role |
|---|---|
| `scripts/01_*.py` | Fetch BV-BRC AMR phenotype JSON per organism |
| `scripts/02_fetch_proteins.py` | Per-genome protein FASTA harvest from BV-BRC |
| `scripts/03_pangenome.py` | CD-Hit clustering + core/accessory/unique partitioning |
| `scripts/04_feature_matrix_and_ml.py` | Feature matrix + SVM-RSE + 5-fold CV per antibiotic |
| `scripts/06_full_pipeline.py` | End-to-end driver invoking Stages 2–4 |
| `scripts/07_download_proteins.py` | Second-pass protein harvest (retry for missing genomes) |
| `scripts/08_amr_gene_audit.py` | Top-50 vs paper S4 known-AMR crosswalk audit |

Scripts numbered `01`, `02`, `03`, `04`, `06`, `07`, `08` are enumerated in REPORT.md; the report describes "9 Python modules" — the two additional modules are not enumerated by name in REPORT.md and are not listed here to avoid fabrication.

---

## Data — supplementary from PLOS (`data/`)

| Artifact | Purpose |
|---|---|
| `data/S1_*.{xlsx,zip}` | Genome list per organism |
| `data/S2_*` | (paper supplementary — present in `data/`) |
| `data/S3_*` | (paper supplementary — present in `data/`) |
| `data/S4_Dataset_annotations.xlsx` | Known-AMR gene annotations — ground truth for the top-50 audit |
| `data/S5_Dataset_figure_data.xlsx` | Figure-1b SA phenotype matrix — used to cross-check R/S counts |

---

## Data — BV-BRC raw AMR phenotype JSON (`data/`)

| Artifact | Notes |
|---|---|
| `data/S_aureus_amr_raw.json` | Complete |
| `data/P_aeruginosa_amr_raw.json` | Complete |
| `data/E_coli_amr_raw.json` | Complete |

---

## Data — per-genome protein FASTAs (`data/<organism>_proteins/`)

| Organism | Target | Present | Missing | % |
|---|---:|---:|---:|---:|
| S. aureus | 288 | 288 | 0 | 100 |
| P. aeruginosa | 456 | 372 | **84** | 82 |
| E. coli | 1,588 | 327 | **1,261** | 21 |

- **Genome ID lists:** `data/pa_genome_ids.txt` (456 lines), `data/ec_genome_ids.txt` — enumerate the intended full cohorts and are the input to a directory-vs-list diff to compute the missing set.

**Impact:** the missing FASTAs are the sole reproducibility blocker (see `failure_analysis.md`).

---

## Results — pan-genome / CD-Hit outputs (`results/`)

| Artifact | Size | Notes |
|---|---|---|
| `results/S_aureus_cdhit` | — | CD-Hit output prefix (SA only) |
| `results/S_aureus_cdhit.clstr` | 41 MB | Full cluster membership — the largest artifact in the replication |
| `results/S_aureus_cdhit.bak.clstr` | — | Backup cluster file |

No PA / EC cluster files exist (Stage 2 was not run for those organisms).

---

## Results — SVM-RSE numeric results (`results/`)

| Artifact | Contents |
|---|---|
| `results/S_aureus_results.json` | Per-antibiotic (6 total) 5-fold-CV Accuracy / MCC / AUC (mean ± std) + top-50 features with mean signed weights |

This JSON is the source of the numeric tables in REPORT.md §3b and the top-50 audit in §3c. It was used directly, without re-running ML, to populate the report.

**Included antibiotics:** ciprofloxacin, clindamycin, erythromycin, gentamicin, tetracycline, trimethoprim/SXT.

No PA / EC results JSON exists.

---

## Report artifacts (`report/`)

| File | Contents |
|---|---|
| `report/REPORT.md` | Canonical audit + verdict + blocker analysis (source of truth for this backfill) |
| `report/REPORT.tex` | LaTeX rendering with dedicated Genuine Critique section |
| `report/open_questions.json` | 5 truly-open questions on encoding, cross-species transfer, model interpretability, MIC regression, class imbalance |
| `report/workflow.md` | Stage-by-stage pipeline reconstruction |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Blocker + methodological caveats |
| `report/PROGRESS.md` | Progress log (referenced in REPORT.md §7; contains harvest checkpoint notes) |

---

## SA pan-genome summary (from `results/S_aureus_cdhit.clstr` per REPORT.md §3a)

| Metric | Value |
|---|---:|
| Total CD-Hit clusters | 5,185 |
| Core genes (missing ≤ 10) | 2,222 |
| Accessory genes | 1,407 |
| Unique (excluded from ML) | 1,556 |
| Core alleles | 20,515 |
| Total feature dim | 21,868–21,922 |

## SA ML summary (from `results/S_aureus_results.json` per REPORT.md §3b)

| Antibiotic | N | R / S | Accuracy | MCC | AUC |
|---|---:|---:|---:|---:|---:|
| ciprofloxacin      | 288 | 260 / 28  | 0.993 ± 0.014 | 0.956 ± 0.088 | 0.998 ± 0.005 |
| clindamycin        | 288 | 256 / 32  | 0.976 ± 0.009 | 0.882 ± 0.047 | 0.992 ± 0.007 |
| erythromycin       | 288 | 261 / 27  | 0.969 ± 0.017 | 0.811 ± 0.114 | 0.992 ± 0.008 |
| gentamicin         | 288 | 141 / 147 | 0.993 ± 0.009 | 0.986 ± 0.017 | 0.995 ± 0.007 |
| tetracycline       | 288 | 151 / 137 | 0.983 ± 0.011 | 0.966 ± 0.021 | 0.991 ± 0.010 |
| trimethoprim/SXT   | 288 | 131 / 157 | 0.969 ± 0.020 | 0.939 ± 0.039 | 0.984 ± 0.013 |

## SA top-50 known-AMR audit summary (from `scripts/08_amr_gene_audit.py` per REPORT.md §3c)

- 8 of 10 documented paper hits recovered (80%).
- Every rank-1 canonical determinant recovered at rank 1: tet(K), dfrA, aac(6')-aph(2''), erm methyltransferases (23S), gyrA, parC.
- 2 misses: both are the same low-rank LmrS allele (paper ranks 40 and 43) in CLI and ERY.

---

## Coverage vs paper's 16-case surface

- 6 of 16 antibiotic cases replicated (all 6 SA).
- 1 of 3 organisms replicated (SA).
- 10 of 16 cases (all PA + all EC) unreplicated.
- Effective replication coverage: **6/16 = 37.5%** of the paper's claim surface.
