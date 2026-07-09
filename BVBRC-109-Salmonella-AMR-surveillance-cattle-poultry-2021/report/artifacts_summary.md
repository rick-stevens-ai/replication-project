# BVBRC-109 — Artifacts Summary

**Replication**: Delgado-Suárez et al., *PLoS ONE* 16(5):e0243681 (2021)
**Verdict**: PARTIAL, 78/100 (Argo GPT-5.2 LLM-judge, 2026-07-05)
**Root dir**: `~/Dropbox/REPLICATE-PROJECT/BVBRC-109-Salmonella-AMR-surveillance-cattle-poultry-2021/`
**Heavy artefacts**: `uicgpu:/data/stevens/bvbrc109/`

---

## Report tier (`report/`)

| File | Type | Purpose |
|---|---|---|
| `REPORT.md` | Markdown | Canonical long-form replication write-up (paper summary, 9-claim table, methods, results, verdict, data availability). 16 KB. |
| `REPORT.tex` | LaTeX | Publication-formatted version of REPORT.md with dedicated GENUINE CRITIQUE section. |
| `brief.md` | Markdown | Short executive summary (paper + verdict + top-3 findings). |
| `attempt_log.md` | Markdown | Chronological log of replication steps and any dead-ends. |
| `artifact_harvest.md` | Markdown | Inventory of what was pulled from the paper (PDF, S1–S7, accessions). |
| `workflow.md` | Markdown | Step-by-step pipeline documentation (Stage 0 through Stage 8) with ASCII dataflow diagram. |
| `artifacts_summary.md` | Markdown | This file — index of all replication outputs. |
| `failure_analysis.md` | Markdown | Deep-dive on the two divergences (ramR reversal, 100% mutation inflation) and lessons learned. |
| `open_questions.json` | JSON | 5 open questions grounded in this replication + next-steps for follow-ups. |
| `evidence/replication_summary_v2.json` | JSON | Machine-readable summary of per-claim results, chi², p-values, ORs. |
| `evidence/judge_verdict.json` | JSON | LLM-judge output (Argo GPT-5.2 rubric-scored, per-claim reasoning). |

## Working tier (`work/`)

### Paper text & metadata
| File | Size approx | Contents |
|---|---|---|
| `paper.pdf` | ~2 MB | PLOS OA printable PDF (curl). |
| `paper.txt` | ~120 KB | pdftotext -layout extraction of paper.pdf. |
| `S1_File.xlsx` / `.csv` | ~80 KB | 77 study isolates + SRR/SAMN accessions + QC flags. |
| `S2_File.xlsx` / `.csv` | ~600 KB | 2400 public NCBI Mexico Salmonella by source (untested C9 data). |
| `S3_File.xlsx` / `.csv` | ~40 KB | 40 public Mexican Typhimurium with pre-computed AMR. |

### Assembly + accession bookkeeping
| File | Size approx | Contents |
|---|---|---|
| `all_prja_assemblies.tsv` | ~few KB | Full BioProject PRJNA480281 SAMN→GCA map from `datasets`. |
| `study_isolates.csv` | ~30 KB | Normalised study metadata (isolate ID, matrix, serovar, SRR, SAMN). |
| `public_isolates.csv` | ~500 KB | Normalised S2 (untested C9 comparison cohort). |
| `study_assemblies.tsv` | ~5 KB | 68-row table of study SAMN + matched GCA + assembly QC. |
| `missing_samns.txt` | ~200 B | 9 SAMNs with SRA reads but no GenBank assembly (documented gap). |

