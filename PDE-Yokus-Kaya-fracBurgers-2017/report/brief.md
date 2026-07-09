# Brief — Yokuş & Kaya (JNSA 2017) time-fractional Burgers'

**What**: Reproduce the exact and numerical solutions for the time-fractional Burgers' equation
`∂^α u/∂t^α + u ∂u/∂x = δ ∂²u/∂x²` (Caputo, 0<α≤1) from Yokuş & Kaya (JNSA 2017,
DOI 10.22436/JNSA.010.07.06). Paper derives an exact traveling-wave solution via a
`(1/G')`-expansion method + Cole-Hopf transformation, then compares against an FDM solver.

**Why**: Verify (C1) the closed-form exact solution actually solves the PDE, (C2) an
independent L1-Caputo + implicit tridiagonal scheme converges to that exact solution,
(C3) the paper's headline Table 1 and Table 2 error magnitudes are attainable.
