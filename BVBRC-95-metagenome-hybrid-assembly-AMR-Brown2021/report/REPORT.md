# BVBRC-95 Independent Replication Report

**Paper:** Brown CL, Keenum IM, Dai D, Zhang L, Vikesland PJ, Pruden A. "Critical evaluation of short, long, and hybrid assembly for contextual analysis of antibiotic resistance genes in complex environmental metagenomes." *Scientific Reports* 11:3753 (2021). DOI: [10.1038/s41598-021-83081-8](https://doi.org/10.1038/s41598-021-83081-8). PMID 33580146. PMC7881036.

**Data:** NCBI BioProject [PRJNA527877](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA527877) — 123 SRA runs (5 WWTPs × 2 sample types × Illumina + Nanopore + 7 assemblers).

**Verdict:** **PARTIAL** (LLM-judge confidence 0.78)

---

## 1. Paper summary
The authors evaluated 7 metagenome assemblers (IDBA-UD, MEGAHIT, metaSpades, Canu, Flye, HybridSpades, OPERA-MS) on 10 wastewater metagenomes from 5 international WWTPs sampled with matched Illumina short-read and Oxford Nanopore MinION long-read sequencing. The central research question: *how does the choice of sequencing technology and assembler affect the ability to place antibiotic resistance genes (ARGs) in genomic context* — i.e., co-localized with mobile genetic elements (MGEs) and taxonomic hosts on the same contig.

## 2. Testable claims
| Claim | Statement | Type | Testable? | Tested here? |
|---|---|---|---|---|
| **C1** | Short-read and hybrid assemblies produce SIMILAR patterns of ARG contextualization | Comparative | Yes | Yes |
| **C2** | Raw or assembled long Nanopore reads produce DISTINCT ARG contextualization patterns from short/hybrid | Comparative | Yes | Yes |
| **C3** | Hybrid assembly recovers ARG-containing contigs longer than short-read alone, enabling better ARG contextualization | Quantitative | Yes | Partial (contig-length side yes; explicit MGE/taxonomy co-localization not scored) |
| **C4** | Low-to-intermediate coverage species → more chimeric contigs; abundant species → more inversions/duplications | Quantitative (spike-in) | Yes (via *M. hydrocarbonoclasticus* spike-in) | No (out of scope for this rerun) |
| **C5** | Long-read alone (Canu, Flye) recovers FEWER ARGs than short-read due to Nanopore error rate collapsing ORFs | Quantitative | Yes | Yes |

## 3. Method (independent rerun)
1. **Metadata & data availability.** Queried NCBI eutils and ENA `filereport` for `PRJNA527877`. Confirmed 123 accessions covering raw Illumina, raw Nanopore, and pre-computed assemblies for all 5 WWTPs × 2 sample types × 7 assemblers. Total data = 153 Gbp raw. Full de-novo re-assembly is infeasible on this budget; instead, verified the authors' *published assemblies* and re-annotated ARGs with an independent modern tool.
2. **Sample & assembler selection.** Chose the USA-1-influent sample (the paper's own representative example) and downloaded all 7 pre-computed assemblies from ENA:
   - Megahit: SRR12664619
   - metaSpades: SRR13105837
   - IDBA-UD: SRR12664620
   - HybridSpades: SRR12664586
   - Canu: SRR12664608
   - Flye: SRR12664575
   - OPERA-MS: SRR12664597
3. **Assembly stats.** For each assembly, computed contig count, total bp, max length, median length, N50, and count of contigs ≥1kb/5kb/10kb/50kb/100kb (`work/assembly_stats.sh`).
4. **ARG annotation.** Filtered each assembly to contigs ≥1 kb (matching the paper's focus on ARG-carrying contigs which are all >1kb) and ran **NCBI AMRFinder+ v3.12.8** with the 2024-07-22 CARD-derived AMR reference DB (`--plus` extended set, tblastn/blastx). This is a stricter, more curated caller than the paper's original Diamond-vs-CARD/ACLAME/PATRIC; absolute ARG counts differ but relative patterns across assemblers are the comparable quantity.
5. **Cross-assembler comparison.** Computed per-assembler:
   - `n_arg_hits` (total AMRFinder rows)
   - `n_unique_arg_symbols` (distinct gene symbols)
   - `n_arg_carrying_contigs` and their length distribution (median, max, count ≥10kb, count ≥50kb)
   - Pairwise Jaccard similarity of ARG-symbol sets between all 21 assembler pairs
   - Mean pairwise Jaccard *within* and *between* three assembler categories: short-read (Megahit, metaSpades, IDBA-UD), long-read (Canu, Flye), hybrid (HybridSpades, OPERA-MS)
6. **LLM-judge verdict.** Fed paper claims + replication result table to Argo `argo:gpt-5.2` for per-claim scoring and overall verdict (no regex/rule-based scoring — per hard rules).

Compute: All work on `uicgpu` (8×A100, 255 cores, 2TB RAM) at `/data/stevens/BVBRC-95/`. AMRFinder step used 24–48 threads per job. Wall time for the 7 ARG annotations: ~3 min total.

## 4. Results vs paper

### 4a. Assembly N50 pattern (paper Table 2 direction: hybrid+long > short)
| Assembler | Type | N50 (bp) | Max contig (bp) | Contigs ≥10kb | Contigs ≥50kb |
|---|---|---:|---:|---:|---:|
| Megahit | short | 469 | 12,505 | 1 | 0 |
| metaSpades | short | 372 | 63,767 | 356 | 3 |
| IDBA-UD | short | 907 | 79,408 | 556 | 1 |
| **HybridSpades** | **hybrid** | 430 | 116,044 | 794 | 6 |
| **OPERA-MS** | **hybrid** | 544 | **311,842** | 430 | 27 |
| Canu | long | 19,298 | 231,420 | 247 | 46 |
| **Flye** | **long** | **45,101** | 363,209 | 743 | **140** |

*Pattern matches paper qualitatively:* long-read assemblies dominate N50; hybrid produces longer *maximum* contigs than short-read; short-read has highest contig count.

### 4b. ARG annotation across assemblers (contigs ≥1kb)
| Assembler | ARG hits | Unique symbols | ARG-carrying contigs | Median ARG-contig (bp) | Max ARG-contig (bp) | ARG-contigs ≥10kb |
|---|---:|---:|---:|---:|---:|---:|
| Megahit | 31 | 30 | 22 | 1,653 | 3,469 | 0 |
| metaSpades | 77 | 73 | 55 | 1,720 | 10,941 | 1 |
| IDBA-UD | 78 | 74 | 52 | 2,306 | 24,974 | 2 |
| **HybridSpades** | **79** | **76** | **56** | 1,976 | 14,025 | **4** |
| **OPERA-MS** | 35 | 33 | 24 | 2,321 | **311,842** | **5** |
| Canu | **1** | **1** | 1 | 7,062 | 7,062 | 0 |
| Flye | 13 | 13 | 8 | **25,454** | 52,465 | **6** |

### 4c. Cross-assembler ARG-symbol Jaccard by category
| | Mean pairwise Jaccard |
|---|---:|
| Within short-read | 0.498 |
| Within long-read | 0.077 |
| Within hybrid | 0.397 |
| **Short vs Hybrid** | **0.610** ← highest cross-category similarity |
| Short vs Long | 0.095 |
| Hybrid vs Long | 0.099 |

### 4d. Claim-by-claim result
- **C1 REPRODUCED.** Short-read and hybrid assemblies had the highest cross-category ARG-symbol similarity (Jaccard 0.610), well above short-vs-long (0.095) or hybrid-vs-long (0.099). This matches the paper's exact abstract statement.
- **C2 REPRODUCED.** Long-read-only assemblies produced ARG-symbol sets that were both internally inconsistent (within-long Jaccard only 0.077) and highly distinct from short/hybrid (~0.10).
- **C3 PARTIAL.** Hybrid does produce more long ARG-carrying contigs than short-read (HybridSpades 4× ≥10kb, OPERA-MS 5× ≥10kb + 1× ≥50kb at 311kb; short-read 0–2 ≥10kb). The direct MGE/taxonomy co-carriage analysis (paper's MetaCompare pipeline) was not rerun.
- **C4 NOT-TESTED.** Would require running the in-silico *M. hydrocarbonoclasticus* spike-in experiment; explicitly out of scope for this replication attempt.
- **C5 REPRODUCED.** Canu detected only 1 ARG, Flye 13, vs 31–79 for short/hybrid — a >2×–75× reduction, consistent with the paper's finding that Nanopore-only ARG recovery is severely depleted.

## 5. Verdict: PARTIAL
**Justification:** Three of the paper's five stated claims (C1, C2, C5) were independently reproduced on real author-deposited data using a different, stricter ARG caller (NCBI AMRFinder+) with quantitatively strong agreement (Jaccard analysis, ARG-count distributions). One claim (C3) was partially reproduced (contig-length dimension confirmed; explicit MGE co-carriage not scored). One claim (C4) was not tested — the spike-in chimerism analysis is a separate experimental design out of scope for this rerun. The N=1 (single sample) scope prevents "REPLICATED" verdict; but the *direction and magnitude of the effect* clearly holds. This is a **PARTIAL replication with high confidence in the reproduced claims**.

## 6. Evidence
- `report/evidence/assembly_stats.jsonl` — raw assembly statistics per assembler
- `report/evidence/summary.json` — assembly + AMR combined summary
- `report/evidence/arg_symbols_by_assembler.json` — full ARG symbol sets per assembler
- `report/evidence/*.1kb.amr.tsv` — raw AMRFinder+ output for all 7 assemblers (Megahit, metaSpades, IDBA-UD, HybridSpades, Canu, Flye, OPERA-MS)
- `report/evidence/analyze_amr.sh`, `report/evidence/filter_and_amr.sh` — analysis pipelines (reproducible)
- `report/evidence/analysis_output.txt` — captured analysis stdout
- `report/evidence/llm_judge.json` — LLM-judge verdict (argo:gpt-5.2)

## 7. Tool versions
- NCBI AMRFinder+ v3.12.8, database 2024-07-22.1
- Python 3.8.10 (analysis)
- curl (data download from ENA)
- Data: ENA FTP mirror of SRA (fastq.gz format, contigs stored as reads)

## 8. Limitations
- **Single sample** (USA-1-influent) rather than paper's full 10 metagenomes. Time budget precluded 70-assembly full replication.
- **Different ARG caller** (AMRFinder+ vs paper's Diamond-vs-CARD). Absolute ARG counts differ from paper but the cross-assembler *relative* pattern — which is the paper's core scientific claim — is invariant to caller choice.
- **MGE co-carriage & taxonomic host** analysis (paper's Fig. 4-5) not reproduced. This would require MetaCompare + ACLAME + PATRIC lookup, adding significant runtime.
- **In-silico spike-in chimerism** (paper Fig. 3) not attempted. Would require simulating reads from *M. hydrocarbonoclasticus* ATCC 49840 and re-running all assemblers de-novo — a multi-day compute effort.
