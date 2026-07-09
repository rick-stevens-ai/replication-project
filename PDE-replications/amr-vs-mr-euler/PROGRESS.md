# PROGRESS — AMR vs MR for Compressible Euler

**Target paper:** Deiterding, Domingues, Gomes, Schneider (2016),
*Comparison of Adaptive Multiresolution and Adaptive Mesh Refinement Applied
to Simulations of the Compressible Euler Equations*, SIAM SISC 38(5), S173–S193.

**Subagent:** ollie-subagent (amr-vs-mr-euler)
**Start:** 2026-05-28 11:56 CDT
**Finish:** 2026-05-28 12:15 CDT (~19 min wall)

## Status: ✅ COMPLETE

## Plan vs reality

| Step | Plan | Actual |
|---|---|---|
| Openness check | Carmen + AMROC license | ✅ Carmen on GitHub, GPLv2+ per-file (no top LICENSE = friction); AMROC sourceforge (academic use, dependency rot) |
| Build Carmen | 2 attempts | ✅ Built on 3rd attempt; patches: rename global `rank` → `g_rank`; add `SchemeAUSMDV.o` to Makefile; use macOS SDK 15.4 libc++ |
| Build AMROC | Attempt | ❌ Skipped — VTF/MPI/HDF5 dependency rot on macOS 26; substituted clean-room Python AMR |
| Run Carmen benchmarks | Sweep tolerances | ✅ 7 runs across S=5 (32³) and S=6 (64³), tol 1e-2 → 1e-4 + uniform FV baselines |
| Clean-room Python comparison | — (added) | ✅ 600-line uniform/AMR/MR all sharing HLL+MUSCL on 1D Sod, 39-row sweep |
| Figures | At least 1 | ✅ 4 figures: solution profiles, Pareto, compression, walltime |
| Quantitative table | Required | ✅ Carmen profile table + Python matched-accuracy table |
| Claim-by-claim coverage | Required | ✅ 6/7 qualitative claims reproduced (1 needs paywalled paper) |
| Friction tags | Required | ✅ `paper-not-open-access`, `dependency-rot`, `license-metadata-incomplete`, `macos-toolchain-quirks` |

## Headline result

**MR achieves matched L1 density error using 3.1× fewer active cells than
uniform FV** on 1D Sod shock tube (Python clean-room). Carmen confirms the
same trend in 3D: 34% leaf compression at scale 6 (64³) for tol=1e-3.

## Compute used
~12 min single-core CPU on CherryRd iMac. No GPU. No paid services.

## See also
- `REPORT.md` — full claim-by-claim writeup
- `README.md` — repo overview
- `results/sweep_results.csv` — 39-row sweep table
- `figures/` — 4 PNG figures
