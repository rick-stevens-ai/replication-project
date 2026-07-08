#!/bin/bash
#PBS -N gpu_test
#PBS -l select=1:ngpus=4
#PBS -l walltime=00:10:00
#PBS -q debug
#PBS -A datascience
#PBS -l filesystems=home:eagle

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate

# Point OpenMM to the CUDA plugin directory
SITE_PKG=$(python -c "import openmm, os; print(os.path.dirname(os.path.dirname(openmm.__file__)))")
export OPENMM_PLUGIN_DIR="${SITE_PKG}/OpenMM.libs/lib/plugins"
echo "OPENMM_PLUGIN_DIR=$OPENMM_PLUGIN_DIR"
ls "$OPENMM_PLUGIN_DIR"/*CUDA* 2>/dev/null

python src/gpu_test.py
