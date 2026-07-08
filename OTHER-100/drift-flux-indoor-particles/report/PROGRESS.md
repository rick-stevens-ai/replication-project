# Progress: Drift-Flux Indoor Particle Model Replication
## Chen, Yu & Lai (2006) — Atmospheric Environment 40, 357-367
**Priority**: TOP OF QUEUE
**Started**: 2026-05-15

## Status: STAGE 1 — RUNNING

### Completed
- [x] Paper analysis and technical extraction (2026-05-15)
- [x] APPROACH.md written with full replication plan
- [x] OpenFOAM case setup: blockMeshDict, BCs, turbulence model (needs OpenFOAM on a machine)
- [x] Particle transport Python solver — vectorized numpy FVM (particle_transport_fast.py)
- [x] Particle property calculations verified (10 sizes, 0.01-10 μm)
- [x] Lai-Nazaroff (2000) deposition model implemented and verified
- [x] Solver stability verified (CFL-limited, dt~0.04s)
- [x] Single particle test: 1μm over 1800s in 38s wall time
- [x] Case 1 (U=0.225) full 10-size run launched (background on CherryRd)

### In Progress
- [ ] Case 1 full run completing (~6 min total for all 10 sizes)
- [ ] Need proper flow field from OpenFOAM (current: analytical approximation)

### Next Steps
- [ ] Run OpenFOAM on uicgpu for proper airflow (simpleFoam + RNG k-ε)
- [ ] Export OpenFOAM velocity + nut fields to Python
- [ ] Re-run particle transport with real flow field
- [ ] Generate validation figures (Figs 3-7)
- [ ] Run Case 2 (U=0.45 m/s)
- [ ] Write replication report

### Performance
- Vectorized numpy solver: ~38s per particle size per 1800s simulation
- 10 sizes × 2 cases = ~12 min total compute (CherryRd)
- Grid: 40×20×20 = 16,000 cells, dt=0.041s, 44,120 steps per 1800s

### Known Issue
- Analytical flow field doesn't conserve mass → C accumulates > 1
- Need OpenFOAM divergence-free velocity field to fix this
- OpenFOAM not installed on CherryRd; available on uicgpu

### Last Updated: 2026-05-15 11:30 CDT
