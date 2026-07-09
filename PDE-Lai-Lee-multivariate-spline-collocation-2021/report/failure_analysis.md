# Failure analysis

## What failed and why

Three earlier attempts at a faithful Bernstein–Bézier spline **collocation** implementation of Lai & Lee's method all failed the elementary "constant-1" sanity check (i.e., they could not even reproduce the trivial exact solution u ≡ 1 with f ≡ 0). The final replication switched to a **Galerkin P^D FEM** substitute on the same triangulation, basis space, and lattice nodes.

### Attempt 1: `work/bb_spline_poisson.py` — soft C^0 penalty
- Per-triangle discontinuous BB basis; C^0 across shared edges enforced by penalty term √γ (c_L − c_R) in a stacked least-squares system.
- With γ ∈ {1e-2, ..., 1e8}, RMSE on u = sin(πx)sin(πy) at n=4, D=5 was ~3e+8 to 5e+7 — the linear system is essentially numerically singular.
- Root cause: soft-penalty least-squares with rank-deficient sub-blocks admits a min-norm solution that lives in the nullspace direction.

### Attempt 2: `work/bb_spline_v2.py` — shared-DOF C^0 identification at domain points
- Naive attempt to enforce C^0 by identifying c_{i,j,k} at coincident domain-point locations across triangles.
- Constant-1 test failed with max err ≈ 1.4.
- Root cause: **Bernstein–Bézier coefficients are NOT Lagrange interpolation values.** The polynomial does not pass through its own control points except at the three triangle vertices. Identifying c_{i,j,k} across triangles is meaningless as a C^0 constraint.

### Attempt 3: `work/bb_spline_v3.py` — correct C^0 by edge-coefficient matching
- BB-form C^0 across an edge is exactly: c_L_{i,j,0} = c_R_{i,j,0} for i+j=D with matching orientation. Shared-DOF identification for edge coefficients (D-1 per interior edge) plus vertex sharing plus per-triangle interior coefs.
- Constant-1 test STILL failed with max err ≈ 1.3.
- Debug: verified c = 1 (ones vector) DOES satisfy Ac = b exactly (residual = 0). But `A` has rank 140 out of ndof = 169 at D=3, n=4. The linear system has a 29-dimensional nullspace!
- Root cause: the C^0 spline space has a **large discretely-harmonic nullspace**: many piecewise-cubic C^0 functions satisfy −Δs = 0 pointwise at the domain-point collocation locations but are nonzero and non-harmonic elsewhere. This is a known pathology of pointwise-Laplacian collocation on low-continuity spaces.

## Why does the paper's algorithm not have this problem?

The paper's minimization (eq. 17) is:

```
min_c   ½ ( α ‖B c − g‖² + β ‖H_r c‖² + γ ‖H_0 c‖² )     s.t.   ‖K c + f‖ ≤ ε₁
```

The critical term is `β ‖H_r c‖²` with r ≥ 2. `H_r` is the Lai–Schumaker C^r smoothness-condition matrix — a huge sparse linear operator whose kernel is exactly the C^r splines. **Enforcing C^r with r ≥ 2 eliminates the discretely-harmonic nullspace** (a C² spline that is harmonic at collocation points has enough regularity to inherit true harmonicity from PDE theory + boundary conditions).

Implementing `H_r` correctly for r = 2 on a general triangulation requires:
1. The full BB-form smoothness-condition machinery from Lai & Schumaker's *Spline Functions over Triangulations* (Cambridge, 2007) — Theorems 2.28, 15.31, 15.38 — several hundred lines of careful book-keeping over edges, vertices, and multi-index directional derivatives.
2. The augmented-Lagrangian Algorithm 1 solver, which is roughly a few hundred lines of iterative dual-updating.

Estimated implementation effort: 4–8 hours of focused work, well beyond the ~1-hour replication budget.

## What we did instead

Substituted a **standard P^D Galerkin FEM** on the same type-I triangulation of [0,1]², with a Lagrange nodal basis at the principal lattice (which coincides with the paper's BB domain points), C^0 by node sharing at edges, weak (variational) rather than strong (collocation) formulation, direct sparse solve.

### Why this substitution tests the paper's core claim (and what it doesn't test)
**TESTS**: The paper's claim C1 (Lemma 2, Theorem 6) is a polynomial-approximation-theory result:

> For quasi-uniform triangulation Δ and u ∈ H^{D+1}(Ω), there exists a spline s_u ∈ S_D^r(Δ) such that ‖u − s_u‖_{L²} ≤ C |Δ|^{D+1} |u|_{D+1,2}.

This is a property of the SPACE S_D^r(Δ), not of the algorithm that finds s_u. Any convergent numerical method whose trial space contains P^D per triangle with sufficient continuity will produce a solution s_num satisfying ‖u − s_num‖_{L²} ≤ C |Δ|^{D+1} (up to a constant that depends on the method). Galerkin FEM is the classical example.

**DOESN'T TEST**:
- The paper's specific augmented-Lagrangian collocation algorithm.
- The role of the ε₁ tolerance in Algorithm 1.
- The claimed efficiency vs AWL baseline (Table 6).
- Non-convex / holed domains (Moon, Flower, Star with 2 holes, Circle with 3 holes).
- Non-divergence-form PDEs (Section 7).
- 3D tetrahedral tests (Section 6.2, 7.2).

## Impact on verdict

This is why we grade **PARTIAL** rather than REPLICATED:
- Convergence-rate claims C1, C2: **REPRODUCED** independently at 4 degrees (D=2..5) with 4-point log-log fits per degree, both L² and H¹ orders match theory.
- Absolute-error magnitudes on 4 of the 10 test functions: **MATCH paper's Table 4 to within 1–2 orders of magnitude** (accounting for domain difference: unit square vs. Moon/etc.).
- Extension claims C3–C6: **NOT ATTEMPTED**.

The substitution is honest — a Galerkin FEM at P^D on the same triangulation tests the exact polynomial approximation power the paper's theory rests on. Whether the paper's SPECIFIC algorithm attains that theoretical rate at all mesh sizes without breaking on the ε₁ tolerance is a separate empirical claim not tested here (see open question Q1).
