# Artifact Harvest — BVBRC-55

All artifacts pulled from public NCBI (free, no auth) via E-utilities efetch.

## Paper
| Artifact | Source | Notes |
|---|---|---|
| Full text XML | Europe PMC `PMC8270841/fullTextXML` | `work/paper_fulltext.xml` (50 KB), CC BY 4.0 |

## Genomes (NCBI nuccore)
| Accession | Name | Length (bp) | File |
|---|---|---:|---|
| MN718463.1 | phiCDKH01 (target phage) | 45,089 | `work/phiCDKH01.fasta`, `work/phiCDKH01.gb` |
| LN681534.1 | phiCD24-1 (closest relative) | 44,129 | `work/phiCD24-1.fasta`, `work/panel/LN681534.fasta` |
| GU949551.1 | phiCD6356 | 37,664 | `work/panel/` |
| HG796225.1 | phiCDHM13 | 33,596 | `work/panel/` |
| HG798901.1 | phiCDHM11 | 32,000 | `work/panel/` |
| LK985321.1 | phiCDHM14 | 32,651 | `work/panel/` |
| LK985322.1 | phiCDHM19 | 54,295 | `work/panel/` |
| LN681535.1 | phiCD111 | 41,560 | `work/panel/` |
| LN681536.1 | phiCD146 | 41,507 | `work/panel/` |
| LN681537.2 | phiCD211 | 131,704 | `work/panel/` (myovirus, contrast) |
| LN681539.1 | phiCD505 | 49,316 | `work/panel/` |
| LN681540.1 | phiCD506 | 33,274 | `work/panel/` |
| CP011970.1 | phiCDIF1296T | 131,326 | `work/panel/` (contrast) |
| JACSDL010000003.1 | Host *C. difficile* CD34-Sr contig NODE_3 | 410,108 | `work/host_contig3.fasta` (prophage integration locus) |

## Tools
- BLAST+ 2.17.0 (`blastn`, `makeblastdb`) — local
- minced (CRISPR detection) — local
- Biopython 1.87 — GenBank parsing, genome stats
- Python 3 (custom VIRIDIC-style intergenomic-identity script)
- LLM judge: Argo proxy `gpt-5.2` (free, localhost:44497)
