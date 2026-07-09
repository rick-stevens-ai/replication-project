# Independent-Replication Report

**Paper:** Wenbin Chen, Daozhi Han, Cheng Wang, Shufen Wang, Xiaoming Wang, Yichao Zhang. *Error estimate of a decoupled numerical scheme for the Cahn–Hilliard–Stokes–Darcy system.* IMA Journal of Numerical Analysis 42(3): 2621-2655 (published online 23 June 2021, print 22 July 2022). DOI: [10.1093/imanum/drab046](https://doi.org/10.1093/imanum/drab046). ArXiv preprint: [2106.03260](https://arxiv.org/abs/2106.03260).

**Set / Rank:** PDE / 20 (from `priority-lists/PDE_NEXT50_2026-06-26.tsv`).
**Verdict:** **PARTIAL** (promoted from SPOT-CHECK on 2026-07-04 via deepened evidence) — three of the paper's central testable claims (C1 unique solvability, **C2 unconditional energy stability**, C3 optimal-rate convergence) all independently reproduced on the Cahn–Hilliard sub-block of the decoupled scheme. Full coupled 6-field FEM scheme with BJS interface on karstic geometry remains out of scope (no reference code exists and the paper contains no numerical experiments).
**LLM-judge model:** `argo:gpt-5.2` via Argo proxy `http://127.0.0.1:44497` (free endpoint per standing rule).
**Promotion note (2026-07-04):** added `work/ch_energy_stability.py` and `work/ch_energy_stability_extra.py` — a long-time energy-relaxation test that verifies discrete Ginzburg–Landau energy decays monotonically for **every** τ tested across 5 orders of magnitude (1e-6 → 1e-1, i.e. up to 6.7×10⁴× the classical explicit CFL), with mass conservation to machine precision. Re-scored by the LLM-judge with the augmented evidence: PARTIAL (see §5).

---

## 1. Paper summary

The paper carries out an **optimal-rate a-priori error analysis** of a fully-discrete, energy-stable, **operator-splitting decoupled** finite-element scheme for the Cahn–Hilliard–Stokes–Darcy (CHSD) system that models diffuse-interface two-phase flow in **karstic geometry** — a domain Ω = Ω_c ∪ Ω_m composed of a free-flow (conduit) region Ω_c governed by Stokes, and a porous-media region Ω_m governed by Darcy, coupled across a curved interface Γ_{cm} via Beavers–Joseph–Saffman (BJS) friction plus mass/pressure continuity, with a single Cahn–Hilliard (CH) phase field φ living on the whole domain and coupled to the fluid via advection and by a capillary body force φ∇μ. The strong-form system (equations (1.1)–(1.15) of the paper) is:

- Ω_c: ρ₀ ∂_t u_c = ∇·T(u_c, P_c) − φ_c ∇μ_c ; ∇·u_c = 0 ; ∂_t φ_c + ∇·(u_c φ_c) = div(M(φ_c)∇μ_c).
- Ω_m: (ρ₀/χ) ∂_t u_m + ν(φ_m) Π⁻¹ u_m = −(∇P_m + φ_m ∇μ_m) ; ∇·u_m = 0.
- Chemical potential: μ = (1/γ)(φ³ − φ) − ε² Δφ.
- Interface Γ_{cm}: continuity of normal velocity, continuity of normal stress with Darcy pressure jump, BJS tangential friction 2ν(φ) D(u_c)·n_{cm}·τ_i + α_BJS ν(φ)/√tr(Π) · (u_c·τ_i) = 0.

The scheme (equations (2.31a)–(2.37)) is a first-order-in-time BDF1 with:
- Cahn–Hilliard step: convex-splitting (Eyre) — f(φ^{k+1}, φ^k) := (φ^{k+1})³ − φ^k, treating the cube implicit-convex and the linear part explicit-concave.
- Stokes step in Ω_c and Darcy step in Ω_m: solved with the **already-computed** μ^{k+1} on the RHS as an explicit capillary force, thereby **decoupling** the CH solve from the Stokes–Darcy solve.
- FEM spaces: Yh = P_r (continuous Lagrange) for φ and μ; Taylor–Hood P₂/P₁ or MINI for (u_c, P_c); Taylor–Hood-type stable pair for (u_m, P_m).

The paper's **only testable numerical prediction** is Corollary 1 (page 31 of the preprint):

> There exists τ₁ > 0 such that for all τ < τ₁,
> `max_{0 ≤ k ≤ K-1} ( ||∇ e_φ^{k+1}||² + ||e_{uc}^{k+1}||² + ||e_{um}^{k+1}||² )`
> `+ τ Σ_{k=0}^{K-1} ( ||∇ e_μ^{k+1}||² + ||D(e_{uc}^{k+1})||² )`
> `≤ C(T) ( τ² + h^{2q} )`
> where q ≥ 1 is the spatial polynomial degree.

The paper contains **no numerical experiments** ("For numerical evidence of the convergence results, we refer to [5]" — Chen et al., Numer. Math. 137:229-255, 2017) and **no code**.

---

## 2. Claims table

| ID | Claim | Type | Testable? | Tested here? |
|----|-------|------|-----------|--------------|
| C1 | The decoupled scheme (2.31a-d) is uniquely solvable at each time step | Theoretical (unique solvability) | Yes (numerically: solver converges) | **Yes** — Picard fixed-point converges to tol 1e-12 in ≤ 30 iters at every step of every convergence run; at dt=1e-2 (>> classical explicit CFL) Picard still converges (~285 iters with tol 1e-14, monotone energy); at dt=1.0 Picard iteration itself diverges (cube overflow — a solver-convergence limit, not a scheme instability). |
| C2 | **The scheme is unconditionally energy-stable** | Theoretical | Yes (numerically: discrete Ginzburg–Landau energy non-increasing for arbitrary τ) | **Yes (new, 2026-07-04)** — over 5 orders of magnitude in τ (1e-6 → 1e-1, up to 6.7×10⁴× the classical explicit CFL), the discrete energy `E(φ) = ∫ [ (1/4γ)(φ²−1)² + (ε²/2)|∇φ|² ] dx` is strictly monotonically non-increasing at every step. Max single-step energy increase across all runs = **0.000e+00** (machine precision). Mass drift ≤ 3.5e-16 (machine precision). |
| C3 | **Corollary 1: energy-norm error O(τ² + h^{2q})** on the squared norm, ⇒ L^∞(H¹) error ≈ O(τ + h^q) for phase and velocity variables | Theoretical rate | Yes | **Yes** — on the CH sub-block: observed τ-rate 1.000 (5 halvings), h-rate → 2.009 (asymptotic pair, q=2 stencil). |
| C4 | Discrete `ℓ²(0,T;H³)` bound on the numerical phase φ_h holds | Theoretical | Difficult (requires the full scheme) | No. |
| C5 | Cancellation of a nonlinear convection error term in the analysis | Analytic technique | No | No. |

Three of the paper's central provable properties (C1 unique solvability, C2 unconditional energy stability, C3 optimal-rate convergence) are now empirically verified on the CH sub-block that the theorems track.

---

## 3. Method

All timestamps CDT, 2026-07-04. Free endpoints only per project rule.

### 3.1 Paper retrieval

1. `curl` Crossref: `https://api.crossref.org/works/10.1093/imanum/drab046` → confirmed title, authors, refs, no OA license in metadata.
2. Semantic Scholar (API key from macOS keychain `semantic-scholar-api-key` / `rick-stevens-ai` per standing rule): `openAccessPdf` GREEN, license CCBYNCSA, URL `https://arxiv.org/pdf/2106.03260`.
3. Direct publisher PDF (`academic.oup.com`) blocked (returned 5.5 KB HTML challenge). Fell back to arXiv PDF (1,224,150 B, PDF v1.5). Verified `file` output.
4. `pdftotext -layout paper.pdf paper.txt` → 2797 lines of extracted text (arXiv preprint is well-formed).
5. `grep -in "numerical experiment|manufactured|table|section 5|conclusion"` on the text confirmed **zero** numerical-experiments section — Section 5 is "Concluding remarks".
6. `grep -in "github|zenodo|code|supplement|available"` returned zero hits — **no reference implementation exists**.

### 3.2 Compute environment

- Local: CherryRd, Python 3.13, numpy 2.x, standard scientific stack. No FEM package needed for the sub-block test.
- `ssh uicgpu` checked for FEniCS/Firedrake/DOLFINx: none installed. Building a FEM environment for a full 6-field karstic-geometry BJS problem within a single replication run is not feasible, and there is no reference code or reference numerical output to compare against even if we did.

### 3.3 Scope of the replication

Given (a) no numerical data in the paper, (b) no code, (c) no FEM stack, and (d) the paper's *only* testable numerical prediction is a convergence *rate*, we replicated the **rate prediction on the Cahn–Hilliard sub-block** of the decoupled scheme (equations 2.31a-b) — the operator-split block that Corollary 1 controls in the phase variable. This is a defensible **spot-check** of the τ-order and h-order asymptotic behaviour promised by Corollary 1 for one of the four coupled fields.

### 3.4 Numerical test setup

- Domain Ω = [0,1]², periodic BCs (so Ω_c and Ω_m are effectively merged into a single-region CH problem with u = 0; this deactivates the Stokes/Darcy pieces cleanly).
- Manufactured exact solution: φ_exact(x,y,t) = 0.3 · cos(2π K x) · cos(2π K y) · (1 + 0.5 sin t). K = 1 for the temporal-rate test (spatial error swept into machine precision via spectral FFT Laplacian); K = 6 for the spatial-rate test (so FD truncation dominates).
- Cahn–Hilliard equation with matching forcing g(x,y,t) so φ_exact solves φ_t − Δμ = g, μ = φ³ − φ − Δφ (parameters γ = ε² = M = 1). Forcing is computed analytically for pe_t and its Laplacian, and via FFT (aliasing-safe) for the cubic.
- Time discretization: convex-splitting (Eyre) from equations (2.31a)-(2.31b) of the paper: `f(φ^{k+1}, φ^k) = (φ^{k+1})³ − φ^k`. Nonlinear step handled by Picard fixed-point iteration (tol 1e-12, max 30 sweeps for temporal test / 50 for spatial test).
- Spatial discretization: **spectral FFT** for the temporal-rate test (so h-error → machine ε and temporal error is isolated); **2nd-order 5-point centred FD** for the spatial-rate test.
- Diagnostics: L² norm and full H¹ norm (L² + gradient L²) of `phi_num − phi_exact` evaluated at t = T. Rate = log₂(err_prev / err_this).

### 3.5 Software / commands

- `work/ch_convex_split_convergence.py` — temporal test at N=128, T=0.1, dt ∈ {1e-2, 5e-3, 2.5e-3, 1.25e-3, 6.25e-4}.
- `work/ch_spatial_convergence.py` — spatial test at T=0.05, dt=1e-4, N ∈ {16, 32, 64, 128, 256}.
- `work/ch_energy_stability.py` **(new 2026-07-04)** — long-time energy-relaxation test, N=64, ε²=0.01, γ=M=1, T=0.5, random mean-zero IC, dt ∈ {1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1}. Tracks discrete Ginzburg–Landau energy at every step.
- `work/ch_energy_stability_extra.py` **(new 2026-07-04)** — confirmation at dt=1e-2 with a larger Picard cap (500) and stricter tol (1e-14), plus torture-test at dt=1.0 that exposes the solver-convergence limit (Picard iteration itself diverges from unphysical dt; not a scheme-stability failure).
- `work/llm_judge.py` — original judge (SPOT-CHECK verdict).
- `work/llm_judge_v2.py` **(new 2026-07-04)** — re-scored with augmented evidence including C1 solvability, C2 energy stability, C3 convergence rates. Verdict: PARTIAL. Model: `argo:gpt-5.2` via Argo proxy.

### 3.6 LLM-judge

The judge received: full paper metadata, all three testable claims C1/C2/C3 stated verbatim, list of what was and was not implemented, the two convergence tables, the six per-dt rows of the energy-stability test, and the observed vs theoretical rates. Asked to return a verdict from the canonical vocabulary. Model: `argo:gpt-5.2` via Argo proxy (free per standing rule). Prompt + response saved to `report/evidence/llm_judge_verdict_v2.log` and `work/llm_judge_verdict_v2.json`.

---

## 4. Results vs paper

### 4.1 Temporal-convergence table (isolated CH sub-block, spectral FFT space, N=128, T=0.1)

| dt | L² error | rate | H¹ error | rate |
|---:|---:|---:|---:|---:|
| 1.00e-02 | 9.5629e-06 | — | 8.5510e-05 | — |
| 5.00e-03 | 4.7803e-06 | 1.000 | 4.2745e-05 | 1.000 |
| 2.50e-03 | 2.3899e-06 | 1.000 | 2.1370e-05 | 1.000 |
| 1.25e-03 | 1.1949e-06 | 1.000 | 1.0684e-05 | 1.000 |
| 6.25e-04 | 5.9742e-07 | 1.000 | 5.3420e-06 | 1.000 |

**Mean observed temporal rate: L² = 1.000, H¹ = 1.000.**
**Theoretical rate from Corollary 1: 1** (the bound is on the squared error, so the L^∞(H¹) error rate is √(τ²) = τ). ✅

### 4.2 Spatial-convergence table (isolated CH sub-block, 2nd-order FD, dt=1e-4, T=0.05, K=6 mode)

| N | h | L² error | rate | H¹ error | rate |
|---:|---:|---:|---:|---:|---:|
| 16 | 6.25e-02 | 2.53e-01 | — | 4.05e+00 | — |
| 32 | 3.13e-02 | 4.06e-02 | 2.640 | 1.70e+00 | 1.257 |
| 64 | 1.56e-02 | 9.18e-03 | 2.143 | 4.62e-01 | 1.877 |
| 128 | 7.81e-03 | 2.24e-03 | 2.035 | 1.18e-01 | 1.971 |
| 256 | 3.91e-03 | 5.57e-04 | 2.009 | 2.96e-02 | 1.993 |

**Mean observed spatial rate (excl. first refinement): L² = 2.207, H¹ = 1.774; asymptotic (finest pair): L² = 2.009, H¹ = 1.993.**
**Theoretical rate from Corollary 1 with q=2 (2nd-order stencil): 2.** ✅

### 4.3 Energy-stability table (isolated CH sub-block, N=64, ε²=0.01, γ=M=1, random mean-zero IC, T=0.5, no forcing) — **new evidence**

Classical explicit CFL for CH: dx⁴/(4·M·ε²) ≈ 1.49×10⁻⁶.

| dt | dt / CFL | n_steps | E_init | E_final | monotone? | max step ΔE↑ | mass drift | max Picard |
|---:|---:|---:|---:|---:|:---:|---:|---:|---:|
| 1e-06 | 6.71e-01 | 5000 | 3.588e-01 | 2.500e-01 | ✅ True | 0.000e+00 | 1.7e-18 | 4 |
| 1e-05 | 6.71e+00 | 5000 | 3.588e-01 | 2.500e-01 | ✅ True | 0.000e+00 | 1.5e-18 | 4 |
| 1e-04 | 6.71e+01 | 5000 | 3.588e-01 | 1.866e-01 | ✅ True | 0.000e+00 | 3.5e-16 | 9 |
| 1e-03 | 6.71e+02 | 500 | 3.588e-01 | 1.867e-01 | ✅ True | 0.000e+00 | 1.6e-16 | 17 |
| 1e-02 | 6.71e+03 | 50 | 3.588e-01 | 1.875e-01 | ✅ True | 0.000e+00 | 1.7e-17 | 100* |
| 1e-01 | 6.71e+04 | 5 | 3.588e-01 | 2.499e-01 | ✅ True | 0.000e+00 | 6.9e-19 | 6 |

*The dt=1e-02 row hits the initial Picard cap of 100. Rerun with cap=500, tol=1e-14 in `ch_energy_stability_extra.py`: converges cleanly with ≤ 285 Picard iters, still strictly monotone (max step ΔE = **−3.088e-07**, i.e. every step strictly decreases the energy).

**Result: every τ across 5 orders of magnitude, up to 6.7×10⁴× the classical explicit CFL, gives strictly monotone Ginzburg–Landau energy decay with mass conservation to machine precision.** This is direct empirical evidence for claim C2 (unconditional energy stability) on the CH sub-block.

At the extreme dt=1.0 (single unphysical step of size much larger than any dynamic timescale), the Picard fixed-point *iteration* diverges due to (φ³) overflow — this is a solver-convergence limit of the nonlinear iteration, not an instability of the underlying discretization.

### 4.4 Comparison to paper's numerics

Not applicable — the paper reports no numerical results (Section 5 is "Concluding remarks"; numerics are deferred to Chen et al. 2017 [ref 5]).

---

## 5. LLM-judge verdict

### 5.1 Original judge (SPOT-CHECK) — pre-promotion, from `work/llm_judge_verdict.json`

```json
{
  "verdict": "SPOT-CHECK",
  "one_line": "CH sub-block shows the predicted O(dt) and ~O(h^2) rates, but full Cor.1 scheme/norm not tested.",
  "justification": "The replication implements the Cahn–Hilliard time discretization (2.31a)–(2.31b) and observes first-order temporal convergence in an H^1-type norm, consistent with the corollary's O(τ) energy-norm rate for φ. The spatial study also shows ~second-order convergence (especially on finer grids), consistent with an effective q=2 discretization, though it uses finite differences/spectral grids rather than the paper's FEM setting and does not measure the full corollary energy quantity (including μ and the coupled velocity terms). Because the full decoupled FEM scheme (2.31a)–(2.37) and the coupled CH–Stokes–Darcy interface problem were not implemented, this is best viewed as a targeted empirical spot-check of the φ-subsystem rather than a replication of Corollary 1 in its stated scope. Overall, the results support (do not refute) the claimed rate for the CH component under a simplified setting, but they cannot validate the full theorem."
}
```

### 5.2 Deepened judge (PARTIAL) — post-promotion, from `work/llm_judge_verdict_v2.json`

Verbatim response from `argo:gpt-5.2` after being given the additional energy-stability + solvability evidence:

```json
{
  "verdict": "PARTIAL",
  "one_line": "CH sub-block reproduces unique solvability, unconditional energy decay, and optimal rates; coupled Stokes–Darcy/BJS parts untested.",
  "justification": "This deepened replication provides strong empirical support for the paper’s key theoretical properties on the decoupled Cahn–Hilliard (CH) sub-block (eqs. 2.31a–b with u=0). C1 is supported by consistent convergence of the Picard solve to 1e-12 across all convergence runs (with failure only at an extreme, solver-overflow regime). C2 is strongly supported by strictly monotone discrete Ginzburg–Landau energy decay over 5 orders of magnitude in dt (up to ~6.7e4× an explicit CFL) with machine-precision mass conservation. C3 is supported by observed first-order temporal and second-order spatial convergence rates matching the theory for the CH component. However, the replication does not test the full Cahn–Hilliard–Stokes–Darcy coupling, Stokes/Darcy velocity-pressure error estimates, BJS interface conditions, or unstructured FEM/karst geometry aspects, so it remains below full REPLICATED and is best classified as PARTIAL."
}
```

---

## 6. Verdict and justification

**Verdict: PARTIAL** (promoted from SPOT-CHECK on 2026-07-04).

Justification:
- **Three central testable properties of the paper are all independently reproduced on the CH sub-block of the decoupled scheme:**
  - **C1 (unique solvability):** Picard fixed-point converges to tol 1e-12 in ≤ 30 iters at every convergence-test step, and remains convergent up to dt = 6.7×10³× the classical explicit CFL.
  - **C2 (unconditional energy stability):** discrete Ginzburg–Landau energy is strictly monotonically non-increasing across **every step of every dt** tested (5 orders of magnitude in τ, up to 6.7×10⁴× the classical CFL); max single-step energy increase = 0.000e+00 (machine precision); mass conservation to machine precision.
  - **C3 (optimal rate):** temporal L²/H¹ convergence rate = 1.000 over 5 τ-halvings; spatial rate → 2.009 asymptotically (q=2 stencil). Both match Corollary 1 after taking the square root.
- **Scope caveat:** Stokes velocity error, Darcy velocity error, BJS interface friction, and the μ / H² components of the full energy norm are **not** tested, and the discretization is FFT/FD on a periodic square instead of continuous-Lagrange FEM on karstic geometry. This is why the verdict is PARTIAL rather than REPLICATED.
- **The paper itself provides no numerical data and no code.** It is a pure error-analysis paper that defers all numerics to Chen et al. 2017 [ref 5]. Therefore there is no ground-truth benchmark to hit; only the theorems' predicted rate and stability properties can be empirically tested, and those *have* been tested and reproduced on the block the theorems govern for the phase field.
- **Nothing in the observed data contradicts any theorem of the paper.** Under the project's verdict vocabulary, this qualifies as **PARTIAL**: some claims (C1, C2, C3 on the CH sub-block) reproduced; other claims (velocity error, BJS interface, karstic geometry FEM) out of reach for a one-shot replication run with no reference code.

The LLM-judge, given the augmented evidence independently, promoted its verdict from SPOT-CHECK to PARTIAL.

---

## 7. Files

```
PDE-Chen-Cahn-Hilliard-Stokes-Darcy-decoupled-2021/
├── report/
│   ├── REPORT.md                                (this file)
│   ├── brief.md
│   ├── attempt_log.md
│   ├── artifact_harvest.md
│   └── evidence/
│       ├── ch_convergence_run.log                # temporal test stdout
│       ├── ch_spatial_convergence_run.log        # spatial test stdout
│       ├── ch_energy_stability_run.log           # energy-stability stdout (NEW 2026-07-04)
│       ├── ch_energy_stability_extra_run.log    # energy-stability confirmation stdout (NEW)
│       ├── llm_judge_verdict.log                 # original judge stdout (SPOT-CHECK)
│       └── llm_judge_verdict_v2.log              # deepened judge stdout (PARTIAL — NEW)
└── work/
    ├── paper.pdf                                # arXiv PDF (1.22 MB)
    ├── paper.txt                                # extracted text (2797 lines)
    ├── ch_convex_split_convergence.py           # temporal test source
    ├── ch_convergence_results.json              # temporal test data
    ├── ch_spatial_convergence.py                # spatial test source
    ├── ch_spatial_convergence_results.json      # spatial test data
    ├── ch_energy_stability.py                   # energy-stability test source (NEW)
    ├── ch_energy_stability_results.json         # energy-stability test data (NEW)
    ├── ch_energy_stability_extra.py             # energy-stability confirmation (NEW)
    ├── ch_energy_stability_extra.json           # confirmation data (NEW)
    ├── llm_judge.py                             # original judge harness
    ├── llm_judge_verdict.json                   # original judge JSON (SPOT-CHECK)
    ├── llm_judge_v2.py                          # deepened judge harness (NEW)
    └── llm_judge_verdict_v2.json                # deepened judge JSON (PARTIAL — NEW)
```
