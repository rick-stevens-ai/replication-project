# Artifact Harvest — OSTI 2526549

## Paper PDF
- URL: https://www.osti.gov/servlets/purl/2526549
- Fetched: 2026-07-02 (via uicgpu HTTPS proxy <lan-host>:3128 — cherryrd tailnet cannot reach OSTI directly)
- Local: `work/paper.pdf`  (923 281 bytes, sha256 recorded below)
- HTTP: 200

## Reference code
- URL: https://github.com/zheyuanhu01/Tempered_Fractional_PINN
- Contents: 12 Python scripts (MCFPINN, MCFPINN_quad, MCFPINN_time, MCFPINN_time_quad, MCTFPINN, MCTFPINN_quad, MCTFPINN_Time, MCTFPINN_Time_quad, and 4 inverse-problem variants for α / λ)
- Cloned on: uicgpu:/tmp/Tempered_Fractional_PINN (fresh clone, 2026-07-02)
- License: not explicitly declared in-repo (author-owned research release)
- Local copy dropped into: `work/code_snapshot/` (see below)

## Datasets
- **No external dataset needed.** The benchmark is a fabricated-solution PDE test:
  - Exact solution `u(x)` given by Eq. (29) (linear combination of `(1-‖x‖²)^{α/2}` and `(1-‖x‖²)^{1+α/2}` weighted by unit-Gaussian coefficients).
  - Forcing term `f(x)` computed analytically per Table 1 of the paper (implemented in the reference code's `resample()` branch for `problem == 7`).
  - Test set: 20 000 points sampled uniformly inside the unit ball.
- All inputs are seeded (`SEED=0`).

## Dependencies
- JAX 0.10.0 + CUDA (jaxcfd-venv on uicgpu; 8 × A100 80 GB visible)
- Haiku 0.0.16, Optax 0.2.8, SciPy 1.17.1, NumPy, tqdm 4.68.3, Pandas 3.0.2

## Code patch applied (minimal, JAX-API compatibility only)
1. `jnp.clip(x, a_min=…)` → `jnp.clip(x, min=…)` (JAX >=0.4 dropped `a_min`/`a_max` kwargs). One-liner `sed -i 's/a_min=/min=/g; s/a_max=/max=/g'` across all 12 files.
2. `from jax.config import config; config.update("jax_enable_x64", True)` → `jax.config.update("jax_enable_x64", True)` in `MCFPINN_quad.py` (the `jax.config` submodule was moved to attribute access in JAX >=0.4).

These are pure compatibility fixes; no algorithmic change.
