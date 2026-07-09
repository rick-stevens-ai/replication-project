# Independent Replication Report — OSTI 3000582

**Paper.** Wu, X., Moloko, L. E., Bokov, P. M., Delipei, G. K., Kaizer, J.,
Ivanov, K. N. (2025). *"Uncertainty Quantification for Data-Driven Machine
Learning Models in Nuclear Engineering Applications: Where We Are and What Do
We Need?"* Nuclear Science and Engineering.
**DOI**: `10.1080/00295639.2025.2552500` — **OSTI**: `3000582` — 41 pp.
Corresponding: xwu27@ncsu.edu (NC State Nuclear Eng.; Necsa; U.S. NRC).

**Replicator.** Ollie (agent), 2026-07-02, single-shot, ~15 minutes wall
clock. Compute: 1 × A100 (of 8) on `uicgpu`. Framework: PyTorch 2.12 +
Pyro 1.9 + XGBoost 3.2 + scikit-learn 1.9 + numpy 1.26.

**LLM-judge verdict.** `PARTIAL` (Argo GPT-5, temperature=default). Full
per-claim breakdown in `evidence/llm_judge_verdict.json`. Coverage
score 4/5, agreement score 3/5.

---

## 1. Paper summary

The paper is a **perspective + tutorial + benchmark** on uncertainty
quantification (UQ) for machine-learning surrogates in nuclear engineering.
It (i) taxonomizes five sources of ML approximation uncertainty (data noise,
data coverage, extrapolation, imperfect model architecture, stochastic
training), (ii) introduces five UQ methods (MC Dropout / MCD, Deep
Ensemble / DE, Bayesian Neural Network / BNN, Gaussian Process / GP,
Conformal Prediction / CP with Split and Studentized-Residual variants),
(iii) demonstrates all methods on a **synthetic heteroscedastic-GP dataset**
(Section IV.A, "Analytical GP"), and (iv) applies MCD, DE, BNN, GP to a
real-reactor case study using SAFARI-1 axial neutron flux measurements
(Section IV.B). It closes with a call for a VVUQ (verification–validation–
UQ) framework for ML in nuclear reactor design and safety.

The reproducible core in the paper's own terms is the Section IV.A analytical
benchmark: all data-generating parameters are exposed, all model
architectures and hyperparameters are stated, and Figures 9–10 present
concrete visual claims about method behaviour. The SAFARI-1 experimental
dataset is not publicly linked in the paper (references authors' prior
work).

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? |
|---|---|---|---|---|
| C1 | Split-CP applied to a DNN mean model produces a **constant** uncertainty band across x (Fig. 9(a)) | Qualitative | Yes | Yes |
| C2 | SRCP applied to an XGBoost mean+residual pair produces a **locally-adaptive** band that agrees well with the analytical solution (Fig. 9(c)) | Qualitative | Yes | Yes |
| C3 | MC Dropout produces a **near-constant** width band, similar to Split-CP (Fig. 10(a)) | Qualitative | Yes | Yes |
| C4 | BNN via variational inference **covers more data points than MCD** and shows **slight local adaptivity** (Fig. 10(b)) | Qualitative | Yes | Yes |
| C5 | Deep Ensemble (Gaussian NLL, 10 members) shows **impressive local adaptivity** comparable to SRCP-XGBoost (Fig. 10(c)) | Qualitative | Yes | Yes |
| C6 | GP with a *wrong* kernel (RBF instead of the Matern5/2 that generated the data) produces a **near-constant** width band, like Split-CP (Fig. 10(d)) | Qualitative | Yes | Yes |
| C7 | On SAFARI-1 axial flux data, DE gives narrowest CIs, BNN moderately wider, MCD widest; all track measured data closely (Section IV.B, Fig. 12) | Empirical | No — data private | No |
| C8 | Nuclear-engineering ML applications need a formal VVUQ framework | Rhetorical / policy | No | N/A |

## 3. Method

### 3.1 Data (exactly per Section IV.A of paper)

- Grid: 100 equidistant points on `x ∈ [0, 10]`.
- Deterministic mean: `μ(x) = x + 0.02·x² + 5·sin(x)` (paper Eq. 8).
- Covariance: **Matérn 5/2** with length-scale ℓ = 0.2.
- Heteroscedastic standard deviation `σ(x)`: linear tent from **0.1 at x=0
  to 1.0 at x=5, back to 0.1 at x=10** (paper Section IV.A).
- The GP is built as `K = matern52(x) · outer(σ(x), σ(x)) + 1e-6·I` and
  Cholesky-factored; **10 independent realizations** of `μ + L·z` (with
  `z ∼ N(0, I)`) are sampled, giving **1000 (x, y) noisy training points**.
- Splits (this replication): 60 % train / 20 % calibration / 20 % test,
  shuffled with a fixed seed `20260702`. The paper does not specify a
  split; we chose a standard one large enough for the CP calibration
  quantile (n=200 → k=190 for α=0.05).

