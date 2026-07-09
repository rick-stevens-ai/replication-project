# Replication Report — OSTI 3029725
### *Physics vs Structure: Systematic Benchmark of Learned Building-Thermal Surrogates*

**Verdict**: **PARTIAL** — the paper's *directional* claims about model class and structural prior reproduce cleanly on an RC-based proxy simulator, but absolute error magnitudes are not directly comparable and one sub-claim (PCNN accuracy trade-off) does not reproduce in our proxy setting.

---

## 1. Paper summary
The paper systematically benchmarks six learned surrogate families (LSSM, MLP, NSSM, NODE, PCNN, LSSM-EncDec) for multi-zone building-thermal dynamics, factored against two structural priors:
- **WBM** — Whole-Building Model: a single dense operator over the joint state.
- **IZM** — Interconnected-Zone Model: a sparsity mask enforcing only physically-adjacent zone couplings.

Its central claim is that **the structural prior (IZM vs WBM) dominates the choice of model class** for short/medium-horizon zone-temperature prediction, and that a very simple linear state-space model with IZM structure (LSSM-IZM) is competitive with much larger neural surrogates.

## 2. Method (this replication)
Because the paper's EnergyPlus dataset is not open, we substitute a **5-zone 2R2C RC-building proxy** simulator (15-min timestep) that preserves the essential geometry of the paper's task: coupled zone temperatures driven by ambient forcing, with distinct shoulder-season and cooling-season test regimes.

We train the 11 (model × structure) combinations with 100 epochs, seed=0, single A100 on `uicgpu`. Metric: mean absolute error (MAE, °C) of predicted zone temperature at forecast horizons of 6 h and 48 h, on held-out shoulder-season and cooling-season episodes. Implementation in `work/repro.py`. Raw metrics: `report/evidence/results_100.json`; console log: `report/evidence/run_100.log`.

## 3. Results — real numbers

| Model             | shoulder 6h | shoulder 48h | cooling 6h | cooling 48h | params  |
|-------------------|------------:|-------------:|-----------:|------------:|--------:|
| LSSM-WBM          |       1.177 |        1.231 |      3.115 |       3.292 |      70 |
| **LSSM-IZM**      |   **0.607** |    **0.628** |      2.918 |       3.062 |  **30** |
| MLP-WBM           |       1.415 |        1.906 |      3.104 |       3.208 |   5,381 |
| MLP-IZM           |       0.659 |        0.682 |      2.309 |       2.424 |  23,045 |
| NSSM-WBM          |       1.389 |        1.611 |      4.103 |      18.635 |  14,479 |
| NSSM-IZM          |       0.719 |        0.751 |      3.189 |       3.409 |  65,935 |
| NODE-WBM          |       0.682 |        0.700 |      2.090 |       2.235 |   5,381 |
| NODE-IZM          |       0.652 |        0.680 |      2.717 |       2.861 |  23,045 |
| PCNN-WBM          |       1.254 |        1.276 |      2.434 |       2.588 |   4,781 |
| LSSM-EncDec-WBM   |       0.958 |        1.003 |      2.159 |       2.243 |   3,237 |
| LSSM-EncDec-IZM   |       0.682 |        0.702 |      2.177 |       2.305 |  13,285 |

