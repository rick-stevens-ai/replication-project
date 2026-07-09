# Artifact Harvest — BVBRC-36

## Paper
| Item | Value |
|---|---|
| Journal version | PLoS ONE 14(7):e0220494, DOI 10.1371/journal.pone.0220494, PMID 31361781, PMC6667211 |
| Preprint | bioRxiv DOI 10.1101/571364 (PPR72441), posted 2019-03-07 |
| OA PDF | https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0220494&type=printable → `work/paper.pdf` (1,314,417 B) |
| Full text XML | Europe PMC PMC6667211 → `work/fulltext.xml` (180,173 B) |

## Genome assemblies (NCBI efetch, nuccore, free/no-auth)
All complete, closed replicons from the paper's deposited PacBio-based assemblies.

| Accession | Strain | Replicon | Length (bp) | sha256[:16] |
|---|---|---|---:|---|
| CP037941 | CFSAN027350 | chromosome | 5,436,079 | 1df828b84c6cf398 |
| CP037942 | CFSAN027350 | plasmid pCFSAN027350 (157kb) | 157,534 | 03461461ae0afc1d |
| CP037943 | CFSAN027343 | chromosome | 5,689,156 | 82be5bc08e21cf4e |
| CP037944 | CFSAN027343 | plasmid pCFSAN027343 (88kb) | 88,848 | 6fd296354dd63374 |
| CP037945 | CFSAN027346 | chromosome | 5,592,581 | e52c88ceb9b3b51c |
| CP037946 | CFSAN027346 | plasmid pCFSAN027346-1 (95kb) | 96,016 | 4573596b789a271f |
| CP037947 | CFSAN027346 | plasmid pCFSAN027346-2 (72kb, AMR-bearing) | 73,152 | dfbdc0246805a324 |

## Raw reads (identified, metadata pulled via ENA; NOT downloaded — see report §Limitations)
| Run | Platform | Reads | Bytes |
|---|---|---:|---:|
| SRR8335317 | Oxford Nanopore (MinION) | 300,787 | 3.49 GB |
| SRR8335318 | Illumina (MiSeq) | 7,900,050 | ~3.8 GB |
| SRR8333590/91/92 | Illumina (MiSeq) | ~1.2–1.5 M ea | ~0.4 GB ea |
| — | PacBio | (assembly-only deposit) | — |

## Reference gene databases (abricate-format nucleotide FASTA, GitHub tseemann/abricate)
| DB | Sequences | Use |
|---|---:|---|
| resfinder | 3,206 | acquired AMR genes |
| vfdb | 4,592 | virulence factors |
| ecoli_vf | 2,701 | E. coli-specific virulence (stx, eae, esp*, tccP, efa1, espI…) |
| plasmidfinder | 488 | Inc replicon typing |

## MLST (PubMLST, E. coli seqdef DB, Achtman scheme #1)
7-locus allele FASTAs (adk fumC gyrB icd mdh purA recA) + 16,242-row profile table → `work/mlst/`.

## Tools
BLAST+ 2.x (`blastn`, `makeblastdb`), Python 3 / Biopython 1.87, curl. All local CPU (~5 min total). All sources free/public.
