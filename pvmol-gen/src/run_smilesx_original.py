"""
Run the original SMILES-X library on T0 data for binary classification.
Matches the paper's approach: extra features (ha_num, o_num), 
augmentation, geometry optimization, Bayesian optimization.
"""
import os
import sys
import logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Add SMILES-X lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'smilesx_lib'))

import numpy as np
import pandas as pd
import tensorflow as tf

logging.basicConfig(level=logging.INFO)

# Report GPU status
gpus = tf.config.list_physical_devices('GPU')
print(f"TensorFlow {tf.__version__}, GPUs detected: {len(gpus)}")
for g in gpus:
    print(f"  {g}")

def run():
    from SMILESX.main import main as smilesx_main

    # Load T0
    df = pd.read_csv('data/T0.csv')
    
    # Prepare inputs matching SMILES-X API
    data_smiles = df[['smiles']]  # DataFrame column
    data_prop = df[['bin_class']]  # Target: binary classification
    
    # Extra features: ha_num and o_num (as paper describes)
    data_extra = df[['ha_num', 'o_num']].fillna(0)
    
    print(f"Data: {len(df)} molecules, {df['bin_class'].sum()} class 1, {(1-df['bin_class']).sum()} class 0")
    print(f"Extra features: ha_num, o_num")
    print(f"Running SMILES-X with geometry opt + Bayesian opt...")

    # Run SMILES-X matching paper's configuration
    smilesx_main(
        data_smiles=data_smiles,
        data_prop=data_prop,
        data_extra=data_extra,
        data_name='pvmol_t0',
        data_units='',
        data_label='bin_class',
        outdir='./results/smilesx_original',
        
        # Model type
        model_type='classification',
        scale_output=False,  # No scaling for binary classification
        
        # Geometry optimization (zero-cost search for architecture)
        geomopt_mode='on',
        embed_bounds=[8, 16, 32, 64, 128, 256, 512, 1024],
        lstm_bounds=[8, 16, 32, 64, 128, 256, 512, 1024],
        tdense_bounds=[8, 16, 32, 64, 128, 256, 512, 1024],
        
        # Bayesian optimization for LR and batch size
        bayopt_mode='on',
        bs_bounds=[8, 16, 32, 64],
        lr_bounds=[2.0, 2.5, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0],
        bayopt_n_rounds=25,
        bayopt_n_epochs=30,
        bayopt_n_runs=3,
        
        # Defaults (in case geom opt doesn't run)
        embed_ref=512,
        lstm_ref=128,
        tdense_ref=128,
        bs_ref=16,
        lr_ref=3.9,
        
        # Training
        k_fold_number=5,
        n_runs=3,  # 3 runs per fold (paper SI)
        check_smiles=True,
        augmentation=True,  # Exhaustive atom rotation
        patience=5,
        n_epochs=100,
        ignore_first_epochs=0,
        
        # Hardware — auto-detect GPUs
        n_gpus=len(tf.config.list_physical_devices('GPU')) or 0,
        
        # Logging
        log_verbose=True,
        train_verbose=True,
    )

if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    run()
