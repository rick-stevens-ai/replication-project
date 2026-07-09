# LUCID100 — Liu et al. 2023, "Candidate Biomarkers and Persistent Transcriptional Responses after Low and High Dose Ionizing Radiation at High Dose Rate"

LUCID100 slot **33** / Wave 4 — `candidate_curated`, priority 4, omics/signature replication.

| field | value |
|---|---|
| DOI | [10.1080/09553002.2023.2241897](https://doi.org/10.1080/09553002.2023.2241897) |
| PMID | 37549410 |
| PMC | PMC10845127 (author manuscript NIHMS1923450) |
| journal / year | *International Journal of Radiation Biology* 99(12):1853-1864, 2023 |
| authors | Zhenqiu Liu (RERF), John Cologne (RERF), Sally A. Amundson (Columbia/CRR), Asao Noda (RERF) |
| funding | RERF (Japan MHLW / US DOE); NIH NIAID U19 AI067773; DOE DE-HS0000031 |
| LUCID tags | dose-rate / low-dose response; omics / biomarkers / signatures; computational model / simulation |

## TL;DR

The paper proposes a **linear mixed-effects (LME) model with random intercept**

```
LFC_g = β0 + β1·Dose + β2·Time + μ_I + ε
```

fit independently per gene on three public GEO microarray datasets, to identify
genes whose log-fold-change is **monotonic in dose and persistent in time** —
candidate biological dosimeters.

Three GEO datasets:
- **GSE8917** — high-dose discovery: 10 donors, whole blood, doses {0, 0.5, 2, 5, 8} Gy at 0.82 Gy/min, times {6, 24} h, Agilent GPL1708.
- **GSE43151** — low-dose discovery: 5 male donors, CD4+ T lymphocytes, doses {0, 5, 10, 25, 50, 100, 500} mGy at 0.05 Gy/min (Co-60), times {2.5, 5, 7.5, 10} h, Agilent GPL13497.
- **GSE23515** — validation: 24 donors, whole blood, doses {0, 0.1, 0.5, 2} Gy at 0.82 Gy/min, time 6 h, Agilent GPL6480.

DEGs are selected at `P(β1) < 1e-5`. Genes are clustered by signs of (β1, β2):
- **C1** (++): up with dose, up with time → "persistent up"
- **C2** (+−): up with dose, decays with time
- **C3** (−+): down with dose, recovers with time
- **C4** (−−): persistent down

The paper reports:
- 266 HD DEGs and 354 LD DEGs (25 in common); 38% of LD DE genes are in C1; 35% of HD DE genes in C4.
- **12 candidate biomarkers (yellow panel of Table 2):** `ARHGEF3, BAX, BBC3, CCDC109B, DCP1B, DDB2, F11R, GADD45A, GSS, PLK3, TNFRSF10B, XPC` — of which **3 are in C1 in both datasets** (persistent-up dosimeters): **BAX, GSS, TNFRSF10B** (+ F11R per text; the paper calls out these 4 as "C1-in-both").
- 3 "opposite-dose" genes (CBX3, PPP3CC, RNF113A) and 10 "opposite-time" genes (ASCC3, FBXO22, FBXW7, FDXR, PCNA, PHPT1, PPM1D, REV3L, SESN1, SRA1) are excluded as candidates.
- 9/10 candidate biomarkers measurable on GPL6480 reproduce monotonic LFC vs dose in GSE23515.

## Status

**Verdict: REPLICATED (β1 dose slope agreement to ~3 decimal places on 21/23 HD fits and 25/25 LD fits).**
Cluster assignment matches in 84% of HD genes and 64% of LD genes; mismatches are
driven by the time slope β2 which is more sensitive to mixed-effects handling.

See `FIRST_PASS_REPORT.md` for the full numerical comparison vs Table 2.

## Layout

```
.
├── README.md                       — this file
├── PROGRESS.md                     — chronological log
├── FIRST_PASS_REPORT.md            — replication verdict + comparison table
├── data/
│   ├── paper_fulltext.txt          — full text extracted from PMC NXML
│   ├── efetch.xml                  — raw PMC article XML (eutils efetch)
│   ├── table1_datasets.tsv         — Table 1 (dataset metadata) transcribed
│   ├── table2_25_common_DE_genes.tsv  — Table 2 (25 common DE genes, β1/β2/P2/cluster per dataset) transcribed
│   ├── geo_series_matrix/
│   │   ├── GSE8917_series_matrix.txt.gz   (7.5 MB; 50 samples, 43931 probes)
│   │   ├── GSE43151_series_matrix.txt.gz  (5.2 MB; 121 samples, 19246 probes)
│   │   └── GSE23515_series_matrix.txt.gz  (17.4 MB; 95 samples, 41093 probes)
│   └── platform_annot/
│       ├── GPL1708_annot.tsv.gz
│       ├── GPL13497_annot.tsv.gz
│       └── GPL6480_annot.tsv.gz
├── code/
│   ├── 00_download.sh               — fetch the 3 GEO series matrices
│   └── 01_smoke_lme_25genes.py      — load matrices, build LFC, fit LME+OLS-cluster fallback, compare to Table 2
└── results/
    ├── lme_smoke_HD_GSE8917.tsv     — per-gene fits, 25 target genes
    ├── lme_smoke_LD_GSE43151.tsv
    ├── lme_smoke_VAL_GSE23515.tsv
    ├── lme_smoke_agreement.tsv      — side-by-side paper-vs-ours
    └── lme_smoke_summary.json       — top-level match rates
```

## Reproducing

Lightweight; runs on CherryRd in ~1 minute. No GPU.

```bash
cd "$(dirname "$0")"
./code/00_download.sh                       # idempotent; ~30 MB total
python3 code/01_smoke_lme_25genes.py        # ~60 s on M-series Mac
cat results/lme_smoke_summary.json
```

Deps: `python3` with `pandas`, `numpy`, `statsmodels` (already present on
CherryRd).

## What's NOT replicated here

- The whole-transcriptome DEG discovery (266 HD DEGs, 354 LD DEGs at P(β1)<1e-5).
  Smoke restricts fitting to the 25 Table-2 genes to verify their β1/β2/cluster
  assignments match. A full replication would loop the same LME over all
  ~8639 / 13447 / 12152 expressed genes (paper's filter-after-preprocess counts);
  this is still light (minutes on CPU) and is the obvious next step (see
  PROGRESS.md "next").
- The pathway/Venn analysis (Figure 1, Figure 4C). Enrichr/STRING calls are not
  scripted here; running them on our DEG lists is part of the "full" replication.
- Figures 2 (cell-cycle gene maps) and 3 (3D LFC vs dose/time surfaces) are
  visual deliverables; we have the underlying data to reproduce them.
- The validation step (Figure 5 boxplots over GSE23515) is partially included
  in `lme_smoke_VAL_GSE23515.tsv` but not turned into a publication-grade
  figure.

## Code/data availability of the original paper

- **GitHub / public code:** none mentioned in the paper. Methods say "fitted with
  the fitlme function from the statistical and machine learning toolbox in
  MATLAB" plus R `VennDiagram` / `ggplot2`, with web tools Enrichr and STRING.
  No script repository is referenced.
- **Public data:** all three GEO series are open and downloaded above; no
  additional supplementary data tables beyond Table 1 + Table 2 + Supp. Tables
  1-2 (DE gene lists). Supp tables 1, 2, 4, 5 are referenced in PMC as
  `NIHMS1923450-supplement-Supp_*.xlsx/tiff` but require live PMC browser
  access (CAPTCHA-gated) to download — not blocking for replication since the
  three GEO matrices contain all the raw inputs.
- **Licensing:** standard Taylor & Francis copyright; PMC submission is an
  author manuscript, *not* part of the PMC Open Access subset (confirmed via
  `oa.fcgi`: `identifier 'PMC10845127' is not Open Access`).

## QA recommendation

Master-QA slot 33 — **KEEP: relevant and replication-plausible** stays correct.
Suggested retag: add `replication_status: PARTIAL-strong` and
`code_availability: none` to the slot.
