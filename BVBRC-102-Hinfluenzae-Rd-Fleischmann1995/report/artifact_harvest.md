# Artifact Harvest — Fleischmann1995 replication

| Artifact | URL / Accession | Size | Checksum | Notes |
|---|---|---|---|---|
| GenBank record NC_000907.1 (H. influenzae Rd KW20, complete sequence, w/ features) | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000907.1&rettype=gbwithparts&retmode=text` | 4,604,072 bytes (4.4 MiB) | MD5 `f13c8a0011a13f610fa9556dd11b5057` | RefSeq derived from original GenBank L42023 (1995 Fleischmann submission). Length = 1,830,138 bp; annotation date `04-APR-2020`. BioProject PRJNA224116, Assembly GCF_000027305.1. Fetched via NCBI E-utilities (free, no auth). |

Additional public references (consulted, not downloaded as bulk data):

- Fleischmann et al. 1995, *Science* 269:496–512, doi:[10.1126/science.7542800](https://doi.org/10.1126/science.7542800), PMID [7542800](https://pubmed.ncbi.nlm.nih.gov/7542800/). Abstract accessible; the paper's specific quantitative claims (1,830,137 bp, ~38% G+C, ~1,743 predicted CDSs, 6 rRNA operons, 54 tRNA genes) are widely cited and appear in the paper's abstract/tables.
- NCBI Assembly GCF_000027305.1 (H. influenzae Rd KW20 reference assembly).
- Fleischmann's TIGR original submission → GenBank L42023 (superseded by NC_000907.1 in RefSeq lineage).

All work performed locally on macOS with Biopython 1.87 / Python 3.14; no GPU or HPC required.
