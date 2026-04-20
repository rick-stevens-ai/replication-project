"""
Run SMILES-X on T0 data with enriched descriptors (8 features).

Two runs:
  (A) Paper baseline:  ha_num, o_num  (2 features)
  (B) Enriched:        ha_num, o_num, n_num, s_num, hbd_num, TPSA, MolLogP, NumRotatableBonds  (8 features)

Both use identical SMILES-X config: geometry opt + Bayesian opt, 
5-fold CV, 3 runs/fold, augmentation, classification.
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

# Shared SMILES-X parameters
SMILESX_PARAMS = dict(
    data_units='',
    data_label='bin_class',
    model_type='classification',
    scale_output=False,

    # Geometry optimization
    geomopt_mode='on',
    embed_bounds=[8, 16, 32, 64, 128, 256, 512, 1024],
    lstm_bounds=[8, 16, 32, 64, 128, 256, 512, 1024],
    tdense_bounds=[8, 16, 32, 64, 128, 256, 512, 1024],

    # Bayesian optimization
    bayopt_mode='on',
    bs_bounds=[8, 16, 32, 64],
    lr_bounds=[2.0, 2.5, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0],
    bayopt_n_rounds=25,
    bayopt_n_epochs=30,
    bayopt_n_runs=3,

    # Fallback defaults
    embed_ref=512,
    lstm_ref=128,
    tdense_ref=128,
    bs_ref=16,
    lr_ref=3.9,

    # Training
    k_fold_number=5,
    n_runs=3,
    check_smiles=True,
    augmentation=True,
    patience=5,
    n_epochs=100,
    ignore_first_epochs=0,

    # Hardware
    n_gpus=len(tf.config.list_physical_devices('GPU')) or 0,

    # Logging
    log_verbose=True,
    train_verbose=True,
)

# Feature sets to compare
FEATURE_SETS = {
    'paper_2feat': ['ha_num', 'o_num'],
    'enriched_8feat': ['ha_num', 'o_num', 'n_num', 's_num', 'hbd_num', 
                       'TPSA', 'MolLogP', 'NumRotatableBonds'],
}


def run(variant='enriched_8feat', fold_index=None):
    from SMILESX.main import main as smilesx_main

    # Load enriched T0
    df = pd.read_csv('data/T0_enriched.csv')
    
    # Drop the one bad SMILES (row with NaN descriptors)
    n_before = len(df)
    df = df.dropna(subset=['ha_num']).reset_index(drop=True)
    if len(df) < n_before:
        print(f"Dropped {n_before - len(df)} rows with NaN descriptors")

    features = FEATURE_SETS[variant]
    fold_str = f", folds={fold_index}" if fold_index is not None else ", folds=all"
    print(f"\n{'='*60}")
    print(f"Variant: {variant}")
    print(f"Features ({len(features)}): {features}{fold_str}")
    print(f"Data: {len(df)} molecules, {df['bin_class'].sum()} class 1, "
          f"{(1-df['bin_class']).sum()} class 0")
    print(f"{'='*60}\n")

    data_smiles = df[['smiles']]
    data_prop = df[['bin_class']]
    data_extra = df[features].fillna(0)

    # Dense depth: 2 for ≤4 features, 3 for more (more layers to learn interactions)
    dense_depth = 3 if len(features) > 4 else 2

    # Build params, adding k_fold_index if specific folds requested
    params = dict(SMILESX_PARAMS)
    if fold_index is not None:
        params['k_fold_index'] = fold_index

    smilesx_main(
        data_smiles=data_smiles,
        data_prop=data_prop,
        data_extra=data_extra,
        data_name=f'pvmol_{variant}',
        outdir=f'./results/smilesx_{variant}',
        dense_depth=dense_depth,
        **params,
    )


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--variant', choices=list(FEATURE_SETS.keys()) + ['both'],
                        default='both', help='Which feature set to run')
    parser.add_argument('--fold', type=int, nargs='+', default=None,
                        help='Specific fold(s) to run, e.g. --fold 1 2')
    parser.add_argument('--best-params', action='store_true',
                        help='Skip BayOpt/GeomOpt, use best known params')
    parser.add_argument('--bs', type=int, default=None, help='Override batch size')
    parser.add_argument('--lr', type=float, default=None, help='Override learning rate exponent')
    parser.add_argument('--embed', type=int, default=None, help='Override embed dim')
    parser.add_argument('--lstm', type=int, default=None, help='Override LSTM dim')
    parser.add_argument('--tdense', type=int, default=None, help='Override time-dense dim')
    args = parser.parse_args()

    os.chdir(os.path.join(os.path.dirname(__file__), '..'))

    # Apply best-params mode: skip expensive search, use fixed hyperparams
    if args.best_params:
        # Best from BayOpt: CherryRd fold 0 Trial #17 (val=0.9244)
        SMILESX_PARAMS['bayopt_mode'] = 'off'
        SMILESX_PARAMS['geomopt_mode'] = 'off'
        SMILESX_PARAMS['embed_ref'] = args.embed or 512
        SMILESX_PARAMS['lstm_ref'] = args.lstm or 64
        SMILESX_PARAMS['tdense_ref'] = args.tdense or 128
        SMILESX_PARAMS['bs_ref'] = args.bs or 64
        SMILESX_PARAMS['lr_ref'] = args.lr or 2.5
        print(f"Best-params mode: embed={SMILESX_PARAMS['embed_ref']}, "
              f"lstm={SMILESX_PARAMS['lstm_ref']}, tdense={SMILESX_PARAMS['tdense_ref']}, "
              f"bs={SMILESX_PARAMS['bs_ref']}, lr=10^-{SMILESX_PARAMS['lr_ref']}")
    else:
        # Allow individual overrides even in search mode
        if args.bs: SMILESX_PARAMS['bs_ref'] = args.bs
        if args.lr: SMILESX_PARAMS['lr_ref'] = args.lr
        if args.embed: SMILESX_PARAMS['embed_ref'] = args.embed
        if args.lstm: SMILESX_PARAMS['lstm_ref'] = args.lstm
        if args.tdense: SMILESX_PARAMS['tdense_ref'] = args.tdense

    if args.variant == 'both':
        for v in FEATURE_SETS:
            run(v, fold_index=args.fold)
    else:
        run(args.variant, fold_index=args.fold)
