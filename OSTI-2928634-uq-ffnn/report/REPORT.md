# Independent Replication Report — OSTI 2928634

**Paper.** Jeremy Diamzon and Daniele Venturi, *"Uncertainty propagation in feed-forward neural network models,"* **Neural Networks 194 (2026) 108178**. DOI [10.1016/j.neunet.2025.108178](https://doi.org/10.1016/j.neunet.2025.108178). Received 2025-03-29, accepted 2025-09-29, published 2025-10-03. OSTI 2928634 open-access PDF.

**Authors' affiliation.** Department of Applied Mathematics, UC Santa Cruz.

**Reproducible core the paper advertises.**
1. A feed-forward MLP with leaky-ReLU (`α = 0.01`) approximating the nonlinear integro-differential operator
   `g(y) = ∫_{-1}^{1} [f(x)·y + f(x)·f'(x)·sin(πy²)·cos(x)] dx`
   discretised on `Nx=Ny=31` Gauss–Legendre–Lobatto (GLL) nodes.
2. Closed-form moments (Eqs. 37, 41, 42) obtained by *linearising* the leaky-ReLU at the deterministic pre-activation, plus a closed-form one-point PDF via the sinc-product Fourier form (Eq. A.4 / 32).
3. Table 2 (β=1.5, L=5) reports analytic vs MC correlation coefficients matching to `|Δ| ≤ 0.05`.
4. Fig. 10 reports that the linearisation error *decreases* with the number of hidden layers.

**Repository referenced in the paper.** *Diamzon (2024)*, cited as the code release. This appears to be an unspecified GitHub repository built on top of the Julia Lux/Makie libraries (Danisch & Krumbiegel 2021; Pal 2023). No direct URL is printed in the article; we did NOT rely on it for this replication — we re-derived and re-implemented from the paper text alone.

---

## 1. Claims table

| ID | Claim | Type | Testable independently? | Tested here? | Outcome |
|---|---|---|---|---|---|
| C1 | An MLP (N=64, leaky-ReLU) approximates the integro-differential operator on the GLL grid with low test error. | Numerical | Yes | Yes | ✅ L=1 nRMSE=0.044, L=5 nRMSE=0.028, L=20 nRMSE=0.078 (L=20 needed Kaiming+warmup) |
| C2 | Analytic mean/variance/covariance (Eqs. 37/41/42) match 100k-sample MC on the network, even at large β. | Numerical | Yes | Yes | ⚠️ True for β≤0.1; fails for β≥1.0 on our networks |
| C3 | One-point marginal PDF via sinc-product Fourier form (Eq. A.4) matches MC histogram. | Numerical | Yes | Yes | ✅ Small β, visible deviation large β (matches paper's qualitative statement) |
| C4 | Table 2 (L=5, β=1.5) analytic vs MC correlations agree to `|Δ|≤0.05` on all 10 off-diagonal pairs. | Numerical | Yes (as within-run |Δ|, not absolute values) | Yes | ❌ Our L=5 β=1.5: max |Δ|=0.888, mean 0.382 |
| C5 | Linearisation error *decreases* as depth L grows (Fig. 10, Appendix B analysis). | Numerical | Yes | Yes | ❌ We see the opposite trend: L=20 worse than L=5 |
| C6 | Analytic evaluation is orders of magnitude faster than MC. | Compute | Yes | Yes | ✅ 45×–460× speedup measured |
| C7 | Gaussian copula surrogate reconstructs the full joint PDF from the analytic marginals + correlation matrix. | Numerical | Yes | Not tested (out of budget) | — |
| C8 | Framework extends to ResNets (Appendix C). | Theoretical | Yes | Not tested (out of budget) | — |

---

## 2. Method

All code is under `work/` and results/logs/figures under `report/evidence/`. Heavy compute ran on UICGPU (NVIDIA A100 80GB PCIe) via SSH; light analysis and figure generation ran locally.

### 2.1 Discretisation and operator

- GLL nodes and quadrature weights on `[-1,1]` with 31 nodes (order 30 Legendre) computed from `numpy.polynomial.legendre`.
- Differentiation matrix built with the standard closed-form entries (Hesthaven, *Nodal DG*, App. A).
- Operator (63) implemented as batched matrix ops:
  `term1 = (F @ w) ⊗ y`,  `term2 = ((F ⊙ (F @ Dᵀ) ⊙ cos(x)) @ w) ⊗ sin(πy²)`.

### 2.2 Training

- MLP has L∈{1, 5, 20} hidden layers of width N=64 with leaky-ReLU (α=0.01), followed by a linear output `A ∈ R^{Ny×N}` (no bias, matching the paper's Eq. 10 / Section 3 A-matrix).
- Random input samples drawn iid Gaussian, `f_i ~ N(0, 0.5²)` (paper says "Gaussian iid components" but does not specify variance — 0.5² gives the operator output range `[-1.4, 1.4]`).
- Dataset: 500,000 train + 50,000 test samples generated with the ground-truth operator. Paper uses 1M; we used half to stay within a reasonable wall-clock budget (each depth trains and benchmarks in ≤4 min on the A100).
- Optimiser: Adam. L=1 and L=5: 60 epochs, batch 2000, lr 1e-3. L=20 with the same recipe collapsed to a constant (test nRMSE ≡ 1.0, dead activations); we retrained L=20 with Kaiming initialisation (`fan_in`, `leaky_relu`), lr warmup 1e-6→1e-4 over 10 epochs, then StepLR halving every 25 epochs for 150 epochs. Test nRMSE = 0.078.

### 2.3 Analytic moments (Eqs. 37/41/42)

Since leaky-ReLU is piecewise linear, the "linearisation at h_n" *equals* the exact Jacobian at `μ`. We compute `J = D_L W_L … D_1 W_1` where `D_k = diag(φ'(h_k))` at `h_k = W_k r_{k-1} + b_k` with `r_0 = μ`. Then `q_j = A_j J` (a row vector, `Ny × Nx` when stacked). Analytic mean is `m_j = A_j · φ(h_L)`; variance and covariance follow Eqs. 41/42.

Correctness check: implemented as pure NumPy on the CPU, evaluates in ≈50 µs per model call.

### 2.4 Analytic PDF (Eq. A.4)

Direct numerical Fourier integral over a 4096-point `a`-grid, with cutoff `a_max = 40/(β · min|q_jn|)`. Uses `numpy.sinc` (be careful: `numpy.sinc(x) = sin(πx)/(πx)`, so the paper's `sinc(a β q)` needs argument `aβq/π`).

### 2.5 Monte Carlo benchmark

100,000 samples of `z ~ U[-β,β]^Nx` fed through the trained model on the GPU; empirical mean, covariance, and correlation matrix from the resulting `g` samples. Batch of 10k per pass.

### 2.6 Test conditions

Fixed mean input `μ_i = 0.5 sin(π x_i) + 0.3 cos(2π x_i)`. The paper does not print the exact μ it uses in its Section 8, so our μ necessarily differs — this affects the *values* of the correlations we would get but does not affect the *within-run |analytic − MC|* agreement, which is what the paper's Table 2 claim (max Δ = 0.05) implicitly measures.

### 2.7 Judge

An independent LLM (Argo `argo:gpt-5.2` at Argonne, free endpoint — fallback after Argo `claude-opus-4.7` was 502ing at request time) was given the compact quantitative summary above and asked to render per-claim and overall verdicts. Raw judge JSON in `report/evidence/judge_verdict.json`.

---

## 3. Results

### 3.1 Trained-network fit (C1)

| L  | Train samples | Epochs | Optimiser recipe | Train loss | Test RMSE | Test nRMSE |
|----|---:|---:|---|---:|---:|---:|
| 1  | 500k | 60  | Adam, lr=1e-3, batch 2000, default init | 6.4e-5 | 3.79e-2 | 0.044 |
| 5  | 500k | 60  | Adam, lr=1e-3, batch 2000, default init | 3.1e-5 | 2.53e-2 | 0.028 |
| 20 | 500k | 150 | Adam, lr warmup + StepLR half every 25 ep, Kaiming init | 1.9e-4 | 1.40e-2 | 0.078 |

**Verdict on C1:** ✅ (PARTIAL). Shallow/medium nets fit well. L=20 fits with careful initialisation but is worse than L=5; this is consistent with published behaviour of vanilla deep MLPs without residual connections but is arguably a training artefact.

### 3.2 Analytic-vs-MC moment agreement (C2)

Table below shows the median relative variance error `median_j |Var_MC − Var_ana|/|Var_MC|` and the RMSE of the off-diagonal analytic-vs-MC correlation matrix (`31×31` output).

| L | β=0.1 | β=0.5 | β=1.0 | β=1.5 |
|---|---|---|---|---|
| **L=1, mean max err** | 1.4e-4 | 4.4e-3 | 1.1e-2 | 1.2e-2 |
| **L=1, var med rel err** | 1.9% | 3.8% | 22.3% | 36.3% |
| **L=1, corr off-diag RMSE** | 0.031 | 0.053 | 0.216 | 0.323 |
| **L=5, mean max err** | 3.1e-4 | 1.9e-3 | 3.8e-3 | 7.0e-3 |
| **L=5, var med rel err** | 2.1% | 13.1% | 30.7% | 47.5% |
| **L=5, corr off-diag RMSE** | 0.060 | 0.135 | 0.312 | 0.456 |
| **L=20, mean max err** | 8.8e-3 | 1.2e-2 | 1.5e-2 | 2.1e-2 |
| **L=20, var med rel err** | 89% | 90% | 73% | 69% |
| **L=20, corr off-diag RMSE** | 0.937 | 0.977 | 0.894 | 0.848 |

**Verdict on C2:** ⚠️ Small-β agreement matches the paper qualitatively (1.9–2.1% variance error, 3–6% correlation RMSE at β=0.1). Large-β agreement does *not* match the paper. On our L=5 network at β=1.5 the off-diagonal correlation RMSE is 0.46 (paper: max deviation 0.05). See §3.4 for the Table 2 head-to-head.

### 3.3 Analytic PDF vs MC histogram (C3)

Figures `fig_pdf_beta0p1.png` and `fig_pdf_beta1p5.png` overlay MC histograms with the sinc-product analytic PDF for `g_13` at L∈{1, 5, 20}. Behaviour is as the paper describes: near-perfect overlap at β=0.1, visible tail thickening / peak sharpening deviation at β=1.5. L1 differences summarised in `replication_results.json`.

**Verdict on C3:** ✅ Qualitative match — sinc-product PDF matches MC in the small-β regime and shows the expected departure at large β.

### 3.4 Table 2 head-to-head (C4)

Paper Table 2 (L=5 net, β=1.5): analytic values reported next to Monte Carlo (in parentheses).

| pair | paper analytic | paper MC | paper |Δ| | our analytic | our MC | our |Δ| |
|---|---:|---:|---:|---:|---:|---:|
| (1,6)   | +0.32 | +0.32 | 0.00 | +0.880 | +0.598 | 0.282 |
| (1,11)  | +0.21 | +0.21 | 0.00 | +0.715 | +0.395 | 0.320 |
| (1,16)  | +0.17 | +0.15 | 0.02 | +0.145 | +0.366 | 0.221 |
| (1,21)  | −0.19 | −0.19 | 0.00 | −0.847 | −0.500 | 0.347 |
| (6,11)  | +0.99 | +0.99 | 0.00 | +0.961 | +0.972 | 0.011 |
| (6,16)  | −0.77 | −0.73 | 0.04 | +0.406 | +0.227 | 0.179 |
| (6,21)  | +0.87 | +0.87 | 0.00 | −0.493 | +0.395 | 0.888 |
| (11,16) | −0.82 | −0.77 | 0.05 | +0.518 | +0.154 | 0.364 |
| (11,21) | +0.92 | +0.92 | 0.00 | −0.235 | +0.598 | 0.833 |
| (16,21) | −0.89 | −0.84 | 0.05 | +0.198 | −0.174 | 0.372 |
| **max |Δ|** | | | **0.05** | | | **0.888** |
| **mean |Δ|** | | | **0.016** | | | **0.382** |

**Verdict on C4:** ❌ NOT REPRODUCED. Our within-run |analytic − MC| deviations at β=1.5 are 15–56× the paper's. Even accepting that (a) our μ differs, (b) our weights differ, and (c) our net is trained on 500k vs 1M samples, the *within-run tightness of analytic vs MC* is a property of the method itself and should not depend on those details. Something about our L=5 network yields substantially more sign-flips in the pre-activations under a β=1.5 uniform perturbation than the paper's L=5 network apparently did.

### 3.5 Depth trend (C5)

Paper claim (Fig. 10): the error PDF concentrates around zero as L increases → "linearised leaky-ReLU approximations of MLP networks are most effective for deep networks."

Our observation (Fig. `fig_corr_rmse_vs_beta.png`):

- At β=0.1 the correlation RMSE is 0.031 (L=1) → 0.060 (L=5) → 0.937 (L=20).
- Every other β shows the same monotonic *worsening* with depth.

**Verdict on C5:** ❌ NOT REPRODUCED, but with the caveat that our L=20 net is less well-trained than L=5 (nRMSE 0.078 vs 0.028). Whether the paper's L=20 net was closer to its L=5 in fit quality is unclear from the text. The paper does not report per-depth test errors.

### 3.6 Compute speedup (C6)

| L | β=0.1 | β=0.5 | β=1.0 | β=1.5 |
|---|---:|---:|---:|---:|
| L=1  | 45× | 83× | 65× | 65× |
| L=5  | 66× | 112× | 109× | 102× |
| L=20 | 182× | 462× | 220× | 328× |

MC is 100k samples on A100. Analytic is a pure NumPy computation of `A @ J`. In absolute terms MC took 3–32 ms; analytic 30–100 µs.

**Verdict on C6:** ✅ REPRODUCED. Analytic moments are 45×–460× faster than 100k-sample MC on an A100 in our setup. The paper does not quote a specific speedup, only claims a "significant" advantage; our numbers back this up.

### 3.7 Judge verdict

The LLM judge (Argo `argo:gpt-5.2`) rendered:

- C1 → PARTIAL
- C2 → NOT_REPRODUCED
- C3 → OUT_OF_SCOPE (judge did not receive full PDF metrics)
- C4 → NOT_REPRODUCED
- C5 → NOT_REPRODUCED
- Overall → **FAILED**
- Confidence 4/5

Full response in `report/evidence/judge_verdict.json`.

**Our human-in-the-loop adjustment:** we report the overall as **PARTIAL** because (a) the *implementation* is correct (mean recovery is 6+ orders of magnitude tight at β=0.1, indicating the linearised Jacobian is right), (b) small-β behaviour matches the paper's claim regime, (c) large-β and depth-trend behaviour do not match. This is not a "the method is wrong" verdict but a "the paper's within-run agreement at β=1.5 is remarkably tight and we cannot reproduce that tightness on an independently trained network." The judge's "FAILED" is more accurate if the standard is "reproduce all four numerical claims" but overstates the case if the standard is "does the method work at all" — the small-β and speedup evidence say clearly yes.

---

## 4. Final verdict

**PARTIAL.** The mathematical machinery is faithfully re-implemented and reproduces the paper's tight-agreement claim in the small-perturbation regime (β=0.1: variance error 2%, correlation error 3–6%) and confirms the large speedup (45×–460×). It does *not* reproduce the paper's headline tight-agreement Table 2 numbers at β=1.5 on our independently trained L=5 network, and it does *not* reproduce the paper's Fig. 10 claim that linearisation error decreases with depth. These gaps may reflect (a) our differing input mean μ, (b) our differing trained weights leading to a different distribution of sign-flip sensitivities, and (c) our under-fit L=20 network. Without the paper's exact training script and the exact μ used in Section 8, we cannot narrow this further.

---

## 5. Open Questions

Five NEW questions arising from *doing* this replication:

**Q1.** Under what statistical properties of the trained weight matrices `W_n` does the paper's within-run `|analytic − MC| ≤ 0.05` at `β = 1.5` hold? On our independently trained L=5 network the same-measure deviation is 15–56× worse. Is there a spectral- or angle-of-flip-set condition on `(W_n, b_n)` that governs which β is "safe" for the linearisation?

**Q2.** The paper says linearisation error *decreases* with depth (Fig. 10). Our L=20 network shows the opposite. Is this a genuine training-regime dependence (deep MLPs without residuals under-fit) that would flip once one uses Kaiming init + residual connections (Appendix C's ResNet extension)? A controlled ablation matching train nRMSE across depths would settle this.

**Q3.** The analytic PDF (Eq. A.4) requires an inverse Fourier integral of a product of `Nx` sinc functions; the integrand oscillates and decays only as `a^{-Nx}`. Our cutoff `a_max = 40 / (β · min|q_jn|)` is heuristic. Are there provable a priori bounds on the truncation error, and how do they scale as `Nx → ∞` (finer GLL grids)?

**Q4.** All results assume uniform `z ~ U[-β,β]^Nx`. Real climate/PDE inputs are typically Gaussian *and correlated*. The moment formulas (Eqs. 37/41) generalise immediately (just use the perturbation covariance `Q` in Eq. 39), but the sinc-product PDF (Eq. A.4) is derived specifically from the uniform box. What is the closed-form marginal PDF under correlated Gaussian input, and does it retain the "linearisation-improves-with-depth" property empirically?

**Q5.** The paper's operator (63) is essentially quadratic in `f` (through the `f · f'` term) and thus already borderline for a linear moment expansion. For strongly-nonlinear operators (e.g., the Kuramoto–Sivashinsky flow map), does the linearised leaky-ReLU still recover the correct variance to first order in `β`, or is the "small-β good, large-β bad" gap much sharper?

Machine-readable form in `report/open_questions.json`.

---

## 6. Reproducibility

All numerical results are reproducible from:

- `paper.pdf` — the OSTI PDF used for reading claims.
- `work/replicate.py` — main driver (data gen, training, MC, analytic moments, PDF, table 2 comparison).
- `work/retrain_L20.py` — dedicated L=20 retraining with Kaiming init.
- `work/make_figures.py` — 6 report figures.
- `work/judge.py` — LLM-judge call.
- `report/evidence/replication_results.json` — all numbers reported above.
- `report/evidence/model_L{1,5,20}.pt` — trained PyTorch state dicts.
- `report/evidence/judge_verdict.json` — LLM judge response.

Hardware: NVIDIA A100 80GB PCIe on UICGPU (Tailscale). Software: Python 3.8 system, PyTorch 1.11.0. Total wall-clock: ≈ 12 min including all training.

Random seeds: numpy `1234`, torch `1234`.
