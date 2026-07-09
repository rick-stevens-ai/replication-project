# OSTI 2907986 — Independent Replication Report

**Paper:** *A Resolution Independent Neural Operator* (RINO)
**Authors:** Bahador Bahmani, Somdatta Goswami, Ioannis G. Kevrekidis, Michael D. Shields (Johns Hopkins)
**Also indexed as:** arXiv:2407.13010 (v3, Dec 2024) — same title, same authors, later published in *Journal of Computational Physics* 539, 2025, art. 114233 (DOI 10.1016/j.jcp.2025.114233).
**Substitution note:** OSTI purl `https://www.osti.gov/servlets/purl/2907986` was **network-unreachable** from CherryRd during this replication (multiple TCP timeouts to `www.osti.gov:443`). We substituted the arXiv preprint of the *same paper* (identical title + author list); SHA-256 recorded.

- `paper.pdf` (arXiv 2407.13010 v3): 5,797,462 bytes, SHA-256 `10536cde4df22672c72e8bdf4710d6f0af51df99332f08662482b562a3fff360`
- Fetched: 2026-07-05 from `https://arxiv.org/pdf/2407.13010`.

**Replication scope (time-boxed ~18 min, free Argo Opus only, CPU / pure NumPy):** minimal SPOT-CHECK reproduction of RINO's *core qualitative claim* on **Example 1 (antiderivative operator)**. We do NOT reproduce absolute error numbers, GRF input distributions, dictionary-learning basis (SIREN/INR), or the more complex 1D-Darcy / Burgers / 2D-elasticity benchmarks.

---

## 1. Claims table

| # | Claim (paraphrased from paper) | Source in paper | Testable in a 15-min replication? |
|---|---|---|---|
| C1 | A **vanilla DeepONet** requires the input function to be **discretized at the same fixed sensor locations** at train and test time; changing the sensor grid degrades predictions. | Abstract; Sec. 1 ¶3; Sec. 2.1 (Eq. describing branch input); Fig. 1 (left column). | **Yes.** Train vanilla DeepONet at N=100, test at N ∈ {50, 75, 100, 125, 200, 400} with the only recourse being nearest-neighbor resampling back to N=100. |
| C2 | **RI-DeepONet / RINO** projects the arbitrarily-discretized input onto a small set of **continuous basis functions** (in the paper: INR/SIREN dictionaries learned by two proposed algorithms). The branch then eats a **fixed-dimensional coefficient vector**, decoupling the model from the sensor grid. | Sec. 2.1 (RI-DeepONet); Sec. 2.2 (dictionary learning); Fig. 1 (right column); Fig. 2 (RINO schematic). | **Partially.** We use a small **fixed Fourier basis** as a stand-in for the learned INR/SIREN dictionary (same mechanism, simpler basis). Branch input is a 16-dim coefficient vector computed on whatever sensor grid arrives. |
| C3 | The RI-DeepONet / RINO scheme is **essentially resolution-invariant** at inference: relative-L2 error is stable across different test discretizations (provided Nyquist-like sampling density is met). | Sec. 3 preamble; Sec. 3.1.1 Fig. 5-6 (Antiderivative Ex.); paper's "Rel. MSE: 1.514e-05 / 1.987e-03" numbers on antideriv with varying sensor counts per sample. | **Yes.** Compare rel-L2 vs test grid N for both models. |
| C4 | Vanilla DeepONet's absolute Rel. MSE ≈ 1.5e-3 on the antiderivative example is achievable when the sensor grid is consistent between train and test. | Sec. 3.1.1 Fig. 5 caption / Fig. 6 numeric annotations. | **Not directly** — we use a much smaller network (2-layer, width 64, output p=48) and fewer epochs; only the qualitative shape is testable in the time budget. |

## 2. Methods (replication)

**Operator:** 1D antiderivative $s(y) = \int_0^y u(x)\,dx$, $y \in [0,1]$ (Sec. 3.1.1 of paper).

**Input-function distribution:** sums of 6 low-frequency sinusoids (k·π·x, k=1..6) with random amplitudes ∝ 1/k and uniform random phases. Simpler than the paper's Gaussian-process-inspired functions but has similar smoothness/bandlimited character.

