# FLUPS Replication — Progress Log

**Target paper:** Caprace, D.-G., Gillis, T., Chatelain, P. (2021). *FLUPS: A Fourier-Based Library of Unbounded Poisson Solvers*. SIAM Journal on Scientific Computing 43(1):C31–C60. DOI: 10.1137/19M1303848

**Repo:** https://github.com/vortexlab-uclouvain/flups (BSD-3-Clause)
**Replication start:** 2026-05-28
**Host:** CherryRd (will offload heavy MPI runs if needed)
**Owner:** Ollie (subagent of Rick's main session)

## Plan

1. ✅ Set up project skeleton + progress JSON
2. ⏳ Verify openness (license, public repo, examples reproducible without auth)
3. ⏳ Pick one concrete claim to reproduce. Candidates from FLUPS paper:
   - **Spectral / high-order convergence** of unbounded Poisson solve for known analytic source (Gaussian → analytical potential).
   - **Boundary condition mixing** (unbounded × periodic × symmetric) accuracy on validation_3d example.
   - **Strong/weak scaling** on a single node (skip multi-node; honest).
4. ⏳ Build FLUPS dependencies: FFTW3 (MPI), HDF5 (parallel), an MPI implementation, optional H3LPR (companion helper).
5. ⏳ Build FLUPS itself with `make` (uses arch-makefile pattern).
6. ⏳ Run `validation` (the in-tree convergence-test driver) for at least one BC combo and sweep N to plot error vs. N.
7. ⏳ Compare slopes / asymptotic error to paper's claims.
8. ⏳ If build fails after two grounded attempts → implement a small independent free-space Poisson solver (FFT + analytic Green's function) and reproduce the spectral-convergence claim there.
9. ⏳ Write REPORT.md with claim table, agreement scores, friction tags, limitations.

## Status timeline

- **14:41 UTC** — directory + JSON created, plan drafted.
- **14:43 UTC** — verified openness: flups public on GitHub, dependency h3lpr also OSS (BSD-3). Found license discrepancy (README claims BSD-3, actual LICENSE is Apache-2.0 — both permit replication).
- **14:44 UTC** — built h3lpr against Homebrew g++-15 via `OMPI_CXX` (Apple clang lacks OpenMP). Installed to `/tmp/install/h3lpr/`.
- **14:45 UTC** — built FLUPS: initial attempt failed because Homebrew's HDF5 is serial-only and `hdf5_io.cpp` needs the MPI symbols. Removed `-DHAVE_HDF5` and rebuilt cleanly. Installed `libflups_{a2a,nb,isr}.a` + LGF/MEHR kernels.
- **14:46 UTC** — built `samples/validation/flups_validation_{a2a,nb,isr}`. Patched macOS dylib install names so dyld can find `libh3lpr.so`.
- **14:46 UTC** — smoke test: fully-unbounded 16^3 CHAT2 Poisson solve runs and reports L2=1.68e-3.
- **14:47–14:54 UTC** — convergence sweep across 3 scenarios × 6 resolutions (18 solves). Largest single solve (96^3 unbounded) took ~17 min CPU.
- **14:55 UTC** — analysis: CHAT2 L2 slope=1.93 (paper says 2nd order ✅); HEJ4 L2 slope=3.19 climbing to 3.74 in the last bin (paper says 4th-order ✅, pre-asymptotic); periodic L2 ~3e-16 (paper says exact ✅).
- **14:56 UTC** — MPI sanity run: 2 ranks at N=64 reproduces serial L2 bit-exactly (1.187796827220e-04).
- **14:58 UTC** — wrote README.md and REPORT.md with claim-by-claim table, friction tags, limitations. DONE.
