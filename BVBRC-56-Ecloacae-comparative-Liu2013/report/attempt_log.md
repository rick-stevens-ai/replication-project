# Attempt Log — BVBRC-56 (Enterobacter cloacae comparative genomics, Liu 2013)

**Analyst:** Ollie (OpenClaw AI subagent) — BVBRC Replication Wave, 2026-07-02.

## Chronology
1. Read WAVE_BRIEF_2026-07-01.md + exemplar BVBRC-17 REPORT.md.
2. Candidate selection from BVBRC_TOPUP85_2026-06-26.tsv ranks 41+. Deduped against existing BVBRC-01..55:
   - rank 41 (archive-wide diversity / BIGSI-type tool): skipped — no genome-replication workflow fit.
   - **rank 42: Enterobacter cloacae comparative genome analysis (2013, 89 cites)** — SELECTED. Enterobacter is entirely absent from the existing set (grep confirmed 0 hits). Highest-ranked genuinely-new study with clear public genome data.
3. Resolved exact paper via Europe PMC TITLE+PUB_YEAR query → PMC3771936 (Liu WY et al., PLoS One 2013;8(9):e74487, CC BY).
4. Created target dir BVBRC-56-Ecloacae-comparative-Liu2013/ (next free number; verified BVBRC-5* stops at 55).
5. Fetched full text XML from Europe PMC (NOT the paid pdf tool). Extracted Materials & Methods + Results → all 11 GenBank accessions + Table 1 numbers + comparative claims.
6. uicgpu recon: brief's `bvbrc14/bvbrc28` conda envs do NOT exist on uicgpu (only gcc12/marlamr/pelec/fempinn). No bioinformatics tools preinstalled. Created a fresh conda env `bvbrc56` (bioconda: diamond, blast, mafft, fasttree, ncbi-datasets-cli, biopython).
7. Downloaded all 11 genomes (.fna + .gbk) via NCBI efetch by accession to /data/stevens/bvbrc56/genomes. Verified sizes.
8. genome_stats.py — parsed GenBank → replicated Table 1 (size/replicons/GC/CDS/tRNA/rRNA). Extracted proteomes for ortholog work.
9. pangenome.py — DIAMOND all-vs-all blastp on the 4 E.cloacae proteomes → reciprocal-best-hit ortholog single-linkage clusters → core=3345, pan=6642, per-strain unique %.
10. functional.py + t6ss_refine.py + t6ss_ge6.py — annotation-keyword feature counts (fimbriae, T6SS clusters, carbohydrate genes). Iterated T6SS clustering thresholds.
11. phylo_lite.py — proteome-wide reciprocal-best-hit AAI (55 pairs) across 8 Enterobacter + 3 Pantoea → NJ tree (Biopython). Confirmed Pantoea outgroup + E.cloacae cluster.
12. LLM judge (free Argo gpt-5.2) scored the full claim table → verdict PARTIAL.

## What worked
- Genome stats replicate near-exactly (CDS counts EXACT for all 4; sizes/plasmids/GC essentially identical). rRNA 25 genes = 8 operons matches paper.
- Pan/core structure directionally reproduced (core 3345 vs 3540; unique-CDS ordering 7.8/7.1/13.3/19.8 vs paper 6/6/12/20 — the ATCC13047=20%/EcWSU1=12% plasticity ordering is the headline and it holds).
- Phylogenomics: clean Pantoea outgroup, tight E.cloacae clade — matches Fig 1 structure via an independent (AAI/NJ) method.
- T6SS: ATCC13047=2 and SDM=1 matched exactly.

## What was partial / failed
- Core count 5.5% low (EDGAR BSR vs DIAMOND RBH methodology difference).
- "ENHKU01 closest to ATCC13047" (4-housekeeping-gene claim) not confirmed by whole-proteome AAI — all 3 other E.cloacae essentially tied; not a contradiction, coarser vs finer signal.
- Carbohydrate gene count (~430, 8-10%) below paper's >640 (13-15%) — my keyword net is narrower than RAST SEED subsystem assignment; method-limited, not a data disagreement.
- Fimbriae/T6SS on ENHKU01 & EcWSU1 undercounted — paper used manual IMG/BLAST curation ("Two T6SSs of ENHKU01 were manually identified"); RefSeq product annotation is sparse for those, exactly as the paper implies.

## Compute
All heavy work on uicgpu (uicgpu01) in conda env bvbrc56. Local machine used only for orchestration + report writing. Free endpoints only (Argo gpt-5.2 for judge).
