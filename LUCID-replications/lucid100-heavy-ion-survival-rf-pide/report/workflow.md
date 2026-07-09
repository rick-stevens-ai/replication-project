# Workflow — lucid100-heavy-ion-survival-rf-pide

Reproducible pipeline for replicating Debreceni et al. 2024 (Toxics 12(8):545), NB1RGB heavy-ion cell survival with LQM / LocReg / RF.

## Environment
- Host: CherryRd (or any Python 3.11+ box with sklearn, scipy, pandas, numpy, matplotlib).
- Dependencies: `pip install numpy pandas scipy scikit-learn matplotlib`.
- No GPU required. Runtime ~1.7 min end-to-end (RF 1000 trees × 100 MC-CV iters).

## Inputs
1. **Paper full text** (already staged): `source/fulltext.xml`, `source/fulltext.txt` (Europe PMC JATS harvest of PMC11359366; open-access CC-BY).
2. **Paper's data (BLOCKED):** GSI PIDE cell-survival ensemble, NB1RGB subset. Behind email-registration form at `https://www.gsi.de/.../pide_registration` (TYPO3 powermail; download link is emailed, never inline-served). Wayback CDX, Zenodo, figshare, GitHub — all negative for the raw file.
3. **Substitute data (used here):** `data/nb1rgb_reconstructed.csv` — 311 pts / 51 experiments, ion mix 12C:24, 20Ne:15, 28Si:7, 56Fe:5. Built from Furusawa (2000) α(LET)/β(LET) that feed PIDE for NB1RGB, plus 15% log-normal clonogenic scatter. Preserves the physics; is NOT the exact PIDE matrix.

## Pipeline (three scripts, all in `code/`)

### Step 1 — Build dataset
```bash
python code/build_dataset.py
# Output: data/nb1rgb_reconstructed.csv
```
Encodes: α(LET) rising to an overkill peak ~150 keV/µm then falling, β(LET) declining with LET; regenerates dose/SF via S = exp(−(αD + βD²)) with realistic per-plate scatter. Ion mix + N match the paper.

### Step 2 — Run three models with Monte-Carlo CV
```bash
python code/run_pipeline.py
# Output: results/pipeline_results.json
```
- **LQM(dose):** `scipy.optimize.curve_fit` on S = exp(−(αD + βD²)), α,β ≥ 0.
- **LocReg(dose):** tricube-kernel locally weighted linear regression on dose.
- **RF(dose, LET):** `RandomForestRegressor(n_estimators=1000)`.
- Validation: 100 Monte-Carlo iterations, 70/30 random point split, R² and RMSE (mean ± std).

### Step 3 — Comparison figure
```bash
python code/make_figure.py
# Output: figures/model_comparison.png
```
Grouped bar chart: paper vs reproduced, R² and RMSE side-by-side, with std error bars.

### Step 4 — Independent LLM judge (already run)
Free Argo endpoint `argo:gpt-5.2` at temperature 0 scored coverage=8, agreement=6, verdict=PARTIAL. Result serialized in `results/judge_verdict.json`.

## Repro checklist (from a clean clone)
1. `pip install -r requirements.txt` (or manual install of the deps above).
2. `python code/build_dataset.py` — recreates `data/nb1rgb_reconstructed.csv` (fixed seed inside the script for reproducibility).
3. `python code/run_pipeline.py` — regenerates `results/pipeline_results.json`.
4. `python code/make_figure.py` — regenerates `figures/model_comparison.png`.
5. Compare against §3 table in `report/REPORT.md` — should match within stochastic noise.

## What is NOT reproducible from these steps
- **Exact paper numbers** (RF R²=0.9685, RMSE=0.0196). Requires the actual GSI PIDE NB1RGB subset, which is email-gated.
- **Leave-experiment-out (LEO) CV** — the paper does not report it and neither does this replication (Open Question Q2). Adding it here would go beyond re-run scope.
- **Mechanistic baselines (MKM, RMF, LQ with α(LET), β(LET))** — Open Question Q3.

## Provenance / lineage
- Paper harvest: Europe PMC JATS XML via `https://europepmc.org/backend/ptpmcrender.fcgi?accid=PMC11359366&blobtype=xml` (no subscription hop needed; open access).
- Original replication run: 2026-07-02 by Ollie (LUCID subagent).
- Backfill artifacts (REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd stub): 2026-07-06 by Ollie backfill subagent, no re-run of sims (per HARD REQUIREMENT).
- Verdict adjudication: independent free Argo LLM judge `argo:gpt-5.2`, temperature 0.

## Free-endpoint compliance
All LLM calls (judge scoring, backfill authoring) use free Argo endpoints (`argo:gpt-5.2` for judge; `argo:claude-opus-4.7` for backfill authoring). No paid endpoints invoked.