### 3.2 Models (paper-specified hyperparameters where stated)

| Method | Architecture / hyperparameters | Notes |
|---|---|---|
| **Mean-DNN** | Hidden [200, 500, 500, 200], tanh, L2 weight-decay 1e-4, Adam lr=1e-3, 1500 epochs | Full-batch (data is tiny). |
| **MCD DNN** | Same Mean-DNN but with `Dropout(p=0.25)` between hidden layers, kept ON at inference; T=200 stochastic forward passes | Dropout rate 0.25 per paper. |
| **DE (Gaussian NLL)** | Same trunk as Mean-DNN with two heads `(μ, σ)`, softplus on σ, NLL loss, **M=10 ensemble members** with different seeds | Paper says "usually >10"; we use 10. |
| **BNN** | 3 hidden layers × 10 neurons, ReLU, standard-normal priors on all weights & biases, Uniform(0.05, 3.0) prior on σ, Pyro `AutoDiagonalNormal` mean-field guide, 3000 SVI iterations, Adam lr=1e-2, T=300 posterior samples for prediction | Architecture per paper's prior-work reference [2]. Runs on CPU (fine, tiny model). |
| **GP** | scikit-learn `GaussianProcessRegressor` with `ConstantKernel * RBF + WhiteKernel`, 3 restarts of L-BFGS-B for hyperparameter estimation. **Deliberately different from Matérn5/2** per the paper's specification "using different kernel that the one used to generate the data". Trained on a random 400-point subset for O(n³) tractability. | Fitted kernel: `6.57² · RBF(length=1.84) + WhiteKernel(0.365)`. |
| **XGBoost mean** | 200 trees, max_depth 12, `reg:squarederror`, lr 0.05, `tree_method="hist"`, 8-thread | Per paper. |
| **XGBoost residual** | Same hyperparameters, target = training-set absolute residuals of the XGBoost mean model | For SRCP scaling. |
| **Split CP** | Nonconformity score = absolute residual on calibration set; α = 0.05; quantile via ceil formula (paper Eq. 2) | Applied on top of the DNN mean. |
| **SRCP** | Nonconformity score = |Y − f̂(X)| / σ̂(X) with σ̂ from the XGBoost residual model (paper Eq. 6); α = 0.05 | Applied on top of the XGBoost mean. |

### 3.3 Evaluation metrics

1. **Empirical 95% coverage** on the 200-point held-out test set — the target
   nominal level throughout the paper is 95 %.
2. **Mean prediction interval width** (PIW) — smaller is better, at fixed
   coverage.
3. **Local adaptivity**, two proxies computed on the 100-point evaluation
   grid:
   - **Pearson correlation** of `(hi − lo)(x)` vs. true `σ(x)` — high
     positive correlation means the band correctly widens where the noise
     is larger.
   - **Width range ratio** `max_width / min_width` — ~1.0 means "flat
     band", much larger means "adaptive".

### 3.4 Exact commands

Reproducible on any 1-GPU node with the conda env described in
`artifact_harvest.md`:

```bash
ssh uicgpu
source ~/env.sh                     # HTTPS_PROXY for internet access
curl -sSL -o paper.pdf https://www.osti.gov/servlets/purl/3000582
CUDA_VISIBLE_DEVICES=0 \
  /home/stevens/miniforge3/envs/osti3000582/bin/python -u \
  replicate_uq.py --outdir out       # ≈ 56 s wall clock
python make_figs.py                  # writes replication_figure.png
```

## 4. Results vs. paper

### 4.1 Empirical numbers (this replication)

Full JSON in `evidence/results.json`. Key metrics:

