# PROGRESS — Low-Rank Vlasov–Poisson Replication — **COMPLETE**

**Target paper:** L. Einkemmer & C. Lubich, "A Low-Rank Projector-Splitting Integrator for the Vlasov–Poisson Equation," SIAM J. Sci. Comput. 40(5), B1330–B1360 (2018). arXiv:1801.01103.

**Status:** completed 2026-05-28 (~75 minutes of subagent wall clock).

## Outcome
* Independent open reimplementation: full-grid baseline + KSL DLR integrator.
* Verified Landau damping rate γ ≈ 0.154 vs analytic 0.1533 (0.5% agreement).
* Two-stream instability captured by DLR for r ≥ 8 (linear+saturation) and r ≥ 16 (filamentation).
* Documented one known KSL non-robustness issue (over-rank instability) and mitigated with rank-adaptive Δt.
* Composite agreement score: **5/6 claims fully reproduced, 1 partial → 0.85**.

## Timeline (actual)
| t | what |
|---|------|
| 11:57 | scaffold, plan, openness check on arXiv |
| 12:00–12:15 | implemented `vp_common`, `vp_full`, `vp_lowrank` (KSL K/S/L) |
| 12:15 | smoke test exposed Poisson sign bug → fixed |
| 12:20 | Landau benchmark, 5/5 quantitative checks pass |
| 12:25–12:45 | two-stream benchmark; hit over-rank KSL blow-up at r=8 |
| 12:45 | stabilization (clip exp args, eigendecomp instead of per-x expm, sub-cycle S-step RK4); rank-adaptive Δt |
| 12:50 | full two-stream sweep r∈{4,8,16,32} |
| 12:55 | figures, report, README |

## Deliverables
* `REPORT.md` — full replication report (10k chars; claim table, friction tags, limitations).
* `README.md` — TL;DR + reproduction instructions.
* `code/` — 6 Python modules, all under 400 lines each.
* `figures/` — 5 PNG + 5 PDF figures.
* `results/` — JSON diagnostics + .npy phase-space snapshots.
* `logs/` — raw stdout from every run.

## Next steps (out of scope here)
* Strang-composed KSL benchmark.
* Implement BUG / Ceruti–Lubich (2022) robust variant.
* Extend to 2D2V with hierarchical low-rank to test the actual high-D speedup claim.
