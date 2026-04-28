# PeleC Ignition Kernel — Aurora (SYCL / Intel PVC) Port

Port status as of 2026-04-24 12:40 UTC.

## Status summary

| Phase | Status | Notes |
|---|---|---|
| 1. Build (SYCL)              | ✅ DONE | Binary: `/home/stevens/software/PeleC-aurora/Exec/Production/IgnitionKernel/PeleC3d.sycl.TPROF.MPI.ex` (115 MB) |
| 2. Verification run          | ✅ DONE | 1 node, 6 PVC GPUs, 117 steps, **T_max(t=0)=3298.05 K — matches uicgpu v2 baseline exactly** |
| 3. Ensemble submission       | ⚠ BLOCKED | Aurora queue policy currently prevents multi-case parallel submission (see below) |

## Build details

- Source: `https://github.com/AMReX-Combustion/PeleC.git` tag `v26.02` cloned to `~/software/PeleC-aurora`.
- Submodule commits (match uicgpu v2): AMReX `53dc0a47`, PelePhysics `ac521b3`, SUNDIALS `0eff3966`.
- Compiler: `icpx 2025.3.2`, `mpich/opt/5.0.0.aurora_test.3c70a61`, `cmake/3.31.11`.
- TPL: SUNDIALS built from PeleC submodule with `ENABLE_SYCL=ON`, installed to `.../PelePhysics/ThirdParty/INSTALL/sycl.SYCL/`.
- GNUmakefile flags used (`GNUmakefile.sycl` in this dir):
  `USE_CUDA=FALSE USE_SYCL=TRUE USE_MPI=TRUE Chemistry_Model=drm19 Eos_Model=Fuego USE_SUNDIALS=TRUE`.
- Build walltime: ~3 min (SUNDIALS TPL ~1 min, PeleC main ~2 min).

### Env setup one-liner
```bash
module load cmake/3.31.11   # only needed at build time for TPL
# everything else is Aurora default set:
# gcc/13.4.0 oneapi/release/2025.3.1 mpich/opt/5.0.0.aurora_test.3c70a61 libfabric/1.22.0 cray-pals/1.8.0 cray-libpals/1.8.0
```

## Required code change vs uicgpu v2

One line in `inputs.inp`:
```diff
- cvode.solve_type      = sparse_direct   # CUDA + KLU only
+ cvode.solve_type      = GMRES            # SYCL-compatible (iterative)
```
Everything else (prob.H/cpp/parm, Make.package, inputs) unchanged from v2_src/.

## Verification run (debug-scaling queue, job 8449552)

- 1 node, 6 MPI ranks, 6 SYCL devices (all 6 PVC GPUs, 1 rank/GPU via `gpu_tile_compact.sh`).
- Ran 500 steps → stopped at `stop_time=5e-6 s` (117 steps at adaptive dt).
- **T_max = 3298.05 K at t=0** — matches v2 baseline (3298 K ✓).
- Per-step cost after SYCL JIT warmup (~36 s STEP 1): **~0.064 s/step at max_level=0**.
- Clean finalize, no NaN, chemistry active (CVODE GMRES), 4 plot files + 1 chk produced.

See `runs/verify/run.log` for full log.

## Ensemble design (ready, not yet submitted to completion)

- 5 realizations × 4 φ values ∈ {0.6, 0.8, 1.0, 1.2} = **20 runs**.
- Realization perturbation: ±0.5 mm random jitter on kernel position (x0, z0). Deterministic seed from (`realization_idx`, `phi`). No code changes required.
- Per-run physics: `stop_time = 1 ms`, `max_level = 2`, AMR tags on `T > 1500 K` and `YOH > 1e-4`, checkpoint every 500 steps.
- Job script: `templates/pbs_ensemble.sh` — 1 node, `mpiexec -n 6 --ppn 6` with `gpu_tile_compact.sh` for device binding, auto-detects latest `chk?????` and restarts.
- Manifest (20 cases, kernel jitter, run dirs): `logs/ensemble_manifest_*.tsv`.
- All 20 run dirs staged on Aurora at `/lus/flare/projects/datascience_collab/stevens/replicate-1559043/runs/phi*_r*/`.

