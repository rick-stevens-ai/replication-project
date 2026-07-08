#!/bin/bash
cd ~/projects/replicate-msm
source ~/projects/replicate/.venv/bin/activate
export OPENMM_CPU_THREADS=4
nohup python src/alanine_long_reference.py > logs/long_reference.log 2>&1 &
echo "PID: $!"
