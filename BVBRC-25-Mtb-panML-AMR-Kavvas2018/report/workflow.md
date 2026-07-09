# Workflow — Kavvas 2018 M. tuberculosis pan-genome ML AMR replication

**Target:** BVBRC-25 replication wave
**Verdict achieved:** PARTIAL (strong on tested core ML claims)
**Compute:** uicgpu (255 cores, 2 TB RAM), free tooling only
**Runtime:** ~6 s (MI) + ~70 s (SVM) after data download; end-to-end well under 15 min

## 0. Bibliographic ingest
1. Europe PMC REST → `europepmc.json` (bibliographic record for PMID 30333483 / PMC6193043).
2. Europe PMC full-text XML → `fulltext.xml` (used to extract method parameters: CD-HIT v4.6 id=0.8 word=5; 200 SVM sims @ 80% bootstrap; L1-SGD hinge; balanced class weight; top-40 per drug; remove PE/PPE/PGRS/transposase/hypothetical/mobile; remove each drug's primary gene from other drugs' analyses).

## 1. Data harvest (authors' GitHub, `data/`)
Download the paper's five processed pan-genome intermediates:

```bash
mkdir -p data && cd data
for f in \
    pangen_allele_df.csv \
    pangen_cluster_df.csv \
    cluster_info.csv \
    resistance_data.csv \
    strain_information.csv; do
  curl -sSLO "https://raw.githubusercontent.com/erolkavvas/microbial_AMR_ML/master/data/$f"
done
```

Verify dimensions:
- `pangen_allele_df.csv` → 1,595 strains × 15,367 alleles (md5 e124e874...)
- `pangen_cluster_df.csv` → 1,595 strains × 11,039 clusters
- `cluster_info.csv` → 11,039 rows, columns Rv id / gene_name / product / pan-category
- `resistance_data.csv` → R/S per strain × 19 drug columns (13 used in paper)
- `strain_information.csv` → strain metadata

No auth required; all matrices load cleanly at exactly the paper's published dimensions.

## 2. C1 — Pan-genome conservation + PE/PPE/PGRS enrichment
`work/pangenome_stats` step (direct counts on `cluster_info.csv`):

1. Group clusters by pan-category (Core / Accessory / Unique).
2. Regex on `product` + `gene_name` for `PE|PPE|PGRS` families.
3. Report per-category PE/PPE/PGRS count and fraction.

Output: `report/evidence/pangenome_stats.json`
Expected: core 3.3%, accessory 24.5%, unique 30.6% (7–9× enrichment in variable genome).

## 3. C2a — Mutual information (`replicate_fast.py`)
Vectorized exact discrete binary–binary MI (in bits) from the 2×2 contingency table of allele-presence × R/S. Vectorized χ² with Bonferroni.

1. Variance filter: keep alleles with 5 ≤ count ≤ N−5 (15,260 / 15,367 pass).
2. For each of 10 drugs with sufficient R/S counts:
   - compute per-allele MI in bits
   - collapse alleles → gene-level best MI via `cluster_info` mapping
   - record top-40 by MI (paper convention) and the MI rank of each canonical primary gene
3. Handle rrs-mediated drugs (AMK/KAN/CAP): note `rrs` absent from protein pan-genome (0 clusters) — structurally unrecoverable.

Runtime: 5.5 s on uicgpu (numpy vectorized, no sklearn per-pair loop).
Output: `report/evidence/association_results.json`

## 4. C2b — Ensemble L1-SVM (`replicate_svm.py`)
Own from-scratch implementation of the paper's ensemble feature selection.

Per drug:
1. Preprocessing (paper's exact recipe):
   - drop PE / PPE / PGRS / transposase / hypothetical / mobile-element clusters
   - drop *other* antibiotics' primary resistance gene alleles (to break MDR co-resistance confound)
2. 200 bootstrap simulations at 80% subsampling of strains.
3. Each simulation fits `SGDClassifier(loss=hinge, penalty=l1, class_weight=balanced)`.
4. Record per-gene selection frequency (fraction of the 200 sims where the gene had ≥1 non-zero-weight allele).
5. Rank genes by selection frequency; record top-40 and rank of canonical primary + known-secondary genes.

Parallelised 64-way via joblib; runtime 70 s for 7 drugs (RIF, INH, EMB, STR, OFL, ETH, PZA).
Output: `report/evidence/svm_results.json`

## 5. C3, C4 — NOT ATTEMPTED
- C3 (97 epistatic interactions): would require full gene-gene logistic-regression sweep over SVM-weight-correlated pairs. Multi-hour compute; deferred.
- C4 (3-D structural mutation mapping): requires PDB structures / homology models + the authors' mutation-mapping pipeline. Deferred.

## 6. LLM-judge verdict
Compact evidence summaries (tables from §4.1–4.3 + limitations) sent as prompts to two independent Argo endpoints:

- **`argo:gpt-5.2`** → `report/evidence/llm_judge_verdict.json` (PARTIAL, coverage 6, agreement 6)
- **`argo:gpt-4o`** → `report/evidence/llm_judge_verdict2.json` (PARTIAL, coverage 8, agreement 6)

Free localhost:44497 Argo proxy. No regex scoring — verdicts are the judges' structured JSON output.

## 7. Report + artifact promotion
1. Assemble `REPORT.md` (already present).
2. Backfill: `REPORT.tex`, `open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`.
3. Do not fabricate any numbers not in `evidence/*.json` outputs.

## 8. Reproducibility one-liner
```bash
source ~/env.sh                       # uicgpu proxy env
mkdir -p data && cd data && \
  for f in pangen_allele_df.csv cluster_info.csv resistance_data.csv; do \
    curl -sSLO "https://raw.githubusercontent.com/erolkavvas/microbial_AMR_ML/master/data/$f"; \
  done && cd ..
python3 replicate_fast.py             # ~6 s : MI recovery of primary genes
python3 replicate_svm.py               # ~70 s : ensemble SVM, ubiA/EMB etc.
```

## 9. Failure-mode escape hatches
- If `SGDClassifier` L1 selection frequencies look empty for a drug: check preprocessing removed too many alleles; verify R/S counts ≥ 100 each; drop to 100 sims to smoke-test then re-run at 200.
- If MI dominated by rpoB/pncA across drugs: **expected** (MDR confound); confirm SVM preprocessing includes remove-other-drugs'-primary-gene.
- If a drug's primary gene is missing entirely: check pan-genome coverage (rrs is protein-invisible; rpoB/pncA/gyrA/katG/embB/rpsL/inhA/ethA/gid/ubiA/embR are all present).