**Data:** 400 train / 200 test pairs. Reference antiderivative computed by trapezoid rule on a length-2001 grid, then interpolated to the target evaluation grid. Output evaluated at Y_N = 64 uniform points on [0,1].

**Architectures (both models — same size, same seed, same optimizer):**
- Branch net: 2-layer tanh MLP, width 64, output dim p = 48.
- Trunk net: 2-layer tanh MLP, width 64, output dim p = 48, input dim 1 (a single query location).
- Output: $\hat s_i(y_j) = b_i \cdot t_j + \text{bias}$.
- Optimizer: hand-written Adam, lr = 1e-3, batch = 32, **300 epochs** (~4 s / model on CPU).
- Loss: MSE.
- Implemented in **pure NumPy** with hand-written forward + backward (no torch, no jax) so it runs anywhere.

**Model A — Vanilla DeepONet:** branch input is the **raw 100-vector of sensor values** at the fixed training grid `x_base = linspace(0,1,100)`. At test time with a *different* grid, the only recourse is nearest-neighbor resampling back to length 100 (this is what a naive user gets without the RINO recipe).

**Model B — Basis DeepONet (RINO-style stand-in):** branch input is a fixed **N_BASIS = 16** vector of Fourier coefficients $c_k = \int_0^1 u(x)\,\varphi_k(x)\,dx$ computed by trapezoid rule on WHATEVER sensor grid arrives (basis: {1, √2 sin(kπx), √2 cos(kπx)} for k = 1..7 + one extra term). The Fourier basis stands in for the paper's learned INR/SIREN dictionary — same architectural idea (fixed-dim coefficient input, arbitrary sensor grid), simpler basis.

**Test protocol:** train both models once at N=100 sensors, then evaluate zero-shot at test grid sizes N ∈ {50, 75, 100, 125, 200, 400}. Report mean relative-L2 test error across 200 test functions per grid.

## 3. Reproduced numbers

Full run log: `work/rino_toy.log`. Full JSON: `work/results.json`. Wall time end-to-end: **~10 s** (data build + train both models + eval at 6 grids).

**Training loss (final epoch 300, MSE):**
- Vanilla DeepONet: 1.317e-3
- Basis-DeepONet: 9.076e-4 (both models converged; not a training-capacity issue)

**Test-time zero-shot rel-L2 error at each test grid:**

| test grid N | Model A: Vanilla rel-L2 | Model B: Basis rel-L2 | ratio A / B |
|---:|---:|---:|---:|
|  50 | **0.3290** (degraded) | 0.1571 | **2.09×** |
|  75 | 0.2798 | 0.1577 | 1.77× |
| 100 *(train grid)* | 0.2182 | 0.1580 | 1.38× |
| 125 | 0.2364 | 0.1581 | 1.50× |
| 200 | 0.2256 | 0.1582 | 1.43× |
| 400 | 0.2211 | 0.1583 | 1.40× |

**Summary metrics:**
- Vanilla at its native grid (N=100): 0.218; **off-grid mean**: 0.257; **off-grid worst (N=50)**: **0.329** — a **51% degradation** from the native-grid error.
- Basis: **0.157 flat** across all six test grids; off-grid mean 0.157; off-grid worst 0.158 — max-min variation **< 1%**.
- At every test grid the basis model matches or beats vanilla, and at the extreme undersampled grid it is more than **2× better**.

## 4. Agreement analysis

| Claim | Paper's assertion | Our observation | Verdict |
|---|---|---|---|
| **C1** Vanilla DeepONet is discretization-locked | Vanilla degrades when sensor grid differs from training | Vanilla rel-L2 swings from 0.218 (native) → 0.329 (undersampled to N=50), a **51% relative increase**. | ✅ **REPLICATED (qualitative)** |
| **C2** Fixed-dim basis-coefficient branch removes sensor-grid dependence | The trapezoid-rule Fourier-coefficient input is *by construction* invariant to sensor placement (once Nyquist is met). | Basis rel-L2 = 0.157–0.158 across N ∈ {50..400}, variation < 1%. | ✅ **REPLICATED (qualitative)** — with the caveat that our Fourier basis is a stand-in for the paper's learned INR/SIREN dictionary. |
| **C3** RI-DeepONet is essentially resolution-invariant at inference | Same as C2 in effect | Confirmed: 6 test grids covering a **factor-of-8 range** (50 → 400) yield <1% error variation for the basis model. | ✅ **REPLICATED (qualitative)** |
| **C4** Absolute Rel. MSE ≈ 1.5e-3 on antideriv. | Achievable with paper's full setup | Our basis model reaches training MSE 9e-4 but **test rel-L2 ≈ 0.16** (much worse than paper's ~0.04 that ~1.5e-3 rel-MSE implies) — expected: we use a tiny 2-layer NumPy net, 400 train fns, fewer than 5-10% of the paper's training compute. | ⚠️ **NOT tested** (out of time-budget scope). |

