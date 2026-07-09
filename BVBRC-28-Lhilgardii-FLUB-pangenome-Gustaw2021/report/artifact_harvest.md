# Artifact Harvest — BVBRC-28

All artifacts are public and free (no auth). Genome data via NCBI Datasets v2alpha REST API.

## Paper (open access)
| Artifact | Source | Notes |
|---|---|---|
| Full-text XML | Europe PMC `PMC8038741/fullTextXML` | 222,923 bytes; used to extract accessions + numeric claims |
| Bibliographic/abstract | Europe PMC `EXT_ID:33917427` core | Title, DOI 10.3390/ijms22073780, OA=Y |

## FLUB primary deposit (from paper Methods)
- **BioProject:** PRJNA595831
- **Chromosome:** CP047121.1 (3,071,102 bp)
- **Plasmids:** CP047122.1 (42,732), CP047123.1 (37,669), CP047124.1 (28,299), CP047125.1 (6,896), CP047126.1 (3,528)
- **Assembly:** GCF_009832765.1 / GCA_009832765.1 (RefSeq / GenBank), total 3,190,226 bp

## Genomes pulled (NCBI Datasets REST, GENOME_FASTA)
| Accession | Strain | Level | Length (bp) | Contigs | GC% | Role |
|---|---|---|---:|---:|---:|---|
| GCF_009832765.1 | FLUB | Complete | 3,190,226 | 6 | 40.09 | **subject** |
| GCF_004354795.1 | ATCC 8290 | Scaffold | 2,769,673 | 92 | 39.87 | type-strain lineage (paper reference) |
| GCF_001434655.1 | DSM 20176 | Contig | 2,603,106 | 125 | 39.58 | = ATCC 8290 deposit |
| GCF_011765585.1 | LMG 07934 | Complete | 2,771,862 | 1 | 39.75 | NZ_CP050262, paper comparator |
| GCF_000159175.1 | ATCC 27305 | Scaffold | 3,144,656 | 106 | 39.14 | = L. brevis gravesensis / closest ANI neighbor |
| GCF_008694025.1 | LH500 | Complete | 2,654,177 | 1 | 39.75 | additional L. hilgardii complete genome |

Download URL pattern:
`https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/<ACC>/download?include_annotation_type=GENOME_FASTA`

## Cross-validation pass — exact paper Table-2 5-strain set (2026-07-01)
| Accession | Strain | Level | Length (bp) | Contigs | GC% | Source |
|---|---|---|---:|---:|---:|---|
| GCA_009832765.1 | FLUB | Complete | 3,190,226 | 6 | 40.09 | NCBI Datasets |
| GCA_011765585.1 | LMG 07934 | Complete | 2,771,862 | 1 | 39.75 | NCBI Datasets |
| GCA_008694025.1 | LH500 | Complete | 2,654,177 | 1 | 39.75 | NCBI Datasets |
| GCA_902374015.1 | MGYG-HGUT-01333 | Scaffold | 3,144,656 | 106 | 39.14 | **ENA** (no seq on NCBI — EBI MAG) |
| GCA_001434655.1 | DSM 20176 | Contig | 2,603,106 | 125 | 39.58 | NCBI Datasets |

ENA fallback URL: `https://www.ebi.ac.uk/ena/browser/api/fasta/GCA_902374015?download=true`

## Tool artifacts produced
- `work/genome_stats.json` / `evidence/genome_stats.json` — assembly stats (both passes)
- `work/fastani_all.tsv`, `evidence/ani_result.json` — all-vs-all FastANI matrix
- `work/roary5/`, `work/roary6/` — Roary pangenome outputs (pipeline 1)
- `evidence/mmseqs_clusters.tsv`, `evidence/pangenome_result.json` — mmseqs2 pangenome (pipeline 2)
- `evidence/core_genome.nwk`, `evidence/core_tree_result.json` — core-genome ML tree + pairwise core-proteome identity
- `evidence/llm_judge_response.json` (pass 1), `evidence/llm_judge_consolidated.json` (consolidated) — Argo gpt-5.2 verdicts
- `work/pangenome.sh`, `work/pangenome_analyze.py`, `work/coregenome_tree.py`, `work/genome_stats.py`, `work/llm_judge2.py` — reproducibility scripts
