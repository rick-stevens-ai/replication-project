# Artifacts Summary — BVBRC-21 (Founou et al. 2022, ESBL *E. coli* from pigs)

**Verdict:** PARTIAL (borderline REPLICATED) — Coverage 10/10, Agreement 7/10.

All artifacts live under `~/Dropbox/REPLICATE-PROJECT/BVBRC-21-ESBL-Ecoli-pigs-Founou2022/`.

---

## Input data

| Artifact | Purpose | Notes |
|----------|---------|-------|
| `data/genome_accessions.tsv` | Maps paper isolate label → NCBI WGS accession | 11 rows; BioProject PRJNA548686 (×10) + PRJNA412434 (PN256E8 ×1) |
| `data/genomes/` | Downloaded WGS assemblies | 11 × `.fna`; observed 4.62–5.35 Mb (paper 4.5–5.3 Mb ✓) |
| `data/paper_table1.tsv` | Ground-truth transcription of paper Tables 1+2 | MLST / phylogroup / serotype / resistome per isolate |

---

## Analysis outputs

| Artifact | Tool | What it contains |
|----------|------|------------------|
| `data/mlst_results.tsv` | `mlst 2.33.1` (`ecoli_achtman`) | ST call + Achtman-7 allele profile per isolate |
| `data/abricate/ncbi.tsv` | `abricate` vs NCBI AMR DB | AMR gene hits, %identity, %coverage, contig, coord |
| `data/abricate/resfinder.tsv` | `abricate` vs ResFinder DB | Second AMR panel for cross-validation |
| `data/abricate/plasmidfinder.tsv` | `abricate` vs PlasmidFinder DB | Inc-type replicon hits per isolate |
| `data/abricate/vfdb.tsv` | `abricate` vs VFDB | Virulence factor hits per isolate |

---

## Scripts

| Artifact | Role |
|----------|------|
| `scripts/run_all.sh` | End-to-end driver: iterates the 11 assemblies through `mlst` + 4 abricate DBs; reproduces every downstream table given `data/genomes/` and installed tools |

---

## Reports

| Artifact | Role |
|----------|------|
| `report/REPORT.md` | Primary human-readable replication report (canonical narrative + judge verdict) |
| `report/REPORT.tex` | LaTeX-formatted replication report with dedicated **GENUINE CRITIQUE** section |
| `report/open_questions.json` | Five open scientific questions the replication cannot itself answer (blaCTX-M variant/plasmid distribution; pig→human clonal transfer evidence; AMU-stewardship intervention effect; mcr co-carriage; African vs European pig-farm genotype divergence) |
| `report/workflow.md` | Step-by-step pipeline description |
| `report/artifacts_summary.md` | *This file* |
| `report/failure_analysis.md` | Honest per-discrepancy breakdown of what did and did not replicate |

---

## Coverage summary

| Category | Paper | This rerun | Coverage |
|---|---|---|---|
| Analyzable isolates | 11 | 11 | **11/11 (100%)** |
| MLST calls | 11 | 10 exact + 1 null | 10/11 exact |
| CTX-M-15 carriers (count) | 6 | 6 | **exact** |
| CTX-M-15 carriers (identity) | (per Table 2) | same 6 isolates | **exact** |
| Universal CTX-M+ | 11/11 | 11/11 | **exact** |
| Genome-size envelope | 4.5–5.3 Mb | 4.62–5.35 Mb | **within** |

---

## Discrepancies (see `failure_analysis.md` for detail)

1. `PN256E8` β-lactamase: paper CTX-M-15+TEM-1B+TEM-141+TEM-206 → rerun CTX-M-**55**+TEM-1B+TEM-141 (allele + TEM-206 differ).
2. `CTX-M-15 + TEM-1B` co-carriage count: paper 3 → rerun 4 (+1).
3. `PR246B1C` MLST: paper ST2144 → rerun `-` (allele identity-cutoff artefact; sibling PR209E1 types cleanly to 2144).

All three plausibly attributable to ResFinder/NCBI DB vintage drift vs the paper's 2021 DB — but not proven, since a pinned-DB re-run was not performed.

---

## What is *not* in the artifact set (and why)

- **Long-read / hybrid re-assemblies** — out of scope; would be needed to physically link CTX-M-15 to its Inc-type plasmid contig.
- **cgMLST / core-genome SNP tree** — out of scope; needed to test the pig→human clonal-transfer hypothesis.
- **Independent phylogroup (ClermonTyping) call** — trusted from paper Table 1.
- **Pinned 2021 ResFinder DB snapshot** — flagged as the single highest-value next step for a follow-up rerun.
