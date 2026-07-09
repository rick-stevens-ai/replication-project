# Low-Rank Vlasov–Poisson — Independent Replication

Independent NumPy/SciPy reimplementation of:

> L. Einkemmer & C. Lubich,
> *"A Low-Rank Projector-Splitting Integrator for the Vlasov–Poisson Equation,"*
> SIAM J. Sci. Comput. 40(5), B1330–B1360 (2018).
> [arXiv:1801.01103](https://arxiv.org/abs/1801.01103)

No author code or proprietary data — analytic initial conditions only,
1D1V phase space. Full report in [`REPORT.md`](./REPORT.md).

## TL;DR

* Implemented a full-grid Fourier semi-Lagrangian Vlasov–Poisson solver
  (Strang-split) as the reference truth.
* Implemented the dynamical low-rank (DLR) **KSL projector-splitting**
  integrator from the paper on the rank-r manifold
  `f(x,v,t) ≈ Σ X_k(x,t) S_kl(t) V_l(v,t)`.
* **Landau damping** (α=0.01, k=0.5): full grid reproduces the analytic
  damping rate γ≈0.1533 to within 0.5%; DLR with rank ≥ 4 matches the
  full grid to ~10⁻³ in L² error.
* **Two-stream** (α=0.05, v₀=2.4): DLR rank ≥ 8 captures linear growth +
  saturation; rank ≥ 16 captures phase-space filamentation.
* **Caveat (claim C6 in the report):** plain KSL is known to be
  non-robust in over-rank regimes. We hit this with r ≥ 8 on two-stream
  at the baseline Δt and had to use rank-adaptive Δt. The modern
  BUG / Ceruti–Lubich (2022) integrators are the proper cure.

## Files

See the layout in `REPORT.md` §8.

## How to reproduce

```bash
cd code
python3 smoke.py
python3 run_landau.py
python3 run_twostream.py
python3 make_figures.py
```

Total wall ~3 minutes on a single CPU core; no GPU, no cluster, no API keys.
