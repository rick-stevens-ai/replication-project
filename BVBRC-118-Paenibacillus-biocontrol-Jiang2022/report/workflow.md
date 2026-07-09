# Workflow — BVBRC-118 (Jiang 2022, *P. peoriae* HJ-2)

## Narrative

```
paper (PMC PMC8876185)                                  paper.pdf (BMC OA)
   |
   +--> pdftotext -layout ---------------------------> paper.txt   (line grep for accessions)
   +--> marker 1.11 (uicgpu GPU 2) -------------------> extraction/marker.md
   +--> nougat 0.1  (uicgpu GPU 3) -------------------> extraction/nougat.mmd

BioProject PRJNA580302 (esearch/elink)
   |
   +--> SRR10363117 (SRA S3 direct, 329 MB) --> fasterq-dump 3.4.1
                                                     |
                                                     v
                       SRR10363117.fastq  (183,095 reads / 1.30 Gbp)
                                                     |
                                                     v
                             flye 2.9.6-b1802 --pacbio-raw --genome-size 6m --threads 64
                                                     |
                                                     v
                     assembly.fasta  (1 contig, 6,007,189 bp, circular=Y, mean_cov=205)
                                       |                |                    |
                                       v                v                    v
                              prokka 1.14.6    antismash 8.0.4        skani + mash
                              (bvbrc76 env)   (run1 basic; run2       vs IBSD35 / HS311 / ZF390
                                               with --cb-known)          (references from NCBI FTP)
                                       |                |                    |
                                       v                v                    v
                            HJ2.gff / .txt      HJ2.json / regions      ANI matrix
                            5244 CDS,           19 BGC regions;         IBSD35=97.59  (highest)
                            39 rRNA, 108 tRNA   6 named compounds       HS311 =97.56
                                                match paper Table 4     ZF390 =96.38
                                                                             |
                                                                             v
                                                              LLM-judge (argo:claude-opus-4.6)
                                                                             |
                                                                             v
                                                              overall_verdict: REPLICATED
                                                                 (100% coverage, 97% agreement)
```

## Enumerated tools/codes/scripts

| # | Tool | Version | Purpose | Host / env |
|---|------|---------|---------|------------|
| 1 | `curl` | system | PDF fetch (BMC OA), SRA S3 fetch, NCBI FTP fetch | CherryRd + uicgpu |
| 2 | `pdftotext` | poppler | Layout text extraction of paper.pdf | CherryRd |
| 3 | `marker_single` | marker ~1.11 | PDF→Markdown structured extraction | uicgpu, `/gpustor/stevens/anaconda3/envs/marker`, GPU 2 |
| 4 | `nougat` | 0.1.x | PDF→Mathpix-flavour Markdown | uicgpu, `/gpustor/stevens/anaconda3/envs/nougat`, GPU 3 |
| 5 | NCBI eutils (esearch/esummary/elink) | v2 REST | Discover accessions from PRJNA580302 | CherryRd |
| 6 | `fasterq-dump` | 3.4.1 | .sra → .fastq | uicgpu, `micromamba/envs/amr` |
| 7 | `flye` | 2.9.6-b1802 | PacBio de novo assembler | uicgpu, `/data/stevens/envs/bvbrc14` |
| 8 | `prokka` | 1.14.6 | Bacterial annotation | uicgpu, `miniforge3/envs/bvbrc76` |
| 9 | `antiSMASH` | 8.0.4 | Secondary-metabolite BGC prediction + MIBiG matching | uicgpu, `/data/stevens/envs/antismash` |
| 10 | `skani` | (amr env) | ANI computation | uicgpu, `micromamba/envs/amr` |
| 11 | `mash` | 2.x | k-mer distance | uicgpu, `micromamba/envs/amr` |
| 12 | `blastp / makeblastdb` | ncbi-blast+ 2.16 | (available; unused this run — antiSMASH knownclusterblast subsumed it) | uicgpu, `bvbrc76` |
| 13 | Custom Python `parse_antismash.py` | this run | Extract per-region MIBiG top-hit compound + hits/total | /tmp on uicgpu |
| 14 | Custom Python `judge_bvbrc118.py` | this run | LLM-judge scoring via LiteLLM aggregator → Argo Opus 4.6 | CherryRd |
| 15 | LiteLLM aggregator | (cherryrd :4000) | Route Argo Opus 4.6 (`argo:claude-opus-4.6`); Free ANL endpoint | CherryRd :4000 |

## Effort estimate

| Phase | Wall clock | Human-equivalent steps | LOC written | GPU-time | CPU-time |
|-------|-----------|------------------------|-------------|----------|----------|
| Paper acquisition + accession discovery | ~5 min | 8 grep/eutils queries | 0 | 0 | 0 |
| Marker + Nougat extraction | ~90 s | 2 job submissions | 0 | ~90 s on 2 GPUs | 0 |
| SRA download + fastq conversion | ~2 min | 2 commands (with 1 proxy pivot) | 0 | 0 | ~30 s CPU (32 threads) |
| Flye assembly | ~9 min | 1 command | 0 | 0 | ~9 min × 64 threads |
| Prokka annotation | ~40 s | 1 command | 0 | 0 | ~40 s × 32 threads |
| antiSMASH run 1 (basic) | ~3 min | 1 command | 0 | 0 | ~3 min × 32 threads |
| antiSMASH run 2 (knownclusterblast + PfamGO) | ~13 min | 1 command | 0 | 0 | ~13 min × 32 threads (diamond blastp dominates) |
| Reference genome downloads (IBSD35, HS311, ZF390) | ~10 s | 3 curl commands | 0 | 0 | 0 |
| skani + mash ANI | ~2 s | 2 commands | 0 | 0 | 0 |
| Circular-rotation analysis | ~1 min | 1 Python snippet | ~25 | 0 | 0 |
| antiSMASH JSON parser | ~2 min | script write + run | 45 | 0 | 0 |
| LLM-judge scoring | ~2 min | 1 API call | 130 | 0 | 0 |
| Report + LaTeX + open questions + failure analysis | ~30 min agent-writing | 5 doc files | ~600 (Markdown/JSON/LaTeX) | 0 | 0 |
| **Total** | **~55 min** end-to-end | ~20 discrete actions | ~800 | ~90 s | ~28 min-thread-equivalent |

Peak concurrent GPU use: 2 (marker on GPU 2, nougat on GPU 3, briefly).
Peak concurrent CPU: 64 threads (Flye).
Peak RAM: ~40 GB on uicgpu during antiSMASH knownclusterblast diamond blastp phase.
