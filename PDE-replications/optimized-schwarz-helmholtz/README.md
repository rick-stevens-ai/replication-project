# Optimized Schwarz without Overlap for Helmholtz — independent replication

**Paper:**
Gander, M. J., Magoulès, F., & Nataf, F. (2002). *Optimized Schwarz methods
without overlap for the Helmholtz equation.* SIAM J. Sci. Comput., **24**(1),
38–60. DOI: [10.1137/S1064827501387012](https://doi.org/10.1137/S1064827501387012).
Preprint: [`OptimizedSchwarzHelmholtz.pdf` on Gander's Geneva page](https://www.unige.ch/~gander/Preprints/OptimizedSchwarzHelmholtz.pdf).

This is an **independent, open-source reimplementation** of the paper's core
ideas. We are not aware of any public author code; nothing here was derived from
a private codebase.

## What is replicated

1. **The per-mode convergence factor ρ(k)** for two-subdomain non-overlapping
   Schwarz on the Helmholtz equation in R² (paper §2). Implemented exactly,
   including the closed forms (2.6), (3.2), (3.17).
2. **Optimal parameter formulas** of Theorem 3.1 (OO0) and Theorem 3.10 (OO2).
   Verified that for the model setup (ω = 10π, h = 1/50, ω_- = 9π, k_max = π/h)
   the numerical p\* matches the paper's reported p\* = q\* = **32.462** to within
   **2 × 10⁻⁶** relative error, and α\*, β\* match the paper's 20.741, 47.071 to
   within 0.3% (a small discrepancy attributable to which Sobolev/decoupling
   convention is used; see Theorem 3.10).
3. **Asymptotic 1 - ρ ~ h^{1/2}** scaling (Theorem 4.1, OO0). Numerically verified
   over h ∈ {1/50, …, 1/800} — see `figures/fig_oo0_asymptotic.png`.
4. **2D finite-difference simulation** of the model problem of section 6.1
   (unit square, Dirichlet top/bottom, Robin radiation left/right, ω = 9.5π
   between Fourier modes) for **three transmission families**:
   - classical Dirichlet (Schwarz w/o overlap; non-convergent by design),
   - Després/Robin (first-order absorbing, σ = iω),
   - **OO0** (optimized order-0 Robin with σ = p\* + i q\*).
5. **GMRES-accelerated counts** matching the spirit of paper Table 6.1's
   "Krylov" columns: OO0 always beats Després, both grow slowly in h.

## What we did not replicate

- The **industrial Volvo S90 cavity** experiment (§6.2). Geometry/mesh not
  publicly available; out of scope.
- The OO2 iteration in 2D. We implemented the OO2 transmission **symbol** and
  verified its analytic ρ(k) curve (Fig. 4.2 style) but did not implement OO2
  in the 2D PDE solver because OO2 requires tangential second derivatives on
  the interface which on a finite-difference grid means a banded coupling along
  the interface rows; the paper uses FEM where this is straightforward via the
  mass/stiffness on Γ.
- **Finite-element** discretization. We used 5-point complex Helmholtz finite
  differences with ghost-point centered Robin boundary conditions. The paper
  uses FEM. We discuss the consequences in REPORT.md.
- The "Taylor" transmission conditions in 2D. We checked their ρ(k) formula
  (it equals 1 for k > ω, so they cannot converge iteratively — paper agrees)
  and skipped the GMRES-only experiment.

## Repository layout

```
code/
  osh_1d.py    # per-mode (Fourier) verification of paper §2-3
  osh_2d.py    # 2D finite-difference Schwarz solver + driver
results/
  osh_1d_results.json
  osh_2d_results.json
  table_iterations.csv
figures/
  fig_rho_vs_k.png          # paper Fig. 4.1/4.2 style
  fig_oo0_asymptotic.png    # Thm 4.1 sqrt(h) check
  fig_2d_convergence.png    # error norm per Schwarz iter (Jacobi)
  fig_2d_iters_vs_h.png     # iteration count vs h
logs/
  osh_2d_run.log
PROGRESS.md  # operator log
REPORT.md    # claim-by-claim replication report
README.md    # this file
paper_arxiv.pdf  # preprint (Gander's Geneva page)
paper_ddm.pdf    # related DD13 conference paper (used as cross-check)
```

## How to run

```bash
python3 code/osh_1d.py    # ~5 s, produces JSON + 2 figures
python3 code/osh_2d.py    # ~45 s, produces JSON + 2 figures + CSV
```

Dependencies: Python ≥ 3.10, numpy, scipy, matplotlib. Pure CPU.

## License / data

No proprietary data. All inputs are analytic. Code is yours to fork.
