# Artifacts and traces — BVBRC-120

## Public artifacts pulled

| Source | Item | URL | Size | Notes |
|---|---|---|---|---|
| NCBI PubMed esummary | Paper metadata | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=37337195` | JSON | confirmed title, DOI, PMC |
| BMC Microbiology | Full-text PDF | `https://bmcmicrobiol.biomedcentral.com/counter/pdf/10.1186/s12866-023-02907-9.pdf` | 10.26 MB | main paper |
| Springer static-content | Supplementary S1 (178 host strains) | `.../12866_2023_2907_MOESM1_ESM.xlsx` | 18,595 B | 178 host names + accessions |
| Springer static-content | Supplementary S2 (functional proteins) | `.../MOESM2_ESM.xlsx` | 11,928 B | 30 COG entries |
| Springer static-content | Supplementary S3 (36 prophages) | `.../MOESM3_ESM.xlsx` | 12,125 B | prophage names + hosts |
| Springer static-content | Supplementary S4 (20 focal lytic phages) | `.../MOESM4_ESM.xlsx` | 10,685 B | 20 focal accessions |
| Springer static-content | Supplementary S5 (homologous seqs of 3 focal phages) | `.../MOESM5_ESM.xlsx` | 14,413 B | 25 blast hits |
| Springer static-content | Supplementary S6 (Type-I lysis module homologs) | `.../MOESM6_ESM.xlsx` | 18,190 B | 105 rows |
| Springer static-content | Supplementary S7 (Type-II lysis module homologs) | `.../MOESM7_ESM.xlsx` | 17,209 B | 105 rows |
| Springer static-content | Supplementary S8 (blast of functional genes) | `.../MOESM8_ESM.xlsx` | 24,282 B | 200+ blast rows |
| Springer static-content | Supplementary S9 (236 lytic phages) | `.../MOESM9_ESM.xlsx` | 17,603 B | 236 accessions + names |
| NCBI efetch nuccore | 231 Bacillus lytic phage genomes | `efetch -db nuccore -id ...` (231 accessions from S9) | ~22 MB FASTA | 5 accessions dropped by NCBI |
| NCBI efetch nuccore | 13 additional focal lytic phages (NC_* series) | as above | ~1 MB FASTA | 7 of 20 focal already in the 231 set |

## Derived artifacts in this repo

| File | Description |
|---|---|
| `paper.pdf` | Full-text paper (10.26 MB) |
| `extraction/marker.md` | Marker parse of paper |
| `extraction/nougat.mmd` | Nougat parse of paper |
| `report/REPORT.md` | Full replication report (Markdown) |
| `report/REPORT.tex` | Full replication report (LaTeX) |
| `report/brief.md` | 1-paragraph what/why summary |
| `report/attempt_log.md` | Chronological attempt log |
| `report/artifact_harvest.md` | Every artifact pulled with provenance |
| `report/open_questions.json` | 5 heavy-duty open questions, each with basis + next_steps |
| `report/workflow.md` | Full workflow + tool list + effort estimate |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Honest failure/gap analysis |
| `report/evidence/summary_236.json` | Length/GC/bin stats on 231 lytic genomes |
| `report/evidence/summary_20.json` | Length/GC on 20 focal lytic genomes |
| `report/evidence/mash_236_stats.json` | Summary stats over 53,130 MASH pairs |
| `report/evidence/mash_20_stats.json` | Summary stats over 380 MASH pairs (20-focal) |
| `report/evidence/protein_clusters.json` | MMseqs2 clustering summary (231-lytic) |
| `report/evidence/protein_clusters_20.json` | MMseqs2 clustering summary (20-focal) |
| `report/evidence/genome_length_gc.tsv` | Per-genome length + GC (231 rows) |
| `report/evidence/lytic_20_lengths_gc.tsv` | Per-genome length + GC (20 rows) |
| `report/evidence/mash_dist_all.tsv` | All-pairs MASH distances (53,361 rows incl. self) |
| `report/evidence/mash_dist_20.tsv` | 20-focal all-pairs MASH distances (400 rows incl. self) |
| `report/evidence/mash_dist_histogram.txt` | Coarse histogram of 231-set distances |
| `report/evidence/mash20_nj.nwk` | Newick BIONJ tree of 20 focal phages |
| `report/evidence/mash20.phy` | PHYLIP square distance matrix (20 focal) |
| `report/evidence/all_236_stats_global.tsv` | seqkit stats summary on 231-set FASTA |
| `report/evidence/logs/*` | Every tool log |
| `work/S1_178_bacillus_strains.csv` | 178 host names + accessions (extracted from S1) |
| `work/S4_20_lytic_phages.csv` | 20 focal accessions (extracted from S4) |
| `work/S9_236_lytic_phages.csv` | 236 lytic accessions (extracted from S9) |
| `work/supp/bvbrc120_supp{1..9}.xlsx` | All 9 supplementary XLSX files |
| `work/paper.txt` | pdftotext dump of paper |

## Reproducibility

- All input data are on NCBI (open, no login).
- All tools are free and installable from bioconda.
- Total genome data volume: ~22 MB (231 FASTA sequences).
- Total compute: ~2 min on 32-thread uicgpu; the Marker + Nougat parses add ~10 min each in parallel.
- All shell scripts + Python analytics are in `/data/stevens/bvbrc120/` on uicgpu and copies in `report/evidence/logs/` (as invocation traces).

## Traces (logs)

- `report/evidence/logs/download_236.log` — efetch batch download log
- `report/evidence/logs/prodigal.log` — ORF prediction (231 + 20)
- `report/evidence/logs/mmseqs.log` — MMseqs2 clustering (231)
- `report/evidence/logs/rapidnj.log` — BIONJ tree construction
- `report/evidence/logs/mafft.log` — MAFFT attempt (abandoned)
- `report/evidence/logs/analyze.stdout`, `phase2.stdout` — orchestrator stdout captures
