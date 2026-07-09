# Artifact harvest — Kunst1997 replication

All artifacts pulled from free, no-auth public endpoints.

| # | Artifact | Source URL | Accession | Bytes | SHA-256 |
|---|---|---|---|---|---|
| 1 | Paper landing/main text (readable HTML) | https://www.nature.com/articles/36786 | doi:10.1038/36786 | (fetched, not cached) | — |
| 2 | B. subtilis 168 chromosome, FASTA | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000964.3&rettype=fasta&retmode=text | RefSeq NC_000964.3 | 4,275,902 | `a334e891ffc0e307f23f48842775d3383177a9d9cb5d5075b552a2cccddfe139` |
| 3 | B. subtilis 168 chromosome, GenBank-with-parts | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000964.3&rettype=gbwithparts&retmode=text | RefSeq NC_000964.3 | 13,415,984 | `ab0ea7ab52d59e3212fca7677b9e0c0df8c0ae2aa0efe659a9d0c7cd9bfd5d94` |

Both files are stored under `work/data/`.

## Provenance note on the reference sequence

The paper describes the 1997-vintage sequence of B. subtilis 168 (deposited then as AL009126.1 / L*-series contigs; length 4,214,810 bp). The current RefSeq NC_000964.3 is the **2009 unified reference** for the same strain (Barbe V. et al., "From a consortium sequence to a unified sequence: the *Bacillus subtilis* 168 reference genome a decade later," *Microbiology* 155:1758–1775, 2009), which is 4,215,606 bp (paper + 796 bp of error corrections). The current annotation is the 2018 curated version (Borriss/Danchin et al. 2018, *Microb Biotechnol* 11:3–17). Using this successor is the honest choice for reproducibility because (a) it is the canonical present-day reference for the strain, (b) whole-genome fractional metrics (GC%, coding density, start-codon fractions, CDS base composition, co-orientation) are essentially invariant under a 0.019% length correction, and (c) it lets us also validate that the paper's claims survived 20+ years of curation.

## Compute footprint

- Total: <20 MB downloaded, <30 s compute on a single CPU core (Biopython on a 4.2 Mb genome).
- No GPU used, no HPC used, no paid endpoint used.
- LLM judges: 2 Argo calls (`argo:gpt-5`, `argo:gpt-5.2`) via free local proxy on 127.0.0.1:44497.
