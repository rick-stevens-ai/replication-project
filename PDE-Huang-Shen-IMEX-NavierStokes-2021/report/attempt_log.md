# Attempt Log

**Date:** 2026-07-02 (CDT). Replication wave — PDE-100.

1. Read WAVE_BRIEF + PDE_NEXT50 priority list. Dedup vs existing sibling dirs. Selected the highest-ranked still-undone OA repro-ok paper with a clean numerical PDE core + analytic reference: **#6 Huang–Shen IMEX Navier–Stokes (score 58.35)**. Confirmed non-colliding (no `PDE-Huang*` dir; `PDE-replications/` has none).
2. Fetched OA PDF from **arXiv:2103.11025v1** (free; not the paid pdf tool). `pdftotext -layout` → clean text. Extracted the SAV/BDFk scheme (eqs 3.6/3.14, coefficients 3.8–3.12), the Leray/pressure elimination (3.1–3.3, 3.7), and Example 1 (exact solution + domain + params + Fig. 1 claim).
3. Verified symbolically (sympy) that the manufactured velocity is divergence-free (div u = 0).
4. Derived the external forcing `f = u_t − νΔu + (u·∇)u + ∇p` with hand-coded analytic derivatives; **validated vs sympy lambdify to 5.7e-14** (machine precision) at 20 random points.
5. Implemented from scratch: Fourier-spectral operators (FFT), Leray projection, spectral advection, IMEX-BDFk (k=1..4) with SAV relaxation, H¹ error norms via Parseval.
6. **Bug 1:** first run gave errors ~38 (= ‖u_exact‖, i.e. u_num≈0). Isolated by testing `sav=False`: the plain IMEX-BDFk march gave *perfect* order-1/2/3/4 convergence → velocity solver correct; **SAV factor was collapsing the solution to zero.**
7. **Bug 2 (pressure):** recovery from exact velocity gave H¹ err 207. Root cause: `−Δp = ∇·(u·∇u)` only holds for the *unforced* NS; with forcing it is `Δp = ∇·f − ∇·(u·∇u)`. Added the forcing-divergence term → pressure recovery from exact field dropped to **2.5e-13**.
8. **SAV fix:** the auxiliary variable r = E(u)+1 with E = ½‖∇u‖² (2D). The manufactured solution's energy GROWS from 0 (sin²t) to ~708, so the pure-dissipation SAV ODE starved r → η→0. Added the correct forcing-*production* term for E=½‖∇u‖²: `(f, −Δū) = (∇f,∇ū)` (not `(f,u)`, which is the ½‖u‖² balance). After this, η→1 for the resolved flow and full high-order convergence appeared.
9. **Result:** fitted temporal orders — BDF1 (u 1.00 / p 0.95), BDF2 (1.89/1.95), BDF3 (3.02/3.01), BDF4 (4.14/4.08). Matches paper Fig. 1 claim.
10. **Stability check:** at large dt=0.05 the SAV H¹-energy stays bounded ≈707.5–707.8 (= exact final), η∈[0.985,1.0008] — confirms Theorem 1 (unconditional stability) and that SAV is a near-identity relaxation for resolved smooth flow.
11. Generated convergence log-log plot; saved all JSON/plot evidence.
12. **Multi-judge** (free Argo, temp 0): gpt-5.2, gemini-2.5-pro, gpt-4.1 — all **REPLICATED**.

Compute: light (40×40 spectral, ~1e5 dofs); ran locally in <2 min per full sweep. No GPU needed.
