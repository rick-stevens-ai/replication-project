# Independent Replication — Anton, Cohen & Quer-Sardanyons (2017/2020): SEXP for the 1D Stochastic Heat Equation

**Paper.** R. Anton, D. Cohen, L. Quer-Sardanyons, *"A fully discrete approximation of the
one-dimensional stochastic heat equation."* arXiv:1711.08340 [math.NA] (22 Nov 2017); published
in *IMA Journal of Numerical Analysis* (priority-list DOI 10.1093/IMANUM/DRV006). Rank 30 on
`PDE_NEXT50_2026-06-26.tsv` (score 52.77, 90 citations).

**Set.** PDE-100 replication wave.
**Target dir.** `~/Dropbox/REPLICATE-PROJECT/PDE-Anton-Cohen-stochastic-heat-1D-2015/`
**Family.** Parabolic SPDE / stochastic PDE numerics (distinct from the wave's Allen-Cahn/SAV,
Burgers, Poisson, Helmholtz coverage; the pre-existing stochastic dirs are Burgers/Zhang-modal/
deepxde, none of which implement this FD + stochastic exponential integrator for the heat SPDE).

---

## 1. Paper summary

The paper studies an explicit fully-discrete scheme for the 1D stochastic heat equation with
multiplicative space-time white noise:

> ∂u/∂t = ∂²u/∂x² + f(t,x,u) + σ(t,x,u) · ∂²W/(∂t ∂x),  on (0,∞)×(0,1),
> u(t,0)=u(t,1)=0,  u(0,x)=u₀(x),

where W is a Brownian sheet. Space is discretized with the standard second-difference
operator (interior grid `x_m=m/M`, `m=1..M-1`, mesh `Δx=1/M`), giving the (M-1)-dim SDE system
`du^M = M²D u^M dt + f dt + √M σ dW^M`, with `D=tridiag(1,-2,1)` and `A:=M²D`. The eigenvalues
of `A` are `λ_j = -4M² sin²(jπ/2M)` with eigenvectors the discrete sine modes `φ_j(x)=√2 sin(jπx)`.

Time is discretized with an **explicit stochastic exponential integrator (SEXP)**, Eq. (15):

> **U^{n+1} = e^{A Δt} U^n + F(U^n) Δt + Σ(U^n) ΔW^n**

where `F(U)_m = f(U_m)`, `Σ(U)` is diagonal with entries `√M σ(U_m)`, and `ΔW^n` are the
(M-1)-dimensional Wiener increments over `[t_n,t_{n+1}]`.

**Main theoretical results.** The scheme has no CFL-type step-size restriction (the exponential
propagator handles the stiff linear part exactly). Under globally-Lipschitz `f,σ` the paper proves
`L^q(Ω)` convergence for all `q≥2`, improving the temporal rate from `1/8⁻` (implicit
Euler–Maruyama, ref. [21]) to `1/4⁻` (Thm 2.3), and almost-sure convergence (Thm 2.4). Under
non-globally-Lipschitz coefficients it proves convergence in probability (Thm 3.1).

**Numerical experiments (Sec 2.2.3).** Test problem: `u₀(x)=cos(π(x-1/2))` (=`sin(πx)`),
`f(u)=u/2`, `σ(u)=1-u`, `T=0.5`, `Δx=2⁻⁹` (M=512). SEXP compared with semi-implicit
Euler–Maruyama (SEM) and Crank–Nicolson–Maruyama (CNM). Time steps `Δt=2⁻¹..2⁻¹⁶`, reference
`Δt_ref=2⁻¹⁶`, expectations over `Ms=500` samples. Fig 1 (loglog) reports the error
`sup_{(t,x)∈[0,0.5]×[0,1]} E[|u^{M,N}(t,x)-u^M(t,x)|²]` and observes **convergence of order 1/2**
for SEXP (reference line slope 1/2). Fig 3 illustrates almost-sure convergence.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Result |
|----|-------|------|-----------|---------|--------|
| C1 | SEXP has no CFL restriction — stable for all Δt∈[2⁻¹,2⁻¹⁶] at M=512 | numerical/stability | yes | yes | **Confirmed**: max\|u\| bounded O(1) for every Δt |
| C2 | SEXP empirical temporal **strong convergence order ≈ 1/2** (Fig 1) | numerical/quantitative | yes | yes | **Confirmed**: measured RMS order **0.558** (500 samples, M=512) |
| C3 | Almost-sure / pathwise convergence (Thm 2.4, Fig 3) | theory + numerical | partially | yes | **Confirmed** numerically: every path converges, per-path order ~0.5 |
| C4 | (sanity) exponential integrator exact for linear part; FD 2nd-order in space | numerical | yes | yes | **Confirmed**: 5.5e-15 time-exactness; 2nd-order (rate 2.000) in dx |
| C5 | Improved temporal rate 1/4⁻ in L^q (Thm 2.3) vs 1/8⁻ of Euler–Maruyama | theory | proof-only | no | Out of scope (proof); the *empirical* Fig-1 order 1/2 is what we reproduce (C2) |

