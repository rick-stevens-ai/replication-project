#!/bin/bash
# Launch parallel BayOpt folds across 8 A100 GPUs
# GPU 0-4: enriched_8feat folds 0-4
# GPU 5-6: paper_2feat folds 0-1 (remaining folds queued after)

cd ~/pvmol-gen
mkdir -p results/logs

export TF_CPP_MIN_LOG_LEVEL=2

echo "Launching 8 parallel jobs at $(date)"

# enriched_8feat: folds 0-4 on GPUs 0-4
for fold in 0 1 2 3 4; do
    echo "GPU $fold → enriched_8feat fold $fold"
    CUDA_VISIBLE_DEVICES=$fold nohup python3 src/run_smilesx_enriched.py         --variant enriched_8feat --fold $fold         > results/logs/enriched_8feat_fold${fold}_gpu${fold}.log 2>&1 &
    echo "  PID: $!"
done

# paper_2feat: folds 0-4 on GPUs 5-7 (first 3), then 5-6 get folds 3-4 after
# Actually let's run folds 0-2 on GPUs 5-7, then queue 3-4
for i in 0 1 2; do
    gpu=$((i + 5))
    echo "GPU $gpu → paper_2feat fold $i"
    CUDA_VISIBLE_DEVICES=$gpu nohup python3 src/run_smilesx_enriched.py         --variant paper_2feat --fold $i         > results/logs/paper_2feat_fold${i}_gpu${gpu}.log 2>&1 &
    echo "  PID: $!"
done

echo ""
echo "8 jobs launched. Remaining paper_2feat folds 3-4 will need to be launched"
echo "when GPUs 5-7 finish their first folds."
echo ""
echo "Monitor with: tail -f ~/pvmol-gen/results/logs/*.log"
echo "Check progress: grep -r 'Trial.*average best' ~/pvmol-gen/results/logs/"
