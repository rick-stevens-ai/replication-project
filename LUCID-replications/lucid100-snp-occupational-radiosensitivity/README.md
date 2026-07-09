# LUCID100 slot 26 — Botbayev et al. 2026 (radioresistance SNP enrichment)

> **First-pass artifact harvest + minimal statistical replication.**
> LUCID100 master rank 57, Wave 3, Tier A.

## Paper

- **Title:** *Genetic Determinants of Radiosensitivity: Evidence of Radioresistance-Associated SNP Enrichment in Occupational Workers Chronically Exposed to Low-Dose Radiation*
- **Authors:** Botbayev D., Sharipov K., Belkozhayev A., Alzhanuly B., Yerkinbek U., Sharipov D., Gulyayev A., Kairgeldina S., Tekebayev K., Zhunussova G., Baurzhan M.
- **Journal:** *Genes* (MDPI), 17(2), 191 (2026)
- **DOI:** [10.3390/genes17020191](https://doi.org/10.3390/genes17020191)
- **PubMed:** 41751575
- **License:** CC-BY 3.0 (open access)

## TL;DR

| | |
|---|---|
| Replication verdict | **PARTIAL (consistent)** — paper-reported chi² / p / OR statistics for the four highlighted SNPs are mathematically reproducible from the published genotype frequencies × Table-1 sample sizes, with 13/16 cohort–SNP cells matching at p<0.05. Three cells show OR/p discrepancies attributable to (a) an apparent column-shift typo in Table 4 (Stepnogorsk × Russian × rs17878362) and (b) the paper appearing to use a non-allelic OR convention (dominant model vs allelic) for rs1625895 and rs1801270. |
| Coverage (of paper's 4 reported main-text SNPs × 4 cohort strata = 16 cells) | 16/16 |
| Statistical agreement (genotype p<0.05 decision matches paper) | 13/16 (81 %) |
| Underlying genotype-level replication | **NOT POSSIBLE** — data availability is "on request from the corresponding author"; no public deposit anywhere |
| Supplementary tables (S1, S2; APC/VEGF/XPD/RAD51) | Not harvested — MDPI bot-management blocked programmatic download |

## Cohort (Table 1)

| Group | N | Kazakhs | Russians | Mean age Kaz | Work exp Kaz | Mean age Rus | Work exp Rus |
|---|---|---|---|---|---|---|---|
| Control (Almaty Blood Center) | 289 | 129 | 160 | 47.7 | – | 42.1 | – |
| Balkhashinskoe (Shantobe) uranium deposit | 238 | 54 | 184 | 44.0 | 11.0 y | 49.0 | 13.7 y |
| Stepnogorsk Mining & Chemical Combine | 224 | 52 | 172 | 35.0 | 15.5 y | 40.0 | 17.3 y |

All male, no personal/family history of cancer or hereditary disorders.

**Dose context:** average annual effective dose at Kazatomprom Group-A workers 1.36–1.51 mSv/y (incl. natural background 0.7–1.2 mSv/y); max individual doses 4–6 mSv/y; cumulative career doses for 10–20-yr workers typically <100 mSv. Site dosimetry includes urine bioassay + EPR tooth enamel.

## SNPs studied

Four reported in main text (Tables 4–7); four in Supplementary S1/S2:

| Gene/locus | rs ID | Polymorphism | RFLP enzyme | Reported as significant? |
|---|---|---|---|---|
| TP53 intron 3 | rs17878362 | 16-bp ins/del | none (length poly) | Yes (Russian, Stepnogorsk, allele p=0.015) |
| TP53 intron 6 | rs1625895 | G>A | MspI | Yes (Russian SMCC, allele p=0.002; Kazakh SMCC genotype p=0.003) |
| TP53 exon 4 | rs1042522 | Arg72Pro (G>C) | BstUI | Yes (Russian Balkash., allele p=0.001; Kazakh Balkash., allele p=0.006) |
| CDKN1A/p21 codon 31 | rs1801270 | Ser/Arg (C>A) | BlpI | Yes (Russian Balkash., genotype p=0.009) |
| APC exon 11 | – | – | RsaI | No (supplementary only) |
| VEGF −2549 | – | ins/del | none | No (supplementary only) |
| RAD51 | rs1801320 | G>C 5'UTR | Bst2UI | No (supplementary only) |
| XPD (ERCC2) | rs13181 | Lys751Gln | PstI | No (supplementary only) |

## What this folder contains

```
.
├── README.md                       # this file
├── PROGRESS.md                     # task log
├── FIRST_PASS_REPORT.md            # verdict + analysis
├── MANIFEST.json                   # artifact manifest
├── paper-landing.pdf               # browser-rendered article (3.9 MB)
├── paper.txt                       # pdftotext -layout extraction
├── tables/
│   └── tables_extracted.json       # Tables 1-7, machine-readable
├── code/
│   ├── replicate_chi2_or.py        # smoke-replication script (chi^2, OR, HWE)
│   └── plot_p_comparison.py        # paper-vs-recomputed -log10(p) scatter
├── results/
│   └── replication_chi2.json       # 16 cohort×SNP rows of replication output
├── figures/
│   └── p_value_comparison.png      # concordance plot
└── docs/, data/, artifacts/        # reserved for future passes
```

## How to reproduce

```bash
cd lucid100-snp-occupational-radiosensitivity
python3 code/replicate_chi2_or.py          # writes results/replication_chi2.json
python3 code/plot_p_comparison.py          # writes figures/p_value_comparison.png
```

Dependencies: numpy, scipy, matplotlib (already in CherryRd default Python env, verified scipy 1.17.1 / numpy 2.4.3).

## Why this is only a "table replication"

The published frequencies in Tables 4–7 contain almost zero independent information beyond what the chi² / p / OR columns already give. The replication confirms **internal numerical consistency** of the paper but does **not independently verify** the underlying genotype calls. A full replication would require either:

1. Author-shared raw genotype data (per Data Availability Statement), or
2. An independent uranium-worker cohort with the same SNP panel (Mayak workers cf. Vorobtsova 2010 [ref 25] is the obvious comparator — see FIRST_PASS_REPORT for cross-cohort scoping).

## Status

- **First-pass:** complete (this report).
- **Next pass (if upgraded):** request raw data from corresponding author *(skipped per task: "no author contact")*; or harvest Mayak comparator cohort allele frequencies from Vorobtsova 2010 / Akulevich 2009 for sanity check.

## QA retag recommendation

**KEEP** the LUCID100 row as `replication_partial_table_only` (Tier A). The paper is real, OA, reproducible-at-table-level, and biologically plausible; key statistics check out. Three printed values appear to be transcription or convention errors, worth flagging in any downstream meta-analysis. **No demotion warranted; no go further than this without author data.**
