# Artifact Harvest — BVBRC-53

All artifacts are free/public. No paywalled sources used (paper full text via Europe PMC OA XML, not the paid `pdf` tool).

## Paper (Open Access, CC-BY)
| Item | Source | Notes |
|---|---|---|
| Full text XML | Europe PMC `PMC8765612/fullTextXML` | 213,061 bytes; used to extract claims + accessions |
| DOI | 10.1371/journal.pone.0258283 | PLOS ONE 17(1):e0258283 (2022), PMID 35041663 |

## Sequences (NCBI nuccore, efetch, no auth)
| Plasmid | Accession | Length (bp) | Fetched files | Role |
|---|---|---:|---|---|
| pEpi56 (epidermin, KSE56) | OK031036 | 64,386 | `work/seqs/OK031036.{fasta,gb}` | primary claim C1 |
| pNuk650 (nukacin, KSE650) | OK031035 | 26,160 | `work/seqs/OK031035.{fasta,gb}` | primary claim C2 |
| pIVK45 (nukacin ref) | KP702950 | 21,840 | `work/seqs/KP702950.{fasta,gb}` | reference for C3/C5 |

FASTA byte-length check confirmed exact deposited lengths (64386 / 26160 / 21840).

Reference cluster accessions cited by the paper (not re-fetched; used only as context): epiY'-epiP cluster **X62386**, epiG-epiT'' cluster **U77778**, epidermin canonical Tü3298 prepeptide (UniProt/GenBank canonical epidermin sequence).

## Tools / DBs
| Tool | Version | Where | Use |
|---|---|---|---|
| efetch (NCBI eutils) | REST | local (CherryRd) | sequence download |
| blastn / makeblastdb | 2.16 (BLAST+) | local | pNuk650↔pIVK45 alignment; insertion mapping |
| abricate | 1.4.0 | uicgpu `/data/stevens/envs/bvbrc14` | PlasmidFinder/CARD/ResFinder/VFDB/MEGARes/BacMet2 screen |
| PlasmidFinder DB | 2026-Apr-03 (488 seqs) | uicgpu | rep-typing (paper's declared BV-BRC workflow) |
| amrfinder (AMRFinderPlus) | 4.2.7 | uicgpu | AMR gene screen |
| Python 3 / Biopython-free parsing | — | local | GC%, CDS count, peptide comparison |

## Compute placement
- Sequence fetch, blastn alignment, peptide/GC/CDS parsing: local (small; ~150 kb of sequence).
- BV-BRC specialty-gene screen (abricate + amrfinder, multiple DBs): **uicgpu** (`ssh uicgpu`, conda env `bvbrc14`), per the heavy-compute-offload rule. Scratch: `/data/stevens/scratch/bvbrc53/`.
- LLM judge: Argo proxy `localhost:44497`, model `argo:gpt-5.2` (free).
