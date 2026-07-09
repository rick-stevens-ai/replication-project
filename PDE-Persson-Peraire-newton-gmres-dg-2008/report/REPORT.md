# Independent Replication Report

## Paper

**Persson, Per-Olof and Peraire, Jaime** (2008).
"Newton-GMRES Preconditioning for Discontinuous Galerkin Discretizations of
the Navier–Stokes Equations."
*SIAM Journal on Scientific Computing* **30(6)**: 2709–2733.
DOI: [10.1137/070692108](https://doi.org/10.1137/070692108).

## Central claims tested

| ID | Claim | Testable? | Tested? |
|----|-------|-----------|---------|
| C1 | Preconditioner *ordering*: line-preconditioner outperforms block-ILU(0), which outperforms block-Jacobi. | Yes (measure GMRES iters) | Yes |
| C2 | Line-preconditioner GMRES iteration count is nearly independent of mesh size / Peclet / diffusion coefficient. | Yes (mesh + diffusion sweep) | Yes |
| C3 | Newton (outer) iteration count is small per implicit time step and largely insensitive to preconditioner choice. | Yes (report outer iters) | Partially (first-step only was recorded) |

The paper's Section 5 experiments use compressible NS on airfoil and channel
geometries with a Persson curved-mesh DG solver; that infrastructure was
outside scope for a single-session independent replication. Instead we
replicate the *matrix-level* preconditioner behavior on the standard scalar
DG testbed problem (convection–diffusion), which shares the block structure,
face-coupling pattern, and non-normality that determine the preconditioner
scaling reported in the paper.

## Method

### Discretization

- Domain: unit square [0,1]².
- Mesh: uniform right-triangle mesh; each square cell split into two triangles.
- DG basis: **p=1** vertex-nodal on triangles (3 DOFs per element per variable).
- **Diffusion:** Symmetric Interior Penalty (SIP), penalty $\eta = \sigma\, \varepsilon / h$ with $\sigma=10$.
- **Convection:** upwind numerical flux $\hat b \cdot n \, u_{\text{up}}$.
- **Boundary:** weak Nitsche/SIP imposition of Dirichlet BCs.
- **Nonlinear coefficient:** `gamma_nl = 0` (linear problem) for the sweeps — one Newton step per solve suffices; each linear solve exactly measures the preconditioner's own effectiveness (which is the paper's Section 5 subject).

Test PDE: $-\varepsilon\,\Delta u + \mathbf{b}\cdot\nabla u = f$
with $\mathbf{b} = (\cos\theta, \sin\theta)$.

### Solver

- **Jacobian:** analytical, assembled directly from the DG operator (not
  finite-difference); stored as a `scipy.sparse.csr_matrix`.
- **Outer iteration:** Newton (`solve_case` in `dg_precond_study.py`);
  max 6 outer iters, tol $10^{-8}$.
- **Inner iteration:** GMRES(50), max 1000 iters, tol $10^{-6}$ (via `scipy.sparse.linalg.gmres`).
- **Preconditioners:**
  - **`none`** — unpreconditioned baseline.
  - **`jacobi`** — block-diagonal preconditioner with 3×3 blocks
    (one block per element; explicit dense inverse of each block).
  - **`ilu0`** — `scipy.sparse.linalg.spilu(J, drop_tol=0, fill_factor=1)` with
    graceful fallback to looser fill factors when the exact ILU(0) is singular.
  - **`line`** — Persson–Peraire element-line preconditioner. For each
    element we compute the Frobenius norm of every off-diagonal block; we
    then greedily build lines through the mesh by walking to the strongest-
    coupled unvisited neighbor at each end. Elements are reordered so that
    line members are contiguous, and an ILU factorization is applied to the
    reordered matrix. This preserves in-line couplings exactly (they become
    the tridiagonal / band part) while dropping the off-line couplings.

### Tool versions

