# Brief — Blattner et al. 1997 (E. coli K-12 MG1655 complete genome)

**Paper:** Blattner F. R., Plunkett G. III, Bloch C. A., *et al.* (1997) "The complete genome sequence of *Escherichia coli* K-12." *Science* **277**(5331):1453–1462. doi:10.1126/science.277.5331.1453.

**What:** Independent re-derivation of the paper's core descriptive / quantitative claims (genome size, G+C, CDS count, mean CDS length, coding density, tRNA and rRNA-operon counts, replication co-orientation) from the current RefSeq reference `NC_000913.3` — the curation-updated successor to Blattner's 1997 sequence for the same MG1655 strain.

**Why:** BVBRC-100 replication wave — validate that the canonical *E. coli* K-12 MG1655 genome paper (foundational reference for essentially all modern *E. coli* systems biology) is honestly reproducible from free public data with local CPU only.

**Method (one line):** `curl` NC_000913.3 FASTA + GenBank from NCBI E-utilities (free, no auth) → Biopython in a local venv → recompute every metric with interval-union coding density and standard replichore assignments → LLM-judge two independent Argo models (gpt-5, gpt-5.2) for the verdict.

**Result:** REPLICATED. Every whole-genome quantitative claim agrees to ≤1.7 percentage points, all operon-level counts are exact (7 rRNA operons, 86 tRNAs), and the strand-bias figure matches at 54.9% vs paper "~55%". The only discrepancies are (a) +2,431 bp (0.052%) of genome-length correction and (b) +30 CDS (+0.7%) annotation drift, both expected after 28 years of continued curation of the same strain.
