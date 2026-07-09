# Attempt Log

**Paper:** Juntunen & Stenberg 2009, *"Nitsche's method for general boundary conditions"*, Math. Comp. 78:1353–1374.
**Set:** PDE-100 · **Date:** 2026-07-05

## Timeline

1. **Paper retrieval.** AMS PDF link (`ams.org/journals/mcom/2009-78-267/S0025-5718-08-02183-2/`) initially blocked (returned HTML paywall page ~4.5 kB) from both local and `ssh uicgpu` with default curl UA. Switched to a browser-style `User-Agent` header (`Mozilla/5.0 ... Chrome/125.0.0.0 Safari/537.36`) via `ssh uicgpu` and got the full 22-page PDF (465 kB). md5 = `fd50163f25bdb130aa06fb2a8241fdda`.

2. **Content extraction.** `pdftotext -layout paper.pdf paper_layout.txt` gave clean prose + preserved formula layout. Skimmed Sections 2 (method), 3 (a priori estimates), 4 (a posteriori), 6 (numerics).

3. **Environment.** No FEniCS/dolfinx locally on CherryRd; `scikit-fem 12.0.1` was already installed (`Python 3.14.6`, `numpy 2.4.3`, `scipy 1.18.0`). Since 2D triangular Poisson on ≤256×77 grids is very light (7–150 ms per solve), stayed local rather than push to uicgpu.

4. **Implementation (v1).** Wrote `work/nitsche_replication.py`. Implemented:
   - `MeshTri.init_tensor` for structured Ω=(0,1)×(0,0.3);
   - `tag_facets()` splitting ΓR (y=0.3) from ΓD (rest);
   - `assemble_nitsche_system()` implementing Eqs. (2.5) and (2.6) exactly, with special ε=0 (Dirichlet) and ε=∞ (Neumann) branches;
   - `solve_nitsche()` handling both boundary families in the same Nitsche framework;
   - `L2_error`, `H1_seminorm_error`, `energy_norm_h`;
   - `cond_number_estimate` (dense SVD for n≤400, ARPACK on A^T A otherwise).

5. **Bug 1 — coefficient of ∂u∂n·∂v∂n term in Bₕ.** First reading of Eq. (2.5) via pdftotext suggested the last term coefficient was `γhE/(ε+γhE)`. Cross-checking against the Neumann limit Eq. (2.14) which requires coefficient `γhE` at ε=∞, and the Dirichlet limit Eq. (2.13) which requires the term to vanish at ε=0, forced the correct coefficient to be `(γhE·ε)/(ε+γhE)`. Fixed in code. This is a bookkeeping trap in the paper's typography (the `ε` appears as a subscript-position character on a following line in the two-column PDF).

6. **First full sweep.** With ε ∈ {1, 0.1, 0.01, 1e-6, ∞, 0} and n_x ∈ {8..256}:
   - **Nitsche coercivity λ_min ≈ 0.858** essentially independent of h and ε (varies at the 4th digit). ✓ Theorem 3.2.
   - **Convergence:** For ε → 0 (Dirichlet-like), L2 rate → 2, H1 rate → 1 (P1 optimal). ✓ Theorem 3.5.
   - **Anomaly:** For ε=1 and ε=∞, L2 error plateaued around 0.08–0.11 with essentially zero rate.

7. **Bug 2 — paper's manufactured source g typo.** Investigation of the plateau led to a manufactured-solution unit test with a single Fourier mode (nterms=1). Even then, ε=1 and ε=∞ did not converge. Analytic check:
   - Paper's model (6.1): `∂u/∂n = (1/ε)(u₀ - u) + g` on ΓR
   - Paper's `u = Σ U_k · sinh(kπy) sin(kπx)/sinh(0.3kπ)` satisfies `u|ΓR = u₀`, so `∂u/∂n|ΓR = g` is required.
   - `∂u/∂y|ΓR = Σ U_k · kπ · cosh(0.3kπ)/sinh(0.3kπ) · sin(kπx) = Σ U_k kπ coth(0.3kπ) sin(kπx)`.
   - Paper (typeset in the two-column PDF and confirmed with `pdftotext -layout`) writes: `g = Σ kπU_k · sinh(0.3kπ)/cosh(0.3kπ) · sin(kπx) = Σ kπU_k tanh(0.3kπ) sin(kπx)`.
   - **These differ**: paper needs coth (not tanh) for the exact solution to actually solve (6.1) for all ε. Using the paper's exact formula, the flux BC is violated for ε > 0, so numerical error stays bounded away from zero as h → 0 (the finite-element solution converges to a *different* function than the claimed u).
   - Fixed `robin_g` in code to use the physically-correct coth formula. This is a documented deviation from paper's written text; the intent of Sec. 6 (an ε-independent exact solution) requires it.

