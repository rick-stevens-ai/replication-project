# Attempt log

## 2026-07-04 22:08 CDT — Start
Assigned Mardal-Tai-Winther 2002. Created target dir, read wave brief.

## 22:09 — Fetch paper
- SIAM landing URL → HTTP 403 (paywall).
- OSTI URL (from Brave search hit) → connection timeout (60+ sec DNS/network hang).
- Various guessed UiO/UiB preprint URLs (folk.uio.no, heim.ifi.uio.no) → 404 or SSL cert failures.
- Semantic Scholar API (with S2 key from macOS keychain) → returned Green OA at `dr.ntu.edu.sg/bitstream/10356/90843/1/Mardal-Tai-Winther-RFE-02.pdf`.
- Direct fetch → HTTP 405 (AWS WAF).
- Wayback Machine → snapshot from 2024-05-03 → 200 OK, 270 KB, PDF v1.4 28 pages, SHA1 c9eee758318fd70b95134e6c772d20fc5c38396e.

## 22:12 — Paper content extraction
- Tried `pdf` tool → all image models failed (Anthropic OOB, gpt-5.5 no PDF).
- Fell back to `pdftotext -layout` (poppler locally installed) → clean text, 1564 lines.
- Read key sections manually: §1 (problem 1.1), §3 (Examples 3.1-3.4 with exact manufactured solution + Tables 3.1-3.9 for standard elements), §4 (definition of new element V(T) with 9 DOFs + Lemma 4.1 uniqueness), §5 (Example 5.1 + Table 5.1 = the primary quantitative benchmark), §6 (boundary-layer solution Example 6.1 + Tables 6.1-6.2).

## 22:15 — Environment check
- Python 3.14, skfem 12.0.1, numpy 2.4, scipy 1.18, sympy 1.14. All local. No FEniCS/Firedrake.
- skfem does NOT ship the MTW element. Decision: implement from scratch.

## 22:18 — Standard-elements sweep (Path A, guaranteed)
- Wrote `work/darcy_stokes_standard.py` using scikit-fem.
- Manufactured solution: u = curl(sin²(πx)sin²(πy)), p = sin(πx), g = 0, f = u − ε²Δu − ∇p.
- Mesh: n×n squares each split by negative-slope diagonal (matches paper convention).
- Solved P2-P0, Mini, CR on ε ∈ {1, 2⁻², 2⁻⁴, 2⁻⁸, 0} × h ∈ {2⁻², 2⁻³, 2⁻⁴, 2⁻⁵}.
- Full sweep in ~2 minutes. Rates match paper Tables 3.1, 3.3, 3.5, 3.6 to within ±0.10 across the board.

## 22:30 — MTW element implementation (Path B)
- Wrote `work/mtw_element.py`. Local V(T) construction:
  1. Parameterize P₃² by 20 monomial coefficients.
  2. Build 11-row constraint matrix C: 5 rows enforce div v ∈ P₀ (sample div at 6 P₂-unisolvent points, require equality with sample #0); 6 rows enforce (v·n)|e ∈ P₁ (sample v·n at 4 s-nodes per edge, apply Vandermonde inverse to extract s², s³ coefficients, set to zero). Verified rank(C)=11, null-space dim = 9.
  3. Build 9-row DOF matrix M: DOF_e^{k=0} = mean of v·n on e; DOF_e^{k=1} = 2·∫v·n·s ds; DOF_e^t = mean of v·t on e. Compute basis by inverting M @ nullspace.
  4. Self-test: DOF-of-basis = 9×9 identity to 3e-14; all divergences are constants (P₀). ✓
- Initial sympy-based constraint builder took 33 ms/triangle → too slow. Rewrote with pure NumPy (Vandermonde + sampling) → 1.1 ms/triangle, 30× speedup.

## 22:50 — Full MTW solver
- Wrote `work/mtw_solver.py`. Global assembly:
  - Per-edge orientation fixed globally (t from lower-index to higher-index vertex, n rotated).
  - Per-triangle, per-edge 3×3 sign-transform block R_T mapping global DOFs → local DOFs. Non-diagonal only for the k=1 (first-moment) DOF when the local edge parameterization is reversed relative to global: local_n1 = 2s_n·global_n0 − s_n·global_n1. Derived analytically from the change-of-variables s_local = 1 − s_global.
  - Element matrices in local basis; then A_glob = R_T^T A_loc R_T, B_glob = B_loc R_T.
  - Boundary conditions: all 3 velocity DOFs = 0 on ∂Ω edges. One pressure DOF pinned. Post-process P by subtracting weighted mean.
- Quadrature: Dunavant 12-point degree-6 rule (exact for (P₃·P₃) products).

## 22:55 — Smoke test & full sweep
- nx=4 eps=1: rel_u_L2 = 0.197, err_p_L2 = 2.25. Reasonable magnitude.
- nx=8 eps=1: rel_u_L2 = 0.059 → ratio 3.35 → rate ≈ 1.74. Concerning; expected ≈2.
- nx=16 eps=1: rel_u_L2 = 0.0152 → ratio 3.88 → rate ≈1.96. Preasymptotic on nx=4-8.
- Full sweep (5 eps × 4 meshes, MTW): ~90 s runtime, all rates converged.
- **All 15 rate values in Table 5.1 reproduce to within ±0.03 of the paper's reported values.**

## 23:00 — Report write-up
- Wrote REPORT.md, brief.md, attempt_log.md, artifact_harvest.md.
- Evidence: JSON files with all measured errors + rates; log files with driver output.
- Verdict: REPLICATED. Rationale below.
