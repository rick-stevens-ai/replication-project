# Artifacts Summary — BVBRC-112

Complete inventory of every file produced or pulled during the replication, plus URLs, accessions, sizes, and (where trivial) checksums. Compiled 2026-07-05 (backfill pass).

## Top-level

| Path | Purpose | Size | Source |
|---|---|---|---|
| `paper.pdf` | Original PDF (item 1 of the 8-artifact standard) | ~2 MB | `https://bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-021-07955-x.pdf` |
| `extraction/marker.md` | Marker/pdftotext plaintext extraction (item 2) | ~30 KB | `pdftotext -layout paper.pdf` fallback (central Eagle SCOUT corpus not queried in this pass) |
| `extraction/nougat.mmd` | Nougat parse (item 3) — **pending** stub | small | Header pointer; needs central Nougat sweep (GPU) |

## `report/` (items 4–8 + supporting)

| Path | Purpose |
|---|---|
| `report/REPORT.tex` | LaTeX detailed replication report (item 4) — 24 KB, section-by-section |
| `report/REPORT.md` | Original markdown report (kept for reference) |
| `report/open_questions.json` | 5 heavy-duty open questions with next_steps (item 5) |
| `report/workflow.md` | Comprehensive workflow narrative + tools + effort estimate (item 6) |
| `report/artifacts_summary.md` | This file (item 7) |
| `report/failure_analysis.md` | Honest failure analysis + critique of evidence (item 8) |
| `report/brief.md` | Original wave brief (short, paper + verdict) |
| `report/attempt_log.md` | Timestamped log of every action taken during the replication |
| `report/artifact_harvest.md` | Provenance table for every file pulled from NCBI/PMC (deprecated by this file for the backfill standard, but kept) |

### `report/evidence/`

| Path | Purpose | Size |
|---|---|---|
| `basic_stats.log` | Output of Python stdlib GenBank parser (C1–C5 raw output) | small |
| `bgc_regions.tsv` | 47-row TSV of antiSMASH region product tags + coords (C6–C7 raw output) | small |
| `claim_comparison.json` | Machine-readable claim-by-claim status | small |
| `antismash_summary/CP016211_antismash.json` | Full antiSMASH 6.1.1 output JSON (C6 evidence) | 26.8 MB |
| `antismash_summary/index.html` | antiSMASH HTML report index | 0.27 MB |
| `antismash_summary/pfa_region042.gbk` | Extracted region GBK for the pfa cluster (C8 evidence) | 130 KB |
| `llm_judge_llama70.txt` | Full Llama-3.3-70B judge output (score 98) | small |
| `llm_judge_nemotron3ultra.txt` | Full Nemotron-3-Ultra judge output (score 95) | small |
| `llm_judge_summary.md` | Judge consensus (REPLICATED, 96) | small |

## `work/`

| Path | Purpose | Size |
|---|---|---|
| `paper.xml` | PMC full-text XML (PMC8436480) | 161 KB |
| `paper_body.txt` | Plaintext body extracted from `paper.xml` | 30 KB |
| `CP016211.fasta` | Complete genome sequence (nuccore CP016211.1) | 16.27 MB |
| `CP016211.gbk` | GenBank flat file w/ all CDS/product/translation | 32.31 MB |
| `A7982_11504.faa` | pfa1/PfaD protein translation | 549 aa |
| `A7982_11505.faa` | pfa2/PfaA protein translation | 2,426 aa |
| `A7982_11506.faa` | pfa3/PfaC protein translation | 2,740 aa |

## External accessions / IDs

| Kind | ID | Resolver |
|---|---|---|
| DOI | `10.1186/s12864-021-07955-x` | https://doi.org/10.1186/s12864-021-07955-x |
| PMID | `34511070` | https://pubmed.ncbi.nlm.nih.gov/34511070/ |
| PMCID | `PMC8436480` | https://pmc.ncbi.nlm.nih.gov/articles/PMC8436480/ |
| NCBI nuccore | `CP016211.1` | https://www.ncbi.nlm.nih.gov/nuccore/CP016211.1 (16,040,666 bp, circular) |
| BioProject | `PRJNA321464` | https://www.ncbi.nlm.nih.gov/bioproject/PRJNA321464 |
| BioSample | `SAMN05017598` | https://www.ncbi.nlm.nih.gov/biosample/SAMN05017598 |
| Locus-tag prefix | `A7982_` | in-record namespace |
| Type strain | *Minicystis rosea* DSM 24000ᵀ (aka SBNa008, NCCB 100349) | https://www.dsmz.de |

## Verdict tag (kept, backfill pass)
- **REPLICATED**, consensus LLM-judge score **96**, no numeric contradictions on tested claims.
- 8-artifact standard: 8/8 present (nougat.mmd is a pending stub — see failure_analysis.md item 4).
