# Artifacts Summary — BVBRC-29

## Report files (`report/`)
| File | Purpose |
|---|---|
| `REPORT.md` | Original narrative replication report (Markdown), PARTIAL verdict. |
| `REPORT.tex` | LaTeX version of REPORT.md with a full honest Critique section; includes `\input{open_questions_section.tex}`. |
| `open_questions.json` | Bare JSON list of 5 open questions (q / basis / next_steps schema). |
| `open_questions_section.tex` | LaTeX rendering of the 5 open questions with concrete uicgpu-scoped next-step probes. |
| `workflow.md` | Stage-by-stage pipeline documentation (paper → download → Prokka → Roary → FastTree → LLM judge). |
| `failure_analysis.md` | Honest critique: what was done vs paper headline, what was NOT done, PARTIAL-verdict rationale. |
| `artifacts_summary.md` | This file. |
| `brief.md` | Task brief / claims extraction working notes. |
| `attempt_log.md` | Chronological attempt log. |
| `artifact_harvest.md` | Notes on what evidence was harvested from each pipeline stage. |

## Evidence artifacts (`report/evidence/`)
| File | Contents |
|---|---|
| `accessions.txt` | 27 GCF accessions selected for the replication (seeded from paper Table 1). |
| `genome_stats.csv` | Per-genome length, GC%, N50, contig count. Flags for partial assembly / GC outlier. |
| `mash_dist.tsv` | All-vs-all Mash distances (k=21, s=1000, 729 pairs). |
| `fastani_out.tsv` | All-vs-all FastANI output (627 usable pairs). |
| `ani_summary.txt` | Summary stats: anthracis intra-clonality; anthracis-vs-cereus/thuringiensis ANI; group ANI distribution. |
| `roary_full27_summary.txt` | Run A (27 genomes, i95, cd99): Pan 48,118 / Core 0. |
| `roary_i80_26genomes_summary.txt` | Run B (26 genomes, i80, cd99): Pan 26,839 / Core 251. |
| `roary_clade1_summary.txt` | Run C (17 Clade-1 subset, i95, cd99): Pan 15,247 / Core 2,415. |
| `panacc_clade1_pan.Rtab` | Pan-genome accumulation curve data (permutation). |
| `panacc_clade1_core.Rtab` | Core-gene accumulation curve data. |
| `panacc_clade1_new.Rtab` | New-genes-per-added-genome curve data. |
| `core_gene_tree_clade1.nwk` | FastTree GTR nucleotide tree on Clade-1 core-gene concatenation. |
| `accessory_binary_tree_clade1.nwk` | Roary accessory-gene presence/absence binary tree. |
| `llm_judge_prompt.py` | Argo-proxy LLM-judge script (retry + model fallback). |
| `llm_judge_verdict.json` | Raw judge output (JSON): overall PARTIAL, per-claim breakdown. |
| `llm_judge_verdict_pretty.json` | Pretty-printed version for humans. |

## Working directory (`work/`)
| File | Contents |
|---|---|
| `bazinet2017.pdf` | Paper PDF. |
| `bazinet2017.txt` | Text extraction. |

## Extraction (`extraction/`) — backfill
| File | Contents |
|---|---|
| `nougat.mmd` | Nougat-format MMD stub for the paper (backfill placeholder; original tables/figures indexed by claim). |

## Verdict
- **PARTIAL (solid).** Biological headlines (C3, C4, C6) reproduced; quantitative headlines (C1, C2) reproduced to correct order of magnitude at reduced scale; topological headline (C5) reproduced at subset level. Independent LLM judge concurred (Argo `gpt-5.2` after `claude-opus-4.8` 502s).
- Verdict cross-check: **PARTIAL preserved**. Headline-exercised only for the biological claims; scale + Scoary + hierBAPS + RAxML-bootstrap not exercised. See `failure_analysis.md` for full breakdown.
