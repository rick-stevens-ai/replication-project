# Attempt Log — BVBRC-61 (Heo et al. 2021, B. siamensis B28)

Analyst: Ollie (OpenClaw subagent). Date: 2026-07-02. Host: CherryRd (local).

1. Read WAVE_BRIEF_2026-07-01.md + BVBRC-17 exemplar REPORT.md for structure/verdict vocabulary.
2. Candidate selection: scanned BVBRC_TOPUP85 ranks 51-88 (real column layout: rank/score/year/cites/organism/workflow/title/...). The "50/17" I first saw was the *score* column, not organism. Went down from rank 50. Rank 50 = *Bacillus siamensis* B28 kimchi (PMID 34441683). Dedup vs existing BVBRC-01..60: no siamensis/B28; existing bacillus dirs are Parageobacillus (23), Paenibacillus (45), B. megaterium (60) — no overlap. Not a tool/DB paper. PICKED rank 50.
3. Confirmed OA: Europe PMC core query → PMC8394110, CC BY, hasSuppl, GCA accession tag. Created target dir BVBRC-61-Bsiamensis-B28-kimchi-Heo2021 (next free after BVBRC-60).
4. Pulled full-text XML from Europe PMC (free OA, not paid pdf tool) → work/paper_fulltext.xml. Extracted claims + methods + genome accessions.
   - B28 genome deposited GenBank CP066219–CP066221 (chromosome + 2 plasmids).
   - Comparator accessions listed in Methods (SCSIO 05746 GCA_002850535.1, KCTC 13613T GCA_000262045.1, etc).
5. Resolved B28 assembly accession via eutils elink nuccore(CP066219)->assembly = GCF_016313165.1 / GCA_016313165.1.
6. Downloaded B28 + 6 comparators with `datasets` CLI v18.25.1. Unzipped, extracted FASTAs.
7. genome_stats.py → B28 chromosome 3,946,178 bp + plasmids 6,117 & 5,433 bp, GC 45.85% — EXACT match to paper. KCTC 13613T = 51 contigs (paper: incomplete ✓); SCSIO 05746 = 2 contigs (complete ✓).
8. Pulled B28 RefSeq annotation (protein.faa 3808, genomic.gff, cds). tRNA=86, rRNA=27 from GFF — EXACT match to paper.
9. ANI: fastANI + skani, B28 vs all refs. KCTC 13613T 98.42/98.54% (paper 98.61); SCSIO 05746 97.55/97.67% (paper 97.73); outgroups ~94% (<species boundary). Reclassification to B. siamensis reproduced.
10. Safety AMR: AMRFinderPlus 4.2.7 (DB 2026-03-24.1) protein+nucleotide+GFF(pgap). 5 hits, ALL scope=core (intrinsic): satA, fosM, 2 beta-lactamases, Tet(L/K/45). Cross-check RGI/CARD 3.2.7: 9 Strict / 0 Perfect (van homolog fragments, qacG/J, FosBx1, tet(45), BcI). Both tools => NO acquired/mobile AMR; intrinsic Bacillus background only. Consistent with paper's phenotypic susceptibility + Table 2 efflux caveat.
    - Gotcha: amrfinder `-a` = annotation_format (needs `pgap`), NOT organism. mlst & rgi subprocesses need env bin on PATH (any2fasta / diamond).
11. Functional/probiotic gene survey (func_survey.py on 3808 proteins) + targeted greps: enterotoxins ABSENT (✓safety); hlyIII "hemolysin family protein" PRESENT (✓); BSH, GABA genes, GGT, subtilisin AprX, sporulation(128)/Spo0A, biofilm/EPS(BslA,EpsG,poly-γ-glutamate), flagella(41), fibronectin, bacteriocin/lantibiotic(surfactin,Blp,circular), ROS(catalase/SOD/GPx/AhpC), LTA, alpha-galactosidase MelA, TAG lipase — all PRESENT. Only the paper's specific "bacitracin operon" NAME not confirmed in RefSeq annotation (bacteriocin biosynthesis broadly confirmed).
12. MLST 2.33.1 (pubMLST bsubtilis scheme): B28 novel allelic profile, no exact ST, distinct from KCTC 13613T (ST101) — consistent with paper's finding B28 is a distinct B. siamensis strain. (Paper used a custom 8-gene Bacillus MLST not in pubMLST; methodological difference noted.)
13. LLM-judge (free Argo gpt-5.2, temp 0): verdict PARTIAL; C1 YES, C2/C3/C4 PARTIAL (docked C2 for annotation counts [since closed: tRNA/rRNA exact], C3/C4 for un-reproducible wet-lab phenotypes/PCR & specific bacteriocin naming).
14. Final verdict: PARTIAL (strong) — see REPORT.md §Verdict.

## What worked / failed
- WORKED: exact chromosome+plasmid sizes, GC, tRNA/rRNA; ANI reclassification; dual-tool AMR agreement; broad functional gene confirmation. All from free public data.
- OUT OF REACH (genome-only): wet-lab PCR of enterotoxins, disc-diffusion antibiotic phenotypes, beta-hemolysis assay, antibacterial-activity assay against pathogens (Figure 2) — these are experimental, cannot be re-run from sequence; assessed via genotype proxy only.
- MINOR: paper's exact "bacitracin/mesentericin operon" naming not reproduced by RefSeq annotation vocabulary; MLST scheme differs from paper's custom scheme.
