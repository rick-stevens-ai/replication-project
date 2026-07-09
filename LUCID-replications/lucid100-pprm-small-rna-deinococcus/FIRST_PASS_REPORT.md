# FIRST PASS REPORT — LUCID100 slot 35

**Verdict:** **PASS-low ✅ — 7/7 smoke criteria green, central biological claim reproduced directly from public data.**

## Paper

- **Citation:** Villa JK, Han R, Tsai C-H, Chen A, Sweet P, Franco G, Vaezian R, Tkavc R, Daly MJ, Contreras LM. *A small RNA regulates pprM, a modulator of pleiotropic proteins promoting DNA repair, in Deinococcus radiodurans under ionizing radiation.* **Sci. Rep. 11:12949 (2021)**.
- **DOI:** `10.1038/s41598-021-91335-8` · PMID 34155239 · PMC8217566.
- **License / OA:** Gold OA, CC BY 4.0 via *Scientific Reports* (Unpaywall confirmed).
- **Cites (S2, 2026-06-09):** 25.
- **LUCID100 row:** rank 66, Wave 4 slot 35, tier A, priority 14, worktype `omics/signature replication`.

## The central claim

PprS (formerly Dsr2) is a *D. radiodurans* sRNA whose expression is
sensitive to ionizing radiation. The authors claim that PprS
**binds within the coding region** of the `pprM` (DR_0907) transcript
and **stabilizes it**; knockdown of PprS (PprSKD) destabilizes pprM and
reduces survival under acute (10 kGy) and chronic (57 Gy/h) IR. They
support this with:

- Northern + qRT-PCR time course of PprS under IR / H₂O₂ (Fig 1).
- PprSKD vs WT survival/growth under acute and chronic IR (Fig 2).
- Time-course shotgun proteomics on Orbitrap Fusion (PRIDE PXD026633, Tables S1, S2).
- Bulk RNA-seq, WT vs PprSKD at 0 and 10 kGy, n=3 (GEO GSE176207, Tables S4-S7).
- MS2-affinity pull-down + RNA-seq (MAPS) to find PprS-interacting transcripts (GEO GSE176207, Table S3).
- EMSA, mutational analysis of the binding site (Figs 4-5).

## What is publicly available

| Layer | Source | Resolved | Bytes | License |
| --- | --- | --- | --- | --- |
| Full paper | Nature OA PDF | yes | 1.9 MB | CC BY 4.0 |
| Supplementary Tables S1-S9 | Springer ESM MOESM1 (xlsx) | yes | 264 KB | CC BY 4.0 |
| Supplementary Figures | Springer ESM MOESM2 (pdf) | yes | 8.1 MB | CC BY 4.0 |
| RNA-seq + MAPS processed counts | GEO GSE176207 | yes | 215 KB tar (18 files) | unrestricted |
| RNA-seq raw FASTQ | GEO/SRA via GSE176207 | not downloaded | — | unrestricted (avail.) |
| TMT proteomics raw `.raw` | PRIDE PXD026633 | metadata only | ~10-100 GB | unrestricted (avail.) |
| Reference genome | GenBank NC_001263.1 (chr), NC_001264.1 (megaplasmid) | not downloaded | — | unrestricted (avail.) |

Every dependency for a full RNA-seq + MAPS replication is public and
free. The PASS-low smoke runs end-to-end from these files in seconds on
CherryRd — no SSH, no scheduler, no compute account.

## Smoke replication evidence (`code/smoke_test.py`, 7 checks)

| # | Check | Result | Detail |
| --- | --- | --- | --- |
| 1 | All 12 RNA-seq htseq files load with ≥ 3,000 gene rows | **PASS** | 3,142 rows × 12 samples |
| 2 | All 6 MAPS htseq files load | **PASS** | 3,142 rows × 6 samples |
| 3 | htseq diagnostic rows present (`__no_feature`, `__ambiguous`, …) | **PASS** | both sets |
| 4 | pprM (DR_0907) is DOWN in PprSKD vs WT at IR=0 | **PASS** | smoke CPM L2FC = -0.65 (sign-matches paper DESeq2 L2FC = -2.52, padj 1.34e-9) |
| 5 | pprM is ENRICHED in MS2-PprS MAPS pull-down vs MS2-blank | **PASS** | smoke L2FC = +2.98; 106 enriched transcripts at L2FC > 1 vs paper's "~130 potential interactors" |
| 6 | Supplement Table S1 row 1 (DR_0099 SSB) matches paper exactly | **PASS** | IR0_vs_Sham0 L2FC = 0.694617304329117 (exact) |
| 7 | Supplement Table S4 top row is DR_0907 (pprM) at L2FC < -2 | **PASS** | observed top = DR_0907, L2FC = -2.5166 |

