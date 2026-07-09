# Attempt Log — BVBRC-25 (Kavvas et al. 2018, Mtb pan-genome ML AMR)

Analyst: Ollie (OpenClaw AI subagent). Date: 2026-07-01 (night wave).

## Chronology

1. **Read wave brief + BVBRC-17 exemplar** to match structure/rigor. Target: genuine rerun on real public data, LLM-judged verdict, free endpoints only.

2. **Located paper.** Europe PMC `EXT_ID:30333483` → PMCID **PMC6193043**, Nat Commun 9:4306, open access. Pulled bibliographic JSON + full-text XML (136,903 bytes).

3. **Parsed Methods from XML.** Extracted the exact pipeline:
   - Data: 1,595 Mtb strains from **PATRIC/BV-BRC**, 13 antibiotics R/S.
   - Pan-genome: **CD-HIT v4.6, 0.8 identity, word length 5** → 11,039 clusters.
   - Allele pan-genome: exact-amino-acid variants per cluster.
   - Association: **Mutual Information (NPEET), chi-squared, ANOVA F-test**, Bonferroni.
   - ML: **ensemble L1-SVM, SGD, 200 sims, 80% bootstrap, balanced class weight**; preprocessing removes each drug's primary gene from *other* drugs' analyses + removes PE/PPE/PGRS/transposase/hypothetical.
   - Code: `github.com/erolkavvas/microbial_AMR_ML`.

4. **Discovered the authors published their processed data** in that GitHub repo:
   `pangen_allele_df.csv` (1595×15,367), `pangen_cluster_df.csv` (1595×11,039),
   `cluster_info.csv` (cluster→Rv/gene/product/pan), `resistance_data.csv`, `strain_information.csv`.
   → This enables a **real re-implementation of the core pipeline on the real data** (our own code, not their notebooks).

5. **Downloaded all 5 data files** (checksums in artifact_harvest.md). Verified shapes:
   1595 strains, 11,039 clusters (Core 3419 / Accessory 2402 / Unique 5218), 15,367 alleles.

6. **First MI attempt local (laptop):** used `sklearn.mutual_info_classif` — pegged 1 core at 100% CPU, too slow (killed after ~2 min per drug). Lesson: per-feature sklearn MI loop doesn't scale to 15k features × 10 drugs.

7. **Moved to uicgpu** (255 cores, 2 TB RAM; `source ~/env.sh` for proxy). Rewrote MI as an **exact vectorized binary–binary discrete MI** (matrix form, bits) + vectorized chi-squared with Bonferroni. Ran all 10 drugs in **5.5 s**.
   - Result: MI recovers primary AMR gene at/near rank 1 for the first-line drugs (see REPORT §4.2).
   - Noted `rrs` (16S rRNA) is absent from the protein pan-genome → explains why amikacin/kanamycin/capreomycin (rrs-driven) don't surface; a real, expected limitation of a protein-allele method, not a replication failure.

8. **Pan-genome conservation check** (Result #1): recomputed core fraction + PE/PPE/PGRS enrichment across pan categories from cluster_info → confirmed variation concentrates in PE/PPE/PGRS (3.3% of core → 24.5% accessory → 30.6% unique).

9. **Ensemble L1-SVM (Result #2 ML half).** Implemented paper's preprocessing (drop PE/PPE/PGRS/transposase/hypothetical/mobile; remove other drugs' primary genes) + 200-sim L1-SGD-SVM, 80% bootstrap, balanced weights, gene-level selection frequency.
   - First run **sequential**: too slow (~9 min still on drug 1). Killed.
   - Rewrote with **joblib Parallel (n_jobs=64)**, max_iter=50. All 7 drugs in **70 s**.
   - Result: SVM recovers **additional** known genes beyond MI — isoniazid+inhA, rifampicin+rpoC, ethambutol+**ubiA** (the paper's flagship example), streptomycin+gid — exactly the paper's claim.

10. **Harvested evidence** back to `report/evidence/`: association_results.json, svm_results.json, pangenome_stats.json, run_logs.txt. Wrote report.

## What worked
- Authors' processed matrices are complete and load cleanly → full core-pipeline rerun feasible.
- Independent vectorized MI reproduces the paper's primary-gene recovery.
- Independent ensemble L1-SVM reproduces the paper's "SVM finds additional known genes" claim, including the specific ubiA/ethambutol case.
- Pan-genome conservation + PE/PPE/PGRS enrichment reproduced from raw cluster table.

## What was out of reach / limitations
- **rrs-driven drugs** (amikacin/kanamycin/capreomycin): rrs is rRNA, not in the protein pan-genome; primary signal not recoverable from this allele matrix. Paper handles second-line drugs with the same caveat.
- Full **RAxML core-SNP phylogeny** (21,206 SNPs, 2803 core genes) not rebuilt — orthogonal to the AMR-signature claims and compute-heavy.
- **3-D structural mutation mapping** (Result #4) and the exhaustive **epistasis** logistic-regression sweep (Result #3, 97 interactions) not rerun — require structure files + the full gene-gene sweep; noted as gap.
- We used the authors' pan-genome matrices rather than rebuilding CD-HIT clustering from 1595 raw proteomes. Rebuilding CD-HIT is feasible but adds days; the matrices are the paper's own published intermediate.
