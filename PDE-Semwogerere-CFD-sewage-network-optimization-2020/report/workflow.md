# Replication Workflow

**Paper:** Semwogerere et al. 2020 — CFD Optimization of Municipal Sewage Networks (Tororo Municipality)
**Verdict:** REPLICATED
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/PDE-Semwogerere-CFD-sewage-network-optimization-2020/`

## Compute allocation

- **CherryRd (local)** — analytical Manning replication, all scripting, all
  post-processing, all reporting.
- **uicgpu (8×A100, but CFD is CPU here)** — OpenFOAM `interFoam` VOF
  spot-check run. Heavy CFD moved off local by policy.

## Stages

### Stage 0 — Paper acquisition
1. Fetch OA PDF from `rajpub.com/index.php/jam/article/download/8345/7894`.
2. Save at `work/paper.pdf`.
3. Identify concrete testable claims → C1 (Table 1), C2 (interFoam VOF fields),
   C3 (flow depends on D and S), C4 (k-ε + VOF suitable), C5 (Tororo policy).

### Stage 1 — Analytical Table 1 replication (C1)
1. Hypothesize provenance: classical Manning self-cleansing formula
   `S_min = (v_min · n / R^(2/3))²` with `R = D/4` (half-full circular).
2. Implement `work/mannings_selfcleansing.py`:
   - Sweep five (v_min, n, fill) configurations against paper's 8 rows.
   - Compute per-row absolute and relative error.
   - Emit `report/evidence/results_table1_replication.csv`.
3. Closed-form least-squares best-fit `v_min` in log-space (fixing `n=0.013`):
   - Emit `report/evidence/results_table1_bestfit.csv` (v_min = 0.595 m/s).
4. Cross-check: `work/manning_Q_curves.py` inverts each (D, S_paper) → v;
   emit `report/evidence/results_Q_curves.csv`.
5. Consolidate metadata → `report/evidence/results_table1_summary.json`.

**Exit criterion:** mean |rel err| < 5%. Achieved: 2.69%.

### Stage 2 — CFD spot-check (C2, C4) on uicgpu
1. Copy setup skeleton to uicgpu: `~/replicate/pde-semwogerere-2020/pipe_case/`.
2. Generate case with `work/interFoam_setup.sh`:
   - `blockMesh` — 8000-cell 2D hex mesh, 20 × 0.5 × 0.1 m.
   - `constant/transportProperties`, `constant/turbulenceProperties`,
     `constant/g` — paper's stated values.
   - `system/setFieldsDict` — initial water column h/D = 0.5.
   - `0/` — inlet U=(0.6,0,0), α=1; outlet zeroGradient + totalPressure;
     walls noSlip + k-ε wall functions.
   - `system/fvSolution`, `system/fvSchemes`, `system/controlDict`.
3. Source OpenFOAM environment, run:
   ```
   blockMesh; cp -r 0 0.orig; setFields; interFoam
   ```
4. Parse per-timestep α, U, p_rgh (Python) → `report/evidence/cfd_field_stats.json`.
5. Sanity checks (each an independent expectation):
   - mean |U| ≈ inlet 0.60 m/s
   - monotone α growth
   - hydrostatic p ≈ ρgh at bottom
   - MULES mass conservation
   - Courant control (Co_max < 0.5)

**Exit criterion:** solver runs to endTime with exit code 0 AND all five
sanity checks pass. Achieved: 18.9 s wall clock, all 5 pass.

### Stage 3 — Judgement
1. Submit REPORT.md text + evidence tables to LLM judge via Argo proxy.
2. Judge output archived at `report/evidence/llm_judge_output.txt`.
3. Judge verdict: REPLICATED.

### Stage 4 — Reporting
1. Compose `report/REPORT.md` with claims table, method, results, verdict,
   justification.
2. Emit companion artifacts:
   - `report/REPORT.tex` — LaTeX with dedicated Genuine Critique section.
   - `report/open_questions.json` — 5 truly-open follow-up questions.
   - `report/workflow.md` — this file.
   - `report/artifacts_summary.md` — inventory of all outputs.
   - `report/failure_analysis.md` — what did not work / caveats.

## Ordering & dependencies

```
Stage 0 (paper)
   │
   ├─► Stage 1 (Manning, local)                ── C1
   │        │
   │        └──► results_table1_*.csv
   │
   ├─► Stage 2 (interFoam, uicgpu)              ── C2, C4
   │        │
   │        └──► cfd_field_stats.json
   │
   └─► Stage 3 (LLM judge)                      ── verdict
            │
            └──► llm_judge_output.txt
                     │
                     └──► Stage 4 (report + backfill)
```

Stages 1 and 2 are independent and can be run in parallel.
Stages 3 and 4 depend on both.

## Reproducibility

- All scripts under `work/`.
- All evidence artifacts under `report/evidence/`.
- CFD case files re-generatable from `work/interFoam_setup.sh` (needs
  OpenFOAM 1906 or newer).
- Analytical scripts need only Python 3 + numpy.
- Total wall clock: analytical < 1 s; CFD ≈ 20 s on 1 core.

## Not attempted (out of scope)

- C5 (Tororo 535 → 1200 connections): policy claim, no municipal database
  available. Marked NOT-TESTED.
- Mesh-convergence study: paper reports no mesh count, so no comparable
  baseline exists.
- 3D circular pipe: paper is explicitly 2D (frontAndBack = empty). We
  respected the paper's geometry rather than "improving" it.
- Sediment / multiphase-solids extension: outside paper's scope.
