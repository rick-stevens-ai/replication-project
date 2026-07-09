# BVBRC-112 — Minicystis rosea DSM 24000ᵀ complete genome & PUFA (Pal et al., BMC Genomics 2021)

**Paper:** Pal S, Sharma G, Subramanian S. *Complete genome sequence and identification of polyunsaturated fatty acid biosynthesis genes of the myxobacterium Minicystis rosea DSM 24000ᵀ.* BMC Genomics 22:655 (2021). DOI 10.1186/s12864-021-07955-x, PMID 34511070, PMC8436480.

**What / why:** Independently reproduce the paper's genome-annotation and biosynthetic-gene-cluster (BGC) claims for the 16.04-Mbp *Minicystis rosea* DSM 24000ᵀ genome (NCBI CP016211.1, BioProject PRJNA321464), including (a) assembly-level Table 1 statistics (length, GC, CDS, tRNA, strand distribution), (b) the antiSMASH count of 47 BGCs comprising ~7.7 % of coding genes, and (c) the four-gene *pfa* PUFA cluster at locus tags A7982_11504–11506 (+ separate *pfaE*).

**Verdict:** **REPLICATED** — all quantitative claims tested (7/7) reproduce within annotation-tool tolerance; antiSMASH 6.1.1 rerun on the public GenBank record yields exactly 47 BGC regions with the *pfa*/PUFA cluster correctly identified as an hglE-KS + T1PKS region (#42) centred on the paper's pfa1–pfa3 locus tags.