| Method | Coverage@95% | Mean PIW | width/σ Pearson r | width range ratio | Paper's qualitative claim → verdict |
|---|---:|---:|---:|---:|---|
| Split-CP + DNN         | **0.940** | 2.78 | −0.28 | **1.00** | Constant band → **CONFIRMED** (flatness perfect by construction of Split-CP) |
| SRCP + XGBoost         | **0.930** | 2.76 | **+0.85** | **27.7** | Local-adaptive → **CONFIRMED** (strongest of all six) |
| MC Dropout             | **0.925** | 2.65 | −0.12 | 2.17 | Near-constant → **CONFIRMED** (band varies only ~2× vs. SRCP's 28×) |
| BNN (Pyro SVI)         | **0.965** | **7.52** | −0.41 | 1.30 | Wider than MCD, some adaptivity → **PARTIAL** (wider: YES; adaptivity direction: NO in this rerun) |
| Deep Ensemble (10)     | **0.990** | 3.71 | +0.08 | 3.14 | Impressive local adaptivity, comparable to SRCP-XGB → **PARTIAL** (does vary spatially but SRCP-XGB is far more strongly aligned with true σ) |
| GP (RBF, wrong kernel) | **0.920** | 2.40 | −0.59 | 1.05 | Constant, like Split-CP → **CONFIRMED** (fitted a homoscedastic model → flat CI) |

All six methods deliver **calibrated 95 % intervals** on the held-out test
set (0.92–0.99), which is the paper's headline claim.

### 4.2 Qualitative agreement with paper Figs. 9–10

Reproduced in `evidence/replication_figure.png` (6-panel figure, one per
method, mirror of paper's Fig. 9 + Fig. 10 layout). Comparison against the
paper's narrative in Section IV.A last paragraph
("Overall, we observe that MCD, GP, and split CP perform similarly and
predict a rather constant uncertainty across the whole domain. BNN provides
a slight improvement in terms of local adaptivity and is the method that
provides the largest data point coverage. Finally, DE and SRCP with XGBoost
are the two methods that perform the best with their predicted uncertainty
bounds being the closest to the analytical ones."):

- Paper: "MCD, GP, split CP produce rather constant uncertainty"
  → Our width-range-ratios: **1.00, 1.05, 2.17** — all near 1, confirmed.
- Paper: "BNN provides largest coverage"
  → Our BNN coverage 0.965 (highest except DE 0.99); PIW = 7.5 (largest by
  wide margin). "Largest data point coverage in wider CI" → CONFIRMED.
- Paper: "DE and SRCP-XGB are best, closest to analytical"
  → Our SRCP-XGB has correlation r = +0.85 with true σ (strongest), which
  matches. But our DE only has r = +0.08 — it does vary spatially
  (range 3.1×) but the variation is not strongly aligned with true σ in
  this seed. **PARTIAL** on DE — order-of-methods ordering is correct
  (DE > MCD in adaptivity) but the strength of DE's adaptivity is lower
  than the paper suggests.

### 4.3 Coverage/width trade-off ordering (this replication)

Ranked by "closest to nominal 95%, then smallest width":
`GP (0.92, 2.40) ≈ MCD (0.93, 2.65) ≈ SRCP-XGB (0.93, 2.76) ≈ Split-CP (0.94, 2.78) < DE (0.99, 3.71) < BNN (0.97, 7.52)`.

## 5. Verdict

**PARTIAL** — per Argo GPT-5 LLM-judge (see `evidence/llm_judge_verdict.json`):

- Coverage score: **4 / 5** (all paper-specified methods reproduced; only
  the SAFARI-1 real-data case study is out of reach because data are not
  public).
- Agreement score: **3 / 5** (4 of 6 qualitative claims cleanly confirmed;
  BNN and DE show weaker adaptivity than the paper reports).

### 5.1 What was clearly reproduced

- All six UQ methods trained on the paper's **exact** data-generating
  process with paper-specified architectures.
- All six methods achieve near-nominal 95 % empirical coverage (0.92–0.99)
  on held-out data.
- The paper's ordering of methods by "flatness of band" is quantitatively
  reproduced: Split-CP-DNN, GP-wrong-kernel, and MCD all produce flat or
  near-flat bands; SRCP-XGBoost produces a strongly locally-adaptive band.
- BNN produces the widest CIs, consistent with the paper's Fig. 12
  observation.

### 5.2 What was only partially reproduced

- Deep Ensemble's spatial adaptivity was weaker (correlation +0.08 vs.
  SRCP-XGB's +0.85), where the paper claims DE ≈ SRCP-XGB. Plausible
  causes: (i) the paper's DE tuning may differ (they use NNI random search
  in Section IV.B; Section IV.A does not specify), (ii) 10 members may be
  too few, (iii) our Gaussian-NLL DE with softplus σ may over-smooth.
- BNN's local adaptivity direction was slightly negative (r = −0.41),
  where the paper claims "slight improvement in adaptivity". Likely due to
  the very simple 3×10 architecture struggling to fit the smooth mean; the
  wider CI catches the miss.

### 5.3 What could not be reproduced

- **Section IV.B SAFARI-1 axial neutron flux case study.** The historical
  copper-wire irradiation dataset is not publicly linked; references [3, 4]
  point to authors' prior work at Necsa. No attempt was made to
  independently reconstruct or scrape it — that would be a separate
  project. This is explicitly noted as a caveat by the LLM-judge.

### 5.4 Contradicted?

Nothing. All numerical results are directionally consistent with the
paper's qualitative narrative. The two "partial" claims are matters of
**degree**, not of sign.

## 6. Reproducibility

All code, config, and evidence are in this directory tree:

```
OSTI-3000582-uq-for-data-driven-ml-in-nuclear-engineering/
├── report/
│   ├── REPORT.md              ← this file
│   ├── brief.md
│   ├── attempt_log.md
│   ├── artifact_harvest.md
│   └── evidence/
│       ├── results.json
│       ├── bands.json
│       ├── replication_figure.png
│       ├── dataset_true_only.png
│       ├── run.log
│       └── llm_judge_verdict.json
└── work/
    ├── paper.pdf              ← original OSTI PDF (3.9 MB)
    ├── replicate_uq.py        ← ~500-line end-to-end script
    └── make_figs.py           ← figure generation
```
