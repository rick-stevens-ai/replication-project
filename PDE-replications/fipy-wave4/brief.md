# Brief — FiPy Replication

**Paper:** Guyer, J. E., Wheeler, D., Warren, J. A. "FiPy: Partial Differential Equations with Python." *Computing in Science & Engineering* 11(3), 2009, pp. 6–15. DOI: 10.1109/MCSE.2009.52
**Upstream code:** https://github.com/usnistgov/fipy (NIST)
**Wave:** PDE-collection Wave 4
**Date:** 2026-06-16

## Goal
Install FiPy in an isolated venv on CherryRd (CPU only, no GPU) and run **one canonical example** from the FiPy documentation, verifying that the numerical result agrees with the analytical reference shown in the docs.

## Chosen example
**1D transient diffusion with a step-function initial condition** — `examples/diffusion/mesh1D.py` from the FiPy distribution.

Why this example:
- It is the *first* worked example in the FiPy documentation/tutorial.
- It has a closed-form analytical solution (the complementary error function `erfc((x-L/2)/(2 sqrt(D t)))`) for an infinite domain with a step initial condition, which FiPy's docs explicitly compare against.
- It exercises core FiPy machinery (Grid1D mesh, CellVariable, TransientTerm, DiffusionTerm, sparse-matrix solve) without requiring a phase-field nonlinear coupling that would muddy the numerical-vs-analytical comparison.

## Pass criteria
- FiPy installs cleanly via `pip` into a fresh Python venv.
- The 1D diffusion example runs to the documented stopping time.
- Numerical solution at the final timestep matches the analytical `erfc` profile within tolerance (L2 error per cell < 1e-2; L∞ < ~3e-2, accounting for finite-domain reflection and finite Δx).
- Convergence: refining the mesh halves the L2 error roughly linearly (first-order in Δx for the implicit Euler / FV scheme used in the tutorial).

## Time budget
30–60 min, CPU only.

## Compute
CherryRd local Python venv. No GPU. No HPC. No external API except optional argo proxy for LLM scoring (not strictly needed).
