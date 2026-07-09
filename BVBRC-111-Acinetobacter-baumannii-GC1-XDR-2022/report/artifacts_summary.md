# BVBRC-111 — Artifact inventory

Everything on disk for this replication, with provenance and where practical a size or checksum note. Paths are relative to the replication dir `~/Dropbox/REPLICATE-PROJECT/BVBRC-111-Acinetobacter-baumannii-GC1-XDR-2022/` unless noted.

## Primary source (paper)

| Artifact | Path | Status | Notes |
|---|---|---|---|
| Paper PDF | `paper.pdf` | **MISSING** (see `paper.pdf.MISSING.md` if present) | OUP/EuropePMC/NCBI-PMC all failed non-interactively; paper not in Eagle Marker or Nougat corpus. |
| DOI | — | 10.1093/jac/dkac115 | https://doi.org/10.1093/jac/dkac115 |
| PMID | — | 35403193 | https://pubmed.ncbi.nlm.nih.gov/35403193/ |
| PMCID | — | PMC9244215 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9244215/ |
| S2 paperId | — | b43c132b5dd2c5d3b00089bc784354c3c1f7302e | Semantic Scholar |

## Extraction artifacts (parses)

| Artifact | Path | Bytes | Status |
|---|---|---|---|
| Marker parse | `extraction/marker.md` | 2338 | Pending stub — see file. Contains fill instructions + explanation of fetch failures. |
| Nougat parse | `extraction/nougat.mmd` | 937 | Pending GPU parse — see file. |

## Report artifacts

| Artifact | Path | Notes |
|---|---|---|
| Canonical narrative report | `report/REPORT.md` | 13,063 bytes. Original report from the main run. |
| Detailed LaTeX report | `report/REPORT.tex` | Written 2026-07-05 backfill. Includes GENUINE CRITIQUE section + Open Questions section. |
| Compiled PDF | `report/REPORT.pdf` | Only present if `pdflatex` was on PATH during backfill (see failure_analysis.md). |
| Open questions | `report/open_questions.json` | 5 heavy-duty JSON records `{q, basis, next_steps}` for downstream research spawning. |
| Brief | `report/brief.md` | One-paragraph summary. |
| Attempt log | `report/attempt_log.md` | Chronological command log of the main run. |
| Artifact harvest | `report/artifact_harvest.md` | Initial artifact inventory (pre-backfill). |
| Evidence | `report/evidence/` | Raw command outputs, per-DB AMR TSVs, locus walks. |
| Workflow narrative | `report/workflow.md` | This backfill: end-to-end workflow, tool versions, effort estimate. |
| Artifact inventory | `report/artifacts_summary.md` | This file. |
| Failure analysis | `report/failure_analysis.md` | Written this backfill: honest failure analysis + gaps. |

## Working code

| File | Size | Purpose |
|---|---|---|
| `work/analyze.sh` | 6656 | Driver: MLST + abricate across 7 DBs + PlasmidFinder + VFDB + locus zooms. |
| `work/features_probe.py` | 3770 | GBFF feature walker for user-specified chromosomal windows. |
| `work/features_probe2.py` | 3175 | Tn7 machinery counter + ISAba1/IS26 census. |
| `work/gyrA_verify.py` | 3207 | GyrA CDS extraction + translation + positional comparison to WT WP_000116449.1. |
| `work/gyrA_verify2.py` | 2965 | Same as gyrA_verify.py but via Biopython PairwiseAligner as cross-check. |
| `work/llm_judge_bvbrc111.py` | 9604 | Argo LLM-judge driver (argo:gpt-5.1 + argo:gemini-2.5-pro). |
| `work/genome/` | (dir) | Downloaded assembly + concatenated FASTA staging. |

## Public data pulled

| Accession | Type | Length | Provenance |
|---|---|---|---|
| GCA_021484925.1 | Assembly | — | NCBI Datasets CLI. Authors' own submission, PGAP annotation of 10-Jan-2022, BioProject PRJNA742487, BioSample SAMN20178847. |
| CP090606.1 | Chromosome | ~4,153,776 bp | Inside GCA_021484925.1. |
| CP080453.1 | Plasmid | 2,178 bp | efetch nuccore. |
| CP080454.1 | Plasmid | 2,725 bp | efetch nuccore. |
| CP080455.1 | Plasmid | 6,772 bp | efetch nuccore. |
| CP080456.1 | Plasmid | 8,731 bp | efetch nuccore. |
| WP_000116449.1 | Protein | 904 aa | efetch protein. WT reference GyrA. |
| — | Combined FASTA | 4,174,182 bp | `MRSN56_complete.fna` on uicgpu:/data/stevens/bvbrc111/. |

## LLM audit trail

| Model | Endpoint | Score | Verdict | Cost |
|---|---|---|---|---|
| argo:gpt-5.1 | http://localhost:44497/v1 (Argo proxy, key=stevens) | 88 | REPLICATED | free |
| argo:gemini-2.5-pro | http://localhost:44497/v1 (Argo proxy, key=stevens) | 95 | FULLY REPLICATED | free |

Mean 91.5 → rounded **REPLICATED (92)**.

## What is NOT on disk

- The paper PDF itself (fetch failed non-interactively across three open-access endpoints).
- Raw MinION/MiSeq reads from ENA/SRA (not needed for replication of a finished-genome paper, and would require ~50 GB of read data + hybrid re-assembly compute).
- RNAseq data for the C7 transcriptional half of the mechanism (the paper does not appear to publish this either, based on the abstract and PMC-cached figures).
- Independent re-annotation with Prokka/Bakta (used PGAP as-shipped in the GCA_021484925.1 GBFF).
