#!/usr/bin/env python
"""
Compare classifier implementations on T0 data:
  1. Original SMILES-X (TensorFlow/Keras) — embed=512/lstm=128/tdense=128
  2. Original SMILES-X (TensorFlow/Keras) — embed=128/lstm=64/tdense=64
  3. PyTorch reimplementation — embed=128/lstm=64/tdense=64

All use same 5-fold stratified CV with random_state=42, threshold=0.47.
Results saved to results/classifier_comparison.csv
"""

import os
import sys
import math
import time
import logging
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, 'smilesx_lib'))
sys.path.insert(0, SCRIPT_DIR)

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

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from config import T0_FILE, RESULTS_DIR, PCE_THRESHOLD, CLASSIFICATION_THRESHOLD, CV_FOLDS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Import PyTorch model from existing script
from stage1_classifier import (
    SmilesXClassifier as PyTorchClassifier,
    SmilesTokenizer as PyTorchTokenizer,
    SmilesDataset as PyTorchDataset,
    augment_smiles_exhaustive,
    tokenize_smiles,
)

# ── Constants ────────────────────────────────────────────────
LR_REF = 3.9
PATIENCE = 25
N_EPOCHS = 100
BATCH_SIZE = 16
THRESHOLD = CLASSIFICATION_THRESHOLD  # 0.47
SEED = 42


# ── TF Early Stopping Callback ──────────────────────────────
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


# ── Data Loading ─────────────────────────────────────────────
def load_t0():
    df = pd.read_csv(T0_FILE)
    if 'source' in df.columns:
        df = df[df['source'] == 'T0_original'].reset_index(drop=True)
    smiles = np.array(df['smiles'].tolist(), dtype=object)
    if 'bin_class' in df.columns:
        labels = df['bin_class'].astype(int).values
    else:
        labels = (df['delta_pce_norm'] >= PCE_THRESHOLD).astype(int).values
    return smiles, labels


# ── TF SMILESX Fold ─────────────────────────────────────────
def run_tf_fold(fold_idx, train_smiles, train_labels, train_indices,
                test_smiles, test_labels, test_indices,
                embed, lstm, tdense, augmentation=True):
    """Train one fold with original TF SMILESX, return metrics dict."""
    K.clear_session()
    
    # Augment — pass labels as 2D to work around library bug with .extend() on scalar
    train_2d = np.array(train_smiles).reshape(-1, 1)
    test_2d = np.array(test_smiles).reshape(-1, 1)
    
    train_res = smilesx_augm.augmentation(train_2d, train_indices, None,
                                          train_labels.astype(float).reshape(-1, 1), True, augmentation)
    test_res = smilesx_augm.augmentation(test_2d, test_indices, None,
                                         test_labels.astype(float).reshape(-1, 1), True, augmentation)
    
    train_enum, _, train_prop_enum, train_prop_clean, train_card, _ = train_res
    test_enum, _, test_prop_enum, test_prop_clean, test_card, _ = test_res
    if train_prop_enum is not None:
        train_prop_enum = train_prop_enum.ravel()
    if train_prop_clean is not None:
        train_prop_clean = train_prop_clean.ravel()
    if test_prop_enum is not None:
        test_prop_enum = test_prop_enum.ravel()
    if test_prop_clean is not None:
        test_prop_clean = test_prop_clean.ravel()
    
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
    y_train = np.array(train_prop_enum, dtype=np.float32)
    y_test = np.array(test_prop_enum, dtype=np.float32)
    
    # Train/val split
    np.random.seed(SEED)
    n_tr = int(len(x_train) * 0.8)
    perm = np.random.permutation(len(x_train))
    x_tr, y_tr = x_train[perm[:n_tr]], y_train[perm[:n_tr]]
    x_val, y_val = x_train[perm[n_tr:]], y_train[perm[n_tr:]]
    
    # Create model
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
        mod.compile(loss='binary_crossentropy',
                    optimizer=Adam(learning_rate=math.pow(10, -LR_REF)),
                    metrics=['accuracy'])
    
    early_stop = EarlyStopBest(patience=PATIENCE)
    mod.fit({"smiles": x_tr}, y_tr,
            validation_data=({"smiles": x_val}, y_val),
            epochs=N_EPOCHS, batch_size=BATCH_SIZE,
            shuffle=True, callbacks=[early_stop], verbose=0)
    
    # Predict
    y_pred = mod.predict({"smiles": x_test}, verbose=0).ravel()
    y_pred_mean, _ = mean_result(test_card, y_pred)
    y_true = np.array(test_prop_clean, dtype=float).astype(int)
    y_pred_class = (y_pred_mean >= THRESHOLD).astype(int)
    
    f1 = f1_score(y_true, y_pred_class, zero_division=0)
    try:
        auc = roc_auc_score(y_true, y_pred_mean)
    except ValueError:
        auc = 0.0
    acc = accuracy_score(y_true, y_pred_class)
    prec = precision_score(y_true, y_pred_class, zero_division=0)
    rec = recall_score(y_true, y_pred_class, zero_division=0)
    
    return {'f1': f1, 'auc': auc, 'accuracy': acc, 'precision': prec,
            'recall': rec, 'best_epoch': early_stop.best_epoch + 1}


