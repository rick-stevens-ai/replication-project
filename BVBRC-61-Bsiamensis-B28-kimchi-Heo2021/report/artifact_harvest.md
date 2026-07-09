# Artifact Harvest — BVBRC-61

All artifacts are free/public. No paywalled resources used. Paper full text pulled from Europe PMC OA (NOT the paid `pdf` tool).

## Paper
| Item | Value |
|---|---|
| Title | Functional Genomic Insights into Probiotic *Bacillus siamensis* Strain B28 from Traditional Korean Fermented *Kimchi* |
| Authors | Heo S, Kim JH, Kwak MS, Jeong DW, Sung MH |
| Journal | Foods 2021, 10(8):1906 |
| DOI | 10.3390/foods10081906 |
| PMID / PMCID | 34441683 / PMC8394110 |
| License | CC BY 4.0 (open access) |
| Full text XML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8394110/fullTextXML → `work/paper_fulltext.xml` (133 KB) |

## Genome assemblies (NCBI Datasets REST/CLI v18.25.1, free, no auth)
| Strain | Accession (used) | Role | Contigs | bp | GC% |
|---|---|---|---|---:|---:|
| *B. siamensis* B28 (THIS PAPER) | **GCF_016313165.1** (= GCA_016313165.1; nuccore CP066219–CP066221) | subject | 3 | 3,957,728 | 45.85 |
| *B. siamensis* SCSIO 05746 | GCA_002850535.1 | comparator (complete) | 2 | 4,280,711 | 45.96 |
| *B. siamensis* KCTC 13613ᵀ | GCA_000262045.1 | comparator (type, incomplete) | 51 | 3,779,696 | 46.34 |
| *B. amyloliquefaciens* FS1092 | GCA_004421045.1 | outgroup | 1 | 4,240,930 | 45.91 |
| *B. amyloliquefaciens* RD7-7 | GCA_001705195.1 | outgroup | 1 | 3,688,209 | 46.25 |
| *B. velezensis* JJ-D34 | GCA_000987825.1 | outgroup | 1 | 4,105,955 | 46.24 |
| *B. velezensis* KMU01 | GCA_015277495.1 | outgroup | 1 | 3,932,437 | 46.53 |

B28 annotation package (RefSeq PGAP): `protein.faa` (3,808 proteins), `genomic.gff`, `cds_from_genomic.fna` via `datasets download genome accession GCF_016313165.1 --include protein,gff3,cds`.

## Tools / databases
| Tool | Version | Source |
|---|---|---|
| NCBI datasets CLI | 18.25.1 | conda/homebrew |
| fastANI | (homebrew) | /usr/local/bin/fastANI |
| skani | (homebrew) | /usr/local/bin/skani |
| AMRFinderPlus | 4.2.7, DB 2026-03-24.1 | miniforge env `amrfinder` |
| RGI / CARD | env `rgi` | miniforge env `rgi` |
| mlst (Torsten Seemann) | 2.33.1 (pubMLST bsubtilis scheme) | miniforge env `mlst-env` |
| BLAST+, HMMER | homebrew / envs | |
| Biopython | 1.87 | system pip |
