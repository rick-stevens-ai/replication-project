#!/bin/bash
#PBS -N ala_dipeptide_gen
#PBS -l select=1:ngpus=1
#PBS -l walltime=02:00:00
#PBS -q preemptable
#PBS -A datascience
#PBS -l filesystems=home:eagle
#PBS -r y

# Alanine dipeptide trajectory generation for MSM replication (Polaris)
# Nüske et al. 2017 — 11,388 trajectories × 20 ps
# Checkpoint-restart: saves every 200 sims, resumes on resubmit

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate
export OPENBLAS_NUM_THREADS=16

mkdir -p logs data/alanine_short

echo "=== Polaris Alanine Dipeptide Generation ==="
echo "Host: $(hostname)"
echo "Date: $(date)"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'none')"
echo "Checkpoint: $(ls -la data/alanine_short/checkpoint.npz 2>/dev/null || echo 'none (fresh start)')"

# Forward SIGTERM to python process for clean checkpoint
LOGFILE="logs/ala_dipeptide_polaris_$(date +%Y%m%d_%H%M%S).log"
python src/alanine_dipeptide_gen.py 2>&1 | tee "$LOGFILE" &
PID=$!
trap "kill -TERM $PID; wait $PID; echo 'Preempted at $(date)' >> $LOGFILE" SIGTERM SIGUSR1
wait $PID
echo "Finished at $(date)"
