# attempt_log.md

Chronological log of the ZSK-1994 replication run on 2026-07-04 (CDT).

## 18:08 — brief read, plan
- Read wave brief, verified target dir does not exist. Created it.
- Plan: pure-numpy collocated fractional-step; run lid cavity at Re=100/400/1000 on N=128; compare centerlines to Ghia 1982.

## 18:10 — solver v1 (`zsk_solver.py`)
- Cell-centered u,v,p on [0,1]^2 uniform grid.
- Ghost-cell BCs (Dirichlet walls, moving lid).
- Central-difference convection + diffusion. Forward Euler predictor.
- Face-flux linear interpolation for Rhie-Chow-style coupling; direct sparse-LU Laplacian for pressure with a pinned cell (p[0,0]=0).
- Local smoke test N=32 Re=100 converged to steady state, u_min=-0.206 vs Ghia -0.211 → looked right.

## 18:15 — first N=128 sweep on uicgpu (BLOWUP)
- Ran on uicgpu (Python 3, numpy+scipy). N=128, Re=100/400/1000.
- Re=100 diverged: NaN by step 2000. CFL 0.3 too aggressive for central-diff convection with the impulsive-start lid (u/dt blowing up early: du/dt ~5e3 at step 1500).

## 18:16 — mitigation attempt 1 (AB2 + cosine ramp)
- Added Adams-Bashforth-2 predictor.
- Added cosine ramp on lid velocity (`ramp_time=1.0`).
- Reduced CFL to 0.15 with a 0.9 safety, cap on both convective and viscous dt.
- On uicgpu still blew up at N=128 Re=100 (NaN after step 500).
- Ran locally at N=128 with CFL=0.05: stable and finished the initial transient.

## 18:20 — mitigation attempt 2 (forward Euler + longer ramp)
- Reverted predictor to plain forward Euler (AB2 was actually worse for
  central-diff convection on this grid; its stability locus is worse in
  a certain direction).
- Kept the 0.9 safety factor on dt.
- Extended `ramp_time` to 2.0 seconds.
- Local N=128 Re=100 test converged in ~72 s wall, u_min=-0.214 (Ghia -0.211),
  v_min=-0.253 (Ghia -0.245), v_max=0.179 (Ghia 0.175).
- Pushed updated solver + sweep to uicgpu.

## 18:22 — production sweep on uicgpu (SUCCESS)
- N=128, Re=100 done in 57 s wall (22000 steps, div_l2=2.2e-15).
- N=128, Re=400 done in 99 s wall (37926 steps, div_l2=2.5e-15).
- N=128, Re=1000 done in 146 s wall (56889 steps, div_l2=2.6e-15).
- Total wall ~5 min. Metrics dumped to `sweep_metrics.json`.
- Peak-velocity magnitudes match Ghia 1982 within 1-3 % at every Re.

## 18:25 — plots
- Generated centerline overlays (`centerlines_vs_ghia.png`), Re=1000
  streamlines (`streamlines_Re1000.png`), and divergence summary
  (`divergence_summary.png`).
- Visual match at all three Re looks essentially on top of the Ghia points
  except for the known Re=400 x=0.9063 outlier.

## 18:26 — LLM judge (Argo)
- Requested judge model: `argo:claude-opus-4.7`.
- Every non-trivial POST to `argo:claude-opus-4.7` returns
  `502 Failed to parse upstream response: 1 validation error(s): Value at
  'choices[0].message' does not match any variant of SystemMessage |
  UserMessage | AssistantMessage | ToolMessage`.
- Confirmed the trivial `say hello` request to 4.7-opus DOES work, so the
  model is present in the proxy and it's the response-side schema validator
  that rejects a nontrivial reply. Filed as an Argo-proxy bug (out of
  scope of this replication).
- Fell back to `argo:claude-opus-4.5` (also a free Argo endpoint) — accepted
  the same prompt cleanly and returned:
    verdict = REPLICATED, core_claim_reproduced = true,
    quantitative_agreement = high, quibbles = 4 (top-wall interpolation,
    single-point Re=400 outlier, side-wall v slight, Cartesian scope).
- Full response saved to `evidence/judge_verdict.json`, including the 4.7
  fallback log.

## 18:30 — report
- Wrote REPORT.md, brief.md, artifact_harvest.md, this log.
- Verdict: **REPLICATED** (Cartesian limit; curvilinear scope note in §5.3).
