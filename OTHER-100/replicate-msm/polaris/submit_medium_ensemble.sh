#!/bin/bash
#PBS -N ala_medium_ens
#PBS -l select=1:ngpus=4
#PBS -l walltime=04:00:00
#PBS -q preemptable
#PBS -A datascience
#PBS -l filesystems=home:eagle
#PBS -r y

# Medium ensemble: 5000 × 200 ps on 4× A100 (4 chunks, 1 per GPU)
# Checkpoint-restart safe. ~2-3h estimated.

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate

mkdir -p logs data/alanine_medium

echo "=== Medium Ensemble (200 ps × 5000) ==="
echo "Host: $(hostname)"
echo "Date: $(date)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null

LOGFILE="logs/medium_ens_$(date +%Y%m%d_%H%M%S).log"
python src/alanine_medium_ensemble.py 4 2>&1 | tee "$LOGFILE" &
PID=$!
trap "kill -TERM $PID; wait $PID; echo 'Preempted at $(date)' >> $LOGFILE" SIGTERM SIGUSR1
wait $PID
echo "Finished at $(date)"
