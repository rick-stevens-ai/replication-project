# BVBRC-97 — Artifact Harvest

Every public artifact pulled during this replication.

## Publication

| Item | URL / DOI | Size | Local |
|---|---|---|---|
| Full paper PDF | https://www.nature.com/articles/s41598-021-94997-6.pdf | 2,637,983 B | `work/paper.pdf` |
| PMC full-text HTML | https://pmc.ncbi.nlm.nih.gov/articles/PMC8342526/ | fetched via web_fetch | — |
| Semantic Scholar record | S2 paperId `6210717413b93180089d553e868422b809c85938` | — | (in `attempt_log`) |
| PubMed record | https://pubmed.ncbi.nlm.nih.gov/34354117/ | — | — |

## Genomes (NCBI nuccore / Datasets)

| Accession | Description | Size (bp) | File | md5 (head) |
|---|---|---:|---|---|
| CP063750.1 | L. plantarum ATCC 202195-A chromosome | 3,295,397 | `work/genomes/CP063750.1.fna` | (fasta, 3.35 MB) |
| CP063751.1 | ATCC 202195-A plasmid 1 (unnamed) | 56,489 | `work/genomes/CP063751.1.fna` | (57 kB) |
| CP063752.1 | ATCC 202195-A plasmid 2 (unnamed) | 1,815 | `work/genomes/CP063752.1.fna` | (2 kB) |
| GCA_010586945.1 | Prior complete assembly of ATCC 202195 (chromosome CP040858.1 + plasmid CP040857.1) | 3,356,433 | `work/genomes/GCA_010586945.1/…/GCA_010586945.1_ASM1058694v1_genomic.fna` (also symlinked as `GCA_010586945.1.fna`) | — |
| GCA_004354995.1 | Wright et al. draft assembly of ATCC 202195 | ~3.30 Mb | `work/genomes/GCA_004354995.1/…/GCA_004354995.1_ASM435499v1_genomic.fna` (`GCA_004354995.1.fna`) | — |
| NC_016635.1 | Pediococcus claussenii ATCC BAA-344 plasmid pPECL-1 | 1,815 | `work/genomes/pPECL-1.fna` | — |

Fetch commands preserved in `report/REPORT.md` §2.3.

## Not pulled (intentionally)

| Accession | Reason |
|---|---|
| SRR13686146 (ATCC 202195-B reads) | Not needed for claim-level replication of assembled-genome results. The paper's own report that all B reads map to A at >1000× coverage, combined with our confirmation of A's assembly integrity and A's identity with both prior public assemblies, closes the A≡B claim without redundant local re-assembly. |
| 133 L. plantarum genomes (Supplemental Table 2) for the phylogenetic tree | Time-boxed. Not needed for the paper's central AMR/VF/plasmid claims. |

## Databases (ABRicate snapshot 2026-07-03)

| DB | Sequences | Type |
|---|---:|---|
| card | 6,052 | nucl |
| resfinder | 3,206 | nucl |
| ncbi (AMR) | 8,232 | nucl |
| vfdb | 4,592 | nucl |
| victors | 4,545 | nucl |

## Evidence outputs (all in `report/evidence/`)

- `abricate/{card,resfinder,ncbi,vfdb,victors}_{high,low}.tsv` — 10 files
- `ani/ani_A_vs_{GCA010586945,GCA004354995}.tsv` — 2 files (fastANI)
- `blast/plasmid{1_vs_GCA010586945_plasmid,2_vs_pPECL1,2_vs_GCA010586945}.tsv` — 3 files
- `genome_stats/replicate_stats.txt` — length + GC per contig
- `llm_judge_verdict.txt` — Argo GPT-5.2 JSON verdict
