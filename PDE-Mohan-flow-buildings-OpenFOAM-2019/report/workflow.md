# Workflow — PDE-Mohan-flow-buildings-OpenFOAM-2019

**Set:** PDE
**Paper:** Mohan, Sundararaj, Thiagarajan (2019), AIP Conf. Proc. 2112, 020149.
**Replicator:** OpenClaw subagent (Argo Opus 4.7)
**Date:** 2026-07-04 (CDT)
**Host:** uicgpu.uic.edu (Ubuntu 22.04, 255-core AMD, 2 TB RAM)
**Verdict:** REPLICATED

---

## Phase-by-phase workflow

### Phase 0 — Paper acquisition

- **Attempt 1 (blocked):** Direct AIP scitation PDF endpoint returned HTTP 403 with JS anti-bot challenge.
- **Attempt 2 (success):** Web Archive capture 2022-12-24 of the same URL. Retrieved 1,835,796 bytes.
  - URL: `https://web.archive.org/web/20221224023802if_/https://aip.scitation.org/doi/pdf/10.1063/1.5112334`
  - sha256: `7c3b2878ab5245ce82fb9bccdcaeda9648146a5589b8f0017093feaee1b68a2f`
- **Lesson:** For publisher-blocked PDFs, wayback snapshot of the same endpoint is often available and byte-identical.

### Phase 1 — Case identification

The paper does not name the OpenFOAM tutorial. Identification was inferential
but tight:

1. Extracted every explicit parameter from the paper's text:
   - Solver: `simpleFoam` (steady incompressible SIMPLE)
   - Turbulence: standard k-epsilon
   - `nu = 1.5e-5 m^2/s`
   - `U_inlet = 10 m/s`
   - Turbulence intensity `I = 0.1`
   - "quad-type mesh, coarser away from buildings"
   - "example case available in OpenFOAM"
2. Searched all `simpleFoam` tutorials in OpenFOAM v1906:
   - `/usr/share/doc/openfoam-examples/examples/incompressible/simpleFoam/*`
3. Grep'd for the parameter fingerprint:
   - Only `windAroundBuildings` has `nu 1.5e-05` + `Uinlet (10 0 0)` +
     `kInlet 1.5   // approx k = 1.5*(I*U)^2 ; I = 0.1` +
     `simulationType RAS; RASModel kEpsilon`.
   - Unique match → identification made.

### Phase 2 — Case setup

```bash
cp -r /usr/share/doc/openfoam-examples/examples/incompressible/simpleFoam/windAroundBuildings \
      /data/stevens/replicate-mohan-2019-buildings/case
cd /data/stevens/replicate-mohan-2019-buildings/case
source /usr/share/openfoam/etc/bashrc
gunzip -k constant/triSurface/buildings.obj.gz   # 600,096 lines
```

### Phase 3 — Meshing

```bash
surfaceFeatureExtract     # 16,107 feature edges → buildings.eMesh
blockMesh                 # 5,000 background hex cells
                          # domain (-20,330) × (-50,230) × (0,140) m
snappyHexMesh -overwrite  # 185,237 cells, 34.34 s wall
checkMesh                 # all mesh-quality checks pass
```

### Phase 4 — Parallel decomposition (one adaptation required)

**Problem:** Debian's `openfoam` package ships only `dummyScotchDecomp`
(no libscotch bindings); tutorial's default `scotch` method fails.

**Fix:** Replace `system/decomposeParDict` with `simple` method:

```
numberOfSubdomains 6;
method             simple;
simpleCoeffs { n (3 2 1); delta 0.001; }
```

Then:

```bash
cp -r 0.orig 0
decomposePar -force
```

### Phase 5 — Solve

```bash
mpirun -n 6 simpleFoam -parallel > log.simpleFoam 2>&1
```

- 400 SIMPLE iterations
- ~120 s wall
- Per-iteration ExecutionTime stable at ~0.08 s
- Final residuals: U_x 2.39e-5, p 4.30e-4, k 7.75e-5, ε 2.69e-4
- All residuals monotonically decreasing

### Phase 6 — Post-processing

```bash
reconstructPar -latestTime
postProcess -func fieldMinMax -latestTime -fields '(U p k epsilon)'
postProcess -func sampleDict -latestTime
```

Custom `system/sampleDict` written to extract quantitative diagnostics (the
paper reports only qualitative visualizations):

- 4 vertical lines at `(x = 0, 100, 200, 300; y = 100)`, `z ∈ [0, 140]`
- 2 horizontal lines at `(z = 20, 60; y = 100)`, `x ∈ [-15, 325]`
- Fields sampled: `U p k epsilon`, `cellPoint` interpolation, raw `.xy` output

### Phase 7 — Independent verification

- Built claims table (5 claims: C1 convergence, C2 roof acceleration,
  C3 wake recirculation, C4 3D flow, C5 upstream undisturbed).
- Cross-referenced each claim against measured field extrema and line
  profiles.
- Wrote LLM-judge prompt (`report/evidence/judge_prompt.md`) summarizing
  paper claims + our measured evidence.
- Called Argo GPT-5.2 via `localhost:44497` proxy (free tier).
- Judge returned: 4/5 fully reproduced, 1/5 partial (C5, near-ground BL is
  real physics unmentioned by paper), OVERALL = REPLICATED.
- Stored judge response at `report/evidence/judge_verdict.txt`.

### Phase 8 — Report generation

- Wrote `REPORT.md` (15 KB) documenting: paper summary, claims table,
  method, results-vs-paper, verdict, caveats.
- Wrote this `workflow.md`.
- Wrote `artifacts_summary.md` (inventory of produced artifacts).
- Wrote `failure_analysis.md` (root-cause list of every non-trivial issue
  encountered).
- Wrote `open_questions.json` (5 genuinely open questions targeting the
  paper's scientific gaps: LES vs RANS, mesh sensitivity, wind-tunnel
  validation, pollutant dispersion extension, ABL inlet).
- Wrote `REPORT.tex` with dedicated GENUINE CRITIQUE section.

---

## Adaptations vs paper (documented)

| # | Adaptation | Reason | Impact on replication |
|---|---|---|---|
| A1 | Debian OpenFOAM 1906 instead of unknown 2019-era version | Paper does not name version | Negligible — `windAroundBuildings` tutorial unchanged across OF6/1806/1906 |
| A2 | `decomposeParDict` method changed from `scotch` to `simple` | Debian ships `dummyScotchDecomp` only | None — SIMPLE algorithm converges to same steady solution regardless of domain partitioning |
| A3 | Added custom `sampleDict` for line profiles | Paper reports no line profiles; needed for quantitative verification | Purely additive — does not alter the solved flow field |

## Runtime cost

- Meshing: ~35 s
- Solve: ~120 s (6-core MPI)
- Post-processing: ~15 s
- **Total wall time: < 3 min on 1 CPU node.**

## Deliverables

Under `report/`:
- `REPORT.md` (canonical Markdown report)
- `REPORT.tex` (LaTeX version + genuine critique section)
- `workflow.md` (this file)
- `artifacts_summary.md`
- `failure_analysis.md`
- `open_questions.json`
- `evidence/` (judge prompt + judge verdict + sample data)
