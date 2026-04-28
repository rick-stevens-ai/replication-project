#!/bin/bash
source /opt/intel/oneapi/setvars.sh >/dev/null 2>&1
EXE=/home/stevens/software/PeleC-chiatta/Exec/Production/IgnitionKernel/PeleC3d.sycl.TPROF.MPI.ex
RUNS_DIR=/home/stevens/replicate-1559043/runs
LOG_DIR=/home/stevens/replicate-1559043/logs
mkdir -p $LOG_DIR

# Cap wall time per batch: use max_step=10000 (~50 min at 0.31s/step)
MAX_STEP=10000
STOP_TIME=1e-3

CONFIGS=(
  phi0.6_r0 phi0.6_r1 phi0.6_r2 phi0.6_r3 phi0.6_r4
  phi0.8_r0 phi0.8_r1 phi0.8_r2 phi0.8_r3 phi0.8_r4
  phi1.0_r0 phi1.0_r1 phi1.0_r2 phi1.0_r3 phi1.0_r4
  phi1.2_r0 phi1.2_r1 phi1.2_r2 phi1.2_r3 phi1.2_r4
)

BATCH_SIZE=8
for ((i=0; i<${#CONFIGS[@]}; i+=BATCH_SIZE)); do
  echo "=== Batch start $(date) idx=$i ==="
  PIDS=()
  for ((j=0; j<BATCH_SIZE && i+j<${#CONFIGS[@]}; j++)); do
    CFG=${CONFIGS[$i+$j]}
    GPU=$j
    (
      cd $RUNS_DIR/$CFG
      rm -rf chk0* plt0* Backtrace.* 2>/dev/null
      ZE_AFFINITY_MASK=$GPU ONEAPI_DEVICE_SELECTOR=level_zero:0 \
        mpirun -n 1 $EXE inputs.inp max_step=$MAX_STEP stop_time=$STOP_TIME amr.max_level=0 \
        > $LOG_DIR/${CFG}.log 2>&1
      echo "[$(date +%H:%M:%S)] $CFG done (exit=$?)"
    ) &
    PIDS+=($!)
  done
  echo "Batch running: ${CONFIGS[@]:$i:$BATCH_SIZE}"
  wait ${PIDS[@]}
  echo "=== Batch done $(date) ==="
done
echo "ENSEMBLE DONE $(date)"
