#!/bin/bash
source /opt/intel/oneapi/setvars.sh >/dev/null 2>&1
EXE=/home/stevens/software/PeleC-chiatta/Exec/Production/IgnitionKernel/PeleC3d.sycl.TPROF.MPI.ex
RUNS_DIR=/home/stevens/replicate-1559043/runs
LOG_DIR=/home/stevens/replicate-1559043/logs
mkdir -p $LOG_DIR

# 8 configs, 1 batch, ~55min wall
CONFIGS=(
  phi0.6_r0 phi0.6_r1
  phi0.8_r0 phi0.8_r1
  phi1.0_r0 phi1.0_r1
  phi1.2_r0 phi1.2_r1
)

echo "=== Batch start $(date) ==="
PIDS=()
for j in "${!CONFIGS[@]}"; do
  CFG=${CONFIGS[$j]}
  GPU=$j
  (
    cd $RUNS_DIR/$CFG
    rm -rf chk0* plt0* Backtrace.* 2>/dev/null
    ZE_AFFINITY_MASK=$GPU ONEAPI_DEVICE_SELECTOR=level_zero:0 \
      mpirun -n 1 $EXE inputs.inp \
        max_step=2000 stop_time=1e-3 amr.max_level=0 \
        pelec.chem_integrator=ReactorRK64 \
      > $LOG_DIR/${CFG}.log 2>&1
    echo "[$(date +%H:%M:%S)] $CFG done (exit=$?)"
  ) &
  PIDS+=($!)
done
echo "Batch running: ${CONFIGS[@]}"
wait ${PIDS[@]}
echo "=== Batch done $(date) ==="
echo "ENSEMBLE DONE"
