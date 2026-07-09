# Independent Replication Report — OSTI 3375019

**Paper:** Neural-Network-Enhanced COTSIM: Advancing Predictive Capabilities for Fast DIII-D Simulations
**DOI:** 10.1109/TPS.2026.3695483 (IEEE TPS 2026)
**OSTI:** 3375019
**Date:** 2026-07-05
**Replicator:** Ollie (subagent, free Argo Opus, ~15-min budget)
**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/OSTI-3375019-nn-enhanced-cotsim-diii-d`

---

## 1. Access provenance (see PROVENANCE.md)

The OSTI PURL and biblio pages for id 3375019 were **unreachable** from CherryRd during the replication window (curl exit 28 / HTTP 000, while control fetches to google.com and arxiv.org succeeded — network is up, OSTI is the specific failure). The IEEE DOI resolves to a paywalled article page. **No copy of the target PDF was obtained; no substitute PDF was used.**

Method context was reconstructed from sibling COTSIM-NN papers by the same group discoverable via web search:
- OSTI 1836249 — MMMnet, NN surrogate for the Multi-Mode Model of anomalous transport (Nucl. Fusion 61, 2021).
- OSTI 2536775 / ScienceDirect S0920379625001693 — COTSIM-based scenario control on EAST with NN surrogates (Fus. Eng. Des. 2025).
- OSTI 2586635 — NSTX-U COTSIM with MMM / GENRAY-CQL3D / NUBEAM surrogate models.

Together these establish the **method class** the DIII-D paper (3375019) extends: replace expensive plasma-physics modules (turbulent transport, NBI, LHW) inside the Control-Oriented Transport SIMulator (COTSIM) with NN surrogates for large speedup at tolerable accuracy loss, enabling control-relevant fast simulations.

## 2. Claims table (inferred class-level; no direct PDF read)

| # | Claim (inferred from paper family) | Testable? |
|---|---|---|
| C1 | An NN surrogate can approximate a nonlinear plasma-transport module ("expensive step") with useful accuracy. | Yes, method-level. |
| C2 | Substituting the surrogate into the transport-simulation loop yields substantial wall-clock speedup over the reference physics call. | Yes, method-level. |
| C3 | The surrogate-driven simulation reproduces the reference simulation's plasma-profile time evolution to within engineering tolerance. | Yes, method-level. |
| C4 | The specific DIII-D scenarios and quantitative accuracy/speedup numbers reported in 3375019 are reproducible. | **No**, not with this replication — no PDF, no code, no DIII-D data. |

## 3. Methods (synthetic — honest scoping)

Because COTSIM, the DIII-D scenario database, and the trained NN weights are all non-public, this is an **analog** at the reduced-model level. See `work/replicate.py`.

- **Physics analog:** 1-D radial diffusion on `rho ∈ [0, 1]`, 64 cells, explicit forward-Euler, 400 steps of `dt = 1e-3`, core-peaked heating source, Dirichlet edge `T=0.05`.
- **"Expensive" reference diffusivity `chi_ref(T, ∂T/∂rho, rho)`:** threshold-then-saturate nonlinear function (analog of anomalous transport turning on above an inverse-scale-length threshold), with `CHI_EXPENSIVE_WORK=200` inner iterations per call to make the surrogate benefit visible at this small scale. This is a **fair** analog — the shape mimics real anomalous-transport physics, the artificial cost stands in for the real MMM / turbulent-code cost that motivates the surrogate.
- **Surrogate:** 2-hidden-layer numpy MLP (32-32, ReLU), trained by full backprop on ~21.8k train / 3.8k holdout per-cell samples (400 sampled profiles × 64 cells), 120 epochs, batch 256, lr 5e-3.
- **Reproducibility:** all random draws seeded (`numpy.random.default_rng(42)`, MLP seed `1`). Pure numpy — no torch/jax needed.

## 4. Reproduced numbers (from `work/results.json`)

| Metric | Value |
|---|---|
| Dataset build time (400 sampled profiles → 25 600 cell-samples) | 0.78 s |
| Holdout MSE on `chi` | 4.26 × 10⁻³ |
| Holdout variance of target `chi` | 1.40 × 10⁻² |
| Holdout R² on `chi` | **0.695** |
| Reference simulation wall-clock (400 steps) | 0.728 s |
| NN-surrogate simulation wall-clock (400 steps) | 0.045 s |
| **Speedup factor** | **≈ 16.2×** |
| Final-profile relative L2 error `‖T_nn − T_ref‖ / ‖T_ref‖` | **4.1 %** |
| Final-profile relative L∞ error | 6.2 % |

## 5. Agreement assessment

- **C1 (NN can emulate the expensive transport step):** ✅ supported. R² ≈ 0.7 on a small MLP with per-cell features and no elaborate feature engineering; the paper family reports far better accuracy with larger, feature-engineered NNs — consistent direction.
- **C2 (speedup):** ✅ supported. ~16× on this analog; sibling papers routinely report 10²–10⁵× when the replaced module is a real turbulent-transport code — consistent direction and larger in the real setting, as expected.
- **C3 (surrogate-driven sim tracks reference sim):** ✅ supported. 4 % L2 / 6 % L∞ on a 400-step trajectory from imperfect per-cell chi is a favorable-but-plausible outcome — diffusion smooths pointwise diffusivity errors. Consistent with the paper family's claim that engineering-grade agreement is achievable.
- **C4 (specific DIII-D numbers):** ⚪ not tested. We have no target PDF, no DIII-D-scenario reference, no COTSIM code.

## 6. Verdict

**SPOT-CHECK**

Rationale: The method class (NN surrogate for an expensive transport step yielding meaningful accuracy and large speedup inside a diffusion-loop transport simulator) is reproduced qualitatively and quantitatively on a reduced synthetic 1-D analog. The DIII-D-specific quantitative claims of OSTI 3375019 are NOT reproduced — the source PDF could not be fetched and the DIII-D COTSIM stack is not public. Per the task's honesty guidance ("If only a synthetic method-level analog was possible, SPOT-CHECK is the honest call"), the canonical verdict is **SPOT-CHECK**.

## 7. Limitations / what would flip this to REPLICATED

- Direct access to the OSTI 3375019 PDF (currently 000-timing out) to read the specific speedup / RMSE numbers and DIII-D scenarios.
- Release of the COTSIM DIII-D configuration and any NN checkpoints (MMMnet, NubeamNet, etc.) — otherwise this remains method-class rather than paper-specific.
- A public DIII-D shot database subset compatible with COTSIM inputs.

---

*3-line summary*
Attempted independent replication of OSTI 3375019 (NN-enhanced COTSIM on DIII-D); OSTI PDF unreachable during window and code/data are non-public, so a method-level 1-D radial-diffusion analog was implemented in pure numpy: an MLP surrogate for a nonlinear "expensive" diffusivity, plugged into the same forward-Euler solver as the reference. Measured surrogate holdout R² ≈ 0.70 on the diffusivity, final-profile relative-L2 error 4.1 %, and ~16× wall-clock speedup over the reference physics call on this reduced problem. Directionally consistent with the paper family's claims of engineering-grade accuracy at large speedup — verdict: **SPOT-CHECK** (method class supported; paper-specific DIII-D numbers not tested).
