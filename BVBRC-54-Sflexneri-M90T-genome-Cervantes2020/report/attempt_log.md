# Attempt Log — BVBRC-54 (S. flexneri 5a M90T)

Analyst: Ollie (OpenClaw AI) · Wave 2026-07-02 · target dir BVBRC-54-Sflexneri-M90T-genome-Cervantes2020

1. Read WAVE_BRIEF_2026-07-01.md + BVBRC-17 exemplar REPORT.md for structure/verdict vocabulary.
2. Candidate selection: read ranks 37–63 of BVBRC_TOPUP85_2026-06-26.tsv; deduped against the 53
   existing BVBRC-* dirs (organism+topic). rank34/35 pre-noted as dupes. rank36 = S. aureus (topic
   overlaps existing BVBRC-03/32). **rank37 = Shigella flexneri M90T** — Shigella is entirely absent
   from the existing 53 → genuinely new organism. PICKED.
3. Europe PMC core query on PMID 32252626: confirmed OA (CC BY), PMC7132871, hasData=Y, EMBL xrefs.
   Pulled abstract + full text XML. Extracted testable claims + exact numbers (chr 4,596,714 bp;
   plasmid 232,195 bp; 6723 pTSS / 7328 sTSS; Canu 1.7; PacBio ~157x).
4. Located the deposited genome: NCBI assembly search → **GCF_004799585.1 (ASM479958v1), Umeå
   University, 2019-04-18, Complete Genome**. Confirmed contig_n50 = 4,596,714 (== paper chromosome)
   and total − chromosome = 232,195 (== paper plasmid). Replicons CP037923 / CP037924.
5. Downloaded genome (FASTA+GFF+protein+seq report) via NCBI Datasets REST (free, no auth) locally.
   Independent FASTA parse: 2 replicons, exact lengths, GC 50.92% / 45.68%.
6. Parsed paper Table 1/2/3 from the XML → chromosome (Genes 4049, CDS 4629, tRNA 102, rRNA 22, IS
   296, pseudo 640) / plasmid (Genes 307, CDS 320, IS 106, pseudo 129) / 402 total IS.
7. Heavy analysis on **uicgpu** (CherryRd under memory pressure). Copied FASTA over. Confirmed tool
   envs: bvbrc28 (prokka 1.12, datasets), bvbrc14 (abricate 1.4.0, amrfinder 4.2.7, mlst 2.33.1).
8. Ran: MLST → ST631 (Achtman). abricate vs vfdb/victors/ecoli_vf/card/resfinder/ncbi/plasmidfinder.
   AMRFinderPlus (--organism Escherichia --plus). Prokka de-novo re-annotation.
9. Results: T3SS (mxi/spa), ipa invasins, ipg chaperones, osp+ipaH effectors, virF/virB, icsA/icsP
   ALL on plasmid NZ_CP037924.1; aerobactin iucABCD/iutA (SHI-2) on chromosome — matches paper
   biology. PlasmidFinder = IncFII on pWR100. AMR = only intrinsic blaEC + emrE efflux (no acquired
   R — consistent with a lab reference strain). Prokka totals within a few % of paper; tRNA/rRNA match.
10. Pulled all outputs back to report/evidence/. Wrote comparison + virulence summary evidence files.
11. LLM-judge (Argo, free) scored claims → verdict.

## What worked
- Base-pair-exact replicon reproduction (both chromosome and plasmid) — strongest possible data check.
- Full independent biological reconstruction of the Shigella T3SS/virulence-plasmid story.

## What was out of reach
- dRNA-seq TSS re-count (6723/7328): raw TEX+/− RNA-seq reads not fetched; requires the SRA dRNA-seq
  libraries + a TSS caller (e.g. ReadXplorer/TSSAR). Data availability verified; count not regenerated.
- IS-element full ISfinder typing (paper's 402) not re-run; corroborated indirectly by pseudogene load.
- Exact CDS/pseudogene totals differ by a few % (independent annotation pipelines — expected).
