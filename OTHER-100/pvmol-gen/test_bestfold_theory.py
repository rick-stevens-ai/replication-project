"""Test "best fold/run model predicts all data" hypotheses.

Plausible workflow that produces inflated metrics:
1. Run 5-fold CV (3 runs per fold) to evaluate the model
2. Select the best fold model (or best run overall)
3. Use that model to predict ALL 314 molecules for downstream use
4. Report those predictions as the "cross-validation" results

Also test:
- Val predictions aggregated instead of test predictions
- Best run per fold, aggregated
- Ensemble of all 15 models on full data
"""

import json
import logging
import os
import sys

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import (
    f1_score, roc_auc_score, accuracy_score, precision_score, recall_score,
    confusion_matrix,
)

from smilesx.tokenizer import SmilesTokenizer
from smilesx.augment import augment_smiles
from smilesx.model import LSTMAttModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/bestfold_theory.log"),
    ],
)
logger = logging.getLogger(__name__)

DATA_PATH = "data/T0.csv"
PAPER_CM = (157, 24, 31, 102)  # TN, FP, FN, TP
PAPER_F1 = 2 * 102 / (2 * 102 + 24 + 31)


def report(label, y_true, y_pred, y_prob=None):
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    f1 = f1_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    acc = accuracy_score(y_true, y_pred)
    auc = roc_auc_score(y_true, y_prob) if y_prob is not None else 0

    match = " *** EXACT MATCH ***" if (tn, fp, fn, tp) == PAPER_CM else ""
    close = ""
    if not match and abs(f1 - PAPER_F1) < 0.05:
        close = " (CLOSE to paper)"

    print(
        f"  {label}\n"
        f"    TN={tn} FP={fp} FN={fn} TP={tp} | "
        f"F1={f1:.4f} Prec={prec:.4f} Rec={rec:.4f} Acc={acc:.4f} AUC={auc:.4f}"
        f"{match}{close}"
    )
    return {"tn": tn, "fp": fp, "fn": fn, "tp": tp, "f1": f1, "auc": auc}


def predict_with_tta(model, smiles_list, tokenizer, max_length, device,
                     extra_features=None, extra_scaler=None, n_extra=0, batch_size=64):
    """Predict probabilities with test-time augmentation."""
    model.eval()
    dummy = [0.0] * len(smiles_list)
    aug_smi, aug_lab, aug_grp = augment_smiles(smiles_list, dummy, augment=True)
    X = tokenizer.encode_batch(aug_smi, max_length)

    if n_extra > 0 and extra_features is not None:
        aug_ext = np.array([extra_features[g] for g in aug_grp], dtype=np.float32)
        if extra_scaler is not None:
            aug_ext = extra_scaler.transform(aug_ext)
    else:
        aug_ext = None

    all_probs = []
    with torch.no_grad():
        for i in range(0, len(X), batch_size):
            xb = torch.from_numpy(X[i:i+batch_size]).long().to(device)
            eb = None
            if aug_ext is not None:
                eb = torch.from_numpy(aug_ext[i:i+batch_size]).float().to(device)
            pred = model(xb, extra=eb)
            all_probs.append(pred.cpu().numpy().ravel())

    raw = np.concatenate(all_probs)
    probs = np.zeros(len(smiles_list))
    for i in range(len(smiles_list)):
        mask = [j for j, g in enumerate(aug_grp) if g == i]
        probs[i] = raw[mask].mean() if mask else 0.0
    return probs


