# Artifact Harvest — BVBRC-83

All artifacts pulled from NCBI on 2026-07-03 (fetched via `eutils.ncbi.nlm.nih.gov`, no auth).

## Target plasmid
| Accession | Description | Size | File | Source URL |
|---|---|---|---|---|
| CP102481.1 | *P. aeruginosa* PE52 plasmid **pPE52IMP** — the target of the paper | 27,635 bp | `work/pPE52IMP_CP102481.gb` (76 KB) + `.fasta` (28 KB) | https://www.ncbi.nlm.nih.gov/nuccore/CP102481.1 |

## Sibling plasmids (Figure 3 comparators)
| Accession | Plasmid | Size | File |
|---|---|---|---|
| AM778842.1 | pMATVIM-7 | 24,179 bp | `work/sibling_AM778842.1.gb/.fasta` |
| CP033834.1 | unnamed (FDAARGOS_570) | 36,032 bp | `work/sibling_CP033834.1.gb/.fasta` |
| KX169264.1 | pD5170990 | 32,424 bp | `work/sibling_KX169264.1.gb/.fasta` |
| KP975076.1 | pMRVIM0713 | 36,032 bp | `work/sibling_KP975076.1.gb/.fasta` |
| MN336501.1 | p4130-KPC | 58,104 bp | `work/sibling_MN336501.1.gb/.fasta` |

## Paper metadata
| Field | Value |
|---|---|
| PMID | 36144465 |
| PMCID | PMC9501424 |
| DOI | 10.3390/microorganisms10091863 |
| Full-text | https://pmc.ncbi.nlm.nih.gov/articles/PMC9501424/ (Open Access, CC-BY) |
| Metadata | `work/pubmed_36144465.json` |

## Derived files
| File | Description |
|---|---|
| `work/candidate_repA_ppe52imp.faa` | 301 aa RepA (paper) / KfrA (siblings) candidate |
| `work/candidate_traI_relaxase_ppe52imp.faa` | 609 aa MOBP11 relaxase |
| `work/all_sibling_proteins.faa` | Concatenated sibling plasmid proteomes (222 CDS) for BLAST |
| `work/sibling_db.p*` | Sibling proteome BLAST database |
| `work/evidence_ppe52imp.json` | Structural claims analysis output |
| `work/evidence_repA_relaxase_blast.json` | Per-sibling best-hit BLAST scores |
| `work/claims_reproduction_table.json` | 13-claim reproduction table |
| `work/evidence_llm_judge.json` | LLM judge outputs (Argo GPT-4o and GPT-5.2 via free Argo proxy) |
