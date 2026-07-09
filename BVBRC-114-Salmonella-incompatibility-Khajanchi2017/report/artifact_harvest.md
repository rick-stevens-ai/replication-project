# Artifact Harvest — BVBRC-114

## Paper
- `paper.pdf` — 2,268,011 bytes; PDF v1.4; from `https://bmcgenomics.biomedcentral.com/track/pdf/10.1186/s12864-017-3954-5` (BMC track/pdf endpoint; PMC PDF endpoint returned HTML).
- CC BY 4.0.

## Focal WGS assemblies (7 strains, BioProject PRJNA312617)
| Strain | Serovar (paper) | WGS master | Assembly acc (this replication) | Assembly size (bp) | Contigs | Source URL |
|---|---|---|---|---:|---:|---|
| SE163A | Typhimurium | LSZD00000000 | GCA_001647955.1 | 5,202,941 | 257 | NCBI Datasets |
| SE696A | Typhimurium | LXHA00000000 | GCF_001700345.1 | 5,096,557 | 230 | NCBI Datasets |
| SE710A | Typhimurium | LXGZ00000000 | GCF_001700365.1 | 5,100,225 | 318 | NCBI Datasets |
| SE819 | Heidelberg | LSZE00000000 | GCF_001647935.1 | 4,914,824 | 233 | NCBI Datasets |
| SE397 | Typhimurium | LYRR00000000 | GCF_001729025.1 | 5,429,084 | 856 | NCBI FTP genomes/all/ |
| SE452 | Typhimurium | LYRS00000000 | GCF_001729035.1 | 5,134,028 | 524 | NCBI FTP genomes/all/ |
| SE478 | Typhimurium | LYRT00000000 | GCF_001729045.1 | 5,158,316 | 585 | NCBI FTP genomes/all/ |

## Reference / comparator genomes (5)
| Strain | Accession | Length (bp) | Note |
|---|---|---:|---|
| LT2 (Typhimurium) | NC_003197.1 | 4,857,432 | Type strain reference |
| CVM29188 (Kentucky) plasmid pCVM29188_101 | CP001121.1 | 101,461 | Paper Table 1 comparator plasmid |
| CVM29188 pCVM29188_146 (IncFIB(K), sit+iuc+iut) | CP001122.1 | 146,811 | Source of tblastn query proteins |
| BovineChina SA972816 (Typhimurium) | CP007484.1 | 4,891,923 | Bovine ST comparator |
| USMARC-1808 (Typhimurium, bovine) | CP014969.1 | 4,936,894 | Paper Table 1 |
| USMARC-1880 (Typhimurium, bovine) | CP014981.1 | 4,815,208 | Paper Table 1 |

## Database
- **PlasmidFinder rep-gene DB** — cloned from `https://bitbucket.org/genomicepidemiology/plasmidfinder_db.git` on 2026-07-05; 488 rep sequences across 10 replicon-family files (`Inc18.fsa Rep1-3.fsa RepA_N.fsa RepL.fsa Rep_trans.fsa NT_Rep.fsa enterobacteriales.fsa`).

## Iron-acquisition query proteins (extracted from CP001122.1 pCVM29188_146)
| Gene | Protein ID | Length (aa) | Product |
|---|---|---:|---|
| sitA | ACF57166.1 | 304 | Fe/Mn ABC transporter binding protein |
| sitB | ACF57037.1 | 274 | Inner membrane subunit |
| sitC | ACF57108.1 | 285 | Inner membrane subunit |
| sitD | ACF57144.1 | 285 | Membrane subunit |
| iucA | ACF57181.1 | 574 | Aerobactin biosynthesis |
| iucB | ACF57105.1 | 315 | Aerobactin biosynthesis |
| iucC | ACF57162.1 | 580 | Aerobactin biosynthesis |
| iutA | ACF57170.1 | 50 | Ferric-aerobactin receptor (short-CDS annotation on CP001122) |
| iroB | ACF57087.1 | 387 | Salmochelin |

## Tools used (with versions)
- Python 3.8.10 (system)
- BLAST+ 2.15.0 (blastn, tblastn, makeblastdb)
- NCBI E-utilities esearch/efetch 22.4
- NCBI Datasets CLI 16.x
- SeqSero2 v1.3+ (k-mer mode)
- mlst 2.35.0 (`salmonella` scheme via PubMLST)
- mash 2.3
- amrfinder (available, not needed for this replication)
- Biopython 1.87 (Phylo.TreeConstruction)
- pdftotext (poppler) — extraction fallback

## Traces
- Full evidence tree at `report/evidence/` (seqsero, mlst, plasmid, iron, phylogeny/mash).
- Scripts on uicgpu at `~/bvbrc-114-salmonella/{fetch2.sh,fetch4.sh,analyze2.sh,plasmid.sh,iron3.sh,phylo.sh}`.
