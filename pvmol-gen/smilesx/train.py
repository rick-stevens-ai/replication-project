"""Training pipeline — 5-fold cross-validation with augmentation.

Reimplements the SMILES-X training loop (main.py) in PyTorch.
"""

import os
import json
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    f1_score, roc_auc_score, accuracy_score, precision_score, recall_score,
    precision_recall_curve, auc,
)
from sklearn.model_selection import train_test_split

from .tokenizer import SmilesTokenizer
from .augment import augment_smiles
from .model import LSTMAttModel

logger = logging.getLogger(__name__)


@dataclass
class FoldResult:
    fold: int
    f1: float
    auc_roc: float
    auc_pr: float
    accuracy: float
    precision: float
    recall: float
    threshold: float
    train_loss_history: List[float] = field(default_factory=list)
    val_loss_history: List[float] = field(default_factory=list)


@dataclass
class CVResult:
    folds: List[FoldResult]

    @property
    def mean_f1(self) -> float:
        return np.mean([f.f1 for f in self.folds])

    @property
    def std_f1(self) -> float:
        return np.std([f.f1 for f in self.folds])

    @property
    def mean_auc(self) -> float:
        return np.mean([f.auc_roc for f in self.folds])

    @property
    def std_auc(self) -> float:
        return np.std([f.auc_roc for f in self.folds])

    def summary(self) -> str:
        lines = ["=" * 60, "SMILES-X PyTorch — Cross-Validation Results", "=" * 60]
        for f in self.folds:
            lines.append(
                f"  Fold {f.fold}: F1={f.f1:.4f}  AUC-ROC={f.auc_roc:.4f}  "
                f"AUC-PR={f.auc_pr:.4f}  Acc={f.accuracy:.4f}  "
                f"Thresh={f.threshold:.3f}"
            )
        lines.append("-" * 60)
        lines.append(
            f"  Mean:  F1={self.mean_f1:.4f}±{self.std_f1:.4f}  "
            f"AUC-ROC={self.mean_auc:.4f}±{self.std_auc:.4f}"
        )
        lines.append("=" * 60)
        return "\n".join(lines)


