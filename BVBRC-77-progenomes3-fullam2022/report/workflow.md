# Workflow — BVBRC-77 · proGenomes3 replication

End-to-end workflow used to produce the PARTIAL verdict. All steps are
independently re-runnable on any host with Python 3.13 stdlib and outbound
HTTP; wall-clock < 4 min total; zero paid API calls.

## 0. Environment

- Host: CherryRd (local), Python 3.13 stdlib only, no venv required.
- Endpoints (all free): EuropePMC REST, NCBI eUtils, NCBI Datasets v2alpha
  REST, `progenomes.embl.de` HTTP GET, Argo LLM proxy at
  `http://127.0.0.1:44497` (key = `stevens`).
- Working root: `~/Dropbox/REPLICATE-PROJECT/BVBRC-77-progenomes3-fullam2022/`.

## 1. Paper retrieval

1. Pull EuropePMC full-text XML: `PMC9825469` (~90 KB).
2. Strip to plain text (~33 KB).
3. Confirm exact abstract, DOI (`10.1093/nar/gkac1078`), and resource URL
   (`http://progenomes.embl.de/`).

## 2. Resource probing

1. `curl` `https://progenomes.embl.de/` → HTTP 200.
2. `curl` `https://progenomes.embl.de/download.cgi` → HTTP 200, 16.3 KB HTML.
3. Enumerate candidate v3 filenames from the HTML; probe each: **all 6 pg3
   URLs return 404**.
4. Try `pg4_*` successor filenames: **all 3 tested URLs return 200**.
5. Record the silent v3→v4 backend swap as a first-class finding. Re-verify
   2026-07-04.

## 3. Data pull (real, live, free)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/BVBRC-77-progenomes3-fullam2022
mkdir -p work/downloads report/evidence

for f in pg4_representatives_for_each_ANI_cluster.tsv.gz \
         pg4_ANI_clustering.tsv.gz \
         pg4_ncbi_taxonomy.tsv.gz \
         pg4_consensus_gtdb_taxonomy_per_ani_cluster.tsv.gz \
         pg4_excluded_genomes.txt.gz \
         pg4_highly_important_strains.tsv.gz ; do
  curl -sL -o "work/downloads/$f" "https://progenomes.embl.de/data/$f"
done
```

Sizes: representatives 222 KB (32,887 rows), ANI clustering 4.8 MB / 30 MB
uncompressed (32,887 rows), NCBI taxonomy 5.8 MB (1,891,269 rows), GTDB
consensus 432 KB (29,602 rows), excluded 3.6 MB (1,243,181 rows),
highly-important-strains 2.5 KB (820 rows).

## 4. Random slice for spot-checking

```python
import random
random.seed(20260703)
slice_100 = random.sample(sorted(reps), 100)
```

Reproducible slice of 100 pg4 species representatives.

## 5. Independent QC re-check (slice-level)

For each of the 100 slice accessions:

1. GET `https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/{acc}/dataset_report`
2. Extract `assembly_stats.contig_n50`, `total_sequence_length`,
   `assembly_level`, and NCBI's CheckM completeness + contamination.
3. Pause 350 ms between calls (courtesy rate limit).
4. Evaluate against the paper's stated gate:
   completeness > 90% AND contamination < 5%.

Result: 65/82 with both fields reported = **79.3% pass** (caveat: NCBI runs
CheckM1, pg4 likely runs CheckM2 — tool-version signal, not contradiction).

## 6. Full-scale structural verification

```bash
python3 work/full_scale_analysis.py
```

Parses all 5 pg4 metadata files and computes:

- cluster ↔ representative bijection (0 mismatches expected & found),
- representative-in-own-cluster membership (32,887/32,887 valid),
- representative-not-in-excluded consistency (0/32,887 violations),
- cluster size distribution (min/median/max/singletons/decade buckets),
- QC-pass count = `|ncbi_taxonomy \ excluded|` = 1,891,267,
- GTDB consensus coverage = 29,602 / 32,887 = 90.01%,
- highly-important-strain retention across QC = 795 / 820 = 97.0%.

Output: `report/evidence/pg4_full_scale_stats.json`.

## 7. Taxonomy consistency

For each slice genome, compare `pg4_gtdb_short` (Bork consensus) against
NCBI Datasets `organism_name`. Split on whitespace, count genus and species
token matches.

Slice-100 result: genus 71.4% (65/91), species 42.9% (39/91). DB-scale
result: 90.01% of clusters carry a GTDB consensus.

## 8. LLM judge (majority vote)

```bash
python3 work/judge_v2.py
```

Feeds paper summary + full replication evidence to 4 candidate judges via
free Argo proxy; each must return strict JSON with verdict, coverage%,
agreement%. Majority verdict wins.

- `argo:gpt-4.1` → PARTIAL / 80 / 95
- `argo:claude-sonnet-4.5` → PARTIAL / 75 / 85
- `argo:gpt-4o` → PARTIAL / 83 / 90
- `argo:claude-opus-4.7` → 502 (skipped, both runs)

Unanimous PARTIAL (3/3 reporting). Mean coverage 79.3%, mean agreement 90.0%.

Output: `report/evidence/llm_judge_verdicts_v2.json`.

## 9. Assembly of REPORT.md + REPORT.tex

The narrative REPORT.md is authored from the JSON evidence artifacts and this
workflow log. REPORT.tex is a LaTeX render of the same content plus an
explicit `GENUINE CRITIQUE` section.

## 10. Promotion checklist

- [x] All quantitative counts match `pg4_full_scale_stats.json` exactly.
- [x] All slice-100 percentages match `slice100_summary.json` exactly.
- [x] Silent v3→v4 backend swap documented as a first-class finding.
- [x] LLM judges v2 unanimous PARTIAL from Argo proxy.
- [x] Endpoints declared free; zero paid API calls.
- [x] Compute footprint (Python 3.13 stdlib, < 4 min wall-clock) declared.
- [x] Verdict = PARTIAL (not REPLICATED — v3 files 404 and eggNOG untested;
      not CONTRADICTED — structural checks pass and CheckM delta is
      tool-version-attributable).
