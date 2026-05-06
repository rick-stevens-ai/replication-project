# PROGRESS — Replication of Vassallo et al. 2022

## Status: ✅ COMPLETE

## Timeline
- **10:58 CDT** — Started, created project directories
- **11:00 CDT** — Confirmed PMC9519451, extracted full paper text from XML
- **11:02 CDT** — Downloaded supplementary tables (MOESM2_ESM.xlsx) from Springer
- **11:03 CDT** — Cloned GitHub repo (chrisdoering8197/phagedefense)
- **11:04 CDT** — Extracted all 21 defence systems × 32 protein accessions from Table S2
- **11:05 CDT** — Downloaded all 32 protein FASTA sequences from NCBI
- **11:07 CDT** — Submitted 21 BLASTP jobs to NCBI BLAST API (vs nr, E. coli restricted)
- **11:15 CDT** — Retrieved BLAST results for all 21 systems
- **11:20 CDT** — Analyzed distribution, cross-referenced with Table S4
- **11:25 CDT** — Wrote REPORT.md

## Final Deliverables
- `report/REPORT.md` — Full replication report with scores
- `data/defense_proteins.fasta` — All 32 protein sequences
- `data/blast_results.json` — BLAST results for all 21 systems
- `data/supplementary_tables.xlsx` — Paper's supplementary data
- `data/phagedefense/` — Cloned GitHub repository
- `data/system_protein_map.tsv` — System-to-protein mapping
- `data/protein_accessions.txt` — All protein accession numbers

## Overall Score: 4.3/5 — SUBSTANTIALLY CONFIRMED
