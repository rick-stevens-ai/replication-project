#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "============================================="
echo "Replication: OSTI 3003857 - Divide and Conquer"
echo "Multi-Step Penalty Neural ODEs"
echo "============================================="

echo ""
echo "--- Step 1: Lorenz-63 Gradient & Loss Landscape Demo ---"
python3 lorenz_gradient_demo.py 2>&1 | tee log_lorenz_gradient.txt

echo ""
echo "--- Step 2: MP-NODE Lorenz-63 Training ---"
python3 mp_node_lorenz.py 2>&1 | tee log_lorenz_mpnode.txt

echo ""
echo "--- Step 3: MP-NODE Kuramoto-Sivashinsky ---"
python3 mp_node_ks.py 2>&1 | tee log_ks_mpnode.txt

echo ""
echo "============================================="
echo "All experiments complete!"
echo "============================================="
