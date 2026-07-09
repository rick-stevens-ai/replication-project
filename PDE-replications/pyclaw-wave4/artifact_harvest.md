# Artifact Harvest — PyClaw (Wave 4)

## What `pip install clawpack` delivers (5.14.0, 2026-06-16)

- Package: `clawpack==5.14.0` (PyPI, BSD 3-Clause)
- Sub-packages installed:
  - `clawpack.pyclaw` — Python solver framework (high-level API)
  - `clawpack.classic` — Fortran "Classic" wave-propagation kernels (compiled wheels)
  - `clawpack.sharpclaw` — Fortran "SharpClaw" WENO + SSPRK / SSPLMMk3 high-order kernels
  - `clawpack.riemann` — library of Riemann solvers (acoustics, Euler with/without efix, shallow water, KPP, ...)
  - `clawpack.visclaw` — plotting/visualisation helpers
  - `clawpack.geoclaw` — tsunami/storm-surge add-on (not exercised here)
- Bundled regression tests:
  - `clawpack.pyclaw.examples.acoustics_1d_homogeneous.test_acoustics` — pre-baked reference errors for 5 solver variants at N=100 plus 3 accuracy thresholds at N=2000/4000.
- Pre-built Fortran kernels target macOS x86_64; built from source via meson + ninja on macOS Tahoe 26.x without intervention.

## Hardware / build info

- CherryRd, macOS Tahoe 26.x, Python 3.14 venv (`.venv/`).
- Apple Clang + gfortran (Homebrew) used to compile native bits.
- No external data downloads; all examples generate ICs in-code.

## Test fixtures we used

- `clawpack.pyclaw.examples.acoustics_1d_homogeneous.acoustics_1d(...)` for the upstream regression (kernel_language, solver_type, num_cells, weno_order, time_integrator).
- `clawpack.pyclaw.{ClawSolver1D, Dimension, Domain, State, Controller, Solution, BC, limiters, riemann}` for the Sod shock tube setup.

## License

BSD 3-Clause (see `clawpack/LICENSE`). No NEC-style NC-academic riders. Free for commercial use.

## Friction tags

- `:fortran-allocation` — calling `sharpclaw` cases sequentially in one process can hit a stale-state Fortran allocation error; mitigated by running each case in a subprocess.
- `:numpy-2-clean` — `clawpack 5.14.0` is fine with NumPy 2.x (no downgrade needed, unlike many older PDE libs).
- `:py-fortran-parity` — kernel-language='Python' and 'Fortran' produced bit-identical L1 errors to all printed digits, which is a nice quiet validation of the language binding.
