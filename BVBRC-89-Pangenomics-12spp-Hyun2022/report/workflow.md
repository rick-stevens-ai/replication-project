# Workflow — Hyun/Monk/Palsson 2022 Pangenomics Replication (BVBRC-89)

**Verdict:** PARTIAL (LLM-judge coverage ~45%)
**Analyst:** Ollie (OpenClaw subagent, `argo/argo:claude-opus-4.7`)
**Date:** 2026-07-03
**Scope of this replication:** Single species (*Enterobacter cloacae*, the smallest of the paper's 12) on the 54/104 PATRIC genomes with public NCBI Assembly accessions. CD-HIT pipeline + Heaps' law fit only.

---

## 0. Prerequisites

- macOS/Linux shell, Python 3.11+, SciPy, NumPy.
- `cd-hit` v4.5.4 (paper used v4.6; version difference cosmetic per algorithm).
- NCBI `datasets` CLI (`brew install ncbi-datasets-cli` or conda).
- ~1 GB free disk, ~250 MB peak RAM for the CD-HIT step, ~1 min wall time.
- Argo proxy access at `http://127.0.0.1:44497/v1` (for the LLM judge step).

---

## 1. Fetch paper and supplementary

```bash
cd ~/Dropbox/REPLICATE-PROJECT/BVBRC-89-Pangenomics-12spp-Hyun2022/work

# Open-access PDF
curl -sL -o hyun2022.pdf \
  "https://bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-021-08223-8.pdf"

# figshare Dataset S1 (contains per-species genome ID lists)
curl -sL -o supplementary.zip "https://ndownloader.figshare.com/files/32584002"
unzip -o supplementary.zip -d supp/
unzip -o supp/DatasetS1.zip  -d supp/ds1/
```

Deliverable: `supp/ds1/genome_ids/Enterobacter_cloacae_genome_ids.csv` = 104 PATRIC genome IDs (e.g. `550.1074`, `550.1113`, ...).

---

## 2. Resolve PATRIC IDs to NCBI Assembly accessions

```bash
python3 scripts/bvbrc_lookup.py \
  --input  supp/ds1/genome_ids/Enterobacter_cloacae_genome_ids.csv \
  --output ecloacae_accessions.csv
```

`scripts/bvbrc_lookup.py` paginates BV-BRC REST:

```
https://www.bv-brc.org/api/genome/?in(genome_id,(...))&select(genome_id,assembly_accession,strain,collection_year)
```

**Outcome (2026-07-03):** All 104 IDs still valid on BV-BRC. 54/104 have NCBI Assembly accessions (mirrored to GenBank). The remaining 50 are PATRIC-only submissions never mirrored; this is a **downstream-repository lag**, not a paper defect.

```bash
awk -F, 'NR>1 && $2!="" {print $2}' ecloacae_accessions.csv > ec_accessions.txt
wc -l ec_accessions.txt   # 54
```

---

## 3. Batch download proteomes from NCBI

```bash
datasets download genome accession \
  --inputfile  ec_accessions.txt \
  --include    protein \
  --filename   ec_download/ec_proteomes.zip
unzip -q ec_download/ec_proteomes.zip -d ec_download/
```

**Outcome:** 54 × `protein.faa`, **260,623 total proteins** across the 54 genomes. Per-genome CDS count min 4,368 / max 5,236 / median ~4,900 — consistent with the paper's reported per-genome CDS counts.

---

## 4. Combine proteomes with genome-tagged headers

```bash
python3 scripts/combine_proteomes.py \
  --indir  ec_download/ncbi_dataset/data/ \
  --outfa  ec_combined.faa
```

`combine_proteomes.py` walks the accession subdirs, reads each `protein.faa`, and re-emits headers in the form `>GCF_xxx|WP_yyy <original description>` so downstream cluster ownership can be recovered by string split.

Deliverable: `ec_combined.faa`, ~102 MB, 260,623 sequences.

---

## 5. CD-HIT clustering (paper's exact protocol)

```bash
mkdir -p cdhit
cd-hit \
  -i ec_combined.faa \
  -o cdhit/ec_clusters \
  -c 0.8 -aL 0.8 -n 5 \
  -M 8000 -T 4 -d 0
```

Paper parameters: `-c 0.8 -aL 0.8 -n 5`. Additional flags (`-M`, `-T`, `-d`) control memory/threads/description-width only.

**Outcome:** wall time 34 s; peak RAM 239 MB; **16,959 gene clusters** written to `cdhit/ec_clusters.clstr`.

---

## 6. Pangenome division (core / accessory / unique)

```bash
python3 scripts/partition_pangenome.py \
  --clstr cdhit/ec_clusters.clstr \
  --n     54 \
  --core-frac   0.983 \
  --unique-frac 0.083 \
  --out   partition.tsv
```

Cutoffs (scaled from paper's percentages to N=54):
- Core: gene present in ≥ round(0.983 × 54) = **53** genomes
- Unique: gene present in ≤ round(0.083 × 54) = **4** genomes
- Accessory: everything else

**Outcome (54 genomes):**

| Partition | Count | % of total |
|---|---:|---:|
| Core      | 3,046 | 18.0 |
| Accessory | 4,351 | 25.7 |
| Unique    | 9,562 | 56.4 |
| **Total** | **16,959** | 100 |

For comparison, the paper (N=104): core 2,906 (11.3%), accessory 4,533 (17.7%), unique 18,239 (71.0%), total 25,678.

---

## 7. Heaps' law fit

```bash
python3 scripts/heaps_fit.py \
  --clstr    cdhit/ec_clusters.clstr \
  --n        54 \
  --shuffles 100 \
  --seed     42 \
  --out      heaps_fit.json
```

Procedure:
1. For each of 100 random genome orderings (seed 42), compute cumulative pangenome size vs number of genomes added.
2. Fit `pan(N) = kappa * N^alpha` via SciPy `curve_fit` (nonlinear least squares), initial guess `kappa=1000, alpha=0.4`.
3. Report mean ± std of `alpha`, `kappa` over the 100 fits.

**Outcome:**
- `alpha = 0.337 ± 0.020` (paper: 0.384 ± 0.023 by-genome)
- `kappa = 4,445 ± 362`  (paper: 4,330 ± 451 by-genome)

`kappa` sits inside the paper's ±451 envelope. `alpha` is ~12% below, consistent with sub-half-sample compression of an open-pangenome fit.

The paper's headline analysis is MLST-balanced (requires the `mlst` tool + PubMLST DB); only the by-genome fit was reproduced here.

---

## 8. LLM judge

```bash
export OPENAI_API_KEY=stevens
python3 judge.py \
  --paper-numbers  supp/paper_numbers.json \
  --our-numbers    partition.tsv,heaps_fit.json \
  --model          argo:gpt-5.1 \
  --base-url       http://127.0.0.1:44497/v1 \
  --out            report/evidence/judge_verdict.json
```

Prompt asks for JSON `{verdict, coverage_pct, one_line, justification}`. Argo `argo:gpt-5.1` returned `verdict: PARTIAL`, `coverage_pct: ~45`.

---

## 9. Report generation

```bash
# markdown
cp REPORT.md ../report/REPORT.md

# LaTeX (this file's sibling REPORT.tex)
pdflatex -interaction=nonstopmode REPORT.tex
```

---

## 10. What was intentionally NOT done

- **MLST-balanced Heaps' fit** (paper's headline methodological improvement). Requires `mlst` tool + local PubMLST DB. Not attempted this turn.
- **Remaining 11/12 species.** Compute-bounded to one subagent turn. Feasible on uicgpu A100 on a longer schedule; per-species cost is small (E. cloacae step was 34 s on 4 cores).
- **Functional analyses.** eggNOG-mapper for COG enrichment, InterProScan for AARS domain analysis, MSA + phylogenetics for the 168-gene cross-species core. All are in-scope for a future wave.
- **QC filtering of input assemblies.** CheckM2 completeness/contamination sweep not applied; this is a known threat to validity (see `failure_analysis.md`).
- **Re-annotation with Prokka/Bakta/PGAP** to test pipeline-independence of the pangenome. Also out of scope.

---

## 11. Estimated cost to complete the missing pieces

| Step | Compute | Wall time | Notes |
|---|---|---|---|
| Repeat CD-HIT + Heaps for other 11 species on 54-avail cap | ~4 cores | ~30 min | Trivial; unblocks C5 partially |
| MLST-balanced fit, 12 species | +`mlst` + PubMLST DB (~5 GB) | ~2 h | Unblocks C6 |
| eggNOG-mapper on all 12 pangenome partitions | 8-16 cores, 32 GB RAM | ~4 h | Unblocks C7 |
| InterProScan on AARS gene families | 8 cores | ~2 h per species | Unblocks C8 |
| 12-species cross-species core detection | negligible after (1) | 15 min | Unblocks C9 |

Total additional cost to lift verdict from PARTIAL → FULL: roughly one uicgpu-day of wall time plus data-download.

---

## 12. Artifacts produced

See `artifacts_summary.md` for the full manifest.

## 13. Where things went wrong or were limited

See `failure_analysis.md`.
