"""Comprehensive investigation: try every plausible theory to replicate
the paper's SMILES-X F1=0.80 and CM: TN=157, FP=24, FN=31, TP=102.

Theories:
1. Aggregated CV with probability averaging across 3 runs per fold
2. Different train/val/test split ratios within folds
3. Threshold optimized on aggregated validation data (not per-fold)
4. Paper's architecture (found via geom+bayopt) differs from ours
5. No extra features (paper's Section 2.1 says SMILES-X "does not require
   molecular descriptors" — maybe ha_num/o_num weren't used for the main CM?)
6. Different augmentation strategy (Keras enumerate vs our augment)
7. Validation predictions reported instead of test predictions
8. Best-of-3-runs selection per fold
9. Class weighting differences
10. No dropout in original Keras SMILES-X
"""

import json
import logging
import os
import sys
from itertools import product

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import (
    f1_score, roc_auc_score, accuracy_score, precision_score, recall_score,
    confusion_matrix, precision_recall_curve, auc,
)

from smilesx.tokenizer import SmilesTokenizer
from smilesx.augment import augment_smiles
from smilesx.model import LSTMAttModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/all_theories.log"),
    ],
)
logger = logging.getLogger(__name__)

DATA_PATH = "data/T0.csv"
PAPER_CM = {"tn": 157, "fp": 24, "fn": 31, "tp": 102}
PAPER_F1 = 2 * 102 / (2 * 102 + 24 + 31)


