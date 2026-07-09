# Artifacts Summary — BVBRC-85 (S. aureus SO-1977, Sudan; Ali et al. 2019)

**Verdict:** PARTIAL REPLICATION (doubly-confirmed by independent second-agent rerun)
**Assembly under test:** `GCA_002224825.1` (WGS `NFZY00000000`), md5 `7bebb2a1b59ec31d004be2d1b0096125`

---

## Report-level artifacts (`report/`)

| File | Description |
|---|---|
| `REPORT.md` | Primary replication report (Markdown) — 22 claims (C1–C22), 3-strain comparative table, verdict + justification, independent second-agent reproduction section |
| `REPORT.tex` | LaTeX version of the report with dedicated Genuine Critique section |
| `brief.md` | Short-form brief of the target and outcome |
| `attempt_log.md` | Chronological attempt log for the replication run |
| `artifact_harvest.md` | Inventory of harvested artifacts (paper text, assemblies, DBs) |
| `workflow.md` | 10-stage workflow documentation |
| `open_questions.json` | 5 genuinely-open questions grounded in the Ali 2019 Sudan context |
| `failure_analysis.md` | Failure modes and partial-verdict rationale |
| `artifacts_summary.md` | This file |

## Evidence artifacts (`report/evidence/`)

### Comparative & summary
| File | Description |
|---|---|
| `evidence_summary.md` | Compact evidence summary passed to LLM-judge models |
| `AMR_comparison_table.tsv` | 3-strain × N-gene AMR presence/absence table (paper Table 4 rerun) |

### abricate outputs — SO-1977
| File | DB | SO-1977 hits |
|---|---|:-:|
| `abricate_card.tsv` | CARD | 16 |
| `abricate_ncbi.tsv` | NCBI | 5 |
| `abricate_resfinder.tsv` | ResFinder | 4 |
| `abricate_vfdb.tsv` | VFDB | 73 |
| `abricate_victors.tsv` | Victors | 33 |
| `abricate_argannot.tsv` | ARGannot | 9 |
| `abricate_megares.tsv` | MEGARes | 19 |
| `abricate_plasmidfinder.tsv` | PlasmidFinder | 3 (repUS43, repUS70, rep5a) |

### abricate outputs — comparators
| File | Genome | DBs |
|---|---|---|
| `abricate_MRSA252_card.tsv` | MRSA252 (`GCF_000011505.1`) | CARD |
| `abricate_MRSA252_ncbi.tsv` | MRSA252 | NCBI |
| `abricate_MRSA252_resfinder.tsv` | MRSA252 | ResFinder |
| `abricate_MRSA252_vfdb.tsv` | MRSA252 | VFDB |
| `abricate_MSSA476_card.tsv` | MSSA476 (`GCF_000011525.1`) | CARD |
| `abricate_MSSA476_ncbi.tsv` | MSSA476 | NCBI |
| `abricate_MSSA476_resfinder.tsv` | MSSA476 | ResFinder |
| `abricate_MSSA476_vfdb.tsv` | MSSA476 | VFDB |

### Taxonomy
| File | Description |
|---|---|
| `SO1977_16S.fa` | Extracted 16S rRNA locus (locus tag `CA803_14545`, contig `NFZY01000100.1`, 48–1604, 1,557 bp) |
| `16S_blast_nt.tsv` | Remote `blastn -db nt -task megablast -perc_identity 99` results (100.000% ID to multiple S. aureus references) |

### mecR1 edge-truncation cross-check
| File | Description |
|---|---|
| `mecR1_query.faa` | MRSA252 MecR1 protein `WP_000952923.1` (585 aa) used as tblastn query |

### MD5 integrity
| File | Description |
|---|---|
| `ncbi_md5checksums.txt` | Authoritative NCBI md5checksums (source of truth) |
| `md5_local.txt` | Locally re-computed md5s — match authoritative |

### LLM-judge verdicts (free-endpoint Argo proxy)
| File | Model | Verdict | Coverage |
|---|---|:-:|:-:|
| `llm_judge_verdict_gpt52.txt` | `argo:gpt-5.2` | PARTIAL | 0.75 |
| `llm_judge_claude-sonnet-4.6.txt` | `argo:claude-sonnet-4.6` | PARTIAL | 0.82 |
| `llm_judge_gemini-2.5-pro.txt` | `argo:gemini-2.5-pro` | PARTIAL | 0.80 |

### Independent second-agent reproduction (`evidence/independent_reproduction/`)
- Fresh downloads (SO-1977, MRSA252, MSSA476) via `datasets` CLI (independent path from `work/downloads/`)
- Own `genome_stats.py` (independent, no code reuse) — matched all 6 stats exactly
- Prodigal V2.60 output — 2,706 CDS (paper 2,629 RAST, primary repl 2,783 PGAP)
- Refreshed abricate 1.4.0 outputs for all 3 strains × {CARD, NCBI, ResFinder, VFDB, PlasmidFinder}
- `indep_summary.json` — machine-readable pass/fail across 16 checked items (16/16 pass)
- `tool_versions.txt` — reproducibility manifest
- `comparison.md` — side-by-side paper vs prior repl vs independent rerun

## Working artifacts (`work/`)

| Path | Description |
|---|---|
| `paper_PMC6558803.xml` | Europe PMC full-text XML (79,504 B) |
| `paper_text_full.txt` | Parsed plain text of the paper |
| `downloads/` | All assembly + comparator FASTAs, GFFs, feature tables, protein FAAs |
| `analysis/` | MLST BLAST scripts, intermediate blastn hit tables, MLST profile lookup |

---

## Headline reproducibility metrics

- **Numeric genome stats:** 8/8 exact match (size, GC, contigs, N50, largest, coverage, assembler, CDS magnitude)
- **Central paper claim (`tet(K)+tet(M)` unique to SO-1977):** REPRODUCED under abricate 1.4.0 + CARD/ResFinder identical-protocol rerun on all 3 strains
- **Secondary comparative claim (`norA` unique):** CONTRADICTED — `norA` present in all 3 strains
- **Data integrity:** MD5 of downloaded FNA matches authoritative NCBI md5 `7bebb2a1b59ec31d004be2d1b0096125`
- **Novel findings not in paper:** ST140 (MLST) + 3 plasmid replicons (repUS43, repUS70, rep5a)
- **LLM-judge consensus:** 3/3 models converge on PARTIAL, coverage 0.75–0.82
- **Independent second-agent reproducibility:** 16/16 checked items reproduce byte-exactly
