# Chronological attempt log

**Session:** 2026-07-06 subagent replication (single-shot).
**Total wall time:** ~30 minutes end-to-end.

## Timeline

1. **~08:16** — Read WAVE_BRIEF_2026-07-01.md. Confirmed target directory does not exist. Created structure.
2. **~08:17** — Queried Semantic Scholar API with DOI → got open-access PDF URL at Prof. Gunzburger's FSU page. Downloaded paper.pdf (202 KB, 19 pages).
3. **~08:18** — Attempted `pdf` tool for extraction — failed (Anthropic PDF credit exhausted, other backends unavailable). Fell back to `pdftotext -layout` which gave clean 1176-line text output. Used this as both `extraction/marker.md` and `extraction/nougat.mmd` (with a note about the tool substitution).
4. **~08:19–08:22** — Read the full paper. **Key discovery:** the paper is *pure theory* — it defines a new method (Eq. 5.10–5.11), proves absolute stability (Thm 5.4) and optimal convergence (Thm 5.5), but contains **zero numerical experiments**. This meant our replication had to design its own numerical tests to verify the theorems.
5. **~08:23** — Decided approach: implement in scikit-fem (12.0.1, already installed locally). Chose Taylor-Green + Kovasznay + linear-polynomial benchmarks.
6. **~08:25** — Wrote first version of `bochev_sgls_stokes.py`. Debugged one immediate issue: `spsolve` block sizing (fixed by ensuring contiguous arrays).
7. **~08:27** — First convergence run: rates ~0.5 for H¹-velocity and pressure — **sub-optimal**. Suspected sign/formulation bug.
8. **~08:28** — Ran a controlled comparison: implemented the *classical* Hughes-Franca-Balestra PSPG (same code, but drop the −Δ_h term). It gave optimal rates ~1.0. So the B-G-specific term was to blame.
9. **~08:31** — Debug hypothesis 1: sign of the discrete-Laplacian term. Flipped it. Didn't help.
10. **~08:33** — Debug hypothesis 2: pressure zero-mean subtraction. Added it. Didn't help.
11. **~08:35** — Ran polynomial-reproduction test: exact linear u=(x,−y), p=x. Should be reproduced to machine precision by any consistent P1/P1 method. My B-G implementation gave errors ~O(1) at n=8 and *growing* with mesh refinement. This was the smoking gun.
12. **~08:36** — Direct inspection of `−Δ_h u_lin`: it was **~40** at boundary nodes and **~8** at interior nodes — should be exactly 0 for a linear u. **Root cause identified:** I was computing `M⁻¹ A u_c` with the *full* mass matrix M (all dofs). But the paper's definition (Eq. 5.1) uses test functions `vʰ ∈ V^h_0` (interior only, vanishing on ∂Ω). Restricting the test space eliminates the boundary contamination.
13. **~08:38** — Also fixed a subtler bug: the `B*(u,q) = ∫u·∇q` bilinear form is only equivalent to `B(u,q) = -∫q ∇·u` **when u vanishes on ∂Ω**. For inhomogeneous Dirichlet BCs (all our benchmarks), the boundary integral `∫qu·n` differs. Switched to the proper `B` form.
14. **~08:40** — Re-ran. Linear polynomial reproduced to 1e−14 ✓. Taylor-Green H¹-velocity rate = **1.00** exactly ✓. L²-pressure rate = **2.04** (super-optimal, expected for smooth solutions on interior-restricted stabilization) ✓.
15. **~08:42** — Ran absolute-stability sweep: δ ∈ {10⁻⁶, 10⁻⁴, 10⁻², 1, 10, 100, 10³, 10⁴}. All solves succeed. ‖pʰ‖_∞ stays bounded from 1.14 (δ=1) up to 1.70 (δ=10⁴) — 4 orders of magnitude of δ with only 1.5× degradation in pressure. Confirms Thm 5.4.
16. **~08:43** — Ran control experiment at δ=0 (standard Galerkin equal-order): matrix exactly singular (LBB failure). Confirms P1/P1 needs stabilization.
17. **~08:44** — Fixed JSON serialization of numpy ints/floats. Regenerated outputs.
18. **~08:45** — Generated 3-panel matplotlib figure (Taylor-Green convergence, Kovasznay convergence, δ-sweep).
19. **~08:46–08:52** — Wrote REPORT.md, REPORT.tex, brief.md, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md.

## What worked

- scikit-fem's `Basis`, `BilinearForm`, `Functional` abstractions made assembly clean.
- Precomputing `M⁻¹A` via block-column `splu.solve` (nu / 128 blocks) was fast enough — dominant cost at n=64 (~90 s), acceptable.
- Building `MinvA` as `P @ Zi` with a sparse extension matrix `P` (interior→full-dof permutation) — 100× faster than `lil_matrix` row assignment for large nu.
- Taylor-Green as the primary benchmark: smooth, analytical, in a unit square that gives clean h = √2 / n for the diagonal triangulation.
- Testing polynomial reproduction to catch formulation bugs — the earlier debug attempts (sign flipping, mean subtraction) were red herrings; the polynomial test immediately localized the problem.

## What didn't work

- Kovasznay at Re=40 on our meshes (n≤64): the boundary-layer at x=-0.5 needs h << 1/λ ~ 0.15 to resolve, so all our meshes are pre-asymptotic. We report it (stable, no crash, ‖p‖ bounded) but it doesn't show convergence rates. Re=1 is the right regime for a smoothness demo.
- The `pdf` tool for automated LLM-judge extraction — API credit issue. Worked around with `pdftotext` (which is actually *cleaner* than most LLM extractions for equation-heavy math papers).
- Initial mass-matrix inversion strategy (LIL matrix row-assignment for MinvA extension): O(nu²) memory + time; became the bottleneck at n=64. Switched to sparse extension-matrix multiplication.

## What was hard

- The paper is very abstract: 20 pages of theorems, no examples, no pictures, no code. The subtlety about V^h vs V^h_0 for −Δ_h is *implicit* in the abstract functional-analysis framework and only surfaces when you sit down to code it. This is exactly the kind of "obvious to a numerical analyst" detail that trips up implementers.
- Choice of benchmark: with no numerical experiments in the paper, we had to design our own — a Taylor-Green + Kovasznay pair covers standard Stokes benchmarking but the reader has to trust our judgment on what constitutes a fair test. The absolute-stability sweep (δ ∈ [10⁻⁶, 10⁴]) is the crispest test of the paper's main claim; the polynomial-reproduction test is the crispest test of weak consistency (Lemma 5.2).
