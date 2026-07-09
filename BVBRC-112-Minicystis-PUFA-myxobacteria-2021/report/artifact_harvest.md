# Artifact Harvest — BVBRC-112

All artifacts pulled 2026-07-05 UTC. Sizes measured on local disk.

| # | Source | URL/command | Local path | Size |
|---|---|---|---|---|
| 1 | PubMed esummary | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=34511070&retmode=json` | (inline) | — |
| 2 | PMC HTML | `https://pmc.ncbi.nlm.nih.gov/articles/PMC8436480/` | (web_fetch cache) | ~20 KB extracted |
| 3 | PMC XML | `efetch db=pmc id=8436480 rettype=xml` | `work/paper.xml` | 161 KB |
| 4 | Paper body text | derived from #3 | `work/paper_body.txt` | 30 KB |
| 5 | Genome FASTA | `efetch db=nuccore id=CP016211.1 rettype=fasta` | `work/CP016211.fasta` | 16.27 MB |
| 6 | Genome GenBank | `efetch db=nuccore id=CP016211.1 rettype=gbwithparts` | `work/CP016211.gbk` | 32.31 MB |
| 7 | pfa1 protein (A7982_11504) | derived from #6 | `work/A7982_11504.faa` | 549 aa |
| 8 | pfa2/PfaA protein (A7982_11505) | derived from #6 | `work/A7982_11505.faa` | 2,426 aa |
| 9 | pfa3/PfaC protein (A7982_11506) | derived from #6 | `work/A7982_11506.faa` | 2,740 aa |
| 10 | antiSMASH 6.1.1 JSON result | docker run antismash/standalone:6.1.1 on uicgpu (see REPORT §3) | `report/evidence/antismash_summary/CP016211_antismash.json` | 26.8 MB |
| 11 | antiSMASH HTML index | (same) | `report/evidence/antismash_summary/index.html` | 0.27 MB |
| 12 | pfa region GBK (region #42) | (same) | `report/evidence/antismash_summary/pfa_region042.gbk` | 130 KB |
| 13 | BGC-region breakdown TSV | derived from #10 | `report/evidence/bgc_regions.tsv` | 47 rows |
| 14 | Claim comparison JSON | machine-readable summary | `report/evidence/claim_comparison.json` | — |

## Accessions / IDs
- **PMID:** 34511070
- **PMCID:** PMC8436480
- **DOI:** 10.1186/s12864-021-07955-x
- **NCBI nuccore accession:** CP016211.1 (16,040,666 bp, circular)
- **BioProject:** PRJNA321464
- **BioSample:** SAMN05017598
- **Locus-tag prefix:** A7982_
- **Strain / type material:** *Minicystis rosea* DSM 24000ᵀ (soil myxobacterium, family Polyangiaceae, suborder Sorangiineae)
- **Sequencing:** PacBio P6C4, 441,539 reads, 3.49 Gbp total, ~217× coverage

## Tools / versions
- `curl 8.x` (host: CherryRd) for eUtils
- `python 3.13` for parsing (stdlib only, plus optional biopython check)
- `docker` on uicgpu running `antismash/standalone:6.1.1` (2021-era antiSMASH, same major version family the paper's antiSMASH run would have used)
