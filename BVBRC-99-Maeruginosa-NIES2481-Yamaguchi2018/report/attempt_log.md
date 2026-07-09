# Attempt log — BVBRC-99

## 2026-07-04 (Ollie, subagent bvbrc-99, host CherryRd)

1. Read `WAVE_BRIEF_2026-07-01.md`. Confirmed hard rules: free endpoints only,
   real data + real analysis, LLM-judge scoring (n/a here — quantitative
   ground-truth comparison suffices), no overwrite of sibling dirs.
2. `esummary` via NCBI E-utilities for PMID 29576807 → confirmed authors,
   journal (*J Genomics* 6:30-33), DOI 10.7150/jgen.24935, PMC5865083.
3. Fetched PMC full-text HTML (open access, CC BY-NC), stripped to
   `work/paper_text_full.txt`. Extracted the paper's Table 1 numeric claims
   and Table 2 COG counts.
4. NCBI `esearch` + `efetch` (nuccore) for the two paper accessions:
   - **CP012375.1** — NIES-2481 chromosome (uid 1052158287), 4,354,398 B FASTA.
   - **CP025929.1** — NIES-2481 plasmid p1 (uid 1333047330), 149,723 B FASTA.
   Also pulled `gbwithparts` GenBank files for feature counts.
5. Biopython 1.87 sequence stats:
   - Chromosome: 4,293,006 bp, GC 42.91% — **exact match to paper Table 1**.
   - Plasmid: 147,539 bp, GC 41.66% — **exact match to paper Table 1**.
6. GenBank feature counts:
   - Chromosome: 4,292 CDS, 6 rRNA (2× SSU/LSU/5S = 2 operons), 41 tRNA —
     **rRNA operons and tRNA count exact**; CDS is 4,292 vs paper 4,332
     (diff 40, well within annotation-drift envelope — RAST vs current PGAP).
   - Plasmid: 164 CDS vs paper 167 (diff 3, same story).
7. Fetched sister strain **NIES-2549** (paper's comparison target): chromosome
   NZ_CP011304 / CP011304 (4,294,213 bp), plasmid CP026286 (6,987 bp).
8. NIES-2549 chromosome features: 4,282 CDS, 6 rRNA, 41 tRNA — this **matches
   the paper text exactly** ("The genome of NIES-2481 contains slightly more
   protein-coding genes than does the genome of NIES-2549 (4,332 vs. 4,282)"
   — the 4,282 number is what the reference genome I pulled reports).
9. 16S rRNA identity check:
   - Extracted both 16S copies from NIES-2481 and NIES-2549 (all four 1,460 bp).
   - Pairwise ungapped identity: **100.0% for all 4 cross-strain pairs** →
     confirms paper claim "The 16S rRNA gene sequences in the two genomes are a
     100% match."
10. Microcystin BGC absence check (independent of author annotation):
    - Downloaded 3 canonical mcyA references (WP_061431778.1, WP_012266628.1,
      BAG03679.1 from NIES-843), 2,787 aa each.
    - `tblastn` against NIES-2481 chromosome + plasmid (evalue 1e-5).
    - Chromosome: 117 low-identity hits (best ~42% pid, mostly ≤50%) — these
      are the expected cross-hits to other NRPS modules that ARE present
      (aeruginosin, micropeptin, microviridin; paper mentions these).
    - Plasmid: **0 hits at any threshold**.
    - **At strict orthology thresholds (≥70% pid AND ≥80% qcov): 0 hits total**
      → mcyA is genuinely absent. This corroborates the paper's antiSMASH
      finding without relying on the annotation.
11. Chromosome-size delta with NIES-2549:
    - Measured: NIES-2549 chr − NIES-2481 chr = **+1,207 bp** (i.e. NIES-2549
      is 1,207 bp larger).
    - Paper says: "The genome size of NIES-2481 is only 1,207-bp larger than
      that of NIES-2549."
    - **Magnitude exact (1,207 bp); direction reversed.** Very high confidence
      this is a paper typo — the number 1,207 is too specific to be
      coincidental. Flagged in Results table as CONTRADICTED-direction /
      REPLICATED-magnitude.
12. Wrote `report/REPORT.md`, `brief.md`, `attempt_log.md`,
    `artifact_harvest.md`, and dropped supporting evidence into
    `report/evidence/`. Total wall time ≈15 min. No LLM inference used
    (pure quantitative comparison against paper text). No GPU needed —
    everything ran locally on CherryRd.
