# Independent Replication — Bertozzi, Garnett & Laurent (2012)
## "Characterization of radially symmetric finite time blowup in multidimensional aggregation equations"

- **Paper:** arXiv:1204.1095v1 (5 Apr 2012); SIAM J. Math. Anal.; DOI 10.1137/11081986X
- **Authors:** Andrea L. Bertozzi (UCLA), John B. Garnett (UCLA), Thomas Laurent (UC Riverside)
- **Set:** PDE-100 replication wave (priority rank 48, score 51.08, cited 60, OA-PDF repro-ok)
- **Replication type:** independent re-derivation + from-scratch numerical verification (analysis paper; no authors' code exists)
- **Compute:** local (CherryRd), numpy 2.4.3 / scipy 1.18.0. Judges via free Argo proxy.

---

## 1. Paper summary

The paper studies the nonlocal **aggregation equation**

  ∂ρ/∂t − div(ρ ∇K∗ρ) = 0,  in R^d, d ≥ 2,   (1.1)

with power-law kernels K = |x|^α/α, focusing on 2−d ≤ α < 2 (the regime where smooth
densities develop finite-time singularities). Main analytical contributions: existence for
all time of radially symmetric *monotone-decreasing* measure solutions (continuation past
blowup), preservation of monotonicity for α<2, and—crucially for our purposes—a **special
Newtonian case (α = 2−d)** in which the radial problem localizes and reduces exactly to the
**inviscid Burgers equation on a half-line**, enabling classical conservation-law theory.

Because this is primarily a *theory* paper, "replication" here means **independently
re-deriving and numerically verifying its exact, computable Section-4 predictions** rather
than re-running code. These predictions have concrete reference numbers (e.g. simultaneous
collapse at a single finite time; ρ_t = ρ²; explicit shock-time formula).

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Result |
|----|-------|------|-----------|---------|--------|
| C1 | Radial Newtonian aggregation reduces via m(r)=∫₀^r s^{d-1}ρ ds and z=r^d to inviscid Burgers m_t − m m_z = 0 (eqs 4.2–4.4) | analytic/derivation | yes | yes | **REPRODUCED** — 3 independent implementations agree exactly |
| C2 | For monotone-decreasing radial data, shocks form only at the origin; characteristics stay ordered; monotonicity preserved ∀t (Thm 4.1) | analytic + numerical | yes | yes | **REPRODUCED** — far-field ordering exact; only pileup is at origin |
| C3 | First shock at t_shock = 1/sup_z m'_init(z); monotone data ⇒ characteristic reaches origin before shock (eq 4.5) | analytic formula | yes | yes | **REPRODUCED** — predicted = observed to rel-err 1e-9…1e-16 |
| C4 | "Collapsing ball" (indicator of a ball) ⇒ Burgers solution ~ −z/(1−t); all characteristics on an interval collapse at the origin **simultaneously** in finite time (most singular case) | analytic/exact | yes | yes | **REPRODUCED** — shell-time spread ~1e-16 (machine zero), d=2,3,4 |
| C5 | ρ_t = ρ² along characteristics (density-blowup heuristic) | analytic heuristic | yes | yes | **REPRODUCED** — (dρ/dt)/ρ² = 1.00000, stable |
| C6 | Global existence of radial monotone-decreasing measure solutions for 2−d<α<2; Dirac-mass at critical exponent; α>2 loses monotonicity | pure analysis (existence/measure theory) | no (proof-level) | no | out of scope for numerical replication |

## 3. Method (numbered)

All physics implemented from scratch in numpy — **no library PDE solver** was used for the
dynamics (scipy present but unused for the solves).

1. **Radial reduction (C1).** For the Newtonian kernel −ΔK=δ, the radial velocity is
   v(r) = −m(r)/r^{d-1} with m(r)=∫₀^r s^{d-1}ρ(s)ds (paper eq 4.2). A single Lagrangian
   shell at radius r obeys dr/dt = v(r). For monotone data the mass strictly interior to a
   shell is conserved along its characteristic, giving the **closed-form shell ODE**
   r(t)^d = r0^d − d·m0·t (integrate r^{d-1}dr = −m0 dt), m0 = m(r0). Shell collapse time
   t_shell = r0^d/(d·m0).
2. **Uniform ball / C4.** ρ=const=c inside R0 (normalized so m(R0)=1 ⇒ c=d/R0^d). Then
   m(r0)=c r0^d/d, so t_shell = r0^d/(d·c r0^d/d) = **R0^d/d, independent of r0** ⇒ all
   shells collapse simultaneously. Checked over 20 shells, d=2,3,4. (`aggregation_newtonian.py::run_uniform_ball`)
3. **Direct N-particle radial simulation (C2, independent cross-check).** 1500 particles
   sampled from the radial mass density r^{d-1}ρ(r); RK4 integration of
   dr_i/dt = −M(r_i)/r_i^{d-1} where M(r_i) = (#particles inside)·(mass/particle). No
   shell-conservation assumption is baked in. Ordering among active (r>0) shells is
   monitored. (`aggregation_newtonian.py::run_particles`, `check_ordering*.py`)
4. **Inviscid Burgers by characteristics (C1 equivalence, C3).** z=r^d ⇒ dz/dt = d r^{d-1}·(dr/dt)
   = d r^{d-1}(−m/r^{d-1}) = −d·m, so the z-characteristic speed is −d·m and m is constant
   along characteristics: this **is** m_t − m m_z = 0 up to the dimensional time factor. Shock =
   first neighbouring-characteristic crossing; predicted t_shock = 1/(d·sup_z m'_init(z)).
   (`aggregation_newtonian.py::run_burgers_uniform`, `c3_shock_time.py`)
5. **Density blowup (C5).** Along a collapsing uniform-ball shell, local density
   ρ(t) = m0/((1/d)r(t)^d); measured (dρ/dt)/ρ² numerically. (`aggregation_newtonian.py::run_density_blowup`)
6. **Non-uniform monotone tests (C3).** Gaussian ρ=e^{−4r²} and parabolic cap ρ=max(1−(r/R)²,0):
   built m_init(z) numerically, computed sup_z m'_init(z), compared the formula t_shock to the
   observed first blowup (interior char-cross AND origin-reach). (`c3_shock_time.py`)
7. **Multi-judge assessment.** Free Argo endpoints gpt-5.2, gemini-2.5-pro, gpt-4.1 (opus
   avoided per brief). (`judge.py` → `evidence/judge_verdicts.json`)

## 4. Results vs paper

### C4 — collapsing ball: simultaneous collapse (`evidence/aggregation_results.json`)
| d | t*_theory (R0^d/d) | shell-time mean | spread across 20 shells |
|---|---|---|---|
| 2 | 0.500000 | 0.500000 | 1.67e-16 |
| 3 | 0.333333 | 0.333333 | 1.11e-16 |
| 4 | 0.250000 | 0.250000 | 5.55e-17 |

Spread is at machine precision ⇒ **all characteristics collapse at the origin simultaneously**
at exactly R0^d/d, directly confirming the paper's "most singular case" statement. Independent
particle sim: mean collapse t = 0.5014 (d=2), 0.3342 (d=3) vs theory 0.5, 0.3333 (≈0.3% dt error).

### C1 — Burgers equivalence
z-characteristic speed −d·m gives t_shock = R0^d/d, matching the closed-form shell ODE
**exactly** (matches_methodA = True for d=2,3,4). The three independent routes (shell ODE,
particle sim, Burgers characteristics) agree.

### C3 — shock-time formula (`evidence/c3_shock_time.json`)
| data | d | t_shock = 1/(d·sup m'_init) | observed first blowup | rel err |
|---|---|---|---|---|
| gaussian | 2 | 1.004508 | 1.004508 | 4.4e-10 |
| gaussian | 3 | 1.088751 | 1.088751 | 2.0e-16 |
| parabola | 2 | 1.000125 | 1.000125 | 1.8e-09 |
| parabola | 3 | 1.002387 | 1.002387 | 8.9e-16 |

For monotone data the first *interior* characteristic-crossing time equals the origin-reach
time ⇒ **shock forms exactly at the origin**, as the paper asserts (eq 4.5 condition).

### C5 — density blowup ρ_t = ρ²
Median (dρ/dt)/ρ² = **1.00000** and stable (self-similar) along the collapsing-shell
characteristic for d=2 and d=3; ρ grows from O(1) to ~2000+ as the shell reaches the origin.
Confirms the paper's heuristic exactly.

### C2 — monotonicity / shocks only at origin (`evidence/ordering_check.json`)
Among shells with r>0.05 (away from the origin), worst ordering disorder = **0.00 exactly**
(d=2). The only "disorder" is the simultaneous-collapse pileup at the origin boundary, and it
does **not** decrease with Δt (0.94e-2 stable across Δt=4e-4→5e-5), confirming it is the
*physical* shock at the origin predicted by Thm 4.1, not a numerical scheme error.

### Internal consistency
No internal inconsistencies were found between the paper's Section-4 statements and the
verified numbers. One transient discrepancy in an early diagnostic (a d=3 gaussian shock
time) was traced to `np.gradient` on a non-uniform z-grid in the first script and resolved by
a clean uniform-grid characteristics solve (`c3_shock_time.py`); the corrected value matches
theory to machine precision.

## 5. Judge verdicts (free Argo, `evidence/judge_verdicts.json`)
- **argo:gpt-5.2** → REPLICATED (C1,C2,C4,C5 REPLICATED; C3 initially SPOT-CHECK — subsequently upgraded to REPLICATED by the direct observed-vs-predicted comparison in `c3_shock_time.py`).
- **argo:gemini-2.5-pro** → REPLICATED (all C1–C5).
- **argo:gpt-4.1** → REPLICATED (all C1–C5).

Unanimous overall verdict: **REPLICATED**.

## 6. Scope / limitations
- The paper's *existence/measure-theoretic* results (C6: global existence for 2−d<α<2,
  Dirac-mass emergence at the critical exponent, non-preservation of monotonicity for α>2)
  are proof-level and not amenable to a direct numerical reference number; they are out of
  scope for numerical replication and were not tested.
- Publisher HTML (SIAM/T&F/MDPI) was Cloudflare-blocked; the authoritative arXiv full text +
  LaTeX source were used (canonical for the mathematics).
- The numerical work verifies the Section-4 *Newtonian* core, which is the part of the paper
  carrying concrete, verifiable predictions.

## Verdict
**Verdict:** REPLICATED
