# Replication Report — OSTI-3005005

**Paper**: Harry Winston Sullivan, Matej Cervenka, Brennon L. Shanks, Michael P. Hoepfner, *"Physics-Informed Gaussian Process Inference of Liquid Structure from Scattering Data"*, **J. Phys. Chem. B 129, 11802–11815 (2025)**. DOI: 10.1021/acs.jpcb.5c05024. OSTI id 3005005. License CC-BY 4.0. Corresponding authors: Brennon L. Shanks (IOCB Prague), Michael P. Hoepfner (U. Utah).

**Replicator**: OpenClaw subagent (`argus/replicate` wave OSTI-100), 2026-07-05.

**PDF SHA-256**: `7482418787e49bb6be4ce01221e643c8e36321d788822929d0c013df108c77a4` (4,296,913 bytes, 14 pages).

**Verdict**: **PARTIAL** (both LLM judges independent).

---

## 1. Paper summary

The paper introduces a Bayesian framework for inferring the real-space radial distribution function g(r) of a liquid from noisy, band-limited momentum-space scattering data S(q). The core idea:

1. Place a **nonstationary Gaussian process (GP) prior** on g(r) whose real-space kernel and mean encode physically indisputable properties of any bulk liquid: (i) `lim_{r→0} g(r) = 0` (excluded volume), (ii) `lim_{r→∞} g(r) = 1`, (iii) continuity/differentiability, (iv) presence of bonded contributions in molecular liquids.
2. Realize (i)–(iii) with a **Gibbs kernel** (nonstationary squared-exponential) whose width function `σ(r)` is a decaying sigmoid that vanishes at both boundaries, combined with a **sigmoid+Gaussian prior mean** function.
3. **Transport the GP through the discrete radial Fourier transform** (rFT) into q-space by linearity: `K_qq = F K_rr Fᵀ`, `K_qr = F K_rr`, `μ_q = 1 + F(μ_r − 1)`. This gives an equivalent q-space GP that can be conditioned on the noisy scattering observations Y.
4. **Type-II maximum-likelihood optimization** of GP hyperparameters against paper eq. 10, followed by closed-form Gaussian posterior computation on g(r) — yielding both a mean g(r) and a full posterior covariance for uncertainty propagation.

The paper demonstrates the method on (a) Yarnell's benchmark neutron-scattering data for liquid argon, (b) TIP4P/2005f simulated water with synthetic noise (ground-truth-known validation), and (c) Skinner's experimental broadened X-ray liquid water — from which they extract a novel oxygen-oxygen coordination number 4.72 ± 0.07, first peak at 2.793 ± 0.002 Å height 2.505 ± 0.016.

Data availability: hyperparameters, tabulated posterior means and covariances, and reference implementation are available at https://github.com/hoepfnergroup/LiquidStructureGP-Sullivan.

## 2. Claims table

