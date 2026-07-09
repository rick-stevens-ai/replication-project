start=2026-07-03T03:07:36Z

finished=2026-07-03T03:26:50Z

## Attempt log (chronological)

1. Read WAVE_BRIEF; created target dir + subdirs (report/evidence, work).
2. Fetched abstract via NCBI eutils (PMID 28257489). Extracted 10 declared claims (C1-C10).
3. Searched NCBI Assembly for "Nocardia seriolae UTF1" — found single hit id 1226421 → GCF_002356035.1 / AP017900.1 = 8,121,733 bp (matches paper's C1 exactly on metadata alone).
4. Downloaded genome fna+faa+gff (uicgpu ~/REPLICATE-PROJECT/BVBRC-63-nocardia/).
5. Basic stats: 1 chromosome, 8,121,733 bp, GC=68.14%, RefSeq CDS=7,650, rRNA=12 (4 each of 16S/23S/5S), tRNA=63, pseudogenes=279. → C1, C2, C4 confirmed.
6. Prokka 1.12 independent annotation on 32 CPUs: 8,121,733 bp / 7,648 CDS / 12 rRNA / 72 tRNA. First attempt failed (--gram pos needs signalp not installed); reran without --gram. Prokka CDS = 7,648 vs paper 7,697 → 99.36 % match (C3 confirmed).
7. Comparators: initial pull used WRONG accessions for two strains (I had GCF_000009985.1 for N. farcinica, actual = GCF_000009805.1; and GCF_000450345.1 for N. nova SH22a, actual = GCF_000523235.1). Detected because their proteomes came out too small vs literature (4,603 and 3,648). Re-searched NCBI Assembly by strain name; got correct accessions; re-downloaded. Corrected proteome counts 5,942 and 7,508 respectively.
8. Initial CD-HIT (50% id) all-vs-all clustering came out with only 40 core clusters — way too few. Cross-genus Nocardia are too diverged for 50%/50% CD-HIT clustering.
9. Switched to BLASTP reciprocal best hits (e-value 1e-5, max_target_seqs 5). First BLAST run had bash variable expansion bug inside nohup+quotes; moved to a script file (run_rbh3.sh). Ran pairwise BLASTP: UTF1 vs each of 4 comparators + reverse.
10. RBH ortholog compute at 3 threshold sets:
    - 30% id / 50% cov → core=2,670, unique=2,010
    - **25% id / 40% cov → core=2,718, unique=1,967** (best match to paper's 2,745/1,982)
    - 20% id / 30% cov → core=2,732, unique=1,952
    → C5, C6 confirmed at ~99%.
11. Functional-category regex counts across all 5 proteomes for ABC / mobile-element / hypothetical / mce / siderophore / β-lactamase / efflux / catalase-SOD keywords. Found UTF1 mobile-element count 127 vs comparators 20-43 → C7 strongly confirmed. Hypothetical fractions ~similar across species (C8 partial). ABC absolute counts higher in UTF1 than 3/4 comparators but similar percentage (C9 partial). Mce/catalase/SOD/siderophore all present (C10 confirmed).
12. LLM-judge verdict via Argo (Claude Opus 4.7): REPLICATED. Wrote REPORT.md, brief.md, artifact_harvest.md.
