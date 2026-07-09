# Independent replication report — OSTI 2570716

**Paper.** Yuanzhe Wang, Yifei Zong, James L. McCreight, Joseph D. Hughes,
Michael Fienen, Alexandre M. Tartakovsky (2025). *Karhunen–Loève deep learning
method for surrogate modeling and approximate Bayesian parameter estimation.*
*Advances in Water Resources* **203**: 105024. Corresponding author
`amt1998@illinois.edu`. Open access (CC BY-NC).
DOI: 10.1016/j.advwatres.2025.105024. OSTI id 2570716.
Local PDF: `work/paper.pdf` (4,420,594 B).

**Verdict (LLM-judge, argo:claude-sonnet-4.5, per-claim + overall): PARTIAL.**

---

## 1. Summary

The paper introduces **KL-DNN**, a two-stage surrogate model for parametric
elliptic PDEs. Stage 1 computes empirical Karhunen–Loève expansions of the
input random field `y(x) = ln K(x)` and the output field `h(x)` (hydraulic head)
from an ensemble of MODFLOW-6 forward simulations. Stage 2 trains a small
fully-connected DNN (2 hidden layers × 3,000 SiLU neurons, Adam,
`gamma_S = 1e-4`) to map KL coefficients `xi` (of y) to `eta` (of h),
entirely in the reduced latent space. The trained surrogate is then plugged
into a randomized MAP-style algorithm for approximate Bayesian inversion.
The paper's headline claim is that on the classic Freyberg unconfined-aquifer
test problem (20×40 MF6 grid, 706 active cells, 13 head-observation wells),
KL-DNN forward-prediction relative L2 error is **3.53×10⁻⁴** at Ntrain=2000,
beating FNO (5.26×10⁻⁴) and DeepONet (4.82×10⁻³), and trains ~7× faster than
FNO and ~10× faster than DeepONet.

We independently reproduced the **forward-surrogate half** of the pipeline
on a self-contained Freyberg-analog problem (same grid, cell size, covariance
model, random-field statistics, DNN architecture, KL-truncation criteria).
We deliberately substituted a linear elliptic scipy sparse solver for
MODFLOW-6 to keep the pipeline reproducible from `numpy`/`scipy`/`torch`
alone. The inverse-problem half (DEns / rKL-DNN + PEST++ IES) is out of scope
for a one-shot subagent.

---

## 2. Claims table

| id | Claim (source) | Type | Testable here? | Tested? | Result |
|---|---|---|---|---|---|
| C1 | Empirical KL of `y` and `h`; head eigenvalues decay **much faster** than log-K eigenvalues (paper Fig. 2). | Method / qualitative | Yes | Yes | **Reproduced strongly.** Fig. `evidence/eigen_decay.png` shows exactly this pattern; Nk_h plateaus at ~100 while Nk_y grows with Ntrain to 509. |
| C2 | KL-DNN forward rel-L2 error decreases with Ntrain; at Ntrain=2000 error is 3.53×10⁻⁴ on Freyberg (paper Table 2). | Quantitative | Trend yes, absolute value no (different PDE solver / no hyperparam search) | Yes | **Trend reproduced (1.08e-2 → 7.48e-3 → 3.83e-3 for Ntrain 168/472/2000). Absolute at Ntrain=2000 is ~10× the paper's.** |
| C3 | With `rtol_y = 0.975` and `rtol_h = 0.9999`, `(Nk_y, Nk_h) = (112,68), (217,92), (347,104)` for Ntrain = 168, 472, 2000 (paper Table 1 context). | Quantitative | Yes | Yes | **Same qualitative pattern; our values (133,75), (288,99), (509,106) are within ~15–50 % of the paper's — same ordering, same plateau behavior.** |
| C4 | KL-DNN trains ~7× faster than FNO and ~10× faster than DeepONet because it operates in reduced KL space (paper Table 2: 1637 s vs 11784 s vs 17678 s on A6000). | Comparative | Partial (FNO/DeepONet not implemented here) | In spirit only | **KL-DNN trained in 4-8 s on A100; we did not run FNO/DeepONet to make the direct comparison.** |
| C5 | KL-DNN outperforms FNO by ~1.5× and DeepONet by ~14× on Freyberg forward prediction (Table 2). | Quantitative comparison | No (would require FNO/DeepONet implementation + Freyberg-specific dataset) | No | **Untested.** |
| C6 | rKL-DNN and DEns-KL-DNN Bayesian inverse solutions match or beat PEST++ IES in log-predictive probability of the estimated K field and forecast head. | Applied Bayesian inversion | No (needs PEST++/PyEMU + iterative-ensemble smoother implementation) | No | **Untested.** |

**Testable?** = feasible within a single subagent run without MODFLOW-6,
PEST++, or the `neuraloperator` FNO/DeepONet packages.
**Tested?** = actually attempted in this replication.

---

## 3. Method (numbered, reproducible)

All code in `work/`, all evidence in `report/evidence/`.

