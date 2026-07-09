# Replication Workflow — PDE-Ketcheson-NodePy-ODE-2020

Session: 2026-07-04, subagent, X-100 project.
Target: Ketcheson et al., *NodePy: A package for the analysis of numerical ODE solvers*, JOSS 5(55), 2515 (2020).

## Stages

### Stage 1 — Environment bootstrap
- `python3 -m venv work/.venv`
- `source work/.venv/bin/activate`
- `pip install nodepy matplotlib numpy sympy scipy`
- Landed `nodepy==1.0.1` (latest PyPI), Python 3.13, macOS 25.3.0.

### Stage 2 — Claim C1: formal order of RK methods
- Loop over `[RK44, Heun33, SSP22, SSP33, SSP53, SSP104, Merson43, Fehlberg45, DP5, CK5, BuRK65]`.
- Call `m = rk.loadRKM(name); p = m.order()`.
- Fallback to `m.order(mode='exact')` when default numeric returns 0 (SSP53 case).
- Emit per-method row into Table 4.1.

### Stage 3 — Claim C2: SSP coefficient
- For each method above, call `m.absolute_monotonicity_radius()`.
- Compare against published values for the 4 SSP methods and confirm 0 for non-SSP methods.
- Emit Table 4.2.

### Stage 4 — Claim C3: absolute stability regions
- For {RK44, DP5, SSP104}, call
  `m.plot_stability_region(N=200, bounds=[-10,2,-6,6])` → save PNG to
  `report/evidence/stability_<name>.png`.
- Independent numeric verification: extract `p, q = m.stability_function()`,
  scan `|p(iy)/q(iy)|` on `y ∈ [0.5, 3.0]` in steps of 0.5, emit Table 4.3.

### Stage 5 — Claim C4: empirical convergence on Dahlquist
- Extract Butcher tableau: `A = np.array(m.A, dtype=float)`, `b = np.array(m.b, dtype=float)`.
- Hand-code classical explicit RK step:
  `k_i = f(t + c_i*h, y + h * sum_j a_ij * k_j)`, `y_{n+1} = y_n + h * sum_i b_i * k_i`.
- IVP: `y' = -y, y(0) = 1`, integrate from `t=0` to `T=1` for
  `N ∈ {10, 20, 40, 80, 160, 320}`. Exact = `exp(-1) = 0.367879441171`.
- Observed order = `log2(err_N / err_{2N})`.
- Emit Table 4.4 + `evidence/convergence.csv`.

### Stage 6 — Verdict
- Assemble evidence bundle (all 4 tables + PNGs + CSV + method notes).
- POST to Argo `argo:claude-opus-4.7` at `http://localhost:44497/v1`
  (FREE endpoint per project rule).
- Judge returned strict-JSON:
  `verdict=REPLICATED`, coverage across all 4 claims, quantitative agreement.

### Stage 7 — Emit outputs
- `report/REPORT.md` (canonical)
- `report/REPORT.tex` (LaTeX + genuine critique)
- `report/open_questions.json` (5 truly-open follow-ups)
- `report/workflow.md` (this file)
- `report/artifacts_summary.md`
- `report/failure_analysis.md`
- `report/evidence/*` (PNGs, CSV, per-method logs)

## Determinism / reproducibility

- No RNG used in any of C1–C4 (all deterministic linear algebra + fixed
  Butcher tableaus + fixed grid sizes).
- Same `nodepy==1.0.1` + Python 3.13 + numpy default backends should
  reproduce every table byte-for-byte modulo float noise below 1e-14.
- LLM-judge output is model-dependent; the machine tables are authoritative.

## Cost

- Zero paid API usage. Argo endpoint is FREE. NodePy is FOSS.
- Compute: single macOS 25.3.0 laptop, seconds per stage.
