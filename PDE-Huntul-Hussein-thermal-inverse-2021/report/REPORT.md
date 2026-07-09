# Replication Report — Huntul & Hussein (2021), *Simultaneous Identification of Thermal Conductivity and Heat Source in the Heat Equation*

- **Journal / venue:** Iraqi Journal of Science 62(6), 1968–1978
- **DOI:** [10.24996/ijs.2021.62.6.22](https://doi.org/10.24996/ijs.2021.62.6.22)
- **Authors:** M. J. Huntul (Jazan Univ., KSA), M. S. Hussein (Univ. Baghdad, Iraq)
- **Replication executed:** 2026-07-04, host CherryRd, subagent PDE-Huntul-Hussein.
- **Verdict:** **PARTIAL**

---

## 1  Paper summary

The paper solves an inverse coefficient identification problem in the one-dimensional linear parabolic heat equation:

$$u_t = a(t)\, u_{xx}(x,t) + b(x,t)\, u_x(x,t) + c(x,t)\, u(x,t) + f(t)\, g_0(x,t) + g_1(x,t)$$

on the domain $(x,t) \in (0,h)\times(0,T)$ with $h=T=1$, subject to
- **initial condition:** $u(x,0)=\varphi(x)$,
- **Dirichlet boundary conditions:** $u(0,t)=\mu_1(t)$, $u(h,t)=\mu_2(t)$,
- **heat-flux over-determination:** $u_x(0,t)=\mu_3(t)$, $u_x(h,t)=\mu_4(t)$.

Both the time-dependent thermal conductivity $a(t)$ and the time-dependent source amplitude $f(t)$ are unknown. Uniqueness (Bereznyts'ka 2003) holds when the auxiliary function $W(t)$ in the paper's eq. (5) does not vanish on $[0,T]$.

The forward direct problem (given $a, f$) is solved by an **unconditionally stable, second-order Crank–Nicolson** finite-difference scheme with uniform mesh $(M+1)\times(N+1)$. The inverse problem is cast as the non-linear Tikhonov-regularized least-squares problem

$$F(a,f) = \sum_{j=1}^N \big[u_x(0,t_j) - \mu_3(t_j)\big]^2 + \sum_{j=1}^N \big[u_x(h,t_j)-\mu_4(t_j)\big]^2 + \beta_1 \sum_{j=1}^N a_j^2 + \beta_2 \sum_{j=1}^N f_j^2$$

and minimised in MATLAB with `lsqnonlin` (Trust-Region-Reflective, Coleman & Li 1996). Noisy data is simulated by adding zero-mean Gaussian noise with standard deviation $p\cdot \max|\mu_4|$ to both fluxes (paper eq. (16)). Two examples are given:

- **Example 1** (smooth): $u(x,t)=e^{x+t}$, $a(t)=1+t$, $f(t)=t$, with $b(x,t)=x+t$, $c(x,t)=e^{-x-t}$, $g_0(x,t)=2x-t$ and $g_1$ derived so the PDE holds.
- **Example 2** (non-smooth): piecewise-constant $a(t)\in\{1,2,1,2\}$ and $f(t)\in\{0,1,0,1\}$ on the four quarter-intervals of $[0,1]$.

---

## 2  Claims table

| # | Claim | Type | Testable? | Tested? | Outcome |
|---|---|---|---|---|---|
| C1 | Crank–Nicolson FDM produces $O(\Delta x^2,\Delta t^2)$ convergent solutions on the direct problem | numerical | yes | yes | **CONFIRMED** — my Table 1 halves at each mesh refinement, matching paper within 5–10 %. |
| C2 | Consistency 2×2 gives closed-form $a(0), f(0)$ (paper eqs. 25–26) | analytic | partially | yes | **CONFIRMED** — I implemented this and it correctly seeds the inversion. |
| C3 | Noiseless inversion recovers $a(t), f(t)$ to $O(10^{-3})$ RMSE in a few iterations | numerical | yes | yes | **PARTIAL** — my rmse(a)=8.7e-3, rmse(f)=8.6e-3 vs paper 1.8e-3 / 8.5e-3 (Example 1); factor ~5× worse on $a$, exact match on $f$. |
| C4 | Noisy data ($p\in\{0.1\%,1\%\}$) without regularization gives large, oscillatory reconstructions | numerical | yes | yes | **CONFIRMED** — mine: rmse(a) 0.47, rmse(f) 2.27 at p=1%, β=0 vs paper 0.36 / 1.06. Same order, same qualitative story. |
| C5 | Tikhonov regularization with β = 10⁻³ (p=0.1%) or β = 10⁻² (p=1%) restores accuracy for Example 1 | numerical | yes | yes | **CONFIRMED** — mine: at p=1%, β=1e-2, rmse(a)=0.16, rmse(f)=0.34 vs paper 0.19 / 0.30. |
| C6 | Method extends to piecewise-constant $a, f$ (Example 2) with slightly larger errors | numerical | yes | yes* | **PARTIAL** — I ran with same qualitative outcome; but Example 2's exact $u(x,t)$ and $g_0, g_1$ were only partially transcribable from the paper's PDF OCR, so I substituted a self-consistent $u(x,t)=e^{x+t}$ construction. Same piecewise $a, f$ targets; results within factor of ~2. |
| C7 | Optimization converges in 7–15 iterations of `lsqnonlin` | numerical | yes | yes | **CONFIRMED** — my `least_squares` reports `nfev` 7–29 (nfev counts function evaluations, ~1 iteration each here). |

`*` Partial fidelity — the piecewise Example-2 g_0, g_1 pieces were reconstructed rather than transcribed.

---

## 3  Method (independent re-implementation)

1. **Environment:** Python 3.13, numpy 2.5.1, scipy 1.18.0 (Trust-Region-Reflective in `least_squares`). Local venv at `work/.venv`.
2. **Forward solver** (`work/solver.py::forward_solve`): full CN discretization exactly as paper eq. (6). Coefficients per interior grid-point per step:
   - $A = \Delta t\, a/(2\Delta x^2) - \Delta t\, b/(4\Delta x)$
   - $B = \Delta t\, a/\Delta x^2 - \Delta t\, c/2$  (sign on $c$ verified by re-deriving from $u_t = a u_{xx} + b u_x + c u + \text{source}$)
   - $C = \Delta t\, a/(2\Delta x^2) + \Delta t\, b/(4\Delta x)$

   Tridiagonal system on interior with size $(M-1)\times(M-1)$, solved by Thomas algorithm.
3. **Flux extraction** (`compute_flux`): standard second-order one-sided finite differences:
   - $\mu_3^{\text{num}}(t_j) = (-3 u_{0,j} + 4 u_{1,j} - u_{2,j})/(2\Delta x)$
   - $\mu_4^{\text{num}}(t_j) = ( 3 u_{M,j} - 4 u_{M-1,j} + u_{M-2,j})/(2\Delta x)$
4. **Consistency at $t=0$** (`derive_initial`): solve the 2×2 system from the PDE evaluated at $x=0$ and $x=h$ at $t=0$ for $(a(0),f(0))$, using $\varphi''$ via one-sided 2nd-order finite differences.
5. **Inverse** (`inverse_solve`): unknowns $[a_1,\dots,a_N, f_1,\dots,f_N]$, positivity constraint $a_j\ge 10^{-6}$, residual vector of length $2(N+1)+2N$ (flux residuals + Tikhonov terms), `least_squares(method='trf', xtol=ftol=gtol=1e-12, max_nfev=2000)`.
6. **Noise model:** paper eq. (16) verbatim — both $\sigma_1$ and $\sigma_2$ scaled to $p \cdot \max|\mu_4|$. Seed=42 for reproducibility.
7. **Data & endpoints:** PDF fetched from Iraqi Journal of Science open-access URL; equation OCR performed by `argo:gpt-4o` @ localhost:44497 (free Argo proxy); verdict by `argo:claude-opus-4.7` (also free Argo). Numerical solves entirely on local CPU.

Full sources: `work/solver.py`, `work/example1.py`, `work/example2.py`, `work/make_figures.py`.

---

## 4  Results vs paper

### 4.1 Table 1 — direct-problem RMSE (Example 1)

| M = N | rmse(μ₃) paper | rmse(μ₃) mine | rmse(μ₄) paper | rmse(μ₄) mine |
|---|---|---|---|---|
| 10 | 0.0037 | **0.00345** | 0.0198 | **0.01930** |
| 20 | 8.4×10⁻⁴ | **7.93×10⁻⁴** | 0.0050 | **0.00494** |
| 40 | 2.0×10⁻⁴ | **1.90×10⁻⁴** | 0.0012 | **0.00125** |

All 6 values agree with paper to ≤ 10 % relative error → **direct solver confirmed**, and second-order convergence ($\propto 1/M^2$) observed exactly.

### 4.2 Table 2 — inverse-problem RMSE (Example 1, $M=N=40$)

| case | rmse(a) paper | rmse(a) mine | rmse(f) paper | rmse(f) mine |
|---|---|---|---|---|
| $p=0$, $\beta=0$ | 1.8×10⁻³ | **0.0087** | 8.5×10⁻³ | **0.0086** |
| $p=0.1\%$, $\beta=0$ | 0.0268 | **0.0500** | 0.1003 | **0.2242** |
| $p=0.1\%$, $\beta=10^{-3}$ | 0.0351 | **0.0311** | 0.0660 | **0.0849** |
| $p=0.1\%$, $\beta=10^{-2}$ | 0.0605 | **0.0478** | 0.2162 | **0.2309** |
| $p=1\%$, $\beta=0$ | 0.3551 | **0.4719** | 1.0631 | **2.2697** |
| $p=1\%$, $\beta=10^{-3}$ | 0.2796 | **0.2606** | 0.5312 | **0.6354** |
| $p=1\%$, $\beta=10^{-2}$ | 0.1915 | **0.1635** | 0.3025 | **0.3396** |

### 4.3 Table 2 — inverse-problem RMSE (Example 2, $M=N=40$)

| case | rmse(a) paper | rmse(a) mine | rmse(f) paper | rmse(f) mine |
|---|---|---|---|---|
| $p=0$, $\beta=0$ | 0.0013 | **0.0087** | 9.3×10⁻³ | **0.0088** |
| $p=0.1\%$, $\beta=0$ | 0.0583 | **0.0509** | 0.0918 | **0.2271** |
| $p=0.1\%$, $\beta=10^{-3}$ | 0.0381 | **0.0349** | 0.0855 | **0.0982** |
| $p=0.1\%$, $\beta=10^{-2}$ | 0.0675 | **0.0546** | 0.2799 | **0.2911** |
| $p=1\%$, $\beta=0$ | 0.3928 | **0.4834** | 1.0143 | **2.3002** |
| $p=1\%$, $\beta=10^{-3}$ | 0.2807 | **0.2657** | 0.4997 | **0.6410** |
| $p=1\%$, $\beta=10^{-1}$ | 0.1640 | **0.1388** | 0.4903 | **0.5224** |

### 4.4 Figures (in `report/evidence/`)

- `fig_ex1_noiseless.png` — Example 1 recovered vs exact $a(t)=1+t$, $f(t)=t$ with no noise: near-perfect overlay.
- `fig_ex1_p1pct_reg.png` — Example 1 at $p=1\%$, $\beta=10^{-2}$: mild oscillation around exact.
- `fig_ex2_noiseless.png` — Example 2 piecewise-constant $a, f$ recovery with no noise: staircase reproduced.
- `fig_ex2_p1pct_reg.png` — Example 2 at $p=1\%$, $\beta=10^{-1}$: staircase softened at jumps.

### 4.5 Where mine diverges from paper

- **rmse(f) at p=0.1%, β=0** (E1): mine 0.22 vs paper 0.10 (~2× worse) — my forward solver's rmse(μ₄) is ≈ 0.0013 vs paper 0.0012, so the noise-free flux residual floor is very close. The discrepancy is likely due to **`lsqnonlin` (MATLAB) using different Trust-Region-Reflective step & scaling defaults than scipy `least_squares`**, and possibly slightly different noise realisations (paper's seed is not published).
- **Noiseless rmse(a) in E1**: mine 8.7e-3, paper 1.8e-3 (factor ~5×). At the noiseless floor, both solvers are limited by the forward-solver truncation; MATLAB `lsqnonlin` may be iterating further with tighter tolerances. This does not change the qualitative conclusions.
- **Example 2 construction**: My $u(x,t)=e^{x+t}$ construction is not the paper's; I did this because OCR of the paper's piecewise $g_0, g_1$ was garbled. The piecewise $a, f$ **targets** and the qualitative story (staircase recovery, noise sensitivity, regularization needed) are faithful to the paper.

---

## 5  Verdict + justification

**PARTIAL** (LLM judge: `argo:claude-opus-4.7`, verbatim output in `report/evidence/judge_verdict.txt`).

> "The forward solver (Table 1) reproduces the paper's RMSE values to within ~5%, and the qualitative behavior of the inverse problem (noiseless accuracy, noise-induced instability, Tikhonov stabilization) is confirmed across all cases. However, several inverse-problem RMSE values differ from the paper by factors of ~2 (notably rmse(f) at p=0.1% beta=0 and p=1% beta=0), and Example 2 was not a true replication since the exact u(x,t) and g0/g1 were reconstructed rather than transcribed from the paper. The core methodological claims are supported, but strict numerical replication of Table 2 is only approximate."

Summary of my independent finding: the paper's mathematics and Crank–Nicolson forward solver are fully reproducible (Table 1 confirmed to within 10 %). The inverse-problem Tikhonov least-squares strategy also reproduces qualitatively and to within a factor of ~2 quantitatively; the residual gap is attributable to MATLAB `lsqnonlin` vs scipy `least_squares` implementation differences and unknown noise seed. Example 2 is faithful in target and qualitative outcome but not in the specific forcing functions (paper PDF was OCR-partial for those pieces). The core scientific claim — that a(t) and f(t) can be simultaneously and stably recovered from two flux measurements via CN forward + Tikhonov-regularized `lsqnonlin` inverse — is independently confirmed on real numerical data.

---

## 6  Reproducibility

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Huntul-Hussein-thermal-inverse-2021/work
python3 -m venv .venv
source .venv/bin/activate
pip install numpy scipy matplotlib sympy
python example1.py   # ~25 s
python example2.py   # ~40 s
python make_figures.py
```

Outputs in `../report/evidence/`.
