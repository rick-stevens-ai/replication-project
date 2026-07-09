# Brief — PDEBench Wave 4 (1D Burgers complementary replication)

**Paper:** Takamoto et al. *PDEBench: An Extensive Benchmark for Scientific Machine Learning.* NeurIPS 2022 D&B. [arXiv:2210.07182](https://arxiv.org/abs/2210.07182).
**Upstream code:** https://github.com/pdebench/PDEBench
**Wave:** PDE-collection Wave 4
**Date:** 2026-06-16

## Positioning

The existing `~/Dropbox/REPLICATE-PROJECT/PDE-replications/pdebench/REPORT.md` (2026-05-28) already covered:
- Artifact-openness check (MIT top-level + NEC sub-dir riders, DaRUS data DOIs).
- The 1D **Advection** data generator + sanity check vs analytic shift.
- The PDEBench `FNO1d` baseline trained for 40 epochs on a small Advection subset, beating a persistence baseline by ~2.85×.

This Wave-4 run is **complementary**: targets a *different* PDE from the same benchmark (**1D viscous Burgers**), focusing on the data-generation half and a self-convergence check.

## Chosen task

1. Generate a small PDEBench-layout Burgers dataset using the *same numerical scheme* as `data_gen_NLE/BurgersEq/burgers_multi_solution_Hydra.py` (upwind convective flux + central diffusion).
2. Verify the scheme is first-order accurate in Δx by self-convergence against an nx=1024 reference.
3. Verify mean conservation (periodic BCs, no source).
4. Write the result in PDEBench's HDF5 layout so it could be drop-in fed to PDEBench's own FNO training script.

## Pass criteria

- HDF5 in `(B, T, X)` layout with `x-coordinate` and `t-coordinate` datasets.
- Empirical convergence order ≥ 0.8 (theoretical 1.0 for upwind).
- Mean drift < 1e-6 (numerical zero on float32).

## Time budget

10–30 min.

## Compute

CherryRd CPU. Reuse the existing `pdebench/venv/`.
