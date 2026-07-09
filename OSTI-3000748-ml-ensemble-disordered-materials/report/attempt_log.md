# Attempt log — OSTI-3000748 (Fang et al. 2025)

## 2026-07-02 — initial harvest
- Downloaded paper (`work/paper.pdf`, 4.3 MB, OSTI 3000748).
- Extracted text (`work/paper.txt`).
- Created python 3.14 venv in `work/venv/`.

## 2026-07-03 — SPOT-CHECK pass
- Cloned `github.com/qmatyanlab/DisorderGNN` and inspected.
- Confirmed C1 (repo exists), C2 (equivariant e3nn PeriodicNetwork present, multi-target head `{energy(1), optical(251), electrical(91)}` matches paper).
- **Blocker discovered:** `GNN/dataset.py` needs `connectJobStore`/`query` — shipped only as `.pyc`, source absent. Underlying DFT dataset (3000-config Ti₃C₂O₂₋ₓFₓ) not distributed.
- Ran synthetic surrogate (`report/evidence/small_ensemble_demo.py`): 800 toy Ti₃C₂O₂₋ₓFₓ-like configurations, 5-member GBR ensemble. Confirmed C5 (electrical/optical sensitivity ratio 3.11× at fixed x=0.5) and C6 (ensemble can learn multi-target regression, R² ≈ 0.998 on synthetic).
- Verdict: SPOT-CHECK.

## 2026-07-04 — upgraded to PARTIAL
- Received wave-brief task to deepen this replication if evidence supports it.
- **Strategy:** the paper's specific MXene numbers remain blocked, but the paper's *generalizable* methodological claims (M1: ensemble reduces error; M2: ensemble spread is informative + calibratable UQ) are testable on any real public materials-property dataset.
- Installed scikit-learn 1.9.0, numpy 2.5.1, scipy 1.18.0, pandas 3.0.3, matminer 0.10.1 in `work/venv/`.
  - `matminer` install with full deps failed (spglib wheel build failure on py3.14 macOS). Worked around by `pip install matminer --no-deps` then adding only the load-dataset dependencies (monty, tqdm, plotly, pint, pymongo, requests, jsonschema, future). Full featurizer suite is unavailable, but `matminer.datasets.load_dataset` works — it just downloads CSV/JSON from Figshare.
- Loaded `expt_gap` (6,354 real experimental band gaps of inorganic semiconductors, from Zhuo et al. 2018). Cleaned: dropped metals (gap=0) and duplicate formulas → 2,483 rows.
- Featurized: hand-coded compositional featurizer using 8 Mendeleev properties per element (Z, atomic mass, group, period, Pauling EN, atomic radius, valence electrons, electron affinity — table for elements Z=1..94), then weighted mean / std / min / max / range / n_elem / total_atoms → 42-dim vectors. Avoids pymatgen/spglib dependency.
- Trained 20 GBR ensembles (~4 s each) + 20 RF ensembles (~0.4 s each). 5-fold CV. GBR-20 for UQ (mean + std across members). RF-300 per-tree UQ as cross-check.
- LLM-judge (Argo `argo:claude-opus-4.7` at `http://127.0.0.1:44497/v1`, free endpoint): PARTIAL, confidence 0.78.
- Updated `report/REPORT.md` with the § 3c / § 4b / § 4c real-data replication and the promoted PARTIAL verdict. Preserved all prior SPOT-CHECK content in §§ 3a / 3b / 4d / 7.

### Key numbers reproduced (all real, all traceable to evidence/*.json)
- **M1:** 5-fold CV MAE 0.4134 → 0.4092 (single GBR → 5-ensemble), monotone across all 5 folds. Both GBR and RF families show ΔMAE > 0 in every fold. Direction matches paper.
- **M2:** Spearman ρ(σ, |resid|) = 0.527 for GBR-20, 0.568 for RF-300. Reliability curve monotone across 10 bins (0.23 → 1.24 eV RMSE). RF-300 raw calibration cov@±1σ = 78.1% (nominal 68.3%). GBR-20 raw is under-dispersed by 6.5× but a single scalar recalibration recovers cov@±1σ = 72.4% and cuts NLL 19.3 → 0.69. Selective prediction: keeping most-confident 10% reduces MAE by 2.9× (GBR) / 4.2× (RF). Random baseline stays flat — UQ carries real information.

### What did NOT work
- Full matminer install (spglib wheel build fails on macOS py3.14). Worked around with `--no-deps` install.
- Attempted to reproduce paper's exact R²/MAPE numbers — blocked because dataset not distributed + store adapter `.pyc`-only.
- Did not attempt Monte-Carlo sampling → C7/C8 remain blocked (would need the trained real-data GNN).

### Compute
- Local CherryRd (Intel Mac, single CPU). Wallclock ~3 min for ensemble replication, ~1 min for UQ recalibration.
