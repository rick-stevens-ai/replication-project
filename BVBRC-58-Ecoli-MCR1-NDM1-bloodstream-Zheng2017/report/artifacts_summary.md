# Artifacts Summary — BVBRC-58 Zheng et al. 2017 Replication

**Root:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-58-Ecoli-MCR1-NDM1-bloodstream-Zheng2017/`

## Report layer (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical narrative replication report (Markdown source). |
| `REPORT.tex` | LaTeX rendition + dedicated Genuine Critique section. |
| `workflow.md` | Step-by-step reproducible pipeline (data → stats → MLST → AMR → typing → judge). |
| `artifacts_summary.md` | This file — inventory of all produced artifacts. |
| `failure_analysis.md` | Honest catalog of what did NOT reproduce and why. |
| `open_questions.json` | 5 truly open scientific questions arising from this replication. |

## Working substrate (`work/`)

| Path | Contents |
|---|---|
| `work/paper_fulltext.xml` | Europe PMC full-text XML for PMC5738369 (~82 KB). |
| `work/genomes/CP021202.fasta` .. `CP021210.fasta` | 9 GenBank replicon FASTAs re-downloaded via NCBI efetch (2 chromosomes + 7 plasmids). |
| `work/strains/EC1002.fasta`, `EC2474.fasta` | Per-strain concatenations (chr + plasmids) used as MLST/AMRFinderPlus input. |
| `work/genome_stats.py` | Biopython 1.87 script — length + GC% per replicon, Δ vs paper Table 1. |

## Evidence (`evidence/`)

| Artifact | Content | Reproduces |
|---|---|---|
| `evidence/evidence_genome_stats.json` | Per-replicon bp + GC%, Δbp vs paper (range −3 to +8 bp), ΔGC ≤0.5%. | **C1 + C2** ✅ |
| `evidence/mlst_results.tsv` | mlst 2.35.0 (`ecoli_achtman_4`): EC1002=ST405, EC2474=ST131 (7-allele profiles exact). | **C3** ✅ |
| `evidence/EC1002_amr.tsv` | AMRFinderPlus 3.12.8 (DB 2024-07-22.1) hits, contig-mapped: mcr-1.1 on CP021205; blaNDM-1 on CP021206; plus per-plasmid resistance gene set. | **C4** ✅ (partial) + **C6** ✅ |
| `evidence/EC2474_amr.tsv` | AMRFinderPlus hits: mcr-1.1 on CP021209; blaNDM-1 on CP021210; per-plasmid gene set. | **C4** ✅ (partial) + **C6** ✅ |
| `evidence/plasmidfinder_results.tsv` | blastn vs PlasmidFinder `enterobacteriales.fsa` (159 refs), pident ≥95% cov ≥60%: 7/7 replicon types match paper (IncA/C2→IncC, IncF→IncFII). | **C5** ✅ |
| `evidence/llm_judge_input.md` | Structured input to Argo `gpt-5.2` judge: paper claims + per-claim replication outputs. | (judge input) |
| `evidence/llm_judge_gpt52.md` | LLM-judge output: per-claim verdicts, coverage 5/6=83.3%, agreement ~85–90%, canonical **PARTIAL**. | (judge output) |

## Key numeric summary

| Metric | Value |
|---|---|
| Testable claims | 6 (C1–C6) |
| Claims fully reproduced | 5 (C1, C2, C3, C5, C6) |
| Claims partially reproduced | 1 (C4 — AMR inventory, database drift) |
| Genome length agreement | 0–8 bp across 9 replicons |
| GC agreement | ≤0.5% across 9 replicons |
| MLST agreement | 2/2 STs exact, 14/14 alleles exact |
| Replicon typing agreement | 7/7 plasmids |
| mcr-1 ↔ blaNDM-1 separate-plasmid check | 2/2 strains confirmed |
| LLM-judge coverage | 83.3% |
| LLM-judge agreement | ~85–90% |
| Canonical verdict | **PARTIAL (strong)** |

## Provenance / free-only stack

- No paid endpoints. LLM judge = Argo `gpt-5.2` (free tier, per standing rule).
- No BV-BRC job submission needed; deposited closed genomes are the correct substrate for C1–C6.
- All tools open-source (Biopython, mlst, AMRFinderPlus, blastn, PlasmidFinder DB).
- All genome data re-downloaded fresh from NCBI, not reused from paper supplements.
