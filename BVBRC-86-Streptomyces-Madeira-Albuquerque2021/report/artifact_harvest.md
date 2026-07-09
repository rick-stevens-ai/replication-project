# Artifact harvest — BVBRC-86

All artifacts pulled from public repositories, no auth required.

## Paper
| Item | URL / accession | Notes |
|------|-----------------|-------|
| PDF (Marine Drugs 2021, 19, 621) | https://europepmc.org/articles/PMC8622039?pdf=render | 1.99 MB, 10 pages. DOI 10.3390/md19110621 |
| Text extraction | pdftotext -layout | 1051 lines, `work/paper.txt` |
| PubMed record | PMID 34822492 | eutils esummary |
| PMC | PMC8622039 | Open-access CC-BY |

## Genome assemblies (NCBI GenBank/RefSeq, BioProject PRJNA754006)
| Isolate | Assembly acc | BioSample | Contig (RefSeq) | Total bp | GC% | Contigs | FTP path |
|---------|--------------|-----------|-----------------|----------|-----|---------|----------|
| MA3_2.13 (*S. profundus* sp. nov.) | GCF_020740535.1 = GCA_020740535.1 | SAMN20720482 | NZ_CP082362.1 | 7,653,710 | 72.14 | 1 | ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/020/740/535/GCF_020740535.1_ASM2074053v1/ |
| S07_1.15 (*S. xinghaiensis* strain) | GCF_020739505.1 = GCA_020739505.1 | SAMN21157270 | NZ_JAJBZK010000001–002.1 | 7,254,545 | 73.07 | 2 | ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/020/739/505/GCF_020739505.1_ASM2073950v1/ |

Files at `work/genomes/` (local) and `/data/stevens/replicate/bvbrc86/` (uicgpu):
- `GCF_020740535.1.fna.gz` (2.02 MB) + `.gff.gz` (0.49 MB)
- `GCF_020739505.1.fna.gz` (1.93 MB) + `.gff.gz` (0.46 MB)

## Reference genomes for ANI
| Ref | Acc | Purpose | Total bp | GC% |
|-----|-----|---------|----------|-----|
| *S. xinghaiensis* S187 | GCA_000220705.1 | ANI vs S07_1.15 | 6,790,523 | 72.5 |
| *Streptomyces* sp. SCSIO 3032 | GCA_002128305.1 | ANI vs MA3_2.13 | 6,287,975 | 73.5 |

## antiSMASH outputs (v6.1.1, docker `antismash/standalone:6.1.1` on uicgpu)
| Isolate | # BGCs (regions) | JSON | Region GBK files | ZIP |
|---------|------------------|------|-----------------|-----|
| MA3_2.13 | 27 | `out_MA3/GCF_020740535.1.json` (33 MB) | region001..region027 | 116 MB |
| S07_1.15 | 24 | `out_S07/GCF_020739505.1.json` (22 MB) | region001..region024 | 58 MB |

Second antiSMASH pass with `--cb-knownclusters` (against MIBiG):
| Isolate | JSON | Known-cluster hits (extract) |
|---------|------|------------------------------|
| MA3_2.13 | `out_MA3_kcb/GCF_020740535.1.json` | atratumycin, triacsins, arsono-polyketide, pladienolide B, BE-14106, elaiophylin, ectoine, desferrioxamine E, geosmin, hopene, +14 more |
| S07_1.15 | `out_S07_kcb/GCF_020739505.1.json` | ectoine, hopene, desferrioxamine E, SapB, kistamicin A, neomycin, isorenieratene, LL-D49194α1, +8 more |

## Tool provenance
| Tool | Version | Where |
|------|---------|-------|
| antiSMASH | 6.1.1 (docker antismash/standalone:6.1.1) | uicgpu |
| skani | 0.3.x | CherryRd /usr/local/bin/skani |
| fastANI | 1.x | CherryRd /usr/local/bin/fastANI |
| Prodigal (via antiSMASH) | shipped in docker image | uicgpu |
| pdftotext (Poppler) | system | CherryRd |
| Argo proxy | localhost:44497, model argo:claude-sonnet-4.6 | LLM-judge for verdict |

## Evidence copied into `report/evidence/`
- `assembly_stats_recomputed.tsv` — bp / GC% / contigs recomputed from downloaded FASTAs.
- `ani_results.tsv` — skani + fastANI outputs for the two species-boundary calls.
- `bgc_summary_table.tsv` — per-region product listing for both isolates.
- `known_cluster_hits.tsv` — top MIBiG hit per region for both isolates.
- `paper_vs_replication_table.md` — side-by-side of every quantitative claim.
- `llm_judge_response.txt` — Argo Claude Sonnet 4.6 verdict.
