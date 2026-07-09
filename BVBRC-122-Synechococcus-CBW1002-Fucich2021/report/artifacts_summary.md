# Artifact Summary — BVBRC-122

All artifacts either downloaded directly from NCBI or computed on uicgpu with FOSS tools. No paywall interactions.

## Public artifacts pulled

| Artifact | URL | Purpose |
|---|---|---|
| Paper PDF | https://europepmc.org/articles/PMC7881327?pdf=render | Source paper (via uicgpu proxy) |
| Paper text | pdftotext -layout paper.pdf | Extraction for LLM-judge and reading |
| CBW1002 fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_015840915.1_ASM1584091v1/… | Primary target genome |
| CBW1006 fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_015840525.1_ASM1584052v1/… | Primary target genome |
| BS55D fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_004332415.1_ASM433241v1/… | Bornholm cluster reference |
| CB0101 fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_000179235.2_ASM17923v2/… | Chesapeake summer subcluster 5.2 |
| WH8102 fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_000195975.1_ASM19597v1/… | Marine subcluster 5.1 |
| PCC7002 fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_000019485.1_ASM1948v1/… | Marine 5.3 |
| PCC6312 fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_000316685.1_ASM31668v1/… | Freshwater |
| Cyanobium gracile PCC6307 fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_000316515.1_ASM31651v1/… | Cyanobium sister-taxon (paper's suggestion) |
| S. elongatus PCC7942 fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_000012525.1_ASM1252v1/… | Freshwater elongatus |
| Synechocystis PCC6803 fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_000009725.1_ASM972v1/… | Freshwater outgroup |
| Prochlorococcus MED4 fna+gff+faa | ftp.ncbi.nlm.nih.gov/…/GCF_000011465.1_ASM1146v1/… | Outgroup |

## Computed artifacts (in `report/evidence/`)

| File | Description |
|---|---|
| `panel_16S.fasta` | 11 16S rRNA sequences extracted from GFF+FASTA (each 1,482-1,490 bp) |
| `panel_16S.aln` | MAFFT --auto multiple alignment (1,494 cols) |
| `tree_panel.nwk` | FastTreeMP GTR+Γ Newick tree |
| `CBW1002_CBW1006_RBH.tsv` | 2,949 reciprocal-best-BLASTp pairs (paper: 3,023) |
| `CBW1002_CB0101_RBH.tsv` | 2,107 RBH pairs |
| `CBW1002_WH8102_RBH.tsv` | 1,808 RBH pairs |
| `CBW1002_PCC6803_RBH.tsv` | 1,548 RBH pairs |
| `CBW1002_Cyanobium6307_RBH.tsv` | 2,251 RBH pairs |
| `CBW1002_BS55D_RBH.tsv` | 1,893 RBH pairs |
| `cbw1002_report.txt` | NCBI assembly stats |
| `cbw1006_report.txt` | NCBI assembly stats |
| `summary_evidence.txt` | flat summary → LLM-judge input |
| `llm_judge.json` | LLM-judge output (Argo GPT-4o) |

## Sizes and (light) integrity checks

- CBW1002 FASTA: 3,902,368 bytes; single-record `NZ_CP060398.1`, length 3,854,122 bp (paper-exact).
- CBW1006 FASTA: 3,908,451 bytes; single-record `NZ_CP060396.1`, length 3,860,130 bp (paper-exact).
- 11-taxon 16S FASTA: 16,393 bytes, 11 records.
- Sum of 6 RBH TSVs: ~600 KB.

## Working / staging locations

- Full computational workspace remains on uicgpu at `~/repl/bvbrc122/` (not sync'd to Dropbox; too large for daily backups).
- Small evidence + report artifacts copied to `~/Dropbox/REPLICATE-PROJECT/BVBRC-122-Synechococcus-CBW1002-Fucich2021/report/evidence/`.
