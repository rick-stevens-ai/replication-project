# Artifacts Summary — BVBRC-86 Streptomyces (Albuquerque et al. 2021)

Inventory of every artifact produced or consumed by this replication, with provenance and role.

## Source material (paper + deposited public data)

| Path | Provenance | Role |
|------|------------|------|
| `work/paper.pdf` | EuropePMC OA render (PMC8622039) | Paper source, 1.99 MB, 10 pp |
| `work/paper.txt` | Text extract from paper.pdf | Claim grep / identification |
| `work/genomes/GCF_020740535.1.fna` | NCBI FTP (assembly UID 11377691) | MA3_2.13 / *S. profundus* nucleotide assembly |
| `work/genomes/GCF_020740535.1.gff` | NCBI FTP | MA3_2.13 PGAP annotation |
| `work/genomes/GCF_020739505.1.fna` | NCBI FTP (assembly UID 11376371) | S07_1.15 / *S. xinghaiensis* nucleotide assembly |
| `work/genomes/GCF_020739505.1.gff` | NCBI FTP | S07_1.15 PGAP annotation |
| `work/genomes/GCA_000220705.1.fna` | NCBI FTP | ANI reference: *S. xinghaiensis* S187 (paper's reference) |
| `work/genomes/GCA_002128305.1.fna` | NCBI FTP | ANI reference: *Streptomyces* sp. SCSIO 3032 (paper's reference) |

## Evidence files (report/evidence/)

| File | Contents | How produced |
|------|----------|--------------|
| `assembly_stats_recomputed.tsv` | Per-record total bp, GC%, contig count for both isolates | Python FASTA parse of `work/genomes/*.fna` |
| `ani_results.tsv` | skani + fastANI ANI values for S07 vs S187 and MA3 vs SCSIO 3032 | `skani dist` + `fastANI` on CherryRd |
| `bgc_summary_table.tsv` | 52 rows (header + one per antiSMASH region), both isolates: region id, product category, length | antiSMASH v6.1.1 general pass JSON export |
| `known_cluster_hits.tsv` | Top MIBiG hit per region: BGC id, blast score, gene-level hit count | antiSMASH v6.1.1 knownclusterblast pass JSON export |
| `paper_vs_replication_table.md` | Full claim-by-claim table paper vs rerun | Assembled from all evidence files |
| `llm_judge_response.txt` | Verbatim Argo Claude Sonnet 4.6 response | POST to `localhost:44497/v1/chat/completions` |
| `antismash/MA3_2.13_general.json.gz` | Full antiSMASH v6.1.1 general-pass JSON for MA3_2.13 (~4.3–7.4 MB compressed) | Docker `antismash/standalone:6.1.1` pass 1 |
| `antismash/MA3_2.13_knownclusters.json.gz` | antiSMASH knownclusterblast JSON for MA3_2.13 | Docker pass 2 |
| `antismash/S07_1.15_general.json.gz` | antiSMASH general-pass JSON for S07_1.15 | Docker pass 1 |
| `antismash/S07_1.15_knownclusters.json.gz` | antiSMASH knownclusterblast JSON for S07_1.15 | Docker pass 2 |

## Off-Dropbox large artifacts (uicgpu)

| Path | Contents | Retrieval |
|------|----------|-----------|
| `uicgpu:/data/stevens/replicate/bvbrc86/out_MA3/` | Full antiSMASH general-pass output tree for MA3_2.13: per-region GBK files, HTML report, PNG plots, region index | `scp -r` on demand |
| `uicgpu:/data/stevens/replicate/bvbrc86/out_MA3_kcb/` | Full knownclusterblast output tree for MA3_2.13 | `scp -r` on demand |
| `uicgpu:/data/stevens/replicate/bvbrc86/out_S07/` | Full antiSMASH general-pass output tree for S07_1.15 | `scp -r` on demand |
| `uicgpu:/data/stevens/replicate/bvbrc86/out_S07_kcb/` | Full knownclusterblast output tree for S07_1.15 | `scp -r` on demand |

Not copied to Dropbox to save space (each full output tree is several hundred MB with all per-region GBKs + HTML + PNGs).

## Reports (report/)

| File | Role |
|------|------|
| `REPORT.md` | Full narrative replication report (source of truth) |
| `REPORT.tex` | LaTeX version with dedicated Genuine Critique section |
| `brief.md` | 1-paragraph summary |
| `attempt_log.md` | Chronological execution log |
| `artifact_harvest.md` | Every public artifact pulled with URL / accession |
| `artifacts_summary.md` | This file — inventory + provenance for evidence artifacts |
| `workflow.md` | Executable workflow, step-by-step |
| `failure_analysis.md` | What was NOT reproduced and why, plus what could go wrong |
| `open_questions.json` | 5 grounded follow-up questions |

## Key resolved identifiers

| Identifier | Value | Points to |
|------------|-------|-----------|
| BioProject | PRJNA754006 | Both isolate deposits |
| Assembly UID | 11377691 | GCF_020740535.1 (MA3_2.13) |
| Assembly UID | 11376371 | GCF_020739505.1 (S07_1.15) |
| BioSample | SAMN20720482 | MA3_2.13 |
| BioSample | SAMN21157270 | S07_1.15 |
| Genome accession | CP082362 | MA3_2.13 chromosome (closed) |
| Genome accession | JAJBZK010000001–002 | S07_1.15 (two contigs) |
| DOI | 10.3390/md19110621 | Paper |
| PMID | 34822492 | Paper |
| PMC | PMC8622039 | Open-access PDF source |
| MIBiG (atratumycin) | BGC0001975 | Top hit for MA3 region_008 |
| MIBiG (triacsins) | BGC0001983 | Top hit for MA3 region_014 |
| MIBiG (arsono-PK) | BGC0001283 | Top hit for MA3 region_021 |

## Tool / compute environment

| Component | Version | Host |
|-----------|---------|------|
| skani | v0.3.x | CherryRd (`/usr/local/bin/skani`) |
| fastANI | v1.x | CherryRd (`/usr/local/bin/fastANI`) |
| antiSMASH docker | `antismash/standalone:6.1.1` | uicgpu 8×A100, 32 CPU per container |
| Argo proxy | localhost:44497 | CherryRd |
| LLM-judge model | `argo:claude-sonnet-4.6` | Free endpoint per wave-brief rule |
| Python | 3.x (FASTA parse, GFF parse) | CherryRd |

## Integrity notes
- Deposited assembly SHA-256 recorded at download time (in `attempt_log.md`).
- antiSMASH JSONs archived compressed and unchanged from container output.
- LLM-judge response saved verbatim (no paraphrasing).
- Docker image tag pinned to `6.1.1`; container image digest NOT archived (limitation — see `failure_analysis.md` and REPORT.tex critique #8).
