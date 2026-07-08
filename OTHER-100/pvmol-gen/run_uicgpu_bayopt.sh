#!/bin/bash
source ~/env.sh

# Use only GPU 0
export CUDA_VISIBLE_DEVICES=0

# cuDNN libs
export LD_LIBRARY_PATH=/usr/lib/python3/dist-packages/tensorflow:$LD_LIBRARY_PATH

# Limit TF memory growth
export TF_FORCE_GPU_ALLOW_GROWTH=true

cd ~/pvmol-gen

echo "=== Starting enriched_8feat BayOpt (all 5 folds) ==="
echo "GPU: $CUDA_VISIBLE_DEVICES"
echo "Time: $(date)"

python3 src/run_smilesx_enriched.py --variant enriched_8feat 2>&1 | tee results/uicgpu_enriched_8feat_bayopt_v2.log

echo "=== Finished at $(date) ==="
