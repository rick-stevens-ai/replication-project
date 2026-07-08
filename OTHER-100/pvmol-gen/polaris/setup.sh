#!/bin/bash
# PVMol-Gen Polaris Setup
# Run this once after rsync'ing the project to Polaris
# Usage: bash ~/pvmol-gen/polaris/setup.sh

set -e

echo "=== PVMol-Gen Polaris Setup ==="

# Load ALCF conda environment (has PyTorch + CUDA pre-built for A100)
module load conda
conda activate base

# Install additional dependencies into user site-packages
pip install --user rdkit-pypi pubchempy transformers datasets scikit-learn seaborn tqdm

echo ""
echo "=== Verifying installation ==="
python -c "
import torch
print(f'PyTorch: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU count: {torch.cuda.device_count()}')
    for i in range(torch.cuda.device_count()):
        print(f'  GPU {i}: {torch.cuda.get_device_name(i)}')
import transformers; print(f'Transformers: {transformers.__version__}')
import rdkit; print(f'RDKit: {rdkit.__version__}')
import sklearn; print(f'Scikit-learn: {sklearn.__version__}')
print('All dependencies OK!')
"

echo ""
echo "=== Setup complete ==="
echo "Submit test job:  qsub ~/pvmol-gen/polaris/test_stage1.pbs"
