# Brief

**Paper:** Ming-Jun Lai & Jinsil Lee, *A Multivariate Spline based Collocation Method for
Numerical Solution of Partial Differential Equations*, arXiv:2109.09698v4 (SIAM J. Sci.
Comput., 2023; DOI 10.1137/22M1469602). PDE-100 rank 24.

**What/why:** The paper proposes a collocation method using multivariate Bernstein–Bézier
(BB) polynomial splines of degree `D`, smoothness `C^r`, over a triangulation, with the BB
"domain points" as collocation points and `C^r` continuity enforced as linear constraints
`Hc = 0`. Its headline claim (Table 4) is that for the Poisson equation `-Δu = f` with
Dirichlet BC, smooth exact solutions are recovered to **near machine precision**
(RMSE ~1e-11…1e-12) using `D=8`, `r=2`. We independently re-implemented the method from
scratch (numpy/scipy only) — BB basis + derivatives, domain points, the `C^2` smoothness
matrix, and the equality-constrained least-squares solve — and reproduced the near-machine-
precision accuracy and high-order convergence on the paper's own analytic test functions.
