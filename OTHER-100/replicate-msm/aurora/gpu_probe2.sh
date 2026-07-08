#!/bin/bash
#PBS -N gpu_probe2
#PBS -l select=1
#PBS -l walltime=00:10:00
#PBS -q debug
#PBS -A datascience
#PBS -l filesystems=home

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate
export OPENMM_DEFAULT_PLATFORM=OpenCL

# Make sure Intel OpenCL ICD is findable
export OCL_ICD_VENDORS=/etc/OpenCL/vendors
export LD_LIBRARY_PATH="/usr/lib64:${LD_LIBRARY_PATH}"

echo "=== Checking OpenCL from Python ==="
python3 -c "
import ctypes, os

# Try loading OpenCL directly
try:
    lib = ctypes.CDLL('libOpenCL.so')
    print('libOpenCL.so loaded OK')
except:
    try:
        lib = ctypes.CDLL('libOpenCL.so.1')
        print('libOpenCL.so.1 loaded OK')
    except Exception as e:
        print(f'Cannot load libOpenCL: {e}')
"

echo "=== OpenMM test ==="
python3 src/gpu_test.py