## 3. Method (numbered, reproducible)

Environment: local CherryRd (numpy 2.4.3, scipy 1.18.0) for validation + pilots; heavy Monte
Carlo on **uicgpu** (8×A100 host, 255 cores; numpy 1.23.5, scipy 1.10.1), 96 worker processes.
All LLM inference on free Argo proxy (localhost:44497). No paid endpoints, no `pdf` tool.

1. **Fetch OA artifact.** `curl https://arxiv.org/pdf/1711.08340v1` and `.../e-print/1711.08340v1`;
   `pdftotext -layout`; `tar xzf` the LaTeX source. (See `artifact_harvest.md`.)
2. **Implement SEXP from scratch** (`work/sexp_heat.py`). `A=M²D` is diagonalized by the discrete
   sine transform: `e^{AΔt}v = IDST( exp(λ Δt) · DST(v) )` using `scipy.fft.dst/idst` type-1,
   `norm='ortho'`. Verified this diagonalization is **exact** vs dense `scipy.linalg.expm`:
   max difference `3.3e-16` at M=16.
3. **Validate on the deterministic analytic case FIRST** (`work/validate_deterministic.py`,
   evidence `evidence/validate_deterministic.txt`):
   - Set σ=0, f=0. Then SEXP integrates `U'=AU` exactly; verified dt-independence
     (`max|u(Δt=2⁻⁴)-u(Δt=2⁻¹⁰)| = 5.5e-15`) and agreement with `e^{λ₁T}sin(πx)` (`1.7e-16`).
   - Convergence of the FD semidiscrete solution to the exact PDE solution
     `u(t,x)=exp(-π²t)sin(πx)`: max errors at T=2⁻⁴ for M=32..1024 give **rate 2.000** throughout
     (standard 2nd-order Laplacian). This validates the spatial operator and eigenstructure.
4. **Strong-convergence experiment** (`work/run_strong_order_mp.py`, uicgpu). Exact paper
   parameters: M=512 (Δx=2⁻⁹), `u₀=cos(π(x-1/2))`, `f(u)=u/2`, `σ(u)=1-u`, T=0.5, `Δt_ref=2⁻¹⁶`,
   coarse `Δt=2⁻³..2⁻¹⁰`, `Ms=500`. Coarse and fine share the SAME Brownian path via block-summing
   of the finest increments (Brownian-consistency), isolating the *temporal* error. Error metric =
   `sup_{(t,x)∈[0,0.5]×[0,1]} E[|u^{M,N}-u^M_ref|²]` (spatial sup via max over nodes; temporal sup
   over a snapshot grid; expectation via 500-sample Monte-Carlo mean). Command:
   `python3 run_strong_order_mp.py --M 512 --kref 16 --kcoarse 3 4 5 6 7 8 9 10 --samples 500 --procs 96`.
5. **Almost-sure/pathwise experiment** (`work/run_as_convergence.py`): 5 independent paths, M=512,
   `Δt_ref=2⁻¹⁵`; per-path sup-in-(t,x) error vs reference as Δt→0.
6. **Multi-judge scoring** (`work/run_judges.sh`): free Argo `gpt-5.2`, `gemini-2.5-pro`, `gpt-4.1`
   (opus avoided), each given the full quantitative summary and asked for a canonical verdict.

## 4. Results vs paper

### C4 — validation (analytic)
| Check | Metric | Result | Expected |
|---|---|---|---|
| SEXP linear part exact in time | `max\|u(2⁻⁴)-u(2⁻¹⁰)\|` | 5.5e-15 | ≈ round-off |
| SEXP vs `e^{λ₁T}sin(πx)` | max abs | 1.7e-16 | ≈ round-off |
| FD → analytic PDE, dx order | rate (M=32→1024) | 2.000, 2.000, 2.000, 2.000, 2.000 | 2 |

### C1 — stability / no CFL (M=512, single path, final max|u|)
| Δt | 2⁻¹ | 2⁻² | 2⁻⁴ | 2⁻⁶ | 2⁻⁸ | 2⁻¹⁰ | 2⁻¹² | 2⁻¹⁴ | 2⁻¹⁶ |
|----|----|----|----|----|----|----|----|----|----|
| max\|u\| | 1.48 | 1.98 | 0.79 | 0.41 | 0.23 | 0.095 | 0.077 | 0.047 | 0.039 |

Bounded O(1) for **all** step sizes → confirms the paper's headline "no CFL-type restriction."

