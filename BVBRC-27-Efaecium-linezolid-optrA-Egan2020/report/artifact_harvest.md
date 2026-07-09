# Artifact Harvest — BVBRC-27 (Egan et al. 2020)

All artifacts are free and public. Pulled 2026-07-01.

## Paper
| Item | Source | Notes |
|---|---|---|
| Full text (OA) | Europe PMC `PMC7303821/fullTextXML` | 80,113 bytes; CC/OA. DOI 10.1093/jac/dkaa075 |

## Study-deposited data (GenBank, via NCBI eutils efetch)
The paper deposited assembled plasmids + optrA-variant regions (NO raw reads / SRA / BioProject).

| Accession | Molecule | Length (bp) | Contents (annotated) |
|---|---|---:|---|
| MN831410 | pM17/0149 (*E. faecalis*) plasmid | 36,331 | optrA, fexA — the "pE349"(=pE394) optrA plasmid |
| MN831411 | pM16/0594 (*E. faecium*) plasmid | 21,849 | poxtA, tet(M), tet(L), IS1216E cassette |
| MN831412 | pM18/0011 (*E. faecalis*) plasmid | 18,280 | poxtA, fexB |
| MN831413 | pM17/0314 (*E. faecium*) plasmid | 103,600 | optrA, cfr(D), erm(B) |
| MN831414 | optrA_I region (*E. faecalis* M17/0240) | 10,551 | optrA, fexA |
| MN831415 | optrA_II region (*E. faecalis* M18/0173) | 9,742 | optrA, fexA |
| MN831416 | optrA_III region (*E. faecium* M17/0314) | 7,967 | optrA |
| MN831417 | optrA_IV region (*E. faecalis* M18/0906) | 11,697 | optrA, fexA, ant(9)-Ia |
| MN831418 | optrA_V region (*E. faecium* M16/0594) | 10,738 | optrA, fexA |
| MN831419 | optrA_VI region (*E. faecalis* M18/0497) | 12,562 | optrA, fexA |

Each downloaded as both `.gb` (GenBank flat file) and `.fasta` into `work/genbank/`.

## Reference data (independent screen)
| Artifact | Source | Size | Use |
|---|---|---|---|
| AMRFinderPlus AMR_CDS.fa | `ftp.ncbi.nlm.nih.gov/pathogen/.../AMRFinderPlus/database/latest/` | 11.07 MB / 9,712 alleles | Curated AMR gene catalog for the independent screen |
| optrA canonical (NG_048023.1) | NCBI eutils | 2,168 bp | Verify optrA identity + variants |
| pE394 (KP399637.1) | NCBI eutils | 36,331 bp | The real reference plasmid the paper calls "pE349" |

## Tools
| Tool | Version | Use |
|---|---|---|
| BLAST+ (blastn, makeblastdb) | 2.x (local /usr/local/bin) | AMR screen + plasmid alignments |
| Biopython | 1.87 | GenBank/FASTA parsing, CDS extraction |
| curl + NCBI eutils | — | data download |
| Argo proxy (localhost:44497, argo:gpt-4o) | free ANL endpoint | LLM-judge verdict |

No paywalled data, no commercial software, no paid API. Total data footprint ~12 MB.
