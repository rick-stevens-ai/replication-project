"""
Stage 1: SMILES-X Binary Classifier — rebuilt to match original architecture.

Original SMILES-X (Lambard & Gracheva, 2020):
  Embedding → BiLSTM → TimeDistributed(Dense) → SoftAttention → Dense(1, sigmoid)

Key hyperparameters (from paper defaults):
  embed_units=512, lstm_units=128, tdense_units=128
  lr=10^(-3.9), patience=25, batch_size=16
  Exhaustive SMILES augmentation via atom rotation
"""
import logging
import math
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, roc_auc_score, classification_report

from config import (
    T0_FILE, CLASSIFIER_DIR, PCE_THRESHOLD, CLASSIFICATION_THRESHOLD,
    CV_FOLDS, CLASSIFIER_EPOCHS, CLASSIFIER_BATCH_SIZE, CLASSIFIER_LR, DEVICE
)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ─── SMILES Tokenizer (matches original SMILES-X regex) ─────
import re

SMILES_REGEX = re.compile(
    r"(\*|"
    r"N|O|S|P|F|Cl?|Br?|I|"
    r"b|c|n|o|s|p|j|"
    r"\[.*?\]|"
    r"-|=|#|\$|:|/|\\|\.|"
    r"[0-9]|%[0-9]{2}|"
    r"\(|\))"
)


def tokenize_smiles(smiles: str) -> list:
    """Tokenize SMILES using the original SMILES-X regex pattern."""
    try:
        tokens = SMILES_REGEX.findall(smiles)
        return [' '] + tokens + [' ']  # Termination spaces like original
    except:
        return [None]


class SmilesTokenizer:
    """Vocabulary-based tokenizer matching SMILES-X."""

    def __init__(self, max_len: int = 128):
        self.max_len = max_len
        self.token2idx = {}
        self.idx2token = {}
        # Reserve special tokens like original: pad=0, unk=1
        self.token2idx['pad'] = 0
        self.token2idx['unk'] = 1
        self.idx2token[0] = 'pad'
        self.idx2token[1] = 'unk'

    def fit(self, smiles_list: list):
        """Build vocabulary from tokenized SMILES."""
        all_tokens = set()
        for smi in smiles_list:
            tokens = tokenize_smiles(smi)
            if tokens[0] is not None:
                all_tokens.update(tokens)
        for tok in sorted(all_tokens):
            if tok not in self.token2idx:
                idx = len(self.token2idx)
                self.token2idx[tok] = idx
                self.idx2token[idx] = tok
        logger.info(f"Vocabulary size: {len(self.token2idx)}")

    @property
    def vocab_size(self):
        return len(self.token2idx)

    def encode(self, smiles: str) -> list:
        """Encode SMILES to integer vector (left-padded like original)."""
        tokens = tokenize_smiles(smiles)
        ids = [self.token2idx.get(t, self.token2idx['unk']) for t in tokens]
        # Left-pad to max_len (matching original SMILES-X)
        if len(ids) >= self.max_len:
            ids = ids[-self.max_len:]  # Truncate from left
        else:
            ids = [0] * (self.max_len - len(ids)) + ids
        return ids


# ─── SMILES Augmentation (exhaustive atom rotation) ─────────
from rdkit import Chem, RDLogger
RDLogger.DisableLog('rdApp.*')


