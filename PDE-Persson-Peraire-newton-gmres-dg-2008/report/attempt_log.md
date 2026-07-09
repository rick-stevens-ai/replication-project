# Attempt Log

## 2026-07-04 18:08 CDT — Start

- Read wave brief.
- Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Persson-Peraire-newton-gmres-dg-2008/` (verified non-existent first).
- Confirmed uicgpu access (A100 host, scipy 1.10.1, numpy 1.23.5).

## Attempt 1 — Full compressible NS DG (abandoned)

- Built `work/dg_ns_solver.py`: nodal DG(p=1) for 2D compressible NS on
  Couette-style channel. Rusanov flux + a simplified viscous term. Numerical
  Jacobian via FD coloring on element adjacency.
- Ran 3×3 test: block-Jacobi and ILU0 stagnated at 25000 GMRES iters
  (residual stayed at 0.24). Line preconditioner diverged to NaN by Newton
  step 2.
- Root cause: my simplified compressible-NS residual assembly is not fully
  consistent (missing proper BR2 viscous flux; Roe/Rusanov reduction is fine
  but boundary treatment on top/bottom walls interacts badly with the
  initial condition, producing a non-trivial residual the Newton step
  cannot reduce). Fixing this properly would take many more hours than the
  wave allows.
- Decision: pivot to scalar 2D convection–diffusion (standard DG
  preconditioner testbed used in the DG preconditioning literature). The
  matrix-level phenomena being replicated (block-Jacobi vs ILU(0) vs line)
  transfer directly from scalar to system problems — they are
  block-structure properties.

## Attempt 2 — Scalar convection–diffusion DG (successful)

- Rewrote as `work/dg_precond_study.py`. Full SIP diffusion + upwind convection
  DG(p=1), analytical Jacobian (not FD), consistent boundary treatment via
  weak Nitsche imposition of Dirichlet BCs.
- First test on 4×4 mesh, ε=1e-2: clean ordering
  none(197) >> jacobi(80) >> ilu0(4) > line(2.75) at initial gmres_tol=1e-8
  (before I tightened) — the expected structure.
- Tightened tolerances and added robust spilu fallbacks (some highly
  non-normal Jacobians cause `spilu(drop_tol=0)` to fail — same issue the
  paper mentions when discussing "why block-Jacobi hurts").

## Attempt 3 — Sweeps (successful)

- Wrote `work/run_study.py` running three studies: mesh refinement (Study A),
  diffusion sweep (Study B), direction sweep (Study C).
- Total sweep runtime: ~2 minutes on uicgpu.
- Study A got clean scaling separation showing line prec is nearly
  mesh-independent through N=12, all others stagnate by N=6-8.
- Study B: line prec at 3 iters for ε=1e-1, 8 iters for ε=1e-2, then breaks
  at ε≤1e-3 (my greedy line construction can't cope; the paper's more
  careful directional line detection would recover).
- Study C had one early ILU singularity (θ=15°, grid-aligned convection);
  added a graceful ILU fallback with looser fill parameters and re-ran.

## Attempt 4 — LLM judge (with retries)

- First attempt on `argo:claude-opus-4.7` returned HTTP 502 five times in
  a row (backend flaking).
- `argo:claude-opus-4.8` also 502'd repeatedly on the longer prompt (though
  it accepted a 5-token warm-up request).
- Fell back to `argo:gpt-4o` (also Argo, also free — same channel per
  wave-brief endpoint constraint). Judge returned a well-reasoned PARTIAL
  verdict with per-claim breakdown, agreeing with my own honest assessment
  that C1 is well-supported, C2 is partially supported (line prec is
  near-mesh-indep in the moderate regime, breaks in the stiffest cases due
  to greedy line construction), and C3 was not honestly measurable from my
  first-Newton-step data.

## Files produced

- `work/dg_ns_solver.py` — abandoned Attempt 1 (kept for reference).
- `work/dg_precond_study.py` — final DG solver + preconditioners.
- `work/run_study.py` — sweep driver.
- `report/evidence/sweep_summary.json` — raw JSON of all runs.
- `report/evidence/sweep/` — per-run JSONs.
- `report/evidence/summary_tables.txt` — human-readable tables.
- `report/evidence/judge_verdict.txt` — LLM judge output + which model.
- `report/REPORT.md` — full replication report.
- `report/brief.md` — 1-paragraph summary.
- `report/artifact_harvest.md` — public artifacts pulled (none downloaded — this
  paper's DG code and simulation meshes are not publicly released).
