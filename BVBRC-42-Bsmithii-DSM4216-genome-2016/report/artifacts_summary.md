# Artifacts summary — BVBRC-42 *B. smithii* DSM 4216ᵀ (Bosma et al., 2016)

Verdict: **PARTIAL REPLICATION (strong, independently confirmed)**.

## Top-level report files
| Path | Purpose |
|---|---|
| `report/REPORT.md` | Human-readable replication report (canonical source of all numbers). |
| `report/REPORT.tex` | LaTeX version with dedicated GENUINE CRITIQUE section. |
| `report/brief.md` | Short-form summary of the replication. |
| `report/attempt_log.md` | Chronological log of steps attempted (successes + failures). |
| `report/artifact_harvest.md` | Inventory of downloaded / regenerated artifacts. |
| `report/workflow.md` | Step-by-step reproduction workflow. |
| `report/failure_analysis.md` | Honest post-mortem of what didn't reproduce and why. |
| `report/open_questions.json` | Five truly-open biological questions grounded in this replication. |

## Evidence (primary replication)
Directory: `report/evidence/`

| File | What it contains |
|---|---|
| `genome_stats.json` | Per-replicon length + GC + feature counts for both GCA (2015) and GCF (2026 RefSeq) assemblies. Tests C2–C5. |
| `func_scan.json` | Annotation name-scan for the Fig. 4 metabolic gene panel across GCA + GCF GFFs. Orthogonal check for C7–C10. |
| `metabolic_tblastn.tsv` | Full tblastn output for 8 curated UniProt reference enzymes vs the *B. smithii* genome. Primary evidence for C7–C10. |
| `cog_compare.json` | Pearson/Spearman comparison of paper Table 5 vs COGclassifier v2 categorisation. Reports all-22-cat and excl-D/R/S variants. |
| `cog_count.tsv` | COGclassifier category counts on the GCA proteome. |
| `cog_count_barchart.png` | COG distribution figure (paper vs re-run). |

## Evidence (independent reproduction, 2026-07-03)
Directory: `report/evidence/independent_reproduction/`

| Path | What it contains |
|---|---|
| `downloads/GCA_001050115.1/` | Fresh NCBI Datasets zip, unpacked (FASTA + GFF + protein.faa) — original 2015 GenBank submission. |
| `downloads/GCF_001050115.1/` | Fresh NCBI Datasets zip, unpacked — 2026 RefSeq PGAP re-annotation. |
| `downloads/refs/indep_refs.faa` | 7 UniProt reference enzymes re-downloaded fresh from UniProt REST. |
| `downloads/blast/bsmithii_indep_db.*` | Fresh BLAST nucleotide DB built from newly-downloaded genome. |
| `downloads/blast/indep_tblastn.tsv` | Fresh `tblastn -evalue 10 -outfmt 6` output (52 HSPs total). |
| `downloads/indep_stats_GCA.json` | Independent genome-stat JSON for GCA. |
| `downloads/indep_stats_GCF.json` | Independent genome-stat JSON for GCF. |
| `code/indep_genome_stats.py` | Own genome-stats script (pure stdlib, does NOT read the original `work/genome_stats.py`). |
| `code/indep_fetch_refs.py` | Own UniProt reference-fetch script. |
| `code/build_summary.py` | Own summariser that produces the comparison JSON + markdown. |
| `indep_summary.json` | Full comparison of paper reported vs independently re-computed for all 15 metrics. |
| `comparison.md` | Rendered comparison table (15/15 MATCH, 0 MISMATCH). |
| `tool_versions.txt` | Versions of NCBI `datasets` CLI, BLAST+, Python. |

## Work / intermediate artifacts
Directory: `work/`

| Path | What it contains |
|---|---|
| `paper_fulltext.xml` | Europe PMC JATS full-text XML of PMC4995803. |
| `genome/GCA_001050115.1/` | Original assembly download (genome/protein/gff/cds). |
| `genome/GCF_001050115.1/` | RefSeq re-annotation download. |
| `genome_stats.py` | Primary genome-stats script (used by original replication). |
| `func_scan.py` | Metabolic gene name-scan script. |
| `fetch_refs.py` | UniProt reference-enzyme fetcher (8 refs). |
| `judge.py` | LLM-judge driver (Argo `argo:gpt-5.2`, temp 0). |
| `blast/refs.faa` | 8 curated reference enzymes for tblastn. |
| `blast/bsmithii_db.*` | Nucleotide BLAST DB. |
| `blast/refs_tblastn.tsv` | Primary tblastn output. |
| `cog_out/` | Full COGclassifier v2 output directory. |
| `judge_result.json` | Structured JSON verdict from the LLM-judge. |

## What is NOT in artifacts (out of scope, per GENUINE CRITIQUE)
- RAST manual-curation intermediate files (paper-specific, not reproduced).
- antiSMASH cluster GBK/GenBank output (out of scope).
- CRISPR-finder outputs (out of scope).
- InterPro domainome / EC-rescue tables (out of scope).
- Table 6 comparative-genomics vs 14 other Bacillus/Geobacillus (not re-run).
- Fig. 4 metabolism map (paper's manual figure not redrawn).
- Wet-lab validation (in-silico only).

## Reproducibility guarantee
Everything under `report/evidence/` and `work/` regenerates from public NCBI + Europe PMC + UniProt with the commands in `workflow.md` — zero paid endpoints, deterministic, ~2 min CPU + fresh downloads. The independent reproduction directory demonstrates this on a fresh subagent with own code.
