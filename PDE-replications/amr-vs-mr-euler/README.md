# AMR vs MR for the Compressible Euler Equations — Replication Study

Replication target: **Deiterding, Domingues, Gomes, Schneider (2016)**,
*Comparison of Adaptive Multiresolution and Adaptive Mesh Refinement Applied
to Simulations of the Compressible Euler Equations*, SIAM J. Sci. Comput.,
38(5), S173–S193.

This study reproduces the **qualitative claim** of the paper — that adaptive
multiresolution (MR) and block-structured adaptive mesh refinement (AMR) trade
off solution accuracy against active degrees-of-freedom and CPU time in
characteristically different ways — using a combination of:

1. **Carmen** (https://github.com/waveletApplications/carmen) — the actual
   open-source MR code cited by the paper, built from source on macOS 26.
2. A **clean-room Python implementation** of all three strategies (uniform FV,
   block-structured 1D AMR, Harten-style MR), so all comparisons share
   *exactly* the same physics, Riemann solver, and limiter — meaning differences
   are attributable to the adaptive strategy alone.

## Repository layout

```
amr-vs-mr-euler/
├── README.md                  ← this file
├── PROGRESS.md                ← live status during the run
├── REPORT.md                  ← findings, tables, claim-by-claim coverage
├── scripts/
│   ├── euler_solver.py        ← Python uniform / AMR / MR Euler solvers
│   └── run_sweep.py           ← runs Sod sweep + generates CSV & figures
├── results/
│   ├── carmen-*.prf           ← Carmen profile (CPU, compression) outputs
│   ├── carmen-*.integral.dat  ← Carmen integral diagnostics
│   └── sweep_results.csv      ← Python Sod sweep table
├── figures/                   ← Pareto plots + solution profiles
└── logs/                      ← Build & run logs
```

## Honest scope

- **MR side (Carmen)**: built and ran successfully on macOS 26 with Apple Clang
  17 + libc++ (two small patches needed; see REPORT.md). I ran a 3D
  Sod-blast-like test at scales 5 and 6 and harvested Carmen's own
  `Leaf/Memory/CPU compression` reports.
- **AMR side**: I did **not** build AMROC. AMROC is heavyweight C++ requiring
  VTF, MPI, HDF5, and several legacy dependencies that no longer install
  cleanly on macOS 26. I disclose this and substitute a clean-room 1D AMR
  implementation for the head-to-head numerics. The substitution is real and
  is flagged in REPORT.md.
- **Python solvers**: ~600 lines, runs in seconds on CPU, all three strategies
  share identical physics so the comparison is meaningful for the
  *qualitative* tradeoff, not for absolute wall-clock numbers (the production
  Carmen code is much faster per cell update than Python).

## Reproducing

```bash
# Carmen MR (optional — requires macOS SDK 15.4 libc++ on macOS 26):
git clone https://github.com/waveletApplications/carmen
# Apply patches: replace global `rank` with `g_rank` in main.cpp,
# Parameters.cpp, Parameters.h, Parallel.cpp; add SchemeAUSMDV.o to carmen.mak
# Then build with libc++ from an older SDK.

# Python comparison:
cd amr-vs-mr-euler
python3 scripts/run_sweep.py
# → produces results/sweep_results.csv + 4 figures in figures/
```

## License

This study's own code (`scripts/*.py`) is released to the public domain (CC0).
Carmen itself is GPLv2+ (per file headers in the upstream repo) — see notes
in REPORT.md about the missing top-level LICENSE file. No Carmen source is
vendored in this repository.
