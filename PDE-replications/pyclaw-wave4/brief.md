# Brief — PyClaw replication (Wave 4)

## Paper
- **Title:** PyClaw: Accessible, Extensible, Scalable Tools for Wave Propagation Problems
- **Authors:** Ketcheson, Mandli, Ahmadia, Alghamdi, Quezada de Luna, Parsani, Knepley, Emmett
- **Venue:** SIAM Journal on Scientific Computing, 2012 (Vol. 34, No. 4, pp. C210–C231)
- **DOI:** 10.1137/110856976
- **Repo:** https://github.com/clawpack/pyclaw (part of the `clawpack` meta-package)

## What the paper is about
PyClaw is a Python wrapper around the Fortran Clawpack/SharpClaw kernels for
solving hyperbolic conservation laws on uniform grids in 1D/2D/3D using
high-order wave-propagation finite-volume schemes (Godunov / WENO / SSP-RK).
The headline contributions are:
1. A clean Python API over battle-tested Fortran kernels (no loss of speed).
2. Parallel scaling via PETSc (PetClaw) up to thousands of cores.
3. Easy extension of Riemann solvers / source terms in pure Python or Fortran.
4. A library of canonical example applications (acoustics, shallow water, Euler,
   shock-tube, KPP, traffic flow, p-system, ...).

## Replication scope (this attempt)
- **Scope chosen:** ONE canonical example — **1D acoustics** (the simplest
  textbook PyClaw example, used throughout the docs and the paper as a
  "hello-world" demo).
- **Reproduction target:** The expected pressure/velocity wave solution at a
  fixed end-time, verified against the analytical d'Alembert solution for
  constant-coefficient 1D acoustics:
  - `p_t + K * u_x = 0`, `u_t + (1/ρ) * p_x = 0`
  - Wave speed `c = sqrt(K/ρ)`; impedance `Z = sqrt(K*ρ)`.
  - With `K=1, ρ=1` → `c=1`. A Gaussian pulse in `p` splits into two
    half-amplitude pulses translating left and right at speed 1.
- **Concrete check:** Place a Gaussian pulse centered at x=0 at t=0, run to
  t=1.0 on x∈[-5,5], periodic BCs. Verify the two pulses are centered at
  x=±1.0 with half the original amplitude, and that the numerical solution
  matches the analytical d'Alembert solution within finite-volume truncation
  error.
- **Solver:** Classic Clawpack 2nd-order wave-propagation method with MC
  limiter (this is the algorithm featured in the original paper).

## Positioning vs. existing PDE replications
This replication complements the existing PDE collection in this folder:
- `godunov-loss/` — NN losses for hyperbolic PDEs (1D Burgers). **PyClaw is
  the classical-numerics counterpoint:** what state-of-the-art finite-volume
  shock capturing actually looks like before ML enters the picture.
- `amr-vs-mr-euler/` — adaptive mesh refinement for Euler. PyClaw is the
  uniform-grid baseline that AMR frameworks are usually benchmarked against.
- `kinetic-jl/` — kinetic / hyperbolic solvers in Julia. PyClaw is the
  Python+Fortran analog; useful to compare API design and the cost of the
  language-binding layer.
- `fno-neuraloperator/` — neural operators for PDEs. PyClaw can serve as a
  classical ground-truth generator (RP-style training data).

Hyperbolic conservation laws sit at the core of CFD, shallow-water /
tsunami modeling, acoustics, and gas dynamics, so a working, scriptable
Clawpack install rounds out the PDE side of the project.

## Constraints
- Free compute — CherryRd CPU only.
- Time budget: 30–60 min wallclock.
- LLM verdict via argo proxy if needed (`argo/argo:claude-opus-4.7`,
  `http://127.0.0.1:44497/v1`, key `stevens`).

## Deliverables
- `brief.md` (this file)
- `artifact_harvest.md` — what `pip install clawpack` actually delivered
- `attempt_log.md` — install/run log
- `evidence/` — example script, run output, plots, JSON of error norms
- `REPORT.md` — verdict, coverage/agreement, resources
