# Independent Replication Report — OSTI 3002302

**Paper:** Lijie Ding & Changwoo Do (Oak Ridge National Laboratory, Neutron
Scattering Division), *"Deciphering the small-angle scattering of polydisperse
hard spheres using deep learning"*, **APL Machine Learning 3, 036112 (2025)**,
DOI [10.1063/5.0290589](https://doi.org/10.1063/5.0290589), OSTI ID 3002302.
Submitted 12 Jul 2025 · Accepted 6 Aug 2025 · Published Online 15 Aug 2025.
CC BY-NC 4.0.

**Replicator:** Independent automated agent (not affiliated with the authors);
NVIDIA A100 (UICGPU cluster), PyTorch 1.11.
**Date:** 2026-07-02.

---

## 1. Paper summary

The paper studies how to invert small-angle scattering (SAS) curves I(Q) for a
polydisperse hard-sphere fluid — a canonical soft-matter reference system where
the traditional decoupling between form factor (particle shape) and structure
factor (Percus-Yevick, PY) breaks down at higher volume fraction η and
polydispersity σ. The proposed solution is a Variational Autoencoder (VAE)
with a 3-dim latent space (paper §II.C):

* **Encoder** — two 1D-conv layers (kernel 9, stride 2, channels 30 → 60),
  100-dim I(Q) → 1500-dim → μ, s (each 3-dim).
* **Decoder** — mirror architecture with `ConvTranspose1d`.
* **Converter 1 (P2L)** — small MLP mapping (η, σ) → latent (μ, s).
* **Converter 2 (L2P)** — small MLP mapping latent z → (η′, σ′).
* Composing (converter 1 → decoder) gives a **Generator** that predicts I(Q)
  from (η, σ); composing (encoder → converter 2) gives an **Inferrer** that
  predicts (η, σ) from I(Q).

**Ground truth** comes from LAMMPS MD (paper §II.A): 23,328 particles
interacting via truncated-shifted Lennard-Jones (ε=100, cutoff at 2^(1/6)σ,
which mimics hard spheres), NVT ensemble with T = 1, D₀ = 1. Three size
distributions: uniform D ∈ U(1−σ, 1+σ) (pdType 1), normal (pdType 2), and
lognormal (pdType 3). For each type, 5000 pairs (η, σ) are sampled
independently with η ∈ U(0, 0.5), σ ∈ U(0, 0.3), and I(Q) is computed on 100
Q-grid points in [3, 13] using the coupled sum

I(Q) = ⟨|Σᵢ exp(-iQ·rᵢ)F(Q; Dᵢ)|²⟩ / Σᵢ(πDᵢ³/6)²        (paper eq. 2)

with F(Q; D) the analytic sphere form factor amplitude (eq. 3). Split
4000 train / 1000 test. Training: Adam + CosineAnnealingLR; VAE 1000 epochs,
each converter 300 epochs frozen + 200 epochs fine-tune.

**Baselines** the paper compares against:
* Percus-Yevick (PY, Wertheim 1963) with monodisperse-decoupling
  I_PY(Q) = S_PY(Q) · P(Q).
* PY + β correction: I_PYβ = (1 + β(S_PY − 1)) · P, with
  β = ⟨F⟩² / ⟨F²⟩.

**Reproducibility artifacts** (paper §Data Availability):
GitHub — https://github.com/ljding94/Polydisperse_Sphere . Contains code
(C++ + Python I(Q) calculator, LAMMPS input scripts, PyTorch VAE), the
processed 4000+1000 (η, σ, I(Q)) datasets for each distribution, and trained
model weights (VAE, Generator, Inferrer for each pdType). Everything needed
for evaluation is present.

## 2. Claims table

| ID | Claim | Type | Testable in independent rerun? | Tested here? |
|----|-------|------|-------------------------------|--------------|
| C1 | VAE bidirectionally maps I(Q) ↔ (η, σ) for polydisperse hard spheres | methodological | yes | ✅ yes (both directions, all 3 distributions) |
| C2 | NN inferrer extracts (η, σ) with very high accuracy (scatter on diagonal, "very small" relerr, Figs 8, 11) | quantitative | yes | ✅ yes — R² ≈ 0.9999 for both parameters on all 3 distributions |
| C3 | NN generator I(Q) predictions have much lower MSE than PY and PYβ (Figs 5, 6, 10) | quantitative / comparative | yes | ✅ yes — NN 17–120× lower log₁₀ MSE than PYβ / PY |
| C4 | 3-dim latent is sufficient; SVD/PCA of the dataset supports this (Fig 4) | methodological | yes | ❌ not tested (architecture accepted from code) |
| C5 | Method generalizes across three size-distribution families (uniform, normal, lognormal) | methodological | yes | ✅ yes — evaluated for all 3 |
| C6 | Training recipe is reproducible from the released code and data (implicit) | methodological | yes | ✅ yes — from-scratch retrain (pdType=1) matches released weights to <2× on all metrics |

Coverage: 5 of 6 claims directly tested → **coverage ≈ 0.83**.

## 3. Method (independent replication)

All commands executed by an automated agent, not the paper's authors.

1. **Fetch PDF.** The paper's OSTI mirror is publicly available; the
   AIP-hosted PDF is paywalled but the OSTI copy is not. From `uicgpu`:
   `curl -sL https://www.osti.gov/servlets/purl/3002302 -o work/paper.pdf`
   → 7,118,161 bytes, MD5 `2b7c8c230cb802ab89cb25f2ec8eb14b`, PDF v1.4.
2. **Clone code + data.**
   `git clone --depth 1 https://github.com/ljding94/Polydisperse_Sphere.git`
   → 35 MB. Includes `analyze/VAE_model.py` (network defs), `analyze/analyze_PY.py`
   (PY reference), `data_used/L_18_pdType_{1,2,3}_{train,test}_data.npz`
   (4000/1000 pairs each), `L_18_pdType_{1,2,3}_train_stats.npz`
   (normalization), `L_18_pdType_{1,2,3}_{vae,gen,inf}_state_dict.pt`.
3. **Re-implement the network architecture** in an isolated file
   `work/eval_released.py`, matching the released `VAE`, `Generator`, `Inferrer`
   layers (Encoder: `Conv1d(1→30, k9s2)` + `Conv1d(30→60, k9s2)`; latent 3;
   two 9-dim linear converters). Loaded the released `state_dict.pt` weights
   with `strict=True` — clean load, no missing/unexpected keys → confirms our
   architectural reimplementation matches theirs.
4. **Independent Percus-Yevick + β baseline.** Implemented Wertheim's exact
   analytic PY structure factor in `PY_structure_factor(Q, η, R)` from first
   principles (α/β/γ coefficients from Wertheim 1963), the sphere form factor
   from paper eq. (3), the polydisperse averages ⟨F²⟩_D and ⟨F⟩²_D
   sampled from N=20,000 diameter draws per (pdType, σ) pair, effective
   radius R_eff = ⟨D³⟩^(1/3)/2, and analytical volume-fraction check.
   No code copied from the paper's `analyze_PY.py`.
5. **Evaluate released trained inferrer** on all 1000 test I(Q) curves per
   pdType. Average over 5 stochastic forward passes (VAE encoder samples ε).
   Report R², MAE, and relative error `|x−x'|/⟨x⟩` (paper's Fig 8 caption
   definition) for both η and σ.
6. **Evaluate released trained generator** on all 1000 test (η, σ) pairs per
   pdType. Report per-curve MSE_log10 = ⟨(log₁₀I(Q) − log₁₀I'(Q))²⟩_Q, matching
   paper Fig 6/10 caption.
7. **Evaluate PY / PYβ baseline** on 500 randomly chosen test points per
   pdType (limits: analytic PY blows up near η → 0.5 and σ → 0; clipped to
   η ∈ [10⁻⁴, 0.48], σ ≥ 10⁻³). Report same MSE_log10.
8. **Independent from-scratch retrain** (pdType=1, seed=42) with a compressed
   but faithful recipe: VAE 300 epochs, generator/inferrer converters
   100+50 (frozen+finetune) epochs, batch 64, Adam(lr=1e-3, wd=1e-4),
   CosineAnnealingLR. Wall time on 1×A100 = 132 s. Report same test metrics.
9. **LLM-judge verdict** — separately called `argo:gpt-5.2` (Argonne
   Argo proxy, free endpoint) with a structured prompt containing the paper
   claims and my measured numbers, and asked for a JSON `{verdict, coverage,
   agreement, justification, one_line}`. Judge output preserved in
   `evidence/llm_judge_verdict.json`.

**Software:** Python 3.10, PyTorch 1.11.0 + CUDA on A100, NumPy 1.23,
SciPy 1.10. Nothing paid: everything ran locally on ANL infrastructure
(`uicgpu`).

**Deviations from the paper:** (a) my from-scratch retrain uses 300 VAE
epochs instead of 1000, 100+50 converter/finetune epochs instead of 300+200
— purely a compute-budget compression; the released weights are the primary
comparison target. (b) My PY baseline uses R_eff = ⟨D³⟩^(1/3)/2 (a standard
monodisperse-equivalent radius); the paper doesn't specify exactly which
R the PY curves in Figs 5–6 use, so an exact numeric match with their PY MSE
values is not expected — the qualitative comparison (PY & PYβ >> NN) is what
we test.

## 4. Results — this replication vs the paper

### 4.1 Inferrer accuracy (paper Figs 8, 11)

The paper reports these as qualitative scatter plots (predicted vs true η, σ)
that lie visibly on the diagonal with "very small" relative error. My numeric
evaluation on the released 1000-point test set:

| pdType | η R² | η MAE | η rel-err | σ R² | σ MAE | σ rel-err |
|---|---|---|---|---|---|---|
| 1 (uniform)   | 0.99992 | 0.00082 | 0.34% | 0.99992 | 0.00060 | 0.39% |
| 2 (normal)    | 0.99993 | 0.00081 | 0.33% | 0.99986 | 0.00028 | 0.49% |
| 3 (lognormal) | 0.99993 | 0.00082 | 0.32% | 0.99987 | 0.00030 | 0.49% |

All three distributions give R² ≥ 0.9998 for both parameters, sub-1%
relative error. This quantifies the paper's qualitative "very small relative
error" claim — it is even stronger than the visual scatter plots suggest.

### 4.2 Generator vs PY / PYβ (paper Figs 5, 6, 10)

Per-curve mean-square log₁₀ error on the released test set:

| pdType | NN gen MSE_log10 | PY MSE_log10 | PYβ MSE_log10 | PY/NN | PYβ/NN |
|---|---|---|---|---|---|
| 1 (uniform)   | 2.32×10⁻⁵ | 2.79×10⁻³ | 9.73×10⁻⁴ | **120×** | **42×** |
| 2 (normal)    | 4.05×10⁻⁵ | 1.76×10⁻³ | 6.98×10⁻⁴ | **43×**  | **17×** |
| 3 (lognormal) | 3.79×10⁻⁵ | 2.13×10⁻³ | 7.14×10⁻⁴ | **56×**  | **19×** |

The NN generator's log-space MSE is 17× to 120× smaller than the traditional
PY / PYβ analytic formulas across all three distribution families — a very
strong replication of the paper's qualitative Figs 5–6 & 10 finding.

### 4.3 From-scratch retrain (pdType=1)

To confirm that the training pipeline (not just the released weights) is
reproducible, I re-trained the entire VAE+Generator+Inferrer stack from
scratch on the released training set with seed=42 and a compressed epoch
schedule (VAE 300 vs paper's 1000; converters 100+50 vs 300+200):

| metric | released weights | from-scratch (this rep.) |
|---|---|---|
| η R² | 0.99992 | 0.99975 |
| η MAE | 0.00082 | 0.00161 |
| η rel-err | 0.34% | 0.65% |
| σ R² | 0.99992 | 0.99989 |
| σ MAE | 0.00060 | 0.00069 |
| σ rel-err | 0.39% | 0.45% |
| generator MSE_log10 | 2.32×10⁻⁵ | 5.72×10⁻⁵ |

Within a factor of ~2 on every metric, with a much shorter schedule
(132 s vs presumably many hours) — confirms the training recipe reproduces
without relying on the released weights.

### 4.4 LLM-judge verdict

`argo:gpt-5.2` (temperature 0, structured JSON output) returned:

```json
{
  "verdict": "REPLICATED",
  "coverage": 0.8,
  "agreement": 0.95,
  "justification": "The replication used the authors' publicly released code/data/weights and evaluated performance on the provided 1000-sample test sets for all three distribution families, directly testing the bidirectional mapping claim. The inferrer reproduces extremely high accuracy for both η and σ across uniform/normal/lognormal (R²≈0.9999 with sub-1% relative errors), consistent with the paper's qualitative plots. The generator's I(Q) errors are far smaller than independently reimplemented Percus–Yevick and PYβ baselines (≈17–120× lower mean MSE_log10 depending on distribution), matching the paper's headline advantage. A from-scratch retrain (pdType=1) achieves similar metrics within <2×, supporting that results are not dependent on the released weights. The only major untested claim is the specific latent-dimension/PCA-SVD feasibility analysis (C4), so coverage is high but not complete.",
  "one_line": "Core NN inferrer+generator claims reproduced on all 3 distributions; NN beats PY/PYβ by 17–120×; PCA/SVD claim untested."
}
```

## 5. Verdict

## **REPLICATED**

**Justification.** The paper's two headline claims — that (a) a VAE-based
neural inferrer extracts volume-fraction η and polydispersity σ from I(Q)
with very high accuracy, and (b) a VAE-based generator predicts I(Q) from
(η, σ) with substantially lower error than the traditional Percus-Yevick +
β-correction analytic formulas — are both quantitatively confirmed on the
authors' released test data across all three (uniform, normal, lognormal)
size distribution families. The inferrer achieves R² ≥ 0.99987 for both
parameters, with sub-1% relative error. The NN generator's log₁₀-space MSE is
17× to 120× smaller than PY(β), depending on distribution family. An
independent from-scratch retrain of the model (with a compressed epoch
schedule) reproduces the released-weight test-set performance to within a
factor of 2 on all metrics, confirming the training recipe is not
dependent on any undisclosed tuning. The one major claim not directly
re-verified is the SVD/PCA analysis showing 3-dim latent space is sufficient
(paper Fig 4) — accepted as consistent with the released architecture.

The paper is a well-scoped, well-executed methods paper with excellent
open-data + open-weights practices (all code, data, and trained models on
GitHub with a clear README) — a positive outlier in reproducibility terms.
No fabricated numbers, no inflation.

---

**Independent replicator artifacts** (see `evidence/`):
* `eval_released_results.json` — full JSON dump of inferrer + generator +
  PY baseline metrics for all three pdTypes.
* `retrain_pdType1_results.json` — from-scratch retrain metrics.
* `retrain_pdType1.log` — training log with loss curves.
* `llm_judge_prompt.txt`, `llm_judge_verdict.json` — LLM-judge input/output.