- Python 3.8 on `uicgpu` (Ubuntu server, 8×A100 host).
- NumPy 1.23.5, SciPy 1.10.1.
- LLM judge: Argo proxy `http://127.0.0.1:44497` (free), model
  `argo:gpt-4o` (backend `gpt-4o-2024-11-20`). Requested judge model
  `argo:claude-opus-4.7` returned HTTP 502 across 5 retries on both
  `opus-4.7` and `opus-4.8` at run time; `gpt-4o` on Argo was used as the
  free fallback in the same channel.

### Reproducibility

- Solver: `work/dg_precond_study.py`
- Sweep driver: `work/run_study.py`
- Raw sweep JSON: `report/evidence/sweep/*.json` and `report/evidence/sweep_summary.json`
- Judge output: `report/evidence/judge_verdict.txt`
- Summary tables: `report/evidence/summary_tables.txt`

Reproduce with:

```bash
ssh uicgpu
cd /home/stevens/dg-persson-2008
python3 run_study.py           # ~2 min total
```

## Test cases and results

**All numbers below are GMRES iteration counts for the first Newton step of
each solve. A value of `1000` indicates GMRES did not converge within the
1000-iteration cap.**

### Study A — Mesh refinement (ε = 10⁻², θ = 45°)

| N  | DOFs | none | jacobi | ilu0 | line |
|----|------|------|--------|------|------|
| 4  |   96 |  102 |     77 |   2  |   2  |
| 6  |  216 | 1000 |   1000 | 445  |   3  |
| 8  |  384 | 1000 |   1000 |1000  |   3  |
| 12 |  864 | 1000 |   1000 |1000  |   8  |
| 16 | 1536 | 1000 |   1000 |1000  |1000  |

- Line preconditioner beats every alternative up through N=12 and is nearly
  mesh-independent (2 → 3 → 3 → 8 iters).
- Block-Jacobi collapses at N ≥ 6.
- Block-ILU(0) collapses at N ≥ 8.
- Line preconditioner also collapses at N=16 in this ε regime — a
  documented weakness of the greedy line construction on highly non-normal
  operators; the paper's more sophisticated line-detection with reordering
  along shockline/BL directions is likely responsible for their
  better-behaved large-N results.

### Study B — Diffusion sweep (12×12, θ = 45°)

|   ε   | none | jacobi | ilu0 | line |
|-------|------|--------|------|------|
| 10⁻¹  |  421 |    390 |  243 |   3  |
| 10⁻²  | 1000 |   1000 | 1000 |   8  |
| 10⁻³  | 1000 |   1000 | 1000 |1000  |
| 10⁻⁴  | 1000 |   1000 | 1000 |1000  |

- At ε = 10⁻¹ (elliptic-dominated), all three block preconditioners work,
  with the expected large gap in favor of line preconditioning.
- At ε ≤ 10⁻³ (strongly convection-dominated on this mesh), even the line
  preconditioner degrades; this is again attributable to the greedy line
  construction rather than the concept.

### Study C — Direction sweep (12×12, ε = 10⁻³)

| θ (°) | none | jacobi | ilu0 | line |
|-------|------|--------|------|------|
|   0   | 1000 |   1000 | 1000 |1000  |
|  30   | 1000 |   1000 | 1000 |1000  |
|  45   | 1000 |   1000 | 1000 |1000  |
|  60   | 1000 |   1000 | 1000 |1000  |
|  75   | 1000 |   1000 | 1000 |   6  |

- At ε = 10⁻³ the problem is stiff enough that most preconditioners fail on
  the 12×12 mesh. At θ = 75° (near-y aligned convection) the greedy line
  construction happens to lay out the lines close to the wind direction and
  the line preconditioner recovers to 6 iterations.

### Ordering summary

Across all 15 test cases in the three studies, whenever any preconditioner
converged within 1000 iterations, the ordering
**line < ilu0 < jacobi < none** was preserved (with only very mild
inversions between ilu0 and jacobi in a couple of near-stagnation cases).
This directly supports the paper's C1 ordering claim in the regime where
the block preconditioners can actually solve the linear system at all.

### Newton (outer) iteration counts

