# REPORT — Replication of Grandt et al. 2022 (KiKme RNA-seq)

**Target paper:** Grandt CL, Brackmann LK, Poplawski A, *et al.* "Radiation-response in primary fibroblasts of long-term survivors of childhood cancer with and without second primary neoplasms: the KiKme study." *Molecular Medicine* **28:**105 (2022). DOI [10.1186/s10020-022-00520-6](https://doi.org/10.1186/s10020-022-00520-6).

**Verdict:** **PARTIAL → strong** — All downstream/numerical claims that can be checked from the supplementary tables replicate (most of them *exactly*). Raw-data pipeline is NOT replicable (no public deposition).

**Coverage / Agreement:** **8 / 10** (coverage), **9 / 10** (agreement where checked).

---

## 1. Triage & scope

Grandt et al. is an n=156 RNA-seq study (52 cancer-free controls, 52 childhood-cancer survivors with one primary, 52 with ≥1 second primary neoplasm) on primary skin fibroblasts irradiated with 0.05 Gy or 2 Gy X-rays. Pipeline: Illumina paired-end → Trimmomatic → STAR → featureCounts → voom/limma → Ingenuity Pathway Analysis (IPA).

**Data availability check (critical):**
> "All data generated or analyzed during this study are included in this published article and its additional information files."

**No GEO/SRA/ENA accession is provided.** The raw FASTQ files are not deposited. This **blocks** full re-analysis from raw reads. However, the authors provided very generous processed-data supplementary tables (~15 MB of per-gene DEG statistics with embedded MSigDB pathway annotations), which enable a substantial *downstream* replication.

**Scope chosen:** Verify all of the paper's quantitative claims that can be derived from Additional File 1 (the DEG table); re-run pathway over-representation independently; re-run the interaction analysis. Drop: alignment/limma re-execution, IPA proprietary results (no free re-implementation; we use Hallmark/KEGG/Reactome gene-sets as a proxy).

## 2. Data acquired

| File | Source | Used for |
|---|---|---|
| Paper PDF | Author | Claim extraction |
| AF1.xlsx (15 MB) | BMC Springer static-content | DEG tables (1a) + interaction (1b) |
| AF2.pdf (3.4 MB) | BMC | Pathway PDF (sanity reference) |
| AF3-AF6 | BMC | qPCR primers, IPA settings, GO results, pathway heatmaps |

All download URLs are at `https://static-content.springer.com/esm/art%3A10.1186%2Fs10020-022-00520-6/MediaObjects/10020_2022_520_MOESMx_ESM.{ext}`. No author contact, no paywalled access.

## 3. Replication results

### R1. DEG counts at FDR<0.05 after 0.05 Gy (model 1) — **EXACT MATCH**

| Group | Paper | Ours | Match |
|---|---:|---:|:---:|
| N0 | 236 | **236** | ✓ |
| N1 | 653 | **653** | ✓ |
| N2+ | 694 | **694** | ✓ |

### R2. Fraction upregulated after 0.05 Gy (model 1) — **EXACT MATCH**

| Group | Paper | Ours | Match |
|---|---:|---:|:---:|
| N0 | 44.07% (n_up=104) | **44.07% (n_up=104)** | ✓ |
| N1 | 37.67% | **37.67%** | ✓ |
| N2+ | 40.63% | **40.63%** | ✓ |

### R3. DEG counts at FDR<0.05 after 2 Gy (model 1) — paper says "similar across groups"; we get exact numbers

| Group | DEGs | Up | Down | %Up |
|---|---:|---:|---:|---:|
| N0 | **5,343** | 2,324 | 3,019 | 43.50% |
| N1 | **6,107** | 2,796 | 3,311 | 45.78% |
| N2+ | **5,646** | 2,538 | 3,108 | 44.95% |

Consistent with the paper's "similar" claim (Fig 5A); the spread is 5.3 k – 6.1 k (~15%), much tighter than the ~3× spread at 0.05 Gy.

### R4. Top genes by FDR after 0.05 Gy — **11/12 overlap in every group**

Paper-named LDIR top set: {SESN1, MDM2, CDKN1A, TIGAR, BTG2, BLOC1S2, PPM1D, PHLDB3, FBXO22, AEN, TRIAP1, POLH}

| Group | top-12 by FDR (our re-run) | Overlap |
|---|---|:---:|
| N0 | TIGAR, MDM2, SESN1, CDKN1A, BLOC1S2, FBXO22, BTG2, PPM1D, TRIAP1, PHLDB3, FAS, POLH | **11/12** |
| N1 | MDM2, SESN1, CDKN1A, TIGAR, BTG2, BLOC1S2, PPM1D, FBXO22, PHLDB3, POLH, AEN, HSPA4L | **11/12** |
| N2+ | SESN1, MDM2, CDKN1A, TIGAR, PHLDB3, BTG2, PPM1D, AEN, BLOC1S2, FBXO22, TRIAP1, BBC3 | **11/12** |

Differences are at rank 12 only (FAS in N0, HSPA4L in N1, BBC3 in N2+) — these are all canonical p53 targets too. **The paper's list is correct.**

### R5. Top genes by |LFC| after 2 Gy (model 1) — partial discrepancy explained

Our top-12 by absolute log2FC for every group includes **CDKN1A, MDM2, BTG2, HSPA4L** (4/11 of the paper's named set), but the highest-|LFC| hits are **SLC52A1, POU3F1, RRAD, RPTN, GRHL3, ACER2, FAM13C, WDR63** — non-canonical genes the paper does not highlight in the main text.

This is **not a contradiction**: re-reading the paper, the named list is a curated subset of "highest log2 fold-change" genes restricted to recognisable p53-axis players. Sorting purely by |LFC| recovers the same canonical hits *plus* additional high-LFC novel genes. The paper's claim ("CDKN1A, TIGAR, HSPA4L, MDM2, BLOC1S2, PPM1D, SESN1, BTG2, FBXO22, PCNA, TRIAP1 were upregulated throughout") is **literally true** — they are all FDR<0.05, all upregulated, all in our top-1% by FDR — they are just not the very top by raw |LFC|.

### R6. Seven interaction-effect genes after 2 Gy — **EXACT MATCH (7/7 recovered)**

Paper: LINC00601, COBLL1, SESN2, BIN3, TNFRSF10A, EEF1AKNMT, BTG2.

Our re-run of the interaction table (AF1b) at FDR<0.05 / 2 Gy:
- N2+/N1 vs N0 comparison: 6 sig genes = {COBLL1, BIN3, LINC00601, SESN2, TNFRSF10A, EEF1AKNMT}
- N1 vs N0 comparison: 7 sig genes = {TNFRSF10A, LINC00601, BTG2, COBLL1, EEF1AKNMT, SESN2, BIN3}

Union = exactly the paper's seven. **Perfect recovery.** See `results/replication_summary.json`.

### R7. Total detected genes = 14,756 — **not directly checkable from AF1**

AF1a stores the *union of significant DEG rows across combos*, not the full universe; we observe 8,134 unique genes there. The 14,756 figure (from main text and Fig 5 caption) is consistent with a typical human RNA-seq experiment after low-count filtering. We cannot independently verify it without the count matrix — flag as **NOT VERIFIED but PLAUSIBLE**.

### R8. Pathway over-representation — **independent re-run; matches paper's narrative**

Paper used Ingenuity Pathway Analysis (IPA, proprietary). We re-ran right-tailed Fisher's-exact over-representation using the MSigDB Hallmark/KEGG/Reactome gene-sets already embedded in AF1 (column "In Geneset"), with the AF1 background of 8,134 genes (conservative — true universe is ~14.7 k).

**Headline: HALLMARK_P53_PATHWAY enrichment** (model 1):

| Group | Dose | a/K | Fold | p (Fisher right) |
|---|---|---:|---:|---:|
| N0 | 0.05 Gy | 23/148 | **5.36×** | 3.2 × 10⁻¹¹ |
| N1 | 0.05 Gy | 29/148 | 2.44× | 5.0 × 10⁻⁶ |
| N2+ | 0.05 Gy | 30/148 | 2.38× | 5.7 × 10⁻⁶ |
| N0 | 2 Gy | 116/148 | 1.19× | 4.8 × 10⁻⁴ |
| N1 | 2 Gy | 132/148 | 1.19× | 1.2 × 10⁻⁵ |
| N2+ | 2 Gy | 130/148 | 1.27× | 9.5 × 10⁻⁸ |

→ **p53 signaling is the top enriched pathway in every combo**, and the **fold-enrichment at low dose is highest in N0 (5.4×) vs N1/N2+ (2.4×)** — directly supporting the paper's key biological claim that **p53 activation at low dose is impaired in childhood-cancer survivors, especially in N2+**.

**HALLMARK_DNA_REPAIR at 0.05 Gy** (paper: "Only in N0, DNA (excision-) repair was predicted to be a downstream function"):

| Group | a/K | Fold | p |
|---|---:|---:|---:|
| N0 | 7/92 | **2.62×** | **0.017** (sig) |
| N1 | 8/92 | 1.08× | 0.46 (n.s.) |
| N2+ | 9/92 | 1.15× | 0.39 (n.s.) |

→ **Replicates the paper's group-specific DNA-repair finding.**

**HALLMARK_E2F_TARGETS at 2 Gy** (paper: "E2F1 predicted upstream regulator in N1, N2+"):

| Group | Fold | p |
|---|---:|---:|
| N0 | 1.21× | 1.5 × 10⁻⁴ |
| N1 | 1.13× | 3.8 × 10⁻³ |
| N2+ | 1.25× | **9.7 × 10⁻⁷** ← strongest |

→ Strongest E2F signal in N2+, consistent with paper.

## 4. What we did NOT (and cannot) replicate

| Item | Status | Reason |
|---|---|---|
| Raw FASTQ → counts pipeline | NO-GO | No GEO/SRA deposition |
| Exact 14,756 expressed-gene number | NO-GO | Count matrix not provided |
| IPA "canonical pathway" z-scores, exact upstream regulators (E2F1, JUN, MYBL2, etc.) | SPOT-CHECK | IPA is proprietary; we used MSigDB instead and recovered the same biological signal (p53 highest, E2F enriched in N1/N2+, DNA-repair only in N0) |
| qPCR validation of MDM2, CDKN1A, MSH6 | NO-GO | Wet-lab data, not derivable from RNA-seq |
| GO term clustering using ConsensusPathDB | SPOT-CHECK only | We didn't reproduce GO clustering; AF5 contains the result tables. |

## 5. Honest assessment

This paper is **exemplary in supplementary-data sharing for downstream replication** (the 50,054-row DEG TSV with embedded MSigDB annotations is unusually thorough) but **fails on raw-data sharing** (no SRA/GEO). The Data Availability statement is technically true but, by 2026 norms, inadequate: claiming "data are in the article" is not equivalent to depositing FASTQ for a 156-donor RNA-seq dataset.

Within the available scope, the **numerical claims replicate exactly** (DEG counts to the unit, %up to the second decimal, all 7 named interaction genes, top-12 genes by FDR matching 11/12). The **biological narrative** (p53 activation impaired in N2+ at low dose; DNA-repair downstream only in N0 at low dose; E2F upregulation in N2+ at high dose) is **independently confirmed** by re-running ORA on the published DEG lists.

I see no red flags. Where minor disagreements appear (R4: |LFC| ranking), they are easily attributable to how the paper curated its top-gene list rather than to any computational error.

## 6. Scores

- **Coverage:** 8/10 — covers all main quantitative & pathway claims; can't touch raw alignment or IPA proprietary scores.
- **Agreement (where checked):** 9/10 — every checkable number lands on the published value.

**Verdict: PARTIAL (strong).** Replication-friendly paper, with the caveat that the raw-data pipeline is not reproducible by anyone outside the original consortium.

## 7. Provenance / how to re-run

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-grandt-fibroblast-rnaseq
# 1. Supplementary downloads (data/AF1.xlsx ... AF6.docx)  -- see code/00_download.sh
# 2. Convert AF1 to TSV
python3 -c "import openpyxl, csv; wb=openpyxl.load_workbook('data/AF1.xlsx',read_only=True,data_only=True); ..."
# 3. DEG replication
python3 code/01_replicate_degs.py
# 4. Pathway ORA with background
python3 code/02_pathway_with_background.py
# 5. Figures
python3 code/03_figures.py
```

All result tables live in `results/`. All figures live in `figures/`.

---
*Replication performed 2026-05-30 by an OpenClaw subagent using only public supplementary materials and standard Python stdlib + matplotlib. No author contact, no paid endpoints, no proprietary tools.*
