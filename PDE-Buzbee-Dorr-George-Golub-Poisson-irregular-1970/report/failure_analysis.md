# Failure analysis

## What actually failed / went sideways during this replication

### F1 — CherryRd → OSTI: direct HTTP fetch hung silently
- **What:** `curl -L https://www.osti.gov/servlets/purl/4060961` from CherryRd
  returned `HTTP=000, size=0` after the max-time cap. No error, no HTML,
  just a timeout.
- **Root cause:** Outbound firewall / OSTI throttling on CherryRd's egress
  path. Not investigated further because the workaround worked.
- **Workaround:** `ssh uicgpu 'source ~/env.sh; curl ...'` — uicgpu is on
  the ALCF proxy (`~/env.sh` sets `http_proxy` / `https_proxy` to Squid),
  and it returned HTTP 200 and a valid PDF in ~2 seconds. `scp`'d back to
  CherryRd.
- **Lesson:** For any OSTI / gov-domain fetch that misbehaves from
  CherryRd, first-line workaround is `ssh uicgpu 'curl ...'` before
  spending time debugging.

### F2 — Sign of the discrete Laplacian (my bug, not the paper's)
- **What:** First solver run produced max errors ~0.07 to 0.17, three
  orders of magnitude worse than expected.
- **Diagnosis path (see `work/diagnose.py`):**
  1. Capacitance-vs-direct-sparse consistency was ~1e-15 — so the
     capacitance correction was NOT the problem.
  2. Residual `||A x - y||_inf` was ~1e-15 — so the linear system WAS
     being solved exactly.
  3. Therefore the linear system I was solving was not the one I thought
     I was solving.
  4. Symbolically: my 5-point stencil `4 u_ij - u_{i±1,j} - u_{i,j±1}`
     is the *negative* of `h^2 * Δ_h`. With `u = x^2 + y^2` and `Δu = 4`,
     one has `(4u - Σ neighbors) = -4 h^2 = -(h^2 * f)`. So `A u = -h^2 f`,
     not `+h^2 f`. My RHS was wrong by a sign.
- **Fix:** Change `y[interior] = +h^2 * f` to `y[interior] = -h^2 * f`.
  Same fix in the imbedded RHS `y_bar`.
- **After fix:** max errors 5e-16 to 9e-15 (float64 machine precision).
- **Lesson:** When implementing a discrete elliptic operator, ALWAYS
  verify sign convention against a scalar test with a known analytic
  Laplacian on a single interior point BEFORE building the whole
  capacitance correction. The correction masked the bug because it was
  self-consistent — the correction preserved the wrong equation exactly.

### F3 — `p` in my code != `p` in paper Table 1
- **What:** Paper Table 1 says `p = 16, 32, 32, 64` for the four
  (Region, h) configs. My code counts `p = 81, 289, 81, 289`
  (= (inner_side * N + 1)^2, the number of hole-boundary + hole-interior
  grid points).
- **Best hypothesis:** The paper is exploiting the 4-fold reflection
  symmetry of the geometry to reduce the capacitance dimension by ~4x,
  or `p` refers to the interface unknowns of a SPLITTING construction
  applied to this same geometry (Section 5 discusses splitting the
  rectangle-with-hole into rectangular subregions along the hole boundary
  extended to the outer boundary — that would give `p ≈ N`).
- **Alternative:** the paper's `p` could just be a typo / OCR artifact
  (LA-4553-MS is a 1971 report OCR'd by ABBYY, not a native TeX source).
- **Not investigated further** because it does NOT affect the
  correctness of the METHOD, the CONVERGENCE RATE, or the achieved
  MAX ERROR. All three of those match the paper. The `p` mismatch
  affects only the *cost* of the specific pathway, and the paper's
  claim (`p^3` preprocessing + `p^2` per-solve) is verified regardless.

### F4 — marker / nougat unavailable on host
- **What:** Neither `marker`, `marker_single`, nor `nougat` was on
  CherryRd or in the accessible envs on uicgpu at replication time.
- **Impact:** No high-fidelity LaTeX-quality PDF parse for
  `extraction/nougat.mmd`. Fell back to a hand-structured stub that
  includes the section headings, key equations (rendered in LaTeX by
  hand from the paper), and Table 1 verbatim. This is the accepted
  fallback pattern in this repository (see the Einkemmer-Lubich
  low-rank sibling replication's own `extraction/marker.md`).
- **Impact on correctness:** none. The numerical replication only
  requires reading the paper text, not machine-parsing it.

### F5 — Did NOT implement a true Buneman / cyclic-reduction fast solver
- **What:** Used `scipy.sparse.linalg.splu(B)` (SuperLU) as the
  rectangle-solver stand-in.
- **Impact:** cannot demonstrate the paper's `θ(N) = 5 N^2 log_2 N`
  operation count as a wall-clock scaling. But the capacitance
  construction is fast-solver-agnostic — the correctness / error /
  consistency results are exactly the same.
- **What would fix it:** wrap `pyFFTW`-based FFT diagonalization of the
  1D Laplacian (Buneman-style) into a `RectangleSolver` class with the
  same `.solve(w)` interface. ~1-2 hours of extra work; not required
  for the paper's scientific claim.

## What to trust in this replication

- **HIGH trust:** the capacitance-matrix construction produces
  round-off-limited solutions on both the rectangle-with-hole and the
  L-shape; O(h^2) convergence to a manufactured solution; agreement with
  a full sparse solve at machine precision. These are the paper's
  central scientific claims and they are verified.

- **MEDIUM trust:** the operation-count claims (`p+1` fast solves for
  `C`, 2 fast solves per new RHS). Verified operationally (we
  instrumented `n_solves`) but not timing-verified because our fast
  solver stand-in is `splu` on a modern laptop.

- **LOW trust:** the *exact* p values in Table 1 (see F3 above). The
  paper's specific `p` values differ from what my direct reading of §4
  yields; the METHOD replication is unaffected but the row-by-row
  Table 1 reproduction is qualitative on the `p` column.

- **NOT REPRODUCED:** the CDC-6600 wall-clock timings in Table 1. This
  is by design — modern hardware makes those numbers meaningless in
  absolute terms.
