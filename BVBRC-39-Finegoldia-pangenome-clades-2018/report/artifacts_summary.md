# Artifacts Summary — BVBRC-39 (Finegoldia pangenome / clades, Brüggemann 2018)

All artifacts live under the replication root:
`~/Dropbox/REPLICATE-PROJECT/BVBRC-39-Finegoldia-pangenome-clades-2018/`

---

## Reports (`report/`)

| File | Purpose |
|------|---------|
| `REPORT.md`             | Primary human-readable Markdown report (paper summary, claims, method, results, verdict, gaps). Source of truth for all backfill files. |
| `REPORT.tex`            | LaTeX version with dedicated **Genuine Critique** section. |
| `open_questions.json`   | 5 open follow-on research questions with concrete next steps. |
| `workflow.md`           | End-to-end pipeline + tool inventory + work estimate. |
| `artifacts_summary.md`  | *This file.* |
| `failure_analysis.md`   | Honest failure / limitations write-up (PDF availability, unrun manual analyses, single-judge caveats). |

---

## Reproducibility artifacts (`work/`)

### Input & mapping
| File | Contents |
|------|----------|
| `fulltext.xml` / `fulltext.txt` | Europe PMC full text (PMC5762925), used to extract WGS accessions and claims text. |
| `paper_17_map.tsv` | 17-row mapping: paper WGS project prefix + strain name → current NCBI GCA accession. 1:1 match verified. |
| `acc_list.txt` | Bare list of 17 GCA accessions used as input to `datasets download`. |

### Genome data
| File | Contents |
|------|----------|
| `fin17.zip` / `fin17/` | 17 assemblies from NCBI Datasets (genome FASTA + protein FASTA + GFF3 each). |
| `genome_paths.txt` | List of assembly-FASTA paths for fastANI input. |
| `blastdb/` | Per-strain `makeblastdb` protein databases (17 dbs). |

### Genome-stats layer (C2)
| File | Contents |
|------|----------|
| `genome_stats.py` | Script: length, contig count, GC%, CDS count from PGAP `protein.faa`. |
| `genome_stats.json` | Per-strain table (17 rows) with all Table-1-equivalent metrics. |

### ANI / clade layer (C3, C4)
| File | Contents |
|------|----------|
| `fastani_raw.tsv` | fastANI all-vs-all output (289 rows = 17×17). |
| `ani_analysis.py` | Loads matrix, computes summary stats. |
| `ani_results.json` | Distribution of ANI values, min/max/mean. |
| `ani_cluster2.py` | SciPy average-linkage, forces 2-cluster cut, names clades by ATCC 29328 presence. |
| `clades2.json` | 2-clade assignment: 9 magna / 8 nericia. Inter-clade min 90.67% ANI, intra-clade mean 96.06% ANI. |

### Pan-genome layer (C5, C6)
| File | Contents |
|------|----------|
| `pan_12.faa` | Concatenated proteomes of the 12-genome subset (4 magna + 8 nericia). |
| `pan_12_cdhit` / `pan_12_cdhit.clstr` | CD-HIT output (c=0.5, n=3) — representative seqs + cluster membership. |
| `pangenome.py` | Parses .clstr → core (12/12), singletons (1/12), pan total, per-k frequency histogram. |
| `pangenome_12.json` | core=1209, singletons=892, pan=2992, freq dist (1→892, 2→222, 3→169, …, 12→1209). |

### Virulence-factor layer (C7 partial, C8, C9)
| File | Contents |
|------|----------|
| `refs/uniprot_vf.faa` / `uniprot_vf2.faa` | UniProt curated *F. magna* reference proteins (7 factors). |
| `vf_query.faa` | Deduped/canonicalized VF query FASTA used for blastp. |
| `vf_survey.py` | Runs blastp per strain, applies presence threshold pident≥40 & cov≥50%; CAMP paralog count at pident≥30 & cov≥40%. |
| `vf_results.json` | Per-strain presence/absence matrix for 6 host-interacting factors + summary. |
| `camp_copies.json` | Per-strain CAMP-factor paralog counts (all 17 = 2 copies). |
| `annotation_survey.json` | Earlier keyword-based sortase/pilus survey (superseded by blastp for VFs, kept for sortase count support of C7). |

### Judge layer
| File | Contents |
|------|----------|
| `llm_judge.py` | Sends claims + numeric results to Argo free (gpt-5.2, opus-4.8 fallback), parses JSON verdict. |
| `llm_judge_output.json` | verdict=REPLICATED, coverage=9/9, agreement=9/9. |

### Log / narrative artifacts (referenced in REPORT.md §3)
| File | Contents |
|------|----------|
| `attempt_log.md` | Chronological log of commands run, versions, and any retries. |
| `artifact_harvest.md` | Provenance notes for every downloaded file (URL, date, SHA where captured). |

---

## Trace summary

Every quantitative number in the primary REPORT.md is directly backed by an on-disk artifact:

| REPORT.md claim | Number | Source artifact |
|-----------------|--------|-----------------|
| CDS/genome mean | 1759   | `genome_stats.json` |
| GC% range       | 31.7–32.1% | `genome_stats.json` |
| Number of clades | 2      | `clades2.json` |
| Inter-clade min ANI | 90.67% | `clades2.json` (from `fastani_raw.tsv`) |
| Intra-clade mean ANI | 96.06% | `clades2.json` |
| 12-set split    | 4 magna / 8 nericia | `clades2.json` |
| Core proteome   | 1209   | `pangenome_12.json` (from `pan_12_cdhit.clstr`) |
| Singletons      | 892    | `pangenome_12.json` |
| Pan-genome families | 2992 | `pangenome_12.json` |
| CAMP copies/strain | 2 (all 17) | `camp_copies.json` |
| Protein L presence | 2/17 (11%) | `vf_results.json` |
| FAF presence    | 12/17 (70%) | `vf_results.json` |
| Alb-binding     | 9/17 (52%) | `vf_results.json` |
| PAB             | 8/17 (47%) | `vf_results.json` |
| Sortase per genome | 4–9 (all 17 positive) | `annotation_survey.json` |
| Overall verdict | REPLICATED | `llm_judge_output.json` (confirms this REPORT.md verdict) |

---

## Corpus-scale note

NCBI Datasets currently indexes **278 *Finegoldia* genome records (168 primary GCA)** — a ~10× expansion since the 2018 paper's n=17. This corpus-availability observation is derived from the NCBI Datasets taxon report captured during accession mapping. Not persisted as a separate JSON artifact, but easy to re-derive: `datasets summary genome taxon Finegoldia --as-json-lines | wc -l`.

---

## Reproducibility one-liner

```bash
cd work/ && bash -c "
datasets download genome accession --inputfile acc_list.txt --include genome,protein,gff3 --filename fin17.zip
unzip -o fin17.zip -d fin17
python3 genome_stats.py
fastANI --ql genome_paths.txt --rl genome_paths.txt -o fastani_raw.tsv
python3 ani_cluster2.py
python3 pangenome.py 12
python3 vf_survey.py
python3 llm_judge.py
"
```

~5 minutes on a laptop; $0.
