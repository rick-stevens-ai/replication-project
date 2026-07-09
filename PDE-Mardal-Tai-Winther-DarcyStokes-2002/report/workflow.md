# Workflow: MTW 2002 Darcy-Stokes Replication

## Overview
End-to-end pipeline for independently reproducing Mardal, Tai, Winther
(SIAM J. Numer. Anal. 40(5), 1605-1631, 2002), "A Robust Finite
Element Method for Darcy-Stokes Flow." Sub-agent execution, single
MacBook host (CherryRd), 2026-07-04.

## Stage 0 — Paper acquisition

1. Try SIAM publisher URL for DOI 10.1137/S0036142901383910 → **HTTP 403**.
2. Try OSTI mirror → **timed out**.
3. Query Semantic Scholar Graph API with keychain key
   (`security find-generic-password -a rick-stevens-ai -s semantic-scholar-api-key -w`) →
   points to Green OA copy on `dr.ntu.edu.sg`.
4. Fetch dr.ntu.edu.sg PDF live → **AWS WAF block**.
5. Fall back to Internet Archive Wayback Machine snapshot 2024-05-03 →
   **HTTP 200, 270 KB, PDF v1.4, 28 pages, SHA1 c9eee75…**
6. Save to `work/paper_MTW2002.pdf`; stamp SHA1.

## Stage 1 — Text extraction

- Tool: Poppler `pdftotext -layout work/paper_MTW2002.pdf work/paper.txt`
- Output: 1564 lines.
- Tables and formulas parsed manually (visual inspection of the PDF)
  because `-layout` is not sufficient for the paper's multi-column
  tabular rate reports.

## Stage 2 — Claim registry

Extract the 7 numbered / tabulated claims C1–C7:
- C1 (Lemma 4.1): dim V(T) = 9, DOFs unisolvent
- C2 (Tables 3.1–3.9): P2-P0 / CR / Mini lose ε-uniformity
- C3 (Table 5.1): MTW element ε-uniform rates
- C4 (§4.2): div V_h ⊂ Q_h and weakly-div-free ⇒ strongly-div-free
- C5 (Theorem 5.1): |||u−u_h|||_ε ≤ c(h²+εh)‖u‖₂
- C6 (Example 6.1): boundary-layer O(hε^{-1/2})
- C7 (§7, Tables 7.1–7.4): elliptic-system extension

Prioritize C1, C2, C3, C4 as the central novel-contribution and
motivating claims; C5 by empirical proxy; C6, C7 deferred.

## Stage 3 — Standard-elements sweep (baseline / C2)

**Code:** `work/darcy_stokes_standard.py`
**Library:** scikit-fem 12.0.1 (P2-P0, Mini, CR built-in).

Steps:
1. Symbolic manufactured solution
   `u = curl(sin²(πx₁) sin²(πx₂))`, `p = sin(πx₁)` (SymPy).
2. Compute RHS `f = u − ε² Δu − ∇p` symbolically.
3. For each element pair E ∈ {P2-P0, Mini, CR}:
   a. Build unit-square n×n mesh, split each square by negative-slope
      diagonal (matches paper convention).
   b. Assemble saddle-point block system; impose Dirichlet u=0 on all
      boundary velocity DOFs; pin one pressure DOF.
   c. Solve with scipy sparse LU.
   d. Post-process: subtract weighted pressure mean.
   e. Compute relative errors in L² velocity, L² pressure, energy.
4. Sweep ε ∈ {1, 2⁻², 2⁻⁴, 2⁻⁸, 0} × h ∈ {2⁻², 2⁻³, 2⁻⁴, 2⁻⁵}.
5. Fit rate = least-squares slope of log(err) vs log(h).

Runtime: ~2 min.
Log: `report/evidence/run_standard.log`.
Data: `report/evidence/standard_elements_results.json`.

## Stage 4 — MTW element implementation (C1, C3, C4)

**Code:** `work/mtw_element.py` (local) + `work/mtw_solver.py` (global).

### 4a — Local V(T)

1. Parameterize P₃² by 20 monomial coefficients per triangle:
   `1, x, y, x², xy, y², x³, x²y, xy², y³` × 2 components.