## 5. Threats to validity / limitations

1. **Fourier basis ≠ SIREN/INR dictionary.** The paper's key methodological contribution is *learned* continuous basis functions that adapt to the data. We replaced this with a fixed Fourier basis — same information-theoretic move, but strictly weaker on data with sharp features / non-periodic behavior. That said, Example 1 of the paper is antiderivative of smooth signals, so the Fourier basis is a fair proxy specifically for this benchmark.
2. **Input-function distribution simpler than paper.** We use bandlimited sinusoid sums instead of GP samples; this makes the Fourier basis look artificially good. This inflates the absolute performance of Model B but does **not** artificially inflate the *resolution-invariance* observation (that follows from trapezoid-rule integration on any sufficiently fine grid).
3. **Absolute error magnitudes are much larger than the paper's** because our nets are 2 orders of magnitude smaller and trained for ~4s each. This is by design (fits the ~18-min time budget on CPU without torch); it does not affect the qualitative claim about resolution-invariance.
4. **N=50 is right at / below Nyquist** for the k=6 mode (π·6·x on [0,1] needs at least 12 samples per period × few periods to be well-resolved). Basis errors would rise if we pushed N well below Nyquist; that would in fact match a caveat the paper explicitly makes ("these strategies of course require sufficient resolution to capture the characteristic length or time scales").
5. **We only tested Example 1 (antiderivative).** The paper's Examples 2-4 (1D nonlinear Darcy, 2D Burgers with spectral solver, elasticity) were out of the time-budget scope.
6. **Single seed.** No error bars across random inits — but the effect size (2× at N=50, flat vs 30% swing across grids) is large enough to be visually unambiguous.
7. **PDF substitution: arXiv, not OSTI-hosted PDF.** Verified same title, same authors, same abstract, same architecture description; not verified byte-for-byte identical to the OSTI-hosted copy.

## 6. Verdict

**SPOT-CHECK**

The paper's *core qualitative claim* — that a fixed-dim basis-coefficient branch input (RI-DeepONet / RINO) removes DeepONet's discretization-lock and yields resolution-invariant inference — **reproduces cleanly** in a stripped-down 2-layer pure-NumPy replication on the paper's Example 1 (antiderivative operator). Vanilla DeepONet rel-L2 swings 51% between its native grid (N=100) and the extreme-undersampled test grid (N=50); the basis-input model stays within <1% variation across a factor-of-8 grid-size range and beats vanilla at every grid tested (up to 2.09× at N=50).

We do **not** verify (a) the specific quantitative Rel. MSE ~ 1.5e-3 numbers, (b) the learned SIREN/INR dictionary being superior to a fixed Fourier basis, (c) generalization to the paper's harder examples (Darcy, Burgers, elasticity), or (d) the two proposed dictionary-learning algorithms in Sec. 2.2. Those would need a larger compute budget, torch/jax, and the paper's data-generation pipelines.

Everything tested in our budget agrees with the paper.

---

## 3-line summary

1. Vanilla DeepONet trained at N=100 sensors degrades ~51% at N=50 (rel-L2 0.218 → 0.329) and varies non-monotonically across N∈{50,75,125,200,400}, exactly the discretization-lock RINO calls out.
2. Substituting a fixed-Fourier basis-coefficient branch input (paper's mechanism, simpler basis) yields rel-L2 = 0.157±<0.001 across a factor-of-8 range of test grid sizes — a clean qualitative reproduction of resolution-invariance.
3. Verdict SPOT-CHECK: paper's core discretization-independence claim replicates on Example 1 (antiderivative); absolute error magnitudes and the harder Darcy/Burgers/elasticity benchmarks + learned SIREN dictionary are out of this replication's time budget.