### Per-genome AMR + typing outputs
| File | Size approx | Contents |
|---|---|---|
| `assemblies_flat/GCA_*.fna` | ~315 MB total | 68 downloaded assemblies (on uicgpu, mirrored subset in Dropbox). |
| `amr_out/GCA_*.tsv` | ~68 files, ~50 KB each | AMRFinderPlus per-genome gene calls. |
| `amr_out/GCA_*.mut.tsv` | ~68 files, ~5 KB each | AMRFinderPlus per-genome mutation calls (`--mutation_all`). |
| `all_amr_calls.tsv` | ~3 MB | Concatenated AMR gene calls across 68 isolates. |
| `all_mut_calls.tsv` | ~500 KB | Concatenated mutation calls across 68 isolates. |
| `mlst_results.tsv` | ~10 KB | mlst 2.33.1 senterica_achtman_2 output for all 68. |
| `sgi1_out/*.blast.tsv` | ~8 files, ~2 KB each | Per-Typhimurium blastn hits vs AF261825.2 reference. |
| `sgi1_ref.fna` | ~45 KB | AF261825.2 SGI-1 reference fetched via efetch. |

### Analysis scripts
| File | Language | Purpose |
|---|---|---|
| `analyze.py` | Python 3.11 | Initial analysis pass (superseded by v2). |
| `analyze_v2.py` | Python 3.11 | Final analysis: AMR class assignment, MDR classification, chi² + Fisher on LN-vs-GB, Typh-vs-Other, ramR-vs-MDR contingencies. Emits `evidence/replication_summary_v2.json`. |
| `judge_prompt.md` | Markdown | Assembled prompt to Argo GPT-5.2 LLM-judge (paper abstract + our claim table + honest divergences). |

---

## Numerical highlights (from `evidence/replication_summary_v2.json`)

| Metric | Paper | This replication |
|---|---|---|
| Isolate count matched | 77/77 | 68/77 (88%, 9 no GenBank assembly) |
| Serovar counts (all 8) | exact match | exact match on 68-subset |
| Kentucky ST | ST-198 | ST-198 (4/4) |
| Typhimurium ST | ST-19 | ST-19 (7/7) |
| monophasic ST | ST-34 | ST-34 (1/1) |
| SGI-1 in Typhimurium | 9/10 | 6/8 in re-analysed subset (consistent) |
| GB vs LN MDR χ² | 12.0 (p=0.0005) | 3.73 (p=0.053) — same direction |
| GB vs LN OR | 6.5 | 2.71 — same direction |
| Typh vs Other MDR χ² | 24.5 (p<0.0001) | 7.46 (p=0.006) — same direction |
| Typh vs Other OR | 45.8 (5.3–399.2) | 12.1 — same direction, attenuated |
| ramR → MDR χ² | 17.7 (p<0.0001) FOR | 37.6 (p=8.7e-10) **AGAINST** — reversed |
| 100% gyrA/soxRS/pmrAB | claimed | 0/68, 0/68, ≤5/68 — inflated by silent variants |
| Top AMR genes | tet, β-lact, qnrB19, fosA, aad/aph | mdsB/A (68), qnrB19 (31), fosA7.7 (21), tet(C) (13), sul1 (7), blaCARB-2 (7), aadA2 (7), tet(G) (6), floR (6) — matches |

## Verdict rollup

- **REPLICATED (5)**: C1 counts, C2 MLST, C3 SGI-1, C5 Typh MDR enrichment, C8 top AMR profile.
- **DIRECTIONAL (1)**: C4 GB-vs-LN MDR (same direction, weaker p).
- **NOT TESTED (1)**: C9 2400-isolate public comparison (data loaded, follow-up possible).
- **CONTRADICTED / DB-DEPENDENT (2)**: C6 ramR-MDR reversed; C7 100% mutation claims inflated.

**Score: 78/100 PARTIAL** — core biology holds; two divergences are database-generation artefacts, not paper-fatal errors.

## Compute resource notes

- All computation on `uicgpu` (Ubuntu, 255 cores, 2 TB RAM, A100 GPUs unused — pure CPU pipeline).
- Total wall-clock: <10 min (dominated by network I/O in `datasets download`).
- No paid API calls except LLM-judge (Argo GPT-5.2, free per Rick's Argo standing rule).
- No data leaves the tailnet; all raw compute on internal storage.
