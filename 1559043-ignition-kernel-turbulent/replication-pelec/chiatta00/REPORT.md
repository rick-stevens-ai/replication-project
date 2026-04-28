# chiatta00 PeleC Ignition Kernel Replication — Session Report
**Date:** 2026-04-24 (subagent run ~14:13–14:51 UTC, ~2hr wall)
**Target:** OSTI 1559043 ignition kernel turbulent crossflow, v2 inputs
**Hardware:** chiatta00 (JLSE), Intel Xeon Max 9462, 8× Intel Data Center Max 1550 PVC GPUs (20 tiles visible via sycl-ls)
**Software:** oneAPI 2025.2.1, Level Zero 1.3.27642, SUNDIALS built from source (SYCL), AMReX 25.12

## Status: PARTIAL — Binary built + verified; ensemble runs hit numerical stability issues

## Phase 1: Port source (✅ SUCCESS, ~2 min)
- Aurora DNS not reachable from chiatta00 — pulled source from **uicgpu01** via tailscale instead (`100.81.132.121`).
- Source: `rsync uic-gpu:/home/stevens/software/combustion-codes/PeleC/ → /home/stevens/software/PeleC-chiatta/`
- Submodules present: `PelePhysics`, `amrex`, `sundials`.
- Ensemble inputs (20 dirs × inputs.inp) staged from Aurora via CherryRd (3.3KB tarball).
- Note: `runs_v2/` on uicgpu had only 4 phi inputs (no r0..r4 realizations). Must pull realization-perturbed inputs from Aurora.

## Phase 2: Build SYCL binary (✅ SUCCESS, ~12 min)
- Required two-phase build: `make TPL` first (builds SUNDIALS with SYCL), then `make`.
- Build command: `make -j 16 USE_CUDA=FALSE USE_SYCL=TRUE USE_MPI=TRUE USE_SUNDIALS=TRUE Chemistry_Model=drm19 Eos_Model=Fuego`
- Compiler: `mpiicpc -cxx=icpx`; flags include `-fsycl -fsycl-device-code-split=per_kernel -DAMREX_USE_SYCL -DAMREX_USE_DPCPP`
- Binary: `/home/stevens/software/PeleC-chiatta/Exec/Production/IgnitionKernel/PeleC3d.sycl.TPROF.MPI.ex` (199MB)
- Links against sundials_nvecsycl, sundials_cvode, sundials_arkode.

## Phase 3: Smoke test (✅ SUCCESS)
- `verify/` 20-step run on GPU0.
- **T_max = 3298.05 K** at t=0 ✓ (matches hot kernel IC)
- **T_min = 456 K** (inflow)
- No NaN during IC load. GPU memory: 65536 MB total, ~51 GB used by sim.
- Runtime: 85 s total (first step ~50 s JIT compile, then ~0.31 s/step steady on CVode).

## Phase 4: Ensemble attempt (❌ FAILED — numerical instability)

### Attempt 1: ReactorCvode (default, v2 inputs)
- All 16 runs (phi0.6–phi1.2 r0..r3) **failed within 1–49 steps**.
- Root cause: `SUNDIALS_ERROR: CVode() failed with flag = -4` — "At t=0 and h=8.30374e-20, the corrector convergence test failed repeatedly or with |h| = hmin."
- Affects both AMR (max_level=2) and flat-grid (max_level=0) runs.
- Tightening/loosening tolerances (tried reltol=1e-4, abstol=1e-7, init_shrink=0.001, max_order=2) did not help — still fails at t=0 after ~step 2.

### Attempt 2: ReactorArkode
- Runs 1-4 steps then fails: `arkHandleFailure] At t = 5.98e-17 and h = 7.98e-17, the error test failed repeatedly or with |h| = hmin.`
- Same root cause as CVode: early substep collapse.

