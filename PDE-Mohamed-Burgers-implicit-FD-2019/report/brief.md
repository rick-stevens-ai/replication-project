# Brief

**Paper.** N. A. Mohamed, "Solving one- and two-dimensional unsteady Burgers'
equation using fully implicit finite difference schemes",
*Arab Journal of Basic and Applied Sciences* 26(1):254–268, 2019.
DOI: [10.1080/25765299.2019.1613746](https://doi.org/10.1080/25765299.2019.1613746).
Gold OA, CC BY-NC 4.0, listed in DOAJ.

**What.** The paper proposes a fully implicit finite-difference scheme for
1-D and 2-D unsteady Burgers' equations: BDF-2 in time (BDF-1 kickoff),
2nd-order central differences in space, and a linear-extrapolation
linearization of the nonlinear term (Kay et al. 2010) that keeps the system
tri-diagonal (1-D) or pentadiagonal 5-point (2-D), so each time step is
one linear solve (Thomas algorithm). The truncation error is O(Δt² + h²).

**Why replicate.** The scheme is described completely with explicit
coefficient formulas (Eqs. 8–23), the four benchmark problems have known
analytical / Cole–Hopf solutions, and Tables 1, 2, 6, 7, 10, 11, 12 give
precise pointwise values and L₂/L∞ error norms that a from-scratch
Python + NumPy/SciPy implementation can hit or refute.

**Method.** Wrote independent implementations of the 1-D scheme
(`burgers1d.py`, banded solve via `scipy.linalg.solve_banded`) and the 2-D
scheme (`burgers2d.py`, sparse pentadiagonal via `scipy.sparse.linalg.spsolve`),
using only the equations in the paper. Compared to reference values scraped
directly from the T&F HTML full-text (Tables 1, 2, 6, 7, 10, 11, 12).

**Result.** REPLICATED. Pointwise values from Tables 1 and 2 match the
paper's "Proposed Scheme BDF-2" column to 4–6 significant figures. L₂/L∞
error norms from Tables 6, 11, 12 match to within a factor of ≲2 across the
full parameter sweep (ν ∈ {10, 1, 0.1, 0.05, 0.01}, Re ∈ {1, 10, 20, 100},
T ∈ [0.01, 3.5], 1-D grids 40–100 nodes, 2-D grids 5×5–30×30).
