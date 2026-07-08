# HARMPI GRMHD Replication — Progress Log

**Subagent:** Slot D
**Started:** 2026-05-27 12:20 CDT
**Mission:** Replicate HARMPI GRMHD benchmark (2D Fishbone-Moncrief torus + optional 3D MAD)
**Target:** AI ATLAS P007 gap-fill (GRMHD / EHT BH imaging)

## Time budget: 12h wall-clock max

## Phases
- [x] Phase 1: Paper + code recon — DONE (PAPER_NOTES.md)
- [x] Phase 2: Setup on uicgpu — DONE (serial gcc -O2, then MPI rebuild for 3D)
- [x] Phase 3: 2D Fishbone-Moncrief torus run — DONE (128², tf=2000M, REPLICATED)
- [x] Phase 4: 3D demo run — DONE (64²×32, MPI 4×4×4, tf=500M, DEMONSTRATED early MRI growth)
- [x] Phase 5: Eval + report — DONE (PDF compiled, indices updated)

## Completion summary
- Wall: ≥2 hours end-to-end (started 12:20 CDT, finished 14:15 CDT)
- CPU-core-hours: 12.2 (1.5 for 2D + 10.7 for 3D)
- GPU-hours: 0
- Verdict: REPLICATED (2D) + DEMONSTRATED (3D)
- Report: `report/harmpi_grmhd_replication_report.pdf` (10 pages, 1.16 MB)

## Setup notes
- uicgpu01: 255 cores, 2TB RAM, 13TB free on /data, gcc 9.4, mpicc OK
- Workspace: `/data/stevens/harmpi/harmpi/` (cloned from atchekho/harmpi)
- Compile: USEMPI=0 USEOMP=0 (serial), -O2, completed in ~30s with only minor warnings
- Binary: `./harm` (about 700KB)
- Default config (init.c TORUS_PROBLEM): a=0.9, gam=5/3, rin=6, rmax=13, beta=100, Rout=1e5, tf=10000M, 128x128 (2D)
  - Note: default is a=0.9, NOT a=0.9375 as the README claimed; will use the code's actual value
- For runtime control we'll reduce tf to 2000M for initial benchmark

