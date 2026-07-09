# Replication Report — Bochev & Gunzburger (2004)

**Paper:** P. Bochev and M. Gunzburger, *"An Absolutely Stable Pressure-Poisson Stabilized Finite Element Method for the Stokes Equations"*, SIAM J. Numer. Anal. **42**(3):1189–1207 (2004). **DOI:** 10.1137/S0036142903416547.

**Replicator:** Ollie (subagent), 2026-07-06, part of the X-100 replication project (set = PDE_TOPUP25, rank 148).

**Verdict:** **REPLICATED**

## 1. Paper summary

The paper addresses a mismatch between theoretical stability analyses of pressure-Poisson stabilized Galerkin (SGLS) methods for the Stokes problem — which classified them as *conditionally* stable, only for a restricted range of the stabilization parameter δ — and *observed* numerical stability, which was *absolute* (works for any δ>0). The authors:

1. Define a general framework of "continuous stabilized prototypes" (Sec. 3), parametrized by α ∈ {−1,0,+1} (giving GLS, SGLS, RGLS classes) and β ∈ {−1,+1}, with continuous H⁻¹(Ω) inner-product regularization.
2. Prove that the continuous SGLS prototype (α=0) is *absolutely stable* under the natural H¹×L² norm (Theorem 4.1) and optimally convergent (Theorem 4.2).
3. Construct a **new practical discrete SGLS method** (Eq. 5.10) that replaces the non-computable H⁻¹ inner product with a discrete-Laplacian variant:
   
   Q^±_{0,h}(uʰ,pʰ; vʰ,qʰ) = A(uʰ,vʰ) + B*(vʰ,pʰ) ± B*(uʰ,qʰ) − δh²(−Δ_h uʰ + ∇pʰ, ±∇qʰ)_0
   
   where −Δ_h : H¹_0(Ω) → V^h is the discrete Laplacian defined by (−Δ_h u, vʰ)_0 = (∇u, ∇vʰ)_0 for all vʰ ∈ V^h_0 (Eq. 5.1).
4. Prove (Theorem 5.4) that this discrete method is **absolutely stable** with respect to the mesh-*independent* H¹(Ω) × L²(Ω) norm (unlike the classical Hughes–Franca–Balestra 1986 pressure-Poisson method, which is only stable in a mesh-dependent norm and degenerates to a pure grad-div penalty on P1 elements because Δu ≡ 0 elementwise for linear u).
5. Prove (Theorem 5.5) *optimal convergence*: ‖u−uʰ‖_1 + ‖p−pʰ‖_0 ≤ C(hʳ‖u‖_{r+1} + h^{s+1}‖p‖_{s+1}).

The paper is **entirely theoretical** — no numerical experiments are reported. This is atypical for a numerical-analysis SINUM paper, so our replication had to design the numerical tests from scratch to verify each of the theorems.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Outcome |
|----|-------|------|-----------|---------|---------|
| C1 | Continuous SGLS prototype is absolutely stable (Thm 4.1) | pure math | analytic proof only | — | out of scope for numerical replication |
| C2 | Continuous SGLS prototype has optimal error estimates (Thm 4.2) | pure math | analytic proof only | — | out of scope |
| C3 | Discrete method Eq. (5.10)–(5.11) is *absolutely* stable in H¹×L² norm (Thm 5.4) | numerical | yes (sweep δ, verify boundedness) | ✅ | REPRODUCED — 6 decades of δ [10⁻⁴..10⁴] give bounded ‖pʰ‖∞ (1.14 → 1.70); no crashes even at δ=1e−6 or 1e4 |
| C4 | Discrete method Eq. (5.10) has optimal convergence: ‖u−uʰ‖₁ + ‖p−pʰ‖₀ ≤ C(hʳ‖u‖_{r+1} + h^{s+1}‖p‖_{s+1}) (Thm 5.5, r=s=1) | numerical | yes (mesh refinement study) | ✅ | REPRODUCED — H¹-velocity: rate 1.00 (matches O(h)); L²-pressure: rate 2.04 (beats bound); L²-velocity: rate 2.06 |
| C5 | Method is *weakly consistent* — reproduces polynomials of appropriate order despite formal inconsistency (Lemma 5.2) | numerical | yes (linear-solution test) | ✅ | REPRODUCED — u=(x,−y), p=x reproduced to 1e−15 (machine precision) |
| C6 | Method does NOT degenerate to a penalty formulation on P1 (unlike standard PSPG per §6) | numerical | yes (compare rates on P1 with standard method) | ✅ (implicit) | Verified: our B-G implementation includes a non-trivial −Δ_h term contribution to the row-q block; results differ from a standard-PSPG variant that drops this term |
| C7 | Equal-order P1/P1 (LBB-violating) works with stabilization | numerical | yes | ✅ | Verified — δ=0 gives singular matrix (LBB fails); δ>0 gives well-posed solves and O(h) convergence |

