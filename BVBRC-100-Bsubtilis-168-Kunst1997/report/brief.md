# Brief — Kunst et al. 1997 (B. subtilis 168 complete genome)

**Paper:** Kunst F. *et al.* (1997) "The complete genome sequence of the Gram-positive bacterium *Bacillus subtilis*." *Nature* 390:249–256. doi:10.1038/36786.

**What:** Independent re-derivation of the paper's core descriptive/quantitative claims (genome size, G+C, CDS count, mean CDS length, coding density, start-codon usage, tRNA/rRNA loci, CDS base composition, replication/transcription co-orientation) from the current RefSeq reference `NC_000964.3` (the 2009 unified successor to the same 168-strain sequence, Barbe et al. 2009).

**Why:** BVBRC-100 replication wave — validate that the canonical B. subtilis 168 genome paper's quantitative body is honestly reproducible from free public data with local CPU only. The paper's original 1997 sequence has been superseded, but the underlying strain and all whole-genome fractions are directly re-derivable.

**Method (one line):** `curl` NC_000964.3 FASTA+GenBank from NCBI E-utilities (free, no auth) → Biopython in a local venv → recompute every metric → LLM-judge two independent Argo models (gpt-5, gpt-5.2) for the verdict.

**Result:** REPLICATED. Every whole-genome fractional metric agrees to ≤1 percentage point; 16S rRNA operons match exactly (10); the only discrepancies are annotation/curation drift (tRNA 86 vs 88; CDS 4,237 vs paper's "will fluctuate around 4,100") and a 796 bp (0.019%) genome-length correction, all explicitly foreseen by the paper or documented in the 2009 unified re-annotation.
