#!/bin/bash
#PBS -N gpu_probe
#PBS -l select=1:ngpus=4
#PBS -l walltime=00:10:00
#PBS -q debug
#PBS -A datascience
#PBS -l filesystems=home:eagle

cd ~/projects/replicate-msm

# Use conda-forge OpenMM with CUDA support
source ~/miniforge3/bin/activate openmm-gpu
export OPENBLAS_NUM_THREADS=16

echo "=== HOST ==="
hostname
nvidia-smi -L

echo "=== OpenMM Platforms ==="
python -c "
import openmm as mm
print('Version:', mm.version.short_version)
print('Platforms:')
for i in range(mm.Platform.getNumPlatforms()):
    p = mm.Platform.getPlatform(i)
    print(f'  {p.getName()} (speed={p.getSpeed()})')
"

echo "=== GPU Detection Test ==="
python src/gpu_test.py