## 🚧 Queue blocker (as of 2026-04-24 12:40 UTC)

**Only 1 job of the 20-case ensemble (phi0.6_r0, jobid 8449560) could be queued.**

Aurora queue inspection (`qmgr -c "list queue ..."`):

| Queue           | max_run | max_queued / threshold | min nodes | max walltime | Enabled |
|-----------------|---------|------------------------|-----------|--------------|---------|
| `debug`         | 1       | 1 Q-state/user         | 1         | 1 h          | yes     |
| `debug-scaling` | 1       | 1 Q-state/user         | 1         | 1 h          | yes     |
| `tiny`          | —       | —                      | 1         | 6 h          | **NO**  |
| `backfill-tiny` | —       | —                      | 1         | 6 h          | **NO**  |
| `small`         | —       | 10/project             | **256**   | 12 h         | yes     |
| `medium`        | —       | 10/project             | **1025**  | 18 h         | yes     |
| `prod` (route)  | —       | —                      | 256       | —            | yes     |

So at single-node scale, the site currently enforces **≤1 queued + ≤1 running per user**, even for held dependency jobs (`qsub -W depend=afterany:X` still triggers "would exceed queue generic's per-user limit of jobs in 'Q' state" on submission).

### Options to unblock (suggested for next session)

1. **Ask ALCF support to re-enable `tiny` / `backfill-tiny`** — these are the normal 1-node multi-hour queues; their disabled status is presumably temporary.
2. **Request a reservation or different project**: `AuroraGPT` allocation (2.57 M node-hr) may route differently.
3. **Redesign ensemble for serial execution on `debug`**: reduce `stop_time` to what fits in 1 h wall (~0.1 ms) and serialize 20 cases via a resubmission daemon. Per-case wall estimate at AMR level 1: ~30–60 min, so each 1-hr `debug` job covers one case.
4. **Bundle cases into a large-queue job**: submit a `small`-queue job requesting 256 nodes, split into 20 simultaneous single-node sub-allocations via MPMD or a wrapper script. Burns 256 node-hrs per hour (plenty of budget, but wasteful).

Recommended next step: contact ALCF support about `tiny` availability before committing to option 3 or 4.

## Files in this bundle

```
aurora/
├── README.md                  # this file
├── GNUmakefile                # SYCL build (active)
├── GNUmakefile.sycl           # same, explicit name
├── Make.package
├── prob.H prob.cpp prob_parm.H  # from uicgpu v2_src, unchanged
├── inputs.inp                 # v2 inputs with only cvode.solve_type=GMRES change
├── templates/
│   ├── pbs_ensemble.sh        # canonical 1-node PBS job, chk-restart aware
│   └── inputs_overrides.template   # per-run (phi, kernel jitter) overrides
├── scripts/
│   ├── prep_ensemble.sh       # generate 20 run dirs (SUBMIT=yes to also qsub)
│   ├── chain_serial.sh        # chain 19 jobs after seed job via afterany deps
│   ├── chain_submit.sh        # per-phi parallel chain submission (not viable on current queues)
│   └── submit_ensemble.sh     # alt submission helper
├── runs/verify/               # verification job output (log, pbs, inputs, pbs stdout)
└── logs/                      # manifests
```

## On Aurora

- Repo: `/home/stevens/software/PeleC-aurora`
- Run scratch: `/lus/flare/projects/datascience_collab/stevens/replicate-1559043/`
  - `runs/verify/` — completed verification job (8449552)
  - `runs/phi*_r*/` — 20 staged but not submitted
  - `scripts/` — prep_ensemble.sh, chain_serial.sh, templates/
  - `logs/` — submission manifests
- Binary: `/home/stevens/software/PeleC-aurora/Exec/Production/IgnitionKernel/PeleC3d.sycl.TPROF.MPI.ex`
- Currently queued: job 8449560 (phi0.6_r0, 1 h debug-scaling).

## Allocation used this session

From `sbank l a -u stevens`: `datascience_collab` at 39,827 node-hrs available.
Charged so far this port: ~0.1 node-hr (one ~2 min verification job). Negligible.