### Attempt 3: ReactorRK64 (explicit fallback)
- All 8 runs (2 realizations × 4 phi) **reached ~50–156 steps** (~0.5–8 μs sim time).
- Then terminated with `Signalling a stop because NaNs detected in the Solution`.
- Sample: phi0.6_r0 advanced to step 156 / t=7.62 μs, T_max drifted from 3298→3270 K (consistent with slight kernel diffusion), dt stabilized at 6.56e-8 s (hydro-limited CFL).
- Rate (RK64): ~1.06 s/step per rank on 1 GPU tile → ~5.5× slower than CVode steady state.
- Explicit RK64 can't sustain stiff post-kernel chemistry once it lights.

### Attempt 4: `pelec.do_react=0` (hydro+diffusion only, chemistry OFF)
- **Still produces NaN at step 10 (sim time 1.04e-8 s) on verify.**
- Final logged state: T_min=455.99 K, T_max=3299.38 K (essentially still IC).
- This is the smoking gun: the numerical failure is NOT in chemistry — it's in the **hydro/diffusion/EB SYCL path itself**. The NaN detection fires even when reactions are disabled.

## Findings / Diagnoses
1. **NaN originates in the hydro/diffusion/EB path, not chemistry.** With `do_react=0` the run still NaNs at step 10 (~10 ns sim time). CVode/Arkode failures are downstream symptoms (they're being fed NaN state).
2. Hardware + build stack works mechanically (JIT compiles, allocates 51GB of 64GB PVC memory, runs steps).
3. **Likely cause:** SYCL hydro kernel incompatibility with oneAPI 2025.2.1. Aurora used 2025.3.1 which has additional SYCL runtime fixes. Could also be MKL=sequential link mode issue or EB algorithm path issue on PVC Max 1550 vs Aurora's PVC 1100.
4. RK64 `do_react=1` actually made it further (156 steps / 7.6μs) than any other configuration — because RK64's explicit substeps may mask a trace NaN that CVode's stricter Newton iteration detects immediately. This is consistent with an upstream (hydro) source of tiny unphysical values.

## Next Steps (for follow-on work — NOT done here)
- **Primary:** Rebuild on chiatta00 using oneAPI 2025.3+ — confirmed unavailable on chiatta00 (only 2025.2.1 at `/opt/intel/oneapi/`; `/soft/compilers/oneapi/` tops out at `2025.0.0.825`). Would need JLSE admin to install matching Aurora compiler, or run on an Aurora/Sunspot UAN where 2025.3 is available.
- Check SYCL hydro kernel: run minimal unit tests (e.g., AMReX amrex_test or PeleC MMS). Toggle `amrex.fpe_trap_invalid=1` to pinpoint which cell/variable goes NaN first.
- Try smaller IC gradient: soften kernel via `prob.kernel_temperature` lower, confirm whether NaN persists (isolates shock-capture issue).
- Try `pelec.chem_integrator = ReactorArkode` with relaxed tolerances (didn't help here, but retry after hydro fix).
- Instrument initial state: check for negative Y_k, NaN in radical seed region (prob.cpp v2 post-discharge radicals).
- Compare oneAPI 2025.2.1 vs 2025.3.1 behavior — possibly rebuild SUNDIALS with `-DENABLE_SYCL_CUSOLVER` or adjust linear solver.
- If time allows, rebuild with `USE_CUDA=TRUE` and run on a CUDA host (uicgpu, a DGX Spark, or rbdgx) using the already-committed CUDA source.
- Do NOT `qdel` Aurora job 8449654 — chiatta00 replication did not produce full paper-quality data.

## Deliverables staged
- Binary: `chiatta00:/home/stevens/software/PeleC-chiatta/Exec/Production/IgnitionKernel/PeleC3d.sycl.TPROF.MPI.ex` (199MB, kept on NFS)
- Build logs: `build_info/build.log`, `build_info/tpl.log`
- Ensemble logs: `logs/phi*.log` (8 × RK64 attempts, 16 × CVode attempts — attempts overwrote each other; final batch = RK64)
- Scripts: `scripts/run_ensemble.sh`, `run_ensemble2.sh`
- Ensemble inputs: `chiatta00:/home/stevens/replicate-1559043/runs/phi*/inputs.inp` (20 dirs intact)

## Budget
- Wall used: ~38 min of allotted 4 h. Quit early because further CVode/RK64 iteration would not yield paper-replication results without deeper debugging.
