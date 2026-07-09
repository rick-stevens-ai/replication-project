# Artifact Harvest — BVBRC-111

Every public artifact pulled during this replication (2026-07-05):

## Paper metadata
| Item | Source | Size |
|---|---|---|
| Abstract + authors + DOI + journal | NCBI eutils esummary/efetch on PMID 35403193 | text (2 KB) |
| DOI 10.1093/jac/dkac115 | J Antimicrob Chemother | (metadata only) |
| PMC full text | PMC9244215 | (not downloaded; abstract sufficient for claims list) |

## Genome sequence data (all from NCBI FTP + eutils)

| Accession | Type | Size | URL / Fetch |
|---|---|---|---|
| GCA_021484925.1 (ASM2148492v1) | Assembly bundle | ~4.7 MB across 6 files | `https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/021/484/925/GCA_021484925.1_ASM2148492v1/` |
| CP090606.1 | Chromosome | 4,153,776 bp | (part of assembly bundle) |
| CP080453.1 | Plasmid pMRSN56-1 | 2,178 bp | efetch nuccore |
| CP080454.1 | Plasmid pMRSN56-2 | 2,725 bp | efetch nuccore |
| CP080455.1 | Plasmid pMRSN56-3 | 6,772 bp | efetch nuccore |
| CP080456.1 | Plasmid pMRSN56-4 | 8,731 bp | efetch nuccore |
| MRSN56_complete.fna (composite) | chr + 4 plasmids | 4,174,182 bp | built locally |

Assembly bundle files retrieved:
- `GCA_021484925.1_ASM2148492v1_assembly_report.txt` (1,290 B)
- `GCA_021484925.1_ASM2148492v1_genomic.fna.gz` (1,201,240 B)
- `GCA_021484925.1_ASM2148492v1_genomic.gff.gz` (244,443 B)
- `GCA_021484925.1_ASM2148492v1_genomic.gbff.gz` (2,670,142 B)
- `GCA_021484925.1_ASM2148492v1_protein.faa.gz` (600,237 B)
- `GCA_021484925.1_ASM2148492v1_feature_table.txt.gz` (151,924 B)

## Reference protein
| Accession | Purpose | Source |
|---|---|---|
| WP_000116449.1 | WT A. baumannii GyrA (904 aa, multispecies) | efetch protein |

## AMR / MLST database snapshots (already installed in `bvbrc14` env)
| DB | Sequences | Date |
|---|---|---|
| ResFinder | 3,206 | 2026-Apr-3 |
| CARD | 6,052 | 2026-Apr-3 |
| NCBI AMRFinder | 8,232 | 2026-Apr-3 |
| MEGARES | 6,635 | 2026-Apr-3 |
| ARG-ANNOT | 2,224 | 2026-Apr-3 |
| PlasmidFinder | 488 | 2026-Apr-3 |
| VFDB | 4,592 | 2026-Apr-3 |
| pubMLST abaumannii_2 (Pasteur/IP) | (in `mlst` 2.33.1) | mlst db bundled |
| pubMLST abaumannii (Oxford) | (in `mlst` 2.33.1) | mlst db bundled |

## No paywalled / non-public artifacts required. No BV-BRC portal calls made.
