#!/usr/bin/env python
"""
Stage 1: SMILES-X Binary Classifier using the ORIGINAL TensorFlow/Keras library.

Uses components from smilesx_lib/SMILESX/ (Lambard & Gracheva, 2020) directly:
  - model.LSTMAttModel.create() for architecture
  - augm.augmentation() for exhaustive SMILES enumeration
  - token.get_tokens(), token.int_vec_encode() for tokenization

Runs 5-fold stratified CV on T0 data, with two hyperparameter configs:
  (A) Original defaults: embed=512, lstm=128, tdense=128
  (B) Reduced capacity:  embed=128, lstm=64,  tdense=64
"""

import os
import sys
import math
import json
import logging
import warnings
import datetime

# Suppress TF noise
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

# Add SMILESX library to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, 'smilesx_lib'))

import tensorflow as tf
tf.get_logger().setLevel('ERROR')

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import Callback
from tensorflow.keras import backend as K

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    f1_score, roc_auc_score, accuracy_score,
    precision_score, recall_score, classification_report
)

from SMILESX import model as smilesx_model
from SMILESX import augm as smilesx_augm
from SMILESX import token as smilesx_token

# ── Configuration ────────────────────────────────────────────
from config import (
    T0_FILE, RESULTS_DIR, PCE_THRESHOLD,
    CLASSIFICATION_THRESHOLD, CV_FOLDS
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Paper hyperparameters
LR_REF = 3.9       # Adam lr = 10^(-3.9) ≈ 1.26e-4
PATIENCE = 25
N_EPOCHS = 100
BATCH_SIZE = 16
N_RUNS = 1          # Single run per fold (paper doesn't mention multiple runs)
THRESHOLD = CLASSIFICATION_THRESHOLD  # 0.47

# Two hyperparameter configurations to compare
CONFIGS = {
    'original': {'embed': 512, 'lstm': 128, 'tdense': 128},
    'reduced':  {'embed': 128, 'lstm': 64,  'tdense': 64},
}


# ── Early Stopping Callback ─────────────────────────────────
class EarlyStopBest(Callback):
    """Save best weights based on val_loss with patience-based early stopping."""
    def __init__(self, patience=25):
        super().__init__()
        self.patience = patience
        self.best_loss = np.inf
        self.best_weights = None
        self.wait = 0
        self.stopped_epoch = 0
        self.best_epoch = 0

    def on_epoch_end(self, epoch, logs=None):
        val_loss = logs.get('val_loss')
        if val_loss is not None and val_loss < self.best_loss:
            self.best_loss = val_loss
            self.best_weights = self.model.get_weights()
            self.best_epoch = epoch
            self.wait = 0
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.stopped_epoch = epoch
                self.model.stop_training = True

    def on_train_end(self, logs=None):
        if self.best_weights is not None:
            self.model.set_weights(self.best_weights)


# ── Data Loading ─────────────────────────────────────────────
def load_t0_data():
    """Load T0 molecules (314 original), return SMILES array and binary labels."""
    df = pd.read_csv(T0_FILE)
    # Filter to T0_original only (314 molecules as in paper)
    if 'source' in df.columns:
        df = df[df['source'] == 'T0_original'].reset_index(drop=True)
    
    smiles = np.array(df['smiles'].tolist(), dtype=object)
    if 'bin_class' in df.columns:
        labels = df['bin_class'].astype(int).values
    else:
        labels = (df['delta_pce_norm'] >= PCE_THRESHOLD).astype(int).values
    
    logger.info(f"Loaded {len(smiles)} T0 molecules: "
                f"{labels.sum()} class 1, {(1-labels).sum()} class 0")
    return smiles, labels


# ── Augmentation Wrapper ─────────────────────────────────────
def augment_split(smiles_arr, labels_arr, indices, augment=True):
    """
    Use SMILESX augm.augmentation() to augment a split.
    Returns: (augmented_smiles_list, augmented_labels, clean_labels, cardinality_indices, clean_indices)
    
    Note: The original augm.augmentation has a bug with 1D data_prop 
    (uses .extend() on scalar). We pass 2D labels to work around it.
    """
    data_smiles_2d = np.array(smiles_arr).reshape(-1, 1)
    # Pass labels as 2D so data_prop[csmiles] is iterable (1-element array)
    data_prop = labels_arr.astype(float).reshape(-1, 1)
    
    result = smilesx_augm.augmentation(
        data_smiles=data_smiles_2d,
        indices=indices,
        data_extra=None,
        data_prop=data_prop,
        check_smiles=True,
        augment=augment
    )
    smiles_enum, extra_enum, prop_enum, prop_clean, card, indices_clean = result
    # Flatten prop arrays back to 1D
    if prop_enum is not None:
        prop_enum = prop_enum.ravel()
    if prop_clean is not None:
        prop_clean = prop_clean.ravel()
    return smiles_enum, prop_enum, prop_clean, card, indices_clean


# ── Single Fold Training ─────────────────────────────────────
def train_fold(config_name, config, fold_idx, 
               train_smiles, train_labels, train_indices,
               test_smiles, test_labels, test_indices,
               augmentation=True):
    """
    Train one fold using the original SMILESX architecture.
    Returns dict with metrics.
    """
    K.clear_session()
    
    embed_units = config['embed']
    lstm_units = config['lstm']
    tdense_units = config['tdense']
    
    logger.info(f"  [{config_name}] Fold {fold_idx}: augmenting training data...")
    
    # Augment train/test
    train_enum, train_prop_enum, train_prop_clean, train_card, train_idx_clean = \
        augment_split(train_smiles, train_labels, train_indices, augment=augmentation)
    test_enum, test_prop_enum, test_prop_clean, test_card, test_idx_clean = \
        augment_split(test_smiles, test_labels, test_indices, augment=augmentation)
    
    logger.info(f"  [{config_name}] Train: {len(train_smiles)} raw → {len(train_enum)} augmented")
    logger.info(f"  [{config_name}] Test:  {len(test_smiles)} raw → {len(test_enum)} augmented")
    
    # Tokenize
    train_tokens = smilesx_token.get_tokens(train_enum)
    test_tokens = smilesx_token.get_tokens(test_enum)
    all_tokens = train_tokens + test_tokens
    
    # Build vocabulary
    vocab = sorted(list(smilesx_token.extract_vocab(all_tokens)))
    vocab.insert(0, 'unk')
    vocab.insert(0, 'pad')
    
    max_length = max(len(t) for t in all_tokens)
    logger.info(f"  [{config_name}] Vocab size: {len(vocab)}, Max token length: {max_length}")
    
    # Encode to integer vectors
    x_train = smilesx_token.int_vec_encode(train_tokens, max_length + 1, vocab)
    x_test = smilesx_token.int_vec_encode(test_tokens, max_length + 1, vocab)
    y_train = np.array(train_prop_enum, dtype=np.float32)
    y_test = np.array(test_prop_enum, dtype=np.float32)
    
    # Split train into train/val (matching SMILESX internal 6:3 split within train_val)
    np.random.seed(42)
    n_train = int(len(x_train) * 0.8)
    perm = np.random.permutation(len(x_train))
    train_perm = perm[:n_train]
    val_perm = perm[n_train:]
    
    x_tr = x_train[train_perm]
    y_tr = y_train[train_perm]
    x_val = x_train[val_perm]
    y_val = y_train[val_perm]
    
    logger.info(f"  [{config_name}] Training: {len(x_tr)}, Validation: {len(x_val)}, Test: {len(x_test)}")
    
    # Create model with original SMILESX architecture
    strategy = tf.distribute.OneDeviceStrategy(device="/cpu:0")
    with strategy.scope():
        model_train = smilesx_model.LSTMAttModel.create(
            input_tokens=max_length + 1,
            vocab_size=len(vocab),
            embed_units=embed_units,
            lstm_units=lstm_units,
            tdense_units=tdense_units,
            dense_depth=0,
            extra_dim=None,
            model_type='classification'
        )
        custom_adam = Adam(learning_rate=math.pow(10, -LR_REF))
        model_train.compile(
            loss='binary_crossentropy',
            optimizer=custom_adam,
            metrics=['accuracy']
        )
    
    if fold_idx == 0:
        model_train.summary(print_fn=lambda x: logger.info(x))
    
    # Callbacks
    early_stop = EarlyStopBest(patience=PATIENCE)
    
    # Train
    history = model_train.fit(
        {"smiles": x_tr}, y_tr,
        validation_data=({"smiles": x_val}, y_val),
        epochs=N_EPOCHS,
        batch_size=BATCH_SIZE,
        shuffle=True,
        callbacks=[early_stop],
        verbose=0
    )
    
    best_epoch = early_stop.best_epoch + 1
    logger.info(f"  [{config_name}] Best epoch: {best_epoch}, Best val_loss: {early_stop.best_loss:.4f}")
    
    # Predict on test (augmented)
    y_pred_test = model_train.predict({"smiles": x_test}, verbose=0).ravel()
    
    # Average predictions over augmentations (per original molecule)
    from SMILESX.utils import mean_result
    y_pred_mean, y_pred_std = mean_result(test_card, y_pred_test)
    y_true = np.array(test_prop_clean, dtype=float)
    
    # Apply threshold
    y_pred_class = (y_pred_mean >= THRESHOLD).astype(int)
    y_true_int = y_true.astype(int)
    
    # Metrics
    f1 = f1_score(y_true_int, y_pred_class, zero_division=0)
    try:
        auc = roc_auc_score(y_true_int, y_pred_mean)
    except ValueError:
        auc = 0.0
    acc = accuracy_score(y_true_int, y_pred_class)
    prec = precision_score(y_true_int, y_pred_class, zero_division=0)
    rec = recall_score(y_true_int, y_pred_class, zero_division=0)
    
    logger.info(f"  [{config_name}] Fold {fold_idx}: F1={f1:.4f}, AUC={auc:.4f}, "
                f"Acc={acc:.4f}, Prec={prec:.4f}, Recall={rec:.4f}")
    
    return {
        'config': config_name,
        'fold': fold_idx,
        'f1': f1,
        'auc': auc,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'best_epoch': best_epoch,
        'n_train_augmented': len(train_enum),
        'n_test_augmented': len(test_enum),
    }


# ── Main Cross-Validation ───────────────────────────────────
def run_cv(config_name='original', augmentation=True):
    """Run 5-fold stratified CV with specified config."""
    smiles, labels = load_t0_data()
    
    config = CONFIGS[config_name]
    logger.info(f"\n{'='*60}")
    logger.info(f"Config: {config_name} — embed={config['embed']}, "
                f"lstm={config['lstm']}, tdense={config['tdense']}")
    logger.info(f"LR=10^(-{LR_REF}), batch={BATCH_SIZE}, patience={PATIENCE}, "
                f"threshold={THRESHOLD}, augmentation={augmentation}")
    logger.info(f"{'='*60}")
    
    skf = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=42)
    results = []
    
    for fold_idx, (train_idx, test_idx) in enumerate(skf.split(smiles, labels)):
        logger.info(f"\n─── Fold {fold_idx + 1}/{CV_FOLDS} ───")
        
        train_smiles = smiles[train_idx]
        train_labels = labels[train_idx]
        test_smiles = smiles[test_idx]
        test_labels = labels[test_idx]
        
        fold_result = train_fold(
            config_name=config_name,
            config=config,
            fold_idx=fold_idx,
            train_smiles=train_smiles,
            train_labels=train_labels,
            train_indices=train_idx,
            test_smiles=test_smiles,
            test_labels=test_labels,
            test_indices=test_idx,
            augmentation=augmentation
        )
        results.append(fold_result)
    
    # Summary
    f1s = [r['f1'] for r in results]
    aucs = [r['auc'] for r in results]
    accs = [r['accuracy'] for r in results]
    
    logger.info(f"\n{'='*60}")
    logger.info(f"CV Summary [{config_name}]:")
    logger.info(f"  F1:       {np.mean(f1s):.4f} ± {np.std(f1s):.4f}  (per fold: {[f'{x:.3f}' for x in f1s]})")
    logger.info(f"  AUC:      {np.mean(aucs):.4f} ± {np.std(aucs):.4f}  (per fold: {[f'{x:.3f}' for x in aucs]})")
    logger.info(f"  Accuracy: {np.mean(accs):.4f} ± {np.std(accs):.4f}")
    logger.info(f"{'='*60}")
    
    return results


