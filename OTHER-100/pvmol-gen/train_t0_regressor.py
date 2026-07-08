"""SMILES-X regressor for continuous norm_dpce prediction on T0 data.

5-fold and 10-fold CV with enriched RDKit descriptors.
Reports R², MAE, RMSE, and Spearman correlation.
"""

import json
import logging
import os
import sys
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
from scipy.stats import spearmanr
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import RobustScaler
from torch.utils.data import DataLoader, TensorDataset

from smilesx.tokenizer import SmilesTokenizer
from smilesx.augment import augment_smiles
from smilesx.model import LSTMAttModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/train_t0_regressor.log"),
    ],
)
logger = logging.getLogger(__name__)

DESCRIPTOR_FUNCS = {
    "molwt": Descriptors.MolWt,
    "logp": Descriptors.MolLogP,
    "tpsa": Descriptors.TPSA,
    "hbd": rdMolDescriptors.CalcNumHBD,
    "hba": rdMolDescriptors.CalcNumHBA,
    "rot_bonds": rdMolDescriptors.CalcNumRotatableBonds,
    "ring_count": rdMolDescriptors.CalcNumRings,
    "aromatic_rings": rdMolDescriptors.CalcNumAromaticRings,
    "frac_csp3": rdMolDescriptors.CalcFractionCSP3,
    "num_heteroatoms": rdMolDescriptors.CalcNumHeteroatoms,
}


def compute_descriptors(df):
    df = df.copy()
    for name, func in DESCRIPTOR_FUNCS.items():
        df[name] = [func(m) if (m := Chem.MolFromSmiles(s)) else np.nan for s in df["smiles"]]
    return df


@dataclass
class FoldResult:
    fold: int
    r2: float
    mae: float
    rmse: float
    spearman: float
    spearman_p: float
    train_losses: List[float] = field(default_factory=list)
    val_losses: List[float] = field(default_factory=list)


@dataclass
class CVResult:
    folds: List[FoldResult]
    target_col: str

    @property
    def mean_r2(self): return np.mean([f.r2 for f in self.folds])
    @property
    def std_r2(self): return np.std([f.r2 for f in self.folds])
    @property
    def mean_mae(self): return np.mean([f.mae for f in self.folds])
    @property
    def std_mae(self): return np.std([f.mae for f in self.folds])
    @property
    def mean_rmse(self): return np.mean([f.rmse for f in self.folds])
    @property
    def mean_spearman(self): return np.mean([f.spearman for f in self.folds])

    def summary(self) -> str:
        lines = ["=" * 70, f"SMILES-X Regressor — {self.target_col} — CV Results", "=" * 70]
        for f in self.folds:
            lines.append(
                f"  Fold {f.fold:2d}: R²={f.r2:.4f}  MAE={f.mae:.4f}  "
                f"RMSE={f.rmse:.4f}  Spearman={f.spearman:.4f}"
            )
        lines.append("-" * 70)
        lines.append(
            f"  Mean:   R²={self.mean_r2:.4f}±{self.std_r2:.4f}  "
            f"MAE={self.mean_mae:.4f}±{self.std_mae:.4f}  "
            f"RMSE={self.mean_rmse:.4f}  Spearman={self.mean_spearman:.4f}"
        )
        lines.append("=" * 70)
        return "\n".join(lines)


