#!/usr/bin/env python3
"""
Run original SMILES-X (TF/Keras) on Polaris/Aurora for classification.
Bypasses bayopt import by calling main() with bayopt_mode='off'.

This uses the ACTUAL original library — not our PyTorch reimplementation.
The paper used: embed=512, lstm=128, tdense=128, lr=3.9, bs=16, patience=25,
augmentation=True, k_fold=5, n_runs=3, model_type='classification'.
"""
import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Patch: make optuna importable as a no-op so bayopt.py doesn't crash
# We won't actually use Bayesian optimization
import types
optuna_mock = types.ModuleType('optuna')
optuna_mock.samplers = types.ModuleType('optuna.samplers')
optuna_mock.samplers.TPESampler = type('TPESampler', (), {})
sys.modules['optuna'] = optuna_mock
sys.modules['optuna.samplers'] = optuna_mock.samplers

# Add SMILES-X library to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, 'smilesx_lib'))

import numpy as np
import pandas as pd
from pathlib import Path

print("Loading SMILES-X original library...")
from SMILESX.main import main as smilesx_main

# ─── Load T0 data ─────────────────────────────
DATA_DIR = Path(PROJECT_DIR) / 'data'
T0_FILE = DATA_DIR / 'T0.csv'

print(f"Loading data from {T0_FILE}")
df = pd.read_csv(T0_FILE)
print(f"Columns: {list(df.columns)}")
print(f"Shape: {df.shape}")
print(df.head(3))

# Find SMILES column
smi_col = [c for c in df.columns if 'smiles' in c.lower()][0]
# Find class/label column
label_col = None
for c in df.columns:
    cl = c.lower()
    if 'class' in cl or 'bin' in cl:
        label_col = c
        break

if label_col is None:
    # Try delta_pce_norm
    pce_col = [c for c in df.columns if 'pce' in c.lower() or 'delta' in c.lower() or 'norm' in c.lower()]
    if pce_col:
        df['bin_class'] = (df[pce_col[0]] >= 0.10).astype(int)
        label_col = 'bin_class'
    else:
        raise ValueError(f"Cannot find label column in {list(df.columns)}")

print(f"SMILES column: {smi_col}")
print(f"Label column: {label_col}")
print(f"Class distribution: {df[label_col].value_counts().to_dict()}")

# Check for extra features (ha_num, o_num) as used in paper
extra_cols = []
for ec in ['ha_num', 'o_num']:
    if ec in df.columns:
        extra_cols.append(ec)

has_extra = len(extra_cols) > 0
print(f"Extra features: {extra_cols if has_extra else 'none'}")

# ─── Configure output directory ───────────────
outdir = os.path.join(PROJECT_DIR, 'results', 'smilesx_original')
os.makedirs(outdir, exist_ok=True)

# ─── Run SMILES-X original ────────────────────
print("\n" + "="*60)
print("Running SMILES-X original classification (5-fold CV)")
print("="*60)
print(f"Hyperparameters (paper defaults):")
print(f"  embed_ref=512, lstm_ref=128, tdense_ref=128")
print(f"  lr_ref=3.9 (Adam lr=10^-3.9 ≈ 1.26e-4)")
print(f"  batch_size=16, patience=25, n_epochs=100")
print(f"  augmentation=True, n_runs=3")
print(f"  bayopt_mode=off, geomopt_mode=off")
print(f"  model_type=classification, scale_output=False")
print()

smilesx_main(
    data_smiles=df[[smi_col]],
    data_prop=df[label_col],
    data_extra=df[extra_cols] if has_extra else None,
    data_name='pvmol_passivation',
    data_units='',
    data_label='class',
    outdir=outdir,
    model_type='classification',
    scale_output=False,
    # Paper hyperparameters
    embed_ref=512,
    lstm_ref=128,
    tdense_ref=128,
    dense_depth=0,
    bs_ref=16,
    lr_ref=3.9,
    # CV settings
    k_fold_number=5,
    n_runs=3,
    # Augmentation (key for small datasets!)
    augmentation=True,
    check_smiles=True,
    # Training
    n_epochs=100,
    patience=25,
    # No hyperparameter optimization — use paper defaults
    bayopt_mode='off',
    geomopt_mode='off',
    # Verbose
    log_verbose=True,
    train_verbose=0,
)

print("\n" + "="*60)
print("SMILES-X classification complete!")
print(f"Results in: {outdir}")
print("="*60)