# ── PyTorch Fold ─────────────────────────────────────────────
def run_pytorch_fold(fold_idx, train_smiles, train_labels, test_smiles, test_labels):
    """Train one fold with our PyTorch reimplementation."""
    device = torch.device('cpu')
    
    # Build tokenizer
    tokenizer = PyTorchTokenizer(max_len=128)
    all_smi = list(train_smiles) + list(test_smiles)
    tokenizer.fit(all_smi)
    
    # Augment training data
    aug_smiles, aug_labels = [], []
    for smi, lab in zip(train_smiles, train_labels):
        variants = augment_smiles_exhaustive(smi)
        aug_smiles.extend(variants)
        aug_labels.extend([lab] * len(variants))
    
    # Update tokenizer with augmented vocab
    tokenizer.fit(aug_smiles + list(test_smiles))
    
    train_ds = PyTorchDataset(aug_smiles, aug_labels, tokenizer)
    test_ds = PyTorchDataset(list(test_smiles), list(test_labels), tokenizer)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE)
    
    model = PyTorchClassifier(
        vocab_size=tokenizer.vocab_size,
        max_len=tokenizer.max_len,
        embed_dim=128, lstm_units=64, tdense_units=64
    ).to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=math.pow(10, -LR_REF))
    criterion = nn.BCEWithLogitsLoss()
    
    best_val_loss = float('inf')
    patience_counter = 0
    best_state = None
    best_epoch = 0
    
    for epoch in range(N_EPOCHS):
        model.train()
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            logits = model(x)
            loss = criterion(logits, y)
            loss.backward()
            optimizer.step()
        
        # Validation = test set (same as TF version for fair comparison)
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for x, y in test_loader:
                x, y = x.to(device), y.to(device)
                val_loss += criterion(model(x), y).item() * x.size(0)
        val_loss /= len(test_ds)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
            patience_counter = 0
            best_epoch = epoch + 1
        else:
            patience_counter += 1
        if patience_counter >= PATIENCE:
            break
    
    if best_state:
        model.load_state_dict(best_state)
    
    # Test-time prediction with augmentation averaging
    model.eval()
    all_probs, all_labels_list = [], []
    with torch.no_grad():
        for smi, lab in zip(test_smiles, test_labels):
            variants = augment_smiles_exhaustive(smi)
            probs = []
            for v in variants:
                ids = torch.tensor([tokenizer.encode(v)], dtype=torch.long).to(device)
                prob = torch.sigmoid(model(ids)).item()
                probs.append(prob)
            all_probs.append(np.mean(probs))
            all_labels_list.append(lab)
    
    all_probs = np.array(all_probs)
    all_labels_arr = np.array(all_labels_list)
    preds = (all_probs >= THRESHOLD).astype(int)
    
    f1 = f1_score(all_labels_arr, preds, zero_division=0)
    try:
        auc = roc_auc_score(all_labels_arr, all_probs)
    except ValueError:
        auc = 0.0
    acc = accuracy_score(all_labels_arr, preds)
    prec = precision_score(all_labels_arr, preds, zero_division=0)
    rec = recall_score(all_labels_arr, preds, zero_division=0)
    
    return {'f1': f1, 'auc': auc, 'accuracy': acc, 'precision': prec,
            'recall': rec, 'best_epoch': best_epoch}


