# Artifacts Summary — BVBRC-125

Inventory of every file produced or pulled during this replication, with size and role.

## Top-level (`/`)
| File | Size | Role |
|---|---|---|
| `paper.pdf` | 9,286,919 B | Source PDF from EuropePMC |

## Extraction (`extraction/`)
| File | Size | Role |
|---|---|---|
| `marker.md` | ~70 kB | JATS-derived full-text markdown (Marker-equivalent) |
| `nougat.mmd` | ~70 kB | JATS-derived full-text markdown (Nougat-equivalent) |

## Report (`report/`)
| File | Role |
|---|---|
| `REPORT.md` | Full narrative report (17 kB) |
| `REPORT.tex` | LaTeX version of the full report (item 4 of 8-artifact standard) |
| `brief.md` | 1-paragraph summary |
| `attempt_log.md` | Chronological log |
| `artifact_harvest.md` | Every artifact pulled with URL/size |
| `workflow.md` | Workflow + tools + effort estimate |
| `artifacts_summary.md` | This file |
| `failure_analysis.md` | Failures and how they were handled |
| `open_questions.json` | 5 heavy-duty open questions with `next_steps` |
| `evidence/` | Copies of key intermediate results (see below) |

## Work directory (`work/`)

### Custom code (10 scripts, ~550 LOC)
| Script | LOC | Role |
|---|---|---|
| `jats_to_md.py` | 75 | JATS XML → markdown |
| `parse_supp.py` | 25 | xlsx → JSON |
| `build_master.py` | 100 | build master systems JSON from supp tables |
| `fetch_proteins.py` | 70 | batch NCBI Protein efetch |
| `hmmer_pfam.py` | 100 | batch CD-Search submit + poll |
| `parse_cdd.py` | 85 | CD-Search tab parser + concordance |
| `prophage_context.py` | 110 | Nuccore GenBank slice + MGE keyword scan |
| `blast_panel.py` | 120 | qblast async wrapper (nr / Bacteria) |
| `blast_retry.py` | 80 | qblast retry (refseq_protein) |
| `llm_judge.py` | 130 | Argo LLM verdict |

### Data files
| File | Size | Content |
|---|---|---|
| `paper.pdf` | 9.3 MB | Source PDF (copy) |
| `paper.txt` | 45 kB | pdftotext fallback |
| `pmc_fulltext.xml` | ~110 kB | PMC JATS full-text XML |
| `paper_full.md` | ~70 kB | JATS-derived markdown |
| `supp_tables.xlsx` | 83 kB | Supplementary Tables S1-S8 |
| `supp_tables_all.json` | ~500 kB | All 8 supp tables → JSON |
| `master_systems.json` | ~15 kB | Independent count of 21 systems + 71 strains + 32 proteins |
| `defense_proteins.faa` | ~14 kB | All 32 defence proteins FASTA |
| `defense_proteins_meta.json` | ~5 kB | Per-protein annotation, length, per-system grouping |
| `cdsearch_results.txt` | 10 kB | NCBI Batch CD-Search results (tabular) |
| `cdd_summary_per_system.json` | ~10 kB | Per-system CD-Search domain summary |
| `cdd_vs_paper_concordance.json` | ~5 kB | HHpred (paper) vs CD-Search concordance table |
| `prophage_context_results.json` | ~15 kB | MGE/prophage scan results per system |
| `gb_PD_*.gb` (21 files) | median ~100 kB each | GenBank ±15 kb slices |
| `blast_rids.json` | ~500 B | qblast job IDs (5 systems) |
| `blast_*.xml` (5 files) | ~2 kB each | qblast results (SIGXCPU on all 5) |
| `blast_retry_results.json` | pending | qblast retry with refseq_protein |
| `llm_judge_verdict.json` | ~600 B | LLM-judge JSON verdict |

## Traces / logs
| File | Content |
|---|---|
| `err.log` | JATS parser lxml FutureWarning (harmless) |
| `cdsearch_run.log` | CD-Search submit/poll trace |
| `blast_run.log` | qblast panel run trace (empty due to tee buffering; real trace via stdout only) |
| `blast_retry.log` | qblast retry trace |
| `cdd_analysis.log` | CD-Search parse + concordance printout |
| `prophage_run.log` | Prophage-context per-system summary |

## Provenance chain

```
PDF (EuropePMC) ──▶ paper.pdf
     │                    │
     └─▶ pdftotext ──▶ paper.txt
PMC JATS XML ──▶ pmc_fulltext.xml ──▶ jats_to_md ──▶ paper_full.md ──▶ marker.md, nougat.mmd

Supp xlsx ──▶ parse_supp ──▶ supp_tables_all.json
                                       │
                                       ├─▶ build_master ──▶ master_systems.json (21 systems verified)
                                       │
                                       └─▶ Table S5 ──▶ 71 strains verified

master_systems ──▶ 32 protein accessions ──▶ fetch_proteins ──▶ defense_proteins.faa (32/32)
                                                                        │
                                                                        ├─▶ CD-Search ──▶ cdsearch_results ──▶ concordance vs paper HHpred
                                                                        │
                                                                        └─▶ qblast (5 panel) ──▶ SIGXCPU ──▶ retry with refseq_protein

master_systems ──▶ 21 contig accessions + coords ──▶ prophage_context ──▶ 21 gb_*.gb ──▶ 21/21 MGE evidence

All above ──▶ llm_judge (Argo gpt-5) ──▶ PARTIAL, coverage 8/10, agreement 9/10
```

## Sibling replications (external references)
- `~/Dropbox/REPLICATE-PROJECT/BVBRC-26-Ecoli-antiphage-defense-Vassallo2022/` — canonical first replication (verdict PARTIAL, 8/9), BV-BRC tool chain.
- `~/Dropbox/REPLICATE-PROJECT/36123438-Anti-phage-defense-Ecoli/` — earlier stub replication with older supp-table copy.
