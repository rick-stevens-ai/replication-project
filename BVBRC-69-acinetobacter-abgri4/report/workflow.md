# Workflow — BVBRC-69: Chan et al. 2020 AbGRI4 replication

**Host:** uicgpu  •  **Working dir:** `/data/stevens/bvbrc69-abgri4/`  •  **Env:** conda `bvbrc14`
**Analyst:** Ollie (OpenClaw AI subagent)  •  **Date:** 2026-07-03

## 0. Inputs

- **Paper:** Chan et al. 2020, *J. Antimicrob. Chemother.* 75(10):2760–2768 (DOI [10.1093/jac/dkaa266](https://doi.org/10.1093/jac/dkaa266); PMID 32681170; PMCID PMC7556812). OA via PMC.
- **NCBI deposits under test:** CP035043–CP035053 (11 replicons across 4 isolates ABUH763/773/793/796).
- **External comparators:** CP001182.2 (AB0057), CP000521.1 (ATCC 17978).
- **Tools:** EDirect 24.0 (`efetch`), Biopython 1.87, `mlst` 2.33.1 (schemes `abaumannii_2` Pasteur, `abaumannii` Oxford), `abricate` 1.4.0 with ResFinder / CARD / NCBI AMRFinderPlus / PlasmidFinder, NCBI BLAST+ v2.16.0.

All tools are free/open-source; no paid endpoints, no proprietary databases, no reference genomes beyond public NCBI.

## 1. Pipeline (numbered steps)

### Step 1 — Retrieve genomes
- Script: `work/download_genomes.sh`
- Action: `efetch` FASTA + GBK for CP035043–CP035053 (paper) and CP001182.2, CP000521.1 (comparators).
- Output: `work/genomes/*.fna`, `work/genomes/*.gbk`
- Free/no key: ✅

### Step 2 — Basic genome stats
- Script: `work/genome_stats.py` (Biopython)
- Action: per-replicon length and GC%; aggregate per isolate.
- Output: `report/evidence/genome_stats.json`
- Cross-check target: paper Table 1 sizes.

### Step 3 — MLST typing
- Script: `work/run_mlst.sh`
- Action: `mlst --scheme abaumannii_2 <chrom.fna>` (Pasteur) and `mlst --scheme abaumannii <chrom.fna>` (Oxford).
- Output: `report/evidence/mlst/*.tsv`
- Cross-check target: paper's declared ST2 (Pasteur) and ST281 (Oxford).

### Step 4 — AbGRI4 region extraction
- Script: `work/extract_abgri4.py` (Biopython)
- Action: slice the paper's Table-1 AbGRI4 coordinates from each positive chromosome (reverse-complement for ABUH793 as its coordinates run reverse).
- Output: `report/evidence/abgri4/ABUH{763,793,796}_AbGRI4.fna` (each expected exactly 8,840 bp)

### Step 5 — AMR annotation of the island
- Script: `work/annotate_abgri4.sh`
- Action: `abricate --db resfinder|card|ncbi|plasmidfinder --minid 90 --mincov 80` on each region FASTA and on whole genomes.
- Output: `report/evidence/abgri4/amr/*.tsv`, `report/evidence/wg_amr/*.tsv`
- Cross-check target: aadB, aadA2, sul1 all present; plus qacEΔ1 and intI1 as class-1 3'-CS markers.

### Step 6 — Island-identity (pairwise Hamming)
- Script: `work/final_evidence.sh` (Biopython)
- Action: pairwise compare the three 8,840-bp regions after orientation matching.
- Output: distance matrix printed inline and captured in `report/evidence/abgri4/hamming.txt`.
- Cross-check target: paper implies the 3 islands are essentially identical.

### Step 7 — IS26 flank verification + target-site locus tags
- Script: `work/final_evidence.sh`
- Action: walk GBK features within each AbGRI4 span; count IS26 CDS (`IS6-like element IS26 family transposase`); confirm one at each flank. Direct locus-tag lookup for `EP550_07220` and `EP550_07290` in the CP035043 GBK.
- Output: inline capture; positions listed in REPORT.md Section 4.6/4.7.

### Step 8 — Comparative BLAST (novelty check)
- Script: `work/final_evidence.sh`
- Action:
  - Build blastdb from AB0057 and ATCC 17978 chromosome FASTAs.
  - `blastn -evalue 1e-30 -perc_identity 90` of EP550_07220 (375 bp) and EP550_07290 (309 bp) against each.
  - `blastn` of the full 8,840-bp AbGRI4 region against AB0057.
  - `efetch -seq_start/-seq_stop` a 20-kb window around the AB0057 azoreductase hit; enumerate neighboring CDS.
- Output: `report/evidence/blast/*.tsv` and text notes on the AB0057 20-kb window.
- Cross-check target: 3' azoreductase flank hits both comparators; 5' α/β-hydrolase flank does NOT — this is the paper's novel-target claim.

## 2. Repeatability

- All scripts are checked in under `work/` and are pure bash + Python.
- All inputs are public NCBI accessions.
- All tool versions are pinned in `report/evidence/tool_versions.txt` (mlst 2.33.1, abricate 1.4.0, BLAST+ 2.16.0, Biopython 1.87, EDirect 24.0).
- Runtime: whole pipeline finishes in <30 minutes on uicgpu; no GPU required.

## 3. Provenance chain

Paper → CP035043–CP035053 (deposited by the authors) → `efetch` → conda-env bacterial-genomics toolchain → `report/evidence/*` → REPORT.md → REPORT.tex. No hidden data, no re-assembly (accepted deposited sequences as given), no proprietary databases.

## 4. Verdict routing

- REPORT.md and REPORT.tex both conclude **REPLICATED** (11/11 testable claims reproduced or partial-consistent; 1 methods claim out of scope).
- Open items and honest limits are recorded in `open_questions.json` and in the **GENUINE CRITIQUE** section of REPORT.tex.
