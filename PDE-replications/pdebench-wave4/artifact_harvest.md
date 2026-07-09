# Artifact Harvest — PDEBench Wave 4 (1D Burgers)

## Upstream artifact reused

- `pdebench/repo/pdebench/data_gen/data_gen_NLE/BurgersEq/burgers_multi_solution_Hydra.py` — reference for the numerical scheme (upwind convective flux + central diffusion + multi-mode sinusoid IC family). License: NEC academic-use only (see header).
- `pdebench/venv/` — reused (already has `numpy<2`, `torch==2.2.2`, `h5py`, `jax==0.4.38`).

## What this Wave-4 run produced

- `evidence/1D_Burgers_Sols_Nu1e-2_small.hdf5` — 8 trajectories × 41 timesteps × 256 cells, 323 KB. PDEBench layout (`tensor` + `x-coordinate` + `t-coordinate`). MIT/CC-BY for the data (numpy-only generator, no NEC code touched).
- `evidence/burgers_results.json` — convergence table, conservation, timing.
- `figures/burgers_trajectory.png`, `figures/burgers_convergence.png`.

## License posture

- Our generator is a numpy re-statement of the published scheme; it does not link or include NEC-licensed code. The generated data is therefore unencumbered (MIT-compatible).
- The original PDEBench Burgers generator (`burgers_multi_solution_Hydra.py`) is NEC-academic-only; we did not redistribute it.

## Friction tags

- `:jax-pmap-cpu` — PDEBench's `burgers_multi_solution_Hydra.py` uses `jax.pmap` for multi-device sharding; on macOS CPU this requires `XLA_FLAGS=--xla_force_host_platform_device_count=N` and is awkward. We avoided this by re-implementing in numpy.
- `:nec-license-rider` — the BurgersEq generator file carries an NEC NC-academic header (~120 lines of license text at the top of the file). Worth flagging for downstream commercial users.
