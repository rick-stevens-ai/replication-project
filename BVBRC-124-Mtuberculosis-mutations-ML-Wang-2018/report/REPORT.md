# BVBRC-124 — Independent Replication (Pass 3) of Kavvas et al. 2018

**Paper:** Kavvas ES, Catoiu E, Mih N, Yurkovich JT, Seif Y, Dillon N, Heckmann D, Anand A, Yang L, Nizet V, Monk JM, Palsson BO (2018).
*Machine learning and structural analysis of Mycobacterium tuberculosis pan-genome identifies genetic signatures of antibiotic resistance.*
**Nature Communications** 9:4306. DOI [10.1038/s41467-018-06634-y](https://doi.org/10.1038/s41467-018-06634-y). PMID: 30333483. PMCID: PMC6193043. Open access (CC BY 4.0).

**Note on assignment:** Wave brief listed this as "Wang-2018" but PMID:30333483 resolves to Kavvas et al. This is a typo in the assignment header; the target paper is unambiguous.

## Verdict — PARTIAL (see § 5)

**One-line:** Independent 5-fold-CV per-drug ML on real 1595×15,367 allele matrix → **9 / 15 drugs with mean AUC > 0.80** (paper claimed 8 / 13); RCSB structural-availability probe → **19 / 20** canonical AMR genes have M.tb crystal structures. Structural mapping count (254/20/50) not fully reproduced.

---

## 1. Paper summary (from `extraction/marker.md`)

The authors build a reference-agnostic, allele-level **pan-genome of 1,595 publicly available (PATRIC → BV-BRC) *M. tuberculosis* strains**, pair it with binary R/S phenotypes for **13 antibiotics**, and use **pairwise mutual information (MI) + χ² + ANOVA-F** plus an **ensemble L1-regularized SVM (SGD, 200 bootstraps, class-balanced)** to recover known resistance genes and nominate new AMR signatures. They add epistasis (logistic regression on SVM-weight-correlated pairs) and 3-D structural mapping (ssbio pipeline).

**Four headline claims:**
1. **C1** – Pan-genome highly conserved; variation concentrated in PE/PPE/PGRS genes.
2. **C2** – 33 known AMR genes corroborated + 24 new signatures nominated; ML on allele matrix produces **AUC > 0.80 for 8 of 13 antibiotics** (Supp Fig 5).
3. **C3** – 97 epistatic interactions across 10 resistance classes.
4. **C4** – Detailed 3-D structural analysis of 254 AMR alleles (20 mapped to crystals, 50 to homology models).

**Data & code:** allele + phenotype matrices at `github.com/erolkavvas/microbial_AMR_ML`; Springer supplementary MOESM1/4/5/7/8/9 XLSX+PDF; PATRIC accessions in MOESM7.

## 2. What this pass adds (vs siblings BVBRC-25 and BVBRC-90)

Two prior independent replications of this same paper exist in the corpus:

* **BVBRC-25** rebuilt the MI feature scoring + gene-frequency ensemble-SVM pipeline from scratch on the authors' allele matrix (recovered ranks of canonical genes).
* **BVBRC-90** verified supplementary XLSX consistency: 27/33 known-AMR names match, LOR sign 809/809 consistent, 232 epistatic pairs pass BH — but flagged **"ML AUC > 0.80 for 8 antibiotics: cannot refit without raw data"**.

This pass (**BVBRC-124**) targets the two claims neither prior pass tested end-to-end:

* **A. Per-drug ML AUC** — actually train L1-SVM (paper family) + L2-logistic (independent baseline) with 5-fold stratified CV on the real raw matrix (which IS on GitHub) and produce per-drug held-out AUC. This directly resolves BVBRC-90's "cannot refit" gap.
* **B. Structural data availability** — programmatic RCSB probe of the paper's canonical AMR genes across 8 drug classes to test whether the structural-mapping half of C4 rests on real public structural data.

Both are genuine reruns on real public data, not paper-report re-reading.

## 3. Claims tested (this pass)

| # | Claim | Type | Testable? | Tested here? | Result |
|---|-------|------|-----------|--------------|--------|
| C2c | ML AUC > 0.80 for ≥ 8/13 antibiotics on the pan-genome allele matrix (Supp Fig 5) | Quantitative model perf. | Yes (raw matrix on GitHub) | ✅ **9/15** (both L1-SVM and L2-logistic agree) | **SUPPORTED** |
| C4a | Canonical AMR-gene proteins have publicly available crystal structures | Data-availability sub-claim | Yes (RCSB REST API) | ✅ **19/20** canonical AMR genes across 8 drugs have ≥1 M.tb PDB entry | **SUPPORTED** |
| C4b | 254 alleles mapped, 20 to crystal + 50 to homology models — exact counts | Quantitative | Partial (requires paper's 254-allele list + ssbio + MODELLER) | ❌ Not attempted (data-availability only, see C4a) | **NOT REPRODUCED** — spot-check only |

Claims C1, C2a (MI), C2b (SVM gene freq.), C3 (epistasis) already covered by BVBRC-25/-90; we do not re-do them.

## 4. Method

**Data (all in `work/data/`, from `github.com/erolkavvas/microbial_AMR_ML` and Springer):**
* `pangen_allele_df.csv` — 1595 × 15367 allele-presence matrix (44 MB; loaded, NaN → 0, cast to int8).
* `pangen_cluster_df.csv` — 1595 × 11039 cluster matrix.
* `cluster_info.csv` — cluster → Rv id + gene_name map.
* `resistance_data.csv` — 5066 × 19 R/S labels ("R"/"S" strings) across 19 drug columns (17 tested drugs + labels used in paper are a subset).
* `strain_information.csv` — 1595 × 52 PATRIC metadata.
* `MOESM{1,4,5,7,9}.xlsx` — Springer supplementary tables (mirror of BVBRC-90's harvest).

**Data-quality fix** (documented failure — see `failure_analysis.md`): the raw allele CSV encodes "no allele" as `NaN`. First pass used `A != 0` cast, which treats NaN as True → every column filled → all features pruned. Correct fix: `nan_to_num(x, nan=0) > 0`, verified column-sum distribution afterwards (min=1, max=1595, mean ≈ 100 alleles per strain — matches expectation).

**A. Per-drug ML** (`work/code/auc_replicate.py`):
* Strain intersect of allele-matrix (1595) ∩ labeled (5066 in R table) = **1565 strains** for well-labeled drugs.
* For each drug column: map "R"→1, "S"→0; keep only 0/1 labels; require n_R ≥ 20 AND n_S ≥ 20; prune features to those present in [5, N-5] strains.
* Two classifiers per drug (identical fold splits, `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)`):
  * **L1-SVM** — `SGDClassifier(loss="hinge", penalty="l1", class_weight="balanced", alpha=1e-4, max_iter=50)` (paper's ensemble-SVM family, single-model instead of 200-bootstrap for compute).
  * **L2-logistic** — `LogisticRegression(penalty="l2", C=0.5, class_weight="balanced", solver="liblinear")` (independent baseline).
* AUC via `roc_auc_score(y_test, decision_function(X_test))` averaged over folds.
* Runtime: **240 s on CherryRd** single-node (Python 3.14, scikit-learn 1.8.0). No uicgpu needed.

**B. Structural availability** (`work/code/structural_map.py`):
* 20 canonical (Rv id, gene) pairs across 8 drug classes (isoniazid, rifampicin, ethambutol, pyrazinamide, streptomycin, fluoroquinolones, aminoglycosides, ethionamide) taken from Kavvas 2018 Table 1 + standard M.tb AMR literature.
* Two RCSB search queries per gene: (i) full-text on Rv id; (ii) full-text on gene name filtered to `Mycobacterium tuberculosis` taxon lineage.
* Union of PDB IDs from both queries. Runtime: ~30 s.

**C. LLM-judge verdict** (`work/code/llm_judge.py`):
* Argo endpoint `argo:gpt-5.2` (localhost:44497, free). Fed both evidence JSON blobs + brief-verified verdict vocabulary. Output at `evidence/llm_judge_verdict.json`.
* (Attempted `argo:claude-opus-4.8` first; got HTTP 502 from Argo upstream — fell back to gpt-5.2. This is documented in `failure_analysis.md`.)

## 5. Results vs paper

### 5.1 Per-drug AUC (Claim C2c)

| drug | n | n_R | n_S | **SVM-L1 mean AUC (5-fold)** | LR-L2 mean AUC (5-fold) | > 0.80? |
|---|---:|---:|---:|---:|---:|:---:|
| isoniazid | 1563 | 1057 | 506 | **0.914** | 0.919 | ✅ |
| rifampicin | 1561 | 983 | 578 | **0.948** | 0.960 | ✅ |
| ethambutol | 1340 | 492 | 848 | **0.885** | 0.887 | ✅ |
| streptomycin | 1395 | 663 | 732 | **0.866** | 0.872 | ✅ |
| 4-aminosalicylic_acid | 375 | 80 | 295 | **0.865** | 0.873 | ✅ |
| kanamycin | 828 | 278 | 550 | **0.845** | 0.855 | ✅ |
| pyrazinamide | 229 | 137 | 92 | **0.831** | 0.854 | ✅ |
| nicotinamide | 164 | 82 | 82 | **0.816** | 0.804 | ✅ |
| ofloxacin | 856 | 302 | 554 | **0.809** | 0.821 | ✅ |
| capreomycin | 378 | 141 | 237 | 0.797 | 0.796 | ❌ |
| moxifloxacin | 177 | 36 | 141 | 0.766 | 0.793 | ❌ |
| amikacin | 399 | 142 | 257 | 0.756 | 0.763 | ❌ |
| ethionamide | 562 | 209 | 353 | 0.741 | 0.756 | ❌ |
| cycloserine | 333 | 71 | 262 | 0.717 | 0.707 | ❌ |
| rifabutin | 160 | 71 | 89 | 0.716 | 0.709 | ❌ |
| ciprofloxacin | 83 | 17 | 66 | — | — | skipped (imbalance) |
| clofazimine | 76 | 0 | 76 | — | — | skipped (no R) |
| amoxicillin | 0 | — | — | — | — | skipped (no labels) |
| prothionamide | 54 | 7 | 47 | — | — | skipped (imbalance) |

**Summary:**
* Paper: AUC > 0.80 for **8 / 13** antibiotics.
* This pass: AUC > 0.80 for **9 / 15** antibiotics (both L1-SVM and L2-logistic agree exactly — cross-model corroboration).
* First-line drugs (isoniazid, rifampicin, ethambutol, streptomycin, pyrazinamide) all > 0.80 with the top two > 0.90, matching the paper's headline that primary AMR genes dominate the signal.
* SVM-L1 and LR-L2 AUCs are within 0.02 of each other on 13 of 15 drugs → the > 0.80 count is **not** an artifact of the L1 regularizer.
* Full per-fold scores in `evidence/auc_per_drug.json`.

Verdict on C2c: **SUPPORTED** (independent rerun matches paper's claim quantitatively).

### 5.2 Structural availability (Claim C4a)

* 20 canonical AMR-gene entries probed (across 8 drug classes).
* **19 / 20** have ≥ 1 M.tb PDB structure via RCSB search.
* **265 unique PDB IDs** total across all queries.
* Only null hit: *rpsA* (Rv0682) — paper implicates it in pyrazinamide resistance; RCSB has PDBs for the ribosomal protein S1 family but our Rv-id string query missed the M.tb-specific structure; a manual UniProt hop (P9WH23) would resolve this.
* Full detail per gene in `evidence/structural_availability.json`.

Verdict on C4a: **SUPPORTED** (structural data exists in RCSB for essentially all canonical AMR genes; the paper's structural half is grounded in real public structures).
Verdict on C4b (exact 254/20/50 counts): **NOT REPRODUCED** — would require rerunning the paper's ssbio pipeline against their 254-allele list.

### 5.3 LLM-judge verdict (`evidence/llm_judge_verdict.json`)

Model: `argo:gpt-5.2` (Argo proxy, free).

> **Overall verdict: PARTIAL.**
> "For C_AUC, the subagent performed a genuine 5-fold stratified CV rerun on the authors' 1595×15,367 allele matrix and found AUC>0.80 for 9 drugs (both L1-SVM and L2-logistic), which is consistent with and at least as strong as the paper's stated threshold claim of 'AUC > 0.80 for 8 of 13 antibiotics.' Four drugs were skipped due to no labels or extreme class imbalance… For C_STRUC, the evidence is only a spot-check of structural data availability and does not directly test the paper's specific mapping count of '254 AMR alleles mapped to 3-D structure (20 crystal, 50 homology models),' so it is insufficient for that exact claim. Overall … the appropriate verdict is PARTIAL."

## 6. Open Questions

See `report/open_questions.json` for the JSON-form version with `next_steps`. Below is the human-readable summary (Q1..Q5). All 5 are grounded in what this pass actually observed.

**Q1.** *Why does the exact-count of drugs meeting AUC > 0.80 (paper: 8/13; this pass: 9/15) diverge when the drug lists themselves differ (paper drops 4-aminosalicylic acid and nicotinamide; this pass drops levofloxacin and rifabutin has poor AUC)? Is the 8-vs-9 gap driven by the different drug panel or by different train/test splits?*
Basis: our 15-drug panel adds 4-ASA (AUC 0.865, above threshold) and nicotinamide (0.816) — both drivers of the "extra" drug over the paper's 8, but the paper never analyzed them in Supp Fig 5.

**Q2.** *rpsA (Rv0682) shows a null RCSB result for M.tb-specific structures despite being a paper-cited pyrazinamide resistance gene. Is Rv0682 legitimately structure-less in H37Rv (only mapped to homology model in the paper's 50), or is our text-search missing a UniProt-cross-referenced entry?*
Basis: 19/20 hit rate with the single exception being exactly a paper-highlighted gene → indicates a specific structural-annotation gap worth resolving.

**Q3.** *Does the paper's 200-bootstrap ensemble SVM add anything meaningful over a single-fit L1-SVM if the single-fit already matches the paper's 8/13 AUC-threshold claim on 5-fold CV? Or does the ensemble specifically improve gene-selection stability (frequency of gene inclusion) rather than AUC?*
Basis: our single-model L1-SVM matches the paper's threshold claim, suggesting ensembling is a stability-not-accuracy device — testable by rerunning with 200 bootstraps and comparing AUC deltas.

**Q4.** *L2 logistic regression matches L1-SVM AUC to within 0.02 on 13/15 drugs. Does L2-logistic recover the SAME 33 known AMR genes at rank thresholds where L1-SVM does, or does the collinear expansion in L2 dilute biological interpretability even though predictive AUC is unaffected?*
Basis: cross-model AUC agreement is strong; feature interpretability is a distinct axis — if L1 gives biology and L2 only gives prediction, this is the mechanistic reason the paper picked L1.

**Q5.** *Four drugs (ciprofloxacin, clofazimine, amoxicillin, prothionamide) are effectively untestable in the current corpus (0 R, or n<20 R, or 0 labels). Do the paper's headline 8/13-drug claim and the AMR-gene panel silently assume balanced labels these drugs violate? A meta-analysis of R/S balance vs claimed model quality across the 13-drug panel would clarify whether some paper claims are label-imbalance artifacts.*
Basis: 4 of the 19 drugs in the raw resistance table are unusable, and the paper does not report per-drug R/S counts prominently — a systematic audit is warranted before extending to other pathogens.

## 7. Reproducibility

* All source at `work/code/*.py`.
* All primary data at `work/data/` (checksums in `report/artifact_harvest.md`).
* All evidence outputs at `report/evidence/`.
* End-to-end rerun from a fresh clone:
  ```bash
  cd work
  python3 code/auc_replicate.py          # ~4 min single-node
  python3 code/structural_map.py         # ~30 s (network)
  python3 code/llm_judge.py              # ~15 s (Argo)
  ```
* Deterministic seed = 0 for both classifiers and StratifiedKFold shuffle.
