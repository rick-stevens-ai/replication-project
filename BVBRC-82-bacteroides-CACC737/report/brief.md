# Brief — BVBRC-82

**Paper:** Kim, Jung, Kim & Kim (2020). *Genome analysis of Bacteroides sp. CACC 737 isolated from feline for its potential application.* J Anim Sci Technol 62(6):952–955. PMID 33987575, PMC7721585, DOI 10.5187/jast.2020.62.6.952.

**What we tested:** All seven deposited GenBank accessions were downloaded and independently re-analyzed. Genome sizes, GC content, CDS/rRNA/tRNA counts, 16S rRNA identity to the *B. uniformis* type strain, presence of CRISPR/Cas features, and cross-plasmid backbone homology were computed from primary GenBank records. An LLM judge (argo:gpt-5) synthesized the per-claim verdict.

**Why:** The BV-BRC-adjacent workflow (PlasmidFinder via Similar Genome Finder + Genome Assembly) is directly checkable because Kim et al. deposited the complete circular chromosome and six plasmids in NCBI. Their numeric claims (size, GC, coding capacity, 16S divergence) are testable end-to-end without re-assembling from raw reads.

**Result:** Chromosome (4,470,359 bp / GC 45.96%), all six plasmids (20.4–40.4 kb, mean GC 40.95%), 13 rRNAs, and 16S identity of 97.83% to *B. uniformis* JCM 5828 reproduce paper claims within noise. CDS totals differ modestly (3,682 vs 3,938) — expected PGAP-vs-RAST annotation-pipeline artifact. Verdict: **REPLICATED**.
