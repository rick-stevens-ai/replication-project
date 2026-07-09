# REPORT — The Finite Element Approximation of the Nonlinear Poisson–Boltzmann Equation
## Chen, Holst, Xu — SIAM J. Numer. Anal. 45(6):2298–2320 (2007) — DOI 10.1137/060675514 — arXiv 1001.1350

## 1. Paper summary

Chen, Holst, and Xu develop and analyze a finite-element discretization for the nonlinear Poisson–Boltzmann equation (PBE), a foundational electrostatics model in biomolecular modeling:

$$-\nabla\!\cdot\!(\varepsilon \nabla \tilde u) + \bar\kappa^2 \sinh(\tilde u) \;=\; \sum_{i=1}^{N_m} q_i \,\delta_{x_i}, \qquad \tilde u(\infty)=0,$$

on ℝ² or ℝ³, with piecewise-constant ε (ε_m ≈ 2 in the biomolecule region Ω_m, ε_s ≈ 80 in the solvent) and κ̄² = ε_s κ² on Ω_s, 0 on Ω_m.

The key difficulty is that the delta sources are **not** in H⁻¹, so standard FEM error theory cannot be applied to the raw equation. The paper's key device is a **regularization by singular subtraction**: let G(x) = Σ q_i / (ε_m |x − x_i|) solve −∇·(ε_m ∇G) = Σ q_i δ_i on ℝ^d. Setting ũ = u + G decouples the singularities into a known, closed-form G, leaving u to satisfy the **regularized PBE (RPBE)** (paper eq. 3.5):

$$-\nabla\!\cdot\!(\varepsilon \nabla u) + \bar\kappa^2\sinh(u+G) = \nabla\!\cdot\!\big((\varepsilon-\varepsilon_m)\nabla G\big) \quad\text{in }\Omega,\qquad u = g - G\;\text{on }\partial\Omega.$$

The RHS now lives in H⁻¹ (its support is Ω_s only), so u ∈ H¹ and standard variational methods apply. A further split u = uˡ + uⁿ (paper eqs. 3.7–3.10) writes uˡ as a linear elliptic solve with source `∇·((ε-ε_m)∇G)` and uⁿ as a nonlinear elliptic solve with sinh reaction. The paper's principal analytical results are:

- **Theorem 6.2 (quasi-optimal a priori H¹ error estimate)**: for the RPBE FEM solution u_h,
  $$\|u - u_h\|_1 \lesssim \inf_{v_h \in V^h}\|u - v_h\|_1.$$
- **Theorems 6.3, 6.4 (discrete L∞ boundedness)**: under an M-matrix-type grid assumption (A1), ‖u_h‖_∞ ≤ C independent of h.
- **Theorems 7.1–7.7 (a-posteriori estimate + convergent AFEM)**: a residual-type estimator drives an adaptive-refinement loop that provably converges.

## 2. Claims table

| ID  | Claim | Type | Testable computationally? | Tested in this replication? |
|-----|-------|------|:---:|:---:|
| C1  | RPBE regularization (ũ = u + G) with G = Σ q_i/(ε_m\|x−x_i\|) is well-posed in H¹; the RHS `∇·((ε-ε_m)∇G)` ∈ H⁻¹ has support in Ω_s only. | analytical + computational | Partially (well-posedness proven mathematically; a discrete solve confirms finite-energy behaviour). | **Yes** (Test B). |
| C2  | Split u = uˡ + uⁿ decouples the linear singularity-lifting part from the nonlinear sinh solve. | computational | Yes. | **Yes** (Test B: uˡ and uⁿ solved separately, each converging). |
| C3  | **Thm 6.2 quasi-optimal H¹ estimate** ⇒ for P1 elements on H²-smooth solutions, ‖u−u_h‖_L2 = O(h²), \|u−u_h\|_H1 = O(h). | computational | Directly testable via a manufactured-solution convergence sweep. | **Yes** (Test A: rates → 2.000, 1.000). |
| C4  | Discrete L∞ bound ‖u_h‖_∞ ≤ C indep. of h under grid assumption (A1). | computational | Requires M-matrix-conforming meshes + L∞ tracking. | **No** (not tested; flagged). |
| C5  | AFEM based on section 7 estimator converges. | computational | Requires full estimator + Dörfler marking + refinement loop. | **No** (not tested; flagged). |

## 3. Method

### 3.1 Data & software
- **Paper source**: `https://arxiv.org/pdf/1001.1350` (author preprint of the SIAM paper). SHA-256 recorded in `artifact_harvest.md`.
- **FEM stack**: `scikit-fem` 12.0.2 (P1 Lagrange elements on triangles), `numpy` 2.5.1, `scipy` 1.18.0 (sparse direct solve via `spsolve`). Fully OSS.
- **LLM judge**: `argo:gpt-5` via the local Argo proxy (`http://127.0.0.1:44497/v1`, key `stevens`). Free ANL endpoint.

