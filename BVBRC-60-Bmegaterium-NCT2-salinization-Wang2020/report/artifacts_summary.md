# Artifacts summary — BVBRC-60 (Priestia megaterium NCT-2, Wang et al. 2020)

Paper: doi:10.1155/2020/4109186 · PMID 32190639 · PMCID PMC7066406
Assembly: GCA_000334875.3 (ASM33487v3, Complete Genome; 11 replicons)
Verdict: **REPLICATED** (coverage 1.00, agreement 1.00)

---

## Top-level report files

| Path (under `report/`) | Purpose |
|---|---|
| `REPORT.md` | Human-readable replication report (markdown). Canonical narrative. |
| `REPORT.tex` | LaTeX version of `REPORT.md` + dedicated "Genuine Critique" section stating the limits of what the replication actually establishes. |
| `workflow.md` | Step-by-step method: data acquisition, computation, tools, versions, reproducibility surface. |
| `artifacts_summary.md` | This file — index of every artifact and where it lives. |
| `failure_analysis.md` | What did not go smoothly / what would have failed the run. |
| `open_questions.json` | Five truly open biological/experimental questions grounded in the NCT-2 salinization phenotype that this replication does *not* answer. |

## Evidence artifacts (under `report/evidence/`)

| File | Source step (see `workflow.md`) | Contents |
|---|---|---|
| `genome_stats.json` | Step 3 | Per-replicon length + GC (11 records) and whole-genome totals for GCA_000334875.3. Supports C1 (architecture) and C2 (GC). |
| `annotation_counts.json` | Step 4 | Feature-type tally from `genomic.gff`: gene / CDS / tRNA / rRNA / pseudogene counts; protein count from `protein.faa`. Supports C3 (annotation totals). |
| `comparative_genome_table.tsv` | Step 5 | Size + GC for NCT-2 and the paper's five Table-1 comparators, computed identically from downloaded FASTAs. Supports C4 (comparative table). |
| `ani_nct2_vs_comparators.tsv` | Step 6 | fastANI output: NCT-2 query vs 5 comparator references. Supports C5 (phylogenetic ordering). |
| `functional_genes_found.txt` | Step 7 | grep hits of paper-claimed functional inventories (N-metabolism, phosphate, IAA, stress/osmoadaptation) against deposited protein-product strings. Supports C6 (gene inventories). |
| `llm_judge_verdict.txt` | Step 8 | LLM (Argo gpt-5.2) adjudication over the machine-produced claim/result JSON. Emits final REPLICATED label. |

## Upstream (not stored in-repo; re-fetchable from public sources)

| Item | Where | Auth | Cost |
|---|---|---|---|
| Paper full-text XML | Europe PMC (PMC7066406) | none | free |
| Study genome bundle (`genomic.fna`, `genomic.gff`, `protein.faa`) | NCBI Datasets v2 REST, accession GCA_000334875.3 | none | free |
| 5 comparator genome bundles | NCBI Datasets v2 REST (QM B1551, DSM 319, *B. subtilis* 168, *B. cereus* Q1, *B. licheniformis* DSM 13) | none | free |
| `fastANI` binary | `/usr/local/bin/fastANI` on the local host | n/a | free |

Upstream bundles are intentionally not committed — everything is deterministically re-fetchable from the accessions in `workflow.md`.

## Claim → artifact mapping

| Claim | Type | Artifact(s) supporting it |
|---|---|---|
| C1 architecture (1 chr + 10 plasmids, 5.88 Mb) | genome | `genome_stats.json` |
| C2 GC content (37.87% whole, 38.2% chr, 33.7–37.0% plasmid) | sequence stat | `genome_stats.json` |
| C3 annotation totals (6039 genes / 5606 CDS / 203 RNA / 230 pseudo / 142 tRNA / 53 rRNA) | annotation | `annotation_counts.json` |
| C4 6-strain comparative table; NCT-2 largest | comparative | `comparative_genome_table.tsv` |
| C5 phylogeny: closest DSM 319 then QM B1551 | phylogeny | `ani_nct2_vs_comparators.tsv` |
| C6 functional inventories (N / phosphate / IAA / stress) | functional | `functional_genes_found.txt` |
| C7 wet-lab provenance + hybrid sequencing workflow | provenance | not testable from deposit alone |

## Agreement snapshot

- 6/6 testable claims tested (coverage 1.00).
- 6/6 AGREE or MINOR-DIFF (agreement 1.00).
- Largest numeric offset: whole-genome GC 37.87% (paper) vs 37.78% (reproduced) = 0.09% absolute, a rounding-level difference consistent with the paper's original v.1 annotation vs the current v.3 assembly.
- Discrete-count deltas: 1 gene (6039 vs 6038) and 1 protein (5606 vs 5605); RNA / pseudogene / tRNA / rRNA subcounts exact.

## What is *not* in the artifact set (by design)

- No wet-lab data (Wang et al. did not deposit strains, cultures, or phenotype measurements; C7 is inherently non-testable from deposition).
- No expression / transcriptomic data (C6 is presence-only, not activity).
- No plasmid-partition analysis of the functional inventories (open question O3 in `open_questions.json`).
- No modern-pangenome comparator set (open question O5 in `open_questions.json`); the replication inherits the paper's 5-strain comparator choice.
