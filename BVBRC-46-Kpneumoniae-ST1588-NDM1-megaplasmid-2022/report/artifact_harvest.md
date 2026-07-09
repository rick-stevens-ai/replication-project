# Artifact Harvest — BVBRC-46

All artifacts are public and free. No paid endpoints used.

## Publication
| Artifact | ID / URL | Notes |
|---|---|---|
| Paper (OA, CC-BY) | PMC9494972 / DOI 10.3390/antibiotics11091207 | Antibiotics 2022, 11(9):1207 |
| Full-text XML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9494972/fullTextXML | 88,640 bytes → `work/fulltext.xml` |

## Sequences (NCBI Datasets v2alpha REST, no auth)
| Accession | Description | Size | md5 (local FASTA) |
|---|---|---|---|
| GCF_023554495.1 | K. pneumoniae UCO-361 assembly (WGS JAMJQY01, BioSample SAMN28534325) | 5.2 MB zip | 988216d6ebc1fda9ca240afcb709f4d8 (zip) |
| NZ_JAMJQY010000001.1 | chromosome | 5,288,551 bp (GC 57.36%) | 7850b8ab9ce126ffb68be5458eaf72e9 |
| NZ_JAMJQY010000002.1 | **megaplasmid pNDM-1_UCO-361** | **314,976 bp** (GC 47.08%) | 6df4325d66e71d0624e599998c7c80fe |
| NZ_JAMJQY010000003.1 | **IncFIB(K) plasmid** | **197,209 bp** (GC 52.15%) | 878f6adbb3d29b516569963a890787f9 |
| NZ_MN598004.1 | pNDM-1-EC12 (E. cloacae, comparison plasmid) | 351,777 bp | cd4d0ce69253e57f059bbb0968943038 |
| CP041388 | Raoultella (K. ornithinolytica) pRAO166a megaplasmid (context only) | 382,325 bp | — (metadata only) |

## Databases / tools (uicgpu conda envs)
| Tool | Version | Env | DB |
|---|---|---|---|
| Kleborate | v3.2.4 (preset kpsc) | /data/stevens/envs/kleborate | bundled KpSC MLST + Kaptive KL/OL + AMRFinderPlus |
| abricate | (2026-Apr-3 DBs) | /data/stevens/envs/bvbrc14 | plasmidfinder(488), resfinder(3206), ncbi(8232), card(6052) |
| AMRFinderPlus | --organism Klebsiella_pneumoniae --plus | /data/stevens/envs/bvbrc14 | NCBI AMR + point/stress |
| blastn / makeblastdb | BLAST+ | local + bvbrc28 | ad-hoc plasmid-vs-plasmid |
| NCBI Datasets | v2alpha REST | bvbrc28 | genome download |
| PGAP annotation | (from GCF_023554495.1 genomic.gff) | — | Tn3000 gene order |

## Evidence files (report/evidence/)
- `summary.json` — all reproduced values vs paper
- `kleborate_result.tsv` — full Kleborate kpsc output (ST/K/O/resistome)
- `abricate_plasmidfinder.tsv`, `abricate_resfinder.tsv`, `abricate_ncbi.tsv` — per-contig typing
- `amrfinder_out.tsv` — AMRFinderPlus full genome (AMR + stress by contig)
- `llm_judge.txt` — free-Argo (gpt-5.2) judge verdict
