# Artifact Harvest — BVBRC-113

## Primary paper
| Artifact | URL / accession | Size | Notes |
|---|---|---|---|
| PMC full text (JATS XML) | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC8765612 | 225,843 B | complete paper + tables |
| DOI | 10.1371/journal.pone.0258283 | — | open-access CC-BY |
| PubMed ID | 35041663 | — | — |
| PMC ID | PMC8765612 | — | — |

## Deposited plasmid sequences (subjects of the paper)
| Accession | Description | Length | Topology | Local file |
|---|---|---|---|---|
| **OK031036** | *S. epidermidis* KSE56 plasmid **pEpi56** | 64,386 bp | circular | `work/sequences/OK031036.gb` (126,481 B) and `.fasta` (65,393 B) |
| **OK031035** | *S. epidermidis* KSE650 plasmid **pNuk650** | 26,160 bp | circular | `work/sequences/OK031035.gb` (51,704 B) and `.fasta` (26,623 B) |

## Comparator sequences (for claim testing)
| Accession | Description | Length | Local file |
|---|---|---|---|
| **KP702950** | *S. epidermidis* IVK45 plasmid **pIVK45** (comparator for pNuk650) | 21,840 bp | `work/sequences/KP702950.gb` (42,613 B) |
| **X62386** | *S. epidermidis* Tü3298 epiY′/Y/A/B/C/D/Q/P (comparator for epiA identity) | 8,700 bp | `work/sequences/X62386.gb` (21,642 B) |
| **U77778** | *S. epidermidis* pTue32 epiG/E/F/H/T′/T″ (Tü3298 downstream cluster) | 5,292 bp | `work/sequences/U77778.gb` (14,020 B) |

## Locally produced evidence
| File | Description |
|---|---|
| `report/evidence/plasmid_summary.json` | length/CDS/gene counts for every accession + high-level claim checks |
| `report/evidence/bacteriocin_alignment.json` | epiA & nukA CDS translations with nt/aa mismatch counts against comparators |
| `report/evidence/pNuk650_vs_pIVK45_blast.json` | BLASTP results and orthology counts for the "additional ORFs" claim |
| `report/evidence/llm_judge_verdict.txt` | Argo `argo:claude-sonnet-4.6` structured per-claim scoring and overall verdict |
| `work/proteins_pNuk650.faa`, `work/proteins_pIVK45.faa` | FASTA proteomes for BLAST |
| `work/ivk45_db.p*` | BLAST protein database over pIVK45 |
| `work/paper.xml` | Full JATS XML of the paper |

## Tools / versions
| Tool | Version | Source |
|---|---|---|
| Python | 3.14.6 | Homebrew CherryRd |
| Biopython | 1.87 | pip |
| BLAST+ (`blastp`, `makeblastdb`) | /usr/local/bin/blastn (system BLAST+) | — |
| NCBI E-utilities | live via HTTPS | — |
| Argo LLM proxy | localhost:44497 (per TOOLS.md) | free Argo, Bearer stevens |
| Judge model | `argo:claude-sonnet-4.6` | free Argo |

## Data availability
All primary sequence data is public (NCBI). All processed evidence is inside this directory. No paywalled resources used.
