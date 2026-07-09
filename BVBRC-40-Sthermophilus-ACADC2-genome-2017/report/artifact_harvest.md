# Artifact Harvest — BVBRC-40

All artifacts free/public. No paid endpoints used.

## Paper
| Artifact | ID / URL | Notes |
|---|---|---|
| Full-text XML | Europe PMC PMC5282782 (`/fullTextXML`) | 106,994 bytes; OA CC BY. `work/paper_fulltext.xml` |
| Cleaned text | derived | `work/paper_text.txt` (42 KB) |
| PMID | 28163827 | |
| PMCID | PMC5282782 | |
| DOI | 10.1186/s40793-017-0227-5 | Standards in Genomic Sciences 12:18 (2017) |

## Genome data (NCBI Datasets v2alpha REST — free, no auth)
| Accession | Type | Size (zip) | Contents |
|---|---|---:|---|
| GCA_900094135.1 | Author-submitted GenBank assembly (= ENA LT604076.1) | 1,398,367 B | genomic.fna, protein.faa, cds_from_genomic.fna, genomic.gff |
| GCF_900094135.1 | RefSeq/PGAP re-annotation (= NZ_LT604076.1) | 1,514,952 B | same set, PGAP annotation |
| BioProject | PRJEB14916 | — | linked project |
| Chromosome | LT604076.1 | 1,731,838 bp | single circular chromosome |

Local paths: `work/genomes/GCA_900094135.1/`, `work/genomes/GCF_900094135.1/`

## Tools / envs
| Tool | Version | Where |
|---|---|---|
| NCBI `datasets` REST | v2alpha | local + curl |
| Python | 3.x stdlib | local (`genome_stats.py`) |
| Prokka | 1.12 | uicgpu conda env bvbrc28 |
| prodigal / barrnap / aragorn | (bundled w/ Prokka) | uicgpu bvbrc28 |
| minced | 2.x | uicgpu bvbrc28 |
| LLM judge | argo:gpt-5.2 (free Argo proxy :44497) | localhost |

## Compute
- Stats recompute: local, <1s.
- Prokka de-novo annotation: uicgpu (A100 node), ~1 min wall.
- minced CRISPR scan: uicgpu, <5s.
