# Artifacts Summary — BVBRC-56 Liu et al. (2013) *E. cloacae*

Verdict: **PARTIAL** · Set: BVBRC-56 · Replication date: 2026-07-02

## Input artifacts

| Type | Source | Access | Notes |
|---|---|---|---|
| Paper text | Europe PMC (PMC3771936) | Free, no-auth (XML full-text) | Used for claim extraction; NOT the paid `pdf` tool |
| ENHKU01 genome | NCBI nuccore **CP003737.1** | Free, `efetch` | Complete chromosome, ~4.73 Mb, 0 plasmids |
| ATCC13047 genome | NCBI nuccore | Free, `efetch` | Complete, ~5.60 Mb, 2 plasmids |
| EcWSU1 genome | NCBI nuccore | Free, `efetch` | Complete, ~4.80 Mb, 1 plasmid |
| SDM genome | NCBI nuccore | Free, `efetch` | Complete, ~4.97 Mb, 0 plasmids |
| Other 4 *Enterobacter* spp. | NCBI nuccore | Free, `efetch` | For AAI phylogenomics |
| 3 *Pantoea* outgroups | NCBI nuccore | Free, `efetch` | For AAI phylogenomics |

**Total re-downloaded genomes:** 11 (all complete, all public, no BV-BRC private data).

## Compute-derived artifacts

| Artifact | Description | Key numbers |
|---|---|---|
| Genome-stats table | Per-strain length, replicon count, GC%, CDS, tRNA, rRNA | 4/4 CDS totals exact; GC 54.54–55.07% |
| Pan-genome cluster set | DIAMOND-RBH single-linkage on 4 *E. cloacae* proteomes | 6642 pan-clusters, 3345 core |
| AAI matrix | 55 pairwise AAI values across 8 Enterobacter + 3 Pantoea | E. cloacae clade 93.6–94.0%; Pantoea↔Ent 72–73% |
| NJ phylogenomic tree | From (100−AAI)/100 distances | E. cloacae clade + clean Pantoea outgroup |
| T6SS cluster calls | Contiguous ≥6-component-gene rule | ATCC13047=2, SDM=1, ENHKU01=1+frag, EcWSU1=0 |
| Fimbriae locus calls | Keyword net over product/gene | 8–19 per strain (paper 9–13) |
| Carbohydrate gene counts | Keyword net over product | 424–432 per strain (paper >640) |
| LLM judge verdict | Free-Argo `gpt-5.2`, full claim table | **PARTIAL** (concordant) |

## Output files (this report dir)

| File | Purpose |
|---|---|
| REPORT.md | Primary narrative report (source of truth) |
| REPORT.tex | LaTeX rendition + dedicated Genuine Critique section |
| workflow.md | Step-by-step reproducibility trace |
| open_questions.json | 5 open-scientific-question objects (Enterobacter complex biology) |
| artifacts_summary.md | This file — input/output inventory |
| failure_analysis.md | What did / did not replicate + limitation audit |

## What the artifacts do NOT include

- No wet-lab antagonism-assay reproduction (C11 is intrinsically out-of-scope for in-silico work).
- No BV-BRC GUI outputs; workflow used equivalent open tools (DIAMOND / Biopython / MAFFT / FastTree) rather than the BV-BRC web service.
- No RAST-SEED subsystem call for carbohydrate genes — used product-keyword net instead (narrower).
- No manual BLAST re-curation of T6SS candidates on ENHKU01 / EcWSU1 (paper did this by hand).
- No EDGAR BSR run for the exact core-count number — used DIAMOND RBH.

## Provenance & reproducibility one-liner

11 public NCBI-nuccore GenBank genomes → DIAMOND-RBH pan/core-genome + AAI/NJ phylogenomics + product-keyword functional calls → free-Argo `gpt-5.2` LLM judge → PARTIAL. All inputs free, all tools open-source, all compute on uicgpu (would run on a laptop).
