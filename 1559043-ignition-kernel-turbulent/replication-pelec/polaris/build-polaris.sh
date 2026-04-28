#!/bin/bash
# Build PeleC IgnitionKernel for Polaris (A100, CUDA 12.9)
# Run from Polaris login node; ALWAYS wrap in tmux if running long.
set -e
module swap PrgEnv-nvidia PrgEnv-gnu 2>/dev/null || true
module load cuda/12.9 2>/dev/null || true
module load craype-accel-nvidia80 2>/dev/null || true
export PATH=$HOME/.local/bin:$PATH

# CRITICAL: CUDA math libs (curand/cusparse/cusolver) live here on Polaris,
# NOT under cuda/12.9/math_libs/lib64 where the makefile expects. Without this
# fix the link step fails with "cannot find -lcurand".
CUDA_MATH_LIB=/opt/nvidia/hpc_sdk/Linux_x86_64/25.5/math_libs/12.9/targets/x86_64-linux/lib
export LIBRARY_PATH=$CUDA_MATH_LIB:$LIBRARY_PATH
export LD_LIBRARY_PATH=$CUDA_MATH_LIB:$LD_LIBRARY_PATH

cd ~/software/PeleC-polaris/Exec/Production/IgnitionKernel

echo "=== make realclean ==="
make realclean 2>&1 | tail -5

echo "=== make -j 8 (full) ==="
make -j 8 USE_CUDA=TRUE USE_MPI=TRUE Chemistry_Model=drm19 Eos_Model=Fuego CUDA_ARCH=80
rc=$?
echo "=== ls *.ex ==="
ls -la *.ex
echo "EXIT:$rc"
