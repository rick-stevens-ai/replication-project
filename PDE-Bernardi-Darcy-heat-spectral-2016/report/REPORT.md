# Independent Replication Report

**Paper:** C. Bernardi, S. Maarouf, D. Yakoubi (2016), *"Spectral discretization of Darcy's
equations coupled with the heat equation"*, IMA Journal of Numerical Analysis.
DOI: [10.1093/IMANUM/DRV047](https://doi.org/10.1093/imanum/drv047).
OA (green) preprint: HAL `hal-01085011`.

**Set:** PDE-100 · **Type:** Numerical PDE (spectral method) · **Date:** 2026-07-01
**Verdict:** **REPLICATED**

---

## 1. Paper summary

The authors study the temperature distribution of a fluid flowing through a porous medium,
modeled by **Darcy's law coupled with the heat equation** under the Boussinesq / quasi-stationary
approximation, with a nonlinear buoyancy source F(T) representing heat production from an
exothermic reaction. On a bounded domain Ω (the square/cube (−1,1)^d):

```
  α u + ∇p = F(T)                 in Ω
  ∇·u = 0                         in Ω
  −λ ΔT + (u·∇)T = h              in Ω
```
with u·n = 0 on ∂Ω, T = T_⋆ on Γ_⋆, ∂T/∂n = θ_♯ on Γ_♯.

Contributions: (i) existence/uniqueness of a weak solution; (ii) a **Legendre–Gauss–Lobatto
(GLL) spectral P_N×P_N×P_N Galerkin discretization with numerical integration** (Sec. 3);
(iii) an **optimal a priori error estimate** (Thm 4.7, eq. 4.16) of the form
‖u−u_N‖ + ‖p−p_N‖_{H¹} + ‖θ−θ_N‖_{H¹} ≤ c N^{d/6−s}‖u‖_{H^s} + c N^{−s}(‖p‖_{H^{s+1}}+‖θ‖_{H^{s+1}}) + …,
i.e. the error decays faster than any algebraic power of N for smooth (analytic) solutions —
**spectral convergence**; (iv) a decoupled **fixed-point iteration** (5.1–5.3) with a proven
contraction (Thm 5.1); (v) numerical experiments (Sec. 5), run in FreeFEM3D.

### Accuracy test (Sec. 5.2, eq. 5.6) — the reproducible core
Manufactured analytic solution on Ω = (−1,1)²:
- u₁ = −sin(πx)cos(πy), u₂ = cos(πx)sin(πy)
- p = −sin(πx)cos(πy),  T = (1/π²) cos(πx)sin(πy)
- temperature-dependent permeability α(x,y) = 1/(T²+1) (interpolated, I_N α); λ = 1.

**Claimed result (Fig. 1):** the L²-norm errors of velocity/pressure/temperature and the
H¹-norm errors of pressure/temperature between numerical and exact solution decay **spectrally**
as the polynomial degree runs N = 5 → 25, confirming estimate (4.16). *"We observe that beyond
degree 20, the leading error is due to the accuracy of the machine, so that the curve stops
decreasing."* **Fig. 2:** exact vs discrete solution at N = 17 cannot be distinguished.

---

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Outcome |
|----|-------|------|-----------|---------|---------|
| C1 | L² errors of u, p, T decay **spectrally** (exponentially in N) on the accuracy test | numerical | yes | yes | **Reproduced** — exp fit e^{−bN}, b≈1.9–2.2, ~7–9×/N reduction |
| C2 | H¹ errors of p, T decay spectrally | numerical | yes | yes | **Reproduced** — b≈2.0–2.05 |
| C3 | Beyond N≈20 the error floors at machine precision | numerical | yes | yes | **Reproduced** — floor at N≈16–18, O(1e-14…1e-16) |
| C4 | Exact vs discrete solution indistinguishable at N=17 (Fig. 2) | numerical | yes | yes | **Reproduced** — max\|T−T_N\| = 1.5e-14 |
| C5 | Decoupled fixed-point scheme (5.1–5.3) converges (Thm 5.1) | numerical/analytic | yes | yes | **Reproduced** — iteration count 4→1 as N grows; contraction |
| C6 | Optimal a priori estimate (4.16), error ~N^{−s} | analytic (proof) | partially | indirectly | Consistent — observed decay ⇒ optimal/spectral; proof not re-derived |
| C7 | Existence/uniqueness of continuous & discrete solution | analytic (proof) | no (theory) | no | Out of scope for numerical replication |
| C8 | Horton–Rogers–Lapwood physical case (Sec. 5.3, Figs 3–5) | numerical (physics) | yes | no | Not attempted (secondary demo; no error metric / no manufactured solution) |

---

## 3. Method (independent, from scratch)

**Data source.** OA preprint PDF from HAL `hal-01085011` (MD5 `2d6ead2ce797287b0718d8cc156a1ecd`,
23 pp). No public author code exists (paper used internal FreeFEM3D spectral code), so this is a
**from-scratch reimplementation**, not a rerun.

**Tools/versions.** Python 3.14.6, numpy 2.4.3, scipy 1.18.0, sympy 1.14.0, matplotlib. macOS
(CherryRd). Light compute — run locally (no GPU needed).

**Steps (commands):**
1. `python3 work/spectral_gll.py` — self-written GLL nodes (roots of P_N'), GLL quadrature
   weights, and closed-form GLL differentiation matrix. Self-test: max derivative error ~1e-14,
   quadrature of x² exact ⇒ machine-precision GLL operators. (evidence/gll_selftest.txt)
2. `python3 work/verify_mms.py` — manufactured-solution consistency check (see §5, Finding).
3. `python3 work/darcy_heat_solver.py` — coupled GLL-Galerkin solve, sweep N = 5..25 →
   `convergence.json`. (evidence/convergence_sweep.txt)
4. `python3 work/analyze.py` — exponential-rate fits + `convergence.png`. (analysis_summary.json)
5. `python3 work/fig_solution.py` — exact vs discrete T at N=17 → `solution_compare.png`.
6. `python3 work/judge.py` — LLM-judge verdict on free Argo endpoints.

**Discretization details (faithful to Sec. 3).**
- Tensor-product GLL grid (N+1)² on (−1,1)²; discrete inner product (·,·)_N = diagonal GLL mass
  (weights ρ_iρ_j) — matches the paper's numerical-integration Galerkin (eq. 3.5, 3.7).
- **Darcy block:** with the diagonal GLL mass, the velocity is eliminated pointwise from the
  first equation, α u = F − ∇p ⇒ u = (F − ∇p)/α; imposing the weak constraint (u,∇q)_N = 0 gives
  a symmetric mean-zero weak-Darcy system for p (Neumann/constant nullspace pinned by a Lagrange
  multiplier), then u is recovered pointwise.
- **Heat block:** GLL-Galerkin (∇θ,∇φ)_N + ((u·∇)θ,φ)_N = (h,φ)_N with Dirichlet data from the
  manufactured solution.
- **Coupling:** the paper's decoupled fixed-point scheme (5.1–5.3): given θ^{n−1}, solve Darcy
  with permeability α(θ^{n−1}); then solve heat with u^n. The permeability and convection are
  re-evaluated at the current iterate; the manufactured RHS data are fixed so the exact triplet
  is the fixed point.
- **Norms:** L²(f)=√((f,f)_N); H¹(f)=√(‖f‖²_{L²}+‖∇f‖²_{L²}) with spectral gradients.

---

## 4. Results vs paper

### Convergence (accuracy test, N = 5..25) — reproduces Fig. 1

| N | L²(u) | L²(p) | L²(T) | H¹(p) | H¹(T) | fp iters |
|---|-------|-------|-------|-------|-------|----------|
| 5 | 4.44e-01 | 2.00e-02 | 1.80e-03 | 1.31e-01 | 1.12e-02 | 4 |
| 8 | 5.70e-03 | 1.60e-04 | 1.04e-05 | 1.47e-03 | 7.96e-05 | 4 |
| 11| 2.35e-05 | 3.23e-07 | 1.68e-08 | 4.08e-06 | 2.02e-07 | 3 |
| 14| 4.34e-08 | 4.31e-10 | 2.21e-11 | 6.85e-09 | 3.22e-10 | 2 |
| 17| 4.21e-11 | 2.58e-13 | 1.24e-14 | 5.00e-12 | 2.26e-13 | 1 |
| 20| 3.50e-14 | 4.94e-15 | 2.84e-16 | 2.62e-14 | 5.39e-15 | 1 |
| 25| 4.30e-14 | 1.60e-14 | 3.66e-16 | 4.77e-14 | 8.02e-15 | 1 |

(full table in `evidence/convergence.json`; figure `evidence/convergence.png`.)

**Interpretation:**
- **Exponential (spectral) decay** — average error reduction of **~7–9× per unit increase in N**
  in the pre-floor window (fitted rates e^{−bN}, b ≈ 1.94 [L²(u)], 2.11 [L²(p)], 2.15 [L²(T)],
  2.02 [H¹(p)], 2.05 [H¹(T)]). Straight lines on a semilog axis = spectral convergence. ✅ **C1, C2**
- **Machine-precision floor** — errors stop decreasing around **N ≈ 16–18** and stagnate at
  O(1e-14) for u/p and O(1e-16) for T, in direct agreement with the paper's statement that
  "beyond degree 20 the leading error is due to the accuracy of the machine." ✅ **C3**
- **Fixed-point convergence** — iteration count decreases 4 → 1 as N increases (the contraction
  in Thm 5.1; smoother/better-resolved iterates converge faster). ✅ **C5**

### Exact vs discrete solution (Fig. 2)
At N = 17, max pointwise |T − T_N| = **1.5e-14** ⇒ exact and spectral solutions are
indistinguishable, reproducing Fig. 2. (`evidence/solution_compare.png`) ✅ **C4**

**Magnitude comparison.** The paper reports only log-scale figures (no numeric error table), so a
number-for-number match is not possible; but the *qualitative and structural* claims — spectral
rate, all five norms decaying, and the machine-precision plateau near N≈20 — are reproduced
exactly, and the plateau magnitudes (~1e-14…1e-16) are what double-precision GLL spectral methods
attain on analytic solutions.

---

## 5. Finding: typo in the printed source terms (eq. 5.6)

Plugging the paper's stated exact solution **and printed source terms** (5.6) into the strong-form
PDE (at N=30 with spectral derivatives) leaves residuals of **O(π)** for the Darcy-momentum and
heat equations (only ∇·u=0 is satisfied). `sympy` pins the discrepancies exactly:
F1_paper − F1_required = (π−1)cos(πx)cos(πy), F2_paper − F2_required = (1−π)sin(πx)sin(πy),
h_paper − h_required = (2π²−1)(2πcos(πx)+cos(πy))sin(πy)/π. These are **transcription typos** in the
printed forcing terms (a common error; they omit/rescale the 1/π² factor in T inside the buoyancy
and mis-scale the diffusion term). This does **not** affect the paper's central claim — the numerical
experiment tests the *discretization's convergence for a smooth solution*. We used the analytically
**consistent** manufactured sources F = α(T_ex)u_ex + ∇p_ex and h = −ΔT_ex + (u_ex·∇)T_ex, for which
the stated exact triplet is the true solution, and recovered the paper's spectral-convergence story.
(evidence/mms_residual_printed_sources.txt)

---

## 6. LLM-judge verdict (free endpoints)

Argo opus-4.8 returned a proxy 502; per the wave-brief fallback rule we used two other free Argo
models. Both returned **REPLICATED** independently:
- **Argo gpt-5.2:** "verdict: REPLICATED … reproduces the paper's central numerical claims …
  spectral decay, machine-precision floor, N=17 indistinguishability, convergent fixed point …
  the source-term typo … does not [affect] the central numerical claim."
- **Argo claude-sonnet-4.5:** "verdict: REPLICATED, agreement: quantitative, coverage: complete …
  This is a paper typo, not a methodological discrepancy."

(Full JSON: `evidence/llm_judge_verdict.txt`.)

---

## 7. Verdict & justification

### **REPLICATED**

An independent, from-scratch Legendre-GLL spectral solver for the coupled Darcy+heat system
reproduces every reproducible central numerical claim of the paper's accuracy test (Sec. 5.2,
Figs 1–2): **spectral (exponential) convergence** of the L²(u,p,T) and H¹(p,T) errors, the
**machine-precision floor near N≈20**, the **indistinguishable** exact/discrete solution at N=17,
and the **convergent decoupled fixed-point** iteration (Thm 5.1). The observed decay is fully
consistent with the paper's optimal a priori estimate (4.16). The only wrinkle — the printed
source terms in eq. (5.6) are typo'd — was diagnosed with an independent symbolic check and does
not touch the substance of the paper; the consistent manufactured sources reproduce the result.
Two independent free LLM judges concur (REPLICATED, complete coverage). The proof-based claims
(existence/uniqueness, the estimate's derivation) and the secondary Horton–Rogers–Lapwood physics
demo were out of scope for numerical replication.

---

## 8. Files
- `work/spectral_gll.py` — GLL nodes/weights/differentiation (self-tested to machine precision)
- `work/darcy_heat_solver.py` — coupled GLL-Galerkin Darcy+heat solver + convergence sweep
- `work/verify_mms.py` — manufactured-solution strong-residual consistency check
- `work/analyze.py` — exponential-rate fits + figure
- `work/fig_solution.py` — exact-vs-discrete comparison (Fig. 2)
- `work/judge.py` — LLM-judge harness (free Argo endpoints)
- `work/paper.txt`, `work/bernardi_darcy_heat_2016.pdf` — source paper
- `report/evidence/` — convergence.json, analysis_summary.json, convergence.png,
  solution_compare.png, convergence_sweep.txt, gll_selftest.txt,
  mms_residual_printed_sources.txt, llm_judge_verdict.txt