### C2 — strong temporal convergence order (M=512, dt_ref=2⁻¹⁶, 500 samples, T=0.5)
| Δt | `E[sup\|·\|²]` | RMS = √(·) |
|----|------------|-----------|
| 2⁻³ | 2.575 | 1.605 |
| 2⁻⁴ | 1.121 | 1.059 |
| 2⁻⁵ | 0.487 | 0.698 |
| 2⁻⁶ | 0.218 | 0.467 |
| 2⁻⁷ | 0.101 | 0.318 |
| 2⁻⁸ | 0.048 | 0.219 |
| 2⁻⁹ | 0.0235 | 0.153 |
| 2⁻¹⁰ | 0.0115 | 0.107 |

- Slope of `E[sup|·|²]` vs Δt (log₂) = **1.115**.
- **Strong (RMS) order = 0.558** (paper: **1/2**). Each halving of Δt reduces RMS by ~2⁻⁰·⁵⁶,
  a clean, consistent 1/2-slope over 8 successive refinements.
- Evidence: `evidence/evidence_strong_order_full.json`.

### C3 — almost-sure / pathwise convergence (5 paths, M=512, dt_ref=2⁻¹⁵)
Per-path sup-in-(t,x) error decreases monotonically with Δt; fitted per-path slopes:
**0.568, 0.525, 0.562, 0.547, 0.535** → every realization converges as Δt→0 with order ≈1/2,
the numerical signature of Thm 2.4 / Fig 3. Evidence: `evidence/evidence_as_convergence.json`.

## 5. Internal-consistency finding (noise scaling)

A literal reading of the practical scheme Eq. (15) — `Σ=√M·σ` with `ΔW^n = W^M(t_{n+1})-W^M(t_n)`
and `W^M := √M·(W(t,x_{m+1})-W(t,x_m)) ~ N(0,Δt)` — applies the `√M` factor **twice**, giving a
net per-node noise amplitude `√M·σ·√Δt`. At M=512 this amplifies the noise by a factor M and the
**explicit** scheme blows up for `Δt > 2⁻¹⁰` (we measured `max|u| ~ 1e6..1e13`), directly
contradicting the paper's own "no CFL" claim and its Fig-1 x-axis range (`10⁻⁵..10⁰`) where the
error stays `≤ 0.1`.

The consistent interpretation is that the discrete increments `ΔW^n` are the space-time
white-noise **cell** increments `~ N(0, Δt·Δx) = N(0, Δt/M)`, so that the net per-node noise is
`√M·σ·√(Δt/M)·ξ = σ(u_m)·√Δt·ξ` — the standard, physically-correct FD discretization of white
noise, with the `√M` in `Σ` exactly canceling the `1/√M` in the cell increment. With this scaling
the scheme is CFL-free (C1) and reproduces the order-1/2 Fig-1 behavior (C2). This is a
presentation ambiguity in the paper, not a defect in the method; all three LLM judges considered
the reconciliation acceptable and standard.

## 6. Judge assessments (free Argo, non-opus)

| Judge | Verdict |
|---|---|
| argo:gpt-5.2 | **REPLICATED** ("good controls… strong-rate estimate consistent with ≈1/2… reconciliation acceptable; flag as reproducibility defect of the paper's presentation") |
| argo:gemini-2.5-pro | **REPLICATED** ("successful and rigorous… 0.558 a convincing match… reconciliation is a strength") |
| argo:gpt-4.1 | **REPLICATED** ("thorough, critical, matches all headline claims… noise-scaling reconciliation is not a concern") |

Full texts in `evidence/judge_*.txt`.

## 7. Files
- `work/sexp_heat.py` — SEXP solver (DST-diagonalized exponential integrator).
- `work/validate_deterministic.py` — analytic-case validation.
- `work/run_strong_order.py`, `work/run_strong_order_mp.py` — strong-order experiment (serial / MP).
- `work/run_as_convergence.py` — almost-sure/pathwise experiment.
- `work/run_judges.sh`, `work/judge_summary.txt` — multi-judge harness + prompt.
- `report/evidence/` — JSON/text outputs, judge responses, validation logs.
- `work/anton_cohen_2015.pdf`, `work/src/` — OA paper + LaTeX source.

## 8. Assessment

Every reproducible headline claim was independently confirmed with a from-scratch implementation:
the exponential integrator is exact for the linear part (validated to machine precision), the
spatial FD operator is exactly 2nd order, the scheme is CFL-free, and the temporal **strong
convergence order matches the paper's 1/2** (measured 0.558 over 500 samples at the paper's exact
parameters), with pathwise convergence also confirmed. The only theoretical claim not reproduced is
the proof-level `1/4⁻` L^q rate (Thm 2.3), which is analytical rather than a benchmarkable number;
the corresponding *empirical* Fig-1 order (1/2) is reproduced. One presentation-level noise-scaling
ambiguity was identified and reconciled without affecting the conclusions.

## Verdict
**Verdict:** REPLICATED