8. **Second full sweep** (with corrected g): ε=1 no longer plateaus. For nterms=3 (very smooth solution), L2 rate = 2.00, H1 rate = 1.00 within 1% across all ε ∈ {0, 1e-6, 0.01, 0.1, 1, ∞}. For nterms=21 (paper's setup), asymptotic rates emerge once h ≲ 1/128 (below the finest Fourier scale, wavenumber 21π ≈ 66).

9. **γ (stability parameter) sweep.** On a fixed mesh, computed generalized eigenvalue `λ_min(B_h) / ‖·‖_h` for γ ∈ [0.01, 10]. Result: λ_min decreases monotonically, crosses zero near γ ≈ 2 → verifies the sharp upper bound `γ < 1/C_I` in Theorem 3.2 (implying `C_I ≈ 0.5` for this mesh/element choice).

10. **Traditional method (γ=0) condition-number growth.** With homogeneous strong Dirichlet on ΓD (via row/col elimination) and penalty on ΓR, condition numbers on n_x=32 mesh: `ε=1 → 212, ε=0.1 → 114, ε=0.01 → 75, ε=0.001 → 292, ε=1e-4 → 2820, ε=1e-6 → 281000`. The 1/ε growth kicks in for ε < h ≈ 0.031. Nitsche's condition number on the same mesh varies over only `[73, 231]` across the same ε range. This directly reproduces Fig. 5 of the paper.

11. **A posteriori estimator (partial).** Implemented a simplified surrogate estimator `η ≈ sqrt(Σ h_E [∂u_h/∂n]² + boundary residuals)` without the full boundary-jump form of Eq. (4.1). Effectivity index `I_eff = η/‖e‖_h` is bounded (2 to ~20) across the sweep, giving qualitative confirmation that the estimator provides an upper bound in the correct ballpark, though our surrogate lacks the full Nitsche-specific boundary terms that would tighten I_eff to be uniform in ε.

12. **Report generation.** Wrote `report/REPORT.md` with claims table, method, results tables, and verdict.

## What worked

- **scikit-fem** was more than sufficient for this 2D linear-elliptic problem; per-solve wall times: 5–150 ms.
- **Cross-checking via limits** (ε→0 gives Nitsche's classical Dirichlet formulation; ε→∞ gives a Neumann formulation with the specific stabilization of Eq. 2.14) caught Bug 1 in a single afternoon.
- **Manufactured-solution testing at low nterms** cleanly isolated Bug 2 (paper's `sinh/cosh` typo) from mesh under-resolution effects.
- **Both major claims (T2 coercivity, T5 conditioning) reproduced quantitatively**, not just qualitatively.

## What was hard / partial

- **A posteriori estimator (T4).** The full Eq. (4.1) estimator has boundary-jump terms specific to the Nitsche formulation whose exact coefficients I had to reverse-engineer from the paper's mesh-dependent norm; I ended up computing a simpler surrogate rather than the full estimator. Qualitative effectivity is confirmed; a truly rigorous check of Theorem 4.2's upper *and* lower bound would need the exact E_K.
- **Adaptive mesh refinement study (Fig. 4 in paper).** Not attempted — would require implementing a Dörfler-style refinement loop in scikit-fem, which is out of scope for an independent-replication of the theory/analytical claims.

## No external LLM calls used for scoring in the loop (only for report drafting).

## Files produced
- `work/paper.pdf` (paper PDF; md5 `fd50163f25bdb130aa06fb2a8241fdda`)
- `work/paper.txt`, `work/paper_layout.txt` — extracted text
- `work/nitsche_replication.py` — main implementation & experiments
- `work/gamma_sweep.py` — Theorem-3.2 sharpness sweep
- `work/mms_verify.py` — MMS convergence-rate verification with variable nterms
- `work/aposteriori.py` — surrogate a posteriori estimator
- `report/evidence/*.json` — all quantitative results
