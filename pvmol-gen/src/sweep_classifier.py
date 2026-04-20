#!/usr/bin/env python3
"""
PyTorch reimplementation of SMILES-X binary classifier for hyperparameter sweep.
Architecture: Embedding → BiLSTM → TimeDistributed Dense → SoftAttention → (extra features) → Dense(sigmoid)

Usage:
  python sweep_classifier.py --embed 256 --lstm 128 --tdense 128 --lr 1e-4 --batch 16 --epochs 200 --patience 25 --dense-depth 0 --extra-features --aug-factor 10 --threshold 0.47

Outputs JSON results to stdout for collection.
"""

import argparse
import json
import os
import sys
import time
import warnings
import random

import numpy as np

warnings.filterwarnings('ignore')

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score, precision_score, recall_score

# ── SMILES Tokenizer ────────────────────────────────────────
# Character-level tokenizer matching SMILES-X approach
SPECIAL_TOKENS = {
    '[Si]', '[N+]', '[C@H]', '[C@@H]', '[O-]', '[nH]', '[n+]',
    '[S+]', '[NH+]', '[NH2+]', '[NH3+]', '[O+]', '[S-]', '[B-]',
    '[BH-]', '[P+]', '[PH]', '[Se]', '[se]', '[te]',
    'Cl', 'Br', 'Si',
}

def tokenize_smiles(smi):
    """Tokenize a SMILES string into a list of tokens."""
    tokens = []
    i = 0
    while i < len(smi):
        # Check multi-char tokens (longest first)
        matched = False
        for tok in sorted(SPECIAL_TOKENS, key=len, reverse=True):
            if smi[i:i+len(tok)] == tok:
                tokens.append(tok)
                i += len(tok)
                matched = True
                break
        if not matched:
            tokens.append(smi[i])
            i += 1
    return tokens


def build_vocab(all_smiles):
    """Build vocabulary from list of SMILES strings."""
    vocab = {'<pad>': 0, '<unk>': 1}
    for smi in all_smiles:
        for tok in tokenize_smiles(smi):
            if tok not in vocab:
                vocab[tok] = len(vocab)
    return vocab


def encode_smiles(smi, vocab, max_len):
    """Encode SMILES to integer vector with padding."""
    tokens = tokenize_smiles(smi)
    ids = [vocab.get(t, vocab['<unk>']) for t in tokens[:max_len]]
    # Pad
    ids = ids + [vocab['<pad>']] * (max_len - len(ids))
    return ids


# ── SMILES Augmentation (atom rotation) ─────────────────────
def augment_smiles(smi, n_aug=10):
    """Generate augmented SMILES via RDKit atom renumbering."""
    try:
        from rdkit import Chem
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            return [smi]
        
        augmented = set()
        augmented.add(smi)
        n_atoms = mol.GetNumAtoms()
        
        for _ in range(n_aug * 3):  # Try more times to get enough unique
            if len(augmented) >= n_aug + 1:
                break
            perm = list(range(n_atoms))
            random.shuffle(perm)
            new_mol = Chem.RenumberAtoms(mol, perm)
            new_smi = Chem.MolToSmiles(new_mol, canonical=False)
            if new_smi:
                augmented.add(new_smi)
        
        return list(augmented)
    except ImportError:
        return [smi]