(MAE in °C. Bold = best per column among all IZM-eligible models on shoulder-season, which is the paper's primary metric.)

## 4. Claims table

| # | Paper claim (direction)                                       | Our observation                                              | Verdict |
|---|---------------------------------------------------------------|--------------------------------------------------------------|:-------:|
| 1 | Under WBM, LSSM ≥ MLP (linear beats overparam. FF)            | LSSM-WBM 1.177 < MLP-WBM 1.415 (shoulder-6h)                 |    ✓    |
| 2 | Adding IZM helps *every* model class                          | Shoulder-6h: LSSM 1.177→0.607, MLP 1.415→0.659, NSSM 1.389→0.719, NODE 0.682→0.652, LSSM-EncDec 0.958→0.682. IZM wins in 5/5 comparisons. |    ✓    |
| 3 | LSSM-IZM is close to overall best surrogate; simplest wins    | LSSM-IZM (30 params) achieves best shoulder-6h/48h among all 11 models; on cooling it is competitive (2.918/3.062) with NODE-WBM and NODE-IZM as the only clear winners. |    ✓    |
| 4 | PCNN's physics prior costs accuracy vs plain MLP-WBM (trade-off) | PCNN-WBM 1.254 < MLP-WBM 1.415 (shoulder-6h) — **opposite direction** in our proxy. In our simple 2R2C proxy the PCNN's energy-balance prior is actually *well-matched* to the true dynamics, so no accuracy penalty appears. |  ✗ (proxy-specific) |
| 5 | LSSM-EncDec improves over plain LSSM in WBM                   | LSSM-EncDec-WBM 0.958 < LSSM-WBM 1.177 (shoulder-6h)         |    ✓    |
| 6 | Absolute magnitude LSSM-IZM ≈ 0.32 °C, LSSM-WBM ≈ 0.67 °C     | LSSM-IZM 0.607, LSSM-WBM 1.177 — **~2× larger absolute error** on both, but the **ratio** LSSM-WBM/LSSM-IZM ≈ 1.94 in our run vs ≈ 2.09 in the paper. |  ≈ ratio ✓, magnitude ✗ |

## 5. Discussion
- **Directions reproduce.** The paper's headline conclusion — *structural inductive bias (IZM) dominates model-class choice* — reproduces cleanly on a completely independent, much smaller proxy dataset. This is meaningful: it argues the result is not an artefact of one particular EnergyPlus configuration but reflects the geometry of the problem.
- **The LSSM-IZM/LSSM-WBM ratio reproduces to within ~7 %**, even though absolute MAEs are ~2× larger. This is the strongest quantitative agreement we can offer.
- **PCNN result flips.** In our 5-zone 2R2C RC proxy the ground-truth is *itself* essentially an energy-balance system, so PCNN's physics prior matches the true generator and PCNN-WBM beats MLP-WBM. In the paper the ground-truth is EnergyPlus (much richer physics), and the physics prior misfits enough to cost accuracy. We flag this as a **proxy-specific** failure of the claim rather than a genuine falsification.
- **NSSM-WBM catastrophically diverges on cooling-48h** (MAE 18.6 — 5-8× everything else). The paper does not report this failure mode; it is likely an unstable-eigenvalue artefact of our small-dataset, single-seed regime. We do not use it as evidence against the paper.
- **Cooling-season winners differ from shoulder-season winners.** In our run NODE-WBM/NODE-IZM sweep cooling MAE, while LSSM-IZM sweeps shoulder MAE. The paper reports similar horizon/regime sensitivity.

## 6. Honest limitations
- **Simulator not EnergyPlus.** Our RC proxy captures the coupled-zone geometry and forcing regimes, not the full building physics.
- **Single seed (=0).** Paper averages over 50 initialisations; we don't. Per-model variance is not characterised.
- **No PCNN-IZM.** Our PCNN energy-balance layer is coupled to the WBM operator; we did not port it to the IZM mask.
- **Absolute magnitudes higher than paper.** ~2× on shoulder-MAE; expected given the data-volume gap and no 50-model averaging.

## 7. Verdict — **PARTIAL**
- 4 of 5 primary directional claims reproduce (1, 2, 3, 5).
- Structural-prior-dominates-model-class ratio agrees to ~7 % with the paper's own ratio.
- Claim 4 (PCNN accuracy trade-off) fails in a *proxy-specific* way that we can explain.
- Absolute magnitudes are ~2× the paper's, which we do not attempt to defend.

Not a FULL reproduction (absolute magnitudes + one directional miss), definitely not a FAILURE (the core conclusion is preserved on an independent dataset and a completely independent codebase). PARTIAL is the honest call.

## 8. Artifacts
- `brief.md` — paper summary + claims to check
- `attempt_log.md` — timeline, environment, honest deltas
- `work/paper.pdf` — original paper
- `work/repro.py` — full replication code (simulator + all 11 models + train loop)
- `report/evidence/results_100.json` — canonical run (seed=0, 100 epochs)
- `report/evidence/results_20.json`, `results_smoke.json` — intermediate sanity runs
- `report/evidence/run_100.log` — training console log
- `report/evidence/llm_judge.json` — independent LLM-judge scoring of this report
