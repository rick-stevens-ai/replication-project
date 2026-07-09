# Workflow — Blackwell 2021 (661k bacterial genomes snapshot) replication

Paper: Blackwell et al. 2021, PLoS Biology 19(11): e3001421.
Verdict landed: **REPLICATED** (LLM-judge argo:gpt-5.1: coverage 96%, agreement 100%).

This file describes the reproducible pipeline used, in the order the steps must run. All commands assume `work/` and `report/evidence/` under the project root.

## 0. Prerequisites

- `curl`, `awk`, `gzip`, `python3` (with `hashlib`, `random`, `collections`, `csv`, `xml.etree`, `requests`).
- Network access to `ftp.ebi.ac.uk`, `api.figshare.com`, `www.ebi.ac.uk` (ENA browser XML API).
- Argo proxy reachable on `localhost:44497` with key `stevens` for the LLM judge (free endpoint policy).
- ~2 GB free disk in `work/` for the metadata + 25 sampled assemblies. Full-artifact pull (assemblies tar, COBS, sourmash, ppsketch) is NOT required for this replication and would cost ~1.75 TB.

## 1. Manifest + checklist pull

```
mkdir -p work report/evidence
cd work
curl -sSLO http://ftp.ebi.ac.uk/pub/databases/ENA2018-bacteria-661k/sampleid_assembly_paths.txt
curl -sSLO http://ftp.ebi.ac.uk/pub/databases/ENA2018-bacteria-661k/checklist.chk
wc -l sampleid_assembly_paths.txt   # -> 661405
wc -l checklist.chk                 # -> 661413 (8 extra rows are index/aux files)
```

## 2. Random 25-sample spot check

```
python3 - <<'PY'
import random, csv
random.seed(661405)
with open('sampleid_assembly_paths.txt') as f:
    rows = [ln.strip().split('\t') for ln in f]
picks = random.sample(rows, 25)
with open('spot_check_sample.tsv','w') as out:
    w = csv.writer(out, delimiter='\t')
    for r in picks: w.writerow(r)
PY
```

For each of the 25 picks, pull the corresponding `SAM*.contigs.fa.gz` (path is in the manifest), compute local MD5 with `hashlib.md5`, and compare against the MD5 for that relative path in `checklist.chk`. Then uncompress in-memory, compute total bp, contig count, GC%, and N50. Serialize to `report/evidence/spot_check_results.json`.

Expected outcome: **25/25 MD5s match**; per-genome stats fall in bacterial ranges (total 1.7–5.2 Mb, GC 28–66%, N50 26k–445k).

## 3. Species labels via ENA XML API

For each of the 25 sample IDs, `GET https://www.ebi.ac.uk/ena/browser/api/xml/{SAM_ID}` and parse `SCIENTIFIC_NAME` + `TAXON_ID`. Serialize to `report/evidence/spot_check_species.json`.

Expected outcome: 25/25 samples return a clinical bacterial pathogen name; no unclassified.

## 4. Figshare metadata pull

```
cd work
curl -sSL https://api.figshare.com/v2/articles/16437939 -o figshare_meta.json
# From figshare_meta.json, extract download URLs for File2 and File4
curl -sSLO <File2_URL>   # File2_taxid_lineage_661K.txt (~95 MB)
curl -sSLO <File4_URL>   # File4_QC_characterisation_661K.txt (~430 MB)
curl -sSLO <File4_desc_URL>   # File4_column_descriptions.txt
```

## 5. Composition recount

Species tally on the full 661k (from File2):

```
python3 - <<'PY'
from collections import Counter
c = Counter()
n = 0
with open('File2_taxid_lineage_661K.txt') as f:
    header = f.readline().rstrip('\n').split('\t')
    sp_idx = header.index('species')
    for line in f:
        parts = line.rstrip('\n').split('\t')
        c[parts[sp_idx]] += 1
        n += 1
total = n
top20 = c.most_common(20)
cum = sum(v for _,v in top20)
print('n =', n, 'unique =', len(c), 'top20 cum% =', 100*cum/total)
PY
```

Expected outcome: `n = 661405`, `unique = 2594`, `top20 cum% ≈ 89.72`. Serialize the full top-20 to `report/evidence/species_diversity_check.json`.

## 6. High-quality count via streamed awk

Stream `File4_QC_characterisation_661K.txt` without materialising to memory:

```
awk -F'\t' 'NR>1 {c[$39]++} END {for (k in c) print k, c[k]}' File4_QC_characterisation_661K.txt
```

Expected outcome: `TRUE 639981`, `NA 21424`, sum 661,405.

## 7. LLM-judge

```
python3 work/llm_judge.py \
  --endpoint http://localhost:44497/v1 --key stevens \
  --model argo:gpt-5.1 \
  --evidence report/evidence/*.json \
  --out report/evidence/llm_judge_verdict.json
```

`llm_judge.py` assembles: paper claims × verification × what-was-NOT-done × Methods & Resources context, and returns JSON `{verdict, coverage_pct, agreement_pct, one_line_summary, reasoning}`.

Retry policy: if `argo:claude-opus-4.7` returns HTTP 502 (as it did on 2026-07-03), swap to `argo:gpt-5.1` and re-run — both are free endpoints under the Argo proxy.

## 8. Report assembly

- Write `report/REPORT.md` with sections: Paper, Claims tested, Method, Results vs Paper, Verdict, Files, Notes.
- Copy verdict JSON into REPORT.md section 4.4.
- Cross-link from REPORT.md to `evidence/*.json`, `attempt_log.md`, `artifact_harvest.md`.

## Ordering notes

Steps 1 → 2 → 3 are one lane (spot-check evidence).
Steps 4 → 5, 4 → 6 are a parallel lane (composition recount).
Both lanes must finish before Step 7 (LLM judge needs all evidence).
Step 8 is strictly last.

## Idempotence

Every step is deterministic given the same seed (`random.seed(661405)`) and the same upstream files (which are MD5-pinned in `checklist.chk`). Re-runs must produce byte-identical spot-check picks and byte-identical species tallies.
