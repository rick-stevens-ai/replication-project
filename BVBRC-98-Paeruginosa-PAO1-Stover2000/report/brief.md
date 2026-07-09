# Brief — Stover et al. 2000 PAO1 Genome

**What:** Independent replication of the descriptive/quantitative claims of the
landmark PAO1 reference-genome paper (Stover et al., *Nature* 406:959-964, 2000)
by re-computing genome size, G+C content, and predicted-ORF count directly from
the current RefSeq assembly GCF_000006765.1 (NC_002516.2, ASM676v1) using
Python on local CPU.

**Why:** BVBRC-100 wave — a foundational reference-genome paper that anchors
downstream *P. aeruginosa* work; verifies that the canonical NC_002516.2
record on file today still matches the numbers the original team published,
and confirms the analytic pipeline (FASTA/GFF parse + base composition) can
be trivially reproduced with free tooling.
