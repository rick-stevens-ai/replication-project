#!/bin/bash
#PBS -N ala_parallel
#PBS -l select=1
#PBS -l walltime=02:00:00
#PBS -q capacity
#PBS -A datascience
#PBS -l filesystems=home
#PBS -r y

# Single Aurora node: 6 Intel PVC GPUs × 2 tiles = 12 OpenCL devices
# Run 8 chunks across GPUs in parallel within one job
# ~1424 sims/chunk, should finish well within 2h

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate
export OPENMM_DEFAULT_PLATFORM=OpenCL
mkdir -p logs data/alanine_short

echo "=== Aurora Parallel Generation ==="
echo "Host: $(hostname) — $(date)"

LOGFILE="logs/aurora_parallel_$(date +%Y%m%d_%H%M%S).log"
python src/alanine_dipeptide_parallel.py 8 2>&1 | tee "$LOGFILE" &
PID=$!
trap "kill -TERM $PID; wait $PID" SIGTERM SIGUSR1
wait $PID
echo "Finished at $(date)"
