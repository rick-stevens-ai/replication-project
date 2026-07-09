# Workflow — PDE-Bernardi-Darcy-heat-spectral-2016

**Paper:** Bernardi, Maarouf, Yakoubi (2016), *Spectral discretization of Darcy's equations
coupled with the heat equation*, IMA J. Numer. Anal. — DOI 10.1093/imanum/drv047.
**Verdict:** REPLICATED.
**Type:** From-scratch reimplementation (no author code exists — paper used internal FreeFEM3D).

---

## Environment

- Host: CherryRd (macOS).
- Python 3.14.6, numpy 2.4.3, scipy 1.18.0, sympy 1.14.0, matplotlib.
- Light compute — local, no GPU.

## Directory layout

```
PDE-Bernardi-Darcy-heat-spectral-2016/
├── work/                             # code + primary artifacts
│   ├── spectral_gll.py               # GLL nodes / weights / differentiation matrix
│   ├── darcy_heat_solver.py          # coupled GLL-Galerkin solver + N-sweep driver
│   ├── verify_mms.py                 # strong-residual MMS consistency check (sympy)
│   ├── analyze.py                    # exponential-rate fits + convergence figure
│   ├── fig_solution.py               # exact-vs-discrete comparison (Fig. 2 replica)
│   ├── judge.py                      # LLM-judge harness (free Argo endpoints)
│   ├── paper.txt
│   └── bernardi_darcy_heat_2016.pdf
├── extraction/                       # PDF extraction (marker/nougat outputs)
└── report/
    ├── REPORT.md                     # source of truth
    ├── REPORT.tex                    # LaTeX render (this backfill)
    ├── open_questions.json           # 5 open questions (this backfill)
    ├── workflow.md                   # this file
    ├── artifacts_summary.md
    ├── failure_analysis.md
    └── evidence/
        ├── convergence.json
        ├── analysis_summary.json
        ├── convergence.png
        ├── solution_compare.png
        ├── convergence_sweep.txt
        ├── gll_selftest.txt
        ├── mms_residual_printed_sources.txt
        └── llm_judge_verdict.txt
```

## Steps (chronological, reproducible)

1. **Acquire paper.**
   OA preprint from HAL `hal-01085011`; MD5 = `2d6ead2ce797287b0718d8cc156a1ecd`, 23 pp.
   Saved to `work/bernardi_darcy_heat_2016.pdf`.

2. **Build GLL machinery from scratch.**
   ```bash
   python3 work/spectral_gll.py
   ```
   Computes GLL nodes as roots of `P_N'`, GLL quadrature weights, and closed-form differentiation
   matrix. Self-tests derivative accuracy (~1e-14) and exact quadrature of `x^2`.
   → `evidence/gll_selftest.txt`.

3. **MMS consistency check (symbolic).**
   ```bash
   python3 work/verify_mms.py
   ```
   Substitutes the paper's stated exact solution + printed source terms (eq. 5.6) into the strong
   Darcy–heat PDE using sympy. Finds `O(π)` residuals in Darcy-momentum and heat (∇·u = 0 holds).
   Symbolically pins the exact discrepancies (typo in printed forcings). Falls back to the
   analytically consistent MMS forcings `F = α(T_ex)u_ex + ∇p_ex`, `h = −ΔT_ex + (u_ex·∇)T_ex`
   for the subsequent convergence sweep.
   → `evidence/mms_residual_printed_sources.txt`.

4. **Convergence sweep.**
   ```bash
   python3 work/darcy_heat_solver.py
   ```
   Solves the coupled Darcy + heat system for N = 5..25 on Ω = (−1,1)²:
   - Tensor-product GLL grid (N+1)²; diagonal GLL mass.
   - Darcy: eliminate u pointwise from `α u = F − ∇p`; impose `(u,∇q)_N = 0` → symmetric weak
     system for p (mean-zero constraint via Lagrange multiplier); recover u pointwise.
   - Heat: GLL-Galerkin `(∇θ,∇φ)_N + ((u·∇)θ,φ)_N = (h,φ)_N` with Dirichlet MMS data.
   - Coupling: paper's decoupled fixed-point (5.1–5.3); iterate until residual < tol.
   → `evidence/convergence.json`, `evidence/convergence_sweep.txt`.

5. **Rate analysis + figure.**
   ```bash
   python3 work/analyze.py
   ```
   Fits `e^{−bN}` to each of L²(u), L²(p), L²(T), H¹(p), H¹(T) in the pre-floor window (N ≤ 14).
   → `evidence/analysis_summary.json`, `evidence/convergence.png`.

6. **Fig. 2 replica.**
   ```bash
   python3 work/fig_solution.py
   ```
   At N=17, plots exact vs discrete T side-by-side. `max|T−T_N| = 1.5e-14`.
   → `evidence/solution_compare.png`.

7. **LLM-judge verdict.**
   ```bash
   python3 work/judge.py
   ```
   Sends the replication artifacts to free Argo endpoints. Opus-4.8 returned proxy 502; per the
   wave-brief fallback, ran gpt-5.2 and claude-sonnet-4.5 instead — both returned **REPLICATED**.
   → `evidence/llm_judge_verdict.txt`.

## Time / cost

- Wall clock end-to-end: order of minutes for the full N=5..25 sweep on one CPU core.
- Compute cost: $0 (Argo endpoints are free; local Python only).

## Reproducibility notes

- The paper's eq. (5.6) source terms as printed are **inconsistent** — reproducing the paper's
  figures literally requires either deriving the correct source terms independently or reading
  the finding in `work/verify_mms.py`. See `failure_analysis.md` §1.
- No random seeds are used; all steps are deterministic to floating-point noise.