def main():
    os.makedirs("logs", exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    df = pd.read_csv(DATA_PATH)
    smiles = df["smiles"].values.tolist()
    y = df["bin_class"].values
    n_extra = 2
    extra_cols = ["ha_num", "o_num"]
    extra_all = df[extra_cols].values.astype(np.float32)
    col_means = np.nanmean(extra_all, axis=0)
    for c in range(n_extra):
        mask = np.isnan(extra_all[:, c])
        extra_all[mask, c] = col_means[c]

    tokenizer = SmilesTokenizer().fit(smiles)
    all_tok = tokenizer.tokenize_batch(smiles)
    max_length = max(len(t) for t in all_tok) + 1

    n_pos = int(y.sum())
    n_neg = len(y) - n_pos
    pos_weight = n_neg / n_pos

    print(f"Paper target: TN=157 FP=24 FN=31 TP=102  F1={PAPER_F1:.4f}")
    print(f"Data: {len(df)} molecules, {n_pos} class 1, {n_neg} class 0\n")

    # ── Train 5 folds × 3 runs, store all models and all predictions ──
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    seeds = [42, 123, 7]

    models_info = []  # (fold, run, model, extra_scaler, val_f1, test_f1, test_probs_on_fold, val_probs, val_indices)

    # Per-molecule: test probs (held-out), val probs, and full-data probs per model
    test_probs_per_run = np.zeros((5, 3, len(smiles)))  # fold, run, molecule (only test molecules filled)
    val_probs_per_run = {}  # (fold, run) -> (val_indices, val_probs, val_labels)
    mol_fold_map = np.full(len(smiles), -1)  # which fold each molecule is test in

    for fold_idx, (train_val_idx, test_idx) in enumerate(skf.split(smiles, y)):
        for i in test_idx:
            mol_fold_map[i] = fold_idx

        tr_smi_raw = [smiles[i] for i in train_val_idx]
        tr_lab_raw = [int(y[i]) for i in train_val_idx]
        te_smi = [smiles[i] for i in test_idx]
        te_lab = y[test_idx]

        tr_ext_raw = extra_all[train_val_idx]
        te_ext = extra_all[test_idx]

        # Train/val split
        tr_smi, val_smi, tr_lab, val_lab, tr_ext, val_ext = train_test_split(
            tr_smi_raw, tr_lab_raw, tr_ext_raw.tolist(),
            test_size=0.2, stratify=tr_lab_raw,
            random_state=42 + fold_idx,
        )
        tr_ext = np.array(tr_ext, dtype=np.float32)
        val_ext = np.array(val_ext, dtype=np.float32)

        for run_idx, seed in enumerate(seeds):
            torch.manual_seed(seed + fold_idx * 100)
            np.random.seed(seed + fold_idx * 100)

            # Augment training
            aug_smi, aug_lab, aug_grp = augment_smiles(tr_smi, tr_lab, augment=True)
            aug_ext = np.array([tr_ext[g] for g in aug_grp], dtype=np.float32)

            # Canonicalize val
            val_smi_c, val_lab_c, val_grp_c = augment_smiles(val_smi, val_lab, augment=False)
            if val_lab_c:
                val_smi_u, val_lab_u = val_smi_c, val_lab_c
                val_ext_u = np.array([val_ext[g] for g in val_grp_c], dtype=np.float32)
            else:
                val_smi_u, val_lab_u = val_smi, val_lab
                val_ext_u = val_ext

            X_tr = tokenizer.encode_batch(aug_smi, max_length)
            y_tr = np.array(aug_lab, dtype=np.float32)
            X_val = tokenizer.encode_batch(val_smi_u, max_length)
            y_val = np.array(val_lab_u, dtype=np.float32)

            # Scale extra
            scaler = RobustScaler(quantile_range=(5.0, 95.0))
            aug_ext_s = scaler.fit_transform(aug_ext)
            val_ext_s = scaler.transform(val_ext_u)

            train_ds = TensorDataset(
                torch.from_numpy(X_tr).long(),
                torch.from_numpy(y_tr).float().unsqueeze(1),
                torch.from_numpy(aug_ext_s).float(),
            )
            val_ds = TensorDataset(
                torch.from_numpy(X_val).long(),
                torch.from_numpy(y_val).float().unsqueeze(1),
                torch.from_numpy(val_ext_s).float(),
            )
            train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
            val_loader = DataLoader(val_ds, batch_size=32, shuffle=False)

            model = LSTMAttModel(
                vocab_size=tokenizer.vocab_size, max_length=max_length,
                embed_dim=512, lstm_units=128, tdense_units=128,
                dense_depth=0, dropout=0.0,
                model_type="classification", n_extra_features=n_extra,
            ).to(device)

            # Train
            optimizer = torch.optim.Adam(model.parameters(), lr=1.26e-4)
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.5, patience=10, min_lr=1e-6)
            criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight], device=device))

            best_val_loss = float("inf")
            best_state = None
            no_improve = 0
            for epoch in range(100):
                model.train()
                for batch in train_loader:
                    xb, yb, eb = batch[0].to(device), batch[1].to(device), batch[2].to(device)
                    optimizer.zero_grad()
                    model.model_type = "regression"
                    out = model(xb, extra=eb)
                    model.model_type = "classification"
                    loss = criterion(out, yb)
                    loss.backward()
                    nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    optimizer.step()

                model.eval()
                vl = 0; n = 0
                with torch.no_grad():
                    for batch in val_loader:
                        xb, yb, eb = batch[0].to(device), batch[1].to(device), batch[2].to(device)
                        model.model_type = "regression"
                        out = model(xb, extra=eb)
                        model.model_type = "classification"
                        vl += criterion(out, yb).item(); n += 1
                vl /= max(n, 1)
                scheduler.step(vl)
                if vl < best_val_loss:
                    best_val_loss = vl
                    best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
                    no_improve = 0
                else:
                    no_improve += 1
                if no_improve >= 25:
                    break

            model.load_state_dict(best_state)
            model.to(device)

            # Predict test set (held-out) with TTA
            te_probs = predict_with_tta(model, te_smi, tokenizer, max_length, device,
                                        extra_features=te_ext, extra_scaler=scaler, n_extra=n_extra)
            for i, idx in enumerate(test_idx):
                test_probs_per_run[fold_idx, run_idx, idx] = te_probs[i]

            # Predict val set
            val_probs = predict_with_tta(model, val_smi, tokenizer, max_length, device,
                                         extra_features=val_ext, extra_scaler=scaler, n_extra=n_extra)

            # Compute val F1 at threshold 0.47
            val_f1 = f1_score(val_lab, (val_probs >= 0.47).astype(int))
            te_f1 = f1_score(te_lab, (te_probs >= 0.47).astype(int))

            # Predict ALL data with this model
            all_probs = predict_with_tta(model, smiles, tokenizer, max_length, device,
                                         extra_features=extra_all, extra_scaler=scaler, n_extra=n_extra)

            models_info.append({
                "fold": fold_idx, "run": run_idx,
                "val_f1": val_f1, "test_f1": te_f1,
                "all_probs": all_probs,
                "val_probs": val_probs, "val_labels": val_lab,
            })

            logger.info(f"  Fold {fold_idx} Run {run_idx}: val_F1={val_f1:.4f} test_F1={te_f1:.4f}")

    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("THEORY A: Normal aggregated 5-fold CV (ground truth)")
    print("=" * 70)
    for run_idx in range(3):
        probs = test_probs_per_run[:, run_idx, :].max(axis=0)  # each mol only in 1 fold
        # Actually need to pick the right fold for each molecule
        agg_probs = np.zeros(len(smiles))
        for i in range(len(smiles)):
            fold = mol_fold_map[i]
            agg_probs[i] = test_probs_per_run[fold, run_idx, i]
        preds = (agg_probs >= 0.47).astype(int)
        report(f"A: aggregated CV, run {run_idx}, threshold=0.47", y, preds, agg_probs)

    # Average across 3 runs
    agg_avg = np.zeros(len(smiles))
    for i in range(len(smiles)):
        fold = mol_fold_map[i]
        agg_avg[i] = test_probs_per_run[fold, :, i].mean()
    for t in [0.40, 0.45, 0.47, 0.50]:
        report(f"A: aggregated CV, avg 3 runs, threshold={t:.2f}", y, (agg_avg >= t).astype(int), agg_avg)

    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("THEORY B: Best fold model → predict ALL 314 molecules")
    print("=" * 70)

    # Sort by val_f1
    by_val = sorted(models_info, key=lambda x: x["val_f1"], reverse=True)
    for i, m in enumerate(by_val[:5]):
        print(f"\n  Model rank {i+1}: Fold {m['fold']} Run {m['run']} "
              f"val_F1={m['val_f1']:.4f} test_F1={m['test_f1']:.4f}")
        for t in [0.40, 0.45, 0.47, 0.50]:
            preds = (m["all_probs"] >= t).astype(int)
            report(f"B: best_val model → all data, threshold={t:.2f}", y, preds, m["all_probs"])

    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("THEORY C: Best test F1 model → predict ALL 314 molecules")
    print("=" * 70)

    by_test = sorted(models_info, key=lambda x: x["test_f1"], reverse=True)
    for i, m in enumerate(by_test[:3]):
        print(f"\n  Model rank {i+1}: Fold {m['fold']} Run {m['run']} "
              f"val_F1={m['val_f1']:.4f} test_F1={m['test_f1']:.4f}")
        for t in [0.40, 0.45, 0.47, 0.50]:
            preds = (m["all_probs"] >= t).astype(int)
            report(f"C: best_test model → all data, threshold={t:.2f}", y, preds, m["all_probs"])

    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("THEORY D: Ensemble all 15 models → predict ALL 314 molecules")
    print("=" * 70)

    all_model_probs = np.array([m["all_probs"] for m in models_info])
    ens_probs = all_model_probs.mean(axis=0)
    for t in [0.30, 0.35, 0.40, 0.45, 0.47, 0.50]:
        preds = (ens_probs >= t).astype(int)
        report(f"D: ensemble 15 models → all data, threshold={t:.2f}", y, preds, ens_probs)

    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("THEORY E: Best model per fold → predict all, aggregate by fold")
    print("  (Each fold's best run predicts all data; use that fold's test")
    print("   predictions only)")
    print("=" * 70)

    # For each fold, pick the run with best val_f1, use its test predictions
    best_per_fold_probs = np.zeros(len(smiles))
    for fold_idx in range(5):
        fold_models = [m for m in models_info if m["fold"] == fold_idx]
        best_run = max(fold_models, key=lambda x: x["val_f1"])
        test_idx_mask = mol_fold_map == fold_idx
        # Use this model's predictions for this fold's test molecules
        best_per_fold_probs[test_idx_mask] = best_run["all_probs"][test_idx_mask]
        print(f"  Fold {fold_idx}: best run {best_run['run']} (val_F1={best_run['val_f1']:.4f})")

    for t in [0.40, 0.45, 0.47, 0.50]:
        preds = (best_per_fold_probs >= t).astype(int)
        report(f"E: best run per fold (test only), threshold={t:.2f}", y, preds, best_per_fold_probs)

    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("THEORY F: Val predictions aggregated (not test predictions)")
    print("  Report val metrics instead of test metrics")
    print("=" * 70)
    # Average val F1 across folds/runs
    val_f1s = [m["val_f1"] for m in models_info]
    print(f"  Mean val F1 (threshold=0.47): {np.mean(val_f1s):.4f} ± {np.std(val_f1s):.4f}")
    print(f"  Max val F1: {max(val_f1s):.4f}")
    print(f"  Per fold-run val F1s:")
    for m in models_info:
        print(f"    Fold {m['fold']} Run {m['run']}: val_F1={m['val_f1']:.4f}")

    # ══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("THEORY G: Best fold model → predict all, optimize threshold on all")
    print("=" * 70)
    best_model = by_val[0]
    probs = best_model["all_probs"]
    best_f1 = 0
    best_t = 0.5
    for t in np.arange(0.1, 0.9, 0.01):
        f1 = f1_score(y, (probs >= t).astype(int))
        if f1 > best_f1:
            best_f1 = f1
            best_t = t
    preds = (probs >= best_t).astype(int)
    report(f"G: best_val model, optimal threshold={best_t:.2f}", y, preds, probs)


if __name__ == "__main__":
    main()
