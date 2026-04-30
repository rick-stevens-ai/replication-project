#!/bin/bash
set -e

# Source environment
source ~/env.sh 2>/dev/null || true

cd "$(dirname "$0")"

echo "========================================="
echo "  Space-CAMELS Emulator Pipeline"
echo "========================================="
echo ""

# Check/install dependencies
echo "--- Checking dependencies ---"
pip install camb scipy --quiet 2>&1 | tail -2
pip install torch matplotlib --quiet 2>&1 | tail -2
echo ""

# Step 1: Generate dataset
echo "========================================="
echo "  Step 1: Generate P(k) dataset with CAMB"
echo "========================================="
python replication/code/gen_dataset.py
echo ""

# Step 2: Train emulator
echo "========================================="
echo "  Step 2: Train MLP emulator"
echo "========================================="
python replication/code/train_emulator.py
echo ""

# Step 3: Evaluate
echo "========================================="
echo "  Step 3: Evaluate & generate plots"
echo "========================================="
python replication/code/eval.py
echo ""

echo "========================================="
echo "  PIPELINE COMPLETE"
echo "========================================="
echo ""
echo "Outputs:"
echo "  replication/data/     — Dataset files"
echo "  replication/figures/  — Diagnostic plots"
echo "  replication/results/  — Evaluation results"
