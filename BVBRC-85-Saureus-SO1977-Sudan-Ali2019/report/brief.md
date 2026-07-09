# Brief — BVBRC-85 · Ali et al. 2019 (MRSA SO-1977, Sudan)

**What:** Independent replication of Ali MS et al. 2019 (BMC Microbiology 19:126; PMID 31185900), which reported the first whole-genome sequence and comparative AMR/virulence analysis of a Sudanese clinical MRSA isolate (SO-1977).

**Why:** The paper is a single-isolate WGS descriptor — its checkable claims are (1) genome-assembly statistics, (2) predicted AMR gene inventory, (3) comparative AMR profile vs. MRSA252 & MSSA476, and (4) taxonomic placement via 16S rRNA. All the underlying data is public (NCBI GenBank WGS `NFZY00000000` → assembly `GCA_002224825.1`, BioProject `PRJNA385553`, 16S `MK713975`), and the analysis is re-doable end-to-end with `abricate + BLAST + pubMLST` on a laptop in minutes — an ideal replication target.

**Result (this replication, 2026-07-03):** **PARTIAL REPLICATION.** Every genome-statistic and the tetracycline-uniqueness core claim reproduce exactly; the paper's secondary claim that `norA` is unique to SO-1977 is **CONTRADICTED** — `norA` is present in both comparator genomes at the same identity, indicating a comparator-annotation artifact in the original analysis. New evidence: independent MLST call = **ST140** (not reported by the authors).
