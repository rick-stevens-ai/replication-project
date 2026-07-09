# Artifacts summary — Blackwell 2021 replication

All paths relative to `~/Dropbox/REPLICATE-PROJECT/BVBRC-88-661k-genomes-Blackwell2021/`.

## Reports (`report/`)

| File | Purpose | Notes |
|---|---|---|
| `REPORT.md` | Canonical Markdown report | Verdict: REPLICATED |
| `REPORT.tex` | LaTeX version with dedicated Genuine Critique section | 9 items in Genuine Critique |
| `open_questions.json` | 5 truly-open follow-up questions | Grounded in 661k / Blackwell 2021 methodology |
| `workflow.md` | Reproducible pipeline, step-by-step | Deterministic (seed=661405) |
| `artifacts_summary.md` | This file | |
| `failure_analysis.md` | What did/could go wrong | |
| `brief.md` | 1-paragraph what/why | |
| `attempt_log.md` | Chronological run log | |
| `artifact_harvest.md` | Every URL and file pulled | |

## Evidence (`report/evidence/`)

| File | Contents | Bytes / rows |
|---|---|---|
| `spot_check_results.json` | 25 sampled genomes: local MD5, checklist MD5, match flag, total bp, contig count, GC%, N50 | 25 records |
| `spot_check_species.json` | 25 sampled genomes: ENA XML `SCIENTIFIC_NAME` + `TAXON_ID` | 25 records |
| `species_diversity_check.json` | Full-661k top-20 species + counts + cumulative % | 20 rows + summary |
| `llm_judge_raw.txt` | Raw response from `argo:gpt-5.1` | 1 blob |
| `llm_judge_verdict.json` | Parsed verdict: `{verdict, coverage_pct, agreement_pct, one_line_summary, reasoning}` | 1 object |

## Work area (`work/`)

| File | Source | Size (approx) | Purpose |
|---|---|---:|---|
| `pbio.3001421.pdf` | PLOS OA | 1.83 MB | Paper source |
| `checklist.chk` | ftp.ebi.ac.uk/pub/databases/ENA2018-bacteria-661k/ | 53 MB | Per-file MD5 (661,413 rows) |
| `sampleid_assembly_paths.txt` | ftp.ebi.ac.uk/pub/databases/ENA2018-bacteria-661k/ | 67 MB | Manifest (661,405 rows) |
| `spot_check_sample.tsv` | Local (random.seed=661405) | small | 25 random sample IDs |
| `sample_assemblies/` | ftp.ebi.ac.uk/pub/databases/ENA2018-bacteria-661k/Assemblies/ | ~10-40 MB | 25 verified SAM*.contigs.fa.gz |
| `File2_taxid_lineage_661K.txt` | Figshare 16437939 | 95 MB | Per-sample species + lineage |
| `File4_column_descriptions.txt` | Figshare 16437939 | small | File4 column reference |
| `File4_QC_characterisation_661K.txt` | Figshare 16437939 | 430 MB | Per-sample QC + AMR + plasmid; streamed via awk (not persisted after use) |
| `figshare_meta.json` | api.figshare.com/v2/articles/16437939 | small | Article metadata + download URLs |
| `llm_judge.py` | Local script | small | Argo proxy client for verdict |

## Paper artifacts NOT pulled (out of scope for this replication)

| Artifact | Approx size | Reason skipped |
|---|---:|---|
| `661_assemblies.tar` | 750 GB | Not needed; 25-sample spot check suffices for integrity claim |
| `661k.cobs_compact` | 872 GB | COBS functional round-trip is Open Question #4 — deferred |
| `661_ppsketch_v1.5.h5` | 67 GB | Pp-sketch distance queries not part of tested claims |
| `661K_sourmash_index_scaled.sbt.zip` | 45 GB | Sourmash queries not part of tested claims |
| `File3_metadata_661K.txt` | ~200 MB | Not required to reproduce C1–C6 |

## Total on-disk footprint

- Persisted: ~2 GB (mostly checklist, manifest, File2, 25 sampled assemblies).
- Peak transient: ~2.5 GB (adds File4 while streaming).
- Would-be full artifact pull: ~1.75 TB — deliberately avoided.

## LLM-judge model chain

- First attempt: `argo:claude-opus-4.7` — HTTP 502 (proxy transient).
- Fallback: `argo:gpt-5.1` — valid JSON verdict returned.
- Both routed through the local Argo proxy (`localhost:44497`, key `stevens`); zero paid provider calls.

## Integrity claim summary

- 25/25 random-sample MD5s matched `checklist.chk`.
- 25/25 random samples had realistic bacterial-genome stats.
- 25/25 random samples returned identifiable pathogen names from ENA XML.
- Full-set cardinality: 661,405 total, 639,981 HQ, 21,424 failed — exact match to paper.
- Full-set composition: top-20 = 89.72% (paper "~90%") on 661k; unique species 2,594 on 661k (paper 2,336 on HQ, Delta explained by 21,424 dropped).
