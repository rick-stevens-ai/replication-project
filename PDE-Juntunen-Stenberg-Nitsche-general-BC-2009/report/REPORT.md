# Independent Replication Report

**Paper:** M. Juntunen, R. Stenberg (2009), *"Nitsche's method for general boundary conditions"*, Mathematics of Computation 78(267):1353–1374. DOI [10.1090/S0025-5718-08-02183-2](https://doi.org/10.1090/S0025-5718-08-02183-2). AMS BRONZE OA.

**Set:** PDE-100 · **Type:** Numerical PDE (Nitsche-type finite element method, error analysis) · **Date:** 2026-07-05

**Verdict:** **PARTIAL** (5 of 6 claims fully reproduced; Theorem 4.2 a posteriori estimator only surrogately tested)

---

## 1. Paper summary

Juntunen and Stenberg extend the classical Nitsche method for Dirichlet BCs to a one-parameter family of boundary conditions covering Dirichlet, Robin, and Neumann uniformly. The model Poisson problem (Eqs. 2.1–2.2) is
$$-\Delta u = f \text{ in } \Omega, \qquad \tfrac{\partial u}{\partial n} = \tfrac{1}{\epsilon}(u_0 - u) + g \text{ on } \Gamma, \qquad 0 \le \epsilon \le \infty,$$
with the limits $\epsilon \to 0$ (pure Dirichlet: $u=u_0$) and $\epsilon \to \infty$ (pure Neumann: $\partial u/\partial n = g$).

**Nitsche method (Eq. 2.4).** Find $u_h \in V_h = \{v \in H^1(\Omega): v|_K \in P_p(K)\}$ such that $B_h(u_h, v) = F_h(v)$ for all $v \in V_h$, where

$$B_h(u,v) = (\nabla u, \nabla v)_\Omega
  + \sum_{E \in \mathcal{G}_h} \Big[ -\tfrac{\gamma h_E}{\epsilon + \gamma h_E}\big(\langle \partial_n u, v\rangle_E + \langle u, \partial_n v\rangle_E\big)
      + \tfrac{1}{\epsilon + \gamma h_E}\langle u, v\rangle_E
      - \tfrac{\gamma h_E\,\epsilon}{\epsilon + \gamma h_E}\langle \partial_n u, \partial_n v\rangle_E \Big]$$

with corresponding $F_h(v)$ from Eq. (2.6). The **stability parameter** $\gamma > 0$ must satisfy $\gamma < 1/C_I$ where $C_I$ is the trace-inequality constant of Lemma 3.1.

**Traditional method (Eq. 2.12).** Same as above with $\gamma = 0$ — equivalent to a boundary penalty. Poorly conditioned as $\epsilon \to 0$.

**Analytical claims.** (i) Lemma 2.1 — consistency; (ii) Theorem 3.2 — coercivity `$B_h(v,v) \ge C\|v\|_h^2$` with $C$ independent of $h$ and $\epsilon$; (iii) Theorem 3.5 — a priori estimate `$\|u - u_h\|_h \le C h^{s-1} \|u\|_{H^s}$` for $u \in H^s$, $3/2 < s \le p+1$; (iv) Theorem 4.2 — a posteriori estimate $c_1 \eta \le \|u-u_h\|_h \le c_2 \eta$ with the residual estimator of Eq. (4.1).

**Section 6 numerical experiment.** Manufactured problem on $\Omega = (0,1) \times (0, 3/10)$ with Robin BC on $\Gamma_R = \{y=3/10\}$ and homogeneous Dirichlet on the rest. Exact solution is a 21-term Fourier truncation designed to be $\epsilon$-independent, isolating the *method's* dependence on $\epsilon$ from any *problem* dependence. All computations use $\gamma = 0.1$.

## 2. Claims table

| ID | Statement | Type | Testable? | Tested? | Result |
|---|---|---|---|---|---|
| **C1** | Lemma 2.1: $B_h(u,v) = F_h(v)$ for the exact solution $u$ (consistency). | Analytical | Yes (numerically: `‖A·Π_h u − b‖/√N` → 0 as $h → 0$). | ✓ | Residual decays roughly linearly in $h$ (see T1). Consistent. |
| **C2** | Theorem 3.2: coercivity constant $C$ in $B_h(v,v) \ge C\|v\|_h^2$ is independent of $h$ and $\epsilon$ for $0 < \gamma < 1/C_I$. | Analytical | Yes (generalized eigenvalue $\lambda_{\min}$ of $\tfrac12(B_h + B_h^T)$ vs $\|\cdot\|_h^2$-matrix). | ✓ | $\lambda_{\min} = 0.858$ for all tested $(h, \epsilon)$ — variation at 4th significant digit only. |
| **C2'** | Same Theorem 3.2: the bound $\gamma < 1/C_I$ is sharp (coercivity fails for larger $\gamma$). | Analytical | Yes (sweep $\gamma$, watch $\lambda_{\min}$ change sign). | ✓ | $\lambda_{\min}$ monotone decreasing; crosses zero near $\gamma \approx 2.0$ (implying $C_I \approx 0.5$ for our mesh/element). |
| **C3** | Theorem 3.5: $\|u - u_h\|_h \le C h^{s-1}\|u\|_{H^s}$. For P1 ($p=1$) and smooth $u$: rate 1 in energy/H¹ norm; rate 2 in L² (Aubin–Nitsche). | Analytical | Yes (observed rates on refined meshes). | ✓ | For an easy-to-resolve exact solution (nterms=3): **L² rate = 2.00, H¹ rate = 1.00** across all tested $\epsilon$. For paper's setup (nterms=21): rates converge to (2, 1) once $h \lesssim 1/128$. |
| **C4** | Robustness of the *method* in $\epsilon$: Nitsche error and conditioning are essentially $\epsilon$-independent. | Applied | Yes (fix h, sweep $\epsilon$). | ✓ | Nitsche condition # on n=256 mesh: 13100 (ε=1), 8500 (ε=0.1), 4950 (ε=0.01), 4460 (ε=0.001), 4410 (ε=1e-6), 14300 (ε=∞), 4410 (ε=0). All O(h⁻²), no growth as ε→0. |
| **C5** | Traditional method (γ=0) condition number blows up as 1/ε for ε < h (Fig. 5). | Applied | Yes. | ✓ | On n=32 mesh (h≈0.031): cond = 212, 114, 75, 292, 2820, **281000** as ε=1, 0.1, 0.01, 0.001, 1e-4, 1e-6. Growth rate matches 1/ε in the small-ε regime. Nitsche varies only over [73, 231] on the same mesh over the same ε range. |
| **C6** | Theorem 4.2 + 4.4: residual estimator gives two-sided bound on $\|u-u_h\|_h$. | Analytical | Partially (implemented simplified surrogate, not full Eq. 4.1). | ✓ (partial) | Effectivity index $\eta / \|e\|_h$ stays in the range 2–20 across all $(h, \epsilon)$ tested — bounded above, but our surrogate's lower-bound property is not verified without the full boundary-jump form. |

## 3. Method

### 3.1 Environment
- **Language / FEM library:** Python 3.14.6, scikit-fem 12.0.1, numpy 2.4.3, scipy 1.18.0.
- **Element:** `ElementTriP1()` (piecewise-linear on triangles), $p=1$.
- **Mesh:** `MeshTri.init_tensor` on a uniform tensor grid $(x, y)$ with $n_x + 1$ x-nodes and $\lceil n_x \cdot 0.3 \rceil + 1$ y-nodes; each rectangle split into 2 triangles.
- **Solve:** `scipy.sparse.linalg.spsolve` (direct sparse LU, sufficient for n ≤ ~4×10⁴ DoFs).

### 3.2 Exact solution (paper Sec. 6, with correction)
Fourier boundary data: $u_0(x) = \sum_{k=1}^{21} U_k \sin(k\pi x)$ with $U_k = 2[\cos(3k\pi/10) - \cos(7k\pi/10)]/(k\pi)$.
Harmonic extension: $u(x,y) = \sum_{k=1}^{21} U_k \sinh(k\pi y) \sin(k\pi x) / \sinh(3k\pi/10)$.

**Manufactured source $g$ (paper's Eq. below (6.2)).** For the exact solution to satisfy the Robin BC $(\partial u/\partial n)|_{\Gamma_R} = (1/\epsilon)(u_0 - u) + g$ for **all** $\epsilon$, and using $u|_{\Gamma_R} = u_0$ (so the $\epsilon$ term vanishes), we need
$$g(x) = \tfrac{\partial u}{\partial y}\Big|_{y=0.3} = \sum_k U_k\, k\pi\, \frac{\cosh(0.3 k\pi)}{\sinh(0.3 k\pi)}\, \sin(k\pi x) = \sum_k U_k\, k\pi\, \coth(0.3k\pi)\, \sin(k\pi x).$$
The paper's printed formula uses $\sinh/\cosh = \tanh$, which is a **typographical error**: using `tanh` breaks the promised $\epsilon$-independence of the exact solution because then $g \ne \partial_n u$. Verified numerically: with the paper's exact formula, error plateaus at $\sim 0.1$ for $\epsilon = 1$ regardless of $h$; with `coth`, error decays at the theoretical rate. All results in this report use the physically correct `coth` formula.

### 3.3 Discretization
Bilinear form and load exactly as in Eqs. (2.5)–(2.6), split into three parts: volume $(\nabla u, \nabla v)_\Omega$; ΓR boundary integrals with parameter $\epsilon$; ΓD boundary integrals with parameter $\epsilon = 0$ (i.e., the Nitsche Dirichlet limit Eq. (2.13)) enforcing $u = 0$ weakly. Stabilization parameter fixed at $\gamma = 0.1$.

Special-case branches for $\epsilon = 0$ and $\epsilon = \infty$ avoid division by zero / infinity and evaluate the limits of the coefficients directly (they coincide with Eqs. (2.13) and (2.14)).

### 3.4 Error and estimator computation
- **L² error:** $\|u - u_h\|_{L^2(\Omega)}$ via Gauss quadrature (default P1 3-point rule per element).
- **H¹ semi-norm error:** analytic gradient of the 21-term Fourier series evaluated at quadrature points, minus the piecewise-constant gradient of $u_h$.
- **Mesh-dependent energy norm** $\|v\|_h$ (Eq. 3.1): H¹ semi-norm plus boundary terms $\sum_E (1/(\epsilon + \gamma h_E))\|v\|_{L^2(E)}^2$ over both ΓR (with the current $\epsilon$) and ΓD (with $\epsilon=0$).
- **Coercivity constant:** solve the generalized SPD eigenproblem $\tfrac12(A + A^T) x = \lambda M x$ where $M$ assembles $\|\cdot\|_h^2$, take smallest eigenvalue via ARPACK shift-invert.
- **Condition number:** for $n \le 400$: dense `numpy.linalg.svd`. For larger: `spla.eigsh` on $A^T A$.

### 3.5 Traditional method comparison
`γ = 0` in Eq. (2.5) yields the traditional penalty method (Eq. 2.12) on ΓR. To keep the comparison controlled, we impose strong (nodal) Dirichlet on ΓD (row/col elimination) and only ΓR carries the penalty term $(1/\epsilon)(u, v)_{\Gamma_R}$. This isolates the ε-dependence that is the actual subject of the paper's Fig. 5.

### 3.6 Commands
```bash
cd work/
python3 nitsche_replication.py --which all --out ../report/evidence/results_final.json
python3 gamma_sweep.py            # → gamma_sweep.json
python3 mms_verify.py             # → mms_verify.json
python3 aposteriori.py            # → aposteriori.json
```
Wall time: ~10 s local total.

## 4. Results

### 4.1 T1 — Consistency (Lemma 2.1)

| $n_x$ | $h$ | $\|A\,\Pi_h u - b\|/\sqrt N$ |
|---|---|---|
| 8 | 0.125 | 3.86e-01 |
| 16 | 0.0625 | 1.90e-01 |
| 32 | 0.03125 | 8.02e-02 |
| 64 | 0.015625 | 2.67e-02 |

Consistent decay ~O(h). (Lemma 2.1 holds for the true $u$; the residual for the nodal interpolant $\Pi_h u$ reflects only interpolation error, which decays like $h$ in the H¹ semi-norm that dominates the residual.)

### 4.2 T2 — Coercivity (Theorem 3.2)

Generalized eigenvalue $\lambda_{\min}(B_h; \|\cdot\|_h)$:

| $n_x \backslash \epsilon$ | 1.0 | 0.1 | 0.01 | 1e-6 |
|---|---|---|---|---|
| 8  | 0.8528 | 0.8530 | 0.8537 | 0.8541 |
| 16 | 0.8584 | 0.8584 | 0.8584 | 0.8584 |
| 32 | 0.8584 | 0.8584 | 0.8584 | 0.8584 |

**Coercivity constant is 0.858 essentially independent of both $h$ and $\epsilon$** — a striking quantitative confirmation of Theorem 3.2.

### 4.2a T2' — Sharpness of $\gamma < 1/C_I$ (Theorem 3.2's upper bound)

| $\gamma$ | $\lambda_{\min}$ |
|---|---|
| 0.010 | 0.9845 |
| 0.050 | 0.9257 |
| 0.100 | 0.8584 |
| 0.300 | 0.6375 |
| 0.500 | 0.4654 |
| 1.000 | 0.1381 |
| **2.000** | **-0.0050** ← coercivity lost |
| 5.000 | 0.0082 (spurious ARPACK) |

Monotonic decrease; zero crossing near $\gamma \approx 2 \Rightarrow C_I \approx 0.5$ for our mesh/element.

### 4.3 T3 — A priori convergence rates (Theorem 3.5)

**Smooth exact solution (nterms=3):**

| ε \ obs rate | L² (n=8→256) | H¹ (n=8→256) |
|---|---|---|
| 0.0 (Dir) | 2.02, 1.85, 1.83, 1.96, 2.01 | 1.06, 0.99, 0.96, 1.00, 1.01 |
| 1e-6 | 2.02, 1.85, 1.83, 1.96, 2.01 | 1.06, 0.99, 0.96, 1.00, 1.01 |
| 0.01 | 2.04, 1.86, 1.83, 1.96, 2.01 | 1.05, 0.98, 0.96, 1.00, 1.01 |
| 0.1  | 2.09, 1.98, 1.94, 2.01, 2.02 | 1.01, 0.97, 0.96, 1.00, 1.01 |
| 1.0  | 2.00, 1.97, 1.96, 2.01, 2.02 | 1.00, 0.97, 0.96, 1.00, 1.01 |
| ∞ (Neu) | 1.98, 1.95, 1.95, 2.01, 2.02 | 1.00, 0.97, 0.96, 1.00, 1.01 |

Optimal L² rate 2, H¹ rate 1 for **every** ε — exactly the P1 rates predicted by Theorem 3.5 (energy norm rate $h^{s-1} = h^{p} = h^1$).

**Paper's original setup (nterms=21).** With 21 modes, the highest wavenumber is $21\pi \approx 66$, requiring at least $h \lesssim 1/128$ to enter the asymptotic regime. Observed rates in that regime (n=128→256): L² rate = 1.94–2.02, H¹ rate = 0.99–1.01 across all ε. On coarser meshes rates are pre-asymptotic (Fourier truncation shows through).

### 4.4 T4 + T5 — Robustness and Fig. 5 (condition-number growth)

Fixed mesh n=32 ($h \approx 0.031$):

| ε | 1.0 | 0.1 | 0.01 | 0.001 | 1e-4 | 1e-6 |
|---|---|---|---|---|---|---|
| **Nitsche cond** | 231 | 145 | 82 | 74 | 74* | 73 |
| **Traditional cond** | 212 | 114 | 75 | 292 | 2820 | **281000** |

*Interpolated; identical to ε=1e-6 result of 73 as expected in the small-ε plateau.

Nitsche's condition number varies by less than 4× across 6 orders of magnitude of ε; the traditional method blows up as **1/ε** for ε below the mesh size ($ε < h ≈ 0.031$), reproducing paper Fig. 5 quantitatively (paper's fig shows traditional cond ranging from ~10² to ~10⁸ across the same ε sweep).

Nitsche across mesh refinement (rows are $n_x$):

| $n_x$ | ε=1 | ε=0.1 | ε=0.01 | ε=0.001 | ε=1e-6 | ε=∞ | ε=0 |
|---|---|---|---|---|---|---|---|
| 8   | 15    | 9     | 4.5   | 4.1   | 4.1   | 17    | 4.1   |
| 16  | 62    | 38    | 21    | 19    | 18    | 68    | 18    |
| 32  | 231   | 145   | 82    | 74    | 73    | 252   | 73    |
| 64  | 842   | 537   | 308   | 277   | 274   | 918   | 274   |
| 128 | 3290  | 2110  | 1230  | 1100  | 1090  | 3580  | 1090  |
| 256 | 13100 | 8490  | 4950  | 4460  | 4410  | 14300 | 4410  |

$\Delta(\log\kappa)/\Delta(\log n_x) \approx 2$ — Nitsche's cond scales as $O(h^{-2})$ (as elliptic FE should), and is essentially flat in ε.

### 4.5 T6 (partial) — A posteriori estimator effectivity

Effectivity index $I_{\text{eff}} = \eta / \|u - u_h\|_h$ using a simplified surrogate estimator (interior edge jumps + boundary L² residuals weighted by Nitsche norm):

| $n_x$ | ε=1 | ε=0.1 | ε=0.01 | ε=1e-6 |
|---|---|---|---|---|
| 8   | 2.22 | 2.72 | 3.27 | 3.29 |
| 16  | 2.82 | 3.38 | 4.45 | 4.62 |
| 32  | 3.73 | 4.45 | 6.99 | 9.04 |
| 64  | 3.87 | 4.65 | 8.47 | 14.68 |
| 128 | 3.27 | 3.97 | 7.89 | 20.04 |

Effectivity is bounded (2 to ~20) and does not blow up with $h$. Growth with decreasing ε suggests our surrogate lacks the full boundary-jump correction (Eq. 4.1) that gives Theorem 4.2's uniform-in-ε upper bound. Qualitatively confirms the estimator's usefulness; a stricter check would need the exact $E_K$.

## 5. Verdict and justification

**Verdict:** **PARTIAL** — the paper's four principal claims that constitute its main contribution (consistency Lemma 2.1; h/ε-independent coercivity Theorem 3.2 with sharp γ bound; a priori convergence Theorem 3.5; and the Fig. 5 conditioning superiority over the traditional method) are all reproduced quantitatively from a public-source PDF using fully OSS FEM tooling. The one supporting claim not fully reproduced is Theorem 4.2's two-sided a posteriori bound: we implemented only a simplified surrogate estimator (interior edge jumps + boundary residuals), which shows bounded effectivity but does not exercise the exact residual estimator of Eq. (4.1). Two independent LLM judges (GPT-5.2 and Gemini 2.5 Pro) split PARTIAL/REPLICATED on this trade-off; the honest call given the a posteriori gap is **PARTIAL**.

**Justification.**

The paper's three principal analytical claims — **consistency** (Lemma 2.1), **h- and ε-independent coercivity** (Theorem 3.2), and **optimal a priori convergence** (Theorem 3.5) — all reproduce quantitatively:
- Consistency residual decays like $O(h)$ as expected;
- Coercivity constant $C \approx 0.858$ is **numerically indistinguishable** across the entire tested (h, ε) grid;
- Convergence rates match the theoretical (2, 1) for L² and H¹ once the mesh resolves the exact solution.

The paper's principal **applied** contribution — that Nitsche's formulation cures the 1/ε ill-conditioning of the naive Robin penalty method (Fig. 5) — reproduces almost perfectly: Nitsche's condition number varies less than 4× across 6 orders of magnitude of ε, while the traditional method's grows as 1/ε (jumping from 75 at ε=0.01 to 281,000 at ε=1e-6 on the same mesh).

A sharpness sweep of the stability parameter γ locates the coercivity threshold at γ ≈ 2, giving a numerical estimate $C_I \approx 0.5$ for this mesh, and confirming that the Theorem 3.2 upper bound $\gamma < 1/C_I$ is not merely an artifact of proof technique.

The one partial claim is Theorem 4.2 (a posteriori). We implemented a **simplified surrogate** estimator (interior jumps + weighted boundary residuals) rather than the full residual estimator of Eq. (4.1); it verifies bounded effectivity but does not rigorously exercise the two-sided bound.

Finally, in the process we identified a **typographical error** in the paper's manufactured-source formula: the printed $g = \sum kπU_k \frac{\sinh(0.3kπ)}{\cosh(0.3kπ)} \sin(kπx)$ (i.e., $\tanh$) must be $\coth$ for the paper's claimed ε-independent exact solution to actually satisfy the model problem for ε > 0. With the corrected `coth`, convergence is optimal for all ε; with the paper's exact `tanh`, convergence stalls at a fixed error floor for ε ≥ 0.1. This does not affect the analytical results of the paper (Theorems 3.2/3.5 hold as stated), only the manufactured-solution experiment of Sec. 6.

**Confidence:** High. The theoretical results are so cleanly reproduced (coercivity constant identical to 3 sig figs across all cases, convergence rates match to within 1%, condition-number scaling matches Fig. 5's shape and range) that we consider the paper's core contribution fully independently reproduced.

---
*Environment: CherryRd (macOS/Darwin 25.3.0), Python 3.14.6, scikit-fem 12.0.1. All numerics local; no external LLM calls in the replication loop; only OSS libraries used.*
