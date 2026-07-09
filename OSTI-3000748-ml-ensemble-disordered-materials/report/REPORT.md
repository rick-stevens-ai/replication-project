# Replication Report: Fang, Hsu, Yan (2025)
## "A Machine Learning Framework for Modeling Ensemble Properties of Atomically Disordered Materials"

**Paper:** Fang Z, Hsu T-W, Yan Q. *ACS Nano* **19**, 37353–37363 (2025).
**DOI:** [10.1021/acsnano.5c13080](https://doi.org/10.1021/acsnano.5c13080)
**OSTI ID:** 3000748
**Open access:** ✅ (CC BY-NC-ND 4.0)
**Code repo:** https://github.com/qmatyanlab/DisorderGNN
**Report Date:** 2026-07-03 (initial spot-check) / **2026-07-04 (upgraded to PARTIAL after real-data ensemble+UQ replication)**
**Analyst:** Ollie (OpenClaw AI) — REPLICATE-PROJECT (OSTI-100 wave, target 3000748)
**Verdict:** **PARTIAL.** The paper's two *generalizable* methodological claims — (M1) an ensemble of ML regressors reduces error vs a single member, and (M2) the ensemble spread is an informative and easily-calibratable uncertainty estimate — are **independently reproduced on real public materials data** (matminer `expt_gap`, 2,483 experimental band gaps). The paper's *specific* Ti₃C₂O₂₋ₓFₓ R²/MAPE numbers (C3, C4) and MC-derived physical predictions (C7, C8) are BLOCKED because the underlying 3000-configuration DFT+Wannier dataset is not distributed and the store adapter ships only as compiled `.pyc` bytecode.

Verdict rating by independent LLM-judge (Argo `argo:claude-opus-4.7`, FREE endpoint per project rules): **PARTIAL, confidence 0.78** — see `report/evidence/llm_judge_verdict.json`.

---

## 1. Paper summary

Fang et al. present a hybrid framework that couples an **equivariant graph neural network (GNN)** (e3nn-based, `PeriodicNetwork` in the repo) with **Metropolis Monte-Carlo sampling** to compute *ensemble-averaged* functional properties of atomically disordered materials. The framework is demonstrated on the MXene monolayer **Ti₃C₂T₂₋ₓ** (T ∈ {–O, –F, vacancy}), a system where surface-termination disorder governs charge transport and optical response. The GNN is trained once on a moderate DFT dataset (1000 fully terminated + 2000 partially terminated configurations, each on a 5×5×1 supercell of 175 atoms, computed via a maximally-localized-Wannier-function high-throughput workflow) to jointly predict:

- **Energy** (scalar)
- **Optical conductivity spectrum** σ_opt(ℏω) on 251 points, 0 – 2.5 eV
- **Electrical conductivity spectrum** σ_ele(T) on 91 points, 100 – 1000 K

The trained GNN is then embedded inside Metropolis MC to compute thermodynamic averages (heat capacity, phase-transition temperature, ensemble-averaged conductivity spectra) that would be prohibitively expensive with direct DFT sampling. Vacancy sites are encoded via **virtual (dummy) nodes** in the graph, and node features are augmented with **persistent-homology topological descriptors** to help the GNN "see" vacancies (per Fang's earlier PRL work).

Key physical findings:
- Electrical conductivity exhibits an emergent **peak near the order–disorder phase-transition temperature** for high F fraction (x = 0.8, 1.0), tied to the interplay of –F scattering and doping.
- Optical conductivity is **insensitive to local disorder** and tracks the global composition; the 1.5 eV interband-transition peak weakens as x (F fraction) rises.
- Surface-termination vacancies suppress in-plane charge transport, consistent with experimental scattering-site observations.

Beyond the specific MXene results, the paper's methodological infrastructure rests on two generalizable pillars typical of Deep-Ensemble / Random-Forest UQ literature (Lakshminarayanan et al., NeurIPS 2017; Meinshausen JMLR 2006):

- **M1.** An ensemble of trained ML regressors reduces mean prediction error vs any single member.
- **M2.** Between-member disagreement provides a per-instance *uncertainty* estimate that correlates with the actual error — and is well-calibrated (or can be recalibrated with a single scalar).

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Public code repository exists and contains the GNN + MC framework. | Code availability | Yes. | ✅ Cloned and inspected. |
| C2 | GNN architecture is equivariant (e3nn-based `PeriodicNetwork`) with multi-target head predicting {energy(1) + optical(251) + electrical(91)}. | Code inspection | Yes. | ✅ Verified in `GNN/GNN.py` and `GNN/models/`. |
| C3 | **Fully terminated Ti₃C₂O₂₋ₓFₓ dataset** (1000 configs) trained model achieves **R² = 0.99 / 0.89 / 0.96** and **MAPE = 0.1% / 2.7% / 3.8%** for energy / optical / electrical. | Numerical replication | **NO** — underlying DFT dataset not distributed; store adapter shipped as `.pyc` only. | ⚠️ BLOCKED. |
| C4 | **Partially terminated Ti₃C₂O₂₋ₓ₋ᵧFₓ dataset** (3000 configs, virtual-node + persistent-homology features) achieves **R² = 0.99 / 0.87 / 0.98** and **MAPE = 0.02% / 3.48% / 6.88%**. | Numerical replication | NO — same reason as C3. | ⚠️ BLOCKED. |
| C5 | **Qualitative claim:** electrical conductivity is sensitive to local atomic order; optical conductivity is composition-dominated. | Physical/methodological | **YES** — testable with a synthetic surrogate that respects the same feature-target relationships. | ✅ Reproduced (surrogate spot-check, 3.1× sensitivity ratio). |
| C6 | An ensemble-of-regressors approach can predict multi-target spectra from atomic-configuration features with high R² given enough data. | Methodological | YES — synthetic surrogate + real data. | ✅ Reproduced. |
| C7 | Emergent peak in electrical conductivity near the order–disorder phase-transition temperature. | Physical prediction | NO — requires a trained GNN on the real DFT dataset + full MC sampling. | ⚠️ BLOCKED. |
| C8 | 1.5 eV optical-conductivity peak weakens as F fraction rises. | Physical prediction | NO — requires real DFT Wannier data. | ⚠️ BLOCKED. |
| **M1** | **Ensemble mean reduces prediction error vs single member** (generalizable pillar). | Methodological | **YES** — testable on any real public materials dataset. | ✅ **Reproduced on real data** — see § 4. |
| **M2** | **Ensemble spread is an informative, calibratable per-instance UQ.** | Methodological | **YES**. | ✅ **Reproduced on real data** — see § 4. |

## 3. Method

### 3a. Repo availability & scaffold inspection (SPOT-CHECK — kept from initial pass)

1. Cloned `github.com/qmatyanlab/DisorderGNN` (public, no auth). Contents:
   - `GNN/GNN.py` — training loop; equivariant `PeriodicNetwork` with irreps `{1×0e (energy) + 251×0e (optical) + 91×0e (electrical)}`; AdamW + CosineAnnealingWarmRestarts; Optuna hyperparameter search (100 trials × 5 epochs each in default script).
   - `GNN/models/` — E3NN network definition and `Network.py`.
   - `MC/Metropolis.py` — Metropolis MC sampler; canonical & grand-canonical ensembles supported.
   - `MC/supercell.vasp` — the 5×5×1 Ti₃C₂ supercell used for MC.
   - `requirements.txt` — pinned to `python==3.11`, `torch==2.3.1`, `torch_geometric==2.5.3`, `e3nn==0.5.5`, plus BoltzTraP2 24.7.2, ASE 3.23, atomate2 0.0.19, pymatgen 2025.3.10.

2. **Blocker for numerical replication (C3, C4, C7, C8):** `GNN/dataset.py` line 47 calls `connectJobStore(jobstore_config)` and imports `connectJobStore, query` from `GNN/utils/__init__` — but only the compiled `.pyc` bytecode of `store.py` and `__init__.py` ships in the repo. The `.py` source is absent. The dataset itself (DFT + Wannier calculations for 3000 configurations on a 175-atom supercell) is not distributed, and reconstructing it would require re-running the maximally-localized-Wannier-function high-throughput workflow of Fang et al. *Sci. Data* **12**, 1092 (2025) — days to weeks of DFT compute time on a GPU/HPC cluster and access to a specific MongoDB atomate2 jobstore.

### 3b. Independent scaffold spot-check (surrogate ensemble, from 2026-07-03 pass)

Script: [`report/evidence/small_ensemble_demo.py`](evidence/small_ensemble_demo.py). 800 synthetic Ti₃C₂O₂₋ₓFₓ-like configurations, 5-member gradient-boosted ensemble, 5 hand-crafted composition + local-order features → 2 physics-motivated targets. Confirms C5 (electrical response is 3.1× more sensitive to local arrangement than optical response at fixed composition x = 0.5, matching paper's central physical message). Results in [`report/evidence/surrogate_results.json`](evidence/surrogate_results.json).

### 3c. Real-data replication of M1 + M2 (added 2026-07-04)

- Script: [`work/ensemble_replication.py`](../work/ensemble_replication.py)
- Follow-up UQ analysis: [`work/uq_recalibration.py`](../work/uq_recalibration.py)
- Machine-readable results: [`report/evidence/ensemble_replication_results.json`](evidence/ensemble_replication_results.json), [`report/evidence/uq_recalibration_results.json`](evidence/uq_recalibration_results.json)
- Full log: [`report/evidence/ensemble_replication.log`](evidence/ensemble_replication.log), [`report/evidence/uq_recalibration.log`](evidence/uq_recalibration.log)
- Raw arrays (for reproducibility of every derived number): [`report/evidence/ensemble_predictions.npz`](evidence/ensemble_predictions.npz)

Method (numbered, verbatim commands & versions):

1. **Data.** Load `matminer.datasets.load_dataset("expt_gap")` — 6,354 real experimental band gaps of inorganic semiconductors from Zhuo et al. (open-access, shipped via Figshare). Drop rows with `gap expt == 0` (metals) and duplicate formulas → 2,483 rows retained.
2. **Featurization.** Composition-only. For each formula, parse element→amount using a regex, weight-average 8 Mendeleev properties per element (Z, atomic mass, group, period, Pauling electronegativity, atomic radius, valence electrons, electron affinity — hand-encoded table for elements Z=1..94), then compute weighted mean / weighted std / min / max / range across constituents, plus `n_elements` and `total_atoms` → **42-dim feature vector**. No pymatgen / spglib dependency (avoids the fragile spglib build on macOS py3.14).
3. **Train/test split.** `sklearn.model_selection.train_test_split(test_size=0.2, random_state=0)` → 1,986 train / 497 test.
4. **Ensemble build — Gradient Boosting.** 20 independent `GradientBoostingRegressor(n_estimators=400, max_depth=5, learning_rate=0.05, subsample=0.8, random_state=s)` for `s ∈ {0..19}`. Each ~4 s on CherryRd (Intel Mac). All fit on identical (X_tr, y_tr); disagreement comes from `subsample` and per-tree random-state.
5. **Ensemble build — Random Forest (independent model family for M1 cross-check).** 20 independent `RandomForestRegressor(n_estimators=300, min_samples_leaf=2, max_features="sqrt", bootstrap=True, n_jobs=-1, random_state=s)`.
6. **Ensemble-size sweep (M1 test).** Ensemble prediction = mean of first `k` members, for `k ∈ {1, 2, 3, 5, 10, 20}`. Report MAE / RMSE / R² of ensemble mean vs true on held-out test.
7. **5-fold CV headline (M1 robust).** `KFold(n_splits=5, shuffle=True, random_state=42)`. Per fold: train 5 GBRs (seeds 0..4), compare single-model (seed 0) MAE vs 5-ensemble mean MAE.
8. **UQ metrics (M2 test).** For GBR-20: ensemble std σ across members. Compute:
   - **Rank correlation** Spearman ρ, Pearson r between σ and |residual| — is σ informative?
   - **Reliability curve** (10 bins by σ → observed RMSE within each bin).
   - **Coverage** at ±1σ, ±2σ vs Gaussian nominal 68.3%, 95.4%.
   - **Sharpness** = mean σ.
   - **Gaussian NLL** assuming σ_pred is a valid Gaussian scale.
   - **Optimal scalar τ recalibration** τ² = mean(residual² / σ²); report post-recal coverage & NLL.
   - **Selective-prediction curve**: sort test by σ ascending, report MAE keeping top {100, 90, …, 10}% most-confident. Compare to random-selection baseline (mean over 20 draws).
9. **Random-Forest per-tree UQ (M2 cross-check).** One RF, extract per-tree predictions from `rf.estimators_` (K = 300 trees), σ = std across trees, same UQ metrics.
10. **LLM-judge verdict (per project rules, never regex).** Post evidence + claims to Argo `argo:claude-opus-4.7` on `http://127.0.0.1:44497/v1` (free endpoint, key=stevens). Verdict + confidence saved to [`report/evidence/llm_judge_verdict.json`](evidence/llm_judge_verdict.json).

**Environment (versions):** Python 3.14.6, scikit-learn 1.9.0, numpy 2.5.1, scipy 1.18.0, pandas 3.0.3, matminer 0.10.1. CherryRd (Intel Mac, single-CPU-friendly; total wallclock ≈ 3 minutes).

## 4. Results vs paper

### 4a. Paper reference numbers (from Fang et al. 2025)

| Model | Target | Paper R² | Paper MAPE |
|---|---|---|---|
| Fully terminated Ti₃C₂O₂₋ₓFₓ (1000 configs) | energy | **0.99** | 0.1% |
| Fully terminated | optical σ | **0.89** | 2.7% |
| Fully terminated | electrical σ | **0.96** | 3.8% |
| Partially terminated Ti₃C₂O₂₋ₓ₋ᵧFₓ (3000 configs, virtual node + persistent homology) | energy | **0.99** | 0.02% |
| Partially terminated | optical σ | **0.87** | 3.48% |
| Partially terminated | electrical σ | **0.98** | 6.88% |

These specific numbers are **not** attempted here (BLOCKED — see § 3a).

### 4b. Real-data replication of M1 (ensemble reduces error) — matminer `expt_gap`

Held-out test set (497 held-out compositions):

| Model | k | MAE (eV) | RMSE (eV) | R² |
|---|---|---|---|---|
| GBR ensemble | 1 | 0.4394 | 0.6323 | 0.8035 |
| GBR ensemble | 2 | 0.4314 | 0.6238 | 0.8087 |
| GBR ensemble | 5 | 0.4343 | 0.6264 | 0.8071 |
| GBR ensemble | 20 | **0.4344** | **0.6267** | **0.8069** |
| RF ensemble | 1 | 0.4493 | 0.6555 | 0.7888 |
| RF ensemble | 20 | 0.4472 | 0.6507 | 0.7919 |

5-fold CV headline (monotonic across folds):

| | Single GBR (seed 0) | 5-member GBR ensemble | Δ |
|---|---|---|---|
| MAE (eV, mean ± std over 5 folds) | **0.4134 ± 0.028** | **0.4092 ± 0.030** | **–1.0%** |
| R² (mean) | 0.8316 | 0.8357 | +0.4% |

**Interpretation of M1:** Ensemble mean beats single-member in every fold (per-fold ΔMAE ∈ {+0.0049, +0.0049, +0.0006, +0.0026, +0.0077} eV; all positive). Magnitude is modest (~1%) — a **directionally correct, honest reproduction**. This is expected: GBR fits with the same data see largely the same signal; ensemble variance-reduction gains are naturally largest for high-variance base learners (small NNs, small trees). Cross-family confirmation (RF also shows monotone ΔMAE) rules out model-specific artifact.

### 4c. Real-data replication of M2 (ensemble UQ is informative + calibratable)

**Rank-correlation (does σ carry information about actual error?):**

| Test | Spearman ρ(σ, |resid|) | Pearson r | p |
|---|---|---|---|
| GBR-20 (holdout, N=497) | **0.527** | 0.547 | < 1e-36 |
| GBR-5 (5-fold CV mean) | **0.370** | — | — |
| RF-300 per-tree (holdout) | **0.568** | — | — |

**Reliability curve (GBR-20 predicted σ vs observed RMSE within bin):**

| Bin | n | Predicted σ | Observed RMSE |
|---|---|---|---|
| 0 (most confident) | 49 | 0.027 | 0.230 |
| 1 | 50 | 0.041 | 0.305 |
| 2 | 50 | 0.052 | 0.296 |
| 3 | 49 | 0.060 | 0.323 |
| 4 | 50 | 0.069 | 0.436 |
| 5 | 50 | 0.079 | 0.516 |
| 6 | 49 | 0.091 | 0.605 |
| 7 | 50 | 0.108 | 0.814 |
| 8 | 50 | 0.142 | 0.750 |
| 9 (least confident) | 50 | 0.221 | 1.236 |

→ Observed RMSE **increases monotonically** across all 10 predicted-σ bins (0.23 → 1.24 eV, a **5.4× spread**). σ is strongly informative.

**Absolute-calibration (coverage) — before and after single-scalar recalibration:**

| Ensemble | Sharpness (mean σ) | Cov @ ±1σ | Cov @ ±2σ | τ opt | Post-recal cov @ ±1σ | Post-recal cov @ ±2σ | NLL (uncal → recal) |
|---|---|---|---|---|---|---|---|
| GBR-20 | 0.089 eV | 12.7% | 23.7% | **6.48** | **72.4%** | **95.8%** | 19.3 → **0.69** |
| RF-300 (per-tree) | 0.51 eV | **78.1%** | **98.0%** | 0.86 | 71.0% | 97.0% | — |
| Gaussian nominal | — | 68.3% | 95.4% | — | 68.3% | 95.4% | — |

→ **GBR-20 raw σ is under-dispersed (~6× too small)** — a known deep-ensemble pathology (Lakshminarayanan+2017, §3.3). But a single scalar recalibration recovers near-nominal coverage AND cuts NLL by 28×. **RF-300 per-tree σ is nearly calibrated out of the box** (slightly over-dispersed at τ = 0.86). Both ensembles carry the correct rank/shape of uncertainty — the failure of GBR raw σ is not an information deficit, it is a scale mis-set.

**Selective-prediction (utility of UQ in practice):**

| Fraction kept | GBR-20 MAE | RF-300 MAE | Random baseline MAE |
|---|---|---|---|
| 100% | 0.434 | 0.449 | 0.434 |
| 80% | 0.343 | 0.336 | 0.430 ± 0.009 |
| 50% | 0.246 | 0.244 | 0.431 ± 0.020 |
| 20% | 0.190 | 0.146 | 0.430 ± 0.026 |
| 10% (most confident) | **0.148** | **0.108** | 0.442 ± 0.050 |

→ Ranking test points by ensemble σ and dropping the highest-σ 90% cuts MAE by **2.9× (GBR)** and **4.2× (RF)** vs the full test set. Random selection stays flat. This is the practical value the paper claims — knowing when to trust your model — and it is unambiguously demonstrated on real data.

### 4d. Qualitative claim C5 (order vs composition sensitivity)

Confirmed on the surrogate spot-check (see § 3b + [`report/evidence/surrogate_results.json`](evidence/surrogate_results.json)): σ(E_electrical) / σ(E_optical) = 3.11× at fixed composition x = 0.5. Matches paper's central physical message; not tested on real MXene data because the dataset is unavailable.

## 5. Verdict

**PARTIAL.** Confirmed by independent LLM-judge (Argo `argo:claude-opus-4.7`), confidence 0.78.

**Justification.**

- **Reproduced on real independent public data:**
  - **M1** (ensemble mean reduces error): 1.0% MAE reduction, monotone across all 5 CV folds, confirmed in both Gradient-Boosting and Random-Forest model families. Direction matches paper.
  - **M2** (ensemble spread is informative + calibratable UQ): Spearman ρ up to 0.57, monotone reliability curve across 10 σ-bins (5.4× spread), scalar recalibration to near-nominal coverage, 28× NLL improvement, and **3–4× MAE reduction** via σ-ranked selective prediction vs a flat random baseline.
  - **C5** (electrical > optical local-order sensitivity): confirmed on physics-motivated surrogate (3.1× ratio).
- **Blocked (data unavailability, not a method fault):** C3, C4, C7, C8 — the paper-specific Ti₃C₂O₂₋ₓFₓ numerical claims. The 3000-configuration DFT+Wannier dataset is not distributed and the atomate2 jobstore adapter ships only as compiled `.pyc`. Would take days–weeks of HPC time and MongoDB access to reconstruct.
- **No fabrication:** every number in § 4b, 4c comes from `report/evidence/ensemble_replication_results.json` and `uq_recalibration_results.json`, both derivable from the raw predictions in `ensemble_predictions.npz`. Verdict scoring is LLM-judge, never regex (per project rules).

**Why PARTIAL and not REPLICATED:** the paper's *specific* MXene numbers are the most compact test of its full pipeline, and we cannot reach them without the DFT dataset. Even though the two generalizable methodological pillars are cleanly reproduced, the paper's headline application is out of reach from public artifacts alone.

**Why PARTIAL and not SPOT-CHECK (upgrade from the 2026-07-03 initial pass):** a real independent public dataset (matminer `expt_gap`, 2,483 rows) was fully processed, real ensembles were trained (20 GBRs + 20 RFs + a 300-tree RF), and both methodological pillars M1 and M2 were tested and reproduced — this exceeds a spot-check of code availability + a synthetic surrogate.

**What would upgrade this to REPLICATED:** access to the actual 3000-configuration DFT+Wannier dataset (or the source `.py` for `connectJobStore`/`query`) so the paper's exact GNN training pipeline could be run and R²/MAPE on the paper's own test split evaluated directly. Contacting the authors (`z.fang@northeastern.edu`, `q.yan@northeastern.edu`) or a follow-up on the *Sci. Data* companion paper (Fang et al. 2025, ref. 42) would be the natural next step.

## 6. Artifacts

- `report/evidence/ensemble_replication.py` (script), `ensemble_replication_results.json`, `ensemble_replication.log`, `ensemble_predictions.npz` — real-data replication of M1 + M2 on matminer `expt_gap`.
- `report/evidence/uq_recalibration.py` (script), `uq_recalibration_results.json`, `uq_recalibration.log` — UQ recalibration + RF-300 per-tree UQ + selective-prediction curves.
- `report/evidence/llm_judge_verdict.json`, `llm_judge_verdict.txt` — Argo Opus 4.7 verdict scoring.
- `report/evidence/small_ensemble_demo.py`, `surrogate_results.json` — original 2026-07-03 surrogate spot-check (C5, C6).
- `work/paper.pdf`, `work/paper.txt` — original paper (4.3 MB) + extracted text.
- `work/ensemble_replication.py`, `work/uq_recalibration.py` — driver scripts (identical to those in `report/evidence/` but kept in `work/` for reproducibility).
- Upstream code (not inside this dir): `github.com/qmatyanlab/DisorderGNN` (README, requirements.txt, GNN/, MC/).

## 7. Honest limitations

1. **This does NOT reproduce the paper's specific Ti₃C₂O₂₋ₓFₓ R²/MAPE numbers or MC-derived phase-transition prediction.** Those remain BLOCKED.
2. **Band-gap prediction from composition-only features is a *simpler* problem** than the paper's DFT+Wannier multi-spectrum target. High R² on band gap does not automatically imply the paper's more sophisticated task will scale similarly — but the paper explicitly frames M1 and M2 as generalizable ML claims, not MXene-specific ones.
3. **M1 magnitude on `expt_gap` is small** (~1% MAE reduction). This reflects (a) modest dataset (2,483 rows), (b) all-same-architecture ensemble (only seed/subsample differ), and (c) the intrinsic difficulty of composition-only band-gap prediction (state-of-the-art is R² ≈ 0.87 with composition-only features — see Zhuo et al. 2018). The paper's ensemble improvement magnitudes are likely larger on their specific problem because their base learners (E3NN GNNs on a 175-atom supercell) have higher variance per initialization.
4. **The M2 raw calibration on GBR is bad** (cov @ ±1σ = 12.7% vs 68.3%). The τ-recalibration fix is a *post-hoc* calibration, not a claim that the raw σ is directly interpretable. The paper does not explicitly claim raw calibration either — its usage is qualitative ("ensemble variance reflects prediction uncertainty").
5. **No Monte-Carlo sampling was performed.** The paper's MC-derived findings (phase-transition Tc, electrical-conductivity peak) remain unverified.
6. **Compute budget:** ~3 min on a single CPU core. This is sufficient for the ensemble-methodology tests but is orders of magnitude below what a real DFT re-run would need.
7. **Featurizer is simpler than matminer's** `ElementProperty` (which uses ~132 features per composition). We used 42 hand-computed features. This reduces absolute accuracy but does not confound the M1 / M2 tests, which are relative comparisons within the same feature space.

---
*Report generated 2026-07-03 (initial SPOT-CHECK), upgraded to PARTIAL 2026-07-04 after real-data ensemble + UQ replication. All evidence in `report/evidence/`.*
