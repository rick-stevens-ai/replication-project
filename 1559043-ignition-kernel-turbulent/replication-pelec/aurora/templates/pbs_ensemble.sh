#!/bin/bash -l
#PBS -N IK_PHI_REAL
#PBS -l select=1:ncpus=208
#PBS -l walltime=WALLTIME
#PBS -l filesystems=home:flare
#PBS -q preemptable
#PBS -A datascience_collab
#PBS -j oe
#PBS -o PBS_LOGDIR/IK_PHI_REAL.out
#
# PeleC ignition-kernel ensemble on Aurora (SYCL / PVC)
# Substituted at submit time: PHI, REAL (realization idx), WALLTIME, PBS_LOGDIR, SEED
#
# One Aurora node = 2x Intel Xeon Max + 6x Intel PVC GPUs (each 2 tiles = 12 SYCL devices)
# We use all 6 PVC GPUs, one MPI rank per GPU (6 ranks). Flat SYCL device per rank.

set -e
cd $PBS_O_WORKDIR
echo "=== Job $PBS_JOBID  node $(hostname)  start $(date) ==="

# Modules (Aurora default set is good; add MPI/compiler explicitly)
module load oneapi/release/2025.3.1 mpich/opt/5.0.0.aurora_test.3c70a61 2>/dev/null || true
module list 2>&1

EXE=__EXE_PATH__
INPUTS=inputs.inp

# Restart detection (preemptable: checkpoint-restart friendly)
LATEST_CHK=$(ls -d chk?????? 2>/dev/null | sort | tail -1 || true)
RESTART_ARG=""
if [ -n "$LATEST_CHK" ]; then
  echo "Restarting from $LATEST_CHK"
  RESTART_ARG="amr.restart=$LATEST_CHK"
fi

# SYCL device selection: let AMReX/PeleC pick devices; bind 1 rank per tile via GPU_TILE_COMPACT
# Use Aurora's standard helper; fallback to explicit ZE_AFFINITY_MASK if missing
NRANKS=6
NDEPTH=1
NPERHOST=6
GPU_SCRIPT=/soft/tools/mpi_wrapper_utils/gpu_tile_compact.sh

if [ -x "$GPU_SCRIPT" ]; then
  mpiexec -n $NRANKS --ppn $NPERHOST -d $NDEPTH --cpu-bind depth \
      $GPU_SCRIPT $EXE $INPUTS $RESTART_ARG 2>&1 | tee run.log
else
  echo "WARN: $GPU_SCRIPT not found; using ZE_AFFINITY_MASK round-robin"
  mpiexec -n $NRANKS --ppn $NPERHOST -d $NDEPTH --cpu-bind depth \
      bash -c 'export ZE_AFFINITY_MASK=$((PMI_LOCAL_RANK%6)); exec '"$EXE"' '"$INPUTS"' '"$RESTART_ARG"'' \
      2>&1 | tee run.log
fi

echo "=== Job $PBS_JOBID end $(date) ==="