def run_all_configs():
    """Run both original and reduced configs, save results."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    all_results = []
    for config_name in ['original', 'reduced']:
        results = run_cv(config_name=config_name, augmentation=True)
        all_results.extend(results)
    
    # Also run without augmentation for comparison
    for config_name in ['original', 'reduced']:
        results = run_cv(config_name=f"{config_name}_noaugm", augmentation=False)
        # Patch config name
        for r in results:
            r['config'] = f"{config_name}_noaugm"
        all_results.extend(results)
    
    # Save
    df = pd.DataFrame(all_results)
    outfile = RESULTS_DIR / "smilesx_original_cv_results.csv"
    df.to_csv(outfile, index=False)
    logger.info(f"\nResults saved to {outfile}")
    
    # Print summary table
    summary = df.groupby('config').agg(
        f1_mean=('f1', 'mean'), f1_std=('f1', 'std'),
        auc_mean=('auc', 'mean'), auc_std=('auc', 'std'),
        acc_mean=('accuracy', 'mean'), acc_std=('accuracy', 'std'),
    ).round(4)
    logger.info(f"\nSummary:\n{summary.to_string()}")
    
    return df


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SMILES-X Original TF Classifier")
    parser.add_argument('--config', choices=['original', 'reduced', 'all'], default='all',
                        help='Which config(s) to run')
    parser.add_argument('--no-augm', action='store_true', help='Disable augmentation')
    args = parser.parse_args()
    
    if args.config == 'all':
        run_all_configs()
    else:
        run_cv(config_name=args.config, augmentation=not args.no_augm)
