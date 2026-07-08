#!/bin/bash
source ~/env.sh
export CUDA_VISIBLE_DEVICES=-1
export TF_CPP_MIN_LOG_LEVEL=2
cd ~/pvmol-gen

echo "=== CPU-only BayOpt: enriched_8feat fold 0 ==="
echo "Time: $(date)"

python3 src/run_smilesx_enriched.py --variant enriched_8feat --fold 0 2>&1

echo "=== Finished at $(date) ==="
