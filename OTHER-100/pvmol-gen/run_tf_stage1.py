#!/usr/bin/env python3
"""Run original TF SMILES-X for Stage 1 binary classification on T0 (314 molecules).

Matches the paper's setup:
  - 5-fold stratified CV
  - augmentation=True
  - model_type='classification'
  - embed=512, lstm=128, tdense=128
  - n_runs=3 per fold
  - scale_output=False (binary labels)
  - n_epochs=100, patience=25
"""

import sys
import os
import pandas as pd
import numpy as np

# Add SMILES-X lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'smilesx_lib'))

from SMILESX import main

# Load T0 dataset
data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'T0.csv'))
print(f"Loaded T0: {len(data)} molecules")
print(f"Class distribution: {data['bin_class'].value_counts().to_dict()}")

# Paper parameters
main.main(
    data_smiles=data[['smiles']],
    data_prop=data[['bin_class']],
    data_name='T0_classification',
    data_label='Effective (1/0)',
    outdir=os.path.join(os.path.dirname(__file__), 'outputs_tf'),
    model_type='classification',
    scale_output=False,
    augmentation=True,
    check_smiles=True,
    # Architecture (paper defaults)
    embed_ref=512,
    lstm_ref=128,
    tdense_ref=128,
    dense_depth=0,
    # Training
    bs_ref=16,
    lr_ref=3.9,  # 10^(-3.9) ≈ 1.26e-4
    n_epochs=100,
    patience=25,
    k_fold_number=5,
    n_runs=3,
    # No hyperparameter search
    geomopt_mode='off',
    bayopt_mode='off',
    train_mode='on',
    # GPU
    n_gpus=1,
    gpus_list=['0'],
    log_verbose=True,
    train_verbose=2,
)