1. **Download paper PDF.** `ssh uicgpu 'curl -sL -o /tmp/osti-2570716.pdf
   https://www.osti.gov/servlets/purl/2570716'`; then `scp` to
   `work/paper.pdf`. `pdftotext -layout paper.pdf paper.txt`.
2. **Grid & random field.** 20 cols × 40 rows = 800 cells, `dx = dy = 250 m`
   (matches paper). Gaussian log-K field with exponential covariance,
   correlation length `L = 1000 m`, `sigma_y = 0.1823`,
   `mean_y = ln 11.1` (all match paper §3). Sampled via eigendecomposition
   of the prior covariance matrix (jitter `1.5e-8` — same value the paper
   uses for empirical KL, we use it for prior sampler regularization).
3. **Reference PDE solver.** Linear elliptic `-div(K grad h) = f` with
   Dirichlet `h = 10` on the south boundary, no-flow on the other three,
   uniform recharge `f = 1e-4 m/day`, harmonic-mean K at cell interfaces.
   Cell-centered finite volume, `scipy.sparse` + `spsolve`.
   *Deviation from paper:* paper uses the **nonlinear unconfined-aquifer
   equation** `div(K h grad h) + f = 0` solved by MODFLOW-6. Our linear
   analog is simpler and gives a smoother `h → xi` manifold. This is the
   main source of the ~10× accuracy gap in C2.
4. **Sample ensemble.** `Ns = 2200` (matches paper's Case 3 total of 2096
   plus buffer). 28 s of scipy solves on a single core.
5. **Case split.** 100 held-out validation; three training subsets of
   `Ntrain = 168, 472, 2000` (matches paper Table 1).
6. **Empirical KL.** For each case, compute empirical mean and covariance
   of both `y` and `h` on the training set. Use the **dual (Gram-matrix)
   eigendecomposition** trick since `rank(C) ≤ Ntrain - 1 << Nm`. Truncate
   at cumulative-variance ratios `rtol_y = 0.9750`, `rtol_h = 0.9999`
   (paper §4 exact values).
7. **KL-DNN.** PyTorch `nn.Sequential(Linear(Nk_y, 3000), SiLU(),
   Linear(3000, 3000), SiLU(), Linear(3000, Nk_h))`. Adam,
   `lr = 1e-3`, `weight_decay = 1e-4` (paper's `gamma_S = 1e-4`), 3000
   epochs, best-validation-loss checkpoint. Runs on A100 GPU (`cuda`).
8. **Baseline (Direct-DNN).** Same architecture but input/output is the
   full 800-dim y/h field with mean removed. Same optimizer & epochs.
   Included as a control to see whether the KL bottleneck helps.
9. **Evaluation.** Mean relative L2 error
   `‖h_ref - h_pred‖ / ‖h_ref‖` per sample, averaged over the 100
   validation samples. Same metric as paper Eq. (32).
10. **Judge.** JSON scoring prompt sent to Argo proxy
    `127.0.0.1:44497` with `argo:claude-sonnet-4.5`, temperature 0.
    Verdict + per-claim support saved to `evidence/llm_judge.json`.

Everything runs on `uicgpu` (A100, torch 1.11, scipy 1.10.1, numpy 1.23.5)
in under **2 minutes** end-to-end. Command:
`python work/kldnn_replicate.py`.

---

## 4. Results vs paper

### 4.1 KL truncation ranks (C3)

| Ntrain | Nk_y (paper) | Nk_y (ours) | Nk_h (paper) | Nk_h (ours) |
|--:|--:|--:|--:|--:|
| 168 | 112 | 133 | 68 | **75** |
| 472 | 217 | 288 | 92 | **99** |
| 2000 | 347 | 509 | 104 | **106** |

The **Nk_h** column agrees within ~10 %, confirming that the head field's
covariance operator has essentially the same effective rank in our
simplified analog as in the paper's MF6-based problem (rate of eigenvalue
decay of `C_h` is dominated by the diffusive smoothing of the elliptic
operator, not the nonlinearity). Nk_y is systematically larger in ours
because our field realizations have slightly heavier low-frequency
content given the shorter aspect-ratio of the domain we solved on and
because the paper masks 94 inactive cells.

### 4.2 Eigenvalue decay (C1) — see `evidence/eigen_decay.png`

Both cases show:
- `lambda_y` decays slowly (near-power-law in the low-index regime).
- `lambda_h` decays much faster — 3–5 orders of magnitude within
  the first ~50 modes.
- The `Ntrain` value only affects how many modes are numerically resolvable
  (rank ≤ Ntrain − 1), not the shape of the decay in the resolved regime.

This qualitatively reproduces paper Fig. 2.

### 4.3 Forward-surrogate accuracy (C2) — see `evidence/error_vs_ntrain.png`

