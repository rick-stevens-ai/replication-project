# Brief — BVBRC-50

**What:** Independent replication of Zhang/Pan et al. 2023 (*Microorganisms* 11:2961), the first complete genome + pan-genome analysis of *Shewanella oncorhynchi* Z-P2, a putrebactin-siderophore–producing bacterium (GenBank CP132914 / RefSeq GCF_030848765.1).

**Why:** BVBRC replication wave (TOPUP85 rank-30). Tests whether the paper's genome-stats, secondary-metabolite BGC content, pan-/core-genome numbers and closest-relative/ANI conclusions reproduce from free public data using independent tools (NCBI Datasets, Prokka, Roary, fastANI) rather than the paper's RAST/IPGA/PanOCT/kSNP pipeline.

**Result:** PARTIAL (strong). Genome size 5,034,612 bp and GC 45.4% exact; 109 tRNA / 31 rRNA exact; all 5 BGCs (incl. putrebactin NIS operon) verified at paper coordinates; pan-genome 9332 vs 9228 (+1.1%) and core 2656 vs 2681 (−0.9%) at comparable threshold; closest strain YZ08 confirmed with ANI 91.25% (paper 90.09%), all comparators <95%. No claim contradicted. LLM-judge (Argo gpt-5.2): PARTIAL, 2 STRONG + 3 MODERATE, coverage 5/7.
