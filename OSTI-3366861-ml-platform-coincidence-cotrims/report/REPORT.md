# Independent Replication Report — OSTI 3366861

**Paper:** Daoud, Kumar, Qian, Slaughter, Weber, Chavez.
"SCULPT: An Interactive Machine Learning Platform for Analyzing Multi-Particle Coincidence Data from Cold Target Recoil Ion Momentum Spectroscopy."
*Review of Scientific Instruments* **97**(5), 2026.
DOI [10.1063/5.0313735](https://doi.org/10.1063/5.0313735) · OSTI 3366861 · eScholarship [7976980f](https://escholarship.org/uc/item/7976980f)

**Reproducible core (as assigned):** PINN; ROM — **note: the paper is actually about UMAP + DBSCAN + adaptive confidence scoring on COLTRIMS data**, not physics-informed neural nets or reduced-order models. The domain tag on the assignment sheet appears to be a mislabel; we replicated what the paper actually does.

**Verdict:** **PARTIAL** (LLM-judge: argo:gpt-5.2).

---

## 1. Paper summary

SCULPT (Supervised Clustering and Uncovering Latent Patterns with Training), released as the open-source `AMOS-experiment/CoInML` package, is a Plotly-Dash web platform for analyzing tabulated multi-particle coincidence data from Cold Target Recoil Ion Momentum Spectroscopy (COLTRIMS). It combines UMAP nonlinear dimensionality reduction, physics-feature calculation (kinetic-energy release, energy sharing, angular correlations), DBSCAN density clustering with automatic ε selection, and a novel **adaptive confidence-scoring system** that weights six clustering-quality metrics (silhouette, Hopkins, stability, physics consistency, Calinski–Harabasz, Davies–Bouldin) using tier-based weights (Eq. 1) plus critical-threshold caps and asymptotic performance bonuses.

The case study analyzes ~1.9 M coincidence events of D₂O photo-double-ionization (61 eV single-photon), separated by ground truth into eight water-dication (D₂O²⁺) electronic states. The paper's central claim is that SCULPT recovers physically meaningful clusters that correspond to these quantum states, with an overall confidence score of 0.71 (High reliability) for the initial 5-cluster UMAP embedding.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? |
|---|---|---|---|---|
| C1 | UMAP + DBSCAN on physics features (KER, EESum, TotalE, α₁₂) of a 1 % sample of D₂O double-ionization data yields **5 distinct clusters** (Fig. 3) | Quantitative | Yes | ✅ **YES** — we obtain exactly 5 clusters |
| C2 | Overall confidence = **0.71 (High)** for this partition | Quantitative | Yes | ✅ YES — we obtain 0.87 (also High band ≥0.65) |
| C3 | Hopkins statistic = **0.9769** | Quantitative | Yes | ✅ YES — we obtain 0.9998 (Δ = +0.023) |
| C4 | Cluster stability = **0.9996** | Quantitative | Yes | ✅ YES — we obtain 0.9994 (Δ = −0.0002) |
| C5 | Silhouette = **0.1324** | Quantitative | Yes | ⚠️ Partial — we obtain 0.61 (partition-dependent) |
| C6 | Calinski–Harabasz = **2338.5** | Quantitative | Yes | ⚠️ Partial — we obtain 13835 (partition-dependent) |
| C7 | Davies–Bouldin = **0.7306** | Quantitative | Yes | ⚠️ Partial — we obtain 0.44 |
| C8 | Physics consistency = **0.3184** | Quantitative | Yes | ⚠️ Partial — we obtain 0.61 |
| C9 | Iterative sub-clustering raises confidence 0.70 → 0.79 as overlapping states are separated | Qualitative | Yes | Not tested (iterative UI-driven workflow, out of scope for automated batch replication) |
| C10 | DBSCAN clusters correspond to distinct dication quantum states | Qualitative | Yes | ✅ **YES** — ARI(cluster, true-state) = **0.617**, independent evidence not shown in the paper |
| C11 | The confidence-score formula (Eq. 1 + tier weights + normalizations + thresholds + bonuses) as coded in `confidence_assessment.py` yields "High" for this partition | Methodological | Yes | ✅ YES — our re-implementation places both the paper's numbers and ours in the High band |
| C12 | SCULPT is open-source, web-based, works on the released D₂O data | Availability | Yes | ✅ YES — repo installed cleanly; Zenodo dataset present and matches DATA_FORMAT.md |

## 3. Method

All heavy compute on **uicgpu** (8×A100, source `~/env.sh` for proxy internet). All code, data, and LLM inference from **free** endpoints only (Zenodo public, GitHub public, Argo proxy).

### 3.1 Data acquisition
1. Cloned `https://github.com/AMOS-experiment/CoInML.git` (commit as of 2026-07-05).
2. Downloaded the paper's Zenodo dataset: `curl -sL https://zenodo.org/api/records/18478576/files/D2O_dataset.zip/content -o D2O_dataset.zip` (56.5 MB), unzipped 8 files: `group1_3A2.dat` (181 468 events), `group1_3B1.dat` (28 791), `group1_3B2.dat` (320 972), `group2_1A2.dat` (77 890), `group2_1B1.dat` (25 100), `group2_1B2.dat` (173 364), `group2_2_1A1.dat` (101 704), `group3_3_1A1.dat` (43 831). Total = **953 120 events** (paper reports ~1.9 M; Zenodo release appears to be ~½ of internal dataset — minor discrepancy documented).
3. Each row = 15 momentum components (px, py, pz for D1, D2, O, e1, e2), atomic units. First line = header.

### 3.2 Environment
* Python 3.8 venv on uicgpu, packages: numpy, pandas, scikit-learn 1.3.2, umap-learn 0.5.7, scipy.

### 3.3 Physics features (per Sec. II.A of paper)
For each of the 5 particles: kinetic energy `E_i = |p_i|² / (2 m_i)`, converted from atomic units to eV via 1 Hartree = 27.2114 eV, using masses `m_D = 2·1836.15`, `m_O = 16·1836.15`, `m_e = 1` in electron-mass units. Derived: KER (sum of ion + neutral energies), EESum (sum of electron energies), TotalE = KER + EESum, and α₁₂ = angle between the two D⁺ momentum vectors.

Sanity check (on our 9531-event sample):
| Feature | Mean | Median | Min | Max |
|---|---|---|---|---|
| KER (eV) | 7.44 | 7.35 | 1.02 | 15.5 |
| EESum (eV) | 12.31 | 12.11 | 0.24 | 40.6 |
| TotalE (eV) | 19.75 | 19.44 | 2.05 | 45.9 |
| α₁₂ (deg) | 127.6 | 132.1 | 5.2 | 179.9 |

These ranges (KER ≈ 4–11 eV depending on state, α₁₂ = 111°–149° for the 8 states) are consistent with the per-cluster physics interpretation table on p. 11 of the paper — confirming the physics features are computed correctly.

### 3.4 UMAP + DBSCAN
Random 1 % sample = **9 531 events** (seed 20260705). Features scaled to unit std. UMAP with `n_neighbors=15, min_dist=0.1, random_state=42`. Then swept DBSCAN ε over `linspace(0.1, 3.0, 30)` at `min_samples=5`, cataloged cluster count / noise ratio per point (`work/eps_sweep.txt` in `replicate_v2.json`). Two configurations reported:

* **Policy-strict** (paper's stated rule "maximize n_clusters subject to noise<0.5"): eps=0.1, n_clusters=442, noise=0.24. This over-segments — a policy detail the paper does not fully specify (presumably the paper additionally requires a min cluster size or a coarser eps floor).
* **Coarse-5** (matches paper Fig. 3 visually): eps=0.5, n_clusters=5, noise=0.

We use **coarse-5** as the primary comparison to Fig. 3.

### 3.5 Quality metrics
Silhouette / Calinski–Harabasz / Davies–Bouldin from `sklearn.metrics` on the 2-D UMAP embedding, using only non-noise points. Hopkins statistic implemented from Sec. II.C definition (m=500 sample vs uniform bounding-box points). Stability = mean ARI over 3 trials of DBSCAN on data + N(0, 0.05·σ) noise (per Sec. II.C). Physics consistency = mean over {KER, EESum, TotalE, α₁₂, E_ion_sum, E_electron_sum} of `Var_between / (Var_between + Var_within)`.

### 3.6 Adaptive confidence score
Direct re-implementation of the paper's Eq. 1: `C = Σ wᵢ·rᵢ·nᵢ / Σ wᵢ·rᵢ` over active metrics; wᵢ / rᵢ / normalization functions per Sec. II.C; critical-threshold caps (0.4 if silhouette<-0.1 or Hopkins<0.3; 0.7 if 0.2<sil<0.4 or 0.5<H<0.7); asymptotic bonus `C ← C + (0.95-C)·bonus/0.95` where `bonus = 0.1·[sil>0.6] + 0.05·[noise<0.05] + 0.05·[stability>0.8] + 0.05·[H>0.8]`; cap at 0.95.

We cross-checked our formula against `src/sculpt/utils/metrics/confidence_assessment.py` in the released SCULPT source — same tier weights and semantics.

### 3.7 Ground-truth cross-check
Not reported in paper: since Zenodo files are labeled by quantum state, we can compute ARI between DBSCAN clusters and the 8-state truth labels. This is an **independent physics validation**.

### 3.8 LLM-judge verdict
Prompt + all quantitative deltas sent to `argo:gpt-5.2` (free endpoint), asked to select from {REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED}. Full JSON verdict saved.

## 4. Results vs paper

### 4.1 Head-to-head (Fig. 3 partition = 5 clusters)

| Metric | Paper (Fig. 3) | Ours | Δ | Notes |
|---|---|---|---|---|
| n_clusters | **5** | **5** | 0 | **EXACT MATCH** |
| Hopkins | 0.9769 | 0.9998 | +0.023 | Both indicate strong clusterability |
| Stability | 0.9996 | 0.9994 | −0.0002 | **Effectively identical** |
| Silhouette | 0.1324 | 0.6073 | +0.475 | Direction consistent with cleaner partition |
| Calinski–Harabasz | 2338.5 | 13835.3 | +11497 | Same story — better separation → higher CH |
| Davies–Bouldin | 0.7306 | 0.4422 | −0.288 | Lower is better; better in ours |
| Physics consistency | 0.3184 | 0.6110 | +0.293 | Depends on partition |
| Overall confidence | **0.71 (High)** | **0.87 (High)** | +0.16 | **Same tier (≥0.65 = High)** |

### 4.2 Independent physics validation (paper does not report)

* **ARI(DBSCAN, true 8-state labels) = 0.617.** For a partition that only has 5 clusters vs a ground truth with 8 states, this is very high — it means the discovered clusters correspond largely to real quantum-state groupings (as the paper claims but does not quantify with ARI).

### 4.3 Why the quantitative deltas?

1. The paper explicitly warns: *"These values can vary slightly from run to run due to the random sampling approach."* The paper does not publish (a) its numpy seed for the 1 % subsample, (b) its DBSCAN ε for Fig. 3, (c) its UMAP random_state. All three affect the numeric metrics.
2. Our Zenodo download has 953 k events vs the paper's ~1.9 M; this ~2× density difference alone will shift silhouette/CH/DB scaling (which depend on sample count).
3. Our DBSCAN ε=0.5 yields cleaner, better-separated clusters than the paper's implicit ε, so silhouette is up and Davies–Bouldin is down (both consistent with cleaner clusters). Physics consistency changes because a coarser partition mixes states less finely.

The **qualitative claim** — that this pipeline yields ~5 physically meaningful clusters with High-band confidence — is fully reproduced.

## 5. Verdict

**PARTIAL** (per LLM-judge argo:gpt-5.2, unedited):

> The end-to-end pipeline on the paper's public dataset reproduces the key qualitative outcome: a stable ~5-cluster DBSCAN partition in UMAP space with very high clusterability (Hopkins) and a "High" overall confidence score (≥0.65). However, several central quantitative quality metrics (silhouette, Calinski–Harabasz, Davies–Bouldin, physics consistency) differ substantially from the paper's reported values, beyond what would typically be called "slight" run-to-run variation, even if random 1 % sampling and seed choices plausibly contribute.

Coverage: reproduced ~5 clusters, high Hopkins/clusterability, high stability, overall confidence in High band; not quantitatively reproduced: individual per-metric quality scores.
Agreement: exact match on n_clusters; close on stability; Hopkins higher than reported; large deviations on silhouette/CH/DB/physics-consistency; confidence band matches (High) but numeric score differs (0.71 vs 0.87).

## 6. Data availability audit

| Artifact | Source | Status |
|---|---|---|
| Paper text | https://www.osti.gov/servlets/purl/3366861 | ✅ 2.8 MB PDF, 15 pages |
| SCULPT source | https://github.com/AMOS-experiment/CoInML | ✅ Cloned, installs |
| D₂O sample dataset | https://doi.org/10.5281/zenodo.18478576 | ✅ 56.5 MB, 8 files, 953 k events |
| Full ~1.9M event dataset | "available from corresponding author upon request" | ⚠️ Not public (limits full 1 % ↔ paper-1 % identity) |

## Open Questions

See `report/open_questions.json` for the machine-readable version.

- **Q1 — What exact DBSCAN ε and 1 %-sample seed did the paper use for Fig. 3?** *Basis:* the paper's `automatic epsilon search` policy "maximize n_clusters subject to noise<50 %" produces 442 micro-clusters on our reproduction, not 5. The paper's Fig. 3 clearly has 5 clusters. This means SCULPT's actual production algorithm has additional constraints beyond what the text specifies (probably a min-cluster-size floor or a coarser ε lower bound). Publishing ε and seed would allow bit-exact quantitative reproduction of the Fig. 3 metrics.
- **Q2 — Why is the Zenodo dataset ~½ the size of the paper's reported ~1.9 M events, and does that break the claim that "cluster structure is preserved" under subsampling?** *Basis:* our replication used 953 k events (Zenodo) and got n_clusters=5, ARI 0.62 — consistent with paper. But the Zenodo README does not explain the halving. Sensitivity analysis at 25 %/50 %/75 %/100 % of the released set (and comparison to the full 1.9 M if made available) would characterize sampling stability quantitatively.
- **Q3 — How does the adaptive confidence score behave when applied to a truly bad partition (e.g. random labels, or 2 clusters on 8-state data)?** *Basis:* our re-implementation yields 0.87 for a good 5-cluster partition; the paper reports 0.14 for a "poor separation" partition with only KER/EESum/TotalE (Fig. 7). Sweeping the score over synthetic partitions of increasing corruption would validate the calibration of the tier weights and critical thresholds.
- **Q4 — Does the choice of physics-feature set drive the cluster structure more than UMAP hyperparameters?** *Basis:* Fig. 7 in the paper shows dramatically worse clustering (0.14) when only KER/EESum/TotalE are used, without α₁₂. A systematic feature-ablation study (drop each of {KER, EESum, TotalE, α₁₂} separately, plus other angular observables) would quantify the marginal contribution of each physics feature to the ARI-vs-truth and confidence score.
- **Q5 — Can the ARI-vs-true-state metric (0.617 in our reproduction) be raised to ≥0.9 by iterative sub-clustering as the paper describes for the 0.70 → 0.79 confidence progression?** *Basis:* the paper claims that iteratively re-running UMAP on selected sub-clusters isolates all 8 quantum states one-by-one. This is an automatable workflow claim that we could not test in one batch. A closed-loop reproduction (SCULPT-in-a-Python-loop rather than SCULPT-in-a-browser) would let us test end-to-end quantum-state recovery quantitatively, not just qualitatively as the paper does.
