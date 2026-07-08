#!/usr/bin/env python3
"""
Stage 1 'match' variant: PyTorch SMILES-X stripped to match TF exactly.

Changes from stage1_classifier.py:
  - dropout=0.0 (TF has no dropout)
  - 3 runs per fold (matching TF n_runs=3)
  - No class weighting (plain BCEWithLogitsLoss)
  - No ignore_first_epochs (TF ignores first 0 by default)
  - Train/val split within each fold (80/20 of training portion)
  - Report per-run and per-fold metrics like TF
  - Same hyperparams: embed=512, lstm=128, tdense=128, lr=10^-3.9, bs=16, patience=25
"""
import sys, os, math, time, logging, json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import (f1_score, precision_score, recall_score, 
                             accuracy_score, average_precision_score)

sys.path.insert(0, os.path.dirname(__file__))
from stage1_classifier import (
    SmilesTokenizer, SmilesXClassifier, augment_smiles_exhaustive,
    SmilesDataset, tokenize_smiles
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ─── Config ─────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'T0.csv')
OUTDIR = os.path.join(os.path.dirname(__file__), '..', 'outputs_match_tf')

K_FOLDS = 5
N_RUNS = 3
MAX_EPOCHS = 100
PATIENCE = 25
EMBED_DIM = 512
LSTM_UNITS = 128
TDENSE_UNITS = 128
LR = math.pow(10, -3.9)   # ~1.26e-4
BATCH_SIZE = 16
DROPOUT = 0.0              # Match TF: no dropout
THRESHOLD = 0.5            # Standard threshold (TF uses 0.5 default)

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss, total_correct, total_n = 0, 0, 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * x.size(0)
        preds = (torch.sigmoid(logits) >= 0.5).float()
        total_correct += (preds == y).sum().item()
        total_n += x.size(0)
    return total_loss / total_n, total_correct / total_n