class SmilesXClassifier:
    """High-level interface for training a SMILES-X binary classifier."""

    def __init__(
        self,
        # Data
        data_path: Optional[str] = None,
        smiles_col: str = "SMILES",
        label_col: str = "class",
        extra_feature_cols: Optional[List[str]] = None,
        data: Optional[pd.DataFrame] = None,
        # Architecture
        embed_dim: int = 512,
        lstm_units: int = 128,
        tdense_units: int = 128,
        dense_depth: int = 0,
        dropout: float = 0.3,
        # Training
        lr: float = 1e-4,
        weight_decay: float = 1e-4,
        batch_size: int = 16,
        n_epochs: int = 100,
        patience: int = 25,
        class_weight: bool = True,
        # Output
        outdir: str = "./outputs",
        device: Optional[str] = None,
        seed: int = 42,
    ):
        if data is not None:
            self.df = data
        elif data_path is not None:
            ext = os.path.splitext(data_path)[1].lower()
            if ext in (".xls", ".xlsx"):
                self.df = pd.read_excel(data_path)
            else:
                self.df = pd.read_csv(data_path)
        else:
            raise ValueError("Provide data_path or data")

        self.smiles_col = smiles_col
        self.label_col = label_col
        self.extra_feature_cols = extra_feature_cols or []
        self.class_weight = class_weight
        self.embed_dim = embed_dim
        self.lstm_units = lstm_units
        self.tdense_units = tdense_units
        self.dense_depth = dense_depth
        self.dropout = dropout
        self.lr = lr
        self.weight_decay = weight_decay
        self.batch_size = batch_size
        self.n_epochs = n_epochs
        self.patience = patience
        self.outdir = outdir
        self.seed = seed

        if device:
            self.device = torch.device(device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        os.makedirs(outdir, exist_ok=True)

    def cross_validate(
        self,
        n_folds: int = 5,
        augment: bool = True,
        threshold: Optional[float] = None,
    ) -> CVResult:
        """Run stratified k-fold cross-validation.

        Parameters
        ----------
        n_folds : int
            Number of CV folds.
        augment : bool
            Whether to augment training SMILES via atom-rotation enumeration.
        threshold : float, optional
            Classification threshold. If None, optimize on validation set.

        Returns
        -------
        CVResult with per-fold and aggregate metrics.
        """
        torch.manual_seed(self.seed)
        np.random.seed(self.seed)

        smiles = self.df[self.smiles_col].values.tolist()
        labels = self.df[self.label_col].values.astype(int).tolist()

        # Extract extra features if configured
        extra_features = None
        n_extra = len(self.extra_feature_cols)
        if n_extra > 0:
            extra_features = self.df[self.extra_feature_cols].values.astype(np.float32)
            # Fill NaN with column means
            col_means = np.nanmean(extra_features, axis=0)
            for c in range(n_extra):
                mask = np.isnan(extra_features[:, c])
                extra_features[mask, c] = col_means[c]
            logger.info(f"Extra features: {self.extra_feature_cols}")

        # Fit tokenizer on full dataset (vocabulary needs all tokens)
        tokenizer = SmilesTokenizer().fit(smiles)
        logger.info(f"Vocabulary size: {tokenizer.vocab_size}")

        # Compute max length from full dataset
        all_tokenized = tokenizer.tokenize_batch(smiles)
        max_length = max(len(t) for t in all_tokenized) + 1  # +1 for safety

        # Compute class weight for BCE if requested
        pos_weight_val = None
        if self.class_weight:
            n_pos = sum(labels)
            n_neg = len(labels) - n_pos
            if n_pos > 0 and n_neg > 0:
                pos_weight_val = n_neg / n_pos
                logger.info(f"Class weighting: pos_weight={pos_weight_val:.3f} (neg={n_neg}, pos={n_pos})")

        skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=self.seed)
        fold_results = []

        for fold_idx, (train_val_idx, test_idx) in enumerate(skf.split(smiles, labels)):
            logger.info(f"\n{'='*40} Fold {fold_idx} {'='*40}")

            # Split into train/val (80/20 of train_val, stratified) and test
            train_smiles_raw = [smiles[i] for i in train_val_idx]
            train_labels_raw = [labels[i] for i in train_val_idx]
            test_smiles = [smiles[i] for i in test_idx]
            test_labels = [labels[i] for i in test_idx]

            # Extra features per split
            train_extra_raw = extra_features[train_val_idx] if extra_features is not None else None
            test_extra = extra_features[test_idx] if extra_features is not None else None

            # Stratified train/val split
            if train_extra_raw is not None:
                train_smiles, val_smiles, train_labels, val_labels, train_extra, val_extra = train_test_split(
                    train_smiles_raw, train_labels_raw, train_extra_raw.tolist(),
                    test_size=0.2, stratify=train_labels_raw, random_state=self.seed + fold_idx,
                )
                train_extra = np.array(train_extra, dtype=np.float32)
                val_extra = np.array(val_extra, dtype=np.float32)
            else:
                train_smiles, val_smiles, train_labels, val_labels = train_test_split(
                    train_smiles_raw, train_labels_raw,
                    test_size=0.2, stratify=train_labels_raw, random_state=self.seed + fold_idx,
                )
                train_extra = val_extra = test_extra = None

            # Augment training data (enumerate atom rotations)
            if augment:
                aug_smiles, aug_labels, aug_groups = augment_smiles(
                    train_smiles, train_labels, augment=True
                )
                logger.info(
                    f"  Training: {len(train_smiles)} → {len(aug_smiles)} (augmented)"
                )
            else:
                aug_smiles, aug_labels, aug_groups = augment_smiles(
                    train_smiles, train_labels, augment=False
                )

            # Replicate extra features for augmented SMILES
            if train_extra is not None:
                aug_extra = np.array([train_extra[g] for g in aug_groups], dtype=np.float32)
            else:
                aug_extra = None

            # Canonicalize val set (no enumeration, just RDKit validation)
            val_smiles_clean, val_labels_clean, val_groups_clean = augment_smiles(
                val_smiles, val_labels, augment=False
            )
            if val_labels_clean:
                val_smiles, val_labels = val_smiles_clean, val_labels_clean
                if val_extra is not None:
                    val_extra = np.array([val_extra[g] for g in val_groups_clean], dtype=np.float32)

            # Encode
            X_train = tokenizer.encode_batch(aug_smiles, max_length)
            y_train = np.array(aug_labels, dtype=np.float32)
            X_val = tokenizer.encode_batch(val_smiles, max_length)
            y_val = np.array(val_labels, dtype=np.float32)
            X_test = tokenizer.encode_batch(test_smiles, max_length)
            y_test = np.array(test_labels, dtype=np.float32)

            # Normalize extra features (fit on train, apply to val/test)
            if aug_extra is not None:
                extra_mean = aug_extra.mean(axis=0)
                extra_std = aug_extra.std(axis=0) + 1e-8
                aug_extra = (aug_extra - extra_mean) / extra_std
                val_extra = (val_extra - extra_mean) / extra_std
                test_extra = (test_extra - extra_mean) / extra_std

            # Build model
            model = LSTMAttModel(
                vocab_size=tokenizer.vocab_size,
                max_length=max_length,
                embed_dim=self.embed_dim,
                lstm_units=self.lstm_units,
                tdense_units=self.tdense_units,
                dense_depth=self.dense_depth,
                dropout=self.dropout,
                model_type="classification",
                n_extra_features=n_extra,
            ).to(self.device)

            # Store context for TTA in _train_fold
            self._current_test_smiles = test_smiles
            self._current_test_labels = test_labels
            self._current_tokenizer = tokenizer
            self._current_max_length = max_length

            # Train
            fold_result = self._train_fold(
                model, X_train, y_train, X_val, y_val, X_test, y_test,
                fold_idx, threshold,
                extra_train=aug_extra, extra_val=val_extra, extra_test=test_extra,
                pos_weight=pos_weight_val,
            )
            fold_results.append(fold_result)

            # Save model
            model_path = os.path.join(self.outdir, f"model_fold_{fold_idx}.pt")
            torch.save(model.state_dict(), model_path)

            # Save tokenizer (once)
            if fold_idx == 0:
                tokenizer.save(os.path.join(self.outdir, "vocab.txt"))

        result = CVResult(folds=fold_results)
        logger.info(f"\n{result.summary()}")

        # Save results
        results_path = os.path.join(self.outdir, "cv_results.json")
        with open(results_path, "w") as f:
            json.dump(
                {
                    "mean_f1": result.mean_f1,
                    "std_f1": result.std_f1,
                    "mean_auc_roc": result.mean_auc,
                    "std_auc_roc": result.std_auc,
                    "folds": [
                        {
                            "fold": fr.fold,
                            "f1": fr.f1,
                            "auc_roc": fr.auc_roc,
                            "auc_pr": fr.auc_pr,
                            "accuracy": fr.accuracy,
                            "threshold": fr.threshold,
                        }
                        for fr in fold_results
                    ],
                },
                f,
                indent=2,
            )

        return result

    def _train_fold(
        self,
        model: LSTMAttModel,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        fold_idx: int,
        threshold: Optional[float],
        extra_train: Optional[np.ndarray] = None,
        extra_val: Optional[np.ndarray] = None,
        extra_test: Optional[np.ndarray] = None,
        pos_weight: Optional[float] = None,
    ) -> FoldResult:
        """Train one fold, return metrics on test set."""

        optimizer = torch.optim.Adam(model.parameters(), lr=self.lr, weight_decay=self.weight_decay)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=10, min_lr=1e-6,
        )

        # Loss: BCEWithLogitsLoss with class weighting if requested
        # We use BCELoss since model outputs sigmoid already, but apply per-sample weighting
        if pos_weight is not None:
            # Use BCEWithLogitsLoss for numerical stability + pos_weight
            criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight], device=self.device))
            use_logits = True
        else:
            criterion = nn.BCELoss()
            use_logits = False

        # DataLoaders — include extra features if present
        train_tensors = [
            torch.from_numpy(X_train).long(),
            torch.from_numpy(y_train).float().unsqueeze(1),
        ]
        val_tensors = [
            torch.from_numpy(X_val).long(),
            torch.from_numpy(y_val).float().unsqueeze(1),
        ]
        if extra_train is not None:
            train_tensors.append(torch.from_numpy(extra_train).float())
            val_tensors.append(torch.from_numpy(extra_val).float())

        train_ds = TensorDataset(*train_tensors)
        val_ds = TensorDataset(*val_tensors)
        train_loader = DataLoader(train_ds, batch_size=self.batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=self.batch_size * 2, shuffle=False)

        has_extra = extra_train is not None

        best_val_loss = float("inf")
        best_state = None
        epochs_no_improve = 0
        train_losses = []
        val_losses = []

        for epoch in range(self.n_epochs):
            # Train
            model.train()
            epoch_loss = 0.0
            n_batches = 0
            for batch in train_loader:
                xb, yb = batch[0].to(self.device), batch[1].to(self.device)
                eb = batch[2].to(self.device) if has_extra else None
                optimizer.zero_grad()
                if use_logits:
                    # Temporarily bypass sigmoid for BCEWithLogitsLoss
                    model.model_type = "regression"
                    logits = model(xb, extra=eb)
                    model.model_type = "classification"
                    loss = criterion(logits, yb)
                else:
                    pred = model(xb, extra=eb)
                    loss = criterion(pred, yb)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                epoch_loss += loss.item()
                n_batches += 1
            train_loss = epoch_loss / max(n_batches, 1)
            train_losses.append(train_loss)

            # Validate
            model.eval()
            val_loss = 0.0
            n_val = 0
            with torch.no_grad():
                for batch in val_loader:
                    xb, yb = batch[0].to(self.device), batch[1].to(self.device)
                    eb = batch[2].to(self.device) if has_extra else None
                    if use_logits:
                        model.model_type = "regression"
                        logits = model(xb, extra=eb)
                        model.model_type = "classification"
                        val_loss += criterion(logits, yb).item()
                    else:
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
                cur_lr = optimizer.param_groups[0]['lr']
                logger.info(
                    f"  Epoch {epoch+1:3d}: train_loss={train_loss:.4f}  "
                    f"val_loss={val_loss:.4f}  best={best_val_loss:.4f}  lr={cur_lr:.2e}"
                )

            if epochs_no_improve >= self.patience:
                logger.info(f"  Early stopping at epoch {epoch+1}")
                break

        # Restore best model
        if best_state is not None:
            model.load_state_dict(best_state)
            model.to(self.device)

        # Evaluate on test set with test-time augmentation (TTA)
        # Average predictions over augmented SMILES variants per molecule
        # This matches the original SMILES-X evaluation protocol
        model.eval()

        # Get original test SMILES for TTA
        test_smiles_for_tta = self._current_test_smiles if hasattr(self, '_current_test_smiles') else None

        if test_smiles_for_tta is not None:
            # Augment test SMILES
            test_labels_for_tta = self._current_test_labels if hasattr(self, '_current_test_labels') else y_test.tolist()
            aug_test_smiles, aug_test_labels, aug_test_groups = augment_smiles(
                test_smiles_for_tta, test_labels_for_tta,
                augment=True,
            )
            X_test_aug = self._current_tokenizer.encode_batch(aug_test_smiles, self._current_max_length)
            if extra_test is not None:
                aug_test_extra = np.array([extra_test[g] for g in aug_test_groups], dtype=np.float32)
            else:
                aug_test_extra = None

            test_tensors_aug = [
                torch.from_numpy(X_test_aug).long(),
                torch.from_numpy(np.array(aug_test_labels, dtype=np.float32)).float().unsqueeze(1),
            ]
            if aug_test_extra is not None:
                test_tensors_aug.append(torch.from_numpy(aug_test_extra).float())
            test_ds = TensorDataset(*test_tensors_aug)
            test_loader = DataLoader(test_ds, batch_size=self.batch_size * 2, shuffle=False)

            all_probs_aug = []
            with torch.no_grad():
                for batch in test_loader:
                    xb = batch[0].to(self.device)
                    eb = batch[2].to(self.device) if has_extra else None
                    pred = model(xb, extra=eb)
                    all_probs_aug.append(pred.cpu().numpy().ravel())

            raw_probs = np.concatenate(all_probs_aug)

            # Average predictions per original molecule
            n_test = len(test_smiles_for_tta)
            probs = np.zeros(n_test)
            for i in range(n_test):
                mask = [j for j, g in enumerate(aug_test_groups) if g == i]
                if mask:
                    probs[i] = raw_probs[mask].mean()
                else:
                    probs[i] = 0.0
            true = y_test[:n_test]
        else:
            # Fallback: no TTA
            test_tensors = [
                torch.from_numpy(X_test).long(),
                torch.from_numpy(y_test).float().unsqueeze(1),
            ]
            if extra_test is not None:
                test_tensors.append(torch.from_numpy(extra_test).float())
            test_ds = TensorDataset(*test_tensors)
            test_loader = DataLoader(test_ds, batch_size=self.batch_size * 2, shuffle=False)

            all_probs = []
            all_labels = []
            with torch.no_grad():
                for batch in test_loader:
                    xb = batch[0].to(self.device)
                    eb = batch[2].to(self.device) if has_extra else None
                    pred = model(xb, extra=eb)
                    all_probs.append(pred.cpu().numpy().ravel())
                    all_labels.append(batch[1].numpy().ravel())

            probs = np.concatenate(all_probs)
            true = np.concatenate(all_labels)

        # Optimize threshold on validation set if not provided
        if threshold is None:
            threshold = self._optimize_threshold(model, val_loader, has_extra=has_extra)

        preds = (probs >= threshold).astype(int)

        # Metrics
        f1 = f1_score(true, preds, zero_division=0)
        try:
            auc_roc = roc_auc_score(true, probs)
        except ValueError:
            auc_roc = 0.0
        try:
            prec_curve, rec_curve, _ = precision_recall_curve(true, probs)
            auc_pr = auc(rec_curve, prec_curve)
        except ValueError:
            auc_pr = 0.0
        acc = accuracy_score(true, preds)
        prec = precision_score(true, preds, zero_division=0)
        rec = recall_score(true, preds, zero_division=0)

        logger.info(
            f"  Fold {fold_idx} test: F1={f1:.4f}  AUC-ROC={auc_roc:.4f}  "
            f"AUC-PR={auc_pr:.4f}  Acc={acc:.4f}  Thresh={threshold:.3f}"
        )

        return FoldResult(
            fold=fold_idx,
            f1=f1,
            auc_roc=auc_roc,
            auc_pr=auc_pr,
            accuracy=acc,
            precision=prec,
            recall=rec,
            threshold=threshold,
            train_loss_history=train_losses,
            val_loss_history=val_losses,
        )

    def _optimize_threshold(self, model: LSTMAttModel, val_loader: DataLoader, has_extra: bool = False) -> float:
        """Find threshold maximizing F1 on validation set."""
        model.eval()
        all_probs = []
        all_labels = []
        with torch.no_grad():
            for batch in val_loader:
                xb = batch[0].to(self.device)
                eb = batch[2].to(self.device) if has_extra else None
                pred = model(xb, extra=eb)
                all_probs.append(pred.cpu().numpy().ravel())
                all_labels.append(batch[1].numpy().ravel())

        probs = np.concatenate(all_probs)
        true = np.concatenate(all_labels)

        best_f1 = 0.0
        best_thresh = 0.5
        for t in np.arange(0.1, 0.9, 0.01):
            preds = (probs >= t).astype(int)
            f1 = f1_score(true, preds, zero_division=0)
            if f1 > best_f1:
                best_f1 = f1
                best_thresh = t

        logger.info(f"  Optimized threshold: {best_thresh:.3f} (val F1={best_f1:.4f})")
        return best_thresh
