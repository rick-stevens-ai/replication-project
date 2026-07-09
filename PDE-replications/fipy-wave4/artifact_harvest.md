# Artifact Harvest — FiPy (Wave 4)

## What `pip install fipy` delivers (4.0.2, 2026-06-16)

- Package: `fipy==4.0.2` (PyPI, NIST public-domain license)
- Bundled examples: `examples/diffusion/*` (mesh1D, mesh2D, ...), `examples/phase/*`, `examples/cahnHilliard/*`, `examples/levelSet/*`, ...
- Default solver: scipy-sparse LU / GMRES, with optional bindings to PySparse, Trilinos, PETSc (none of those required for the 1-D example).
- Tested upstream against Python 3.x via the FiPy CI; runs cleanly under Python 3.14 in our venv.

## License

NIST public-domain (see `LICENSE.txt` in the source tree). Free for any use.

## Hardware / build info

- CherryRd, macOS Tahoe 26.x, Python 3.14 venv.
- Pure-Python install; no C/Fortran build needed beyond what SciPy already ships.

## Friction tags

- `:long-runtimes` — implicit Euler with dt ∝ Δx² leads to 17 778 steps at nx=400; FiPy doesn't auto-suggest a larger time step. Easily fixed by users who notice.
- `:reference-mismatch` — the docs example compares the finite-domain solve to the half-space `erfc`. Users may be surprised that mesh refinement does *not* reduce the apparent error below ~1 % in this setup; a self-convergence study against a high-resolution FiPy reference is what one actually wants for an order-of-accuracy check.
- `:no-numpy2-issue` — `fipy 4.0.2` is NumPy 2 compatible; no downgrade needed.