def report(label, y_true, y_pred, y_prob=None, verbose=True):
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    f1 = f1_score(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    auc_roc = roc_auc_score(y_true, y_prob) if y_prob is not None else 0

    match = " *** EXACT MATCH ***" if (tn == 157 and fp == 24 and fn == 31 and tp == 102) else ""
    close = ""
    if not match and abs(f1 - PAPER_F1) < 0.05:
        close = " (CLOSE)"

    if verbose:
        print(
            f"  {label}\n"
            f"    TN={tn} FP={fp} FN={fn} TP={tp} | "
            f"F1={f1:.4f} Prec={prec:.4f} Rec={rec:.4f} Acc={acc:.4f} AUC={auc_roc:.4f}"
            f"{match}{close}"
        )
    return {"f1": f1, "tn": tn, "fp": fp, "fn": fn, "tp": tp, "auc": auc_roc}


def train_model(
    model, train_loader, val_loader, device, has_extra,
    lr, weight_decay, n_epochs, patience, pos_weight=None,
):
    """Train one model, return best state."""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.5, patience=10, min_lr=1e-6,
    )

    if pos_weight is not None:
        criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight], device=device))
        use_logits = True
    else:
        criterion = nn.BCELoss()
        use_logits = False

    best_val_loss = float("inf")
    best_state = None
    epochs_no_improve = 0

    for epoch in range(n_epochs):
        model.train()
        for batch in train_loader:
            xb, yb = batch[0].to(device), batch[1].to(device)
            eb = batch[2].to(device) if has_extra else None
            optimizer.zero_grad()
            if use_logits:
                model.model_type = "regression"
                out = model(xb, extra=eb)
                model.model_type = "classification"
                loss = criterion(out, yb)
            else:
                out = model(xb, extra=eb)
                loss = criterion(out, yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

        model.eval()
        val_loss = 0
        n = 0
        with torch.no_grad():
            for batch in val_loader:
                xb, yb = batch[0].to(device), batch[1].to(device)
                eb = batch[2].to(device) if has_extra else None
                if use_logits:
                    model.model_type = "regression"
                    out = model(xb, extra=eb)
                    model.model_type = "classification"
                    val_loss += criterion(out, yb).item()
                else:
                    out = model(xb, extra=eb)
                    val_loss += criterion(out, yb).item()
                n += 1
        val_loss /= max(n, 1)
        scheduler.step(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1

        if epochs_no_improve >= patience:
            break

    if best_state:
        model.load_state_dict(best_state)
        model.to(device)
    return model


def predict_with_tta(model, smiles_list, tokenizer, max_length, device,
                     extra_features=None, has_extra=False, batch_size=64):
    """Predict with test-time augmentation."""
    model.eval()
    dummy_labels = [0.0] * len(smiles_list)
    aug_smiles, aug_labels, aug_groups = augment_smiles(smiles_list, dummy_labels, augment=True)
    X = tokenizer.encode_batch(aug_smiles, max_length)

    if has_extra and extra_features is not None:
        aug_extra = np.array([extra_features[g] for g in aug_groups], dtype=np.float32)
    else:
        aug_extra = None

    tensors = [torch.from_numpy(X).long()]
    if aug_extra is not None:
        tensors.append(torch.from_numpy(aug_extra).float())

    all_probs = []
    with torch.no_grad():
        for i in range(0, len(X), batch_size):
            xb = tensors[0][i:i+batch_size].to(device)
            eb = tensors[1][i:i+batch_size].to(device) if aug_extra is not None else None
            pred = model(xb, extra=eb)
            all_probs.append(pred.cpu().numpy().ravel())

    raw_probs = np.concatenate(all_probs)
    probs = np.zeros(len(smiles_list))
    for i in range(len(smiles_list)):
        mask = [j for j, g in enumerate(aug_groups) if g == i]
        probs[i] = raw_probs[mask].mean() if mask else 0.0
    return probs


def run_full_cv(
    df, smiles_col, label_col, extra_cols,
    embed_dim, lstm_units, tdense_units, dense_depth, dropout,
    lr, weight_decay, batch_size, n_epochs, patience,
    n_folds, n_runs, class_weight, augment, device, seed,
    val_size=0.2, global_threshold=None,
):
    """Full CV with multiple runs per fold. Returns per-molecule probabilities."""
    smiles = df[smiles_col].values.tolist()
    labels = df[label_col].values.astype(int).tolist()

    n_extra = len(extra_cols)
    extra_features = None
    if n_extra > 0:
        extra_features = df[extra_cols].values.astype(np.float32)
        col_means = np.nanmean(extra_features, axis=0)
        for c in range(n_extra):
            mask = np.isnan(extra_features[:, c])
            extra_features[mask, c] = col_means[c]

    tokenizer = SmilesTokenizer().fit(smiles)
    all_tok = tokenizer.tokenize_batch(smiles)
    max_length = max(len(t) for t in all_tok) + 1

    n_pos = sum(labels)
    n_neg = len(labels) - n_pos
    pos_weight_val = n_neg / n_pos if class_weight and n_pos > 0 else None

    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)

    # Store per-molecule probabilities for each run
    all_run_probs = np.zeros((n_runs, len(smiles)))
    # Track which fold each molecule belongs to
    mol_fold = np.full(len(smiles), -1)

    # Also store val probs for threshold optimization
    all_val_probs = {}  # fold -> list of (run_probs, val_indices)

    for fold_idx, (train_val_idx, test_idx) in enumerate(skf.split(smiles, labels)):
        for i in test_idx:
            mol_fold[i] = fold_idx

        train_smiles_raw = [smiles[i] for i in train_val_idx]
        train_labels_raw = [labels[i] for i in train_val_idx]
        test_smiles = [smiles[i] for i in test_idx]

        train_extra_raw = extra_features[train_val_idx] if extra_features is not None else None
        test_extra = extra_features[test_idx] if extra_features is not None else None

        # Split train/val
        if train_extra_raw is not None:
            tr_smi, val_smi, tr_lab, val_lab, tr_ext, val_ext = train_test_split(
                train_smiles_raw, train_labels_raw, train_extra_raw.tolist(),
                test_size=val_size, stratify=train_labels_raw,
                random_state=seed + fold_idx,
            )
            tr_ext = np.array(tr_ext, dtype=np.float32)
            val_ext = np.array(val_ext, dtype=np.float32)
        else:
            tr_smi, val_smi, tr_lab, val_lab = train_test_split(
                train_smiles_raw, train_labels_raw,
                test_size=val_size, stratify=train_labels_raw,
                random_state=seed + fold_idx,
            )
            tr_ext = val_ext = test_ext = None

        for run in range(n_runs):
            run_seed = seed + fold_idx * 100 + run
            torch.manual_seed(run_seed)
            np.random.seed(run_seed)

            # Augment
            if augment:
                aug_smi, aug_lab, aug_grp = augment_smiles(tr_smi, tr_lab, augment=True)
            else:
                aug_smi, aug_lab, aug_grp = augment_smiles(tr_smi, tr_lab, augment=False)

            if tr_ext is not None:
                aug_ext = np.array([tr_ext[g] for g in aug_grp], dtype=np.float32)
            else:
                aug_ext = None

            # Encode
            X_train = tokenizer.encode_batch(aug_smi, max_length)
            y_train = np.array(aug_lab, dtype=np.float32)

            # Val (canonical only)
            val_smi_c, val_lab_c, val_grp_c = augment_smiles(val_smi, val_lab, augment=False)
            if val_lab_c:
                val_smi_use, val_lab_use = val_smi_c, val_lab_c
                if val_ext is not None:
                    val_ext_use = np.array([val_ext[g] for g in val_grp_c], dtype=np.float32)
                else:
                    val_ext_use = None
            else:
                val_smi_use, val_lab_use = val_smi, val_lab
                val_ext_use = val_ext

            X_val = tokenizer.encode_batch(val_smi_use, max_length)
            y_val = np.array(val_lab_use, dtype=np.float32)

            # Scale extra features
            if aug_ext is not None:
                scaler = RobustScaler(quantile_range=(5.0, 95.0))
                aug_ext = scaler.fit_transform(aug_ext)
                val_ext_scaled = scaler.transform(val_ext_use)
                test_ext_scaled = scaler.transform(test_extra)
            else:
                val_ext_scaled = test_ext_scaled = None

            # Build tensors
            train_tensors = [torch.from_numpy(X_train).long(),
                           torch.from_numpy(y_train).float().unsqueeze(1)]
            val_tensors = [torch.from_numpy(X_val).long(),
                         torch.from_numpy(y_val).float().unsqueeze(1)]
            if aug_ext is not None:
                train_tensors.append(torch.from_numpy(aug_ext).float())
                val_tensors.append(torch.from_numpy(val_ext_scaled).float())

            train_loader = DataLoader(TensorDataset(*train_tensors), batch_size=batch_size, shuffle=True)
            val_loader = DataLoader(TensorDataset(*val_tensors), batch_size=batch_size*2, shuffle=False)

            # Build and train model
            model = LSTMAttModel(
                vocab_size=tokenizer.vocab_size, max_length=max_length,
                embed_dim=embed_dim, lstm_units=lstm_units,
                tdense_units=tdense_units, dense_depth=dense_depth,
                dropout=dropout, model_type="classification",
                n_extra_features=n_extra,
            ).to(device)

            model = train_model(
                model, train_loader, val_loader, device,
                has_extra=(n_extra > 0),
                lr=lr, weight_decay=weight_decay,
                n_epochs=n_epochs, patience=patience,
                pos_weight=pos_weight_val,
            )

            # Predict test set with TTA
            test_probs = predict_with_tta(
                model, test_smiles, tokenizer, max_length, device,
                extra_features=test_ext_scaled,
                has_extra=(n_extra > 0),
            )

            # Store probs for test molecules
            for i, idx in enumerate(test_idx):
                all_run_probs[run, idx] = test_probs[i]

            logger.info(f"  Fold {fold_idx} Run {run}: done")

    return all_run_probs, mol_fold, tokenizer, max_length


def main():
    os.makedirs("logs", exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    df = pd.read_csv(DATA_PATH)
    y = df["bin_class"].values

    print(f"Paper's SMILES-X: TN=157 FP=24 FN=31 TP=102  F1={PAPER_F1:.4f}")
    print(f"Data: {len(df)} molecules, {y.sum()} class 1\n")

    configs = [
        # (name, extra_cols, embed, lstm, tdense, depth, dropout, lr, wd, bs, epochs, patience, class_wt, aug)
        ("T1: Paper defaults (512/128/128, no extra, no dropout)",
         [], 512, 128, 128, 0, 0.0, 1.26e-4, 0, 16, 100, 25, False, True),
        ("T2: Paper defaults + class weight",
         [], 512, 128, 128, 0, 0.0, 1.26e-4, 0, 16, 100, 25, True, True),
        ("T3: Paper defaults + ha_num/o_num",
         ["ha_num", "o_num"], 512, 128, 128, 0, 0.0, 1.26e-4, 0, 16, 100, 25, False, True),
        ("T4: Our optuna config (32/128/64/d2, ha+o, dropout=0.3)",
         ["ha_num", "o_num"], 32, 128, 64, 2, 0.3, 1.67e-4, 5e-6, 32, 100, 25, True, True),
        ("T5: Paper defaults + patience=5 (Keras default)",
         [], 512, 128, 128, 0, 0.0, 1.26e-4, 0, 16, 100, 5, False, True),
        ("T6: Paper defaults, no augmentation",
         [], 512, 128, 128, 0, 0.0, 1.26e-4, 0, 16, 100, 25, False, False),
        ("T7: Deeper model (512/128/128/d2, no extra)",
         [], 512, 128, 128, 2, 0.0, 1.26e-4, 0, 16, 100, 25, False, True),
        ("T8: Paper defaults + ha_num/o_num + depth=2",
         ["ha_num", "o_num"], 512, 128, 128, 2, 0.0, 1.26e-4, 0, 16, 100, 25, False, True),
    ]

    all_results = []

    for cfg in configs:
        name, extra_cols, embed, lstm, tdense, depth, dropout, lr, wd, bs, epochs, pat, cw, aug = cfg
        print(f"\n{'='*70}")
        print(f"  {name}")
        print(f"{'='*70}")

        run_probs, mol_fold, _, _ = run_full_cv(
            df, "smiles", "bin_class", extra_cols,
            embed, lstm, tdense, depth, dropout,
            lr, wd, bs, epochs, pat,
            n_folds=5, n_runs=3, class_weight=cw, augment=aug,
            device=device, seed=42,
        )

        # Strategy A: Average probs across runs, then threshold
        mean_probs = run_probs.mean(axis=0)

        # Strategy B: Best run per fold (highest val F1)
        # Strategy C: Each run separately

        # Try multiple thresholds
        print(f"\n  Strategy: Average 3 runs, sweep thresholds:")
        for t in [0.30, 0.35, 0.40, 0.45, 0.47, 0.50]:
            preds = (mean_probs >= t).astype(int)
            report(f"  avg_runs threshold={t:.2f}", y, preds, mean_probs)

        # Optimize threshold on all predictions
        best_f1 = 0
        best_t = 0.5
        for t in np.arange(0.1, 0.9, 0.01):
            preds = (mean_probs >= t).astype(int)
            f1 = f1_score(y, preds)
            if f1 > best_f1:
                best_f1 = f1
                best_t = t
        preds = (mean_probs >= best_t).astype(int)
        res = report(f"  avg_runs BEST threshold={best_t:.2f}", y, preds, mean_probs)

        # Per-run results
        print(f"\n  Per-run results (threshold=0.47):")
        for run in range(3):
            preds = (run_probs[run] >= 0.47).astype(int)
            report(f"  run {run} threshold=0.47", y, preds, run_probs[run], verbose=True)

        all_results.append({"name": name, "best_f1": best_f1, "best_t": best_t, **res})

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY — Best F1 per theory")
    print(f"{'='*70}")
    print(f"  Paper target: F1={PAPER_F1:.4f}")
    print()
    for r in all_results:
        gap = PAPER_F1 - r["f1"]
        print(f"  {r['name'][:55]:<55s}  F1={r['f1']:.4f}  gap={gap:+.4f}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
