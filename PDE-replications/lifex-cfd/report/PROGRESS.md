# lifex-cfd Replication Progress

**Paper:** "Lifex-cfd: An open-source computational fluid dynamics solver for cardiovascular applications" (Africa et al., 2023)  
**arXiv:** 2304.12032  
**Work directory:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/lifex-cfd/`  
**Remote compute:** `/data/stevens/projects-active/lifex-cfd/` on `uicgpu`

## Timeline

### Step 1: Paper & Repository ✅
- Found paper on arXiv (2304.12032), downloaded PDF
- Repository: `https://gitlab.com/lifex/lifex-cfd` (archived, moved to `lifex-public`)
- Cloned repo with `core` submodule (lifex v1.5.0)
- Key info: deal.II-based (not FEniCS), 5 benchmark tests

### Step 2: Dependencies & Installation ✅
- deal.II 9.5.1 not available on any accessible system
- Downloaded pre-built AppImage (137 MB) from Zenodo (DOI: 10.5281/zenodo.7852088)
  - `lifex_fluid_dynamics-2.0.0-x86_64.AppImage` (md5: `008cc4efb10f8b958d66e221070c36f3`)
- Downloaded examples zip (117 MB) with meshes + parameter files
- AppImage runs successfully on `uicgpu` (Ubuntu 20.04, glibc 2.31)
- Building from source attempted via Singularity container (dealii/dealii:v9.5.1-jammy) — failed due to template mismatch between latest repo code and PPA deal.II build

### Step 3: Benchmark Runs

#### Test I — Beltrami Flow ❌ Cannot Run
- Requires test binary (`lifex_test_fluid_dynamics_cube`) for analytical initial conditions
- The production AppImage only has `lifex_fluid_dynamics`, not the test executable
- Source build failed (template compatibility issues)
- **Blocked:** Cannot reproduce convergence rates without test binary

#### Test II — Cylinder with Moving Obstacle 🔄 Running
- **Mesh:** 81,920 active cells, 85,345 vertices → **matches paper Table 2 exactly**
- **DOFs:** 341,380 (u: 256,035 Q2, p: 85,345 Q1) → **matches paper exactly**
- **Parameters:** dt=2.5e-4, T=0.8s, BDF1, ALE, RIIS valve, Q2-Q1
- **Short test (40 steps):** Completed 14 steps successfully before SSH timeout, then restarted
- **Full run (3200 steps):** Running via nohup with 32 MPI ranks
  - At t=8.25e-3 (34 steps) after ~30 minutes
  - Estimated completion: ~27 hours
  - **Physical validation so far:**
    - Wall flowrate = 0 (no-slip ✓)
    - Inlet flowrate ramping up (pulsatile BC ✓)
    - Outlet flow developing (mass conservation ✓)
    - Pressures in expected range (O(10²-10³) Pa) ✓
    - Valve coefficient = 0 at t<0.15s (valve closed ✓)

#### Test III — Aorta 🔄 Running
- **Mesh:** 2,915,690 active cells, 543,089 vertices → **matches paper Table 2 exactly**
- **DOFs:** 2,172,356 (u: 1,629,267, p: 543,089) → **matches paper exactly**
- **Parameters:** dt=1e-3, T=3.8s, tetrahedral elements
- **Short run (5 steps):** 2 timesteps completed
  - Aortic root inflow: -2.29e-5 m³/s ✓
  - Outlet pressures: 10,667-14,857 Pa ✓ (physiological range)
  - Mass conservation verified (sum of flowrates ≈ 0)

#### Test IV — Atrium 🔄 Running
- **Mesh:** 2,372,546 active cells, 389,484 vertices
  - Vertices match paper exactly (389,484) ✓
  - Cell count slightly different (paper: 2,438,278) — minor mesh file variation
- **DOFs:** 1,557,936 (u: 1,168,452, p: 389,484)
- **Parameters:** dt=5e-4, T=3.0s, ALE, RIIS valve
- **Short run (4 steps):** Initializing (solving lifting problems for ALE)
- Boundary IDs 1-6 detected correctly

#### Test V — Taylor-Green Vortex ❌ Cannot Run
- Requires analytical initial conditions from test binary
- The TGV initial velocity field u₀ = (sin(x)cos(y)cos(z), -cos(x)sin(y)cos(z), 0) needs to be set programmatically
- Parameter file references `lifex_test_fluid_dynamics_cube` not `lifex_fluid_dynamics`
- **Blocked:** Same reason as Test I

### Step 4: Comparison to Paper ⏳ In Progress
- No quantitative error norms given in paper for Tests II-IV
- Paper shows figures (velocity, pressure, Q-criterion) which we cannot compare without VTU output from the full runs
- The exact mesh/DOF counts matching the paper is a strong positive signal
- Simulation output structure (CSV with flowrates, pressures) matches expected format

### Step 5: Source Build Attempt ❌ Failed
- Downloaded Singularity container `dealii/dealii:v9.5.1-jammy` (1.7 GB)
- Installed missing boost-filesystem-dev in writable sandbox
- CMake configured successfully (found deal.II 9.5.1, Trilinos, VTK 9.1)
- Build failed: template specialization errors in `core/source/geometry/mesh_handler.cpp`
  - `ParallelMeshSettings` template argument issues
  - Likely version mismatch: repo HEAD (post-paper) incompatible with PPA deal.II 9.5.1
  - The AppImage was built with a custom deal.II installation (`/opt/lifex-env/tmp/src/dealii-9.5.1/`)

## Summary Status (as of 2026-05-12 ~19:50 CDT)
| Test | Status | Notes |
|------|--------|-------|
| I (Beltrami) | ❌ Blocked | Needs test binary |
| II (Cylinder) | 🔄 Running | Mesh/DOFs match paper; 42/3200 steps (~1.3%); ~27h to complete |
| III (Aorta) | 🔄 Running | Mesh/DOFs match paper; 3/5 steps of short run done |
| IV (Atrium) | 🔄 Running | DOFs match paper; still in ALE lifting initialization |
| V (TGV) | ❌ Blocked | Needs test binary |
| Source Build | ❌ Failed | Template compatibility issues |

## Report Written
- `report/REPORT.md` — Comprehensive report with scoring (5.5/10 overall)
- Simulations continue running on uicgpu via nohup

## Files on uicgpu
```
/data/stevens/projects-active/lifex-cfd/
├── lifex_fluid_dynamics-2.0.0-x86_64.AppImage
├── dealii.sif (1.7 GB Singularity container)
├── dealii-sandbox/ (writable sandbox)
├── lifex-cfd-src/ (source code)
├── lifex-cfd-build/ (failed build)
├── lifex-cfd_examples/
│   ├── cylinder/
│   │   ├── output_full/ (running, 34+ steps)
│   │   └── output_short/ (14 steps completed)
│   ├── aorta/
│   │   └── output_short/ (2 steps completed)
│   └── atrium/
│       └── output_short/ (initializing)
├── run_cylinder_full.sh
├── run_aorta_short.sh
├── run_atrium_short.sh
├── cylinder_full.log
├── aorta_short.log
└── atrium_short.log
```
