#!/bin/bash
#PBS -N ala_long_ref
#PBS -l select=1:ngpus=4
#PBS -l walltime=06:00:00
#PBS -q preemptable
#PBS -A datascience
#PBS -l filesystems=home:eagle
#PBS -r y

# Long reference trajectories: 10 × 100 ns on 4× A100
# Checkpoint-restart safe. ~5h estimated (each A100 runs 2-3 trajs sequentially)

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate

mkdir -p logs data/alanine_long

echo "=== Long Reference Trajectories ==="
echo "Host: $(hostname)"
echo "Date: $(date)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null

LOGFILE="logs/long_ref_$(date +%Y%m%d_%H%M%S).log"
python src/alanine_long_reference.py 2>&1 | tee "$LOGFILE" &
PID=$!
trap "kill -TERM $PID; wait $PID; echo 'Preempted at $(date)' >> $LOGFILE" SIGTERM SIGUSR1
wait $PID
echo "Finished at $(date)"
