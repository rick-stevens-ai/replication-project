# Artifact Harvest — BVBRC-48

All artifacts are free/public. No paid endpoints used.

## Paper (open access, CC BY 4.0)
| Item | Source | URL |
|---|---|---|
| Full-text XML | Europe PMC REST | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9244215/fullTextXML |
| DOI | Oxford / JAC | https://doi.org/10.1093/jac/dkac115 |
| PMCID / PMID | | PMC9244215 / 35403193 |

## Genome — MRSN 56 (the paper's exact deposited replicons)
BioProject **PRJNA742487**; fetched via NCBI eutils efetch (fasta), free/no-auth.

| Replicon | Accession | Length (bp) | Role |
|---|---|---:|---|
| Chromosome | CP080452.1 | 4,033,258 | main |
| pMRSN56-1 | CP080453.1 | 2,178 | plasmid |
| pMRSN56-2 | CP080454.1 | 2,725 | plasmid |
| pMRSN56-3 | CP080455.1 | 6,772 | plasmid |
| pMRSN56-4 | CP080456.1 | 8,731 | plasmid |

Multifasta: `work/mrsn56_paper.fna` (4,053,664 bp total, 5 records).
Reads (not downloaded, listed for completeness): SRR14998418 (Illumina MiSeq), SRR14008417 (Oxford Nanopore).

## Comparison sequences (plasmid-identity + ampC claims)
| Accession | What | Used for |
|---|---|---|
| CP021783.1 | pA85-1 (2726 bp) | pMRSN56-2 identity check |
| CP010782.1 | pA1-1 (8731 bp), RepAci1 | pMRSN56-4 identity check |
| CP010781.1 | A1 chromosome (standard GC1 ampC) | ampC-78 context (referenced) |

## IS-element references
| Accession | Element | Length used |
|---|---|---|
| EU029998.1 | ISAba1 transposase region (partial CDS) | ~570 bp transposase segment (blastn) |
| WP_001988464.1 | ISAba125-family transposase | 341 aa (tblastn) |

## Tools / databases (all free)
| Tool | Version | DB |
|---|---|---|
| NCBI Datasets CLI | 18.32.0 | — |
| mlst | 2.33.1 | abaumannii_2 (Pasteur), abaumannii (Oxford) |
| AMRFinderPlus | 4.2.7 | bundled AMR DB (Apr 2026) |
| abricate | 1.4.0 | card, resfinder, ncbi |
| BLAST+ (blastn/tblastn/makeblastdb) | (bvbrc28) | — |

## LLM judge
- Free Argo proxy `http://127.0.0.1:44497/v1`, model `argo:gpt-5.2`, temperature 0. No paid inference.
