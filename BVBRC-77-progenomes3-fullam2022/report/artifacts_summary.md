# Artifacts summary — BVBRC-77 · proGenomes3

All artifacts under
`~/Dropbox/REPLICATE-PROJECT/BVBRC-77-progenomes3-fullam2022/`.

## Report artifacts (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Primary narrative replication report (17 KB, source of truth). |
| `REPORT.tex` | LaTeX-formatted rendering of REPORT.md with explicit GENUINE CRITIQUE section. |
| `open_questions.json` | 5 truly-open follow-up questions grounded in Fullam 2022 proGenomes3. |
| `workflow.md` | End-to-end reproducible workflow log. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Honest failure-mode assessment. |
| `evidence/pg4_full_scale_stats.json` | Full-DB structural stats (32,887 clusters, 1,891,267 genomes). |
| `evidence/slice100_summary.json` | Slice-100 NCBI Datasets QC re-check. |
| `evidence/llm_judge_verdicts_v2.json` | v2 LLM-judge verdicts (3 × PARTIAL). |

## Downloaded resource files (`work/downloads/`)

Pulled live from `https://progenomes.embl.de/data/`, all HTTP 200:

| File | Compressed size | Rows |
|---|---|---|
| `pg4_representatives_for_each_ANI_cluster.tsv.gz` | 222 KB | 32,887 |
| `pg4_ANI_clustering.tsv.gz` | 4.8 MB | 32,887 |
| `pg4_ncbi_taxonomy.tsv.gz` | 5.8 MB | 1,891,269 |
| `pg4_consensus_gtdb_taxonomy_per_ani_cluster.tsv.gz` | 432 KB | 29,602 |
| `pg4_excluded_genomes.txt.gz` | 3.6 MB | 1,243,181 |
| `pg4_highly_important_strains.tsv.gz` | 2.5 KB | 820 |

## Scripts (`work/`)

| Script | Function |
|---|---|
| `full_scale_analysis.py` | Full-DB structural verification (< 15 s, 2 GB RAM). |
| `compute_claims.py` | Slice-100 QC re-check via NCBI Datasets REST. |
| `slice_analysis.py` | Taxonomy consistency (pg4-GTDB vs NCBI organism_name). |
| `judge_v2.py` | LLM judge invocation via free Argo proxy. |

## Reproduced quantitative results (grounded in above artifacts)

- **HQ genomes on pg4 successor:** 1,891,267 (paper v3: 907,388; +108.4%).
- **ANI clusters on pg4:** 32,887 (paper v3 specI: 41,171; −20.1%).
- **Representatives on pg4:** 32,887 (matches clusters, 1:1 bijection).
- **QC-excluded pool:** 1,243,181 IDs; intersection with QC-passed = 2
  (near-perfect disjoint).
- **Implied input pool:** 3,134,448 genomes; overall QC pass rate 60.3%.
- **GTDB consensus coverage (DB-scale):** 29,602 / 32,887 = 90.01%.
- **Structural integrity:** 32,887 / 32,887 (100%) reps belong to own
  cluster; 0 / 32,887 (0%) reps appear in excluded list.
- **Cluster size distribution:** median 1, mean 57.5, max 544,186;
  singletons 54.2%.
- **Highly-important-strain retention:** 795 / 820 = 97.0% preserved.
- **Slice-100 CheckM re-check:** 65 / 82 with both fields = 79.3% pass
  (caveat: NCBI CheckM1 vs pg4 likely CheckM2).
- **Slice-100 N50:** min 12,911; median 351,648; mean 1,272,730;
  max 7,090,212 bp.
- **Slice-100 taxonomy agreement with NCBI:** genus 71.4% (65/91),
  species 42.9% (39/91).
- **LLM judges v2 (Argo proxy, free):** 3 × PARTIAL, mean coverage 79.3%,
  mean agreement 90.0%; Opus-4.7 502'd twice and was skipped.

## Provenance

- Executed by Ollie subagent; initial spot-check 2026-07-03; promoted
  2026-07-04.
- Compute: local (CherryRd), Python 3.13 stdlib, no venv.
- Wall-clock: < 4 min end-to-end.
- Cost: zero paid API calls (all endpoints free).
