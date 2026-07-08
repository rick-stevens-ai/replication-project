#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
source ~/env.sh 2>/dev/null
set -e
cd /data/stevens/sowfa_windfarm/windfarm-gnn/gnn_framework
source ../../.venv/bin/activate
# Use just 1 GPU
export CUDA_VISIBLE_DEVICES=0
echo "=== nvidia-smi pre ==="
nvidia-smi --query-gpu=index,name,memory.free --format=csv,noheader
echo "=== start training ==="
date
python -u train.py -c run_config.yml 2>&1
echo "=== done ==="
date
