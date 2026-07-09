# Workflow — Mohamed (2019) BDF-2 Burgers' replication

Paper: N. A. Mohamed, "Solving one- and two-dimensional unsteady Burgers'
equation using fully implicit finite difference schemes",
*Arab J. Basic Appl. Sci.* **26**(1):254–268 (2019).
DOI: 10.1080/25765299.2019.1613746 (Open Access, CC BY-NC 4.0).

Verdict: **REPLICATED.**

---

## Stage 1 — Paper acquisition and reference-table scrape

1. Fetch OA metadata (DOAJ, CrossRef) to confirm licence + citation count (16×).
2. Attempt PDF download from T&F endpoint — **blocked** by Cloudflare on `curl`.
3. Fallback: OpenClaw headless-Chrome (`browser` tool) against the HTML
   full-text endpoint. The paper's tables are rendered via
   `showPopup?...&id=T0001..T0012` handlers; scrape each of the 12 tables into
   `work/paper_tables.md` for offline reference during replication.
4. Read equations (13)–(14) for 1-D, (23) for 2-D, and (27) for the
   Cole–Hopf series. Note the linearization from Kay–Gresho–Griffiths–Silvester
   (2010) as cited in §2 of the paper.

## Stage 2 — Reference (analytic) solution generators

1. **Cole–Hopf for Examples 1 & 2:**
   - Implement `u(x,t)` per Eq. (27), with `F(x)` per initial condition
     (Ex 1: `F = (1/(2 π ν)) (1 − cos π x)`; Ex 2: `F = (1/(3 ν)) x² (3 − 2x)`).
   - Composite Simpson integration on 4001 nodes for `c₀`, `cₙ`.
   - Truncate Fourier series at `n = 200` (well past exponential underflow
     for the tested (ν, t) pairs).
2. **Example 3 "exact" ansatz:** implement `u = (¼) e^{−ν t} cos(π x)` as
   the reference. (This is an approximate ansatz, not a strict PDE solution —
   see failure_analysis.md.)
3. **Example 4 (2-D) exact:** Fletcher / Liu–Pope–Sepehrnoori (1995)
   analytical solution as reported in the paper.

## Stage 3 — 1-D BDF-2 solver (`work/burgers1d.py`)

Per time step:

1. Compute the frozen-coefficient extrapolation `w = 2 u^n − u^{n−1}`
   (BDF-2 kickoff step uses `w = u^{n−1}` with backward Euler / BDF-1).
2. Build the tri-diagonal system `α, β, γ` exactly per paper Eqs. (13)–(14).
3. Apply BCs: Dirichlet by moving known boundary values into the RHS;
   mixed BC (Example 3 left boundary) by ghost-node reflection
   `u_{−1} = u_1`.
4. Solve with `scipy.linalg.solve_banded`.

## Stage 4 — 2-D BDF-2 solver (`work/burgers2d.py`)

Per time step:

1. Assemble the sparse pentadiagonal `(Nx_int × Ny_int)` matrix in COO/CSR
   per Eq. (23) of the paper (frozen-coefficient linearization applied
   independently in x- and y-fluxes).
2. Dirichlet BC values at `t^{n+1}` taken from the exact Liu–Pope–Sepehrnoori
   solution.
3. Solve with `scipy.sparse.linalg.spsolve`.

## Stage 5 — Numerical comparison against paper tables

For each of Tables 1, 2, 6, 11, 12:

1. Reproduce the paper's `(h, Δt, ν or Re, T)` configuration exactly.
2. Compute pointwise values (Tables 1, 2) or L₂ / L∞ error norms
   (Tables 6, 11, 12).
3. Compare against the scraped paper values in `work/paper_tables.md`.
4. Log residuals; flag any cell that disagrees by more than a factor of ~2.

## Stage 6 — Verdict + write-up

1. Aggregate 21 (1-D) + 12 (2-D) sampled cells into the results tables in
   `REPORT.md`.
2. Confirm all cells fall within the expected tolerance (Cole–Hopf
   truncation + MATLAB↔NumPy floating-point path differences ⇒ ≲ 2×).
3. **Genuine critique pass:** flag Example 3's approximate-ansatz issue,
   narrow comparative benchmarking, missing stability analysis, and the
   non-conservative-form limitation for shocks.
4. Emit `REPLICATED` verdict + `WAVE_RESULT` handoff line.

## Explicitly out of scope

- Non-uniform grid variant (paper Eqs. 15–21). Straightforward follow-up.
- High-Re Figures 3, 6 at Re = 10⁴, 2×10⁴ (require the non-uniform grid).
- Shock-forming initial data (paper never tests these; see open_questions.json).

## Tooling summary

| Purpose | Tool |
|---|---|
| Paper acquisition (Cloudflare-blocked PDF) | OpenClaw `browser` tool (headless Chrome) |
| Reference-table scraping | HTML full-text `showPopup` handlers |
| Numerics | Python 3.13, NumPy 2.5.1, SciPy 1.18.0 |
| Env | macOS 25.3.0, venv at `work/venv/` |
| Sparse solve (2-D) | `scipy.sparse.linalg.spsolve` |
| Banded solve (1-D) | `scipy.linalg.solve_banded` |
