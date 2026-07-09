# Artifact Harvest — BVBRC-85 · Ali et al. 2019 MRSA SO-1977

All artifacts pulled 2026-07-03 from public sources (no login, no auth required).

## Paper full text
| Item | URL | Size | Note |
|---|---|---|---|
| PMC XML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6558803/fullTextXML | 79,504 B | Europe PMC OA REST; saved as `work/paper_PMC6558803.xml` |
| DOI | https://doi.org/10.1186/s12866-019-1470-2 | — | BMC Microbiology, open access (CC BY 4.0) |

## Paper-declared accessions (from Table 1)
| Accession | Kind | Source | Independent-status |
|---|---|---|---|
| `NFZY00000000` | WGS master | GenBank | ✅ resolvable, links to assembly UID 1156631 |
| `PRJNA385553` | BioProject | NCBI | ✅ resolvable |
| `SAMN06894057` | BioSample | NCBI | ✅ resolvable |
| `MK713975` | 16S rRNA seq | GenBank | ✅ present (matched by 100% BLAST to extracted 16S from assembly) |

## Genome assemblies downloaded (subject + comparators from paper Table 4)
| Strain | Accession | FTP root | Local file | md5 (local) |
|---|---|---|---|---|
| SO-1977 (subject) | GCA_002224825.1 / GCF_002224825.1 (ASM222482v1) | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/224/825/GCA_002224825.1_ASM222482v1/ | `work/downloads/SO1977_genomic.fna` (2,877,714 B) | 7bebb2a1b59ec31d004be2d1b0096125 |
| SO-1977 proteome | ↑ | ↑ | `SO1977_protein.faa` (976,288 B) | af14eb8497e69fc11ad4faf9de8e0378 |
| SO-1977 feature table | ↑ | ↑ | `SO1977_feature_table.txt` (849,299 B) | 7a5f837cf69168dcffed9fb1c86e8d19 |
| SO-1977 GFF | ↑ | ↑ | `SO1977_genomic.gff` (1,439,025 B) | ba9c98de6193e66a5c7db06e8bcd62f2 |
| MRSA252 | GCF_000011505.1 (ASM1150v1) | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/011/505/ | `GCF_000011505.1_genomic.fna` (2,938,978 B) | 03cc5fb90c6040bc1ad1a014d176ebcc |
| MSSA476  | GCF_000011525.1 (ASM1152v1) | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/011/525/ | `GCF_000011525.1_genomic.fna` (2,855,876 B) | 1f791149a2a9e5024cf56994c87093c6 |
| NCBI md5 authoritative | — | `md5checksums.txt` from each FTP root | `evidence/ncbi_md5checksums.txt` | (matches local; verified) |

## Reference databases
| DB | Version | Fetched by | Sequences |
|---|---|---|---|
| CARD | abricate 2026-Jul-03 build | `abricate --list` | 6,052 nucl |
| NCBI AMR | 2026-Jul-03 | ↑ | 8,232 |
| ResFinder | 2026-Jul-03 | ↑ | 3,206 |
| VFDB | 2026-Jul-03 | ↑ | 4,592 |
| PlasmidFinder | 2026-Jul-03 | ↑ | 488 |
| ARG-ANNOT | 2026-Jul-03 | ↑ | 2,224 |
| MEGARes | 2026-Jul-03 | ↑ | 6,635 |
| Victors | 2026-Jul-03 | ↑ | 4,545 |
| pubMLST S. aureus scheme | shipped with mlst 2.19.0 | `/usr/local/Cellar/mlst/2.19.0/libexec/db/pubmlst/saureus/` | 7 MLST loci + profile table |
| NCBI nt (remote BLAST) | 2026-07-03 remote via NCBI | `blastn -remote -db nt` | — |

## Tools / versions
- abricate 1.4.0
- ncbi-blast+ (blastn, tblastn, makeblastdb) — Homebrew build (MBEDTLS warning benign)
- pubMLST saureus scheme via manual blastn (mlst binary blocked by Homebrew Perl 5.34↔5.32 mismatch; re-implemented in ~30 lines of Python that call blastn directly against `*.tfa` files)
- Python 3.13 stdlib for parsing / stats
- Argo proxy (localhost:44497) → `argo:gpt-5.2`, `argo:claude-sonnet-4.6`, `argo:gemini-2.5-pro` for LLM-judge (FREE endpoint — no Anthropic/OpenAI/OpenRouter direct calls)
