# Artifact Harvest — BVBRC-26

All artifacts are public and free. Sequence bytes from NCBI Datasets; identity/curation
layer from BV-BRC (patricbrc.org data API). Checksums = first 16 hex of SHA-256.

## Primary literature
| Artifact | Source | Accession/URL | Size | SHA-256(16) |
|---|---|---|---|---|
| Paper full text (JATS XML) | Europe PMC | PMC9519451 (`/webservices/rest/PMC9519451/fullTextXML`) | 136K | e655f994b2f0f4c4 |
| Supplementary Tables S1–S8 | Nature Microbiol. (from sibling dir; MOESM2_ESM.xlsx) | 41564_2022_1219_MOESM2_ESM | 84K | b3ab38d4c16bea68 |

## Defence system proteins (paper-deposited)
| Artifact | Source | Detail | Size | SHA-256(16) |
|---|---|---|---|---|
| `defense_representatives.fasta` | NCBI protein (via sibling harvest) | 21 system reps (1 CDS/system) | 12K | 8fe30da56aa22e0e |
| `defense_proteins.fasta` | NCBI protein | all 32 CDS components | 16K | 432940535fa785c1 |

## Corpus: 71 source strains
| Artifact | Source | Detail | Size | SHA-256(16) |
|---|---|---|---|---|
| `paper_S5_source_strains.json` | Table S5 | 71 strains, GCA assembly accessions | — | — |
| `bvbrc_genome_map.json` | BV-BRC `genome` API | 71/71 GCA → BV-BRC genome_id (by `assembly_accession`) | 28K | a717c32ba96a5e1b |
| `ncbi_proteomes/*.faa` (71) | NCBI Datasets REST (PROT_FASTA, by GCA) | 348,507 proteins; files named by BV-BRC genome_id | 122M | (per-file) |
| `ncbi_proteome_summary.json` | — | per-strain protein counts | 8K | eeb5f738f2a4cd62 |

BV-BRC genome_ids used (all in the source Genome Group): ECOR panel 562.333xx / 562.334xx
(52 strains) + UMB clinical panel 562.387xx / 562.388xx / 562.453xx (19 strains). Full
GCA↔genome_id map in `bvbrc_genome_map.json`.

## Analysis outputs
| Artifact | Produced by | Detail | Size | SHA-256(16) |
|---|---|---|---|---|
| `blast/rep_vs_all71.tsv` | BLASTP 21 reps vs 71-strain DB | 101 hit rows (outfmt 6) | 8K | e60a2de4bb380829 |
| `blast/distribution_summary.json` | build_distribution.py | per-system presence across 71 strains + source recovery | 8K | 8ef35d3d1b393d2a |
| `mge_context_summary.json` | mge_context.py | ±20-gene MGE/prophage + hotspot context per system | 16K | cb42637c1e858bd4 |
| `crispr_rm_survey.json` | crispr_survey.py | CRISPR-Cas + RM presence across 71 strains | 20K | 82c6f6eeb4ed3173 |
| `llm_judge_verdict.txt` | llm_judge.py (Argo argo:gpt-o3, free) | verdict + scores | — | — |

## APIs / tools
- BV-BRC data API: `https://patricbrc.org/api/{genome,genome_feature}/` — free, no auth.
- NCBI Datasets v2alpha REST: `https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/<GCA>/download` — free, no auth.
- Europe PMC REST — free.
- Local: BLAST+ (blastp, makeblastdb), Python 3, openpyxl.
- LLM: Argo proxy `http://127.0.0.1:44497/v1` (key=stevens), model `argo:gpt-o3` — free.
