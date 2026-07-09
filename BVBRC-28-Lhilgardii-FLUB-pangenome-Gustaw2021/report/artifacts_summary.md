# Artifacts Summary — BVBRC-28 (Gustaw 2021 *L. hilgardii* FLUB Pangenome)

**Verdict:** PARTIAL REPLICATION (strong; borderline REPLICATED).
**Coverage:** 6/6 paper claims addressed (C6 indirectly via ANI); 7/7 in the consolidated LLM-judge pass.
**Agreement:** 0 contradictions. 4 AGREE / 3 PARTIAL / 0 DISAGREE (consolidated).

---

## Report artifacts (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Human-readable Markdown report (initial + cross-validation pass). |
| `REPORT.tex` | LaTeX version with dedicated *Genuine Critique* section. |
| `open_questions.json` | 5 truly open follow-up questions grounded in the paper's biology. |
| `workflow.md` | End-to-end pipeline recipe + data-flow diagram. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | What did not replicate and why. |

---

## Evidence artifacts (`evidence/`)

### C1 — Genome statistics (EXACT MATCH)
| File | Content |
|---|---|
| `genome_stats.json` | Total length, contig count, GC%, N50 for all 6 assemblies; per-replicon lengths for FLUB. |

**Headline numbers:** FLUB total 3,190,226 bp (= paper exactly); chromosome CP047121.1 = 3,071,102 bp; five plasmids CP047122–126.1 = 42,732 / 37,669 / 28,299 / 6,896 / 3,528 bp (every replicon matches Table 1 to the base pair); G+C 40.09% (= paper exactly).

### C2 — Annotation
| File | Content |
|---|---|
| `cds_counts.txt` | Per-genome Prokka CDS counts. |

**Headline numbers:** FLUB Prokka CDS = 2991 (vs. paper PGAP+PATRIC 2871; ~4% delta, expected pipeline difference). "FLUB richest CDS" preserved qualitatively (2991 > 2707 ≥ others).

### C3, C4 — Pangenome (two independent pipelines)
| File | Content |
|---|---|
| `roary5_summary.txt` | Roary results on the 5-genome paper-equivalent set. |
| `roary6_summary.txt` | Roary results on the 6-genome set. |
| `pangenome5_uniq.txt` | Per-strain singleton counts (Roary 5). |
| `pangenome6_uniq.txt` | Per-strain singleton counts (Roary 6). |
| `mmseqs_clusters.tsv` | mmseqs2 cluster table (pipeline 2). |
| `pangenome_result.json` | Consolidated partition + singletons (pipeline 2). |

**Headline numbers:**
- Total pan clusters: paper 4181 vs. Roary 4089 vs. mmseqs2 4190 (paper *between* the two pipelines).
- Core fraction: paper 49.3% vs. Roary 48.9% vs. mmseqs2 45.9%.
- FLUB singletons: paper 266 vs. Roary5 268 vs. Roary6 269 vs. mmseqs2 260 (three independent numbers within ±3 of the paper).
- Per-strain singleton rank order (LMG 07934 > FLUB > others) matches the paper.

### C5 — Whole-genome ANI
| File | Content |
|---|---|
| `fastani_all.tsv` | fastANI all-vs-all over 6 genomes. |

**Headline numbers:** FLUB ↔ ATCC 27305 = 99.77% (paper 99.909%; closest-neighbor structure reproduced). FLUB ↔ {ATCC 8290, DSM 20176, LH500, LMG 07934} = 96.86–97.09%. All pairs conspecific (≥95% species threshold). One marginal pair sits at 96.86% (just under the paper's stated ≥97% floor; inside fastANI method variance).

### C_phylo — Core-genome ML tree (cross-validation, maps to paper's PATRIC Codon Tree)
| File | Content |
|---|---|
| `core_genome.nwk` | Newick topology: `(LH500,DSM20176,(LMG07934,(FLUB,MGYG)));` |
| `core_tree_result.json` | 400-gene single-copy-core supermatrix stats (125,120 aa), pairwise core-proteome identities. |

**Headline:** FLUB and MGYG-HGUT-01333 are sisters (core-proteome identity 99.97%); LMG 07934 next. Exactly matches the paper's PATRIC Codon Tree relationship.

### Verdict artifacts
| File | Content |
|---|---|
| `llm_judge_response.json` | Pass 1 Argo gpt-5.2 verdict (PARTIAL; 2 agree / 4 partial / 0 disagree; coverage 6/6). |
| `llm_judge_consolidated.json` | Consolidated verdict after cross-validation (REPLICATED; 4 agree / 3 partial / 0 disagree; coverage 7/7). |

---

## Work / code artifacts (`work/`)

| File | Purpose |
|---|---|
| `gstats.py` | Total length + GC% + N50 per assembly. |
| `genome_stats.py` | Per-replicon parser (Biopython) for exact-match verification of Table 1. |
| `pangenome.sh` | Prodigal + mmseqs2 driver (pipeline 2). |
| `pangenome_analyze.py` | Partition analyzer for the mmseqs cluster table. |
| `coregenome_tree.py` | Single-copy-core extractor + MAFFT alignment + concat + FastTree driver. |
| `uniq.py` | Roary `gene_presence_absence.csv` singleton counter. |
| `attempt_log` | Chronological record including the Perl `File::Find::Rule` 5.22-vs-5.26 fix. |

---

## Input data provenance

| Source | Objects | Auth |
|---|---|---|
| NCBI Datasets v2alpha REST | GCF_009832765.1, GCF_004354795.1, GCF_001434655.1, GCF_011765585.1, GCF_000159175.1, GCF_008694025.1 | None (free). |
| ENA browser API | MGYG-HGUT-01333 FASTA (no GCA sequence via NCBI). | None (free). |
| Europe PMC REST | Full-text XML + accessions from the paper. | None (free). |

---

## Compute footprint

- **Host:** uicgpu (8×A100; only CPU used).
- **Wall clock:** ~15 min total (Prokka × 6 dominates at ~6 min; Roary 5-genome ~3 min; mmseqs2 clustering ~1 min; MAFFT alignments ~2 min; everything else <1 min).
- **Cost:** $0 (all free public services + local compute + Argo proxy on `localhost:44497`).
