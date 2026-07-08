#!/usr/bin/env python
"""
Run 5-fold CV with original TF SMILESX model.
Designed to run as a background job with output saved to file.
Runs both 'original' (512/128/128) and 'reduced' (128/64/64) configs.
"""

import os
import sys
import math
import time
import json
import warnings
import logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, 'smilesx_lib'))

import numpy as np
import pandas as pd

import tensorflow as tf
tf.get_logger().setLevel('ERROR')
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score, precision_score, recall_score

from SMILESX import model as smilesx_model
from SMILESX import augm as smilesx_augm
from SMILESX import token as smilesx_token
from SMILESX.utils import mean_result

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(PROJECT_DIR, 'results', 'tf_cv_run.log'))
    ]
)
logger = logging.getLogger(__name__)

# ── Config ───────────────────────────────────────────────────
PCE_THRESHOLD = 0.10
THRESHOLD = 0.47
CV_FOLDS = 5
SEED = 42
LR = math.pow(10, -3.9)  # ~1.26e-4
PATIENCE = 25
N_EPOCHS = 100
BATCH_SIZE = 16

CONFIGS = {
    'original': {'embed': 512, 'lstm': 128, 'tdense': 128},
    'reduced':  {'embed': 128, 'lstm': 64,  'tdense': 64},
}


class EarlyStopBest(tf.keras.callbacks.Callback):
    def __init__(self, patience=25):
        super().__init__()
        self.patience = patience
        self.best_loss = np.inf
        self.best_weights = None
        self.wait = 0
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
                self.model.stop_training = True

    def on_train_end(self, logs=None):
        if self.best_weights is not None:
            self.model.set_weights(self.best_weights)


def load_t0():
    t0_file = os.path.join(PROJECT_DIR, 'data', 't0_molecules.csv')
    df = pd.read_csv(t0_file)
    if 'source' in df.columns:
        df = df[df['source'] == 'T0_original'].reset_index(drop=True)
    smiles = np.array(df['smiles'].tolist(), dtype=object)
    if 'bin_class' in df.columns:
        labels = df['bin_class'].astype(int).values
    else:
        labels = (df['delta_pce_norm'] >= PCE_THRESHOLD).astype(int).values
    return smiles, labels


def augment_data(smiles_arr, labels_arr, indices, augment=True):
    data_smiles_2d = np.array(smiles_arr).reshape(-1, 1)
    data_prop = labels_arr.astype(float).reshape(-1, 1)
    result = smilesx_augm.augmentation(data_smiles_2d, indices, None, data_prop, True, augment)
    smiles_enum, _, prop_enum, prop_clean, card, idx_clean = result
    if prop_enum is not None:
        prop_enum = prop_enum.ravel()
    if prop_clean is not None:
        prop_clean = prop_clean.ravel()
    return smiles_enum, prop_enum, prop_clean, card