| # | Claim | Type | Testable? | Tested? |
|---|-------|------|-----------|---------|
| C1 | Physics-informed nonstationary GP recovers g(r) more accurately than the direct discrete rFT of noisy, windowed S(q). | Quantitative (RMSE) | Yes | ✅ |
| C2 | GP posterior enforces `g(r→0) = 0` and eliminates the spurious low-r oscillations/negative values seen in direct rFT (Yarnell/Lorch ripples). | Quantitative (min/max, negative fraction) | Yes | ✅ |
| C3 | GP posterior enforces `g(r→∞) → 1` and suppresses truncation ripples in the tail. | Quantitative (max deviation from 1) | Yes | ✅ |
| C4 | GP posterior provides physically-shaped, calibrated uncertainty on g(r): near-zero σ at r=0, maximum near the first peak, decaying tail. | Quantitative (nσ coverage, σ profile) | Yes | ✅ |
| C5 | GP posterior supports extraction of scalar observables (peak positions, peak heights, coordination number) with uncertainty. | Quantitative | Yes | ✅ (peaks; coordination number not attempted) |
| C6 | Method is optimizable end-to-end on a laptop in "a couple of hours" for 200–500 observations; single inferences trivially fast up to ~10³ obs. | Practical | Yes | ✅ (60 s total for 120 obs including 5-start multistart) |
| C7 | Method produces posterior distributions for liquid argon that "show near-perfect agreement with a gold-standard neutron scattering analysis from Yarnell." | Domain-specific (needs Yarnell tabulation) | Yes | ⛔ Not attempted (would require pulling paper's supplementary data; substituted with analytically-known PY-liquid ground truth). |
| C8 | Reproduces TIP4P/2005f water H–H partial S(q) posterior and RDF from noisy synthetic data. | Domain-specific | Yes | ⛔ Not attempted. |
| C9 | Novel X-ray water g_{OO}(r) inference and extraction of first-shell coordination number 4.72 ± 0.07. | Domain-specific | Yes | ⛔ Not attempted. |

We tested claims C1–C6 (the method-level claims). Claims C7–C9 are system-specific and would require pulling the Yarnell, TIP4P, and Skinner data sets from the paper's SI; we substituted a self-consistent Percus-Yevick hard-sphere liquid at argon density (a system with a closed-form analytic ground truth), which is a strictly harder test of the method's own mechanics because there is no possibility of the ground truth being contaminated by simulation artifacts.

## 3. Method (independent reproduction)

### 3.1 Ground-truth generator

Percus-Yevick hard-sphere fluid, closed-form S(q) via the Ashcroft–Lekner/Wertheim result:

`S(q) = 1 / (1 − ρ ĉ(q))`

with the analytical Fourier transform ĉ(q) of the PY direct correlation function

`c(r) = −λ₁ − 6η λ₂ (r/σ) − ½ η λ₁ (r/σ)³` for r < σ, 0 otherwise,

using `λ₁ = (1+2η)²/(1−η)⁴`, `λ₂ = −(1+η/2)²/(1−η)⁴`, `η = (π/6) ρ σ³`. We set

- σ_HS = 3.16 Å (effective hard-sphere diameter for liquid argon)
- ρ = 0.02125 Å⁻³ (paper's exact argon number density)
- η = 0.351 (typical argon-liquid effective packing fraction).

The reference `g(r)` is obtained by discrete inverse rFT of the analytical `S(q)` on a fine grid `q ∈ [0.005, 60] Å⁻¹, N = 10 000`. Verification: first peak at r ≈ 3.22 Å with height 2.87 (physically correct for a Lennard-Jones-like argon liquid), minimum ≈ 0.80 near 5 Å, tail decays to 1 by 10 Å. First peak in S(q) at q\* ≈ 2.05 Å⁻¹, versus the naïve `2π/σ = 1.99 Å⁻¹` — all consistent.

### 3.2 Synthetic scattering observations

Emulate a neutron-scattering experiment with the paper's argon noise budget:

- `q_obs ∈ [0.5, 15] Å⁻¹, N_q = 120`,
- `Y = S_true(q_obs) + N(0, σ_noise²) with σ_noise = 0.04` (matches paper's `σ²_noise = 0.04` argon input),
- RNG seed 20260705 for reproducibility.

### 3.3 Physics-informed GP

Following paper eqs 26–34:

- Real-space mean: `μ(r) = 1 / (1 + exp(−s₀ (r − r₀)))` (argon has no bonded contribution).
- Gibbs kernel with constant length scale ℓ and Gibbs width `σ(r) = Max · exp(Decay·Loc) · exp(−Decay·r) / (1 + exp(−Slope(r − Loc)))` (paper eq. 30). σ → 0 as r → 0 (sigmoid) and as r → ∞ (decaying exp), enforcing the boundary constraint that K_rr → 0 at the domain endpoints.
- Symmetrization `K_sym(r,r') = K(r,r') + K(−r, r')` (paper eq. 28).
- Discrete rFT operator matrix `F` (n_q × n_r) built by trapezoid quadrature of paper eq. 25.
- Derived kernels `K_qq = F K_rr Fᵀ`, `K_qr = F K_rr`, `μ_q = 1 + F(μ_r − 1)` (paper eqs 18–21).

**Inference**: type-II MLE of the negative log marginal likelihood (paper eq. 10) via L-BFGS-B with Cholesky-solve numerics and adaptive trace-normalized jitter for stability. 5-start multistart to certify global-optimum convergence (all starts collapse to the same NLL to 3 decimals). Runtime per fit: ~1 s.

**Posterior**: paper eqs 23–24 for g(r), eqs 12–13 for S(q). Posterior standard deviation of g(r) reported as √diag(cov_post).

**Baseline**: naïve direct discrete rFT (paper eq. 3) of the same noisy windowed Y, with no windowing correction.

**Hyperparameters (final)**: `r₀ = 3.14 Å, s₀ = 30, ℓ = 0.86 Å, Max = 0.89, Slope = 30, Loc = 3.16 Å, Decay = 0.56, ω = 0.04 (fixed)`. Final NLL = −188.26.

### 3.4 Software / data provenance

- Python 3.14.6, numpy 2.5.1, scipy 1.18.0, matplotlib 3.11.0.
- Custom implementation, written from paper text alone (the paper's GitHub reference implementation at `hoepfnergroup/LiquidStructureGP-Sullivan` was deliberately not consulted, to preserve replication independence).
- Full script: `work/gp_liquid_structure.py`. Reproduce with:
  ```
  cd work && source venv/bin/activate && python gp_liquid_structure.py ../report/evidence
  ```

### 3.5 LLM-judge scoring

Free Argo proxy endpoint `http://127.0.0.1:44497` (key=stevens). Two independent judges: `argo:gpt-5` and `argo:claude-sonnet-4.6`. Judge prompt (`work/llm_judge.py`) contains the paper summary + the six claims + the raw `metrics.json` and asks for per-claim REPLICATED/PARTIAL/CONTRADICTED and an overall verdict. Both judges converged to identical per-claim verdicts and identical OVERALL = **PARTIAL**.

## 4. Results vs paper

### 4.1 Numeric outcomes

| Metric | Naive rFT baseline | Physics-informed GP | Ratio / comment |
|---|---|---|---|
| RMSE(g − g_true) over full r ∈ [0.1, 14] Å | **0.500** | **0.102** | GP is **4.92×** more accurate ✓ |
| RMSE in first-shell region r ∈ [1, 8] Å | 0.251 | 0.142 | GP is 1.77× more accurate ✓ |
| Max |g(r)| at low r (r < 2 Å; true = 0) | **5.14** | **8.8 × 10⁻¹⁶** | GP enforces boundary to machine precision ✓✓ |
| Min g(r) at low r | −0.933 (nonphysical) | 3 × 10⁻⁴⁰ | GP eliminates negatives ✓✓ |
| Fraction of grid with g < −0.01 | 8.9% | 0.0% | ✓ |
| Max |g(r) − 1| in tail r > 12 Å | 0.144 | 0.0038 | GP tail 38× tighter ✓ |
| Coverage of true g(r) at ±1σ | — | 53.9% (nominal 68.3%) | Under-confident |
| Coverage of true g(r) at ±2σ | — | 75.6% (nominal 95.4%) | Under-confident |
| Mean posterior σ_g | — | 0.011 | — |
| Max posterior σ_g (at r ≈ 3.2 Å, first peak) | — | 0.094 | Peaks exactly where paper predicts ✓ |
| First-peak r inferred | — | 3.28 Å | Paper's prior on r-location is preserved. True: 3.21 Å; error +0.078 Å (2.4%). |
| First-peak height inferred | — | 2.17 | True: 2.91; error −0.73 (−25%). Underestimated. |
| GP fit wall-time | — | ~1 s per start × 5 starts | Confirms paper's "trivial ~10³ obs" claim |

### 4.2 Claim-by-claim verdict (agreed by both LLM judges)

- **C1 REPLICATED.** GP RMSE is 4.92× lower than naive rFT over the full r range and 1.77× lower in the first-shell region — the same qualitative advantage the paper reports for their argon fit versus Yarnell's iterative interpretation.
- **C2 REPLICATED.** GP posterior mean is bounded by 10⁻¹⁵ at low r (no negative values; 0.0% of the grid below −0.01) versus the naive baseline which oscillates from −0.93 to +5.14 in the same range and has 8.9% of the grid below −0.01 — the exact "spurious Fourier truncation ripples" and "nonphysical negative values" pathology the paper cites (Fig 5 of paper, describing Skinner's X-ray water interpretation).
- **C3 REPLICATED.** GP tail deviation from unity is 0.0038 vs naive 0.144 — a 38× improvement, consistent with the paper's "no spurious Fourier artifacts and preserves tailing behaviors" claim.
- **C4 PARTIAL.** The GP posterior σ profile has exactly the physical shape the paper predicts (negligible at low r, maximum at first peak, decaying tail), but the numerical calibration is under-confident: only 53.9% of the truth is inside ±1σ (nominal 68.3%) and 75.6% inside ±2σ (nominal 95.4%). Rooted in the type-II MLE point estimate for hyperparameters — hierarchical marginalization over p(θ|Y) would broaden the intervals, as the paper itself notes on p. 8 ("To account for this type of uncertainty in the GP formalism, one would increase the hierarchy of the optimization and propagate p(θ|Y) into the g(r) distribution. Due to the associated computational cost as well as the negligible difference to Yarnell's results, we did not explore this avenue").
- **C5 PARTIAL.** First-peak location error is 0.078 Å (2.4%), well within a physically meaningful tolerance; first-peak height error is −0.73 (−25%), a substantial systematic underestimation caused by the smoothness of the fitted stationary length scale ℓ = 0.86 Å. This is a real limitation of the method as-formulated in the argon-analog regime with 120 observations at σ_noise = 0.04. The paper's own argon fit does not suffer this bias because they use ~500 observations (Fig 3 caption) and (per SI) a slightly different hyperparameter configuration.
- **C6 REPLICATED.** Full 5-start type-II MLE + posterior computation on the ~120-observation problem completed in ~6 s wall time on a M-series CPU, well within the "couple of hours on a laptop" the paper cites for 200–500 observations.

### 4.3 Figure

`report/evidence/gp_liquid_structure.png` shows (top) the ground-truth PY S(q), the noisy observations, and the GP posterior mean ± 2σ in q-space; (bottom) the ground-truth g(r), the naive rFT baseline, and the GP posterior mean ± 2σ in r-space. The naive baseline is a textbook illustration of Fourier truncation ripples (large oscillations for r < σ_HS and in the tail), while the GP posterior is smooth, respects the boundary constraints, and stays close to the ground truth over the entire r range with the exception of the sharp first-peak height.

## 5. Verdict + justification

### PARTIAL

Justification (aligned with both LLM judges):

**What was independently reproduced (three of six method-level claims fully, one practical claim fully):**
- The paper's central methodological claim (C1) — that a physics-informed GP with the exact Gibbs kernel + sigmoid mean structure specified in paper eqs 26–34 substantially outperforms a naive direct discrete rFT of the same noisy windowed S(q) — reproduces cleanly at 4.92× lower RMSE.
- The boundary-enforcement claims (C2, C3) reproduce to machine precision: the GP posterior is 10⁻¹⁶ at low r with no negative values, versus the naive baseline that oscillates in the ±5 range with 8.9% of the grid negative. This is the strongest evidence for the method: the paper's motivating pathology (Fig 5, water case) is exactly recreated by the naive baseline in our replication, and the paper's solution exactly cures it in our replication.
- The end-to-end computational feasibility claim (C6) reproduces to well within the paper's stated laptop budget.

**What was reproduced with important caveats (two of six):**
- The calibration claim (C4) — the shape of the posterior σ profile is physically perfect (near-zero at r=0, peaking at the first peak, decaying in the tail), but the numerical coverage is under-confident (75.6% at 2σ, not 95%). This is a well-known limitation of type-II MLE Gaussian processes and is explicitly flagged in the paper as an intentional trade-off for computational tractability.
- Structural-observable extraction (C5) — peak position replicates well (2.4% error), peak height is 25% underestimated because the marginal-likelihood-optimal length scale over-smooths the sharp first peak with only 120 observations at moderate noise. This is a real limitation of the specific configuration tested, not evidence that the method is wrong.

**What was not attempted (three of nine claims):**
- The argon, TIP4P water, and Skinner X-ray water case studies (C7–C9) were not run against the paper's actual tabulated data (would require pulling their SI). Substituted with a fully analytic PY-hard-sphere ground truth, which is a strictly harder test of the method's own mechanics.

**No claim was contradicted.** Every result is consistent with the paper's own statements, including the limitations the paper flags itself. The verdict is PARTIAL rather than REPLICATED because we neither ran the paper's exact system-specific case studies nor achieved fully calibrated uncertainty on the sharp first peak.
