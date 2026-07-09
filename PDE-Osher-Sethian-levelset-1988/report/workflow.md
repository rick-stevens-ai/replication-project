# Workflow — Osher & Sethian (1988) level-set replication

End-to-end procedure used to produce REPORT.md. All steps are
reproducible from the artifacts in this directory tree.

## 0. Scope decision
- Target paper: Osher, S. and Sethian, J. A. (1988), *Fronts propagating with
  curvature-dependent speed: Algorithms based on Hamilton–Jacobi formulations*,
  J. Comput. Phys. 79, 12–49.
- Wave: minimal 2-D replication in pure NumPy on a laptop CPU.
- Out of scope by design: higher-order ENO+RK order-of-accuracy test (C4);
  3-D / N-D generalization (C5); no external level-set library dependency.

## 1. Paper harvest
- Fetched the PDF from J. Sethian's UC-Berkeley page:
  `http://math.berkeley.edu/~sethian/2006/Papers/sethian.osher.88.pdf`
- Recorded sha256 (`508150b5…`) and page count (38 pages) in
  `report/artifact_harvest.md`.

## 2. Claim extraction
- Read the paper and enumerated testable core claims:
  - C1  constant-speed circle expansion `dR/dt = 1`
  - C2  mean-curvature circle collapse `R(t) = sqrt(R0^2 - 2*eps*t)`
  - C2b non-convex 7-pointed star smooths, perimeter monotone decreasing
  - C3  two-disk automatic topological merger without re-meshing
  - C4  higher-order ENO+RK gives higher-order accuracy (not tested)
  - C5  method generalizes to 3-D / N-D (not tested)
- Recorded in the "Claims table" section of `report/REPORT.md`.

## 3. Environment setup
- Python 3.13 venv at `work/venv`.
- Installed: NumPy 2.5.1, SciPy 1.18.0, Matplotlib 3.11.0,
  scikit-image 0.26.0.

## 4. From-scratch implementation (`work/levelset.py`)
- `upwind_grad_norm(phi, dx, dy, F)`: Rouy–Tourin form of the paper's
  Godunov flux (Eq. 3.11) with the correct max/min pattern for the sign
  of F.
- `central_curvature(phi, dx, dy)`: every derivative (∂x, ∂y, ∂xx, ∂yy,
  ∂xy, and the |∇φ| that multiplies K) is a central stencil, as the
  paper insists in §III.C.
- Time stepping: forward Euler.
  - Hyperbolic CFL for convection.
  - Parabolic CFL `Δt = 0.2·Δx²/ε` for the curvature part.
- Boundary conditions: periodic via `np.roll` (fronts stay well inside
  the domain in every experiment).
- Initialization: signed distance to the initial front; union of disks
  via `min(phi_1, phi_2)`.

## 5. Experiments (single command: `python levelset.py`)
| Exp | N | Δx | ε | Δt | Steps | Final T |
|-----|---|----|---|----|-------|---------|
| C1 (expand F=1)   | 201 | 0.01    | –    | 4.0e-3  |    125 | 0.5 |
| C2 (MCF) N=101    | 101 | 0.012   | 0.10 | 2.88e-4 |  1 389 | 0.4 |
| C2 (MCF) N=201    | 201 | 0.006   | 0.10 | 7.20e-5 |  5 556 | 0.4 |
| C2 (MCF) N=301    | 301 | 0.004   | 0.10 | 3.20e-5 | 12 500 | 0.4 |
| C2b (star)        | 301 | 0.00333 | 0.05 | 3.33e-5 |  9 000 | 0.3 |
| C3 (merge, F=1)   | 251 | 0.008   | –    | 3.20e-3 |    125 | 0.4 |

Total wall-clock < 3 min on a laptop CPU.

## 6. Analysis
- C1: compare numerical `R(T)` against exact `R0 + T`; report absolute,
  relative, and max trajectory error.
- C2: grid-refinement study at N∈{101, 201, 301}; compute L² and L∞
  errors on the well-resolved subset `R > 3Δx` and observed convergence
  order between consecutive grids.
- C2b: monitor perimeter and area every step; count fraction of steps
  with a perimeter increase (must be 0).
- C3: count connected components; measure merge time (first step at
  which components collapse from 2 → 1); compare to analytic 0.15.

## 7. LLM-judge pass
- Model: `argo:gpt-4o` via Argo proxy at
  `http://127.0.0.1:44497/v1/chat/completions` (free endpoint,
  `Authorization: Bearer stevens`), temperature 0.
- Input: paper claims + numerical results JSON.
- Output persisted to `report/evidence/llm_judge.txt`; summary reproduced
  in REPORT.md §5. All four sub-claims scored `pass`; overall verdict
  `REPLICATED`.

## 8. Report assembly
- `report/REPORT.md`: canonical Markdown report.
- `report/REPORT.tex`: LaTeX rendering of the same content plus a
  dedicated GENUINE CRITIQUE section listing 8 real limitations of this
  wave's scope.
- Evidence CSVs and snapshot PNGs under `report/evidence/`:
  `C1_expanding_circle.csv`, `C1_expanding_circle.png`,
  `C2_shrink_N101.csv`, `C2_shrink_N201.csv`, `C2_shrink_N301.csv`,
  `C2b_star_snapshots.png`, `C3_merge_snapshots.png`,
  `llm_judge.txt`, `artifact_harvest.md`.

## 9. Verdict
**REPLICATED.** C1 relative error 0.36% at N=201; C2 observed order
≈ 1.6–1.9; C2b perimeter strictly decreasing over 9 000 steps;
C3 merge-time relative error 0.27%.
