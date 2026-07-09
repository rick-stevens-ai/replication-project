# Attempt Log — BVBRC-42 (chronological)

Analyst: Ollie (OpenClaw AI). Date: 2026-07-01 (night wave).

1. **Dedup.** `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "smithii|DSM4216|DSM 4216"` → no existing dir. Proceeded.
2. **Read brief + exemplar** (WAVE_BRIEF_2026-07-01.md, BVBRC-17 REPORT.md). Confirmed structure + free-endpoint discipline.
3. **Located paper** via Europe PMC search → PMC4995803, DOI 10.1186/s40793-016-0172-8 (SIGS 2016, OA CC BY 4.0). Fetched full-text JATS XML (123 KB) — NO paid pdf/image tools used.
4. **Parsed genome accession from full text:** chromosome CP012024.1 (3,368,778 bp) + plasmid CP012025.1 (12,514 bp), 3880 genes, RAST annotation. Extracted paper Tables 1–6 (classification, project info, genome summary, genome statistics, COG categories, Bacillus comparison).
5. **Found NCBI assembly** = GCF_001050115.1 / GCA_001050115.1 (ASM105011v1, BioProject PRJNA258357, BioSample SAMN03246763, locus BSM4216) — exact DSM 4216ᵀ type-strain genome of the paper. Downloaded both (RefSeq re-annotation + original GenBank submission) via NCBI Datasets v2 REST (free, no auth): genome/protein/gff3/cds.
6. **Genome statistics** (`genome_stats.py`, Biopython-free pure Python) from the actual FASTA + GFF:
   - Fixed a glob bug (was matching `cds_from_genomic.fna`); corrected to genome FASTA.
   - GCA: 3,381,292 bp total (EXACT vs paper), chr 3,368,778 + plasmid 12,514 (EXACT), GC 40.75% (paper 40.8%), 3,619 protein-coding (paper 3,627), tRNA 94, rRNA 33 (=11 operons ×3, EXACT to paper's "11 rRNA operons"), coding 81.4% (paper 82.8%).
7. **Functional gene present/absent scan** (`func_scan.py`) over the RefSeq GFF product names for the paper's Fig. 4 central-metabolism claims. Confirmed presence of Ldh, ilvBH, xylB, pdhABC, PGI, transketolase, PFK; confirmed ABSENCE of pta, ackA, pyruvate decarboxylase, PFOR by name.
8. **Rigorous tblastn confirmation** of the headline absent/present claims: fetched 8 curated reference enzymes from UniProt (Pta P39646, AckA P37877, PflB P09373, Pdc P06672, PFOR P94692, Ldh P13714, AlsS Q04789, PdhA P21881); `makeblastdb` on the B. smithii genome; `tblastn`. Positive controls PRESENT (Ldh 64.9%/e-134, PdhA 76%/e=0); headline claims ABSENT (Pta 26.4% e=0.62; AckA 24.4% e=2.3; PflB, Pdc, PFOR all sub-ortholog). Clean confirmation of "striking absence of standard acetate pathway."
9. **COG functional categories** (`COGclassifier` in local venv; auto-downloaded NCBI COG DB; rpsblast) on the real proteome vs paper Table 5. All-22-cat Pearson 0.615; excluding DB-era-unstable D/R/S → Pearson 0.912, Spearman 0.919.
10. **LLM-judge** (free Argo `argo:gpt-5.2` via localhost:44497, key=stevens): coverage 8/10, agreement 9/10, verdict PARTIAL.
11. Assembled report/ + evidence/ + work/. No sibling dirs touched. No paid endpoints used at any step.

## What worked
- NCBI Datasets REST gave the exact paper assembly instantly; genome stats reproduced to the byte.
- tblastn cleanly resolved the paper's headline pta/ackA absence with strong positive controls.
- COGclassifier ran offline-cached in 31 s.

## What was out of reach
- The RAST manual-curation pipeline, antiSMASH/CRISPR-finder, and the InterPro "domainome" rescue of borderline EC numbers (paper-specific workflows, not needed to test the claims).
- Full manual redraw of the Fig. 4 metabolic map.
