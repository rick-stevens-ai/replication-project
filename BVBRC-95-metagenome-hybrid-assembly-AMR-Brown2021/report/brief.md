# BVBRC-95 — Independent replication of Brown et al. 2021 (Sci Rep)

**What:** Re-ran ARG detection (NCBI AMRFinder+ v3.12.8, 2024-07-22 DB) on all 7 author-deposited assemblies (Megahit, metaSpades, IDBA-UD, HybridSpades, Canu, Flye, OPERA-MS) of the USA-1-influent wastewater metagenome from BioProject PRJNA527877, then compared ARG symbol overlaps across assembler categories.

**Why:** Paper claims (a) short-read and hybrid assemblies give SIMILAR ARG contextualization patterns; (b) long-read alone gives DISTINCT patterns; (c) long-read alone recovers far fewer ARGs due to Nanopore error rate. Verify these with an independent, stricter ARG caller.

**Result:** All three central claims (C1, C2, C5) REPRODUCED. Short-vs-hybrid Jaccard = 0.610 (highest cross-category), short-vs-long = 0.095, hybrid-vs-long = 0.099. Canu recovered 1 ARG, Flye 13, vs 31–79 for short/hybrid. C3 (hybrid → longer ARG contigs) PARTIAL. C4 (chimerism spike-in) NOT-TESTED. Verdict: **PARTIAL** with high confidence (LLM-judge 0.78, argo:gpt-5.2).
