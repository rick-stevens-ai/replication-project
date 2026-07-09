# Attempt Log (chronological)

1. Selected candidate from PDE_NEXT50_2026-06-26.tsv. Skipped all ALREADY-DONE and
   Allen-Cahn/SAV/phase-field families; skipped stochastic-Burgers/Zhang/deepxde siblings.
   Chose **rank 30**: Anton–Cohen–Quer-Sardanyons, 1D stochastic heat equation (parabolic
   SPDE, distinct family, rigorous verifiable convergence-order claim). Confirmed on arXiv
   (1711.08340). Dedup: no colliding sibling dir.

2. Downloaded OA PDF + LaTeX e-print from arXiv. `pdftotext -layout`. Extracted exact
   scheme (Eq.15), spatial discretization (A=M²D, DST eigenstructure), and the numerical
   experiment parameters (Sec 2.2.3): u0=cos(π(x-1/2)), f(u)=u/2, σ(u)=1-u, T=0.5,
   dx=2⁻⁹, dt_ref=2⁻¹⁶, 500 samples; headline = temporal strong order 1/2.

3. Implemented SEXP from scratch (`sexp_heat.py`) using DST-I to diagonalize A.
   Verified DST diagonalization is EXACT vs dense `scipy.linalg.expm` (3.3e-16 at M=16).

4. VALIDATION FIRST (`validate_deterministic.py`):
   - (a) σ=f=0: SEXP exact in time, dt-independent (5.5e-15), matches e^{λ₁T}sin(πx) (1.7e-16).
     [Initial run showed spurious 8e-2 error — root cause was choosing T not divisible by dt
      so the two runs integrated to different final times; fixed by T=multiple of dt.]
   - (b) FD -> analytic PDE exp(-π²t)sin(πx): 2nd order in dx confirmed, rates all 2.000.

5. First stochastic pilot BLEW UP (errors 1e20) at large dt. Diagnosed: naive noise reading
   dW~N(0,dt) with Σ=√M·σ amplifies noise by factor M -> explicit blow-up for dt>2⁻¹⁰ at
   M=512. Checked paper Fig 1 axis range (x: 10⁻⁵..10⁰, y: 10⁻⁴..10⁻¹) -> paper does NOT
   blow up at large dt. Resolved: correct scaling uses space-time white-noise CELL increments
   ~N(0, dt·dx)=N(0,dt/M); net per-node noise = σ·√dt·ξ. Verified this gives bounded O(1)
   solutions for ALL dt∈[2⁻¹,2⁻¹⁶] -> reproduces the paper's "no CFL" claim.

6. Re-ran pilot with correct scaling: monotone convergence, RMS slope ≈0.57.

7. Full experiment on **uicgpu** (96 procs, `run_strong_order_mp.py`): M=512, dt_ref=2⁻¹⁶,
   coarse dt=2⁻³..2⁻¹⁰, 500 samples, T=0.5. Wall 10 s. Result: E[sup|.|²] slope 1.115 =>
   **strong (RMS) order 0.558** (paper: 1/2). Validation re-confirmed on uicgpu too.

8. Almost-sure/pathwise check (`run_as_convergence.py`): 5 paths, each converges to the
   reference as dt->0 with per-path slope 0.53–0.57 (order ~1/2), supporting Thm 2.4.

9. Multi-judge (free Argo, non-opus): gpt-5.2, gemini-2.5-pro, gpt-4.1 — all **REPLICATED**.

10. Wrote report artifacts. Done.
