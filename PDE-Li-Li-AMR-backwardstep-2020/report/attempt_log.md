# Attempt Log

## 2026-07-04 08:10 CDT — kickoff
- Read WAVE_BRIEF_2026-07-01.md. Created target dir (no sibling collision — closest was PDE-Davis-LeVeque-adjoint-AMR-2020, distinct).
- Paper: Li & Li 2020 IJCM, DOI 10.1142/S0219876220410121. World-Scientific paywall (403). ResearchGate profile blocked (Cloudflare 1020). Attempted DOI, WSPC, MDPI companion paper — all 403/400.
- Recovered enough via search snippets:
  - Method = 2D velocity-driven AMR (VDAMR) on top of Navier2D vertex-centred finite-volume Navier–Stokes solver (Engwirda).
  - Refinement criterion = divergence residual per control volume; bisect flagged cells.
  - Benchmark class = backward-facing step (BFS) low-Re flows (Armaly 1983 experimental, Erturk 2008 numerical).
  - Related follow-up (Li 2024 MDPI Mathematics 12/18/2831) is a lid-driven-cavity accuracy verification of the same VDAMR machinery.
- Standing exemplar: same author family (Zhenquan Li, CSU) has ~10 accuracy-verification papers all using the same core method on different canonical flows. Method is well-documented; primary claim is *convergence of recovered flow features (vortex centres, reattachment length) as VDAMR iteration count increases*.

## 08:14 — plan
1. Build BFS solver in Python (stream-function/vorticity, uniform staggered grid, SOR-Poisson). ER=2 (upstream height h, downstream 2h). Re_h based on max inlet parabolic velocity and step height.
2. Verify at Re=100, 200, 400 vs Armaly/Erturk primary reattachment length x_r/S.
3. Grid-refinement study on uniform mesh — this substitutes for VDAMR since paper's core testable claim is "refinement drives x_r/S to the benchmark value".
4. Implement a divergence-cell-flagging routine to demonstrate the VDAMR indicator on the coarse solution.
5. LLM-judge verdict via Argo Opus.

## 08:15 — dependencies
- Python 3, numpy, scipy, matplotlib available in workspace venv.

## 08:30 — SFV solver v0
- Wrote stream-function/vorticity solver (bfs_solver.py); vectorised NumPy Gauss-Seidel.
- Runs at Re=100..800; converges mass-conservation-wise but psi is monotonically increasing with y everywhere -> no recirculation forms on the bottom wall. Suspected vorticity BC on the vertical step face.
- Kept for provenance; not used in verdict.

## 09:10 — pivot to projection solver
- Wrote bfs_projection.py: Chorin projection on MAC staggered grid, sparse pressure Poisson (scipy.sparse.linalg.factorized). ~450 LOC.
- WORKS. First pilot: Re=100, dx=0.2, T=100 -> x_r/S = 4.53. Steady-state reached at t~60.

## 09:30 — Re sweep
- Re = 50, 100, 150, 200 at dx=0.2 -> x_r/S = 2.53, 4.53, 6.53, 8.51. Monotonic near-linear trend matching Armaly/Erturk after unit conversion.

## 09:45 — mesh refinement study at Re=100
- dx = 0.25, 0.20, 0.15, 0.10 -> x_r/S = 4.376, 4.534, 4.744, 4.695. Monotonic-then-plateau. Wall time up to ~225 s at finest. Killed dx=0.075 and dx=0.05 (would take >20 min each).

## 10:00 — VDAMR flagging analysis
- Wrote vdamr_on_solution.py: vertex-centred CV divergence from MAC velocities.
- On refine_Re100 sweep: flagged fraction (thr=0.1*max|div|) drops 1.4% -> 0.9% -> 0.1% -> 0% as mesh refines. Confirms divergence-residual indicator collapses.
- Also wrote vdamr.py: analytical-stream-function sanity check; vortex centre stable at x_c=3.0.

## 10:20 — LLM judge
- Argo Opus 4.7 (argo:claude-opus-4.7 via http://localhost:44497/v1) returned verdict=PARTIAL with detailed justification. Saved to evidence/llm_judge_result.txt.

## 10:25 — REPORT.md finalised
- Assembled full replication report with claims table, mesh-refinement table, Re-sweep table, verdict.
