"""
Run SMILES-X with best hyperparams from Bayesian opt (bs=16, lr=3.5).
Skip bayopt, skip geomopt. Just full 5-fold CV × 3 runs.
"""
import os
import sys
import logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'smilesx_lib'))

import numpy as np
import pandas as pd
import tensorflow as tf

logging.basicConfig(level=logging.INFO)

gpus = tf.config.list_physical_devices('GPU')
print(f"TensorFlow {tf.__version__}, GPUs detected: {len(gpus)}")
for g in gpus:
    print(f"  {g}")

def run():
    from SMILESX.main import main as smilesx_main

    df = pd.read_csv('data/T0.csv')
    data_smiles = df[['smiles']]
    data_prop = df[['bin_class']]
    data_extra = df[['ha_num', 'o_num']].fillna(0)

    print(f"Data: {len(df)} molecules, {int(df['bin_class'].sum())} class 1, {int((1-df['bin_class']).sum())} class 0")
    print(f"Using BEST hyperparams from Bayesian opt: bs=16, lr=3.5")
    print(f"Skipping geomopt and bayopt — going straight to 5-fold CV × 3 runs")

    smilesx_main(
        data_smiles=data_smiles,
        data_prop=data_prop,
        data_extra=data_extra,
        data_name='pvmol_passivation',
        data_units='',
        data_label='bin_class',
        outdir='./results/smilesx_bestparams',

        model_type='classification',
        scale_output=False,

        # Skip geometry and Bayesian optimization
        geomopt_mode='off',
        bayopt_mode='off',

        # Best params from trial #0 (val_score=0.7781)
        bs_ref=16,
        lr_ref=3.5,

        # Use defaults for architecture (from geomopt earlier runs)
        embed_ref=512,
        lstm_ref=128,
        tdense_ref=128,

        # Full training
        k_fold_number=5,
        n_runs=3,
        check_smiles=True,
        augmentation=True,
        patience=5,
        n_epochs=100,
        ignore_first_epochs=0,

        n_gpus=len(tf.config.list_physical_devices('GPU')) or 0,
        log_verbose=True,
        train_verbose=True,
    )

if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    run()
