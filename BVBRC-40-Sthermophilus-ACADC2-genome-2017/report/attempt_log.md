# Attempt Log — BVBRC-40 (2026-07-01)

1. **Dedup check** — `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "thermophilus|ACA-DC|streptococcus"` → NO_DUP_FOUND. Proceeded.
2. **Read brief + exemplar** — WAVE_BRIEF_2026-07-01.md and BVBRC-17 REPORT.md for structure.
3. **Located paper** — Europe PMC search. First generic search surfaced a 2025 QS paper; refined query `"Streptococcus thermophilus" "ACA-DC 2" genome sequence` → hit PMID 28163827 / PMC5282782 / DOI 10.1186/s40793-017-0227-5 (Stand Genomic Sci 12:18, 2017). Correct paper.
4. **Pulled OA full text** — `PMC5282782/fullTextXML` (107 KB), cleaned to text. Extracted accessions: ENA **LT604076**, BioProject **PRJEB14916**. Extracted Table 3 genome statistics verbatim.
5. **Resolved assembly** — NCBI Datasets `genome/bioproject/PRJEB14916/dataset_report` → GCA_900094135.1 + GCF_900094135.1 (ASM90009413v1).
6. **Downloaded genomes** — NCBI Datasets REST, both GCA (author) and GCF (RefSeq), with GENOME_FASTA + PROT_FASTA + GFF + CDS_FASTA. Free, no auth.
7. **Recomputed stats** — `genome_stats.py` (stdlib): size, GC, contigs, CDS, tRNA, rRNA, pseudogenes, gene biotypes. GCA reproduces paper Table 3 to the digit (1,731,838 bp; 39.21% GC; 1,556 CDS; 56 tRNA; 14 rRNA; 224 pseudo; 1,850 total).
8. **De-novo re-annotation** — copied GCA fna to uicgpu (bvbrc28 env, Prokka 1.12). Env activation needed full path `/data/stevens/envs/bvbrc28` (short name resolved to wrong prefix). Prokka: CDS 1,818, tRNA 56 (exact), rRNA 15, tmRNA 1. Function 653/1818 (35.9%).
9. **CRISPR** — minced default (minNR=3) → 0 arrays (single-spacer arrays = 2 repeats, below default; corroborates paper's "one spacer each"). minNR=2 → 6 candidates; one at ~849.6 kb coincides with paper's cas-flanked CRISPR near locus STACADC2_0849. CRISPR presence confirmed.
10. **LLM-judge** — free Argo argo:gpt-5.2. Verdict PARTIAL, Coverage 10/10, Agreement 7/10. Output in `work/judge_output.txt`.
11. **Wrote report/** — REPORT.md, brief.md, artifact_harvest.md, this log, evidence/.

## What worked
- Europe PMC XML gave clean full text + accessions with zero paid calls.
- NCBI Datasets resolved BioProject→assembly and delivered genome+annotation in one call.
- GCA author assembly matched Table 3 exactly (public-record fidelity confirmed).
- Prokka tRNA count = exact match; PGAP re-annotation within variance.

## What was partial / limited
- Function-assignment % not reproducible with default Prokka (paper used RAST+WebMGA+EggNOG+Pfam+manual). Expected.
- Exact CRISPR count is tool/threshold-dependent (CRISPRFinder curated 2 vs minced-nr2 6 candidates); qualitative claim reproduced.
- Did not run the actual BV-BRC Comprehensive Genome Analysis (RASTtk) web service; used Prokka as the free local RASTtk-analog.
