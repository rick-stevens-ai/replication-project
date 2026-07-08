#!/bin/bash
source ~/env.sh
source ~/tf-gpu-env/bin/activate
export LD_LIBRARY_PATH=/home/stevens/tf-gpu-env/lib/python3.8/site-packages/nvidia/cudnn/lib:/home/stevens/tf-gpu-env/lib/python3.8/site-packages/nvidia/cublas/lib:$LD_LIBRARY_PATH
export TF_FORCE_GPU_ALLOW_GROWTH=true
export CUDA_VISIBLE_DEVICES=7

cd ~/pvmol-gen
echo "=== Starting enriched_8feat BayOpt on GPU 7 ==="
echo "Time: $(date)"
python src/run_smilesx_enriched.py --variant enriched_8feat 2>&1 | tee results/uicgpu_gpu7_enriched_8feat.log
echo "=== Finished at $(date) ==="
