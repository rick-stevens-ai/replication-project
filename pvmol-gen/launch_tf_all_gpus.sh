#!/bin/bash
# Launch TF SMILES-X across 8 A100 GPUs
# enriched_8feat: folds 0-4 on GPUs 0-4
# paper_2feat: folds 0-4 on GPUs 5-7 (3 at a time, then 2 more)

cd ~/pvmol-gen
source ~/env.sh 2>/dev/null
mkdir -p results/tf_logs

export LD_LIBRARY_PATH=/usr/lib/python3/dist-packages/tensorflow:$LD_LIBRARY_PATH
export TF_FORCE_GPU_ALLOW_GROWTH=true

echo "Launching TF SMILES-X parallel jobs at $(date)"

# enriched_8feat: 8 features, folds 0-4 on GPUs 0-4
for fold in 0 1 2 3 4; do
    gpu=$fold
    echo "GPU $gpu → enriched_8feat fold $fold"
    CUDA_VISIBLE_DEVICES=$gpu nohup python3 src/run_smilesx_enriched.py \
        --variant enriched_8feat --fold $fold \
        > results/tf_logs/enriched_8feat_fold${fold}_gpu${gpu}.log 2>&1 &
    echo "  PID: $!"
done

# paper_2feat: 2 features, folds 0-4 on GPUs 5-7 (first 3)
for fold in 0 1 2; do
    gpu=$((fold + 5))
    echo "GPU $gpu → paper_2feat fold $fold"
    CUDA_VISIBLE_DEVICES=$gpu nohup python3 src/run_smilesx_enriched.py \
        --variant paper_2feat --fold $fold \
        > results/tf_logs/paper_2feat_fold${fold}_gpu${gpu}.log 2>&1 &
    echo "  PID: $!"
done

echo ""
echo "8 jobs launched (5 enriched + 3 paper_2feat)."
echo "paper_2feat folds 3,4 will run after folds 0-2 finish on GPUs 5-7."
echo "Monitor: tail -f ~/pvmol-gen/results/tf_logs/*.log"
