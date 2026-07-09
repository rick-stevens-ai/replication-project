# Artifact Harvest — BVBRC-44

All public, all free (NCBI eutils / Datasets, no auth). Downloaded to `uicgpu:/data/stevens/scratch/bvbrc44-pCl107/genomes/`.

## Primary study assemblies (strain Cl107)
| Accession | Description | Size (bytes fasta) | Length (bp) | Notes |
|---|---|---:|---:|---|
| CP098521.1 | *A. baumannii* Cl107 **chromosome** | 4,114,260 | 4,056,235 | Exact match to paper |
| CP098522.1 | *A. baumannii* Cl107 plasmid **pCl107** | 201,639 | 198,716 | Exact match to paper; 197 CDS in RefSeq annotation |
| CP098522.1.gbff | pCl107 GenBank flatfile (annotation) | 471,211 | — | Used for module/gene coordinate mining |

SRA raw reads (referenced, not downloaded/reassembled): SRR20613520 (Illumina MiSeq), SRR20613519 (MinION).

## Reference plasmids (comparative / evolutionary analysis)
| Accession | Plasmid | Length (bp) | Role in paper |
|---|---|---:|---|
| KU744946.1 | pA297-3 (A297/RUH875) | ~200,633 | AbGRI1-related resistance region reference |
| CP012005.1 | pAB3 (ATCC 17978-mff) | ~151,167 | AbGRI1 ancestral-structure reference |
| KT779035.1 | pD4 | ~132,632 | MPF_I ST25 plasmid family |
| MF399199.1 | pD46-4 | ~207,977 | MPF_I ST25 plasmid family |
| MK531536.1 | pMC1.1 (MC1, ST991 Bolivia) | ~184,770 | Paper's closest relative to pCl107 |

## Paper (open access, CC BY)
- Europe PMC full-text XML: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10117892/fullTextXML (172 KB, saved to work/fulltext.xml)
- DOI: 10.1093/femsmc/xtac027 · PMC10117892 · PMID 37332503

## Databases used
- AMRFinderPlus 3.12.8 (bundled DB) · abricate DBs: resfinder, plasmidfinder, card (2026-Apr build) · PubMLST *abaumannii* (Pasteur) + *abaumannii_2* (Oxford) schemes via `mlst`.
