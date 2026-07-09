# Artifact Harvest — BVBRC-125

All artifacts pulled during this replication, with URL, size, checksum where computed.

## Publisher / PMC
| Artifact | URL | Size | Local path |
|---|---|---|---|
| Paper PDF (OA) | https://europepmc.org/articles/PMC9519451?pdf=render | 9,286,919 B | `paper.pdf` |
| PMC JATS full-text XML | https://europepmc.org/backend/rest/PMC9519451/fullTextXML | 18 lines (single-line XML, ~110 kB) | `work/pmc_fulltext.xml` |
| PMC OA package (listed, not fetched) | ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/6a/0a/PMC9519451.tar.gz | (not used — earlier stub 990 B in 36123438 dir was truncated) | — |

## Supplementary Tables
| Artifact | URL / Source | Size | Local path |
|---|---|---|---|
| Supplementary Tables S1–S8 | https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-022-01219-4/MediaObjects/41564_2022_1219_MOESM2_ESM.xlsx (available via `36123438-*/data/`) | 83,480 B | `work/supp_tables.xlsx` |

## NCBI Protein (all 32 defence-system proteins)
Batch efetch via `eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=<comma-list>`.
| Accession | Length (aa) | System |
|---|---|---|
| RRM93940.1 | 400 | PD-T4-1 |
| RCO39066.1 | 364 | PD-T4-2 |
| RCO27183.1 | 257 | PD-T4-3 |
| RCO57999.1 | 467 | PD-T4-4 |
| RCO57988.1 | 189 | PD-T4-4 |
| RCQ99930.1 | 314 | PD-T4-5 |
| RRM76169.1 | 436 | PD-T4-6 |
| RRN43039.1 | 352 | PD-T4-7 |
| RCP52534.1 | 408 | PD-T4-8 |
| RCP66309.1 | 192 | PD-T4-9 |
| RCP66310.1 | 77  | PD-T4-9 |
| RCP66311.1 | 129 | PD-T4-9 |
| RCO36089.1 | 171 | PD-T4-10 |
| RCO36088.1 | 251 | PD-T4-10 |
| RCP76574.1 | 500 | PD-λ-1 |
| RCO93357.1 | 92  | PD-λ-2 |
| RCO93356.1 | 402 | PD-λ-2 |
| RCO93355.1 | 375 | PD-λ-2 |
| RCP74640.1 | 159 | PD-λ-3 |
| RCP74641.1 | 267 | PD-λ-3 |
| RCP74642.1 | 477 | PD-λ-3 |
| RCP47953.1 | 1283| PD-λ-4 |
| RCP47952.1 | 248 | PD-λ-4 |
| RCQ13837.1 | 501 | PD-λ-5 |
| RCQ13838.1 | 294 | PD-λ-5 |
| RRK48647.1 | 131 | PD-λ-6 |
| RCQ85672.1 | 449 | PD-T7-1 |
| RRM73498.1 | 320 | PD-T7-2 |
| RRM73410.1 | 596 | PD-T7-2 |
| RCP48690.1 | 455 | PD-T7-3 |
| RRL46918.1 | 219 | PD-T7-4 |
| RRM82777.1 | 390 | PD-T7-5 |

Combined FASTA: `work/defense_proteins.faa` (all 32; ~14 kB).

