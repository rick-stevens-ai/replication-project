# Artifact manifest — LUCID100 slot 51

Paper: Clark-Hachtel et al. (2024) *Curr. Biol.* 34:1819–1830.
DOI:  10.1016/j.cub.2024.03.019
PMID: 38614079
PMCID: PMC11078613 (NIHMS1979636, free author manuscript; not OA-licensed)

## Public artifacts harvested (no paid endpoints, no author contact)

### Paper text
| Path | Size | Source |
|---|---|---|
| `artifacts/paper.pdf` | 1.96 MB | Europe PMC author manuscript (`europepmc.org/articles/PMC11078613?pdf=render`) |
| `artifacts/paper.txt` | layout text via `pdftotext -layout` |
| `artifacts/pmc_efetch.xml` | 177 kB | NCBI eFetch JATS XML (`eutils/efetch.fcgi?db=pmc&id=11078613`) |
| `artifacts/oai.xml` | 177 kB | OAI-PMH GetRecord (PMC) |

### Bibliographic + linkage metadata
| Path | Source |
|---|---|
| `artifacts/epmc_meta.json` | Europe PMC search API core record |
| `artifacts/datalinks.json` | Europe PMC text-mined data accessions (19 cross-refs) |

### RNA-seq processed data (GEO public, Apr 2024)
SuperSeries: **GSE253471** (Series_status: Public on Apr 12 2024)
- SubSeries **GSE240501** — Ionizing radiation, 100/500/2180 Gy + 0 Gy, 3 reps each (12 samples). *Raw SRA only; no processed supplementary in GEO.*
- SubSeries **GSE253470** — Bleomycin, 10 µg/mL, 100 µg/mL, 1 mg/mL + control, 3 reps each (12 samples). **Processed featureCounts + per-contrast EdgeR outputs deposited.**

| Path | Size (bytes) | Description |
|---|---|---|
| `data/GSE253470/GSE253470_He_Bleo_featurecounts.txt.gz` | 690 355 | Raw featureCounts matrix, 19 700 genes × 12 samples |
| `data/GSE253470/GSE253470_He_Bleo_10ugvC_EdgeR_output.txt.gz` | 284 716 | EdgeR DE: 10 µg/mL Bleo vs control (14 290 genes) |
| `data/GSE253470/GSE253470_He_Bleo_100ugvC_EdgeR_output.txt.gz` | 329 596 | EdgeR DE: 100 µg/mL Bleo vs control |
| `data/GSE253470/GSE253470_He_Bleo_1mgvC_EdgeR_output.txt.gz` | 352 455 | EdgeR DE: 1 mg/mL Bleo vs control |
| `artifacts/GSE253471.soft.txt`, `GSE240501.soft.txt`, `GSE253470.soft.txt`, `GSE240501.acc.html`, `GSE240501.full.soft.txt` | — | GEO SOFT/HTML metadata |

### Genome / annotation
| Path | Size | Description |
|---|---|---|
| `data/genome/feature_table.txt.gz` | 942 kB | NCBI `GCA_002082055.1_nHd_3.1` feature table — 19 946 BV898 locus tags → product names. *(Paper used the v3.1.5 re-annotation hosted at tardigrades.org, which was unreachable during this run; v3.1 has identical locus tags but sparser naming.)* |

### Other accessions (catalogued only, not downloaded)
- **ENA / SRA raw FASTQ**: SRP098563, SRP098585, SRX2527616/798, SRX2661843/844, SRX2663153/154, BioProjects PRJNA1065858, PRJNA1003921, PRJNA1065867. ~24 paired-end Illumina NextSeq2000 libraries, 2×50 bp; full re-mapping is out of scope for this first pass.
- **ProteomeXchange / PRIDE**: PXD047724 (label-free quant proteomics, 9 samples). DOI 10.6019/PXD047724. Not downloaded — used only as paper-cited orthogonal evidence.
- **GCA_002082055.1**: *Hypsibius exemplaris* (nHd) reference genome (paper used v3.1.5 annotation, an updated GFF).
- **Dryad 10.5061/dryad.50r1b**: text-mined by Europe PMC as a "related dataset" — VERIFIED to be Beltran-Pardo et al. 2015 *PLOS ONE* (older work, unrelated). **Do not treat as a Clark-Hachtel artifact.**

### Author / code
- "This paper does not report original code." (PMC Data and code availability statement)
- No GitHub repository under author handles (Goldstein lab, Clark-Hachtel, Hibshman). Verified via GitHub search API.

### NOT obtained (gated)
- `NIHMS1979636-supplement-1.xlsx` — Data S1 (full per-gene EdgeR tables for **both** IR and Bleo arms; Tables S1–S4). Listed in PMC JATS XML but blocked by reCAPTCHA on every PMC/EuropePMC download endpoint attempted. Would require manual browser download or institutional access.
- `NIHMS1979636-supplement-2.pdf` — Supplementary Figures S1–S5. Same gating.
- ScienceDirect `mmc1.xlsx` / `mmc2.pdf` — gated by 403/406.

The IR-arm DE table (Data S1B) is therefore not on disk; we only have IR-arm raw FASTQ (via SRA). The Bleomycin arm — which is the paper's own radiomimetic positive-control arm and validated as IR-correlated — is fully analyzable with the GEO supplementary files alone.
