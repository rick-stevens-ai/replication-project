# Artifact Harvest — BVBRC-37

## Paper
| Item | Value |
|---|---|
| Title | Phylogenomic Analysis of *Salmonella enterica* subsp. *enterica* Serovar Bovismorbificans from Clinical and Food Samples … Two Distinct Polyphyletic Genome Pathotypes |
| Authors | Gopinath GR, Jang H, Beaubrun JJ-G, Gangiredla J, Mammel M, Müller A, Tamber S, Patel IR, Ewing L, et al. |
| Journal | *Microorganisms* 10(6):1199 (2022) |
| DOI | 10.3390/microorganisms10061199 |
| PMC | PMC9228720 · PMID 35744717 |
| OA | GOLD, CC-BY (full text via PMC) |

## Data (all public, free, no-auth NCBI Datasets REST)
| Artifact | Accession / URL | Notes |
|---|---|---|
| BioProject (paper's deposition) | PRJNA378379 (GenomeTrakr; umbrella PRJNA186875) | 425 total genomes; **82 are serovar Bovismorbificans** |
| Bovismorbificans genome set | 82 assemblies (81 Contig + 1 Chromosome), GCA_009757xxx–GCA_0097xxxxx series | Downloaded as one 117 MB datasets zip (`bovis_all.zip`), validated 82/82 |
| BioSample cross-check | e.g. SAMN12657228 = strain N14_0646 = WGS WSDC01 (matches paper Table 1) | Confirms these ARE the paper's genomes |
| Source/host metadata | NCBI BioSample attributes per accession | 70 clinical/human, 8 food, + animal/env/feed; CH 75 / CA 5 / US 2 |

## Tools / DBs
| Tool | Version | Source |
|---|---|---|
| NCBI datasets CLI | 18.32.0 | bioconda (micromamba env `amr`) |
| SeqSero2 | 1.3.2 | bioconda |
| mlst | 2.35.0 (scheme `senterica_achtman_2`, pubMLST) | bioconda |
| mash | 2.3 | bioconda (installed this run) |
| AMRFinderPlus | 3.12.8, DB 2024-07-22.1 | bioconda |
| scipy | 1.18.0 (average-linkage hierarchical clustering) | local |

## Compute
- uicgpu (8×A100, 255 cores) — download + SeqSero2 + mlst + mash + AMRFinder; proxy internet via `~/env.sh`.
- Local (CherryRd) — clustering, figures, LLM-judge.

## Evidence files (`report/evidence/`)
- `mlst.tsv`, `seqsero_summary.tsv`, `mash_dist.tsv`, `amr_all.tsv`, `amr_summary.json`
- `cluster_result.json`, `genome_table.tsv/json`, `source_meta.json`, `dendrogram.png`
- `llm_judge_verdict.txt`
