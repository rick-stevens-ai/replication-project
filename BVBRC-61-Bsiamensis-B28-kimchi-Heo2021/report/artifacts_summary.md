# Artifacts Summary — BVBRC-61 (Heo et al. 2021, *B. siamensis* B28)

Audit trail of every artifact produced by this replication. All paths relative to the set root:
`~/Dropbox/REPLICATE-PROJECT/BVBRC-61-Bsiamensis-B28-kimchi-Heo2021/`.

## Paper & metadata
| Artifact | Path | Source | Notes |
|---|---|---|---|
| Paper full-text XML | `work/paper_fulltext.xml` | Europe PMC OA | PMC8394110, CC BY 4.0 |
| Claim extraction | `work/claims.md` | manual + regex | C1–C5 |
| Accession list | `work/accessions.txt` | manual | CP066219–21, GCF_016313165.1 + 6 comparators |

## Genomes (NCBI `datasets` v18.25.1)
| Strain | Assembly | Files | Contigs | Purpose |
|---|---|---|---|---|
| **B28** | GCF_016313165.1 | genomic.fna, protein.faa (3,808), genomic.gff | 3 (chr + 2 plasmids) | Query genome |
| B. siamensis KCTC 13613ᵀ | GCA_000262045.1 | genomic.fna | 51 (incomplete) | ANI reference |
| B. siamensis SCSIO 05746 | GCA_002850535.1 | genomic.fna | 2 (complete) | ANI reference |
| B. amyloliquefaciens FS1092 | (paper accession) | genomic.fna | — | ANI reference |
| B. amyloliquefaciens RD7-7 | (paper accession) | genomic.fna | — | ANI reference |
| B. velezensis JJ-D34 | (paper accession) | genomic.fna | — | ANI reference |
| B. velezensis KMU01 | (paper accession) | genomic.fna | — | ANI reference |

Full manifest in `artifact_harvest.md` with checksums.

## Analysis outputs
| Artifact | Path | Tool + version | Key result |
|---|---|---|---|
| Genome stats | `work/genome_stats.tsv` | `genome_stats.py` | chr 3,946,178 bp / GC 45.85% / 86 tRNA / 27 rRNA — **all EXACT vs paper** |
| fastANI matrix | `work/fastani.tsv` | fastANI (default) | 98.42% / 97.55% (siamensis) vs 94.32% / 94.21% (velezensis / amyloliquefaciens) |
| skani matrix | `work/skani.tsv` | skani | 98.54% / 97.67% vs 94.18% / 94.19% |
| AMRFinderPlus report | `work/amrfinderplus.tsv` | AMRFinderPlus 4.2.7 / DB 2026-03-24.1 | 5 hits, all `scope=core` |
| CARD/RGI report | `work/card_rgi.json` | RGI/CARD 3.2.7 (DIAMOND, protein) | 9 Strict / 0 Perfect — all intrinsic |
| Enterotoxin scan | `work/enterotoxin_scan.txt` | proteome regex | 0 hits (Nhe/Hbl/CytK ABSENT) |
| Hemolysin-III scan | `work/hly_scan.txt` | proteome regex | 4 hits (PRESENT — matches paper) |
| Functional survey | `evidence/func_survey.json` | `func_survey.py` | all paper categories confirmed |
| MLST | `work/mlst.tsv` | mlst 2.33.1 (bsubtilis scheme) | matched paper |
| LLM-judge | `evidence/llm_judge.txt` | Argo gpt-5.2 (free), temp 0 | verdict: PARTIAL |

## Reports
| Artifact | Path | Purpose |
|---|---|---|
| Markdown report | `report/REPORT.md` | Primary human-readable report |
| **LaTeX report** | `report/REPORT.tex` | **Formal report + Genuine Critique section (this backfill)** |
| Workflow | `report/workflow.md` | Method / pipeline log |
| Artifacts summary | `report/artifacts_summary.md` | This file |
| Failure analysis | `report/failure_analysis.md` | What didn't reproduce / limitations |
| Open questions | `report/open_questions.json` | 5 follow-on scientific questions |
| Artifact harvest | `artifact_harvest.md` | Full tool/version/checksum audit |

## Evidence dir
| Artifact | Path | Content |
|---|---|---|
| Functional survey | `evidence/func_survey.json` | Regex-matched hits per functional category |
| LLM judge transcript | `evidence/llm_judge.txt` | Full Argo gpt-5.2 verdict + reasoning |

## Verdict summary
- **Verdict:** PARTIAL (strong)
- **Testable-from-sequence claims:** ~8/9 reproduced (one naming caveat on bacteriocin operon)
- **Wet-lab claims:** 3 out of reach (enterotoxin PCR gel, disc-diffusion phenotype, antibacterial-activity plate)
- **Contradictions:** 0
- **Cost:** $0 (free tools + free Argo LLM + Europe PMC OA XML)