2. Build 11-row constraint matrix C ∈ ℝ^{11×20}:
   - **5 rows** for `div v ∈ P₀`: sample `div v` at 6 P₂-unisolvent
     points on T (3 vertices + 3 edge midpoints); require
     `div v(x_i) = div v(x_0)` for i=1..5.
   - **6 rows** for `(v·n)|_e ∈ P₁` (2 per edge): parameterize edge
     by s ∈ [0,1]; sample `v·n(s)` at 4 s-nodes; apply Vandermonde
     inverse to extract s² and s³ coefficients; force to zero.
3. Verify `rank(C) = 11` and `dim ker C = 9`.
4. Build 9-row DOF matrix M ∈ ℝ^{9×20}, one row per DOF (5-pt
   Gauss–Legendre for edge integrals).
5. Solve `M · Q = I` with Q ∈ ℝ^{20×9} constrained to ker C:
   Q columns are the coefficient vectors of the 9 basis functions.

### 4b — Self-tests (C1)

- DOF-of-basis matrix identity: `‖M @ Q − I‖ = 2.9e-14` ✓
- `div φᵢ` constant per basis function to `< 1e-12` residual ✓

### 4c — Global assembly

- DOF numbering: 3 per edge (mean-n, first-moment-n, mean-t).
- Global edge orientation fixed once: `v_lower → v_higher`,
  `n_global = [t_global[1], −t_global[0]]`.
- Per-triangle per-edge sign transform `R_T[e] ∈ ℝ^{3×3}`:
  - `s_t = +1`: `local = diag(s_n, s_n, 1) · global`.
  - `s_t = −1`: k=1 first moment mixes:
    `local_n1 = 2 s_n global_n0 − s_n global_n1`.
- Per-triangle stiffness / mass via 12-point Dunavant degree-6
  quadrature (exact for P₃·P₃ mass and P₂·P₂ gradient).
- Transform: `A_global_block = R_T^T A_local R_T`.

### 4d — Boundary conditions and solve

- All 3 DOFs = 0 on every boundary edge.
- Pin one pressure DOF; scipy sparse LU.
- Post-process: subtract weighted pressure mean over Ω.

### 4e — Error norms

Re-evaluate `u_h`, `Du_h`, `div u_h` at the 12-point Dunavant rule per
triangle:
- `‖u − u_h‖_0`, `‖p − p_h‖_0`
- broken energy `|||u − u_h|||_ε` (broken H¹ Du term)
- `‖div(u − u_h)‖_0`

Sweep ε ∈ {1, 2⁻², 2⁻⁴, 2⁻⁸, 0} × h ∈ {2⁻², 2⁻³, 2⁻⁴, 2⁻⁵}, fit
rates.

**Cost:** nx=32 (~9200 velocity + 2048 pressure DOFs) solves in ~3 s;
full sweep ~90 s.

Log: `report/evidence/run_mtw.log`.
Data: `report/evidence/mtw_convergence.json`.

## Stage 5 — Verdict adjudication

- Match tolerance: ±0.10 per rate (loose) or ±0.03 mean (tight).
- Observed: 15/15 MTW rates within ±0.07, mean |Δ| = 0.024.
- Divergence-error absolute floor: `max ‖div u_h‖_0 = 6.4e-11` across
  all 20 solves (C4 ✓).
- Standard-elements sweep confirms negative results within noise (C2 ✓).
- Verdict: **REPLICATED**.

## Stage 6 — Report generation

- `report/REPORT.md` (canonical narrative).
- `report/REPORT.tex` (LaTeX version with dedicated critique section).
- `report/evidence/` (logs, JSONs).
- `report/open_questions.json` (5 genuinely-open follow-ups).
- `report/workflow.md` (this file).
- `report/artifacts_summary.md` (index).
- `report/failure_analysis.md` (post-mortem of dead ends).

## Reproduce

```
cd work/
python3 darcy_stokes_standard.py all    # ~2 min
python3 mtw_solver.py                   # ~90 s
```

All input paper (SHA1 stamped), all code, all logs, all evidence JSONs
are under this directory.
