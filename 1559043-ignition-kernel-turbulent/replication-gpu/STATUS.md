# GPU Replication Status - OSTI 1559043 Ignition Kernel

## Date: 2026-04-21

## Build Status: ✅ COMPLETE

### Executables Built
1. **GPU (MPI+CUDA SM80):** `PeleLMeX3d.gnu.TPROF.MPI.CUDA.ex` - 246MB
   - Location: `~/software/combustion-codes/PeleLMeX/Exec/Production/IgnitionKernel/`
   - DRM19 methane chemistry (21 species, 84 reactions)
   - CUDA arch SM 80 (A100)

2. **CPU (MPI-only):** `PeleLMeX3d.gnu.TPROF.MPI.ex`  
   - Same location, for testing/validation
   - Verified: initializes and runs correctly on CPU

### Custom Ignition Kernel Case
- Created in `Exec/Production/IgnitionKernel/`
- Problem files: `pelelmex_prob.H`, `pelelmex_prob.cpp`
- Input file: `ignition-kernel-3d.inp`
- Physics:
  - Hot kernel T=3300K, R=2mm (post-expansion from T1=5300K)
  - Crossflow at u=20 m/s, T=456K
  - Stratified: air below splitter (6.4mm), premixed CH4-air above
  - DRM19 mechanism with CVODE integrator
  - Domain: 32mm × 16mm × 16mm, dx=0.25mm (matching paper)

### Run Scripts
- `test_2gpu.sh` - Quick validation on 2 GPUs
- `run_ignition_study.sh` - Full 4-phi study on 8 GPUs
- Phi values: 0.6, 0.8, 1.0, 1.2

## BLOCKER: NVIDIA Driver Mismatch ❌

**Problem:** Kernel module version 570.153 ≠ Userspace library version 570.207

```
$ cat /sys/module/nvidia/version → 570.153.02
$ ls /usr/lib/x86_64-linux-gnu/libcuda.so.570.207
```

**Impact:** CUDA runtime crashes on initialization. `nvidia-smi` fails. GPU executables cannot run.

**Root Cause:** Driver packages were updated (apt) but the machine hasn't been rebooted in 182 days. The kernel module is stale.

**Fix Required:** Machine reboot (requires sudo/admin access)

## Next Steps (After Reboot)
1. Verify `nvidia-smi` shows 8× A100 GPUs
2. Run `test_2gpu.sh` to validate MPI+CUDA
3. Run `run_ignition_study.sh` for full study
4. Post-process results and write LaTeX report