# ── Main Comparison ──────────────────────────────────────────
def run_comparison():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    smiles, labels = load_t0()
    
    logger.info(f"T0: {len(smiles)} molecules, {labels.sum()} class 1, {(1-labels).sum()} class 0")
    
    skf = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=SEED)
    all_results = []
    
    methods = [
        ('TF_original_512', {'embed': 512, 'lstm': 128, 'tdense': 128}),
        ('TF_reduced_128',  {'embed': 128, 'lstm': 64,  'tdense': 64}),
        ('PyTorch_128',     None),  # Uses PyTorch reimplementation
    ]
    
    for method_name, config in methods:
        logger.info(f"\n{'='*60}")
        logger.info(f"Running: {method_name}")
        logger.info(f"{'='*60}")
        
        fold_results = []
        start = time.time()
        
        for fold_idx, (train_idx, test_idx) in enumerate(skf.split(smiles, labels)):
            logger.info(f"  Fold {fold_idx + 1}/{CV_FOLDS}")
            
            train_smi = smiles[train_idx]
            train_lab = labels[train_idx]
            test_smi = smiles[test_idx]
            test_lab = labels[test_idx]
            
            if config is not None:
                # TF SMILESX
                result = run_tf_fold(
                    fold_idx, train_smi, train_lab, train_idx,
                    test_smi, test_lab, test_idx,
                    embed=config['embed'], lstm=config['lstm'], tdense=config['tdense'],
                    augmentation=True
                )
            else:
                # PyTorch
                result = run_pytorch_fold(fold_idx, train_smi, train_lab, test_smi, test_lab)
            
            result['method'] = method_name
            result['fold'] = fold_idx
            fold_results.append(result)
            
            logger.info(f"    F1={result['f1']:.4f}, AUC={result['auc']:.4f}, "
                        f"Acc={result['accuracy']:.4f}")
        
        elapsed = time.time() - start
        f1s = [r['f1'] for r in fold_results]
        aucs = [r['auc'] for r in fold_results]
        
        logger.info(f"\n  {method_name} Summary:")
        logger.info(f"    F1:  {np.mean(f1s):.4f} ± {np.std(f1s):.4f}")
        logger.info(f"    AUC: {np.mean(aucs):.4f} ± {np.std(aucs):.4f}")
        logger.info(f"    Time: {elapsed:.1f}s")
        
        all_results.extend(fold_results)
    
    # Save detailed results
    df = pd.DataFrame(all_results)
    outfile = RESULTS_DIR / "classifier_comparison.csv"
    df.to_csv(outfile, index=False)
    logger.info(f"\nDetailed results saved to {outfile}")
    
    # Summary table
    summary = df.groupby('method').agg(
        f1_mean=('f1', 'mean'), f1_std=('f1', 'std'),
        auc_mean=('auc', 'mean'), auc_std=('auc', 'std'),
        acc_mean=('accuracy', 'mean'), acc_std=('accuracy', 'std'),
        prec_mean=('precision', 'mean'), rec_mean=('recall', 'mean'),
    ).round(4)
    
    logger.info(f"\n{'='*80}")
    logger.info("COMPARISON SUMMARY")
    logger.info(f"{'='*80}")
    logger.info(f"\n{summary.to_string()}")
    logger.info(f"\nPaper targets: F1 ≈ 0.80, AUC ≈ 0.88")
    logger.info(f"{'='*80}")
    
    return df


if __name__ == "__main__":
    run_comparison()