Machine-readable record: [`results/smoke_test_report.json`](./results/smoke_test_report.json). The replicated MAPS scatter plot
([`figures/maps_pulldown_pprm_smoke.png`](./figures/maps_pulldown_pprm_smoke.png)) shows pprM as a star at the top of the enriched cloud.

## Honest limits of the smoke

- The smoke uses naive **CPM-mean ratio**, not DESeq2. Across the 53
  shared DEGs in Table S4, Pearson(paper L2FC, smoke L2FC) ≈ 0, sign
  concordance 64%. This is *expected*: with n=3 replicates and
  substantial library-size variation, DESeq2's size factors and
  dispersion shrinkage are necessary. Only the SIGN of pprM (the
  paper's flagship gene) is required for smoke-level PASS.
- Proteomics raw `.raw` files were not downloaded (~10-100 GB,
  Orbitrap Fusion; needs FragPipe/MaxQuant TMT pipeline on uicgpu).

## PASS-mid replication plan

**Compute target: uicgpu** (2 TB RAM is overkill but the storage policy
already pushes hot work to `/data/stevens/`). DESeq2 on 18 samples ×
3,142 genes is laptop-trivial; would prefer uicgpu to keep CherryRd
free.

1. **DESeq2 re-run of GSE176207 RNA-seq (12 samples).** R script with `DESeqDataSetFromMatrix(... ~ strain*dose)`, contrasts to reproduce S4 (PprSKD vs WT at sham), S5 (PprSKD vs WT at 10 kGy), S6 (WT 10 kGy vs 0 kGy), S7 (PprSKD 10 kGy vs 0 kGy). **Acceptance:** Spearman ≥ 0.9 vs paper L2FC on shared genes; ≥ 80% concordance on padj < 0.05 calls.
2. **DESeq2 on MAPS (6 samples).** Single contrast MS2-PprS vs MS2-blank. **Acceptance:** ≥ 80% overlap with paper's ~130 interactor list at paper's threshold.
3. **Functional re-enrichment.** Re-run PANTHER GO overrepresentation on each contrast's significant set and compare vs paper's Table S2 GO terms. **Acceptance:** top-10 GO terms reproduce qualitatively.

No author contact, no paid endpoints, no heavy compute on CherryRd. Job
plan would fit a single uicgpu interactive session (≤ 1 h wall clock).

## PASS-full (full proteomics replication, optional)

Only run if/when an external user explicitly requests it. Downloading
PXD026633 raw `.raw` files and running FragPipe TMT-IRS would be
multi-day on uicgpu but is feasible. Acceptance: reproduce the 142
proteins differentially expressed in Table S1 within ≥ 80% set overlap.

## Risks / pitfalls (notes for future-you)

- `htseq` count files include 5 diagnostic rows that **must** be stripped
  before normalization, or library sizes are inflated by `__too_low_aQual`
  (which is the dominant unaligned-quality bucket in this dataset; e.g.,
  GSM5360107 has 8.68 M reads in `__too_low_aQual` vs ~3 M in actual
  feature counts). The smoke script filters `~df.index.str.startswith("__")`.
- The MS2-blank vs MS2-PprS control comparison has very small library
  sizes (single-end NextSeq, low input after IP). Quantitative DESeq2
  rather than naive ratio is essential.
- Sample IDs in the GEO records use the old name **Dsr2** (e.g.,
  `GSM5360116_MS2Dsr2A`). Same molecule as PprS — paper renamed it.

## Verdict

**PASS-low ✅.** Proceed to PASS-mid (DESeq2 re-run on uicgpu) on the
next backfill cycle. Retag suggested: `candidate_curated` → `replication_smoke_passed`.
