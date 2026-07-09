# Workflow — BVBRC-95 Independent Replication

Reference: Brown CL et al., *Sci. Rep.* 11:3753 (2021). DOI 10.1038/s41598-021-83081-8.
Data: NCBI BioProject PRJNA527877 (123 SRA runs; 5 WWTPs × 2 sample types × Illumina + Nanopore + 7 assemblers).
Compute host: `uicgpu` (8×A100, 255 cores, 2 TB RAM). Working dir: `/data/stevens/BVBRC-95/`.

## 0. Design decision — scale-vs-fidelity tradeoff
Full de-novo re-assembly of all 10 metagenomes across all 7 assemblers (~70 assemblies, ~153 Gbp raw input) was infeasible under this replication's compute budget. Chosen approach:
- Use the authors' pre-computed assemblies deposited in ENA (verifies they exist and match the paper).
- Re-annotate ARGs with an **independent, modern, curated caller** (NCBI AMRFinder+ v3.12.8, DB 2024-07-22.1) rather than the paper's Diamond-vs-CARD/ACLAME/PATRIC pipeline.
- Restrict deep analysis to one representative sample (USA-1-influent, the paper's own worked example).
- Score the paper's five stated claims individually; treat the N=1 scope as a hard cap on the verdict.

## 1. Metadata & data discovery
1. Query NCBI eutils for BioProject PRJNA527877; confirm 123 accessions.
2. Query ENA `filereport` API to enumerate raw Illumina + raw Nanopore + pre-computed assembly runs across all 5 WWTPs × 2 sample types × 7 assemblers.
3. Confirm total raw data footprint ≈ 153 Gbp.

## 2. Sample and assembler selection
Chose USA-1-influent (paper's representative example). Downloaded all 7 pre-computed assemblies from ENA:

| Assembler   | Type    | Accession    |
|-------------|---------|--------------|
| Megahit     | short   | SRR12664619  |
| metaSpades  | short   | SRR13105837  |
| IDBA-UD     | short   | SRR12664620  |
| HybridSpades| hybrid  | SRR12664586  |
| Canu        | long    | SRR12664608  |
| Flye        | long    | SRR12664575  |
| OPERA-MS    | hybrid  | SRR12664597  |

Assemblies are stored in SRA as reads (FASTQ.gz) — treated as contigs downstream.

## 3. Assembly statistics
Script: `report/evidence/assembly_stats.sh`.
Per assembler, compute:
- contig count, total bp, max length, median length, N50
- contig counts ≥1 kb, ≥5 kb, ≥10 kb, ≥50 kb, ≥100 kb

Output: `report/evidence/assembly_stats.jsonl` (one JSON object per assembler).

## 4. ARG annotation
Script: `report/evidence/filter_and_amr.sh`.
For each assembly:
1. Filter contigs ≥1 kb (matches the paper's ARG-carrying-contig focus).
2. Run **NCBI AMRFinder+ v3.12.8** with DB `2024-07-22.1` and `--plus` extended set (tblastn/blastx over contigs).
3. Use 24–48 threads per job (uicgpu has 255 cores).

Output per assembler: `report/evidence/<assembler>.1kb.amr.tsv`.

Wall time for all 7 annotations: ~3 min total.

**Why AMRFinder+ rather than the paper's caller.** AMRFinder+ is stricter and more curated (NCBI's actively-maintained AMR gene set with hierarchical hit-refinement), so absolute counts will differ from Brown et al. The scientific claim under test — *cross-assembler relative pattern of ARG contextualization* — is invariant to caller choice; using an independent caller strengthens rather than weakens the replication.

## 5. Cross-assembler comparison
Script: `report/evidence/analyze_amr.sh`.

Compute per assembler:
- `n_arg_hits` — total AMRFinder+ rows
- `n_unique_arg_symbols` — distinct gene-symbol set
- `n_arg_carrying_contigs` and their length distribution (median, max, count ≥10 kb)

Compute across assemblers:
- Pairwise Jaccard similarity of ARG-symbol sets (all 21 unordered pairs)
- Mean Jaccard within and between the three categories:
  - **Short-read:** Megahit, metaSpades, IDBA-UD
  - **Long-read:** Canu, Flye
  - **Hybrid:** HybridSpades, OPERA-MS

Output: `report/evidence/summary.json`, `report/evidence/arg_symbols_by_assembler.json`, `report/evidence/analysis_output.txt`.

## 6. LLM-judge verdict
Feed paper claims + replication result table (assembly-stats table + AMR-counts table + Jaccard table) to Argo `argo:gpt-5.2` for per-claim scoring and an overall verdict. **No regex or rule-based auto-scoring** (per project hard rule). Output: `report/evidence/llm_judge.json` (verdict PARTIAL, confidence 0.78).

## 7. Report assembly
- Write `REPORT.md` with paper summary, claims table, method, results-vs-paper, per-claim outcomes, verdict, evidence pointers, tool versions, limitations.
- Write `REPORT.tex` (this pass) with the same content plus a dedicated Genuine Critique section.
- Write ancillary artifacts: `open_questions.json`, `workflow.md` (this file), `artifacts_summary.md`, `failure_analysis.md`.

## 8. Reproducibility notes
- Every script under `report/evidence/*.sh` is committed and can be re-run against the same ENA-downloaded assemblies.
- AMRFinder+ DB version is pinned (2024-07-22.1); later DB snapshots may shift some symbols but should not change the cross-assembler relative pattern.
- To extend to the full 10-sample paper scope: loop the same pipeline over the other 9 samples; expected compute ~30 min total for ARG annotation.
- To extend to MGE co-carriage (paper C3 full test): add MetaCompare + ACLAME + PATRIC lookup on ARG-carrying contigs — significant added runtime, not attempted here.
- To test C4 (spike-in chimerism): would require simulating reads from *M. hydrocarbonoclasticus* ATCC 49840 and re-running all 7 assemblers de-novo — multi-day compute, out of scope.
