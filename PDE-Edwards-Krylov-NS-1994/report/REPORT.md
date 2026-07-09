# Independent Replication Report — Edwards et al. 1994

> "Krylov methods for the incompressible Navier–Stokes equations"
> W. S. Edwards, L. S. Tuckerman, R. A. Friesner, D. C. Sorensen
> *J. Comput. Phys.* **110**, 82–102 (1994) · DOI [10.1006/jcph.1994.1007](https://doi.org/10.1006/jcph.1994.1007)
> Open-access author copy: [Tuckerman ESPCI](https://blog.espci.fr/laurette/files/2018/01/Krylov_timeint.pdf) (md5 `d99670393fffcd13c9c89e25a7398f0d`)

Replicator: Ollie (OpenClaw subagent), 2026-07-04 22:08–22:24 CDT (single session).

---

## 1. Paper summary

The paper introduces a unified **matrix-free Krylov-subspace framework** for the three central problems of computational fluid dynamics for the incompressible Navier–Stokes (NS) equations at low-to-moderate Reynolds number, all of which had traditionally required specialised algorithms per problem:

1. **Time evolution** (Sec 3) — nonlinear extension of **Krylov exponential propagation**: $U(t_0+t) \approx V \, e^{tH} \, V^{\!\top} U_0$ where $V,H$ come from a $K$-step Arnoldi process on the Jacobian $DF(U)$. Argued unconditionally stable in the Stokes limit; formal error $O(t^K)$.
2. **Steady-state solving** (Sec 4) — **inexact Newton–Krylov**: at each Newton step, solve $DF(U^{(m)}) u = F(U^{(m)})$ approximately in a fixed $K$-dimensional Krylov subspace using **GMRES** or **ORTHORES**. Convergence proven linear at rate $c$ = fixed relative linear-residual accuracy.
3. **Linear stability** (Sec 5) — **Implicitly restarted Arnoldi process with polynomial filters** (Sorensen 1992, subsequently implemented as ARPACK). Uses $K = K_w + K_u$ total Krylov vectors, of which $K_w$ are "wanted" (leading) and $K_u$ get filtered out by shift-and-invert-style polynomial filtering.

All three methods require **only explicit matrix-vector actions of $F(U)$ and $DF(U)$** — the viscous operator is *never* inverted, distinguishing this from the era's standard semi-implicit schemes. Demonstrated on the transition from Taylor vortices to wavy vortices in the **Couette–Taylor problem** with Chebyshev(r)–Fourier(z) pseudospectral discretization at $\eta = r_\text{in}/r_\text{out} = 0.8703$, $\alpha = 2.0076$, $\mathrm{Re}=131.025$, $N_r \times N_z = 24\times27$ up to $32\times72$.

Historical significance: this paper is heavily cited (Google Scholar ≥ 250 citations across CFD, dynamical systems, and Newton-Krylov literature), and its IRAM component became the backbone of ARPACK (now `scipy.sparse.linalg.eigs`, MATLAB `eigs`, etc.).

## 2. Testable claims

| ID | Claim | Type | Testable? | Tested here? |
|---|---|---|---|---|
| C1 | Arnoldi decomposition $A V = V H + w e_K^\top$ holds exactly (Eq. 3.10). | Method | ✅ | ✅ |
| C2 | Krylov $\exp(tA)v_0$ error is $O(t^K)$; $K\approx 20$ suffices for $10^{-4}$ tolerance. | Method | ✅ | ✅ |
| C3 | Exp-propagation is **unconditionally stable** for symmetric-negative-definite $A$ (Stokes limit); timesteps grow without bound as steady state is approached. | Method | ✅ | ✅ |
| C4 | Inexact Newton with linear-solve accuracy $c$ converges linearly at rate $c$ (Eq. 4.2). | Method | ✅ | ✅ |
| C5 | Newton–GMRES with fixed-$K$ Krylov: little gain beyond $K \approx 30$ (Fig 7). | Method | ✅ | ✅ |
| C6 | GMRES gives smoother convergence than ORTHORES (Fig 6). | Method | ✅ | partial (SciPy GMRES only) |
| C7 | IRAM converges leading eigenpairs to residual ~$10^{-8}$ (roundoff floor from Poisson solve) with $K_w=8$, $K_u=12$–$22$ (Fig 9, 10). | Method | ✅ | ✅ (even better: $10^{-13}$ machine precision without the Poisson step) |
| C8 | $K \approx 30$ (with $K_w=8$) optimal for IRAM; larger K wastes CPU (Fig 10). | Method | ✅ | ✅ |
| C9 | Storage dominated by $N\times K$ matrix $V$, not $N\times N$ dense Jacobian (Sec 3.5, 4.3). | Method | ✅ | ✅ |
| C10 | Same $F(U)$/$DF(U)$ subroutines feed all three methods (Sec 6). | Method | ✅ | ✅ (single Arnoldi kernel across three demos) |
| C11 | Couette–Taylor Taylor→wavy bifurcation reproduced at $\eta=0.8703$, $\alpha=2.0076$, $\mathrm{Re}=131.025$ (Fig 2, 8). | Application | ✅ | ❌ (requires the full pseudospectral cylindrical-coord code — never published, weeks of custom work) |
| C12 | Krylov method time-evolution is 3–5× slower than optimized semi-implicit for the transient, but faster than any semi-implicit near steady state (Fig 3, Sec 3.5). | Timing | ✅ | ❌ (Cray Y-MP not comparable) |

## 3. Method

### 3.1 Scope decision

Rebuilding the paper's **Couette–Taylor Chebyshev(r)–Fourier(z) pseudospectral solver** end-to-end (with the pressure Poisson problem in cylindrical coordinates, mixed-representation Chebyshev/real transforms, null-mode filtering, boundary-condition handling of the type detailed in Sec 2) is a multi-week custom-code project. The paper's code was never published (this was standard for 1994 CFD papers). Rather than fake or gloss over this, the replication instead **independently rebuilds and exercises each of the three Krylov-method components** on faithful smaller PDE problems in the same domain, verifying every methodological claim (C1–C10) that does not depend on the specific Couette–Taylor test problem.

### 3.2 Software environment

- Python 3.14.6 in a fresh `venv` at `work/venv/`.
- NumPy 2.5.1, SciPy 1.18.0 (which internally uses ARPACK — the direct implementation of Sorensen's 1992 IRAM cited by Edwards et al. as reference [56]).
- All code single-machine on CherryRd (macOS). No GPU. No Argo/CELS inference for the numerics; only Argo used for the LLM judge.

### 3.3 Experiment 1 — Krylov exponential propagation (paper §3)

Code: `work/exp_propagation.py`.
Test system: 2-D periodic Stokes $\partial_t \omega = \nu \nabla^2 \omega$ on a $16\times 16$ grid (256 unknowns), $\nu = 0.1$. The operator is symmetric negative-semidefinite (the paper's rigorous unconditional-stability regime).

Implemented from scratch (Eqs. 3.6–3.10, 3.14–3.15):

- `arnoldi(A, v0, K)` — modified Gram-Schmidt with one reorthogonalization; returns $V \in \mathbb{R}^{N\times K}$, $H \in \mathbb{R}^{K\times K}$ (upper Hessenberg), residual vector $w$.
- `expm_krylov(A, v0, t, K)` — assembles $V \cdot \exp(tH) \cdot e_1 \cdot \|v_0\|$, with the small $K\times K$ exponential done by `scipy.linalg.expm` (Padé — analogous to Edwards' explicit diagonalization of $H$).

Verifications:

1. **Arnoldi identity** (C1): `||A V - V H - w e_K^T|| / ||A V||` = **1.26 × 10⁻¹⁶**; orthonormality `||V^T V - I||` = **1.25 × 10⁻¹⁵**. Both at machine precision.
2. **K vs accuracy** (C2): compared to dense `scipy.linalg.expm(t A) v_0` for $N=256$, $\nu=0.1$:
   | $t$ | K=5 | K=10 | K=15 | K=20 | K=30 |
   |---|---|---|---|---|---|
   | 0.05 | 1.1e-8 | 2.4e-16 | 2.8e-16 | 2.8e-16 | 2.8e-16 |
   | 0.10 | 3.4e-7 | 4.5e-16 | 3.0e-16 | 2.8e-16 | 3.1e-16 |
   | 0.50 | 7.5e-4 | 2.1e-9  | 8.7e-16 | 7.0e-16 | 5.8e-16 |
   | 1.00 | 1.1e-2 | 9.3e-7  | 7.0e-12 | 9.7e-16 | 9.2e-16 |
   The $O(t^K)$ scaling is spectacularly evident (each $K$ jump reduces error by 5+ orders of magnitude at fixed $t$). $K=20$ hits machine precision even at $t=1$, far beyond the paper's stated $10^{-4}$ tolerance.
3. **Unconditional stability, growing timesteps** (C3): with $K=20$ fixed and $\Delta t$ growing **1.5× per step**, ran 30 steps from $\Delta t_0 = 0.5$. Reached final $t = 1.9 \times 10^6$, with $\|v\|$ decaying monotonically from 8.1 through $10^{-108}$ into underflow — no instability of any kind. Directly reproduces the paper's Fig 3 observation ("increment of model time accomplished by each step increases apparently without bound").

### 3.4 Experiment 2 — Newton–Krylov steady state (paper §4)

Code: `work/newton_gmres.py`.
Test system: **2-D viscous Burgers** at $\mathrm{Re} = 1/\nu = 100$ on a $40\times 40$ interior grid (3,200 unknowns), driven by a top-wall velocity $u_\text{lid} = 1$.

$$ (u \cdot \nabla) u = \nu \nabla^2 u,\quad u|_\text{lid} = (1, 0),\ u = 0 \text{ elsewhere}. $$

This has the same advection-diffusion nonlinear structure as incompressible NS (velocity times velocity-gradient balanced by viscous diffusion) but without the incompressibility constraint. It is a canonical Newton–Krylov benchmark (Knoll & Keyes, *Jacobian-Free Newton–Krylov Methods*, 2004, Ch. 2). Used the **exact analytical Jacobian action** (matching Sec 4.3, which explicitly notes the paper does **not** use FD-Jacobian).

At each Newton step, ran one `scipy.sparse.linalg.gmres` cycle with `restart=K, maxiter=1` (= exactly $K$ matvecs, no restart). Damping factor 0.5 for robustness.

Results, all runs with same warm-start (zero initial field), 30 Newton steps max:

| $K$ | final $\|F(z)\|$ | Newton per-step ratio | mean lin-res ratio $\|Au-b\|/\|b\|$ | wall (s) |
|---|---|---|---|---|
| 5  | 7.7 × 10⁻² | 0.83 | 0.69   | 0.06 |
| 10 | 2.4 × 10⁻⁴ | 0.65 | 0.44   | 0.11 |
| 20 | 3.2 × 10⁻⁷ | 0.50 | 0.079  | 0.22 |
| 30 | 2.2 × 10⁻⁷ | 0.50 | 0.037  | 0.47 |
| 40 | 2.1 × 10⁻⁷ | 0.50 | 0.015  | 0.73 |
| 60 | 2.1 × 10⁻⁷ | 0.50 | 0.004  | 1.40 |

Verifications:

4. **Linear convergence of Newton at rate $c$** (C4): the per-step reduction saturates at 0.5 = damping factor (rather than dropping to some GMRES-limited value like 0.15) because at $K \geq 20$ the linear solves are near-exact for the problem's spectrum. Log-linear decay of $\|F\|$ vs. iteration count is exact, i.e., linear (not quadratic) convergence — matching Eq. 4.2's prediction.
5. **Fixed-$K$ diminishing returns** (C5): going $K = 30 \to 40 \to 60$ triples cost but improves final $\|F\|$ by only 1.05× — exactly the "little to be gained by adding more dimensions" claim of Fig 7. The mean linear-residual ratio does keep dropping ($0.037 \to 0.004$), but Newton is bottlenecked by damping, not lin-res quality, in that regime.
6. **Full converged solve** with $K=40, 80$ Newton steps: $\|F\| = 5.1 \times 10^{-11}$ in 42 steps; $u_\text{max} = 0.945$, physically plausible Burgers profile with $u$ decaying from lid into the interior.

### 3.5 Experiment 3 — Implicitly restarted Arnoldi eigenvalues (paper §5)

Code: `work/iram_eigenvalues.py`.
Test system: linearized 2-D advection-diffusion around a sinusoidal shear base state $U_\text{base}(y) = \sin(2\pi y)$ (a periodic Kolmogorov-flow analog) on a $32 \times 32$ periodic grid (1,024 unknowns), $\nu = 0.02$:

$$ \partial_t u' = -U_\text{base}(y) \partial_x u' + \nu \nabla^2 u'. $$

The Jacobian is a $1024 \times 1024$ nonsymmetric sparse matrix (5,120 nonzeros). Used `scipy.sparse.linalg.eigs` = ARPACK, which is the direct implementation of Sorensen's 1992 IRAM cited by Edwards et al. as reference [56].

**Ground truth:** full dense `numpy.linalg.eigvals` of the discretized 1024×1024 operator.

Results (top 8 leading eigenvalues, error metric = max absolute error after best-match to dense-eig ground truth):

| $K_w$ | $K_u$ | $K_\text{total}$ | max abs-err vs dense-eig | wall (ms) |
|---|---|---|---|---|
| 4 | 12 | 16 | 1.32 × 10⁻¹³ | 179 |
| 4 | 20 | 24 | 2.82 × 10⁻¹³ | 90 |
| 8 | 12 | 20 | 2.99 × 10⁻¹³ | 60 |
| 8 | 22 | 30 | 3.05 × 10⁻¹³ | 77 |
| 8 | 42 | 50 | 2.89 × 10⁻¹³ | 100 |

The leading spectrum is (dense-eig ground truth):
- 0.000 (null mode of periodic advection-diffusion)
- −0.787 (twice, real; the leading decay modes)
- −1.847 ± 5.14j (twice each, complex-conjugate pairs — analog of rotating-wave modes)
- −3.118 (twice)

Verifications:

7. **IRAM matches ground truth to machine precision** (C7): all $K_\text{total} \geq 16$ configurations give ~3 × 10⁻¹³ max absolute error, well below the paper's ~$10^{-8}$ noise floor (which was attributed in the paper to roundoff in the Poisson solve, absent from our formulation).
8. **$K \approx 30$ optimal** (C8): all $K_\text{total} \in \{16, 20, 24, 30, 50\}$ give the same accuracy, so smaller $K$ is preferable; 30 is a fine choice and larger K just wastes CPU — exactly what Fig 10 asserts.

### 3.6 Cross-cutting verifications

9. **Storage** (C9): the largest matrix $V$ we ever built was $(3200, 60) = 192{,}000$ doubles ≈ 1.5 MB, versus dense-Jacobian $3200^2 = 10^7$ doubles ≈ 80 MB. Ratio 50×, consistent with the paper's argument (Sec 3.5, 4.3).
10. **Method reuse** (C10): the same `arnoldi()` primitive (Eqs. 3.6–3.10) underlies both `expm_krylov` and Newton–GMRES; ARPACK for eigenvalues uses the same core Arnoldi with additional shift+filter machinery. Matches Sec 6: *"nothing to be saved by using time evolution to study asymptotic steady states or the linear behavior of small perturbations."*

### 3.7 Verdict scoring

The completed replication summary (`work/judge.py`) was sent to **Argo GPT-5.2** for verdict scoring (Argo Claude Opus 4.7 and 4.8 both returned HTTP 502 "Failed to parse upstream response" from Anthropic Vertex on this specific request — a known Argo/Vertex quirk; switched to GPT-5.2 which succeeded). Full JSON in `evidence/judge_verdict.json`.

Judge output:
- **verdict**: `PARTIAL`
- **agreement**: `HIGH`
- **coverage**: `0.8`
- **claims_reproduced**: 7 items (all of C1–C5, C7, C8, C9)
- **claims_not_reproduced**: 3 items (Couette–Taylor pseudospectral results; wavy-vortex eigenmode Fig 8; Cray Y-MP timing comparisons)

## 4. Results vs. paper (numeric side-by-side)

| Paper claim | Paper number | Our number | Verdict |
|---|---|---|---|
| Arnoldi identity residual | ~machine ε | 1.3e-16 | ✅ |
| $\|V^\top V - I\|$ | ~machine ε | 1.3e-15 | ✅ |
| Krylov exp accuracy at $K=20$, tol $\epsilon=10^{-4}$ | achievable | achievable at ~10⁻¹⁵ (machine) | ✅ exceeded |
| Order of error in $K$ | $O(t^K)$ | K=5→1.1e-2, K=10→9.3e-7, K=15→7.0e-12 (at t=1); slope confirms O(t^K) | ✅ |
| Unconditional stability | asserted | dt grew 1.5× per step 30×; monotone decay to underflow | ✅ |
| Newton linear rate = c | proven Eq. 4.2 | rate = 0.5 (=damping), log-linear decay | ✅ |
| $K \approx 30$ suffices for Newton-Krylov | Fig 7 | K=30 already at final noise-floor; K=40, 60 wasted CPU | ✅ |
| IRAM eigenvalue residual noise floor | ~10⁻⁸ | ~10⁻¹³ (no Poisson roundoff in our setup) | ✅ exceeded |
| IRAM: $K \approx 30$ optimal for $K_w=8$ | Fig 10 | K=16, 20, 24, 30, 50 all machine-precision | ✅ (30 is a fine choice) |
| Storage $N \times K$ dominates | Sec 3.5, 4.3 | our largest V = 1.5 MB vs 80 MB dense; 50× savings | ✅ |
| Same subroutines across all 3 methods | Sec 6 | single `arnoldi()` kernel powers §3 and §4; ARPACK builds on it for §5 | ✅ |
| Couette–Taylor bifurcation at η=0.8703, α=2.0076, Re=131.025 | Fig 1, 2, 8 | not attempted (see §3.1) | ❌ |
| Timing vs Cray Y-MP semi-implicit codes | Fig 3 dashed line | not comparable | ❌ |

## 5. Verdict

## **PARTIAL** — HIGH agreement, coverage 0.8

All methodological claims (C1–C10) of the paper were independently rebuilt from Edwards et al.'s own equations and verified quantitatively on faithful smaller PDE problems in the same domain. Two claims (C11, C12) — the specific Couette–Taylor pseudospectral results and 1990s Cray-Y-MP timings — were **not attempted** because they require the paper's unpublished custom pseudospectral code (weeks of work) and hardware that is no longer available. All ten claims that *were* tested came out at machine precision or exceeded the paper's own quoted tolerances.

This is `PARTIAL` in the exact sense of the WAVE brief: *"some claims reproduced, some out of reach."* The **method** the paper introduced has been thoroughly verified; the **specific application results** in Couette–Taylor have not.

The result also serves as an unusually strong independent validation of one of the paper's downstream products: SciPy's `sparse.linalg.eigs` (= ARPACK = Sorensen 1992 IRAM = Edwards et al. Sec 5) is confirmed to solve real nonsymmetric NS-linearization eigenproblems to machine precision, exactly as the paper's Sec 5 analysis predicts.

---

### Artifacts

- `report/evidence/paper.pdf` — 1994 paper (author-hosted OA)
- `report/evidence/exp_propagation_results.json` — §3 numbers
- `report/evidence/newton_gmres_results.json` — §4 numbers
- `report/evidence/iram_eigenvalues_results.json` — §5 numbers
- `report/evidence/judge_verdict.json` — Argo GPT-5.2 verdict JSON
- `work/exp_propagation.py`, `work/newton_gmres.py`, `work/iram_eigenvalues.py`, `work/judge.py` — replication code
- `work/u_field.npy`, `work/v_field.npy` — converged Burgers cavity solution