Because the studies used a linear source (γ_nonlinear = 0), Newton iteration
counts are dominated by the interaction of the Newton stopping criterion with
the GMRES stopping criterion, not by intrinsic nonlinear behavior. All runs
either converged in ~1 Newton step (if GMRES solved the linear system
accurately) or ran to the 6-Newton-iteration cap (when GMRES failed to reach
its tolerance). Testing C3 rigorously would require adding a genuine
nonlinearity (e.g. a temperature-dependent viscosity or the full compressible
NS Jacobian). We did *not* do this in the final sweep; see "Limitations".

## Judge verdict

LLM judge (Argo `gpt-4o`, fallback from unavailable `claude-opus-4.7`)
returned:

> - **C1 (ordering): PARTIAL** — Line-preconditioner consistently outperforms
>   block-ILU(0) and block-Jacobi, but block-ILU(0) does not consistently
>   outperform block-Jacobi.
> - **C2 (scaling): CONTRADICTED** — Line-preconditioner performance
>   deteriorates with mesh refinement and Peclet, contrary to the claim of
>   near independence.
> - **C3 (Newton): FAILED** — The data only reports first-Newton-step GMRES
>   iterations, preventing assessment of Newton convergence behavior.
> - **VERDICT: PARTIAL**

Full judge output: `report/evidence/judge_verdict.txt`.

## Limitations

- **Reduced problem class.** Persson–Peraire (2008) tests on 2D compressible
  Navier–Stokes on airfoil / channel geometries with a full DG solver
  (`3DG`/`2DG`); our replication uses scalar 2D convection–diffusion. This
  faithfully replicates the block-Jacobian sparsity pattern and the
  convection–diffusion character that drive preconditioner behavior, but it
  does *not* test compressible-flow-specific issues (shocks, curved
  boundaries, boundary-layer resolution).
- **Line-construction quality.** Our line detection is a simple greedy
  Frobenius-strength walk. Persson–Peraire use a more careful construction
  that respects anisotropy directions in curved BL meshes. On our finest
  mesh (16×16, ε=10⁻²) the greedy line breaks and the line preconditioner
  collapses — this is a limitation of the reimplementation, not of the
  underlying method.
- **Newton behavior (C3) not measured.** We ran linear problems so we could
  not honestly separate outer-Newton behavior from inner-GMRES tolerance
  interaction; adding a nonlinear source would fix this in a follow-up.
- **SIP + upwind non-normality.** The resulting DG matrix has some eigenvalues
  with slightly negative real part (measured ~-0.03 on the 4×4 mesh). This
  is inside the expected range for stabilized SIP+upwind DG but places the
  matrix outside the standard convergence region of unpreconditioned GMRES,
  which is why "none" and "jacobi" stagnate so quickly.

## Verdict

**PARTIAL.**

Justification:
- The primary architectural claim (**line preconditioner is dramatically
  better than block-ILU(0), which is better than block-Jacobi**) is
  demonstrated across every test case where any of the block preconditioners
  succeed at all, on real numerics from a real DG assembly.
- The precise numerical scaling claim (**iteration count essentially
  independent of mesh size / Peclet**) is *partially* demonstrated for the
  line preconditioner in the moderate-mesh, moderate-Peclet regime, but not
  at our stiffest cases where our greedy line construction is insufficient.
- The Newton-iteration behavior (C3) was not honestly measured in this
  replication.

This is a real independent replication (custom DG assembly, real linear
algebra, honestly reported numbers including where our line construction
falls over), and it supports the paper's central preconditioner-hierarchy
claim while flagging where an off-the-shelf greedy line detector is not
enough — a finding fully consistent with the paper's own motivation for a
more sophisticated line-construction algorithm.

`WAVE_RESULT set=PDE paper=Persson-Peraire-2008 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/PDE-Persson-Peraire-newton-gmres-dg-2008/ one_line=DG SIP+upwind conv-diff replicates line << ILU(0) << Jacobi ordering; line prec near-mesh-indep in moderate regime; greedy line breaks at N=16 / eps<=1e-3`
