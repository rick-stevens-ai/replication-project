# Attempt Log

**2026-07-04 08:08 CDT** — Subagent spawned for PDE-Ketcheson-NodePy-ODE-2020.

1. Read WAVE_BRIEF; confirmed target dir empty; created `report/{evidence}` and `work/`.
2. Created venv `work/.venv`, `pip install nodepy matplotlib numpy sympy scipy`. Verified `nodepy==1.0.1` imports.
3. **Claim 1 (orders):** Loaded 10 canonical RK methods via `nodepy.runge_kutta_method.loadRKM`, called `.order()` on each. Every returned integer matched theoretical published order. `SSP53` needed `mode='exact'` fallback (Butcher-tree numerical roundoff at default tolerance) — a known NodePy caveat, not a paper failure.
4. **Claim 2 (SSP coefficients):** Called `.absolute_monotonicity_radius()`. SSP22=1.0, SSP33=1.0, SSP53=2.651, SSP104=6.0 — all match published Ketcheson/Shu-Osher values. Non-SSP methods (RK44 etc.) correctly returned 0.
5. **Claim 3 (stability regions):** Used `.plot_stability_region()` for RK44/DP5/SSP104 → PNGs in evidence/. Independently verified by evaluating stability function `p(z)/q(z)` along imag axis; boundary crossings match classical values.
6. **Claim 4 (empirical convergence):** Wrote a manual RK stepper (extracted `A`, `b` from each method, converted sympy Floats → numpy float) and integrated Dahlquist `y'=-y, y(0)=1` to T=1 for N=10..320. Estimated order via log2 error-ratio between successive N. Every method's estimated order → its formal order to 2 decimals (except DP5 which hit machine epsilon at N≥160 — expected).
7. **LLM-judge:** Sent evidence bundle to Argo `argo:claude-opus-4.7` at localhost:44497 (FREE endpoint per hard constraint). Verdict: REPLICATED.

## Failures / gotchas
- Initial convergence script failed because `method.A`, `method.b` are sympy `Float` objects — numpy `np.log` doesn't accept them. Fixed by wrapping in `np.array(..., dtype=float)` and using `float(np.dot(...))`.
- `SSP53.order()` returns 0 at default tol (roundoff message); works with `mode='exact'`. Documented in evidence.
