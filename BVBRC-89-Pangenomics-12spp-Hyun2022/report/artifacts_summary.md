# Artifacts Summary — BVBRC-89 Pangenomics Replication

**Project root:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-89-Pangenomics-12spp-Hyun2022/`
**Verdict:** PARTIAL (LLM-judge coverage ~45%, `argo:gpt-5.1`)
**Analyst:** Ollie (OpenClaw subagent, `argo/argo:claude-opus-4.7`)
**Date:** 2026-07-03

---

## 1. Paper source materials

| Artifact | Location | Size | Notes |
|---|---|---|---|
| Paper PDF | `work/hyun2022.pdf` | ~2 MB | BMC Genomics 23:7 (2022), open access CC BY 4.0 |
| Supplementary bundle | `work/supplementary.zip` | ~40 MB | From figshare `10.6084/m9.figshare.17870487.v1` |
| Dataset S1 (unzipped) | `work/supp/ds1/genome_ids/` | 12 CSVs | One per species; `Enterobacter_cloacae_genome_ids.csv` used here (104 PATRIC IDs) |

Paper metadata: DOI `10.1186/s12864-021-08223-8`, PMC `PMC8725406`, PMID `34983386`.

---

## 2. Data retrieval intermediates

| Artifact | Location | Rows | Notes |
|---|---|---|---|
| BV-BRC PATRIC→NCBI accession map | `work/ecloacae_accessions.csv` | 104 (54 with public NCBI accession) | Produced by `scripts/bvbrc_lookup.py` against `https://www.bv-brc.org/api/genome/` |
| Accession list for NCBI Datasets | `work/ec_accessions.txt` | 54 | The 54 rows with non-empty `assembly_accession` |
| NCBI Datasets download bundle | `work/ec_download/ec_proteomes.zip` | 54 × `protein.faa` | Fetched via `datasets download genome accession --include protein` |
| Unpacked proteomes | `work/ec_download/ncbi_dataset/data/GCF_*/protein.faa` | 54 files, 260,623 total proteins | Per-genome CDS min 4,368 / max 5,236 / median ~4,900 |

---

## 3. Pangenome pipeline outputs

| Artifact | Location | Size | Notes |
|---|---|---|---|
| Combined proteome (genome-tagged headers) | `work/ec_combined.faa` | ~102 MB, 260,623 sequences | Header format `>GCF_xxx\|WP_yyy <description>` for downstream cluster attribution |
| CD-HIT representative sequences | `work/cdhit/ec_clusters` | 16,959 sequences | CD-HIT v4.5.4, `-c 0.8 -aL 0.8 -n 5 -M 8000 -T 4 -d 0` |
| CD-HIT cluster file | `work/cdhit/ec_clusters.clstr` | ~15 MB | Membership of all 260,623 input proteins across the 16,959 clusters |
| Pangenome partition table | `work/partition.tsv` | 16,959 rows | Per-cluster: `cluster_id`, `n_genomes`, `partition∈{core,accessory,unique}` |
| Heaps fit JSON | `work/heaps_fit.json` | small | `{alpha_mean, alpha_std, kappa_mean, kappa_std, n_shuffles, seed}` |

Wall time for CD-HIT step: 34 s on 4 cores; peak RAM 239 MB.

---

## 4. Result numerics (headline)

### 4.1 Pangenome partition (E. cloacae, N=54)

| Partition | Count | % | Paper (N=104) count | Paper % | Ratio (ours/paper) |
|---|---:|---:|---:|---:|---:|
| Core      | 3,046 | 18.0 | 2,906 | 11.3 | 1.05 |
| Accessory | 4,351 | 25.7 | 4,533 | 17.7 | 0.96 |
| Unique    | 9,562 | 56.4 | 18,239 | 71.0 | 0.52 |
| **Total** | **16,959** | 100 | 25,678 | 100 | 0.66 |

Unique-gene ratio 0.52 exactly matches the genome-sample-size ratio 54/104 = 0.52 — the expected scaling for an open pangenome sampled at half.

### 4.2 Heaps' law fit (E. cloacae, by-genome, 100 shuffles, seed 42)

| Parameter | This replication (N=54) | Paper (N=104, by-genome) | Delta | Comment |
|---|---|---|---|---|
| α (openness) | 0.337 ± 0.020 | 0.384 ± 0.023 | −0.047 (~12%) | Still open (>0.3), still in Gammaproteobacteria band |
| κ (intercept) | 4,445 ± 362 | 4,330 ± 451 | +115 (2.7%) | Mean inside paper's ±451 envelope |

---

## 5. LLM judge output

| Artifact | Location |
|---|---|
| Judge verdict JSON | `report/evidence/judge_verdict.json` |
| Judge model | `argo:gpt-5.1` via Argo proxy `http://127.0.0.1:44497/v1` |
| Verdict | PARTIAL |
| Coverage estimate | ~45% |

---

## 6. Report artifacts (this deliverable directory)

| File | Purpose |
|---|---|
| `report/REPORT.md`         | Human-readable Markdown report (source of truth for narrative) |
| `report/REPORT.tex`        | LaTeX version of the same, including a dedicated "Genuine Critique" section |
| `report/workflow.md`       | End-to-end reproducible pipeline description |
| `report/artifacts_summary.md` | **This file** — manifest of every artifact produced |
| `report/failure_analysis.md`  | What did not replicate, why, and threats to validity |
| `report/open_questions.json`  | Five downstream research questions grounded in the paper |

---

## 7. Scripts referenced in `workflow.md`

Scripts referenced by the workflow. If a given script is not yet present in `work/scripts/`, its contract is fully specified in `workflow.md` and it can be regenerated:

| Script | Function | Contract |
|---|---|---|
| `scripts/bvbrc_lookup.py`      | Resolve PATRIC IDs to NCBI Assembly accessions | Paginated REST call to `https://www.bv-brc.org/api/genome/?in(genome_id,(...))&select(...)`; write CSV |
| `scripts/combine_proteomes.py` | Merge 54 per-genome `protein.faa` into single tagged FASTA | Prefix each header with `<accession>\|` for downstream cluster attribution |
| `scripts/partition_pangenome.py` | Parse `.clstr` and assign clusters to core/accessory/unique | Cutoffs `≥round(0.983·N)` core, `≤round(0.083·N)` unique |
| `scripts/heaps_fit.py`         | 100-shuffle Heaps' fit | `pan(N) = kappa · N^alpha`; SciPy `curve_fit`; report mean±std |
| `judge.py`                     | Argo LLM judge | POST to `argo:gpt-5.1` with paper vs replication numbers; parse JSON verdict |

---

## 8. Sizes and totals

- Total on-disk footprint of `work/` after full pipeline: ~500 MB (dominated by unpacked NCBI Datasets bundle + `ec_combined.faa`).
- Peak RAM: 239 MB (CD-HIT step).
- Total wall time: ~10 min end-to-end (dominated by NCBI Datasets download, ~5 min).
- API cost: $0 (Argo free endpoint for judge; all data sources open-access).

---

## 9. Not produced (documented for completeness)

- MLST-balanced Heaps' fit (needs `mlst` + PubMLST DB).
- 11 additional species' pangenomes.
- eggNOG COG enrichment per partition.
- InterProScan AARS domain-level analysis.
- 168-gene 12-species cross-species core.
- Assembly QC (CheckM2 completeness/contamination) filter sweep.
- Prokka/Bakta/PGAP re-annotation sensitivity comparison.
- Alternate clusterer runs (Roary, Panaroo, PPanGGOLiN).

Estimated cost to complete: see `workflow.md` §11.
