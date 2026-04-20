#!/bin/bash
#PBS -N ala_dipeptide_gen
#PBS -l select=1
#PBS -l walltime=01:00:00
#PBS -q debug
#PBS -A datascience
#PBS -l filesystems=home
#PBS -r y

# Alanine dipeptide trajectory generation for MSM replication (Aurora)
# Nüske et al. 2017 — 11,388 trajectories × 20 ps
# Checkpoint-restart: saves every 200 sims, resumes on resubmit
# Aurora: Intel Data Center Max GPUs (PVC) — use OpenCL platform

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate
export OPENMM_DEFAULT_PLATFORM=OpenCL

mkdir -p logs data/alanine_short

echo "=== Aurora Alanine Dipeptide Generation ==="
echo "Host: $(hostname)"
echo "Date: $(date)"
echo "Python: $(python --version 2>&1)"
echo "Checkpoint: $(ls -la data/alanine_short/checkpoint.npz 2>/dev/null || echo 'none (fresh start)')"

# Forward SIGTERM to python process for clean checkpoint
LOGFILE="logs/ala_dipeptide_aurora_$(date +%Y%m%d_%H%M%S).log"
python src/alanine_dipeptide_gen.py 2>&1 | tee "$LOGFILE" &
PID=$!
trap "kill -TERM $PID; wait $PID; echo 'Preempted at $(date)' >> $LOGFILE" SIGTERM SIGUSR1
wait $PID
echo "Finished at $(date)"
