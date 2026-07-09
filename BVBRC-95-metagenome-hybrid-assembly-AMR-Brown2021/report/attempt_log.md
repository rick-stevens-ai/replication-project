# BVBRC-95 attempt log
2026-07-04T21:09:28Z

## Step 1: Fetch paper metadata

## Step 2: Data availability confirmed
ENA filereport for PRJNA527877: 123 SRA runs found. Total 153 Gbp. Split: 63 Illumina, 60 Oxford Nanopore. 33 raw Illumina + 24 raw Nanopore + 66 pre-computed assemblies (7 assemblers × 10 samples with some gaps).

## Step 3: Scope decision
Full de-novo re-assembly of all 10 metagenomes across 7 assemblers = infeasible in job window (each assembly = hours; 70 = days). Decision: use author's pre-computed assemblies (available as fastq.gz on ENA, each contig stored as a "read"), pick 1 representative sample (USA-1-influent) covering all 7 assemblers, and re-annotate ARGs with a completely independent tool (AMRFinder+ vs paper's Diamond+CARD).

## Step 4: Data pull
Downloaded 7 assembly SRAs from ENA in parallel (~8 sec, ~275 MB total after decompression):
- SRR12664619 Megahit (16 MB, 98k contigs, N50=469)
- SRR13105837 metaSpades (85 MB, 649k contigs, N50=372)
- SRR12664620 IDBA-UD (44 MB, 174k contigs, N50=907)
- SRR12664586 HybridSpades (86 MB, 597k contigs, N50=430, max=116kb)
- SRR12664608 Canu (4 MB, 2125 contigs, N50=19298)
- SRR12664575 Flye (9 MB, 971 contigs, N50=45101, max=363kb)
- SRR12664597 OPERA-MS (18 MB, 86k contigs, N50=544, max=311kb)

Fastq→fasta conversion via awk. Path scheme lesson: ENA subdirs use last 3 digits mod 1000 (padded 3 digits) — resolved via ENA REST filereport rather than trying to compute path.

## Step 5: AMRFinder attempts
First try: run on unfiltered assemblies. metaSpades (649k contigs) triggered blastx mode — after 30+ min still running. Killed. Restarted after filtering to contigs ≥1kb per assembler (paper's own ARG focus is on long contigs). Result: 7 AMRFinder runs completed in ~3 min total. Tool DB path required explicit `-d` flag because conda env not properly registered.

## Step 6: Analysis
Computed per-assembler ARG counts, unique symbols, ARG-carrying contig lengths, pairwise Jaccard of ARG symbol sets, and per-category (short/long/hybrid) mean pairwise Jaccard.

## Step 7: LLM-judge
argo:claude-opus-4.7 upstream proxy returned 502 parse error; switched to argo:gpt-5.2 which worked. Judge output saved to `evidence/llm_judge.json`. Per-claim verdict: C1/C2/C5=REPRODUCED, C3=PARTIAL, C4=NOT-TESTED. Overall: PARTIAL, confidence 0.78.
