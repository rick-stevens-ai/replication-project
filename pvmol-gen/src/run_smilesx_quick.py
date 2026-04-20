"""
SMILES-X quick run — fits in 1-hour debug queue.
5 BayOpt rounds (not 25), skip geometry opt.
"""
import os, sys, logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'smilesx_lib'))

import numpy as np
import pandas as pd
import tensorflow as tf

logging.basicConfig(level=logging.INFO)

gpus = tf.config.list_physical_devices('GPU')
print(f'TensorFlow {tf.__version__}, GPUs detected: {len(gpus)}')

def run():
    from SMILESX.main import main as smilesx_main

    df = pd.read_csv('data/T0.csv')
    data_smiles = df[['smiles']]
    data_prop = df[['bin_class']]
    data_extra = df[['ha_num', 'o_num']].fillna(0)
    
    print(f'Data: {len(df)} molecules, {df["bin_class"].sum()} class 1')

    smilesx_main(
        data_smiles=data_smiles,
        data_prop=data_prop,
        data_extra=data_extra,
        data_name='pvmol_quick',
        outdir='./results/smilesx_quick',
        model_type='classification',
        scale_output=False,
        
        # Skip geometry opt — use paper defaults
        geomopt_mode='off',
        embed_ref=512,
        lstm_ref=128,
        tdense_ref=128,
        
        # Reduced BayOpt: 5 rounds fits in 1hr
        bayopt_mode='on',
        bs_bounds=[8, 16, 32, 64],
        lr_bounds=[2.0, 2.5, 3.0, 3.5, 4.0],
        bayopt_n_rounds=5,
        bayopt_n_epochs=30,
        bayopt_n_runs=3,
        
        # Training
        k_fold_number=5,
        n_runs=3,
        check_smiles=True,
        augmentation=True,
        patience=5,
        n_epochs=100,
        
        n_gpus=len(tf.config.list_physical_devices('GPU')) or 0,
        log_verbose=True,
        train_verbose=True,
    )

if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    run()