## NCBI Nuccore (21 GenBank contig slices)
For each of the 21 systems, `efetch.fcgi?db=nuccore&id=<contig>&rettype=gb&retmode=text&seq_start=<orf-15000>&seq_stop=<orf+15000>`.
Contig list (accession, ~size of ±15 kb slice varies with # CDS):

| Contig | System | GB slice file |
|---|---|---|
| RRWJ01000003 | PD-T4-1  | `gb_PD_T4_1.gb` |
| QOYX01000002 | PD-T4-2  | `gb_PD_T4_2.gb` |
| QOZA01000068 | PD-T4-3  | `gb_PD_T4_3.gb` |
| QOYR01000017 | PD-T4-4  | `gb_PD_T4_4.gb` |
| QOXT01000046 | PD-T4-5  | `gb_PD_T4_5.gb` |
| RRWI01000019 | PD-T4-6  | `gb_PD_T4_6.gb` |
| RRWT01000001 | PD-T4-7  | `gb_PD_T4_7.gb` |
| QOXQ01000011 | PD-T4-8  | `gb_PD_T4_8.gb` |
| QOXH01000008 | PD-T4-9  | `gb_PD_T4_9.gb` |
| QOYX01000006 | PD-T4-10 | `gb_PD_T4_10.gb` |
| QOXL01000020 | PD-λ-1   | `gb_PD_L_1.gb` |
| QOYB01000002 | PD-λ-2   | `gb_PD_L_2.gb` |
| QOXN01000003 | PD-λ-3   | `gb_PD_L_3.gb` |
| QOXP01000002 | PD-λ-4   | `gb_PD_L_4.gb` |
| QOWS01000001 | PD-λ-5   | `gb_PD_L_5.gb` |
| RRUL01000001 | PD-λ-6   | `gb_PD_L_6.gb` |
| QOYF01000088 | PD-T7-1  | `gb_PD_T7_1.gb` |
| RRWG01000006 | PD-T7-2  | `gb_PD_T7_2.gb` |
| QOXP01000001 | PD-T7-3  | `gb_PD_T7_3.gb` |
| RRVG01000013 | PD-T7-4  | `gb_PD_T7_4.gb` |
| RRWJ01000050 | PD-T7-5  | `gb_PD_T7_5.gb` |

## NCBI Batch CD-Search (32-protein batch)
- Endpoint: https://www.ncbi.nlm.nih.gov/Structure/bwrpsb/bwrpsb.cgi
- Job ID: `QM3-qcdsearch-1087ADA6AF84AC0E-AA223DDB9807D51`
- Result: `work/cdsearch_results.txt` (9.9 kB, tab-separated hits)
- Runtime: 7 s

## NCBI qblast API (5-system representative panel)
- Endpoint: https://blast.ncbi.nlm.nih.gov/Blast.cgi
- Database: nr, restricted to txid2 (Bacteria)
- Job IDs (all completed READY, but all hit SIGXCPU due to NCBI CPU-time limit for nr+Bacteria queries with 500 hits):
  - PD-T4-3 (RCO27183.1): `4P0CU3D8016`
  - PD-T4-5 (RCQ99930.1): `4P0CXXKU014`
  - PD-T4-8 (RCP52534.1): `4P0D1RJ8014`
  - PD-T7-2 (RRM73498.1): `4P0D5S5R014`
  - PD-λ-1  (RCP76574.1): `4P0D8JTD016`
- Retry with refseq_protein (smaller DB, tighter E, HITLIST 250): `blast_retry_results.json`

## LLM-judge
- Argo endpoint: http://localhost:44497/v1/chat/completions
- Model: argo:gpt-5 (Claude opus-4.7/4.8 returned 502 today — upstream Anthropic response validation error)
- Prompt + response: `work/llm_judge.py`, `work/llm_judge_verdict.json`

## Sibling replications consulted
- BVBRC-26-Ecoli-antiphage-defense-Vassallo2022 (Rick's earlier canonical replication, verdict PARTIAL, 8/9, tool chain: BV-BRC data API).
- 36123438-Anti-phage-defense-Ecoli (earlier stub replication; used for supp-table copy and PMC tarball reference).

## Total data pulled
- 1 PDF (9.3 MB)
- 1 JATS XML (~110 kB)
- 1 supplementary xlsx (83 kB)
- 32 protein FASTA records
- 21 GenBank slices (median ~100 kB each = ~2 MB total)
- 1 CD-Search result set (10 kB)
- 5 BLAST XML results (5 × 2 kB, all SIGXCPU — see failure_analysis.md)

Total network fetch: ~13 MB, ~30 API calls, all free endpoints (NCBI Entrez + Structure + BLAST, EuropePMC, Argo localhost).