def run_fold(config_name, config, fold_idx, 
             train_smi, train_lab, train_idx, 
             test_smi, test_lab, test_idx):
    K.clear_session()
    
    embed = config['embed']
    lstm = config['lstm']
    tdense = config['tdense']
    
    t0 = time.time()
    
    # Augment
    train_enum, train_prop, train_clean, train_card = augment_data(
        train_smi, train_lab, train_idx, augment=True)
    test_enum, test_prop, test_clean, test_card = augment_data(
        test_smi, test_lab, test_idx, augment=True)
    
    logger.info(f"  [{config_name}] Fold {fold_idx}: {len(train_smi)}→{len(train_enum)} train, "
                f"{len(test_smi)}→{len(test_enum)} test")
    
    # Tokenize
    train_tokens = smilesx_token.get_tokens(train_enum)
    test_tokens = smilesx_token.get_tokens(test_enum)
    all_tokens = train_tokens + test_tokens
    vocab = sorted(list(smilesx_token.extract_vocab(all_tokens)))
    vocab.insert(0, 'unk')
    vocab.insert(0, 'pad')
    max_length = max(len(t) for t in all_tokens)
    
    x_train = smilesx_token.int_vec_encode(train_tokens, max_length + 1, vocab)
    x_test = smilesx_token.int_vec_encode(test_tokens, max_length + 1, vocab)
    y_train = np.array(train_prop, dtype=np.float32)
    y_test = np.array(test_prop, dtype=np.float32)
    
    # Train/val split (80/20 within training)
    np.random.seed(SEED + fold_idx)
    n_tr = int(len(x_train) * 0.8)
    perm = np.random.permutation(len(x_train))
    x_tr, y_tr = x_train[perm[:n_tr]], y_train[perm[:n_tr]]
    x_val, y_val = x_train[perm[n_tr:]], y_train[perm[n_tr:]]
    
    # Create & compile model
    strategy = tf.distribute.OneDeviceStrategy(device="/cpu:0")
    with strategy.scope():
        mod = smilesx_model.LSTMAttModel.create(
            input_tokens=max_length + 1,
            vocab_size=len(vocab),
            embed_units=embed,
            lstm_units=lstm,
            tdense_units=tdense,
            dense_depth=0,
            model_type='classification'
        )
        mod.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=LR),
                    metrics=['accuracy'])
    
    # Train
    early_stop = EarlyStopBest(patience=PATIENCE)
    mod.fit({"smiles": x_tr}, y_tr,
            validation_data=({"smiles": x_val}, y_val),
            epochs=N_EPOCHS, batch_size=BATCH_SIZE,
            shuffle=True, callbacks=[early_stop], verbose=0)
    
    # Predict & aggregate over augmentations
    y_pred = mod.predict({"smiles": x_test}, verbose=0).ravel()
    y_pred_mean, y_pred_std = mean_result(test_card, y_pred)
    y_true = np.array(test_clean, dtype=int)
    y_pred_class = (y_pred_mean >= THRESHOLD).astype(int)
    
    f1 = f1_score(y_true, y_pred_class, zero_division=0)
    try:
        auc = roc_auc_score(y_true, y_pred_mean)
    except ValueError:
        auc = 0.0
    acc = accuracy_score(y_true, y_pred_class)
    prec = precision_score(y_true, y_pred_class, zero_division=0)
    rec = recall_score(y_true, y_pred_class, zero_division=0)
    
    elapsed = time.time() - t0
    logger.info(f"  [{config_name}] Fold {fold_idx}: F1={f1:.4f}, AUC={auc:.4f}, "
                f"Acc={acc:.4f}, Prec={prec:.4f}, Rec={rec:.4f}, "
                f"best_ep={early_stop.best_epoch+1}, time={elapsed:.0f}s")
    
    return {
        'config': config_name, 'fold': fold_idx,
        'f1': f1, 'auc': auc, 'accuracy': acc, 
        'precision': prec, 'recall': rec,
        'best_epoch': early_stop.best_epoch + 1,
        'elapsed_s': elapsed
    }


def main():
    os.makedirs(os.path.join(PROJECT_DIR, 'results'), exist_ok=True)
    
    smiles, labels = load_t0()
    logger.info(f"T0: {len(smiles)} molecules, {labels.sum()} pos, {(1-labels).sum()} neg")
    
    skf = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=SEED)
    
    all_results = []
    
    for config_name in ['reduced', 'original']:
        config = CONFIGS[config_name]
        logger.info(f"\n{'='*60}")
        logger.info(f"Config: {config_name} (embed={config['embed']}, "
                    f"lstm={config['lstm']}, tdense={config['tdense']})")
        logger.info(f"{'='*60}")
        
        fold_results = []
        for fold_idx, (train_idx, test_idx) in enumerate(skf.split(smiles, labels)):
            result = run_fold(
                config_name, config, fold_idx,
                smiles[train_idx], labels[train_idx], train_idx,
                smiles[test_idx], labels[test_idx], test_idx
            )
            fold_results.append(result)
            
            # Save intermediate results
            pd.DataFrame(all_results + fold_results).to_csv(
                os.path.join(PROJECT_DIR, 'results', 'tf_cv_intermediate.csv'), index=False)
        
        f1s = [r['f1'] for r in fold_results]
        aucs = [r['auc'] for r in fold_results]
        logger.info(f"\n{config_name} SUMMARY:")
        logger.info(f"  F1:  {np.mean(f1s):.4f} ± {np.std(f1s):.4f}")
        logger.info(f"  AUC: {np.mean(aucs):.4f} ± {np.std(aucs):.4f}")
        
        all_results.extend(fold_results)
    
    # Save final
    df = pd.DataFrame(all_results)
    outfile = os.path.join(PROJECT_DIR, 'results', 'tf_cv_results.csv')
    df.to_csv(outfile, index=False)
    logger.info(f"\nFinal results saved to {outfile}")
    
    # Summary
    summary = df.groupby('config').agg(
        f1_mean=('f1', 'mean'), f1_std=('f1', 'std'),
        auc_mean=('auc', 'mean'), auc_std=('auc', 'std'),
    ).round(4)
    logger.info(f"\n{summary.to_string()}")
    logger.info(f"\nPaper targets: F1≈0.80, AUC≈0.88")
    
    # Write completion marker
    with open(os.path.join(PROJECT_DIR, 'results', 'tf_cv_DONE.txt'), 'w') as f:
        f.write(f"Completed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(summary.to_string())


if __name__ == "__main__":
    main()
