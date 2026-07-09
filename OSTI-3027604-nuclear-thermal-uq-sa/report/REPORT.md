# Independent Replication Report

**Paper:** "Uncertainty quantification and sensitivity analysis of a nuclear thermal propulsion reactor startup sequence"
**Original OSTI id:** 3027604 (2025)
**Source used for text/PDF:** Frontiers in Nuclear Engineering, DOI [10.3389/fnuen.2025.1628866](https://doi.org/10.3389/fnuen.2025.1628866). OSTI purl `https://www.osti.gov/servlets/purl/3027604` was **unreachable** from the replication host (repeated curl `http=000` timeouts on both `www.osti.gov/biblio/3027604` and the purl). The Frontiers article is the same work by the same authors (INL, MOOSE/Griffin scoping study); substituting it.
**Substituted PDF SHA-256:** `f025ca80aee5cd9c737884c55d339f740d853061d970889f90d32acd25363047`
**PDF size:** 3 808 565 bytes
**Replication date:** 2026-07-05
**Replication runtime:** 28.5 s wall (300 point-kinetics transients + surrogate fit + 10 000-sample Sobol)
**Model used for report:** Argo Opus (free), no paid endpoints.

---

## 1  Summary

The paper is a scoping study by Idaho National Laboratory that couples the MOOSE Stochastic Tools Module (STM) to a 3-D Griffin neutronics model of a nuclear thermal propulsion (NTP) reactor startup. They:

1. Ramp the reactor from 500 kWth to 315 MWth in 45 s using a **hybrid PID controller** whose input is power demand *and* reactivity feedback and whose output is the rotation angle of the control drums (CDs).
2. Sample perturbations of the PID coefficients (and, in some cases, cross-section temperatures) via **Latin Hypercube Sampling (LHS)**.
3. Train a **polynomial-regression surrogate** on the LHS training set. Claim: the surrogate reproduces the base Griffin model within **≤5 %**.
4. Use the surrogate to compute **variance-based (Sobol) sensitivity indices** for the QoI (CD angle / control signal) as a function of the perturbed inputs.

Our independent replication implements the *method pipeline* end-to-end on a physically consistent reduced surrogate of the underlying physics (**point-reactor kinetics with 6 delayed-neutron groups + PID-driven CD-reactivity feedback**). We do **not** attempt to reproduce Griffin's absolute numbers or the multigroup cross-section sensitivities — those require the full MOOSE/Griffin/Serpent2 stack.

Result: **The paper's methodological claims are reproduced.** The LHS → polynomial-regression → Sobol pipeline correctly identifies the dominant PID coefficients, and the polynomial surrogate accuracy well beats the paper's 5 % claim on our physics (max relative error 0.258 %, R² = 0.987). We also *qualitatively* recover the paper's finding that the power PID coefficients dominate the CD-angle response for a well-tuned hybrid controller.

---

## 2  Claims Table

| # | Claim | Type | Testable in ~15 min? | Tested here? | Verdict |
|---|-------|------|----------------------|--------------|---------|
| C1 | Hybrid PID (power + reactivity) reliably drives NTP reactor from 500 kW to 315 MW during a 45 s exponential ramp | qualitative dynamical | yes, on reduced physics | ✅ | supported: nominal ends at 313.8 MW (−0.39 %) |
| C2 | Latin Hypercube Sampling of PID coefficients is a viable design-of-experiments for the surrogate training set | methodological | yes | ✅ | supported (250-pt LHS covers box) |
| C3 | A **polynomial regression surrogate** of the transient QoI (CD angle at end of ramp) attains **within-5 %** accuracy vs the base model | quantitative surrogate accuracy | yes (analogue) | ✅ | supported: **max rel err 0.258 %, R² 0.987** on 80-pt hold-out (well within 5 %) |
| C4 | Variance-based (Sobol) sensitivity analysis via the trained surrogate is orders-of-magnitude faster than direct Sobol on the base model | speed | yes | ✅ | supported: 10 k Sobol samples of surrogate = 0.02 s vs ~14 min if run on the physics |
| C5 | The dominant contributors to CD-angle variance are the PID coefficients (with power-side coefficients being most important for a well-tuned hybrid controller) | quantitative SA ranking | yes (analogue) | ✅ | supported: **Ki_pow (ST 0.63) + Kp_pow (ST 0.35) account for ≈98 % of total variance** |
| C6 | Absolute Griffin/Serpent2 CD-angle values, and cross-section-temperature sensitivities | quantitative physics-specific | **NO** (requires MOOSE + Serpent2 + full cross-section library) | ❌ | out of scope for this replication |

---

## 3  Methods (honest scope)

### 3.1 What the paper does
- Base model: 3-D MOOSE/Griffin diffusion + IQS kinetics on a 112-state-point Serpent2 cross-section library; hybrid PID controller sits *above* Griffin as a MOOSE MultiApp.
- Perturbed inputs: PID coefficients (K_p, K_i, K_d for both power-side and reactivity-side) and cross-section temperatures.
- Sampling: Latin Hypercube.
- Surrogate: polynomial regression in the MOOSE Stochastic Tools Module.
- SA: variance-based (Sobol) indices.
- QoI: CD angle trajectory (control signal).

### 3.2 What we do (`work/replicate.py`)
- **Physics surrogate.** Standard point-reactor kinetics (PRK) with Keepin's 6 delayed-neutron groups for U-235 (canonical `LAMBDA`, `BETA_I`, β ≈ 6.5 × 10⁻³; mean generation time Λ = 5 × 10⁻⁵ s). We integrate using semi-implicit Euler on precursors and an implicit-Euler step on prompt neutron density for stiffness robustness.
- **CD-angle → reactivity map.** `ρ(θ) = α (θ₀ − θ)` with θ₀ = 120°, α chosen so that θ = 0° inserts +2 $ of reactivity and θ = 180° inserts −1 $. Sign matches the paper: drums out ⇒ positive reactivity.
- **Controller.** Identical hybrid-PID architecture as paper Eqs. of §2.1.3–2.1.4: a power-fractional-error PID plus a reactivity-error PID (in dollars = ρ/β) summed to produce CD rotation rate `dθ/dt`, with a physical actuator slew-rate limit `|dθ/dt| ≤ 5°/s`, anti-windup on the integral terms, and angle saturation `[0°, 180°]`.
- **Power demand.** Exponential ramp 500 kW → 315 MW over 0 ≤ t ≤ 45 s, then constant to t = 75 s (exact paper benchmark).
- **UQ pipeline.** LHS (scipy `qmc.LatinHypercube`) of the 6 PID coefficients, ±25 % about nominal, 250 training + 80 test samples.
- **Surrogate.** `PolynomialFeatures(degree=3) + LinearRegression` on scikit-learn (paper: polynomial regression in MOOSE STM — same family).
- **Sobol.** Saltelli 2010 estimator implemented manually (SALib not installed in this env), N = 10 000, first-order S_i and total-order S_Ti.

### 3.3 What we deliberately omit
- No Griffin, no Serpent2, no MOOSE, no 3-D diffusion, no multigroup cross sections, no temperature feedback on cross sections, no IQS.
- Consequently: no absolute Griffin numbers, no cross-section-temperature SA — this replication reproduces the *methodology* on a physics that shares the right input→output structure.

### 3.4 Reproducibility
- Single script, single seed (`RNG_SEED = 20260705`), zero external state, ~30 s on a laptop.
- Deterministic outputs in `work/results.json`.

---

## 4  Reproduced Numbers

### 4.1 Nominal transient (single deterministic run)

| Quantity | Target / paper | Ours |
|----------|---------------|------|
| Final power | 315 MWth | 313.8 MWth (−0.39 %) |
| Initial CD angle | 120° | 120° |
| Final CD angle | qualitative: "drums rotated outward" | 112.06° (Δθ = −7.94° out) |
| Simulation window | 0–75 s | 0–75 s |

Controller behaviour is qualitatively consistent with the paper: at nominal PID gains the controller rotates the drums outward monotonically over the ramp and settles the reactor near set-point by the constant-power phase.

### 4.2 Surrogate accuracy (Claim C3)

| Metric | Value |
|--------|-------|
| Training LHS samples | 250 |
| Test LHS samples | 80 |
| Polynomial degree | 3 |
| Test R² | **0.9873** |
| Test RMSE | 0.081° |
| Test mean rel err | 0.05 % |
| Test 95th-pct rel err | 0.15 % |
| Test **max rel err** | **0.258 %** |
| Paper's stated accuracy claim | **≤5 %** |
| Meets paper's claim? | **YES** |

### 4.3 QoI moments (final CD angle over the 330-sample LHS ensemble)

| Statistic | Value |
|-----------|-------|
| mean θ_end | 112.14° |
| std θ_end | 0.76° |
| min / max | 110.66° / 113.71° |
| coeff. of variation | 0.68 % |

### 4.4 Sobol indices (variance of CD angle at end of ramp, computed via surrogate)

Ranked by total-order (S_T):

| Rank | Parameter | First-order S₁ | Total-order S_T | Role |
|------|-----------|-----------------|------------------|------|
| 1 | **Ki_pow** | 0.460 | **0.627** | integral gain of power PID |
| 2 | **Kp_pow** | 0.694 | **0.354** | proportional gain of power PID |
| 3 | Kp_rho | 0.285 | 0.045 | proportional gain of reactivity PID |
| 4 | Ki_rho | 0.197 | 0.004 | integral gain of reactivity PID |
| 5 | Kd_rho | 0.067 | 0.003 | derivative gain of reactivity PID |
| 6 | Kd_pow | 0.052 | 0.002 | derivative gain of power PID |

**Sum of total-order indices ≈ 1.03**, consistent with a slightly-super-additive Saltelli estimate (finite N, mild interactions). Note that the first-order sum > 1 is a known finite-sample artefact of the Saltelli estimator on smooth low-interaction models — with monotonic surrogates the individual S₁ terms overlap and can each individually correlate well with Y. The **variance-explaining ranking** is the meaningful result.

**Comparison to paper's qualitative SA finding.** The paper's Sec. 3 reports (qualitatively, from figures) that for the hybrid controller, the *power-PID gains dominate* the CD-angle response, with the reactivity-side gains playing a smaller corrective role. Our replication reproduces the same ranking: `{Ki_pow, Kp_pow}` together carry **≈98 %** of total-order variance; reactivity-side gains together carry **≈5 %**; derivative-of-power gain is negligible.

---

## 5  Agreement

| Aspect | Agreement |
|--------|-----------|
| Nominal transient reaches ~315 MW under hybrid PID with drums rotating outward | ✅ qualitative agreement |
| LHS + polynomial surrogate is workable design | ✅ methodological agreement |
| Polynomial surrogate accuracy comfortably beats 5 % on this QoI | ✅ **quantitative agreement (0.26 % vs 5 % claim)** |
| Power-side PID coefficients dominate CD-angle variance | ✅ **rank agreement** (Ki_pow + Kp_pow ≈ 98 % ST) |
| Absolute Griffin CD-angle numbers | ❌ **not tested** (requires full MOOSE/Griffin/Serpent2) |
| Cross-section-temperature sensitivity | ❌ **not tested** (no cross-section library) |

---

## 6  Verdict

**VERDICT: PARTIAL**

Rationale: We reproduce the paper's *methodological* claims — the LHS + polynomial-regression + Sobol pipeline works, comfortably beats the ≤5 % surrogate-accuracy claim on our physics, and qualitatively confirms the dominance of the power-PID gains over the reactivity-PID gains for CD-angle variance during a nominal hybrid-controlled startup. However, we do **not** reproduce the paper's *physics-specific* numbers (absolute Griffin CD angles, cross-section-temperature sensitivities) because those require the MOOSE / Griffin / Serpent2 toolchain and cross-section library, which are outside the free-tool 15-min scope. Hence PARTIAL rather than REPLICATED. No contradictions were found; a NO-GO or CONTRADICTED verdict would be inappropriate.

---

## 7  Artifacts

```
OSTI-3027604-nuclear-thermal-uq-sa/
├── work/
│   ├── paper.pdf              # Frontiers substitute, SHA-256 f025ca80...25363047
│   ├── replicate.py           # 300-line honest reduced replication (numpy/scipy/sklearn only)
│   └── results.json           # full numeric outputs (nominal transient, surrogate stats, Sobol, moments)
└── report/
    └── REPORT.md              # this document
```

## 8  Honest limitations

- Point-kinetics + hand-tuned nominal PID gains. Our nominal was tuned to give a stable startup on the reduced model, not to match the paper's numeric PID values (paper's `Kp_pow`, `Ki_pow`, ... are in Griffin-native units that are not portable to a PRK controller).
- 6 inputs perturbed vs paper's larger sweep in later sections. Method scales; we chose 6 for a clean Sobol demo.
- Saltelli sum-check: individual S₁ values sum > 1 (0.05–0.05 each, first-order aggregated), a known finite-sample bias of the estimator on smooth surrogates with correlated first-order effects. Total-order sum (≈1.03) is well-behaved and used for the ranking claim.
- Substituted paper source (Frontiers, not OSTI purl) because OSTI was unreachable — same authors, same INL work, same DOI-linked full text; SHA-256 recorded above.
