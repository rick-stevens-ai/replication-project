# Artifacts Summary — BVBRC-95 Independent Replication

All artifacts live under `report/` in this replication package. Verdict: **PARTIAL** (LLM-judge confidence 0.78).

## Primary report artifacts
| File | Purpose |
|---|---|
| `REPORT.md` | Human-readable narrative replication report (paper summary, claims, method, results, verdict, evidence pointers, limitations) |
| `REPORT.tex` | LaTeX version of the same report plus a dedicated Genuine Critique section |
| `workflow.md` | Step-by-step pipeline documentation (design decision → data → assemblies → ARG annotation → cross-comparison → judge → report) |
| `open_questions.json` | Five truly open follow-up questions grounded in the paper's findings and this replication's gaps, with basis + concrete next steps |
| `artifacts_summary.md` | This file — inventory + role of every deposited artifact |
| `failure_analysis.md` | Honest catalog of what was skipped, why, and what would be required to close each gap |

## Evidence artifacts (under `report/evidence/`)
| File | Content |
|---|---|
| `assembly_stats.jsonl` | Per-assembler assembly statistics: contig count, total bp, max length, median length, N50, contigs ≥1/5/10/50/100 kb |
| `summary.json` | Combined assembly + ARG summary (one JSON object per assembler) |
| `arg_symbols_by_assembler.json` | Full ARG gene-symbol set (as detected by AMRFinder+) per assembler |
| `megahit.1kb.amr.tsv` | Raw NCBI AMRFinder+ v3.12.8 output on Megahit contigs ≥1 kb |
| `metaspades.1kb.amr.tsv` | Raw AMRFinder+ output on metaSpades contigs ≥1 kb |
| `idba-ud.1kb.amr.tsv` | Raw AMRFinder+ output on IDBA-UD contigs ≥1 kb |
| `hybridspades.1kb.amr.tsv` | Raw AMRFinder+ output on HybridSpades contigs ≥1 kb |
| `canu.1kb.amr.tsv` | Raw AMRFinder+ output on Canu contigs ≥1 kb |
| `flye.1kb.amr.tsv` | Raw AMRFinder+ output on Flye contigs ≥1 kb |
| `opera-ms.1kb.amr.tsv` | Raw AMRFinder+ output on OPERA-MS contigs ≥1 kb |
| `filter_and_amr.sh` | Executable pipeline: filter contigs ≥1 kb → AMRFinder+ |
| `analyze_amr.sh` | Executable pipeline: aggregate per-assembler stats + compute pairwise Jaccard |
| `analysis_output.txt` | Captured stdout of the analysis pipeline |
| `llm_judge.json` | LLM-judge verdict (Argo `argo:gpt-5.2`) — per-claim scores + overall verdict + confidence |

## Headline quantitative findings (all traceable to files above)

**N50 pattern (paper Table 2 direction):** long > hybrid > short.
- Flye N50 = 45,101 bp; Canu N50 = 19,298 bp.
- OPERA-MS max contig = 311,842 bp (also carries an ARG).
- Short-read (Megahit / metaSpades / IDBA-UD) N50 = 372–907 bp.

**ARG counts (contigs ≥1 kb):**
- Short: Megahit 31, metaSpades 77, IDBA-UD 78.
- Hybrid: HybridSpades 79 (max), OPERA-MS 35.
- Long: Canu 1, Flye 13.

**Cross-assembler ARG-symbol Jaccard by category:**
- Short vs Hybrid = **0.610** (highest cross-category — matches paper C1).
- Short vs Long = 0.095; Hybrid vs Long = 0.099 (matches paper C2).
- Within-long = 0.077 (long assemblers disagree even with each other).

**Long-read ARG depletion (paper C5):**
- Canu 1 ARG vs Megahit 31 (>30× reduction).
- Flye 13 ARGs vs HybridSpades 79 (>6× reduction).

## Claim outcomes (traceable to `llm_judge.json` and the tables above)
| ID | Outcome |
|---|---|
| C1 | REPRODUCED |
| C2 | REPRODUCED |
| C3 | PARTIAL (contig-length side confirmed; explicit MGE co-carriage not scored) |
| C4 | NOT-TESTED (spike-in out of scope) |
| C5 | REPRODUCED |

## Tool versions
- NCBI AMRFinder+ v3.12.8, database 2024-07-22.1
- Python 3.8.10 (analysis scripts)
- curl (ENA data download)
- Argo `argo:gpt-5.2` (LLM-judge)
- Compute: uicgpu (8×A100, 255 cores, 2 TB RAM)

## Provenance
All source assemblies downloaded from ENA (mirror of NCBI SRA under BioProject PRJNA527877). Every processing step is captured in an executable shell script under `report/evidence/` so the analysis can be re-run bit-identically against the same inputs.