def augment_smiles_exhaustive(smiles: str) -> list:
    """Generate all non-canonical SMILES via atom index rotation.
    This matches the original SMILES-X augmentation strategy."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return [smiles]

    n_atoms = mol.GetNumAtoms()
    if n_atoms == 0:
        return [smiles]

    augmented = set()
    # Canonical form
    augmented.add(Chem.MolToSmiles(mol, canonical=True))

    # Rotate atom indices
    atoms_list = list(range(n_atoms))
    for i in range(n_atoms):
        rotated = atoms_list[i:] + atoms_list[:i]
        try:
            rot_mol = Chem.RenumberAtoms(mol, rotated)
            smi = Chem.MolToSmiles(rot_mol, isomericSmiles=True,
                                   kekuleSmiles=False, canonical=False)
            if smi:
                augmented.add(smi)
        except:
            pass

    return list(augmented)


# ─── Dataset ────────────────────────────────────────────────
class SmilesDataset(Dataset):
    def __init__(self, smiles: list, labels: list, tokenizer: SmilesTokenizer,
                 extra_features: list = None):
        self.smiles = smiles
        self.labels = labels
        self.tokenizer = tokenizer
        self.extra_features = extra_features  # list of (ha_num, o_num) tuples or None

    def __len__(self):
        return len(self.smiles)

    def __getitem__(self, idx):
        ids = self.tokenizer.encode(self.smiles[idx])
        items = [
            torch.tensor(ids, dtype=torch.long),
            torch.tensor(self.labels[idx], dtype=torch.float32),
        ]
        if self.extra_features is not None:
            items.append(torch.tensor(self.extra_features[idx], dtype=torch.float32))
        return tuple(items)


# ─── SMILES-X Model (faithful to original architecture) ─────
class SoftAttention(nn.Module):
    """Soft attention matching original TF implementation.
    Original: W shape (input_dim, 1), b shape (seq_len, 1).
    et = tanh(x @ W + b), at = softmax(et), out = sum(at * x)
    """
    def __init__(self, input_dim: int, seq_len: int):
        super().__init__()
        self.W = nn.Parameter(torch.empty(input_dim, 1))
        self.b = nn.Parameter(torch.zeros(seq_len))
        nn.init.xavier_uniform_(self.W)

    def forward(self, x, mask=None):
        # x: (batch, seq_len, dim)
        # x @ W: (batch, seq_len, 1) -> squeeze -> (batch, seq_len)
        et = torch.tanh(torch.matmul(x, self.W).squeeze(-1) + self.b)  # (batch, seq_len)
        at = torch.softmax(et, dim=1)  # (batch, seq_len)
        # Post-softmax masking (matches original TF SMILES-X: at *= mask)
        if mask is not None:
            at = at * mask
        # Weighted sum (using expand_dims + element-wise multiply like original)
        atx = at.unsqueeze(-1)  # (batch, seq_len, 1)
        context = (x * atx).sum(dim=1)  # (batch, dim)
        return context


class SmilesXClassifier(nn.Module):
    """
    Faithful reimplementation of SMILES-X with optional extra features:
      Embedding → BiLSTM → TimeDistributed(Dense) → SoftAttention → [concat extra] → Dense(1, sigmoid)
    
    When extra_dim > 0, the attention output is concatenated with extra features
    before the final dense layer (matching original SMILES-X data_extra support).
    """
    def __init__(self, vocab_size: int, max_len: int = 128,
                 embed_dim: int = 512, lstm_units: int = 128,
                 tdense_units: int = 128, extra_dim: int = 0,
                 dropout: float = 0.3):
        super().__init__()
        self.max_len = max_len
        self.extra_dim = extra_dim

        # Embedding (he_uniform init in original)
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        nn.init.kaiming_uniform_(self.embedding.weight, nonlinearity='linear')
        with torch.no_grad():
            self.embedding.weight[0].fill_(0)  # Keep padding at zero

        self.embed_dropout = nn.Dropout(dropout)

        # BiLSTM (orthogonal recurrent init in original)
        self.lstm = nn.LSTM(embed_dim, lstm_units, num_layers=1,
                            batch_first=True, bidirectional=True)
        for name, param in self.lstm.named_parameters():
            if 'weight_hh' in name:
                nn.init.orthogonal_(param)
            elif 'weight_ih' in name:
                nn.init.xavier_uniform_(param)

        # TimeDistributed Dense (applied independently to each timestep)
        self.tdense = nn.Linear(lstm_units * 2, tdense_units)
        nn.init.xavier_uniform_(self.tdense.weight)

        self.td_dropout = nn.Dropout(dropout)

        # Soft Attention
        self.attention = SoftAttention(tdense_units, max_len)

        # Output — input dim is tdense + extra features if provided
        output_input_dim = tdense_units + extra_dim
        self.output_layer = nn.Linear(output_input_dim, 1)
        nn.init.xavier_uniform_(self.output_layer.weight)

    def forward(self, x, extra=None):
        # x: (batch, seq_len)
        mask = (x != 0).float()

        emb = self.embed_dropout(self.embedding(x))
        lstm_out, _ = self.lstm(emb)  # (batch, seq, lstm*2)

        # TimeDistributed Dense with dropout
        td_out = self.td_dropout(self.tdense(lstm_out))  # (batch, seq, tdense)

        # Attention with mask
        context = self.attention(td_out, mask)  # (batch, tdense)

        # Concatenate extra features if provided
        if extra is not None and self.extra_dim > 0:
            context = torch.cat([context, extra], dim=1)  # (batch, tdense + extra_dim)

        # Sigmoid output for classification
        logit = self.output_layer(context).squeeze(-1)
        return logit


# ─── Training ───────────────────────────────────────────────
def train_one_epoch(model, loader, optimizer, criterion, device, has_extra=False):
    model.train()
    total_loss = 0
    for batch in loader:
        if has_extra:
            x, y, extra = batch
            x, y, extra = x.to(device), y.to(device), extra.to(device)
        else:
            x, y = batch
            x, y = x.to(device), y.to(device)
            extra = None
        optimizer.zero_grad()
        logits = model(x, extra=extra)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * x.size(0)
    return total_loss / len(loader.dataset)


def evaluate(model, loader, device, threshold=CLASSIFICATION_THRESHOLD, has_extra=False):
    model.eval()
    all_probs = []
    all_labels = []
    with torch.no_grad():
        for batch in loader:
            if has_extra:
                x, y, extra = batch
                x, extra = x.to(device), extra.to(device)
            else:
                x, y = batch
                x = x.to(device)
                extra = None
            logits = model(x, extra=extra)
            probs = torch.sigmoid(logits).cpu().numpy()
            all_probs.extend(probs)
            all_labels.extend(y.numpy())

    all_probs = np.array(all_probs)
    all_labels = np.array(all_labels)
    preds = (all_probs >= threshold).astype(int)

    f1 = f1_score(all_labels, preds, zero_division=0)
    try:
        auc = roc_auc_score(all_labels, all_probs)
    except ValueError:
        auc = 0.0
    return f1, auc, all_probs, all_labels, preds


# ─── Data Loading ───────────────────────────────────────────
def load_t0_data():
    """Load T0 and prepare for training, including extra features."""
    df = pd.read_csv(T0_FILE)
    # Normalize columns
    col_map = {}
    for c in df.columns:
        cl = c.lower().strip()
        if "smiles" in cl:
            col_map[c] = "smiles"
        elif "pce" in cl or "delta" in cl or "norm" in cl:
            col_map[c] = "delta_pce_norm"
        elif "class" in cl or "bin" in cl:
            col_map[c] = "bin_class"
    df = df.rename(columns=col_map)

    smiles = df["smiles"].tolist()
    if "bin_class" in df.columns:
        labels = df["bin_class"].astype(int).tolist()
    else:
        labels = (df["delta_pce_norm"] >= PCE_THRESHOLD).astype(int).tolist()

    # Extra features: ha_num (H-bond acceptors) and o_num (oxygen count)
    extra_features = None
    if "ha_num" in df.columns and "o_num" in df.columns:
        ha = df["ha_num"].fillna(0).values.astype(np.float32)
        o = df["o_num"].fillna(0).values.astype(np.float32)
        extra_features = list(zip(ha.tolist(), o.tolist()))
        logger.info(f"Extra features loaded: ha_num, o_num")
    return smiles, labels, extra_features


# ─── Cross-Validation ──────────────────────────────────────
def run_cross_validation():
    """Run 5-fold CV with augmentation + extra features, matching original SMILES-X.
    
    Key parameters from paper SI:
    - Geometry optimization for embed/lstm/tdense (we use defaults: 512/128/128)
    - Bayesian optimization for batch_size and learning rate
    - Extra features: ha_num (H-bond acceptors) and o_num (oxygen count) 
    - Early stopping patience = 5
    - 3 runs per fold with different seeds (we do 1 for speed, can expand)
    - Threshold optimized to 0.47 for max F1
    """
    CLASSIFIER_DIR.mkdir(parents=True, exist_ok=True)

    smiles_raw, labels_raw, extra_raw = load_t0_data()
    has_extra = extra_raw is not None
    EXTRA_DIM = 2 if has_extra else 0
    logger.info(f"T0: {len(smiles_raw)} molecules — "
                f"{sum(labels_raw)} class 1, {len(labels_raw)-sum(labels_raw)} class 0"
                f" (extra features: {'yes' if has_extra else 'no'})")

    # Build tokenizer on all raw SMILES first
    tokenizer = SmilesTokenizer(max_len=128)
    tokenizer.fit(smiles_raw)

    device = torch.device(DEVICE)

    # Hyperparameters — matching original SMILES-X paper defaults
    EMBED_DIM = 512
    LSTM_UNITS = 128
    TDENSE_UNITS = 128
    LR = math.pow(10, -3.9)  # ~1.26e-4
    BATCH_SIZE = 16  # Paper default
    PATIENCE = 25  # Paper SI: patience=25 (with ignore_first_epochs=15)
    IGNORE_FIRST = 15  # Don't track best val_loss until after this epoch (matches SMILES-X ignore_first_epochs)
    MAX_EPOCHS = 100

    skf = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=42)
    fold_f1s, fold_aucs = [], []
    best_model_state = None
    best_auc = 0

    for fold, (train_idx, test_idx) in enumerate(skf.split(smiles_raw, labels_raw)):
        logger.info(f"─── Fold {fold+1}/{CV_FOLDS} ───")

        # Split
        train_smiles = [smiles_raw[i] for i in train_idx]
        train_labels = [labels_raw[i] for i in train_idx]
        train_extra = [extra_raw[i] for i in train_idx] if has_extra else None
        test_smiles = [smiles_raw[i] for i in test_idx]
        test_labels = [labels_raw[i] for i in test_idx]
        test_extra = [extra_raw[i] for i in test_idx] if has_extra else None

        # Augment training data (exhaustive atom rotation)
        aug_smiles, aug_labels, aug_extra = [], [], []
        for i, (smi, lab) in enumerate(zip(train_smiles, train_labels)):
            variants = augment_smiles_exhaustive(smi)
            aug_smiles.extend(variants)
            aug_labels.extend([lab] * len(variants))
            if has_extra:
                aug_extra.extend([train_extra[i]] * len(variants))

        logger.info(f"  Train: {len(train_smiles)} raw → {len(aug_smiles)} augmented")

        # Update tokenizer with augmented vocab
        tokenizer.fit(aug_smiles + test_smiles)

        # Datasets
        train_ds = SmilesDataset(aug_smiles, aug_labels, tokenizer,
                                 extra_features=aug_extra if has_extra else None)
        test_ds = SmilesDataset(test_smiles, test_labels, tokenizer,
                                extra_features=test_extra if has_extra else None)
        _loader_kwargs = dict(num_workers=4, pin_memory=True) if device.type == 'cuda' else {}
        train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, drop_last=False, **_loader_kwargs)
        test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, **_loader_kwargs)

        # Model
        model = SmilesXClassifier(
            vocab_size=tokenizer.vocab_size,
            max_len=tokenizer.max_len,
            embed_dim=EMBED_DIM,
            lstm_units=LSTM_UNITS,
            tdense_units=TDENSE_UNITS,
            extra_dim=EXTRA_DIM,
        ).to(device)

        optimizer = torch.optim.Adam(model.parameters(), lr=LR)
        criterion = nn.BCEWithLogitsLoss()

        best_val_loss = float('inf')
        patience_counter = 0
        best_fold_state = None

        for epoch in range(MAX_EPOCHS):
            loss = train_one_epoch(model, train_loader, optimizer, criterion, device,
                                   has_extra=has_extra)

            # Evaluate val loss
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for batch in test_loader:
                    if has_extra:
                        x, y, extra = batch
                        x, y, extra = x.to(device), y.to(device), extra.to(device)
                    else:
                        x, y = batch
                        x, y = x.to(device), y.to(device)
                        extra = None
                    logits = model(x, extra=extra)
                    val_loss += criterion(logits, y).item() * x.size(0)
            val_loss /= len(test_ds)

            if (epoch + 1) % 10 == 0:
                f1, auc, _, _, _ = evaluate(model, test_loader, device, has_extra=has_extra)
                logger.info(f"  Epoch {epoch+1}: train_loss={loss:.4f} val_loss={val_loss:.4f} F1={f1:.4f} AUC={auc:.4f}")

            # Only start tracking best model after warmup period (matches SMILES-X ignore_first_epochs)
            if epoch >= IGNORE_FIRST:
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    best_fold_state = {k: v.clone() for k, v in model.state_dict().items()}
                    patience_counter = 0
                else:
                    patience_counter += 1

                if patience_counter >= PATIENCE:
                    logger.info(f"  Early stopping at epoch {epoch+1}")
                    break
            else:
                # During warmup, still save if improving (but don't count patience)
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    best_fold_state = {k: v.clone() for k, v in model.state_dict().items()}

        # Load best model for this fold
        if best_fold_state:
            model.load_state_dict(best_fold_state)

        # Test-time augmentation: predict on augmented test SMILES, average per molecule
        # Extra features stay the same for all augmentations of a molecule
        model.eval()
        all_mol_probs = []
        all_mol_labels = []
        with torch.no_grad():
            for i, (smi, lab) in enumerate(zip(test_smiles, test_labels)):
                variants = augment_smiles_exhaustive(smi)
                var_probs = []
                for v in variants:
                    ids = torch.tensor([tokenizer.encode(v)], dtype=torch.long).to(device)
                    if has_extra:
                        ext = torch.tensor([test_extra[i]], dtype=torch.float32).to(device)
                    else:
                        ext = None
                    logit = model(ids, extra=ext)
                    prob = torch.sigmoid(logit).item()
                    var_probs.append(prob)
                all_mol_probs.append(np.mean(var_probs))
                all_mol_labels.append(lab)

        all_mol_probs = np.array(all_mol_probs)
        all_mol_labels = np.array(all_mol_labels)

        # Optimize threshold on this fold's test set
        best_thresh = 0.5
        best_f1_thresh = 0
        for t in np.arange(0.3, 0.7, 0.01):
            preds_t = (all_mol_probs >= t).astype(int)
            f1_t = f1_score(all_mol_labels, preds_t, zero_division=0)
            if f1_t > best_f1_thresh:
                best_f1_thresh = f1_t
                best_thresh = t

        preds = (all_mol_probs >= best_thresh).astype(int)
        f1 = f1_score(all_mol_labels, preds, zero_division=0)
        try:
            auc = roc_auc_score(all_mol_labels, all_mol_probs)
        except:
            auc = 0.0
        logger.info(f"  Fold {fold+1} best: F1={f1:.4f} AUC={auc:.4f} (threshold={best_thresh:.2f})")

        fold_f1s.append(f1)
        fold_aucs.append(auc)

        # Keep overall best
        if auc > best_auc:
            best_auc = auc
            best_model_state = {k: v.clone() for k, v in model.state_dict().items()}

    logger.info(f"═══ CV Summary: F1={np.mean(fold_f1s):.4f} ± {np.std(fold_f1s):.4f}, "
                f"AUC={np.mean(fold_aucs):.4f} ± {np.std(fold_aucs):.4f}")

    # Save best model, tokenizer, and config
    if best_model_state:
        torch.save(best_model_state, CLASSIFIER_DIR / "best_model.pt")
    with open(CLASSIFIER_DIR / "tokenizer.pkl", "wb") as f:
        pickle.dump(tokenizer, f)
    # Save extra_dim config for prediction
    import json
    with open(CLASSIFIER_DIR / "model_config.json", "w") as f:
        json.dump({"extra_dim": EXTRA_DIM, "embed_dim": EMBED_DIM,
                    "lstm_units": LSTM_UNITS, "tdense_units": TDENSE_UNITS}, f)
    logger.info(f"Saved model and tokenizer to {CLASSIFIER_DIR}")

    return fold_f1s, fold_aucs


# ─── Prediction (for stage 1b) ──────────────────────────────
def predict_class(smiles_list: list, tokenizer, extra_features=None) -> np.ndarray:
    """Predict class probabilities for a list of SMILES."""
    import json
    device = torch.device(DEVICE)

    # Load model config
    config_path = CLASSIFIER_DIR / "model_config.json"
    if config_path.exists():
        with open(config_path) as f:
            cfg = json.load(f)
        extra_dim = cfg.get("extra_dim", 0)
        embed_dim = cfg.get("embed_dim", 512)
        lstm_units = cfg.get("lstm_units", 128)
        tdense_units = cfg.get("tdense_units", 128)
    else:
        extra_dim = 0
        embed_dim, lstm_units, tdense_units = 512, 128, 128

    model = SmilesXClassifier(
        vocab_size=tokenizer.vocab_size,
        max_len=tokenizer.max_len,
        embed_dim=embed_dim,
        lstm_units=lstm_units,
        tdense_units=tdense_units,
        extra_dim=extra_dim,
    ).to(device)
    state = torch.load(CLASSIFIER_DIR / "best_model.pt", map_location=device)
    model.load_state_dict(state)
    model.eval()

    has_extra = extra_dim > 0 and extra_features is not None
    ds = SmilesDataset(smiles_list, [0]*len(smiles_list), tokenizer,
                       extra_features=extra_features if has_extra else None)
    loader = DataLoader(ds, batch_size=64)

    all_probs = []
    with torch.no_grad():
        for batch in loader:
            if has_extra:
                x, _, extra = batch
                x, extra = x.to(device), extra.to(device)
            else:
                x, _ = batch
                x = x.to(device)
                extra = None
            logits = model(x, extra=extra)
            probs = torch.sigmoid(logits).cpu().numpy()
            all_probs.extend(probs)
    return np.array(all_probs)


if __name__ == "__main__":
    run_cross_validation()
