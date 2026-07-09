# Artifacts Summary — BVBRC-51 Minicystis rosea DSM 24000T

**Paper:** Pal S, Sharma G, Subramanian S. *BMC Genomics* 22:655 (2021). DOI 10.1186/s12864-021-07955-x; PMID 34511070; PMC8436480. CC BY 4.0.
**Replication date:** 2026-07-02
**Verdict:** PARTIAL (strong).

---

## 1. Input artifacts (external, harvested)

| # | Artifact | Source | Type | Notes |
|---|---|---|---|---|
| I1 | `fulltext.xml` | Europe PMC (PMC8436480) | Paper XML | Full text; extracted CP016211.1, PRJNA321464, methods for antiSMASH + *pfa* references. |
| I2 | Genome assembly bundle **GCA_001931535.1** | NCBI Datasets REST API | FASTA + GFF3 + faa (proteome) | Chromosome CP016211.1, one circular contig. MD5 of the zip recorded in `artifact_harvest.md`. |
| I3 | Pfa reference proteins (×10) | NCBI `efetch` | Protein FASTA | AIJ50372–77 (Aetherobacter), CAN90975–77 + CAN95221 (S. cellulosum So ce56). |
| I4 | antiSMASH 8.0.4 databases | antiSMASH project | Reference DBs | Pre-built into the uicgpu conda env. |

## 2. Evidence artifacts (produced, canonical)

Stored under `evidence/`.

| # | File | Produced by | Content | Used for claim |
|---|---|---|---|---|
| E1 | `genome_stats.json` | `genome_stats.py` | Genome size, GC%, CDS + strand split, tRNA / rRNA counts, coding density | C2, C3 |
| E2 | `pfa_blast_summary.json` | `pfa_blast.py` | Per-reference best-hit table + %id + summed-HSP coverage + top-hit synteny (loci, strands, gaps) | C5 |
| E3 | `antismash_summary.json` | antiSMASH 8.0.4 + parse script | Per-region product category tally + total BGC count | C4 |
| E4 | `llm_judge_gpt52.txt` | Argo `gpt-5.2` | Claim-by-claim scoring + verdict (PARTIAL) | Verdict |
| E5 | `llm_judge_opus48.txt` | Argo `claude-opus-4.8` | Claim-by-claim scoring + verdict (REPLICATED) | Verdict |

## 3. Work artifacts (intermediate, `work/`)

- `work/fulltext.xml` — Europe PMC full-text XML.
- `work/GCA_001931535.1/` — genome FASTA, GFF3, proteome faa.
- `work/pfa_refs.faa` — 10-protein Pfa reference set.
- `work/blast_db/` — `makeblastdb` output on the M. rosea proteome.
- `work/pfa_blast.tsv` — raw BLAST tabular output.
- `work/mrosea_asmash8/` — antiSMASH 8.0.4 output tree, incl. `mrosea.json`.
- `work/scripts/` — `genome_stats.py`, `pfa_blast.py`, JSON-parse helpers.

## 4. Report artifacts (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical human-readable replication report. |
| `REPORT.tex` | LaTeX version with dedicated `Genuine Critique` section. |
| `open_questions.json` | Five truly-open questions grounded in the 2021 M. rosea BGC / large-myxobacterial-genome context. |
| `workflow.md` | Stage-by-stage pipeline description + data-flow diagram. |
| `artifacts_summary.md` | This index. |
| `failure_analysis.md` | What did not cleanly reproduce and why. |
| `attempt_log.md` | Per-stage chronological record (commands + timings). |
| `artifact_harvest.md` | External-artifact provenance (URLs, accessions, checksums). |

## 5. Key numerical results (headline)

| Metric | Paper | Replication | Match |
|---|---:|---:|---|
| Genome size (bp) | 16,040,666 | 16,040,666 | EXACT |
| CDS | 14,018 | 14,018 | EXACT |
| CDS (+) | 6,983 | 6,983 | EXACT |
| CDS (−) | 7,035 | 7,035 | EXACT |
| GC % | 69.07 | 69.10 | Δ0.03 |
| Coding density % | 87.31 | 87.59 | Δ0.28 |
| tRNA | 88 | 89 | Δ1 |
| rRNA | 4 operons | 4×16S + 4×23S + 2×5S | ~consistent |
| BGCs (antiSMASH) | 47 (v5.0) | 53 (v8.0.4) | +6 (version-shift) |

## 6. Compute + auth footprint

- **CherryRd:** Python 3, Biopython, NCBI `entrez-direct` + `datasets` CLI, BLAST+.
- **uicgpu (A100):** conda env with antiSMASH 8.0.4 + prodigal.
- **LLM:** Argo proxy (`argo:gpt-5.2`, `argo:claude-opus-4.8`), both free.
- **No paid endpoints touched.**

## 7. Reproducibility invariants

- Assembly accession `GCA_001931535.1` (chromosome `CP016211.1`) — the identity signal is the strand-resolved CDS count `6,983 / 7,035`, which pins this to exactly the paper's deposited genome.
- Any replicator repeating this workflow with the same accession + antiSMASH 8.0.4 should reproduce the numbers to the same tolerances shown in §5. The BGC total is version-locked; rerunning against antiSMASH v5.0 should recover the paper's 47.