def train_fold(
    model, X_train, y_train, X_val, y_val,
    extra_train, extra_val,
    device, batch_size, lr, weight_decay, n_epochs, patience,
):
    """Train one fold, return best model state and loss histories."""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.5, patience=10, min_lr=1e-6,
    )
    criterion = nn.MSELoss()

    has_extra = extra_train is not None

    train_tensors = [torch.from_numpy(X_train).long(), torch.from_numpy(y_train).float().unsqueeze(1)]
    val_tensors = [torch.from_numpy(X_val).long(), torch.from_numpy(y_val).float().unsqueeze(1)]
    if has_extra:
        train_tensors.append(torch.from_numpy(extra_train).float())
        val_tensors.append(torch.from_numpy(extra_val).float())

    train_loader = DataLoader(TensorDataset(*train_tensors), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(TensorDataset(*val_tensors), batch_size=batch_size * 2, shuffle=False)

    best_val_loss = float("inf")
    best_state = None
    epochs_no_improve = 0
    train_losses, val_losses = [], []

    for epoch in range(n_epochs):
        model.train()
        epoch_loss, n_batches = 0.0, 0
        for batch in train_loader:
            xb, yb = batch[0].to(device), batch[1].to(device)
            eb = batch[2].to(device) if has_extra else None
            optimizer.zero_grad()
            pred = model(xb, extra=eb)
            loss = criterion(pred, yb)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            epoch_loss += loss.item()
            n_batches += 1
        train_loss = epoch_loss / max(n_batches, 1)
        train_losses.append(train_loss)

        model.eval()
        val_loss, n_val = 0.0, 0
        with torch.no_grad():
            for batch in val_loader:
                xb, yb = batch[0].to(device), batch[1].to(device)
                eb = batch[2].to(device) if has_extra else None
                pred = model(xb, extra=eb)
                val_loss += criterion(pred, yb).item()
                n_val += 1
        val_loss /= max(n_val, 1)
        val_losses.append(val_loss)

        scheduler.step(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1

        if (epoch + 1) % 10 == 0 or epoch == 0:
            cur_lr = optimizer.param_groups[0]["lr"]
            logger.info(
                f"    Epoch {epoch+1:3d}: train={train_loss:.6f}  val={val_loss:.6f}  "
                f"best={best_val_loss:.6f}  lr={cur_lr:.2e}"
            )

        if epochs_no_improve >= patience:
            logger.info(f"    Early stopping at epoch {epoch+1}")
            break

    if best_state:
        model.load_state_dict(best_state)
        model.to(device)

    return train_losses, val_losses


def evaluate_with_tta(model, test_smiles, test_labels, test_extra, tokenizer, max_length, device, batch_size, has_extra, target_scaler):
    """Evaluate with test-time augmentation, return predictions in original scale."""
    model.eval()

    aug_smiles, aug_labels, aug_groups = augment_smiles(test_smiles, test_labels, augment=True)
    X_test_aug = tokenizer.encode_batch(aug_smiles, max_length)

    if has_extra and test_extra is not None:
        aug_extra = np.array([test_extra[g] for g in aug_groups], dtype=np.float32)
    else:
        aug_extra = None

    test_tensors = [torch.from_numpy(X_test_aug).long()]
    if aug_extra is not None:
        test_tensors.append(torch.from_numpy(aug_extra).float())
    # Dummy labels for DataLoader
    test_tensors.insert(1, torch.zeros(len(X_test_aug), 1))

    test_loader = DataLoader(TensorDataset(*test_tensors), batch_size=batch_size * 2, shuffle=False)

    all_preds = []
    with torch.no_grad():
        for batch in test_loader:
            xb = batch[0].to(device)
            eb = batch[2].to(device) if has_extra and aug_extra is not None else None
            pred = model(xb, extra=eb)
            all_preds.append(pred.cpu().numpy().ravel())

    raw_preds = np.concatenate(all_preds)

    # Average per original molecule
    n_test = len(test_smiles)
    preds = np.zeros(n_test)
    for i in range(n_test):
        mask = [j for j, g in enumerate(aug_groups) if g == i]
        preds[i] = raw_preds[mask].mean() if mask else 0.0

    # Inverse-transform to original scale
    preds_orig = target_scaler.inverse_transform(preds.reshape(-1, 1)).ravel()
    true_orig = target_scaler.inverse_transform(np.array(test_labels).reshape(-1, 1)).ravel()

    return true_orig, preds_orig


def run_cv(df, target_col, extra_cols, n_folds, outdir, device, seed=42):
    """Run k-fold CV regression."""
    os.makedirs(outdir, exist_ok=True)
    torch.manual_seed(seed)
    np.random.seed(seed)

    smiles = df["smiles"].values.tolist()
    targets = df[target_col].values.astype(np.float32)

    n_extra = len(extra_cols)
    extra_features = None
    if n_extra > 0:
        extra_features = df[extra_cols].values.astype(np.float32)
        col_means = np.nanmean(extra_features, axis=0)
        for c in range(n_extra):
            mask = np.isnan(extra_features[:, c])
            extra_features[mask, c] = col_means[c]

    tokenizer = SmilesTokenizer().fit(smiles)
    all_tokenized = tokenizer.tokenize_batch(smiles)
    max_length = max(len(t) for t in all_tokenized) + 1

    logger.info(f"Target: {target_col}, Vocab: {tokenizer.vocab_size}, Max len: {max_length}")
    logger.info(f"Extra features ({n_extra}): {extra_cols}")

    kf = KFold(n_splits=n_folds, shuffle=True, random_state=seed)
    fold_results = []

    for fold_idx, (train_val_idx, test_idx) in enumerate(kf.split(smiles)):
        logger.info(f"\n{'='*40} Fold {fold_idx} {'='*40}")

        train_smiles_raw = [smiles[i] for i in train_val_idx]
        train_targets_raw = targets[train_val_idx]
        test_smiles = [smiles[i] for i in test_idx]
        test_targets = targets[test_idx]

        train_extra_raw = extra_features[train_val_idx] if extra_features is not None else None
        test_extra = extra_features[test_idx] if extra_features is not None else None

        # Train/val split
        if train_extra_raw is not None:
            (train_smiles, val_smiles, train_targets_split, val_targets,
             train_extra, val_extra) = train_test_split(
                train_smiles_raw, train_targets_raw, train_extra_raw,
                test_size=0.2, random_state=seed + fold_idx,
            )
        else:
            train_smiles, val_smiles, train_targets_split, val_targets = train_test_split(
                train_smiles_raw, train_targets_raw,
                test_size=0.2, random_state=seed + fold_idx,
            )
            train_extra = val_extra = test_extra = None

        # Scale target values (fit on training only)
        target_scaler = RobustScaler(quantile_range=(5.0, 95.0))
        train_targets_scaled = target_scaler.fit_transform(train_targets_split.reshape(-1, 1)).ravel()
        val_targets_scaled = target_scaler.transform(val_targets.reshape(-1, 1)).ravel()
        test_targets_scaled = target_scaler.transform(test_targets.reshape(-1, 1)).ravel()

        # Augment training
        aug_smiles, aug_labels, aug_groups = augment_smiles(
            train_smiles, train_targets_scaled.tolist(), augment=True,
        )
        logger.info(f"  Training: {len(train_smiles)} → {len(aug_smiles)} (augmented)")

        # Replicate extra features
        if train_extra is not None:
            aug_extra = np.array([train_extra[g] for g in aug_groups], dtype=np.float32)
        else:
            aug_extra = None

        # Canonicalize val (no augmentation)
        val_smiles_clean, val_labels_clean, val_groups = augment_smiles(
            val_smiles, val_targets_scaled.tolist(), augment=False,
        )
        if val_labels_clean:
            val_smiles, val_targets_scaled = val_smiles_clean, np.array(val_labels_clean, dtype=np.float32)
            if val_extra is not None:
                val_extra = np.array([val_extra[g] for g in val_groups], dtype=np.float32)

        # Encode
        X_train = tokenizer.encode_batch(aug_smiles, max_length)
        y_train = np.array(aug_labels, dtype=np.float32)
        X_val = tokenizer.encode_batch(val_smiles, max_length)
        y_val = val_targets_scaled if isinstance(val_targets_scaled, np.ndarray) else np.array(val_targets_scaled, dtype=np.float32)

        # Scale extra features
        if aug_extra is not None:
            extra_scaler = RobustScaler(quantile_range=(5.0, 95.0))
            aug_extra = extra_scaler.fit_transform(aug_extra)
            val_extra = extra_scaler.transform(val_extra)
            test_extra = extra_scaler.transform(test_extra)

        # Build model
        model = LSTMAttModel(
            vocab_size=tokenizer.vocab_size,
            max_length=max_length,
            embed_dim=32,
            lstm_units=128,
            tdense_units=64,
            dense_depth=2,
            dropout=0.3,
            model_type="regression",
            n_extra_features=n_extra,
        ).to(device)

        # Train
        train_losses, val_losses = train_fold(
            model, X_train, y_train, X_val, y_val,
            aug_extra, val_extra,
            device, batch_size=32, lr=1.67e-4, weight_decay=5e-6,
            n_epochs=100, patience=25,
        )

        # Evaluate with TTA
        true_orig, preds_orig = evaluate_with_tta(
            model, test_smiles, test_targets_scaled.tolist(), test_extra,
            tokenizer, max_length, device, batch_size=32,
            has_extra=(n_extra > 0), target_scaler=target_scaler,
        )

        # Metrics in original scale
        r2 = r2_score(true_orig, preds_orig)
        mae = mean_absolute_error(true_orig, preds_orig)
        rmse = np.sqrt(mean_squared_error(true_orig, preds_orig))
        sp_corr, sp_p = spearmanr(true_orig, preds_orig)

        logger.info(
            f"  Fold {fold_idx} test: R²={r2:.4f}  MAE={mae:.4f}  "
            f"RMSE={rmse:.4f}  Spearman={sp_corr:.4f} (p={sp_p:.2e})"
        )

        fold_results.append(FoldResult(
            fold=fold_idx, r2=r2, mae=mae, rmse=rmse,
            spearman=sp_corr, spearman_p=sp_p,
            train_losses=train_losses, val_losses=val_losses,
        ))

        # Save model
        torch.save(model.state_dict(), os.path.join(outdir, f"model_fold_{fold_idx}.pt"))
        if fold_idx == 0:
            tokenizer.save(os.path.join(outdir, "vocab.txt"))

    result = CVResult(folds=fold_results, target_col=target_col)
    logger.info(f"\n{result.summary()}")

    with open(os.path.join(outdir, "cv_results.json"), "w") as f:
        json.dump({
            "target": target_col,
            "n_folds": n_folds,
            "mean_r2": result.mean_r2,
            "std_r2": result.std_r2,
            "mean_mae": result.mean_mae,
            "std_mae": result.std_mae,
            "mean_rmse": result.mean_rmse,
            "mean_spearman": result.mean_spearman,
            "folds": [
                {"fold": f.fold, "r2": f.r2, "mae": f.mae, "rmse": f.rmse,
                 "spearman": f.spearman, "spearman_p": f.spearman_p}
                for f in fold_results
            ],
        }, f, indent=2)

    return result


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    os.makedirs("logs", exist_ok=True)

    df = pd.read_csv("data/T0.csv")
    df = compute_descriptors(df)
    extra_cols = ["ha_num", "o_num"] + list(DESCRIPTOR_FUNCS.keys())

    # Run on both targets with 5-fold CV
    for target in ["norm_dpce", "delta_pce"]:
        logger.info(f"\n{'#'*70}")
        logger.info(f"# TARGET: {target}")
        logger.info(f"{'#'*70}")
        outdir = f"models/t0_regressor_{target}"
        run_cv(df, target, extra_cols, n_folds=5, outdir=outdir, device=device)
