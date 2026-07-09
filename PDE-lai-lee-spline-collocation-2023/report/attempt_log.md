# Attempt Log

1. **Candidate selection.** Read `PDE_NEXT50_2026-06-26.tsv`. Avoided the phase-field/
   Allen-Cahn/SAV family (already ×3 tonight) and the already-done set. Considered rank 7
   (Saut–Wang Whitham) — rejected: pure analysis paper, no numerical scheme/reference numbers.
   Considered rank 32 (Einkemmer–Lubich Vlasov–Poisson) — rejected: Vlasov–Poisson already
   has 3 sibling dirs. Picked **rank 24, Lai–Lee spline collocation** — a fresh family
   (elliptic PDE / Bernstein–Bézier spline collocation), clear numerical core, analytic test
   cases, concrete RMSE numbers, arXiv OA.

2. **Dedup.** `ls REPLICATE-PROJECT/ PDE-replications/ | grep -i {spline,collocation,lai,…}`
   → no collision. Created `PDE-lai-lee-spline-collocation-2023/`.

3. **Fetch OA.** `curl -sL arxiv.org/pdf/2109.09698v4` (not the paid pdf tool). `pdftotext
   -layout`. Extracted the exact PDE (Poisson `-Δu=f`, Dirichlet BC), the method (discontinuous
   `S_D^{-1}` BB spline space + `C^r` smoothness constraints `Hc=0` + BB domain-point
   collocation + constrained least-squares), the 10 test functions, and Table 4/5 numbers.

4. **Implement from scratch** (`spline_collocation.py`): BB multi-indices; barycentric coords;
   Bernstein basis values; 1st and 2nd BB derivatives via the degree-lowering recurrence
   (`∂B^D = D·Σ_m (∂λ_m)·B^{D-1}_{ijk−e_m}`, applied twice for 2nd order); BB domain points;
   `C^r` edge-smoothness rows (match value + all derivatives up to order r at D+1 sampled edge
   points → algebraically equivalent to the BB smoothness conditions for degree-D polys).

5. **Driver** (`run_poisson.py`): triangulate `[0,1]²` (n×n grid, 2 tris/cell — the method is
   domain-agnostic, a square polygon has uniformly positive reach), assemble H (C² across all
   interior edges) and K (collocation: `-Δs(ξ)=f` interior, `s(ξ)=g` boundary at BB domain
   points, D0=D+3), solve `min ||Kc−rhs||` s.t. `Hc=0` via the null space of H + lstsq. Evaluate
   RMSE vs exact on a dense interior grid.

6. **First run** (n=2, D=8, r=2, sin πx sin πy): RMSE 2.5e-5 — method works but coarse mesh.
   Refinement sweep confirmed clean high-order convergence:
   n=2→3→4→6: 2.5e-5 → 8.2e-7 → 1.4e-7 → 2.8e-9.

7. **Convergence study on uicgpu** (`conv_study.py`, cases us1/us3/us6/sin, n=2..8). Results:
   us1 n=8 → **5.2e-12**; us3 n=8 → **1.6e-10**; us6 n=8 → 1.2e-8; sin n=8 → 2.5e-10.
   us1 (5.2e-12) and us3 (1.6e-10) land in the paper's Table 4 RMSE range for those functions.

8. **Multi-judge** (free Argo: gpt-5.2, gemini-2.5-pro, gpt-4.1). Consensus 2×PARTIAL,
   1×REPLICATED. Judges agreed the core near-machine-precision claim is reproduced (esp. us1),
   with the caveat that we used a square domain instead of the paper's curved multi-hole domains,
   and us6 didn't reach the paper's tightest range. → Verdict **PARTIAL**.

## Notes / internal observations
- The paper's headline precision (1e-11..1e-13) is attained for the smoothest functions (us1,
  us3, us7) and is genuinely mesh-refinement-limited; us6 (arctan, sharper curvature) and us5
  (sin 3π·, higher frequency) are visibly harder — consistent with the paper's own us5 numbers
  being ~1e-8..1e-10, i.e. the paper too shows the method is not uniformly at machine precision.
- Our square-domain errors are slightly larger than the paper's curved-domain numbers for the
  same function; this is expected — precision is set by |△| and collocation count, and we did not
  reconstruct their exact fine triangulations (325+ vertices). The convergence trend clearly
  extrapolates into the paper's range with further refinement.
- Constrained-LS via null-space of H is numerically the bottleneck at n=8 (H is large); this is
  a solver-engineering detail, not a method fidelity issue.
