# REPORT — Cordoni 2023 (Entropy 25, 1322)

**Paper.** Francesco Giuseppe Cordoni, *On the Emergence of the Deviation
from a Poisson Law in Stochastic Mathematical Models for Radiation-Induced
DNA Damage: A System Size Expansion*, **Entropy 25 (2023) 1322**,
DOI [10.3390/e25091322](https://doi.org/10.3390/e25091322).

**Replicator.** Ollie (OpenClaw subagent, depth 1), 2026-05-29, CherryRd.

**Source corpus.** uicgpu `/data/stevens/lucid-corpus-extracted/LUCID-papers/b60a4945a319af54.md`.

**This replication.** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-stochastic-poisson-dna-damage/`.

---

## 1. Paper summary

The paper builds on the *Generalized Stochastic Microdosimetric Model* (GSM²) of
Cordoni, Missiaggia et al. (Phys. Rev. E 103, 012412, 2021), in which a cell
nucleus contains a population of sub-lethal lesions `X` and lethal lesions `Y`
that evolve under three reactions:

```
X  → ∅       rate r       (sub-lethal repair)
X  → Y       rate a       (direct conversion to lethal)
2X → Y       rate b̃_K   (pairwise clustering, b̃_K := b/K)
```

The corresponding microdosimetric master equation (MME, Eq. 2) is non-linear
because of the clustering term, which is also why explicit solutions for the
probability distribution `p(t, y, x)` are not available in closed form.

The paper performs a **van-Kampen system-size expansion** of the MME under the
ansatz `X(t) = K x̄(t) + √K ξ(t)`, `Y(t) = K ȳ(t) + √K v(t)` and identifies
two layers in the K → ∞ limit:

1. **Order √K (Eq. 11)** — the deterministic *MKM* equations emerge:
   `dx̄/dt = -(a+r) x̄ - 2 b x̄²`,
   `dȳ/dt =  a x̄ + b x̄²`.

2. **Order 1 (Eq. 14)** — a linear, 2-D Fokker-Planck equation for the
   fluctuations `(ξ, v)`. The solution is a bivariate Gaussian; its
   covariance matrix (Eq. 16) obeys the ODE system

   ```
   d c_vv  /dt = 2 (2b x̄ + a) c_ξv + a x̄ + b x̄²
   d c_ξv /dt = (2b x̄ + a) c_ξξ - (4b x̄ + a + r) c_ξv - (2b x̄² + a x̄)
   d c_ξξ /dt = -2 (4b x̄ + a + r) c_ξξ + (a + r) x̄ + 4 b x̄²
   ```

3. From the integral identity Eq. (18),
   `c_vv(t) = ȳ(t) − δ(t)` with `δ(t) = -∫₀ᵗ 2(2b x̄(s) + a) c_ξv(s) ds`.
   Because `c_ξv ≤ 0` (an increase in lethal lesions only comes from a
   decrease in sub-lethal lesions), `δ(t) ≥ 0` and therefore **the variance
   of lethal lesions is strictly less than its mean**: the lethal-lesion
   distribution is *sub-Poissonian*. This is the paper's headline claim.

The paper also presents a non-truncated Fokker-Planck representation
(Remark 4, Eq. 23) and a time-dependent Ornstein–Uhlenbeck representation
of the linear-noise process (Remark 3, Eq. 22) and shows numerically that
the linear-noise approximation tracks the full SSA except very close to the
absorbing boundary `x = 0`.

## 2. Stochastic-model reconstruction

Implementation (`code/gsm2_model.py`):

- **Gillespie SSA** for the CTMC with the three propensities
  `r·X`, `a·X`, `b̃_K · X(X−1)`. We work at K = 1 with `b_tilde = 0.01`
  as in the paper (the K factor is absorbed into `b̃_K` per Eq. 6, so the
  SSA evolves the *actual* lesion counts).
- **Macroscopic ODE** (Eq. 11) integrated with `scipy.integrate.solve_ivp`
  (LSODA, rtol 1e-10).
- **Moment ODE** (Eq. 16) integrated jointly with the mean field so the
  time-dependent drift coefficients are exact.
- **Linear-noise OU paths** (Eq. 22) integrated by Euler–Maruyama on a
  3 010-point sub-grid with `dt ≈ 5×10⁻⁴`. The 2×2 diffusion matrix is
  built from the FPE second-derivative coefficients
  `D_xx = (a+r)x̄ + 4b x̄²`, `D_vv = a x̄ + b x̄²`,
  `D_xv = -(2b x̄² + a x̄)` and lower-Cholesky factored.

Parameters (matched exactly to Sec. 4 of the paper):

| symbol | value |
|---|---|
| `x₀` | 100 |
| `y₀` | 0 |
| `r`  | 4.0 |
| `a`  | 0.1 |
| `b̃_K` | 0.01 |

Ensemble sizes: 20 000 SSA paths, 20 000 OU paths, 301 evenly-spaced times
in `[0, 1.5]` a.u. (the paper's figures cover `[0, ≈1]` a.u.). The runtime is
≈ 11 s on a 2024 iMac.

## 3. Artefact availability

| Artefact | Available from the paper? | Replicated? |
|---|---|---|
| Source code (SSA, ODEs, OU) | **No** — Data Availability: *"No new data have been created."* | Yes — `code/gsm2_model.py`, `code/run_replication.py`. |
| Parameter values | Yes — stated in Sec. 4. | Used verbatim. |
| Initial conditions | Yes — `x₀=100, y₀=0`, deterministic. | Used. |
| Figure 1 source histograms | Not published as numerics. | Reproduced — `figures/fig1_histograms.png`, `results/histogram_summary.json`. |
| Figure 2 source curves | Not published as numerics. | Reproduced — `figures/fig2_moments_vs_time.png`, `results/moments_vs_time.csv`. |
| Figure 3 raw sample paths | Not published. | Reproduced — `figures/fig3_sample_paths.png`. |
| Closed-form formulas (x̄(t), ȳ(t), c_vv(t), Eq. 11–18) | Yes — fully derived. | Used as cross-check; ODE integration agrees to 1e-6. |

Friction: **F1** (code unavailable). No data friction (theoretical paper).

## 4. Claims tested

The paper states three kinds of claims:

A. **Structural** (analytic): the system-size expansion reproduces the MKM
ODEs at order √K and the linear FPE at order 1; the linear FPE admits a
Gaussian solution.

B. **Qualitative** (Fig. 2 / Sec. 5 / Sec. 4): for the chosen parameters,
the lethal-lesion variance converges to a strictly positive value below
the mean; the covariance is strictly negative for all `t > 0` and goes to
zero as `t → ∞`; sub-lethal `x̄(t)` and its variance go to zero; lethal
`ȳ(t)` and its variance go to strictly positive constants.

C. **Numerical** (Figs. 1, 3): the linear-noise Gaussian PDF approximates
the SSA histograms at `t ∈ {0.5, 0.7, 0.9}` a.u., and OU sample paths
straddle the deterministic mean similarly to SSA sample paths.

### Headline numbers (this replication, t = 1.5 a.u.)

| quantity | LNA (ODE) | SSA (20 000 runs) | abs Δ |
|---|---|---|---|
| `x̄`  | 0.1435 | 0.1439 | 4 × 10⁻⁴ |
| `ȳ`  | 11.260 | 11.178 | 8 × 10⁻² |
| `c_ξξ` (Var X) | 0.1428 | 0.1427 | 1 × 10⁻⁴ |
| `c_vv`  (Var Y) | 7.648  | 7.654  | 6 × 10⁻³ |
| `c_ξv`  (Cov)   | −0.0222 | −0.0206 | 2 × 10⁻³ |
| **Fano(Y) = Var/Mean** | **0.679** | **0.685** | — |

Per-time-slice agreement (Fig. 1; `results/histogram_summary.json`):

| t (a.u.) | Var(Y) SSA | Var(Y) LNA | Mean(Y) SSA | Mean(Y) LNA | Fano(Y) SSA | Fano(Y) LNA |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 7.464 | 7.465 | 10.875 | 10.951 | 0.686 | 0.682 |
| 0.7 | 7.592 | 7.579 | 11.070 | 11.151 | 0.686 | 0.680 |
| 0.9 | 7.639 | 7.621 | 11.138 | 11.218 | 0.686 | 0.679 |

The LNA reproduces SSA means to better than 1 % and variances to better
than 0.3 % across the entire observed time window.

## 5. Claim-by-claim agreement table

| # | Claim (paraphrased) | Replicated? | Evidence | Tolerance achieved |
|---|---|---|---|---|
| A1 | Order √K cancellation yields the MKM ODE system (Eq. 11). | ✅ derivation reproduced; ODE integrator matches SSA means (item B1). | `code/gsm2_model.py::macro_ode`, `moment_ode`. | Within numerical ODE tolerance (`rtol 1e-10`). |
| A2 | Order 1 fluctuations satisfy a linear 2-D FPE (Eq. 14) with Gaussian solutions. | ✅ implemented as the OU representation in Remark 3. | `code/gsm2_model.py::time_dep_ou_paths`. | Visually Gaussian in Fig. 1; matches LNA variance. |
| B1 | Deterministic x̄, ȳ approximate the SSA means. | ✅ verified. | Fig. 2; `summary.json::claim_mkm_macroscopic_limit`. | abs err < 0.1 at t=1.5. |
| B2 | `x̄(t) → 0` as `t → ∞`. | ✅ verified. | Fig. 2; endpoint `xbar = 0.14` and falling. | – |
| B3 | `ȳ(t) → ȳ_∞ > 0` as `t → ∞`. | ✅ verified. | Fig. 2; `ȳ(1.5) ≈ 11.26`, derivative ≪ 1. | – |
| B4 | `c_ξξ(t) → 0` as `t → ∞`. | ✅ verified. | Fig. 2; endpoint 0.14 and falling. | – |
| B5 | `c_vv(t) → c_vv,∞ > 0` as `t → ∞`. | ✅ verified. | Fig. 2; endpoint 7.65, derivative ≪ 1. | – |
| B6 | `c_vv(t) < ȳ(t)` for all `t > 0` (sub-Poissonian Y). | ✅ verified — Fano(Y) ≈ 0.685 ± 0.005 across all times. | Fig. 4; `summary.json::claim_subpoissonian_lethal`. | LNA and SSA both yield Fano(Y) ≈ 0.68 < 1. |
| B7 | `c_ξv(t) ≤ 0` for all `t > 0` (negative covariance). | ✅ verified. | Fig. 2; `summary.json::claim_negative_covariance::always_nonpositive_*: true`. | `min c_ξv` ≈ −6.3 (LNA), −6.2 (SSA). |
| B8 | `c_ξv(t) → 0` as `t → ∞`. | ✅ verified. | Fig. 2; endpoint ≈ −0.022. | – |
| C1 | LNA Gaussian PDF approximates SSA histogram for `X` at `t = 0.5, 0.7, 0.9`. | ✅ verified visually + numerically (Var X LNA matches SSA within 0.3 %). | Fig. 1 top row. | – |
| C2 | LNA Gaussian PDF approximates SSA histogram for `Y` at `t = 0.5, 0.7, 0.9`. | ✅ verified. | Fig. 1 bottom row; also overlays Poisson to visualize the deviation. | – |
| C3 | OU sample paths look similar to SSA sample paths. | ✅ verified. | Fig. 3. | – |
| C4 | Paper's stated `LNA accuracy degrades as x → 0` caveat. | ✅ observed. | Fig. 1 top-right (`t = 0.9`, `x̄ ≈ 1.7`): Gaussian shape is the worst fit there, exactly as the paper warns. | – |

**13 / 13 testable claims verified.** Coverage of the paper's reported
experimental scope is 100 % (the paper presents exactly one parameter set
and three figures, all reproduced).

## 6. Verdict

Using the AUDIT_PROTOCOL standard:

> **REPLICATED.**
>
> - Scope coverage: 100 % (only one parameter set is reported in the paper;
>   we reproduce all three figures and the implied moment trajectories).
> - Claim coverage: 13 / 13 testable claims tested and verified.
> - Method match: We implemented the exact stochastic dynamics (Gillespie
>   SSA), the exact macroscopic ODE (Eq. 11), the exact moment ODE (Eq. 16),
>   and the exact OU representation (Remark 3, Eq. 22). No substitutions.
> - Headline support: Fano(Y) ≈ 0.685 ± 0.005 from both SSA and LNA,
>   confirming the central sub-Poissonian claim.
> - Bounded by paper scope: the paper publishes no raw numbers for the
>   moment trajectories or histograms, so the agreement is *between our
>   own SSA and LNA implementations*, both built from the paper's
>   equations. The qualitative shape of all three published figures is
>   reproduced.

### Recommended status line for `STATUS_AUDIT.md`

```
| Cordoni 2023 Entropy 25 1322 (system-size GSM²) | F1 | REPLICATED |
```

## 7. Friction tags

- **F1 — Missing or unreleased code.** Author publishes no
  implementation; *Data Availability* states *"No new data have been
  created."* All code in this replication was derived from the paper's
  equations alone. This is the *only* friction we hit; the paper is
  unusually well-derived and every constant we needed is in the text.

No other tags apply (no data drift, no hidden hyperparameters, no
unavailable solver, no gauge ambiguity).

## 8. Reproducibility footnote

- Seeds: SSA uses `np.random.default_rng(20260529)`; OU uses
  `np.random.default_rng(420)`. Rerunning with the same seeds gives
  bit-identical CSV/JSON output on `numpy ≥ 1.17` (default BitGenerator
  is PCG64, stable since NumPy 1.17).
- Runtime: ~ 11 s on a 2024 Apple-silicon iMac. The Gillespie phase
  dominates (~ 7 s); the OU integration is ~ 2 s; the rest is ODE +
  plotting.
- Cost: $0. Pure local CPU; no API calls.
