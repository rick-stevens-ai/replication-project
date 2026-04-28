# Polaris PeleC Ignition Kernel — STATUS

**Last update:** 2026-04-24 09:45 CDT (after retry subagent completion)

## Build ✅ COMPLETE
- Binary: `~/software/PeleC-polaris/Exec/Production/IgnitionKernel/PeleC3d.gnu.TPROF.MPI.CUDA.ex` (250 MB)
- Also staged: `/lus/eagle/projects/IMPROVE_Aim1/stevens/replicate-1559043/verify/PeleC3d.gnu.TPROF.MPI.CUDA.ex`
- Config: GNU + CUDA 12.9 + Cray MPICH 9.0.1, drm19 chem, Fuego EOS, SUNDIALS, AMREX_USE_EB, CUDA_ARCH=80
- **Gotcha fixed**: makefile's `-L.../cuda/12.9/math_libs/lib64` is wrong on Polaris. Libs actually live in `/opt/nvidia/hpc_sdk/Linux_x86_64/25.5/math_libs/12.9/targets/x86_64-linux/lib`. Fix: set `LIBRARY_PATH` (build) and `LD_LIBRARY_PATH` (runtime) to include that path. Captured in `build-polaris.sh`.
- Resume strategy that worked: kept prior `tmp_build_dir` objects (from mux-killed run) and re-ran `make` — only needed to redo link (~90 sec).

## Verify ✅ PASSED
- Job 7099640 (debug queue, 1 node, 4× A100)
- **T_max at t=0: 3298.05 K** (spec: 3298K — exact match)
- 117 steps to stop_time=5e-6, walltime ~18 sec → **6.4 steps/sec** per node
- dt settled near 6.5e-8 s, no NaN, 4 A100s active (40 GB each, ~1.5 GB used)
- Projected 1 ms run: ~15,400 steps × 0.155 s/step ≈ **40 min** per ensemble job

## Ensemble ✅ SUBMITTED (20 jobs)
- 5 realizations × 4 φ ∈ {0.6, 0.8, 1.0, 1.2}
- Jitter: `kernel_x0` ±0.4 mm, `turb_intensity` 0.08–0.12 (r=1..5 → −2,−1,0,+1,+2 × delta)
- Queue: `preemptable` (max 10 concurrent)
- Walltime per job: 2 h (actual ~40 min)
- Allocation: IMPROVE_Aim1 (95,895 node-hrs, cost ≈14 node-hrs)
- Job IDs: 7099651–7099670
- At submission: **2 R, 18 Q** — first results ETA ~45 min

## Files (Dropbox)
- `build-polaris.sh` — reproducible build (with CUDA math-lib fix)
- `pelec_verify.pbs` — debug-queue verify script
- `submit_ensemble.sh` — ensemble launcher (writes per-run inputs, PBS, submits 20)
- `prob.cpp`, `prob.H`, `prob_parm.H`, `inputs.inp` — v2 problem setup
- `STATUS.md` — this file

## Output locations (on Polaris)
- `/lus/eagle/projects/IMPROVE_Aim1/stevens/replicate-1559043/verify/` — verify run
- `/lus/eagle/projects/IMPROVE_Aim1/stevens/replicate-1559043/ensemble/runs/phiX_rY/` — ensemble
- `/lus/eagle/projects/IMPROVE_Aim1/stevens/replicate-1559043/ensemble/jobs/*.pbs` — scripts
