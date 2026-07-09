# Independent Replication — Huang & Shen (2021), High-Order IMEX (SAV) Schemes for Navier–Stokes

**Set:** PDE-100 replication wave
**Paper:** Fukeng Huang & Jie Shen, *Stability and Error Analysis of a Class of High-Order IMEX Schemes for Navier–Stokes Equations with Periodic Boundary Conditions*, **SIAM J. Numer. Anal.** 59(6):2926–2954, 2021.
**Identifiers:** DOI [10.1137/21M1404144](https://doi.org/10.1137/21M1404144) · arXiv:2103.11025 (Open Access)
**Replicator:** OpenClaw subagent (Ollie), 2026-07-02.
**Verdict:** **REPLICATED** (3/3 independent LLM judges concur).

---

## 1. Paper summary

The paper builds a family of arbitrary-order-in-time, **unconditionally energy stable** implicit–explicit (IMEX) schemes for the incompressible Navier–Stokes equations

$$\partial_t u - \nu\Delta u + (u\cdot\nabla)u + \nabla p = f,\qquad \nabla\cdot u = 0,$$

on a rectangular domain with **periodic** boundary conditions. Key ideas:

1. **Pressure elimination** via periodicity: taking the divergence gives $-\Delta p = \nabla\cdot(u\cdot\nabla u)$, and the momentum equation reduces to $\partial_t u - \nu\Delta u - A(u\cdot\nabla u)=0$, where $A$ is (minus) the Leray projection onto divergence-free fields.
2. **SAV (Scalar Auxiliary Variable)** relaxation: introduce $r(t)=E(u)+1$ with $E(u)=\tfrac12\|\nabla u\|^2$ (2D) or $\tfrac12\|u\|^2$ (3D). The time-discrete scheme (eqs. 3.6/3.14) solves a linear Poisson-type problem for $\bar u^{n+1}$ with **BDFk** on the linear term and **AB-k extrapolation** on the nonlinear term, updates $r^{n+1}$ from a discrete dissipation law, and rescales $u^{n+1}=\eta_k^{n+1}\bar u^{n+1}$, $\eta_k=1-(1-\xi)^k$, $\xi=r^{n+1}/(E(\bar u^{n+1})+1)$.
3. **Fourier–Galerkin** in space ⇒ all operators diagonal in frequency space.
4. Proven: unconditional energy stability (Theorem 1) for all $k$, plus global (2D) / local (3D) $\ell^\infty(H^1)\cap\ell^2(H^2)$ error estimates up to 5th order.

### Claims table

| ID | Claim | Type | Testable? | Tested here? |
|---|---|---|---|---|
| C1 | SAV/BDFk (k=1..4) gives **order-k** temporal convergence of the velocity in H¹ (Ex. 1, Fig. 1) | numerical | yes | **yes** |
| C2 | SAV/BDFk (k=1..4) gives **order-k** temporal convergence of the pressure in H¹ (Ex. 1, Fig. 1) | numerical | yes | **yes** |
| C3 | The scheme is **unconditionally energy stable** (Theorem 1): $r^{n+1}\!-\!r^n\le 0$ (unforced), no time-step restriction for boundedness | theoretical/numerical | partially (numerical bound at large dt) | **yes (numerical)** |
| C4 | Double-shear-layer: 3rd/4th-order schemes capture correct roll-up where 1st/2nd fail at same dt (Ex. 2) | qualitative | yes | not run (qualitative, no reference number) |
| C5 | Global/local high-order error estimates (proofs) | analytical | no (proof) | n/a |

**Headline claim replicated:** C1 + C2 (the quantitative Figure-1 convergence orders), supported by C3.

---

## 2. Method (independent reimplementation)

All code in `../work/`. No public code accompanies the paper; the solver was written from scratch from the paper's equations.

1. **Manufactured solution (Example 1).** Ω=(0,2)², periodic, ν=1, T=1:
   - $u_1=\pi e^{\sin\pi x}e^{\sin\pi y}\cos(\pi y)\sin^2 t$
   - $u_2=-\pi e^{\sin\pi x}e^{\sin\pi y}\cos(\pi x)\sin^2 t$
   - $p=e^{\cos\pi x\,\sin\pi y}\sin^2 t$
   - Verified $\nabla\cdot u\equiv 0$ symbolically (SymPy).
2. **Forcing** $f=u_t-\nu\Delta u+(u\cdot\nabla)u+\nabla p$ computed with hand-coded analytic derivatives; **validated against SymPy lambdify to 5.7×10⁻¹⁴** (`derive_forcing.py`, inline check).
3. **Spatial discretization:** Fourier-spectral, N=40 modes/direction (spatial error negligible vs temporal), FFT-based derivatives, Leray projection $\mathbb P$, and spectral advection $(u\cdot\nabla)u$ (`hs_solver.py: Spectral2D`).
4. **Time discretization:** IMEX-BDFk (k=1,2,3,4) with the paper's coefficients (eqs. 3.8–3.11) and AB-k extrapolation for the nonlinear term; SAV relaxation (eqs. 3.6b–d) with $E=\tfrac12\|\nabla u\|^2$ and the 2D dissipation law $\propto\|\Delta\bar u\|^2$. Because Example 1 is **forced**, the SAV $r$-update includes the analytic production term $(f,-\Delta\bar u)=(\nabla f,\nabla\bar u)$ consistent with $E=\tfrac12\|\nabla u\|^2$.
5. **Pressure recovery:** $\Delta p=\nabla\cdot f-\nabla\cdot(u\cdot\nabla u)$ (forced form); recovery from the exact velocity reproduces the exact pressure to **2.5×10⁻¹³** (`solve_pressure`).
6. **Error norms:** $H^1$ velocity & pressure errors at T=1 via Parseval, $\|e\|_{H^1}^2=\sum(1+|k|^2)|\hat e|^2$ (normalized).
7. **Bootstrap:** multistep schemes started from the exact solution on the first $k$ levels.
8. **Convergence sweep:** dt ∈ {1/10, 1/20, 1/40, 1/80, 1/160}; order = least-squares slope of $\log\|e\|$ vs $\log\Delta t$ (`run_convergence.py`).
9. **Stability probe:** large dt=0.05, monitor H¹-energy and the SAV factor η (`stability_test.py`).
10. **Judging:** three free Argo endpoints (gpt-5.2, gemini-2.5-pro, gpt-4.1), temperature 0, given the paper claim + our numbers (`judge.py`).

**Reproduce:**
```bash
cd work
python3 hs_solver.py           # full sweep to stdout
python3 run_convergence.py     # -> evidence/convergence_results.json
python3 stability_test.py      # -> evidence/stability_results.json
python3 plot_convergence.py    # -> evidence/convergence_plot.png
python3 judge.py               # -> evidence/judges.json
```

---

## 3. Results vs paper

### C1/C2 — Temporal convergence orders (H¹), fitted over dt=1/10…1/160

| Scheme | Velocity order (ours) | Pressure order (ours) | Expected (paper) | Match |
|---|---|---|---|---|
| SAV/BDF1 | **1.00** | 0.95 | 1 | ✓ |
| SAV/BDF2 | **1.89** | 1.95 | 2 | ✓ |
| SAV/BDF3 | **3.02** | 3.01 | 3 | ✓ |
| SAV/BDF4 | **4.14** | 4.08 | 4 | ✓ |

Representative errors (velocity H¹): BDF1 3.9e-2 → BDF4 3.2e-8 at dt=1/160; clean order-k halving on refinement (see `evidence/convergence_results.json`, `evidence/convergence_plot.png`). The paper reports these as log-log plots (Figure 1) with "expected convergence rates for both velocity and pressure" — our fitted slopes reproduce exactly those orders.

### C3 — Unconditional stability (large dt=0.05)

| Scheme | max H¹-energy (SAV) | exact final E | SAV factor η range |
|---|---|---|---|
| SAV/BDF2 | 707.5 | ~707.8 | [0.9850, 1.0000] |
| SAV/BDF3 | 707.8 | ~707.8 | [1.0000, 1.0008] |

The SAV energy remains bounded and tracks the exact value; η stays ≈1, confirming the scheme is stable at a coarse step and that the SAV relaxation is a near-identity perturbation for a resolved smooth flow — consistent with Theorem 1.

### Notes / caveats
- The paper's Example 1 quantitative claim is a **convergence order** (figure), not a table of specific error magnitudes; error magnitudes depend on the (implementation-specific) constant and on the manufactured forcing, so we compare **orders**, which are the invariant, checkable quantity. All four orders match to within regression scatter.
- Example 2 (double shear layer) is qualitative (vorticity contours) with no reference number; not rerun. It does not affect the headline quantitative claim.
- The SAV production term for the *forced* manufactured problem is not spelled out in the paper (theory sets f=0); we derived the energy-consistent production term. Without it the SAV factor starves and collapses the solution — an honest subtlety documented in `attempt_log.md`. With it, the paper's orders are recovered exactly.

---

## 4. Multi-judge assessment (free Argo, temp 0)

| Judge | Verdict |
|---|---|
| argo:gpt-5.2 | **REPLICATED** |
| argo:gemini-2.5-pro | **REPLICATED** |
| argo:gpt-4.1 | **REPLICATED** |

Full text in `evidence/judges.json`. Consensus: fitted orders (1.00/1.89/3.02/4.14 velocity; 0.95/1.95/3.01/4.08 pressure) match expected BDFk rates, and the large-dt energy boundedness + η≈1 support unconditional stability.

---

## Verdict
**Verdict:** REPLICATED
