#!/usr/bin/env bash
# Single entrypoint for the OSTI 3003857 re-pass.
#
# Runs all four re-pass artifacts on CherryRd (free compute, CPU/MPS via
# Python 3.11 + PyTorch 2.2.2 + torchdiffeq + numpy + scipy + matplotlib).
#
# Total wall time: ~3-4 minutes on CherryRd (M3 + MPS).
#
# Outputs land in results/repass/{lorenz,ks,kolmogorov,era5}.

set -euo pipefail
cd "$(dirname "$0")"
export PYTHONUNBUFFERED=1
PY=/usr/local/bin/python3.11

echo "============================================================"
echo "OSTI 3003857 RE-PASS: Divide and Conquer (MP-NODE)"
echo "============================================================"
echo "Step 1/4: Lorenz-63 gradient explosion diagnostic"
$PY -u lorenz_gradients.py

echo "============================================================"
echo "Step 2/4: KS re-pass (paper Table 1 row 7 hyperparams: K=25, S=3, mu_min=1e-4)"
$PY -u ks_repass.py

echo "============================================================"
echo "Step 3/4: Kolmogorov agreement-gap diagnosis"
$PY -u kolmogorov_diagnosis.py

echo "============================================================"
echo "Step 4/4: ERA5 data-block diagnosis"
$PY -u era5_diagnosis.py

echo "============================================================"
echo "Done."
echo "Outputs: results/repass/{lorenz,ks,kolmogorov,era5}"
