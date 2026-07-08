#!/bin/bash
# Repass: Reference model inference on Test-EM (54 cases).
# Same CLI as the pass-1 Selected run, only --ckpt changes and --outdir.
set -e

PYTHON=/data/stevens/CAMELS/.venv/bin/python
CODE_DIR=/data/stevens/tsunami/code
DATA_DIR=/data/stevens/tsunami/data/Test-EM
RESULTS_DIR=/data/stevens/tsunami/results_reference
WEIGHTS=$CODE_DIR/weights/Reference_8L_cont05_dc100.pt
SPLIT_LIST=$CODE_DIR/splits/split_testEM_case6_onlyM4.txt

echo "[$(date)] Starting F-FNO Reference inference on Test-EM (54 scenarios)..."
echo "PyTorch: $($PYTHON -c 'import torch; print(torch.__version__, torch.cuda.is_available())')"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)"

mkdir -p $RESULTS_DIR

START_TIME=$(date +%s)

$PYTHON $CODE_DIR/inference.py \
    --ckpt $WEIGHTS \
    --test_list_txt $SPLIT_LIST \
    --data_root $DATA_DIR \
    --outdir $RESULTS_DIR \
    --device cuda \
    --amp \
    --seq_len 10 \
    --horizon 200 \
    --make_fig1_all_buoys \
    --fig1_aggregated \
    --buoy_mode fixed \
    --buoy_epicenters "40.9,138.9;40.2,138.7;39.0,138.0;38.3,137.7" \
    --buoy_target_lat 37.1 \
    --buoy_target_lon 129.39 \
    --buoy_fixed_dists_km 80 160 240 320 400 480 560 640 720

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
echo "[$(date)] Reference inference complete! Elapsed: ${ELAPSED}s"
echo "ELAPSED_SECONDS=$ELAPSED" > $RESULTS_DIR/timing.txt
