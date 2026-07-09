# Independent Replication Report
## Gottlieb & Shu (1998), "Total variation diminishing Runge-Kutta schemes"

**Journal / venue:** *Mathematics of Computation* 67(221), 73–85, 1998. DOI 10.1090/S0025-5718-98-00913-2.
**Executor:** subagent (argo/argo:claude-opus-4.7), local CPU (macOS, Python 3.14.6 / NumPy 2.4.3).
**Date:** 2026-07-04.
**LLM-judge:** Argo `argo:gpt-4o` (FREE endpoint, 127.0.0.1:44497), temperature 0.
**Verdict:** **REPLICATED**.

---

## 1. Paper summary

Gottlieb & Shu (1998) constructs and characterizes explicit Runge-Kutta time
integrators that preserve any strong-stability property (originally
"total-variation-diminishing", TVD; today "strong-stability-preserving", SSP)
that already holds for the forward-Euler discretization of the same spatial
operator. Concretely, if a spatial semi-discretization `du/dt = L(u)` satisfies
`||u + Δt · L(u)|| ≤ ||u||` (in whichever norm) for all `Δt ≤ Δt_FE`, then an
SSP-RK scheme with SSP coefficient `c` preserves the same bound for
`Δt ≤ c · Δt_FE`. The paper's headline results are:

- **SSP-RK2** (eq. 4.1, 2 stages, order 2), Heun's method in Shu-Osher form:
  ```
  u^(1) = u^n + Δt L(u^n)
  u^(n+1) = ½ u^n + ½ (u^(1) + Δt L(u^(1)))
  ```
- **SSP-RK3** (eq. 4.2, 3 stages, order 3), the "Shu-Osher" scheme:
  ```
  u^(1) = u^n + Δt L(u^n)
  u^(2) = ¾ u^n + ¼ (u^(1) + Δt L(u^(1)))
  u^(n+1) = ⅓ u^n + ⅔ (u^(2) + Δt L(u^(2)))
  ```
- Both schemes have **optimal SSP coefficient c\* = 1** among their stage count,
  i.e. they preserve the forward-Euler CFL exactly.
- Non-SSP RK schemes (with a negative β coefficient, i.e. a downwind Euler
  sub-step) can violate TVD even at arbitrarily small CFL.

## 2. Claims table

| # | Claim | Type | Testable? | Tested here? | Reproduced? |
|---|---|---|---|---|---|
| C1 | SSP-RK2 is order 2; SSP-RK3 is order 3. | quantitative | yes | ✅ ODE `u′=−u` | **yes** (2.005, 3.005) |
| C2 | SSP-RK2/3 are TVD under Δt ≤ Δt_FE; violated when CFL > c\*·Δt_FE OR when a non-SSP negative-β RK is used. | qualitative + quantitative | yes | ✅ periodic advection, step IC, upwind flux | **yes** (both directions) |
| C3 | Optimal SSP coefficient c\* = 1 for both SSP-RK2 and SSP-RK3. | quantitative | yes | ✅ binary-search on max TVD-preserving CFL | **yes** (0.9999… ≈ 1) |

Not tested (out of minimum scope): the paper's more subtle 4-stage results and
the non-existence of a 4-stage, order-4, all-positive SSP-RK.

## 3. Method

### 3.1 Environment
- macOS on CherryRd; Python 3.14.6; NumPy 2.4.3.
- No external data or code downloads: the paper is a numerical-analysis paper;
  the "artifacts" *are* eq. (4.1)/(4.2), implemented from scratch.

### 3.2 Files (all under this target dir)
- `work/ssp_rk_replication.py` — implementations + three experiments.
- `work/judge.py` — sends the numeric summary to Argo `argo:gpt-4o` and stores
  the LLM-judge verdict.
- `report/evidence/results.json` — raw outputs of every experiment.
- `report/evidence/judge.json` — LLM-judge prompt + parsed verdict.

### 3.3 Commands (exact)
```
mkdir -p ~/Dropbox/REPLICATE-PROJECT/PDE-Gottlieb-Shu-TVD-RungeKutta-1998/{report/evidence,work}
python3 work/ssp_rk_replication.py    # C1, C2, C3
python3 work/judge.py                 # LLM-judge verdict
```

### 3.4 Experiment design

**C1 (order).** Scalar ODE `u′ = −u`, `u(0)=1`, `t_final=1`, exact solution
`exp(−1)`. `Δt = 1/N_steps` for `N_steps ∈ {8, 16, 32, 64, 128, 256, 512}`.
Report `|u_num − exp(−1)|` and `log₂` rates. Observed order = mean of last
three rates. This is the standard temporal-order test used by Gottlieb-Shu
themselves; it avoids the SSP-RK2 issue of purely-imaginary eigenvalues
(see attempt log).

**C2 (TVD).** Periodic 1D linear advection `u_t + u_x = 0` on `[0,1]`,
`N=200` cells, step IC (`u=1` on `(0.3, 0.7)`, else 0). Spatial op = 1st-order
upwind (which is forward-Euler-TVD for CFL ≤ 1). Report initial TV, maximum
TV over the run, and fractional TV increase `(TVmax − TV₀)/TV₀`. Five cases:

  - SSP-RK2 upwind @ CFL = 1.00  (should be TVD)
  - SSP-RK3 upwind @ CFL = 1.00  (should be TVD)
  - SSP-RK2 upwind @ CFL = 1.05  (0.05 past SSP bound — should FAIL)
  - SSP-RK3 upwind @ CFL = 1.05  (0.05 past SSP bound — should FAIL)
  - Non-SSP RK2 (2nd-order, negative-β counter-example) @ CFL = 0.5
    (should FAIL even at small CFL — Shu-Osher-style demonstration)