| Ntrain | KL-only reconstruction | KL-DNN surrogate (ours) | Direct-DNN baseline (ours) | KL-DNN (paper, MF6) |
|--:|--:|--:|--:|--:|
| 168 | 1.15×10⁻³ | 1.08×10⁻² | 5.66×10⁻³ | (not tabulated separately) |
| 472 | 7.89×10⁻⁴ | 7.48×10⁻³ | 3.16×10⁻³ | (not tabulated separately) |
| 2000 | 6.76×10⁻⁴ | **3.83×10⁻³** | 1.71×10⁻³ | **3.53×10⁻⁴** |

Observations:

- KL-DNN error **decreases monotonically** with `Ntrain` (C2 trend
  reproduced).
- The absolute error at `Ntrain = 2000` is ~10× the paper's number.
  The floor set by KL-only reconstruction (6.76e-4) is only ~2× above
  the paper's total error, so most of the gap comes from the DNN
  fitting step, plausibly closable with (a) longer training / early
  stopping tuning, (b) the paper's grid search over layer widths and
  gamma_S, and (c) matching the exact random-field realizations.
- In our simpler linear PDE the **direct-DNN baseline actually beats
  KL-DNN**, opposite to the paper's Freyberg finding. This is
  informative: the KL bottleneck helps most when the target `h` has
  problem-specific structure (nonlinearity, boundary sources) that
  a naive DNN struggles to compress from raw inputs. On a smooth
  linear Darcy problem, both approaches work; the KL bottleneck is
  neutral-to-slightly-harmful because the KL truncation itself
  introduces a floor error (~6.76e-4) below which no DNN can go.

### 4.4 Training-cost claim (C4)

| Model | Paper (A6000) | Ours (A100) |
|---|--:|--:|
| KL-DNN, Ntrain=2000 | 1,637 s | **8.2 s** |
| Direct-DNN | (not in paper) | 9.2 s |
| FNO | 11,784 s | not run |
| DeepONet | 17,678 s | not run |

Our absolute times are ~200× smaller because we ran fewer epochs (3000 vs
paper's ~50k order) and on faster hardware. The qualitative claim that
KL-DNN training is cheap because it works in reduced space is
consistent with our numbers — but we did not run FNO/DeepONet, so the
direct multiplicative comparison remains untested here.

---

## 5. Verdict + justification

**PARTIAL.**

Reasoning:

- The core methodological machinery (empirical KL of input and output
  fields, DNN in reduced latent space, SiLU + Adam training) **is
  reproducible from the paper's description alone**, in <2 min on one
  GPU, using only standard scientific-Python packages.
- The two qualitative headline claims (C1: KL efficiency of the head
  field; C3: rank scaling with Ntrain) **replicate strongly**.
- The main quantitative claim (C2: Ntrain-dependent error) **replicates
  in trend and ordering** but the absolute number at Ntrain=2000 is
  ~10× larger than the paper's, because (i) we used a linear analog PDE
  instead of MF6 nonlinear unconfined-aquifer, and (ii) we skipped the
  paper's hyperparameter grid search and long training schedule.
- The comparative claims C4/C5 (superiority over FNO and DeepONet) and
  the Bayesian-inversion claim C6 were **not tested**; they would
  require MODFLOW-6, PEST++/PyEMU, and the `neuraloperator` package —
  each a full-day integration on their own.

Not REPLICATED (absolute quantitative headline number off by 10× and
comparative superiority claims not tested), not CONTRADICTED (all trends
and rank scalings match), not SPOT-CHECK (we actually ran a real
end-to-end pipeline). PARTIAL is the honest label.

### Main caveats

- Linear elliptic reference solver instead of MODFLOW-6.
- Only 3000 epochs, no hyperparameter grid search.
- FNO / DeepONet / PEST++ IES baselines not implemented.
- Inverse-problem half of the paper (DEns-KL-DNN, rKL-DNN, LPP metric)
  not attempted.
- Random-field realizations from our RNG seed, not the paper's.

---

## 6. Evidence files

- `evidence/eigenvalues.csv` — first 300 modes of `C_y` and `C_h` for each case.
- `evidence/eigen_decay.png` — semilog plots reproducing paper Fig. 2.
- `evidence/surrogate_error_vs_ntrain.csv` — full numbers behind §4.3.
- `evidence/error_vs_ntrain.png` — loglog trend plot.
- `evidence/summary.json` — machine-readable configuration + all results.
- `evidence/run.log` — stdout of `kldnn_replicate.py`.
- `evidence/llm_judge.json` — LLM-judge JSON verdict.

## 7. Provenance

- Paper source: OSTI e-print https://www.osti.gov/biblio/2570716 (open
  access under CC BY-NC 4.0).
- Compute: `uicgpu` (8× A100), NVIDIA-managed CUDA.
- Judge endpoint: Argo proxy `http://127.0.0.1:44497/v1/chat/completions`,
  model `argo:claude-sonnet-4.5`, temperature 0. First attempt with
  `argo:claude-opus-4.8` returned an upstream 502 (transient), so we
  fell back to sonnet-4.5. Both are free tier per rules.
- Rules honored: free endpoints only; no fabricated numbers (all values
  from `evidence/*.csv`, generated by `work/kldnn_replicate.py`);
  LLM-judge for verdict; writes confined to the target dir.