### 3.2 Test A — manufactured-solution convergence test (checks C3)
- Domain: Ω = (0,1)². Element: P1 on `MeshTri` obtained by iteratively refining a 2-triangle base mesh (levels 1…7 → h = 2⁻¹…2⁻⁷).
- Coefficients: ε ≡ 80 on Ω (uniform, isolating the pure convergence-rate test from interface complications), κ̄² = 80, one atom placed at x₀ = (−1.5,−1.5) *outside* Ω so G is C^∞ on Ω (matching Theorem 6.2's smoothness setup).
- Exact solution: u_ex(x,y) = sin(πx) sin(πy). RHS `f = −ε Δu_ex + κ̄² sinh(u_ex + G)` computed analytically at every quadrature point.
- Newton loop: damped-step Newton, boundary-condensed sparse solve, tolerance `|du|_2 < 1e-10`.
- Errors reported in `L²`, `H¹` semi-norm and `H¹` full norm using skfem's built-in quadrature via `basis.interpolate(u_h).grad`.
- Code: `work/rpbe_mms.py`. Run: `python rpbe_mms.py > report/evidence/rpbe_mms_run.log`.

### 3.3 Test B — two-atom RPBE with the paper's uˡ + uⁿ split (checks C1, C2)
- Domain: Ω = (−1,1)² with a 2D "molecule" region Ω_m = { |x|<0.2, |y|<0.2 } and Ω_s = Ω \ Ω_m.
- Coefficients: ε_m = 2, ε_s = 80, κ̄²_s = 80 (0 in Ω_m). Two atoms (a dipole) with q = (+1, −1) at x = (±0.1, 0). All inside Ω_m so their contribution enters through G only, as prescribed by the regularization.
- Solve:
  1. **Linear step (paper eq. 3.7)**: `−∇·(ε∇uˡ) = ∇·((ε−ε_m)∇G)` on Ω, `uˡ = 0` on ∂Ω. Weak form: `∫ ε ∇uˡ·∇v = ∫ (ε−ε_m) ∇G·∇v` (integration by parts of the RHS; note ε−ε_m has support on Ω_s only).
  2. **Nonlinear step (paper eq. 3.9)**: `−∇·(ε∇uⁿ) + κ̄² sinh(uⁿ + uˡ + G) = 0`, `uⁿ = g − G` on ∂Ω. For this schematic test we chose `g = G` on ∂Ω (so `uⁿ|_∂Ω = 0`), the cleanest choice that keeps the reaction term nontrivial.
- Damped Newton with residual-based backtracking (α → α/2 if the argument of sinh would swing by ≥ 50× the current level). Newton iterations 3–5, quadratic convergence at each level.
- Diagnostics: total energy `E(uⁿ) = ½ ∫ ε|∇uⁿ|² + ∫ κ̄² cosh(uⁿ+uˡ+G)` tracked per iteration; H¹-norm-difference across consecutive refinement levels as Cauchy-in-h proxy; probed value of ũ = u + G at a solvent-far point (0.9, 0.9) checked for smoothness.
- Code: `work/rpbe_twoatom.py`. Run: `python rpbe_twoatom.py > report/evidence/rpbe_twoatom_run.log`.

## 4. Results vs paper

### 4.1 Test A — convergence rates (evidence: `rpbe_mms_results.json`, `rpbe_mms_run.log`)

| level | h | ndof | \|e\|_L2 | rate L2 | \|e\|_H1 | rate H1 |
|:---:|:---:|---:|---:|:---:|---:|:---:|
| 1 | 0.500 | 9      | 2.448e−01 | —      | 1.522e+00 | —      |
| 2 | 0.250 | 25     | 7.566e−02 | 1.694  | 8.422e−01 | 0.854 |
| 3 | 0.125 | 81     | 2.003e−02 | 1.917  | 4.323e−01 | 0.962 |
| 4 | 0.062 | 289    | 5.084e−03 | 1.978  | 2.176e−01 | 0.990 |
| 5 | 0.031 | 1 089  | 1.276e−03 | 1.994  | 1.090e−01 | 0.998 |
| 6 | 0.016 | 4 225  | 3.193e−04 | 1.999  | 5.451e−02 | 0.999 |
| 7 | 0.008 | 16 641 | 7.983e−05 | **2.000** | 2.726e−02 | **1.000** |

**Empirical rates converge to exactly the theory**: L² → 2.000, H¹ → 1.000. This is the standard best-possible rate for P1 elements on H²-regular solutions, and it is what Theorem 6.2's quasi-optimal bound predicts once combined with the Bramble–Hilbert P1 interpolation estimate. Newton behaved textbook-quadratically at every level (residual reduced ~1e2 → 1e-13 in 3–4 steps).

### 4.2 Test B — two-atom RPBE split (evidence: `rpbe_twoatom_results.json`, `rpbe_twoatom_run.log`)

| level | h | ndof | \|uˡ\|_H1 | \|uⁿ\|_H1 | Newton iters | energy monotone? | E first → last | H¹-Cauchy-diff vs prev |
|:---:|:---:|---:|---:|---:|:---:|:---:|:---:|---:|
| 1 | 1.000 | 13     | 3.75e−02 | 9.50e−02 | 3 | ✅ | 3.227e+02 → 3.223e+02 | —     |
| 2 | 0.500 | 41     | 9.80e−01 | 1.79e−01 | 3 | ✅ | 3.344e+02 → 3.334e+02 | 7.99e−01 |
| 3 | 0.250 | 145    | 4.82e+00 | 3.67e−01 | 4 | ✅ | 3.461e+02 → 3.426e+02 | 3.66e+00 |
| 4 | 0.125 | 545    | 6.42e+00 | 6.75e−01 | 4 | ✅ | 3.882e+02 → 3.776e+02 | 1.29e+00 |
| 5 | 0.062 | 2 113  | 7.37e+00 | 9.86e−01 | 5 | ✅ | 4.381e+02 → 4.141e+02 | 7.02e−01 |
| 6 | 0.031 | 8 321  | 7.46e+00 | 9.59e−01 | 5 | ✅ | 4.305e+02 → 4.083e+02 | **1.34e−01** |

Observations:
- **Energy strictly monotonically decreasing along Newton at every level** (paper's Lemma 4.1: u minimises the energy). ✅
- **|uˡ|_H1 saturates around 7.4–7.5** once h ≤ 1/16 begins resolving the singular structure near the atoms; the transient growth from level 2 → 4 is the mesh capturing the near-atom G-gradient (expected).
- **H¹-Cauchy-diff drops rapidly** once the near-atom region is resolved (0.80 → 3.66 [peak: resolution phase] → 1.29 → 0.70 → 0.13), consistent with mesh convergence.
- **Newton converges in 3–5 iterations** with quadratic residual reduction at every level, corroborating the paper's monotone-bounded-cosh Jacobian structure (Lemma 6.1).
- ũ probed at (0.9, 0.9) is finite and mild (~−0.034…−0.037), as expected for a dipole seen from far away.

### 4.3 Not exercised
- **C4** (discrete L∞ boundedness): the paper needs M-matrix-conforming meshes ("5-tet cube split", Figure 1) which scikit-fem does not natively assemble; deferred.
- **C5** (adaptive-FEM convergence): implementing the section-7 estimator + a Dörfler marking loop was out of scope for the wave.

## 5. Verdict

**PARTIAL**  *(via LLM judge `argo:gpt-5` — full response in `report/evidence/judge_verdict.md`)*

**One-line summary (LLM judge)**: *Optimal rates and a stable linear/nonlinear split were reproduced on uniform meshes, but L∞ bounds and adaptive convergence were not tested.*

**Per-claim** (LLM judge, condensed):
- **C1** — partially supported: discrete RPBE solved cleanly with singular internal sources; well-posedness *theorems* obviously cannot be checked computationally, but the empirical evidence is consistent.
- **C2** — supported in practice: uˡ + uⁿ split implemented per paper; both parts converge, uⁿ Newton exhibits full quadratic behaviour.
- **C3** — **strongly supported**: manufactured-solution rates match `O(h²)`, `O(h)` to 4 significant figures at level 7. Theorem 6.2's quasi-optimality is directly corroborated.
- **C4** — not tested.
- **C5** — not tested.

**Justification** (LLM judge): "The replication provides strong empirical confirmation of the optimal convergence rates predicted by Theorem 6.2 and demonstrates that the linear/nonlinear split is numerically effective with robust Newton convergence. It also shows that the regularized formulation handles internal point charges without numerical pathologies. However, the discrete L∞ bounds and adaptive estimator convergence were not evaluated, and the theoretical well-posedness aspects cannot be fully proven computationally."

## 6. Reproducibility

```
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Chen-Holst-Xu-FEM-nonlinear-PB-2007/work
python3 -m venv .venv && source .venv/bin/activate
pip install scikit-fem numpy scipy
python rpbe_mms.py         # ~1 second wall
python rpbe_twoatom.py     # ~1 second wall
python judge.py            # requires local Argo proxy on :44497
```

Wall-clock for the full replication: **~5 s** compute + LLM judge call. No GPU needed. All resources public/free.
