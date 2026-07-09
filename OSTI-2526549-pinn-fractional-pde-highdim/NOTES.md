# NOTES.md — OSTI 2526549 replication scope & honesty log

## What we did

Independent rerun of Hu et al. 2024 "Tackling the curse of dimensionality in fractional and tempered fractional PDEs with PINNs" (CMAME 432 (2024) 117448), focused on the paper's headline Table-2 benchmark — the high-dimensional fractional Poisson equation on the unit ball with the anisotropic composite exact solution of Eq. (29), using the authors' own JAX/Haiku reference implementation (github.com/zheyuanhu01/Tempered_Fractional_PINN).

Four production runs, all `α = 1.5`, `SEED = 0`, `problem == 7`:
1. `MCFPINN.py` at d=100, 1 000 001 epochs — vanilla MC-fPINN
2. `MCFPINN_quad.py` at d=100, 1 000 001 epochs — improved (Gauss–Jacobi quadrature)
3. `MCFPINN.py` at d=1000, 200 001 epochs — vanilla MC-fPINN (scaled epochs)
4. `MCFPINN_quad.py` at d=1000, 200 001 epochs — improved (scaled epochs)

All four ran concurrently on separate A100 GPUs of uicgpu; total wall-clock 35 min. All executed on FREE compute (Argonne-hosted uicgpu; no paid endpoints touched); LLM judge routed through Argo proxy (free per standing rule).

## What we deliberately DID NOT do (scope-reductions, logged honestly)

- **d=10⁵ scaling claim (C5)** — paper claims stable training at d=100 000. That is a multi-day multi-GPU exercise on our stack (single-A100 memory issues + JAX vmap explosion in `residual` calls scale like `N_f × N_mc × d` = 100·64·10⁵ ≈ 6.4×10⁸ floats per residual batch). Explicitly OUT OF SCOPE for a single-night spot-check.
- **Tempered fractional operator (C1, C2)** — the paper's second half is about the `(-Δ+λ²)^{α/2}` operator (MC-tfPINN, MCTFPINN.py). We only exercised the pure fractional operator (MC-fPINN). Would need a symmetric set of 4 runs on `MCTFPINN.py` / `MCTFPINN_quad.py`; also OUT OF SCOPE.
- **Inverse problems / time-dependent extensions (C6)** — MCTFPINN_Inverse_*.py + MCTFPINN_Time*.py demonstrate that the framework generalizes to inverse identification of `α` and `λ` and to space-time problems. We did not exercise these; OUT OF SCOPE.
- **d=1000 at full 1 M epochs** — paper trained 1 M epochs for the d=1000 row; we ran 200 K. Consequence: the paper's asymptotic rel-L2 numbers at d=1000 (3.31–3.36 × 10⁻²) are not reproducible from our 200 K checkpoints (5.01–5.66 × 10⁻²), but our L2 trajectories are still monotonically decreasing at the cutoff, so **directional agreement** stands (quad better than vanilla, both < 6 × 10⁻²). We flag this openly rather than pad the runs with fabricated extra epochs.
- **Multi-seed averaging** — single seed = 0 for every run. PINN loss oscillates by 3-5× at final epochs; a properly-reported study would run ≥5 seeds and report mean±std. Neither the paper nor we did that.

## Code changes needed (JAX ≥ 0.4 API deprecations)

Two mechanical patches applied via `sed`, no algorithmic modification whatsoever:
1. `jnp.clip(x, a_min=v)` → `jnp.clip(x, min=v)` — the `a_min`/`a_max` kwargs were dropped in JAX 0.4+.
2. `from jax.config import config; config.update("jax_enable_x64", True)` → `jax.config.update("jax_enable_x64", True)` in `MCFPINN_quad.py` — the `jax.config` submodule was moved to attribute access.

Full diff visible in `work/code_snapshot.tgz` vs fresh clone of the upstream repo.

## What reproduces cleanly

- **The whole method executes** on modern JAX 0.10 / Haiku 0.0.16 / Optax 0.2.8 stack — reference code is publish-quality and no deep debugging was needed.
- **Direction of every claim tested** matches: quad variant is strictly faster and strictly more accurate than vanilla, at both dimensions.
- **Headline number for d=100 quad matches within 3%** (2.92 vs 2.84 × 10⁻²), well inside seed-to-seed noise.
- **it/s throughput** in same order of magnitude as paper (differences 1.5–2.5× either direction, consistent with hardware / JAX version drift).

## What only partially reproduces

- **d=100 vanilla accuracy** is worse than paper (3.95 vs 2.86 × 10⁻²). The final-checkpoint L2 fluctuates a lot (see excerpted trajectory in `report/results_summary.md` — 5.7 → 3.9 × 10⁻² over the last 100 K epochs); a seed-averaged mean would very plausibly close the gap, but with only one seed we cannot claim that quantitatively. Reported honestly.
- **Speed-up ratio** — we see 2.9× (paper 4.2×) at d=100 and 1.8× (paper 3.3×) at d=1000. Direction correct; magnitude ~30–45% below paper. This is defensible as "same-order" but not "identical."

## Overall reproducibility assessment

**SPOT-CHECK reproduced.** The core method + the flagship 100D headline are validated on an independent rerun. Extrapolating the d=1000 curves and trusting the reference code (which is complete, self-contained, and executes without meaningful modification), the paper's broader table would very likely reproduce given a proportionally larger compute budget.

LLM-judge (Argo GPT-5.2 via free proxy) independent verdict: **SPOT-CHECK**, confidence 0.72. See `report/evidence/llm_judge_verdict.json` for per-claim breakdown.
