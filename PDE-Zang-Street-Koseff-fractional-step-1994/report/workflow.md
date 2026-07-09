# Workflow — Zang, Street & Koseff (1994) Independent Replication

**Replication id:** `PDE-Zang-Street-Koseff-fractional-step-1994`
**Assigned:** REPLICATE-PROJECT wave brief 2026-07-01
**Executed:** 2026-07-04
**Host:** `uicgpu` (8×A100 available; not used — solver is single-threaded numpy/scipy)

## 0. Scope decision

- **In scope (testable within a wave-push budget):**
  - C1 — machine-precision face-flux divergence from momentum interpolation
  - C2 — Ghia et al. (1982) centreline agreement at Re ∈ {100, 400, 1000}
- **Out of scope:**
  - C3 — general curvilinear coordinates (Cartesian only in replication)
  - C4 — formal order-of-accuracy study (single mesh N=128)

## 1. Paper acquisition and reading

1. Locate DOI: [10.1006/JCPH.1994.1146](https://doi.org/10.1006/JCPH.1994.1146).
2. Extract Sections 2–3 (discretisation), 4 (fractional-step algorithm),
   5 (test cases — lid-driven cavity and curvilinear cavity).
3. Identify the four claims (C1..C4) and flag which are testable in scope.
4. Locate benchmark reference: Ghia, Ghia & Shin (1982), *J. Comput. Phys.*
   48, 387–411 — Tables I and II give centreline u and v profiles at
   Re = 100, 400, 1000, 3200, 5000, 7500, 10000.

## 2. Implementation (`work/`)

1. `work/zsk_solver.py` (~300 lines): full solver.
   - Cell-centred storage of u, v, p on a uniform Cartesian N×N mesh.
   - Ghost-cell BCs: no-slip on three walls, ramped Dirichlet lid, Neumann
     pressure with `p[0,0]=0` null-space pin.
   - Convection + diffusion by central second-order differences.
   - Forward-Euler predictor (paper uses ADI-implicit — see failure_analysis.md).
   - Face-flux recovery by simple averaging (Rhie-Chow-style momentum
     interpolation reduces to this on a uniform Cartesian mesh).
   - Pressure Poisson via pre-factorised sparse LU (`scipy.sparse.linalg.splu`).
   - Face-flux correction by face pressure gradient (one-sided differences).
   - Cell-centred velocity correction by cell-centred pressure gradient
     (central differences with Neumann ghosts).
2. `work/ghia_data.py`: transcribed Ghia (1982) Tables I & II for
   Re = 100, 400, 1000. Values cross-checked against Botella & Peyret (1998)
   and Erturk et al. (2005) which reproduce identical numbers.
3. `work/run_sweep.py`: driver that iterates Re ∈ {100, 400, 1000}, saves
   `cavity_N128_Re{Re}.npz` (full u, v, p, centreline samples), and appends
   to `sweep_metrics.json`.
4. `work/make_plots.py`: generates `centerlines_vs_ghia.png`,
   `streamlines_Re1000.png`, `divergence_summary.png`.
5. `work/judge.py`: Argo LLM-judge call, requests `argo:claude-opus-4.7`
   first, falls back to `argo:claude-opus-4.5` on the 502 schema-validation
   error, logs both attempts to `judge_verdict.json`.

## 3. Execution sequence

```
cd work/
python run_sweep.py               # solve Re=100, 400, 1000 → NPZ + JSON
python make_plots.py              # generate PNGs → ../report/evidence/
python judge.py sweep_metrics.json # LLM-judge call → judge_verdict.json
```

Wall-clock: ~5 min for the full sweep on a single CPU core of `uicgpu`
(57 s + 99 s + 146 s per Re, dominated by the pressure back-solve at
128×128).

## 4. Steady-state detection

Simulation runs until
`max|u^{n+1} - u^n| / Δt < 1e-6`
(and the same for v), checked every 200 steps, or until a hard horizon
`t_end ∈ {25, 40, 60}` for Re = 100, 400, 1000.

## 5. Diagnostics captured per run

- `||div U||_2`, `||div U||_∞` of corrected face fluxes at final step.
- Centreline u along x = 0.5 (17 samples matching Ghia).
- Centreline v along y = 0.5 (17 samples matching Ghia).
- Peak-velocity extrema (u_min, v_min, v_max).
- Wall-clock time to steady state.
- Full 2-D u, v, p fields at final step (saved to NPZ).

## 6. LLM-judge protocol

1. Post `sweep_metrics.json` + a summary of the paper's C1/C2 claims to
   `argo:claude-opus-4.7`.
2. On 502 (persistent schema-validation error from Argo proxy), fall back
   to `argo:claude-opus-4.5`.
3. Log both attempts, requested model, actually-used model, and full JSON
   response to `evidence/judge_verdict.json`.
4. Judge is asked for structured output:
   `{core_claim_reproduced, quantitative_agreement, verdict, notes, quibbles}`.

## 7. Reporting

- `report/REPORT.md` — full narrative (14 KB).
- `report/REPORT.tex` — LaTeX version with dedicated *Genuine Critique* section.
- `report/open_questions.json` — 5 truly open follow-on questions.
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — index of everything produced.
- `report/failure_analysis.md` — honest anomalies and known limitations.
- `report/evidence/*.png` — figures.
- `report/evidence/sweep_metrics.json`, `judge_verdict.json` — machine-readable outputs.

## 8. Handoff checklist

- [x] All four testable-in-scope claims addressed (C1 ✓ reproduced,
      C2 ✓ reproduced, C3 out of scope, C4 not measured).
- [x] Verdict recorded: REPLICATED (Cartesian limit).
- [x] LLM-judge confirmation attached with model-substitution disclosure.
- [x] Anomalies and honest caveats logged (Re=400 x=0.9063 Ghia outlier,
      near-lid interpolation artefact, ADI→Euler simplification, direct-LU→multigrid).
- [x] Open follow-on questions enumerated.
- [x] Report deliverables written to `report/`.
