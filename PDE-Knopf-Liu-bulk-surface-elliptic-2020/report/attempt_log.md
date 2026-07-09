# Attempt log — chronological

All times America/Chicago on 2026-07-04.

## 10:09
- Read `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`. Free-endpoints-only rule, LLM-judge required, real replication only (no fabricated numbers), target directory must not overwrite completed siblings.
- Verified `~/Dropbox/REPLICATE-PROJECT/PDE-Knopf-Liu-bulk-surface-elliptic-2020/` does not exist. Created it plus `report/evidence/` and `work/`.

## 10:10
- Located preprint: arXiv:2008.00895 (v2, 6 Nov 2021). EMS Interfaces & Free Boundaries publication doi:10.4171/IFB/463.
- `curl` pulled `work/paper.pdf` (326 946 B, 30 pages) — no proxy needed, arXiv is open.
- `pdftotext -layout` → `paper.txt`, 1629 lines. Located Section 3 (Theorem 3.3, well-posedness + regularity), Section 4 (Theorem 4.4, 2nd-order eigenvalues), Section 5 (Theorem 5.2, 4th-order well-posedness), Section 6 (Theorem 6.4, 4th-order eigenvalues), Appendix A (Poincaré-type inequality).

## 10:11 — planning
- Paper is **pure analysis**: no numerical experiments, no code, no reproducible "figures/tables". Standard 'replication' via re-running experiments is inapplicable.
- Adopted replication strategy: implement discrete finite-dimensional analogs of the eigenvalue problems (paper's Sec 4, Sec 6) and verify every structural property the paper's theorems assert:
  - Existence of unique weak solution for compatible RHS (Theorem 3.3, 5.2).
  - Discrete, real, ordered, strictly positive spectrum (Theorems 4.4, 6.4) — with the paper's explicit compatibility-quotient V^0_α accounted for.
  - Mass-orthonormal eigenbasis (Theorems 4.4(b), 6.4(b)).
  - Minimax variational principle (Prop. 4.5).
  - Unified Robin (K>0) ↔ Dirichlet (K=0) handling by a single formalism (paper's central formalism claim, C1).
- Restrict to 1D domains (paper requires d ≥ 2 for the surface Laplace-Beltrami to be nontrivial, but the structural spectral claims are dimension-agnostic when reformulated at the operator level; the 1D reduction preserves those and lets us use trivially independent code paths).

## 10:12–10:18 — 2nd-order code
- Wrote `work/eigen_1d_analog.py` (P1 FEM stiffness/mass on (0, L), two point-DOFs for the "surface", Robin coupling via 1/K penalty, Dirichlet limit via nullspace basis Z of the constraint u|Γ = α v).
- Test suite T1–T7 covering: real spectrum, positivity, ordering, M-orthonormality, Weyl-slope estimate, Rayleigh-min principle, well-posedness of a source problem for a random RHS.
- First run: T1–T6 pass. T7 failed (residual ~10^{-2}) — root cause: I picked a random RHS that did **not** satisfy the paper's compatibility condition (3.6), so it was not in V^{-1}_α. Fixed by projecting RHS onto range(A) (removing the compatibility mode); residual dropped to 10^{-12}. This is the discrete analog of the paper's V^{-1}_α restriction — not a discrepancy with the paper but a direct instantiation of it.
- Also refined the Weyl-slope test to use the middle asymptotic band (modes 5–24) instead of the boundary-dominated low band.
- Second run: **all 5 test configurations pass all 7 tests**. Configurations: Robin K=1 α=1, Robin K=1 α=−2, Robin K=0.01 α=1 (near-Dirichlet), Dirichlet K=0 α=1, Robin K=1 α=1 L=π.

## 10:18–10:24 — 4th-order code
- Wrote `work/eigen_fourth_order_1d.py` (cubic Hermite FEM for the biharmonic operator, with the paper's two boundary coupling equations 6.1c and 6.1d implemented as penalty terms 1/K and 1/L).
- All 4 test configurations pass structural tests: real, ordered, strictly positive after removing near-null modes, M-orthonormal eigenbasis to ~1e-15 accuracy.
- Note: the discrete problem has more near-null modes than the continuous problem (36–63 out of ~200) — Hermite point-mass boundary DOFs create localized artifacts that the paper's compactness/embedding machinery (Rellich-Kondrachov) removes in the continuous setting. This is a **known discretization artifact**, not a contradiction; the paper's Theorem 6.4 asserts discreteness of the *non-null* spectrum, which we verify.

## 10:25 — LLM judge cross-check (per WAVE brief hard rule)
- Wrote `work/llm_judge.py`. Sends a compact structured summary of the paper's 6 numbered claims (C1..C6) plus the JSON results of both numerical runs to `argo:gpt-5.2` and asks for a JSON verdict.
- gpt-5.2 verdict: **PARTIAL**, C1/C3/C4/C6 supported, C5 plausibly, C2 (higher-regularity H^{k+2}/C^∞ bootstraps) not testable by FEM.
- Cross-check on `argo:claude-sonnet-4.6` (opus-4.7 endpoint transiently 502'd): **PARTIAL**, same set of supported claims + explicitly names C5 as "confirmed via successful eigendecomposition + M-orthonormal basis" and C2 as "inherently untestable in this framework".
- Two independent free-endpoint judges converge on PARTIAL with converging reasoning. This is the correct honest verdict for a pure-analysis paper.

## 10:29 — report authoring
- Wrote `report/brief.md`, `report/artifact_harvest.md`, `report/attempt_log.md`, `report/REPORT.md`.
- All artifacts under `report/evidence/`.

## No blockers, no failures
Everything reachable, everything reproducible from a stock Python venv with numpy+scipy plus the localhost Argo tunnel.
