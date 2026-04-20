#!/bin/bash
#PBS -N ala_parallel
#PBS -l select=1:ngpus=4
#PBS -l walltime=02:00:00
#PBS -q preemptable
#PBS -A datascience
#PBS -l filesystems=home:eagle
#PBS -r y

# Single Polaris node: 4 A100 GPUs
# Run 8 chunks across 4 GPUs in parallel (2 chunks per GPU)
# ~1424 sims/chunk, should finish well within 2h

cd ~/projects/replicate-msm
source ~/miniforge3/bin/activate openmm-gpu
export OPENBLAS_NUM_THREADS=16
mkdir -p logs data/alanine_short

echo "=== Polaris Parallel Generation ==="
echo "Host: $(hostname) — $(date)"
echo "GPUs: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | wc -l)"

LOGFILE="logs/polaris_parallel_$(date +%Y%m%d_%H%M%S).log"
python src/alanine_dipeptide_parallel.py 8 2>&1 | tee "$LOGFILE" &
PID=$!
trap "kill -TERM $PID; wait $PID" SIGTERM SIGUSR1
wait $PID
echo "Finished at $(date)"
