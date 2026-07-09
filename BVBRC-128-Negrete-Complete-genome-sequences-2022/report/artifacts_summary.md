# Artifacts Summary — BVBRC-128 Negrete

## Downloaded artifacts (real, public)

| Artifact | Source | Size | Purpose |
|----------|--------|-----:|---------|
| paper.pdf | https://gutpathogens.biomedcentral.com/counter/pdf/10.1186/s13099-022-00500-5.pdf | 2,220,111 B | Source paper (OA BMC) |
| work/sequences/CP078106.fna | NCBI EFetch (nuccore, fasta) | 4,425,011 B | GK1025B chromosome (4,362,605 bp) |
| work/sequences/CP078106.ft  | NCBI EFetch (nuccore, ft) | 1,115,320 B | GK1025B chromosome feature table (CDS count) |
| work/sequences/CP078107.fna | NCBI EFetch | 103,316 B | pGK1025B_1 (101,769 bp) |
| work/sequences/CP078107.gb  | NCBI EFetch (gbwithparts) | 240,068 B | pGK1025B_1 full annotation |
| work/sequences/CP078108.fna | NCBI EFetch | 121,992 B | pGK1025B_2 (120,182 bp) |
| work/sequences/CP078108.gb  | NCBI EFetch | 266,535 B | pGK1025B_2 full annotation (T6SS, arsenic operon) |
| work/sequences/CP078109.fna | NCBI EFetch | 47,286 B  | pGK1025B_3 (46,528 bp) |
| work/sequences/CP078109.gb  | NCBI EFetch | 115,920 B | pGK1025B_3 full annotation (T4SS, phospholipase D) |
| work/sequences/CP078110.fna | NCBI EFetch | 4,412,846 B | H322 chromosome (4,350,614 bp) |
| work/sequences/CP078110.ft  | NCBI EFetch | 1,121,066 B | H322 chromosome feature table |
| work/sequences/CP078111.fna | NCBI EFetch | 102,268 B | pH322_1 (100,741 bp) |
| work/sequences/CP078111.gb  | NCBI EFetch | 242,004 B | pH322_1 full annotation (SSU5 prophage) |
| work/sequences/CP078112.fna | NCBI EFetch | 119,961 B | pH322_2 (118,185 bp) |
| work/sequences/CP078112.gb  | NCBI EFetch | 270,505 B | pH322_2 full annotation (T6SS, arsenic operon, ~6 Kbp deletion region) |
| work/SSU5_NC_018843.fna | NCBI EFetch | 104,828 B | Salmonella phage SSU5 (BLAST reference) |
| work/plasmidfinder_db/enterobacteriales.fsa | https://bitbucket.org/genomicepidemiology/plasmidfinder_db/raw/HEAD/enterobacteriales.fsa | 130 KB | CGE PlasmidFinder Enterobacteriales replicon DB (159 sequences) |

## Generated artifacts (traces of replication)

| Artifact | Kind | Purpose |
|----------|------|---------|
| work/verify_table1.py | script | Recomputes length + GC + CDS count from FASTA/GB |
| work/all_plasmids.fna | intermediate | Concatenated 5 plasmid FASTA for BLAST DB |
| work/plasmids_blastdb.{nhr,nin,nsq} | BLAST DB | Local DB of 5 plasmids |
| work/plasmidfinder_hits.tsv | raw output | All BLAST hits (any pident>=60) |
| work/plasmidfinder_cge_defaulthits.tsv | raw output | Filtered to CGE defaults (>=95% id, >=60% cov) — 0 rows |
| work/mlst_query/CP078110_result.json | raw output | PubMLST live sequence query response for H322 chromosome |
| work/mlst_query/CP078106_result.json | raw output | PubMLST live sequence query response for GK1025B chromosome |
| report/evidence/table1_verification.json | evidence | Structured Table-1 recomputation results |
| report/evidence/mlst_results_summary.json | evidence | Consolidated MLST results |
| report/evidence/plasmidfinder_summary.json | evidence | Consolidated PlasmidFinder results |
| report/evidence/ssu5_blast_summary.json | evidence | SSU5 phage BLAST coverage summary |
| report/evidence/secretion_system_spans.json | evidence | T4SS/T6SS cluster span measurements |
| report/REPORT.md | required | Full replication report (Markdown) |
| report/REPORT.tex | required | Full replication report (LaTeX, section-by-section) |
| report/open_questions.json | required | 5 heavy open questions with next steps |
| report/workflow.md | required | Workflow + tools + effort estimate |
| report/failure_analysis.md | required | Honest failure/gap analysis |
| report/artifact_harvest.md | required | Chronological artifact harvest log |
| report/attempt_log.md | required | Chronological attempt log |
| extraction/marker.md | required | Marker-substitute text extraction (pdftotext -layout) |
| extraction/nougat.mmd | required | Nougat-substitute text extraction (pdftotext) |

## External accessions cited
- **NCBI GenBank:** CP078106, CP078107, CP078108, CP078109, CP078110, CP078111, CP078112
- **NCBI BioProject:** PRJNA258403 (data submission), PRJNA186875 (parent GenomeTrakr)
- **NCBI BioSample:** SAMN04329637 (GK1025B), SAMN06124518 (H322)
- **NCBI SRA:** SRR8305966, SRR8305970 (short-read polishing; not re-downloaded)
- **NCBI RefSeq (reference phages):** NC_018843 (SSU5), NC_028699, NC_019708, NC_031940, NC_005856, NC_006949