# ── Model ────────────────────────────────────────────────────
class SoftAttention(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.W = nn.Linear(hidden_size, 1, bias=True)
    
    def forward(self, x):
        # x: (batch, seq_len, hidden)
        scores = self.W(x)  # (batch, seq_len, 1)
        weights = F.softmax(scores, dim=1)  # (batch, seq_len, 1)
        attended = (x * weights).sum(dim=1)  # (batch, hidden)
        return attended


class SMILESXClassifier(nn.Module):
    def __init__(self, vocab_size, embed_units, lstm_units, tdense_units,
                 max_len, extra_dim=0, dense_depth=0, dropout=0.1):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_units, padding_idx=0)
        self.lstm = nn.LSTM(embed_units, lstm_units, batch_first=True, bidirectional=True)
        self.td_dense = nn.Linear(lstm_units * 2, tdense_units)  # *2 for bidirectional
        self.attention = SoftAttention(tdense_units)
        self.dropout = nn.Dropout(dropout)
        
        # Optional dense layers after attention + extra features
        input_dim = tdense_units + extra_dim
        dense_layers = []
        current_dim = input_dim
        for i in range(dense_depth):
            next_dim = max(current_dim // 2, 2)
            if next_dim <= 1:
                break
            dense_layers.append(nn.Linear(current_dim, next_dim))
            dense_layers.append(nn.ReLU())
            dense_layers.append(nn.Dropout(dropout))
            current_dim = next_dim
        
        self.dense_stack = nn.Sequential(*dense_layers) if dense_layers else nn.Identity()
        self.output = nn.Linear(current_dim, 1)
    
    def forward(self, smiles_input, extra_input=None):
        x = self.embedding(smiles_input)
        x, _ = self.lstm(x)
        x = self.td_dense(x)
        x = self.attention(x)
        x = self.dropout(x)
        
        if extra_input is not None:
            x = torch.cat([x, extra_input], dim=-1)
        
        x = self.dense_stack(x)
        x = self.output(x)
        return torch.sigmoid(x).squeeze(-1)


# ── Training ─────────────────────────────────────────────────
def train_fold(model, train_loader, val_loader, device, lr, epochs, patience, 
               threshold=0.47, has_extra=False):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.BCELoss()
    
    best_val_auc = 0
    best_state = None
    patience_counter = 0
    
    for epoch in range(epochs):
        # Train
        model.train()
        train_loss = 0
        for batch in train_loader:
            if has_extra:
                x_smi, x_extra, y = batch
                x_smi, x_extra, y = x_smi.to(device), x_extra.to(device), y.to(device)
                pred = model(x_smi, x_extra)
            else:
                x_smi, y = batch
                x_smi, y = x_smi.to(device), y.to(device)
                pred = model(x_smi)
            
            loss = criterion(pred, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        # Validate
        model.eval()
        all_preds = []
        all_labels = []
        with torch.no_grad():
            for batch in val_loader:
                if has_extra:
                    x_smi, x_extra, y = batch
                    x_smi, x_extra = x_smi.to(device), x_extra.to(device)
                    pred = model(x_smi, x_extra)
                else:
                    x_smi, y = batch
                    x_smi = x_smi.to(device)
                    pred = model(x_smi)
                all_preds.extend(pred.cpu().numpy())
                all_labels.extend(y.numpy())
        
        all_preds = np.array(all_preds)
        all_labels = np.array(all_labels)
        
        try:
            val_auc = roc_auc_score(all_labels, all_preds)
        except ValueError:
            val_auc = 0.5
        
        if val_auc > best_val_auc:
            best_val_auc = val_auc
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            patience_counter = 0
        else:
            patience_counter += 1
        
        if patience_counter >= patience:
            break
    
    # Restore best model and compute final metrics
    model.load_state_dict(best_state)
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for batch in val_loader:
            if has_extra:
                x_smi, x_extra, y = batch
                x_smi, x_extra = x_smi.to(device), x_extra.to(device)
                pred = model(x_smi, x_extra)
            else:
                x_smi, y = batch
                x_smi = x_smi.to(device)
                pred = model(x_smi)
            all_preds.extend(pred.cpu().numpy())
            all_labels.extend(y.numpy())
    
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    
    pred_class = (all_preds >= threshold).astype(int)
    
    f1 = f1_score(all_labels, pred_class)
    auc = roc_auc_score(all_labels, all_preds) if len(set(all_labels)) > 1 else 0.5
    acc = accuracy_score(all_labels, pred_class)
    prec = precision_score(all_labels, pred_class, zero_division=0)
    rec = recall_score(all_labels, pred_class, zero_division=0)
    
    return {
        'f1': float(f1), 'auc': float(auc), 'acc': float(acc),
        'prec': float(prec), 'rec': float(rec),
        'best_epoch': epoch + 1 - patience_counter,
    }


def main():
    p = argparse.ArgumentParser(description="SMILES-X Classifier Hyperparameter Sweep")
    p.add_argument('--embed', type=int, default=256)
    p.add_argument('--lstm', type=int, default=128)
    p.add_argument('--tdense', type=int, default=128)
    p.add_argument('--lr', type=float, default=1.26e-4)
    p.add_argument('--batch', type=int, default=16)
    p.add_argument('--epochs', type=int, default=100)
    p.add_argument('--patience', type=int, default=25)
    p.add_argument('--dense-depth', type=int, default=0)
    p.add_argument('--dropout', type=float, default=0.1)
    p.add_argument('--extra-features', action='store_true')
    p.add_argument('--aug-factor', type=int, default=10, help='SMILES augmentation factor (0=no aug)')
    p.add_argument('--threshold', type=float, default=0.47)
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--data', type=str, default='data/T0.csv')
    p.add_argument('--folds', type=int, default=5)
    p.add_argument('--device', type=str, default='auto')
    p.add_argument('--output', type=str, default=None, help='Output JSON file (default: stdout)')
    args = p.parse_args()
    
    # Reproducibility
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(args.seed)
    
    # Device
    if args.device == 'auto':
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    else:
        device = torch.device(args.device)
    
    print(f"Device: {device}", file=sys.stderr)
    
    # Load data
    import csv
    with open(args.data) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    smiles_list = [r['smiles'].strip() for r in rows]
    labels = [int(r['bin_class'].strip()) for r in rows]
    
    extra_features = None
    if args.extra_features:
        extra_features = np.array([
            [float(r.get('ha_num', 0) or 0), float(r.get('o_num', 0) or 0)]
            for r in rows
        ], dtype=np.float32)
    
    extra_dim = 2 if args.extra_features else 0
    
    print(f"Data: {len(smiles_list)} molecules, {sum(labels)} class 1, {len(labels) - sum(labels)} class 0", file=sys.stderr)
    
    # Build vocab from all SMILES (including augmented)
    all_smiles_for_vocab = list(smiles_list)
    if args.aug_factor > 0:
        for smi in smiles_list:
            all_smiles_for_vocab.extend(augment_smiles(smi, n_aug=args.aug_factor))
    
    vocab = build_vocab(all_smiles_for_vocab)
    
    # Compute max_len
    max_len = max(len(tokenize_smiles(s)) for s in all_smiles_for_vocab)
    max_len = min(max_len + 2, 150)  # Pad slightly, cap at 150
    
    print(f"Vocab: {len(vocab)} tokens, max_len: {max_len}", file=sys.stderr)
    
    # Cross-validation
    skf = StratifiedKFold(n_splits=args.folds, shuffle=True, random_state=args.seed)
    fold_results = []
    
    t0 = time.time()
    
    for fold_idx, (train_idx, val_idx) in enumerate(skf.split(smiles_list, labels)):
        fold_t0 = time.time()
        print(f"Fold {fold_idx}/{args.folds}...", file=sys.stderr)
        
        train_smiles = [smiles_list[i] for i in train_idx]
        train_labels = [labels[i] for i in train_idx]
        val_smiles = [smiles_list[i] for i in val_idx]
        val_labels = [labels[i] for i in val_idx]
        
        if args.extra_features:
            train_extra = extra_features[train_idx]
            val_extra = extra_features[val_idx]
        
        # Augment training data
        aug_smiles = []
        aug_labels = []
        aug_extra = []
        
        for j, (smi, lab) in enumerate(zip(train_smiles, train_labels)):
            if args.aug_factor > 0:
                variants = augment_smiles(smi, n_aug=args.aug_factor)
            else:
                variants = [smi]
            for v in variants:
                aug_smiles.append(v)
                aug_labels.append(lab)
                if args.extra_features:
                    aug_extra.append(train_extra[j])
        
        print(f"  Train: {len(train_smiles)}→{len(aug_smiles)}, Val: {len(val_smiles)}", file=sys.stderr)
        
        # Encode
        X_train = torch.LongTensor([encode_smiles(s, vocab, max_len) for s in aug_smiles])
        y_train = torch.FloatTensor(aug_labels)
        X_val = torch.LongTensor([encode_smiles(s, vocab, max_len) for s in val_smiles])
        y_val = torch.FloatTensor(val_labels)
        
        if args.extra_features:
            E_train = torch.FloatTensor(np.array(aug_extra))
            E_val = torch.FloatTensor(val_extra)
            train_ds = TensorDataset(X_train, E_train, y_train)
            val_ds = TensorDataset(X_val, E_val, y_val)
        else:
            train_ds = TensorDataset(X_train, y_train)
            val_ds = TensorDataset(X_val, y_val)
        
        train_loader = DataLoader(train_ds, batch_size=args.batch, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=args.batch, shuffle=False)
        
        # Create model
        model = SMILESXClassifier(
            vocab_size=len(vocab),
            embed_units=args.embed,
            lstm_units=args.lstm,
            tdense_units=args.tdense,
            max_len=max_len,
            extra_dim=extra_dim,
            dense_depth=args.dense_depth,
            dropout=args.dropout,
        ).to(device)
        
        # Train
        result = train_fold(
            model, train_loader, val_loader, device,
            lr=args.lr, epochs=args.epochs, patience=args.patience,
            threshold=args.threshold, has_extra=args.extra_features,
        )
        result['fold'] = fold_idx
        result['train_size'] = len(aug_smiles)
        result['val_size'] = len(val_smiles)
        result['time_s'] = time.time() - fold_t0
        fold_results.append(result)
        
        print(f"  Fold {fold_idx}: F1={result['f1']:.4f}, AUC={result['auc']:.4f}, "
              f"Acc={result['acc']:.4f}, time={result['time_s']:.0f}s", file=sys.stderr)
    
    total_time = time.time() - t0
    
    # Aggregate
    mean_f1 = np.mean([r['f1'] for r in fold_results])
    std_f1 = np.std([r['f1'] for r in fold_results])
    mean_auc = np.mean([r['auc'] for r in fold_results])
    std_auc = np.std([r['auc'] for r in fold_results])
    mean_acc = np.mean([r['acc'] for r in fold_results])
    
    summary = {
        'params': vars(args),
        'mean_f1': float(mean_f1),
        'std_f1': float(std_f1),
        'mean_auc': float(mean_auc),
        'std_auc': float(std_auc),
        'mean_acc': float(mean_acc),
        'folds': fold_results,
        'total_time_s': float(total_time),
        'device': str(device),
        'vocab_size': len(vocab),
        'max_len': max_len,
    }
    
    output = json.dumps(summary, indent=2)
    
    if args.output:
        os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"\nResults saved to {args.output}", file=sys.stderr)
    else:
        print(output)
    
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"SUMMARY: F1={mean_f1:.4f}±{std_f1:.4f}, AUC={mean_auc:.4f}±{std_auc:.4f}, "
          f"Acc={mean_acc:.4f}, Time={total_time:.0f}s", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)


if __name__ == '__main__':
    main()
