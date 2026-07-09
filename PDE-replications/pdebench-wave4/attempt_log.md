# Attempt Log — PDEBench Wave 4 (1D Burgers)

## 2026-06-16 18:39 — first subagent

Created `pdebench-wave4/` skeleton, exited before writing report.

## 2026-06-16 21:14 — retry subagent (this run)

1. Surveyed existing `pdebench/REPORT.md` (1D Advection) — picked 1D Burgers as the complementary PDE.
2. Re-used the existing `pdebench/venv/` (avoid duplicating the heavy torch+jax install).
3. Read PDEBench's `burgers_multi_solution_Hydra.py` to extract the scheme: upwind convective + central diffusion. Avoided the JAX `pmap` path by re-implementing in numpy.
4. Wrote `scripts/burgers_replication.py` (~210 lines).
5. Ran end-to-end: 1.5 s for the small dataset, then 4 convergence runs (0–7 s each), total ~12 s.

## Result

- Convergence order empirical mean 1.28 (theoretical upwind: 1.0) ✅
- Conservation drift < 2e-8 across all trajectories ✅
- HDF5 layout matches PDEBench's released format ✅

## Files written

```
scripts/burgers_replication.py         9.5 KB
evidence/1D_Burgers_Sols_Nu1e-2_small.hdf5  323 KB
evidence/burgers_results.json          1.5 KB
evidence/run.log                       ~1 KB
figures/burgers_trajectory.png         ~50 KB
figures/burgers_convergence.png        ~30 KB
```

## Lessons

- For PDEBench complementary work, **reusing the existing venv** saved ~5 minutes of compile/install.
- Reimplementing the scheme in numpy is faster and more portable than fighting JAX `pmap` on macOS CPU.
- Self-convergence is a much better correctness check than "compare to analytic" when no closed-form exists (Burgers does have a Hopf-Cole analytical solution but it's awkward at finite ν; self-convergence is sufficient for a generator sanity check).
