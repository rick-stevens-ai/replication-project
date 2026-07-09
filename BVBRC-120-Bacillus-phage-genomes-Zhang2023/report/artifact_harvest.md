# Public artifact harvest — BVBRC-120

## Paper metadata

| Item | Value |
|---|---|
| PMID | 37337195 |
| PMC | PMC10278307 |
| DOI | 10.1186/s12866-023-02907-9 |
| Journal | BMC Microbiology 23:170 |
| Publication date | 2023-06-19 |
| First author | Yating Zhang |
| Last author | Bingxue Li |

## PDF

| URL | Bytes | SHA-256 note |
|---|---|---|
| `https://bmcmicrobiol.biomedcentral.com/counter/pdf/10.1186/s12866-023-02907-9.pdf` | 10,264,695 | Fetched from uicgpu with `Mozilla/5.0` UA + proxy <lan-host>:3128 |

## Supplementary XLSX (from Springer static-content)

Base URL: `https://static-content.springer.com/esm/art%3A10.1186%2Fs12866-023-02907-9/MediaObjects/`

| File | Bytes | Contents |
|---|---|---|
| `12866_2023_2907_MOESM1_ESM.xlsx` | 18,595 | S1: 178 Bacillus strains + prophage counts |
| `12866_2023_2907_MOESM2_ESM.xlsx` | 11,928 | S2: 30 functional protein COG entries |
| `12866_2023_2907_MOESM3_ESM.xlsx` | 12,125 | S3: 36 prophages + host GCA accessions |
| `12866_2023_2907_MOESM4_ESM.xlsx` | 10,685 | S4: 20 focal lytic phage accessions |
| `12866_2023_2907_MOESM5_ESM.xlsx` | 14,413 | S5: 25 blastn homologs of Carmel_SA, Cherry, Fah |
| `12866_2023_2907_MOESM6_ESM.xlsx` | 18,190 | S6: 105 Type-I lysis-module homologs |
| `12866_2023_2907_MOESM7_ESM.xlsx` | 17,209 | S7: 105 Type-II lysis-module homologs |
| `12866_2023_2907_MOESM8_ESM.xlsx` | 24,282 | S8: blast of ~200 functional gene rows |
| `12866_2023_2907_MOESM9_ESM.xlsx` | 17,603 | S9: 236 Bacillus lytic phage accessions |

## NCBI genome downloads (via `efetch -db nuccore -id ... -format fasta`)

- 236 accessions requested from S9 → **231 unique sequences returned** (~22 MB FASTA).
- 20 focal lytic accessions from S4: 7 already present in the 231-set; 13 fetched additionally → **20/20 recovered**.

Full accession lists in `work/S1_178_bacillus_strains.csv`, `work/S4_20_lytic_phages.csv`, `work/S9_236_lytic_phages.csv`.

## Sample accessions (first 5 from each list)

**S9 (236 lytic phages):**
```
OK500002.1  Bacillus phage vB_BanS_Athena
MN604230.1
NC_049972.1
NC_049971.1
CP042877.1
```

**S4 (20 focal lytic phages):**
```
KY963371.1  Bacillus phage Carmel_SA  (Siphoviridae, Wbetavirus, B. anthracis host)
DQ222851    Bacillus phage Cherry
NC_007814   Bacillus phage Fah
MG967616    (lytic)
JN797796    (lytic)
```

**S1 (178 hosts, first 3):**
```
Bacillus abyssalis    MTIQ01000000    1 prophage
Bacillus altitudinis  (accession)     2 prophages
...
```

## Non-fetched (planned open-question follow-ons)

- 178 host genome FASTA (only names/accessions extracted; not re-downloaded — would be needed for VirSorter2 rerun per open question Q2)
- COG functional annotations (WebMGA web service; would need local CDD flat file per Q1)
- Type-I/II lysis-module HMM profiles (not built; would enable full 231-panel scan per Q4)
