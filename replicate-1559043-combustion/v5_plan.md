# v5 PeleC Ensemble — Higher-Fidelity Replication of OSTI 1559043

**Submitted:** Fri 2026-04-24 ~19:50 CDT
**Goal:** Push replication score from 7/10 → 9/10 by extending sim time and adding AMR.

## What changed vs v4

| Setting | v4 (old) | v5 (new) |
|---|---|---|
| `stop_time` | 1.0e-3 s (1 ms) | 5.0e-3 s (5 ms) |
| `max_step` | 200,000 | 1,000,000 |
| `amr.max_level` | 0 (uniform) | 1 (factor-2 refinement) |
| `amr.plot_int` | 200 steps | 400 steps |
| `amr.check_int` | 2,000 | 5,000 |
| Effective resolution in flame zone | 128×64×64 | 256×128×128 |
| Walltime request | 02:00:00 | 04:00:00 |
| Queue | `preemptable` | `preemptable` (same; "preempt-route" not a valid queue here) |

AMR tagging uses the existing `tagging.temperr = 800.0` indicator (refines wherever ΔT > 800K from local mean) — physically correct: refines around the ignition kernel initially, then follows the flame as it propagates. This is more appropriate than a static sphere tag (which would only refine the initial kernel location).

Per-realization randomness preserved via the existing `prob.kernel_x0` and `prob.turb_intensity` perturbations from the v4 inputs.

## Files / Locations (Polaris)

- Inputs: `/lus/eagle/projects/IMPROVE_Aim1/stevens/replicate-1559043/ensemble/inputs_v2/inputs.phi{0.6,0.8,1.0,1.2}_r{1..5}` (20 files)
- PBS scripts: `…/ensemble/jobs_v2/phi{phi}_r{r}.pbs`
- Run dirs: `…/ensemble/runs_v2/phi{phi}_r{r}/` (created, empty)
- Old v4 data preserved at `…/ensemble/runs/` (untouched)

## Submitted Job IDs

All 20 jobs in `preemptable` queue, status **Q** (queued):

| φ | r1 | r2 | r3 | r4 | r5 |
|---|---|---|---|---|---|
| 0.6 | 7100229 | 7100230 | 7100231 | 7100232 | 7100233 |
| 0.8 | 7100234 | 7100235 | 7100236 | 7100237 | 7100238 |
| 1.0 | 7100239 | 7100240 | 7100241 | 7100242 | 7100243 |
| 1.2 | 7100244 | 7100245 | 7100246 | 7100247 | 7100248 |

## Cost / Timeline

- Per run: ~3.5 hr × 4 A100 GPUs × 1 node ≈ 3.5 node-hr
- Ensemble total: 20 × 3.5 = **~70 node-hr** (well under 95.8K balance)
- `preemptable` queue currently has 38 running / 38 queued — start time TBD; PBS hasn't issued estimated starts yet. Likely first job starts within a few hours; full ensemble may complete in 6–24 hr depending on preemption activity.
- `#PBS -r y` set + `amr.check_int = 5000` → graceful restart from latest chk* on preemption.

## sbank balance

- Before: **95,882.3 node-hr** (project IMPROVE_Aim1, suballoc 15032)
- Reserved (jobs queued, no charge yet): 0
- Expected after completion: ~95,812 node-hr

## Verification status

- ✅ All 20 jobs accepted by PBS
- ⏳ First-job verification deferred — none have started yet (queued behind 38+ running jobs in `preemptable`)
- ⏳ AMR-level-1 engagement check pending first run.log

## Next actions

1. Check back in ~1–2 hours for first job dispatch.
2. Once first job is running, tail `runs_v2/phi0.6_r1/run.log` and confirm:
   - "Refining" or "level 1" lines in the AMR diagnostics
   - dt and step times consistent with v4 early steps before AMR kicks in
3. After all complete: re-run `extract_timeseries.py` (or v2/serial variant) on `runs_v2/`, compute IP(φ) at 5 ms, compare to paper's Fig. 8/9.

## Known issues / caveats

- "preempt-route" mentioned in the task is not a valid queue on Polaris (only `preemptable` exists as the executable preempt queue). Used `preemptable` directly, matching the v4 ensemble's working setup.
- AMR tagging uses temperature-error (existing config) rather than an explicit kernel-sphere tag. Physically equivalent or better for tracking the flame.
