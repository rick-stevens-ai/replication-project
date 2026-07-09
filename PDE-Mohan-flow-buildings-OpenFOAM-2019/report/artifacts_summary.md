# Artifacts Summary — PDE-Mohan-flow-buildings-OpenFOAM-2019

**Paper:** Mohan, Sundararaj, Thiagarajan (2019), AIP Conf. Proc. 2112, 020149.
**Replicator:** OpenClaw subagent (Argo Opus 4.7)
**Date:** 2026-07-04 (CDT)
**Verdict:** REPLICATED

---

## Report artifacts (under `report/`)

| Artifact | Purpose | Format |
|---|---|---|
| `REPORT.md` | Canonical Markdown report — paper summary, claims table, method, results-vs-paper, verdict, caveats | Markdown |
| `REPORT.tex` | LaTeX version + dedicated GENUINE CRITIQUE section (scientific critique of paper's scope, methodology, presentation) | LaTeX |
| `workflow.md` | Phase-by-phase workflow, adaptations, runtime cost, deliverable inventory | Markdown |
| `artifacts_summary.md` | This file — inventory of all produced artifacts | Markdown |
| `failure_analysis.md` | Root-cause list of every non-trivial issue encountered during replication | Markdown |
| `open_questions.json` | 5 genuinely open questions targeting paper's scientific gaps | JSON |
| `evidence/judge_prompt.md` | LLM-judge prompt (claims + measured evidence summary) | Markdown |
| `evidence/judge_verdict.txt` | Argo GPT-5.2 judge response | Plain text |

## Source paper artifacts (under `paper/`)

| Artifact | Description | sha256 | Size |
|---|---|---|---|
| `Mohan2019.pdf` | Web-archive capture 2022-12-24 of AIP scitation PDF | `7c3b2878ab5245ce82fb9bccdcaeda9648146a5589b8f0017093feaee1b68a2f` | 1,835,796 B |

## Case artifacts (under `case/` or workdir `/data/stevens/replicate-mohan-2019-buildings/case/`)

| Artifact | Description |
|---|---|
| `constant/transportProperties` | `nu 1.5e-05` (paper-verified) |
| `constant/turbulenceProperties` | `simulationType RAS; RASModel kEpsilon` |
| `constant/triSurface/buildings.obj` | 600,096-line triangulated building surface (decompressed from tutorial) |
| `constant/triSurface/buildings.eMesh` | 16,107 feature edges from `surfaceFeatureExtract` |
| `0.orig/U` | `Uinlet (10 0 0)` (paper-verified) |
| `0.orig/k` | `kInlet 1.5` (paper-verified via `k = 1.5*(I*U)^2`, I=0.1) |
| `0.orig/epsilon` | `epsilonInlet 0.05` (paper-verified via `Cμ · k^{3/2}/L`) |
| `system/controlDict` | `application simpleFoam; endTime 400` (paper-verified) |
| `system/decomposeParDict` | Modified: method `simple`, `numberOfSubdomains 6`, `simpleCoeffs n (3 2 1)` (adaptation A2) |
| `system/sampleDict` | Custom (added by replicator) — 6 line samples for quantitative verification |
| `constant/polyMesh/` | Background mesh from `blockMesh` (5000 hex cells) |
| Snappy mesh output | 185,237 cells after `snappyHexMesh -overwrite` (34.34 s wall) |

## Solve artifacts

| Artifact | Description |
|---|---|
| `log.blockMesh` | blockMesh log |
| `log.snappyHexMesh` | Meshing log (34.34 s wall, 185,237 cells) |
| `log.decomposePar` | Parallel decomposition log (6 subdomains) |
| `log.simpleFoam` | Solver log — 400 SIMPLE iterations, ~120 s wall |
| `log.reconstructPar` | Time-directory reconstruction log |
| `log.checkMesh` | Mesh-quality check — all pass |
| `postProcessing/fieldMinMax/400/fieldMinMax.dat` | Global min/max of U, p, k, ε at t=400 |
| `postProcessing/sampleDict/400/*.xy` | Line profiles at 6 sample lines (raw XY files) |
| `postProcessing/streamLines/400/*.vtk` | 40 streamline tracks, 18,543 total sample points |

## Numerical result summary (from artifacts, reproduced in REPORT.md §4)

**Global field extrema (fieldMinMax @ t=400):**

- `max|U|`      = 20.663 m/s at (8.84, 97.6, 4.38) m — leading-building corner acceleration (2.07× inlet)
- `min U_x`     = −9.997 m/s at (31.2, 101.3, 0.87) m — strong reverse-flow bubble
- `max U_y`     = +16.848 m/s at (31.3, 103.1, 2.63) m
- `min U_y`     = −16.147 m/s at (7.09, 101.0, 0.87) m
- `max U_z`     = +15.214 m/s at (7.11, 125.9, 31.1) m
- `min U_z`     = −12.385 m/s at (157.2, 136.1, 21.9) m
- `max k`       = 27.84 m²/s² at (5.29, 102.8, 29.3) m — 18.6× k_inlet
- `max ε`       = 45.36 at (227.4, 110.1, 50.0) m
- `min p` (kin.)= −146.26 Pa·m⁻¹ at (10.57, 117.4, 35.0) m
- `max p` (kin.)= +196.53 Pa·m⁻¹ at (7.43, 122.4, 9.63) m

**Convergence (@ iter 400):** U_x res 2.39e-5, p res 4.30e-4, k res 7.75e-5, ε res 2.69e-4.

**Line profile summary:**

| Line | Description | U_x range (m/s) | \|U\| range | % U_x<0 |
|---|---|---|---|---|
| inletZ  | x=0, z∈[0,140] | 0.05 → 10.99 | 0.06 → 11.64 | 0 |
| x100Z   | x=100 vertical | −0.90 → 15.04 | 0.01 → 15.16 | 12 |
| x200Z   | x=200 vertical | 8.34 → 14.07 | 9.05 → 14.08 | 0 |
| x300Z   | x=300 vertical | −1.15 → 13.48 | 0.00 → 13.51 | 30 |
| z20X    | z=20 streamwise | −1.62 → 12.81 | 0.47 → 17.07 | 29 |
| z60X    | z=60 streamwise | 7.86 → 15.16 | 7.91 → 15.33 | 0 |

## Tool versions

| Tool | Version |
|---|---|
| OpenFOAM | 1906 (Debian `openfoam 1906.191111+dfsg1-2build1`) |
| Case package | `openfoam-examples 1906.191111+dfsg1-2build1` |
| OpenMPI | as shipped with Debian OpenFOAM (`/usr/bin/mpirun`) |
| Python | 3.10 (stats only) |
| Argo LLM proxy | `localhost:44497`, model `argo:gpt-5.2` (free tier) |

## Sizes

- Report set (Markdown + LaTeX + support): ~40 KB
- Solve logs + post-processing: ~5 MB
- Streamlines VTK: ~2 MB
- Line profile XY files: ~200 KB
- Field data (converged snapshot t=400 reconstructed): ~50 MB (retained on uicgpu workdir; not copied to Dropbox)