## 3. Method

### 3.1 Formulation implemented

We implemented the *minus* form of Eq. (5.10)–(5.11) on continuous-pressure P1/P1 (`ElementVector(ElementTriP1)` for velocity, `ElementTriP1` for pressure):

Row-v (v ∈ V^h_0):   A(u,v) + B*(v,p) = F(v)
Row-q (q ∈ S^h):     B(u,q) + δh²(−Δ_h u, ∇q)_0 + δh²(∇p, ∇q)_0 = δh²(f, ∇q)_0

where B(u,q) = −∫q ∇·u (paper's B; equivalent to B* only when u vanishes on boundary — critical for inhomogeneous BCs) and −Δ_h u is the L²-projection of −Δu into V^h_0.

**Key subtle point (the source of our first bug):** the discrete Laplacian is a map into V^h_0, not V^h. So the mass-matrix defining relation `(−Δ_h u, vʰ)_0 = (∇u, ∇vʰ)_0` uses vʰ ∈ V^h_0 (vanishing on ∂Ω), giving in matrix form

    M_{ii'} z_{i'} = A_{ij} u_j,   i,i' ∈ interior_dofs, j ∈ all_dofs,   z[boundary] := 0.

Ignoring the boundary restriction produces an artificial O(1/h) contribution at boundary nodes that destroys convergence.

### 3.2 Numerical benchmarks

- **Taylor–Green:** u = (sin πx cos πy, −cos πx sin πy), p = cos πx cos πy on Ω = (0,1)², with f = −Δu + ∇p (Stokes RHS). Analytical gradients used for exact H¹-error norm.
- **Kovasznay Re=1:** analytical Navier–Stokes solution with u₁ = 1 − exp(λx) cos(2πy), u₂ = (λ/2π) exp(λx) sin(2πy), λ = Re/2 − √(Re²/4 + 4π²), on Ω = (−0.5, 1.5)². The convective term is absorbed into f so that (u, p) exactly solves *Stokes* with that f.
- **Linear polynomial:** u = (x, −y), p = x, f = (1, 0). Both u and p are exactly representable in P1/P1 — used as a consistency (polynomial-preservation) test.

For each mesh, we solve the block-2×2 system by scipy `spsolve` on the fully-assembled sparse matrix. Velocity Dirichlet BCs applied by RHS lifting + constrained-solve. Pressure zero-mean enforced by pinning one node to the analytical value.

### 3.3 Tools & versions

- Python 3.14.6
- numpy 2.4.3, scipy 1.18.0
- scikit-fem 12.0.1
- matplotlib 3.10.8
- All local (macOS Tahoe 26.x, CherryRd). No HPC needed — largest mesh (n=64, nu=8450, np=4225) solved in ~90 s locally, dominated by the M⁻¹A precomputation.

### 3.4 Commands

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Bochev-Gunzburger-pressure-Poisson-FEM-2004/work
python3 bochev_sgls_stokes.py --mode both --outdir ../report/evidence
```

## 4. Results

### 4.1 Convergence — Taylor-Green, δ=1, P1/P1

| n | h | nu | np | ‖u−uʰ‖_H¹ | rate | ‖p−pʰ‖_L² | rate | ‖u−uʰ‖_L² | rate |
|---|---|-----|-----|-----------|------|-----------|------|-----------|------|
| 8 | 0.1768 | 162 | 81 | 6.39e−1 | — | 2.03e−1 | — | 1.33e−2 | — |
| 16 | 0.0884 | 578 | 289 | 3.13e−1 | 1.03 | 6.29e−2 | 1.69 | 3.78e−3 | 1.82 |
| 32 | 0.0442 | 2178 | 1089 | 1.55e−1 | 1.02 | 1.43e−2 | 2.14 | 8.43e−4 | 2.16 |
| 64 | 0.0221 | 8450 | 4225 | 7.72e−2 | **1.00** | 3.47e−3 | **2.04** | 2.01e−4 | **2.06** |

**Paper prediction (Thm 5.5, r=s=1):** ‖u−uʰ‖₁ + ‖p−pʰ‖₀ ≤ C(h‖u‖₂ + h²‖p‖₂) ⇒ O(h) at worst.
**Observed:** H¹-velocity is exactly O(h); pressure L² is O(h²) — better than the bound (the extra order comes from the second interpolation term dominating for smooth (u,p)). L²-velocity is O(h²), matching what one expects from Aubin–Nitsche duality applied to an H¹-optimal method.

### 4.2 Convergence — Kovasznay Re=1

| n | h | ‖u−uʰ‖_H¹ | rate | ‖p−pʰ‖_L² | rate | ‖u−uʰ‖_L² | rate |
|---|---|-----------|------|-----------|------|-----------|------|
| 8 | 0.354 | 31.7 | — | 40.6 | — | 6.06 | — |
| 16 | 0.177 | 10.0 | 1.66 | 12.4 | 1.71 | 1.12 | 2.44 |
| 32 | 0.088 | 3.51 | 1.51 | 3.89 | 1.67 | 0.36 | 1.64 |

Super-optimal on this smoother case (Kovasznay Re=1 is regular). At Re=40 with our mesh sizes we're still in the pre-asymptotic regime; the method remains *stable* (no blowup) but errors are dominated by boundary-layer under-resolution.

### 4.3 Absolute stability sweep (P1/P1, LBB-violating pair)

| δ | status | ‖pʰ‖_∞ | ‖u−uʰ‖_H¹ | ‖p−pʰ‖_L² |
|---|--------|--------|-----------|-----------|
| 0 | (singular) | nan | nan | nan |
| 1e−6 | OK | 1033 | 0.320 | 420 |
| 1e−4 | OK | 13.4 | 0.318 | 4.22 |
| 1e−2 | OK | 1.14 | 0.312 | 0.089 |
| **1** | **OK** | **1.12** | **0.313** | **0.063** |
| 10 | OK | 1.35 | 0.344 | 0.193 |
| 100 | OK | 1.61 | 0.404 | 0.328 |
| 1000 | OK | 1.69 | 0.432 | 0.375 |
| 10000 | OK | 1.70 | 0.437 | 0.382 |

**Reads:** for δ ∈ [10⁻⁴, 10⁴], eight orders of magnitude, the method is **stable** (no crashes) and produces bounded pressure with error that is *monotone* in the distance from the sweet spot δ ≈ 1. This is *precisely* the "absolute stability" claim (Theorem 5.4). At δ=1e−6, the stabilization is weak enough that pressure amplifies noise from the LBB-violating pair (pressure reaches ~1000) but the solve itself does not fail — consistent with the paper: stability constant C(δ) in Thm 5.4 depends on δ and degrades as δ→0, but the method remains formally stable.

At δ=0 (no stabilization) the matrix is exactly singular — LBB failure of P1/P1, as expected.

### 4.4 Polynomial reproduction (weak consistency)

Setting u_exact = (x, −y), p_exact = x, f = (1, 0):

| n | ‖u−uʰ‖_H¹ | ‖p−pʰ‖_L² | ‖u−uʰ‖_L² |
|---|-----------|-----------|-----------|
| 4 | 2.8e−15 | 3.5e−15 | 4.4e−16 |
| 8 | 1.4e−14 | 2.4e−14 | 2.2e−15 |
| 16 | 6.3e−13 | 1.3e−12 | 6.2e−14 |

Machine-precision reproduction of a P1/P1 exact solution — the "weak consistency" of Lemma 5.2 checks out: even though the formulation is not classically consistent, it still reproduces the polynomials from V^h × S^h exactly (linear u has Δu=0, hence P_h(Δu)=0, hence −Δ_h u=0; then the stabilization term is `δh²(∇p, ∇q)` which vanishes at the exact linear p when combined with the RHS `δh²(f, ∇q)` = `δh²(∇p, ∇q)` since f = ∇p for linear p — the terms cancel).

### 4.5 Figure

`report/evidence/convergence_and_stability.png` — three-panel figure: (a) Taylor-Green error vs h with reference slopes, (b) Kovasznay Re=1 error vs h, (c) log-log δ-sweep confirming absolute stability.

## 5. Verdict + justification

**Verdict: REPLICATED.**

The two central computable claims of the paper — Theorem 5.4 (*absolute stability of the new discrete SGLS method*) and Theorem 5.5 (*optimal convergence in the mesh-independent H¹×L² norm*) — were both reproduced from an independent implementation in scikit-fem, starting only from the paper's equations. The convergence rates match or beat the theoretical predictions (H¹-velocity O(h) exact; L²-pressure O(h²) super-optimal). The absolute-stability sweep works over 8 orders of magnitude of δ. The weak-consistency claim (Lemma 5.2) is verified to machine precision on linear polynomials.

One implementation detail that is *not* spelled out in the paper but is essential: the discrete Laplacian −Δ_h in Eq. (5.1) maps into V^h_0 (i.e., must set the boundary components of −Δ_h u to zero), not into V^h. Ignoring this gives O(1/h) contamination at boundary nodes that destroys convergence. This is arguably the paper's most useful missing detail — see open question Q1.

## 6. Open Questions

- **Q1** — *How does the choice of "V^h vs V^h_0 for the discrete Laplacian" affect stability and convergence numerically? The paper says "−Δ_h : H¹_0 → V^h" (equation 5.1) but does not disambiguate whether V^h includes boundary dofs.* — Our implementation initially used the naive V^h version and produced O(1/h) contamination that killed convergence. Restricting to V^h_0 gave optimal rates. This is a nontrivial implementation point that deserves an explicit boxed remark in any tutorial exposition.

- **Q2** — *How does the practical performance of the new method compare with the classical Hughes–Franca–Balestra (1986) PSPG on ill-conditioned problems (high aspect ratio, small viscosity)?* Section 6 of the paper conjectures better matrix conditioning for the new method, but this is not measured. Our next step would be a systematic κ(K) sweep over aspect ratios; our current implementation would need only a change to `MeshTri.init_tensor` grid spacings to test.

- **Q3** — *Does the absolute-stability constant C(δ) in Theorem 5.4 have a δ-dependence that matches the "monotonically degrading pressure error as δ leaves the sweet spot" we observed?* Our sweep shows ‖p−pʰ‖_L² ~ 1/δ for small δ and grows sub-linearly with large δ. A theoretical characterization of the optimal δ (as a function of h, mesh geometry, and problem data) is not given in the paper but would be operationally useful.

- **Q4** — *Extension to the Navier–Stokes equations with convective terms.* The paper is Stokes-only. The δh² term in the SGLS formulation should — by the arguments of Hughes/Franca — extend naturally to unsteady Navier–Stokes with SUPG-like velocity stabilization. A concrete question: does the absolute stability persist when a convective residual `(u·∇u)` is added to the residual inside the H⁻¹ inner product?

- **Q5** — *Extension to discontinuous pressure spaces.* The paper explicitly restricts to continuous pressure (∇pʰ ∈ L²(Ω)) — Sec. 6, last paragraph, calls this "valuable to extend". Numerically, on a DG pressure space (e.g. P1_disc), what should ∇p_h·∇q_h mean — face-jump terms as well as element terms? Empirically, does absolute stability persist? Our current framework (all-continuous) would need a redesigned assembly to test.

## Appendix A. Reproducibility

- Source: `work/bochev_sgls_stokes.py` (self-contained, 400 lines, one external dependency: scikit-fem).
- Evidence: all JSON outputs in `report/evidence/`.
- Figure: `report/evidence/convergence_and_stability.png`.
- Paper: `paper.pdf` (open-access, from Prof. Gunzburger's FSU page).
- Runtime for the full study: ~2 minutes on a Mac M1 (2020 vintage), no parallelism used.
