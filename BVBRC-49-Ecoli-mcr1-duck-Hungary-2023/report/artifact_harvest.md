# Artifact Harvest — BVBRC-49

All artifacts free / public. No paid endpoints used.

## Publication
| Artifact | ID / URL | Notes |
|---|---|---|
| Full text XML | Europe PMC `PMC10604428/fullTextXML` | 120 KB, MD5 `20aa9f144c8a351a30a594c5b49a42da`. → `work/fulltext.xml`, `work/fulltext.txt` |
| DOI | 10.3390/antibiotics12101519 | Antibiotics 2023, 12(10):1519, OA CC BY 4.0 |
| PMID / PMCID | 37887221 / PMC10604428 | |

## Genome data (NCBI)
| Artifact | Accession | Size | Notes |
|---|---|---|---|
| BioProject | PRJNA1012593 | — | Strain Ec45-2020 deposit |
| Assembly | GCF_038709795.1 / GCA_038709795.1 (ASM3870979v1) | — | Chromosome level, biosample SAMN37265790 |
| Download zip | via NCBI Datasets v2alpha REST | 3.1 MB | genome+protein+GFF+seq_report → `work/GCF_038709795.1.zip` |
| Genome FASTA | 6 replicons | 5.4 MB | MD5 `3a9547a5aa4bf5103b048122af878eac` |

### Replicons (accession → paper name → length bp / GC%)
- NZ_CP134085.1 → chromosome → 4,967,063 / 50.73
- NZ_CP134088.1 → pEc45-2020-254kb (IncHI MDR) → 254,224 / 47.51
- NZ_CP134087.1 → pEc45-2020-190kb (virulence) → 190,488 / 50.81
- NZ_CP134086.1 → pEc45-2020-101kb → 101,848 / 47.37
- NZ_CP134089.1 → pEc45-2020-33kb (IncX4, **mcr-1**) → 33,541 / 41.84
- NZ_CP134090.1 → pEc45-2020-5kb → 5,714 / 46.94

## Tool databases
| Tool | Version | DB version |
|---|---|---|
| mlst | 2.33.1 | ecoli_achtman_4 scheme (bundled) |
| AMRFinderPlus | 4.2.7 | 2026-03-24.1 |
| abricate | 1.4.0 | resfinder / plasmidfinder / vfdb, 2026-Apr-3 |

## Evidence files (report/evidence/)
- `genome_stats.json` — per-replicon length + GC
- `mlst.tsv` — ST162 allele profile
- `amrfinder.tsv` — full AMRFinderPlus output (AMR + point mutations + virulence + stress)
- `amrfinder.err` — AMRFinder run log (63 s)
- `abricate_resfinder.tsv` — acquired ARGs with coordinates
- `abricate_plasmidfinder.tsv` — plasmid replicon types with coordinates
- `abricate_vfdb.tsv` — 124 virulence-factor hits
- `llm_judge_input.txt` / `llm_judge_gpt52.md` — free-Argo gpt-5.2 scoring (Coverage 8/10, Agreement 9/10, PARTIAL)
