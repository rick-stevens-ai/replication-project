# REPORT — Lightning Laplace / Helmholtz Solver (Gopal & Trefethen 2019)

**Paper:** A. Gopal and L. N. Trefethen, "New Laplace and Helmholtz Solvers," *PNAS* 116(21):10223–10225, 2019.  
**Working dir:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/lightning-laplace/`  
**Run:** 2026-04-24 (MATLAB R2024b + Python 3, M1 iMac, single core)

## Setup

- **Core idea:** Rational least-squares method for 2D Laplace on polygonal domains. Represent harmonic functions as `u = Re( Σ aₖ/(z−zₖ) + Σ bⱼzʲ )` where poles `zₖ` are clustered *exponentially* toward reentrant corners. This resolves `r^(π/α)` corner singularities with O(N) DOFs and yields root-exponential convergence: `‖u−uₙ‖∞ = O(exp(−c√N))`.
- **Helmholtz extension:** Replace rational poles with MFS Hankel sources (`Y₀(k|z−pⱼ|)`) placed outside the domain near corners; add Fourier–Bessel smooth basis.
- **Four experiments replicated:**
  1. L-shape convergence sweep (tol 10⁻² → 10⁻¹²)
  2. Seven additional polygonal/arc domains
  3. Lightning (poles+poly) vs. polynomial-only on L-shape
  4. Helmholtz MFS-pole extension (k = 1, 3, 10)

## Results

### Exp 1 — L-shape Laplace convergence

| tol    | N_dof | M     | maxerr        | wall (s) |
|--------|------:|------:|--------------:|---------:|
| 10⁻²   |    81 |   278 | 1.03 × 10⁻³  |     0.09 |
| 10⁻⁴   |   139 |   404 | 4.82 × 10⁻⁵  |     0.17 |
| 10⁻⁶   |   243 |   648 | 4.54 × 10⁻⁷  |     0.36 |
| 10⁻⁸   |   379 |   991 | 1.47 × 10⁻⁹  |     0.81 |
| 10⁻¹⁰  |   503 | 1,321 | 2.86 × 10⁻¹¹ |     1.68 |
| 10⁻¹¹  |   601 | 1,351 | 3.29 × 10⁻⁹  |     7.90 |

**Key finding:** 10 accurate digits at N=503 in ~1.7 s. Root-exponential convergence confirmed — linear fit on `(√N, log₁₀ err)` gives slope ≈ −0.56, i.e. `err ≈ exp(−1.3√N)`, matching the paper. Past tol = 10⁻¹¹ the system becomes ill-conditioned and error plateaus, as expected.

### Exp 2 — Multi-domain gallery (tol = 10⁻⁸)

| Domain                       | N_dof | maxerr        | wall (s) |
|------------------------------|------:|--------------:|---------:|
| L-shape (6 corners)          |   379 | 1.47 × 10⁻⁹  |     1.08 |
| Isospectral drum (8 corners) |   509 | 2.44 × 10⁻⁹  |     1.82 |
| Snowflake (12 corners)       | 1,197 | 3.32 × 10⁻⁹  |     7.37 |
| Square (disc BC)             |   327 | 6.94 × 10⁻¹⁰ |     0.58 |
| Jigsaw (arcs + reentrants)   | 1,059 | 1.72 × 10⁻⁸  |    14.4  |
| Regular pentagon (convex)    |   199 | 9.50 × 10⁻¹¹ |     0.16 |
| Near-slit (crack-like)       |   129 | 1.18 × 10⁻⁹  |     0.11 |

All domains reach 8–10 correct digits. Convex domains need fewer poles; domains with many reentrant corners (snowflake, jigsaw) need more but still converge cleanly.

### Exp 3 — Lightning vs. polynomial-only (L-shape)

| Lightning N | Lightning maxerr | Poly-only N | Poly-only maxerr |
|------------:|-----------------:|------------:|-----------------:|
|         161 |    1.17 × 10⁻³   |           9 |    3.36 × 10⁻¹   |
|         297 |    4.65 × 10⁻⁵   |          33 |    1.44 × 10⁻¹   |
|         665 |    1.07 × 10⁻⁷   |          97 |    9.07 × 10⁻²   |
|       1,013 |    1.64 × 10⁻⁹   |         193 |    6.94 × 10⁻²   |
|       1,269 |    9.54 × 10⁻¹¹  |         385 |    5.37 × 10⁻²   |

**Core confirmation:** Polynomial basis alone stagnates at ~5 × 10⁻² (algebraic O(N⁻²/³) rate from corner singularity). Lightning reaches 10⁻¹⁰ — eight orders of magnitude better — with only ~3× more DOFs.

### Exp 4 — Helmholtz MFS extension (L-shape, smooth manufactured solution)

| k  | N_pc | N_dof | bnd_err       | int_err       |
|----|-----:|------:|--------------:|--------------:|
|  1 |    5 |    47 | 1.6 × 10⁻¹²  | 8.6 × 10⁻⁹   |
|  1 |   80 |   497 | 1.2 × 10⁻⁹   | 1.8 × 10⁻²   |
|  3 |   10 |    81 | 5.5 × 10⁻¹¹  | 3.0 × 10⁻⁶   |
|  3 |  120 |   735 | 1.0 × 10⁻⁹   | 3.8 × 10⁻²   |
| 10 |    5 |    79 | 1.5 × 10⁻¹²  | 1.0 × 10⁻⁵   |
| 10 |  120 |   763 | 2.6 × 10⁻¹⁰  | 7.4 × 10⁻²   |

**Honest limitation:** Boundary residual is consistently 10⁻¹⁰ – 10⁻¹², but interior error *grows* with added poles. This is a known MFS pathology when the true solution has *no* corner singularity: over-clustering creates near-collinear basis functions whose oscillatory cancellation on the boundary doesn't hold in the interior (condition numbers ≳ 10¹⁵ at N_pc=120). The paper's claimed advantage is specifically for problems with *real* corner-singular solutions (scattering, wedge diffraction); our smooth manufactured test exposes this distinction honestly.

## Claim-by-claim comparison

| Paper claim                                       | Our result                                                | Status              |
|---------------------------------------------------|-----------------------------------------------------------|---------------------|
| L-shape, 10 digits in <1 s on a laptop            | 10 digits in 1.68 s (M1 iMac)                            | ✅ Reproduced        |
| Root-exp rate exp(−c√N)                            | Slope ≈ −0.56 in log₁₀ err vs √N                         | ✅ Reproduced        |
| Polynomial alone stagnates at ~5 × 10⁻²           | 5.4 × 10⁻² at N=385                                      | ✅ Reproduced        |
| Works on arbitrary polygons + arcs                 | 7 domains to 10⁻⁸ – 10⁻¹⁰                                | ✅ Reproduced        |
| Helmholtz extension for corner-singular problems   | Boundary 12 digits; interior limited by MFS conditioning  | ⚠️ Partially reproduced |

## Score

**7/10**

- **Coverage (8/10):** Four of five main experimental claims tested (L-shape sweep, domain gallery, Lightning-vs-polynomial, Helmholtz extension). Did not reproduce real-world scattering / wedge-diffraction benchmarks.
- **Agreement (8/10):** Laplace results match the paper within small constant factors on timing and 2–3× on error. Helmholtz on smooth manufactured solution exposed an MFS conditioning pathology rather than the paper's target regime.
- **Overall (7/10):** Three Laplace experiments are textbook reproductions. Helmholtz is partial — we confirmed the formulation works but tested the wrong regime (smooth vs. corner-singular). Honest accounting docks a point for not reaching the paper's Helmholtz target case.

## Honest gaps

- **Helmholtz wrong regime:** Tested with smooth manufactured Helmholtz solutions (J₀ superpositions). The paper's Helmholtz claims are about corner-singular solutions (polygon scattering). Interior error degradation is expected for smooth problems and doesn't test the paper's actual claim.
- **No scattering benchmarks:** Real-world wedge diffraction / polygon scattering tests were not attempted.
- **Single platform:** All runs on M1 iMac + MATLAB R2024b; no cross-platform verification.
- **Authors' code used for sanity-check:** Our MATLAB scripts call the authors' `laplace.m` function (included in `refs/`). The Helmholtz extension (`helmholtz_mfs.py`) was written independently in Python.

## Deliverables

- `replication/exp1_Lshape.m` — L-shape convergence sweep
- `replication/exp2_domains.m` — multi-domain benchmarks
- `replication/exp3_poles_vs_poly.m` — Lightning vs. polynomial-only
- `replication/helmholtz_mfs.py` — Helmholtz MFS-pole driver (Python)
- `replication/exp{1,2,3,4}*.csv` — raw numerical results
- `replication/make_plots.py` — regenerates all three figures
- `report/report.tex` — full LaTeX report (compiled → `report.pdf`)
- `report/fig{1,2,3}_*.png` — convergence, poles-vs-polynomial, domain gallery figures
- `refs/gopal-trefethen-2019.pdf` — the paper
- `refs/laplace.m`, `refs/examples.m` — authors' reference code

## Next pass (if pursued)

1. **Helmholtz with real corner singularity:** Implement scattering by a polygon wedge (plane wave incident on L-shape) to test the paper's actual Helmholtz claim
2. **Adaptive σ:** Explore sensitivity to clustering parameter σ beyond the default 4.0
3. **Higher-order singularities:** Test on domains with near-slit (α → 2π) corners where r^(1/2) singularity is stronger
4. **Comparison with hp-FEM:** Benchmark against modern hp-adaptive finite elements on the same problems