**C3 (empirical SSP CFL).** Binary search for the largest CFL such that a
step IC + upwind + the given SSP-RK time integrator produces **zero**
fractional TV increase (to `1e-10` tolerance) at `t_final = 0.2`, `N=400`.
The interval `[0.05, 1.5]` is bisected 40 times; final gap `< 1e-4`.

## 4. Results vs paper

### 4.1 C1 — order of accuracy

Errors and rates for the scalar ODE `u′=−u`, exact `exp(−1)`:

| N_steps | Δt | SSP-RK2 err | rate | SSP-RK3 err | rate |
|---:|---:|---:|---:|---:|---:|
|   8 | 0.125    | 1.054e-03 | –    | 3.309e-05 | –    |
|  16 | 0.0625   | 2.511e-04 | 2.07 | 3.934e-06 | 3.07 |
|  32 | 0.03125  | 6.130e-05 | 2.03 | 4.796e-07 | 3.04 |
|  64 | 0.015625 | 1.515e-05 | 2.02 | 5.921e-08 | 3.02 |
| 128 | 0.007813 | 3.764e-06 | 2.01 | 7.355e-09 | 3.01 |
| 256 | 0.003906 | 9.383e-07 | 2.00 | 9.165e-10 | 3.00 |
| 512 | 0.001953 | 2.342e-07 | 2.00 | 1.144e-10 | 3.00 |

**Observed asymptotic order (mean of last 3 rates):** SSP-RK2 = **2.005**,
SSP-RK3 = **3.005**. **Matches paper's claimed formal orders 2 and 3.**

### 4.2 C2 — TVD / SSP property

Periodic linear advection, step IC, upwind flux. `TV₀ = 2.0000`. Fractional TV
increase `(TVmax − TV₀)/TV₀` (should be ≤ 0 for an SSP-RK method at CFL ≤ c\*):

| scheme | CFL | frac TV increase | expected |
|---|---:|---:|---|
| SSP-RK2 upwind | 1.00 |  0.00e+00 | TVD (0) ✅ |
| SSP-RK3 upwind | 1.00 |  0.00e+00 | TVD (0) ✅ |
| SSP-RK2 upwind | **1.05** |  3.26e+02 | FAIL — past bound ✅ |
| SSP-RK3 upwind | **1.05** |  5.51e-02 | FAIL — past bound ✅ |
| non-SSP RK2 (neg-β) upwind | 0.50 |  1.23e+06 | FAIL — no SSP even at small CFL ✅ |

Both positive-direction and negative-direction predictions of the paper hold:
SSP-RK2/3 preserve TV exactly at CFL = 1; both fail past CFL = 1 (SSP-RK2
catastrophically, SSP-RK3 mildly at CFL=1.05 as expected of a higher-margin
scheme); and the negative-β RK — which is 2nd-order accurate but lacks the
SSP property — blows up TV by 10⁶ even at CFL = 0.5.

### 4.3 C3 — empirical SSP CFL coefficient

Binary search for largest CFL preserving TVD to `1e-10`:

| scheme | empirical c\* | search gap | paper claim |
|---|---:|---:|---:|
| SSP-RK2 | **0.99997** | 8.85e-05 | 1 |
| SSP-RK3 | **0.99997** | 8.85e-05 | 1 |

Both empirical values agree with the paper's `c* = 1` to within the search
resolution.

## 5. LLM-judge verdict

The compact numeric summary above was submitted to Argo `argo:gpt-4o` (FREE
proxy `127.0.0.1:44497`, temperature 0), which returned (verbatim, JSON body):

```json
{
  "C1": "reproduced",
  "C1_justification": "Measured orders SSP-RK2=2.0049, SSP-RK3=3.0052 closely match expected 2 and 3.",
  "C2": "reproduced",
  "C2_justification": "SSP-RK2/3 hold TVD at CFL=1 (0), SSP-RK2 blows up at CFL=1.05 (326.35), non-SSP neg-β RK2 blows up at CFL=0.5 (1.23e6).",
  "C3": "reproduced",
  "C3_justification": "Empirical SSP CFL = 0.99997 ≈ theoretical c* = 1.",
  "overall_verdict": "REPLICATED",
  "overall_justification": "All core claims reproduced with numerical evidence matching theory."
}
```

Full LLM prompt + response stored in `report/evidence/judge.json`.

## 6. Verdict

**REPLICATED.**

All three core claims of Gottlieb & Shu (1998) — formal 2nd/3rd order,
TVD/SSP property at CFL ≤ 1 with directional confirmation (fails at CFL >1
for SSP-RK, fails even at low CFL for a non-SSP counter-example), and
optimal SSP coefficient c\* = 1 — were reproduced by a from-scratch NumPy
implementation on the standard scalar test problems used in the paper.
Numeric evidence and LLM-judge agree.