def eval_metrics(model, loader, device, threshold=0.5):
    model.eval()
    all_probs, all_labels = [], []
    total_loss = 0
    criterion = nn.BCEWithLogitsLoss()
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            total_loss += criterion(logits, y).item() * x.size(0)
            probs = torch.sigmoid(logits).cpu().numpy()
            all_probs.extend(probs)
            all_labels.extend(y.cpu().numpy())
    
    all_probs = np.array(all_probs)
    all_labels = np.array(all_labels)
    n = len(all_labels)
    preds = (all_probs >= threshold).astype(int)
    
    acc = accuracy_score(all_labels, preds)
    prec = precision_score(all_labels, preds, zero_division=0)
    rec = recall_score(all_labels, preds, zero_division=0)
    f1 = f1_score(all_labels, preds, zero_division=0)
    try:
        auc = average_precision_score(all_labels, all_probs)
    except:
        auc = 0.0
    
    return {
        'loss': total_loss / n, 'acc': acc, 'prec': prec, 
        'rec': rec, 'f1': f1, 'auc_pr': auc,
        'probs': all_probs, 'labels': all_labels
    }


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    
    # Load data
    df = pd.read_csv(DATA_FILE)
    smiles = df['smiles'].tolist()
    labels = df['bin_class'].astype(int).tolist()
    logger.info(f"Loaded T0: {len(smiles)} molecules, {sum(labels)} class-1, {len(labels)-sum(labels)} class-0")
    
    device = torch.device(DEVICE)
    logger.info(f"Device: {device}")
    
    skf = StratifiedKFold(n_splits=K_FOLDS, shuffle=True, random_state=42)
    
    all_fold_results = []
    all_test_probs = {}
    t_start = time.time()
    
    for fold, (train_val_idx, test_idx) in enumerate(skf.split(smiles, labels)):
        fold_start = time.time()
        logger.info(f"\n{'='*60}")
        logger.info(f"Fold {fold}/{K_FOLDS}")
        logger.info(f"{'='*60}")
        
        # Split train_val into train + val (80/20 like TF)
        tv_smiles = [smiles[i] for i in train_val_idx]
        tv_labels = [labels[i] for i in train_val_idx]
        test_smiles = [smiles[i] for i in test_idx]
        test_labels = [labels[i] for i in test_idx]
        
        tr_smiles, val_smiles, tr_labels, val_labels = train_test_split(
            tv_smiles, tv_labels, test_size=0.2, stratify=tv_labels, random_state=fold
        )
        
        # Augment training SMILES
        aug_smiles, aug_labels = [], []
        for smi, lab in zip(tr_smiles, tr_labels):
            variants = augment_smiles_exhaustive(smi)
            aug_smiles.extend(variants)
            aug_labels.extend([lab] * len(variants))
        
        # Augment val and test too (like TF)
        aug_val_smiles, aug_val_labels = [], []
        for smi, lab in zip(val_smiles, val_labels):
            variants = augment_smiles_exhaustive(smi)
            aug_val_smiles.extend(variants)
            aug_val_labels.extend([lab] * len(variants))
        
        aug_test_smiles, aug_test_labels = [], []
        for smi, lab in zip(test_smiles, test_labels):
            variants = augment_smiles_exhaustive(smi)
            aug_test_smiles.extend(variants)
            aug_test_labels.extend([lab] * len(variants))
        
        logger.info(f"  Train: {len(tr_smiles)} → {len(aug_smiles)} augmented")
        logger.info(f"  Val:   {len(val_smiles)} → {len(aug_val_smiles)} augmented")
        logger.info(f"  Test:  {len(test_smiles)} → {len(aug_test_smiles)} augmented")
        
        # Build tokenizer
        tokenizer = SmilesTokenizer(max_len=128)
        tokenizer.fit(aug_smiles + aug_val_smiles + aug_test_smiles)
        
        # Datasets
        kwargs = dict(num_workers=2, pin_memory=True) if device.type == 'cuda' else {}
        train_ds = SmilesDataset(aug_smiles, aug_labels, tokenizer)
        val_ds = SmilesDataset(aug_val_smiles, aug_val_labels, tokenizer)
        test_ds = SmilesDataset(aug_test_smiles, aug_test_labels, tokenizer)
        
        train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, drop_last=False, **kwargs)
        val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, **kwargs)
        test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, **kwargs)
        
        fold_run_metrics = []
        
        for run in range(N_RUNS):
            run_start = time.time()
            logger.info(f"\n  --- Run {run}/{N_RUNS} ---")
            
            # Fresh model each run (different random init)
            torch.manual_seed(42 + fold * 100 + run)
            model = SmilesXClassifier(
                vocab_size=tokenizer.vocab_size,
                max_len=tokenizer.max_len,
                embed_dim=EMBED_DIM,
                lstm_units=LSTM_UNITS,
                tdense_units=TDENSE_UNITS,
                dropout=DROPOUT,
            ).to(device)
            
            optimizer = torch.optim.Adam(model.parameters(), lr=LR)
            criterion = nn.BCEWithLogitsLoss()
            
            best_val_loss = float('inf')
            patience_counter = 0
            best_state = None
            
            for epoch in range(MAX_EPOCHS):
                train_loss, train_acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
                
                # Val loss for early stopping
                val_m = eval_metrics(model, val_loader, device)
                
                if (epoch + 1) % 20 == 0 or epoch == 0:
                    logger.info(f"    Ep {epoch+1}: train_loss={train_loss:.4f} train_acc={train_acc:.4f} "
                               f"val_loss={val_m['loss']:.4f} val_acc={val_m['acc']:.4f}")
                
                if val_m['loss'] < best_val_loss:
                    best_val_loss = val_m['loss']
                    best_state = {k: v.clone() for k, v in model.state_dict().items()}
                    patience_counter = 0
                else:
                    patience_counter += 1
                
                if patience_counter >= PATIENCE:
                    logger.info(f"    Early stop at epoch {epoch+1}")
                    break
            
            # Load best model
            if best_state:
                model.load_state_dict(best_state)
            
            # Evaluate on all 3 sets
            train_m = eval_metrics(model, train_loader, device)
            val_m = eval_metrics(model, val_loader, device)
            test_m = eval_metrics(model, test_loader, device)
            
            run_dur = time.time() - run_start
            logger.info(f"    Run {run} ({run_dur:.0f}s): "
                        f"Train F1={train_m['f1']:.4f} AUC={train_m['auc_pr']:.4f} | "
                        f"Val F1={val_m['f1']:.4f} AUC={val_m['auc_pr']:.4f} | "
                        f"Test F1={test_m['f1']:.4f} AUC={test_m['auc_pr']:.4f}")
            
            fold_run_metrics.append({
                'fold': fold, 'run': run,
                'train': {k: v for k, v in train_m.items() if k not in ('probs', 'labels')},
                'val': {k: v for k, v in val_m.items() if k not in ('probs', 'labels')},
                'test': {k: v for k, v in test_m.items() if k not in ('probs', 'labels')},
            })
        
        # Fold summary (average across runs)
        test_f1s = [r['test']['f1'] for r in fold_run_metrics if r['fold'] == fold]
        test_aucs = [r['test']['auc_pr'] for r in fold_run_metrics if r['fold'] == fold]
        test_accs = [r['test']['acc'] for r in fold_run_metrics if r['fold'] == fold]
        
        fold_dur = time.time() - fold_start
        logger.info(f"\n  Fold {fold} overall ({fold_dur:.0f}s):")
        logger.info(f"    Test Acc  = {np.mean(test_accs):.4f} ± {np.std(test_accs):.4f}")
        logger.info(f"    Test F1   = {np.mean(test_f1s):.4f} ± {np.std(test_f1s):.4f}")
        logger.info(f"    Test AUC  = {np.mean(test_aucs):.4f} ± {np.std(test_aucs):.4f}")
        
        all_fold_results.extend(fold_run_metrics)
    
    # ─── Final Summary ───────────────────────────────
    total_dur = time.time() - t_start
    logger.info(f"\n{'='*60}")
    logger.info(f"FINAL RESULTS (total: {total_dur:.0f}s)")
    logger.info(f"{'='*60}")
    
    # Per-fold averages
    for fold in range(K_FOLDS):
        fold_runs = [r for r in all_fold_results if r['fold'] == fold]
        f1s = [r['test']['f1'] for r in fold_runs]
        aucs = [r['test']['auc_pr'] for r in fold_runs]
        accs = [r['test']['acc'] for r in fold_runs]
        logger.info(f"  Fold {fold}: F1={np.mean(f1s):.4f}±{np.std(f1s):.4f}  "
                     f"AUC={np.mean(aucs):.4f}±{np.std(aucs):.4f}  "
                     f"Acc={np.mean(accs):.4f}±{np.std(accs):.4f}")
    
    # Overall
    all_test_f1s = [r['test']['f1'] for r in all_fold_results]
    all_test_aucs = [r['test']['auc_pr'] for r in all_fold_results]
    all_test_accs = [r['test']['acc'] for r in all_fold_results]
    
    logger.info(f"\n  Overall (5-fold × 3-run):")
    logger.info(f"    F1   = {np.mean(all_test_f1s):.4f} ± {np.std(all_test_f1s):.4f}")
    logger.info(f"    AUC  = {np.mean(all_test_aucs):.4f} ± {np.std(all_test_aucs):.4f}")
    logger.info(f"    Acc  = {np.mean(all_test_accs):.4f} ± {np.std(all_test_accs):.4f}")
    
    # Save results
    with open(os.path.join(OUTDIR, 'results.json'), 'w') as f:
        json.dump({
            'config': {
                'dropout': DROPOUT, 'n_folds': K_FOLDS, 'n_runs': N_RUNS,
                'embed': EMBED_DIM, 'lstm': LSTM_UNITS, 'tdense': TDENSE_UNITS,
                'lr': LR, 'batch_size': BATCH_SIZE, 'patience': PATIENCE,
                'max_epochs': MAX_EPOCHS, 'device': str(device),
            },
            'fold_results': all_fold_results,
            'summary': {
                'f1_mean': float(np.mean(all_test_f1s)),
                'f1_std': float(np.std(all_test_f1s)),
                'auc_mean': float(np.mean(all_test_aucs)),
                'auc_std': float(np.std(all_test_aucs)),
                'acc_mean': float(np.mean(all_test_accs)),
                'acc_std': float(np.std(all_test_accs)),
            },
            'total_seconds': total_dur,
        }, f, indent=2)
    
    logger.info(f"\nResults saved to {OUTDIR}/results.json")


if __name__ == '__main__':
    main()
