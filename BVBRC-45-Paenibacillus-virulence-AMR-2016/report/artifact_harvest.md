# Artifact Harvest — BVBRC-45

All artifacts free / no-auth. Fetched 2026-07-01.

## Paper (open access, CC BY)
| Artifact | Source | Notes |
|---|---|---|
| Full-text XML | Europe PMC REST `PMC4761199/fullTextXML` | 130,763 bytes; `work/paper_fulltext.xml` |
| Bibliographic record | Europe PMC search API | PMID 26900405, PMCID PMC4761199, DOI 10.1186/s13099-016-0089-1 |

## Genomes (NCBI Datasets v2 REST, no auth)
| Accession | Organism / strain | Level | Use |
|---|---|---|---|
| **GCF_001029205.1** (=GCA_001029205.1, ASM102920v1) | ***Paenibacillus* sp. VT-400** (the paper's strain; WGS LELF01000000, DSM 100755) | Contig (115) | Query genome — stats, AMR, virulence, ANI |
| GCF_036894225.1 | *P. amylolyticus* Y5S-7 | Complete | ANI reference (closest relative) |
| GCF_001908275.1 | *P. xylanexedens* | — | ANI reference |
| GCF_036884255.1 | *P. tundrae* | — | ANI reference |
| GCF_023101145.1 | *P. pabuli* | — | ANI reference |
| GCF_046058935.1 | *P. taichungensis* | — | ANI reference |

Genome + protein + GFF3 pulled for VT-400; genome only for the 5 references.

## Tools (all free, on uicgpu)
| Tool | Version | Env |
|---|---|---|
| NCBI `datasets` | 18.32.0 | /data/stevens/envs/bvbrc28 |
| fastANI | 1.34 | /data/stevens/envs/bvbrc28 |
| AMRFinderPlus | 3.12.8 (DB 2024-07-22.1) | ~/micromamba/envs/amr |
| BLAST+ (blastn/makeblastdb) | present | /data/stevens/envs/bvbrc28 |
| prokka | present (available, not needed — NCBI PGAP annotation used) | /data/stevens/envs/bvbrc28 |

## LLM judge
- Free Argo proxy (localhost:44497), model `argo:gpt-5.2`, temperature 0. Prompt + raw JSON in `report/evidence/`.

## Key identifiers verified public
- WGS master: **LELF01000000** · Assembly: **GCF_001029205.1** · Type strain deposit: **DSM 100755**
