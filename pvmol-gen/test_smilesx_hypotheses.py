"""Test hypotheses for SMILES-X performance gap vs paper.

The paper says: 5-fold CV, 3 runs per fold, threshold=0.47.
We get F1~0.62. What did they get, and could evaluation methodology explain it?

Hypotheses:
1. Train-set evaluation: train on all, predict on all with threshold=0.47
2. Train on all, optimize threshold on same data
3. Single best fold cherry-picked
4. 3-seed averaging reduces variance significantly
5. Original Keras SMILES-X gives different results than PyTorch port
"""

import logging
import os
import sys

import numpy as np
import pandas as pd
import torch
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score, confusion_matrix

from smilesx.tokenizer import SmilesTokenizer
from smilesx.augment import augment_smiles
from smilesx.model import LSTMAttModel
from smilesx import SmilesXClassifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/smilesx_hypotheses.log"),
    ],
)
logger = logging.getLogger(__name__)
logging.getLogger("smilesx.train").setLevel(logging.WARNING)

DESCRIPTOR_FUNCS = {
    "molwt": Descriptors.MolWt, "logp": Descriptors.MolLogP, "tpsa": Descriptors.TPSA,
    "hbd": rdMolDescriptors.CalcNumHBD, "hba": rdMolDescriptors.CalcNumHBA,
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


def predict_all_folds(model_dir, df, smiles_col="smiles", threshold=0.47):
    """Load each fold model, predict on ALL data, average across folds."""
    from smilesx.predict import load_model, predict as smilesx_predict

    smiles_list = df[smiles_col].tolist()
    all_probs = []

    # Count fold models
    fold_files = [f for f in os.listdir(model_dir) if f.startswith("model_fold_") and f.endswith(".pt")]
    n_folds = len(fold_files)

    for fold in range(n_folds):
        model, tokenizer = load_model(model_dir, fold=fold, embed_dim=32, lstm_units=128,
                                       tdense_units=64, dense_depth=2)
        probs, _, _ = smilesx_predict(smiles_list, model, tokenizer,
                                       threshold=threshold, augment=True)
        all_probs.append(probs)

    # Ensemble average across folds
    mean_probs = np.mean(all_probs, axis=0)
    return mean_probs


def report(label, y_true, y_pred, y_prob=None):
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    f1 = f1_score(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred)
    auc = roc_auc_score(y_true, y_prob) if y_prob is not None else 0
    print(
        f"  {label}\n"
        f"    CM: TN={tn} FP={fp} FN={fn} TP={tp}  |  "
        f"F1={f1:.4f}  Acc={acc:.4f}  AUC={auc:.4f}"
    )
    return f1


def main():
    os.makedirs("logs", exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    df = pd.read_csv("data/T0.csv")
    df = compute_descriptors(df)
    y = df["bin_class"].values

    extra_cols_paper = ["ha_num", "o_num"]  # Paper only used these
    extra_cols_enriched = ["ha_num", "o_num"] + list(DESCRIPTOR_FUNCS.keys())

    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 70)
    print("HYPOTHESIS 1: Train 5-fold CV, then predict ALL data with each fold")
    print("  (ensemble average of fold models on full dataset)")
    print("=" * 70)

    # First train a normal 5-fold CV to get the models
    outdir_h1 = "models/smilesx_hypotheses/h1"
    os.makedirs(outdir_h1, exist_ok=True)

    clf = SmilesXClassifier(
        data=df, smiles_col="smiles", label_col="bin_class",
        extra_feature_cols=extra_cols_paper,
        embed_dim=32, lstm_units=128, tdense_units=64, dense_depth=2,
        dropout=0.3, lr=1.67e-4, weight_decay=5e-6, batch_size=32,
        n_epochs=100, patience=25, class_weight=True,
        outdir=outdir_h1, seed=42,
    )
    cv_result = clf.cross_validate(n_folds=5, augment=True, threshold=None)

    print(f"\n  Normal 5-fold CV result:")
    print(f"    Mean F1={cv_result.mean_f1:.4f} ± {cv_result.std_f1:.4f}")
    print(f"    Mean AUC={cv_result.mean_auc:.4f}")
    for f in cv_result.folds:
        print(f"    Fold {f.fold}: F1={f.f1:.4f} AUC={f.auc_roc:.4f} Thresh={f.threshold:.3f}")

    # Now load each fold model and predict on ALL data
    try:
        mean_probs = predict_all_folds(outdir_h1, df, threshold=0.47)
        for t in [0.30, 0.35, 0.40, 0.45, 0.47, 0.50]:
            preds = (mean_probs >= t).astype(int)
            report(f"H1: ensemble({5} folds) → predict(ALL) threshold={t:.2f}",
                   y, preds, mean_probs)
    except Exception as e:
        logger.warning(f"H1 predict_all_folds failed: {e}")
        # Fallback: train on ALL data directly
        print("  (Falling back to single model trained on all data)")

    # ═══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("HYPOTHESIS 2: Train single model on ALL data, predict ALL data")
    print("=" * 70)

    outdir_h2 = "models/smilesx_hypotheses/h2"
    os.makedirs(outdir_h2, exist_ok=True)

    # Train on full dataset (1-fold = no holdout)
    smiles = df["smiles"].values.tolist()
    labels = df["bin_class"].values.tolist()
    extra_features = df[extra_cols_paper].values.astype(np.float32)
    col_means = np.nanmean(extra_features, axis=0)
    for c in range(extra_features.shape[1]):
        mask = np.isnan(extra_features[:, c])
        extra_features[mask, c] = col_means[c]

    tokenizer = SmilesTokenizer().fit(smiles)
    all_tok = tokenizer.tokenize_batch(smiles)
    max_length = max(len(t) for t in all_tok) + 1

    # Augment all training data
    aug_smiles, aug_labels, aug_groups = augment_smiles(smiles, labels, augment=True)
    aug_extra = np.array([extra_features[g] for g in aug_groups], dtype=np.float32)

    X_all = tokenizer.encode_batch(aug_smiles, max_length)
    y_all_aug = np.array(aug_labels, dtype=np.float32)

    from sklearn.preprocessing import RobustScaler
    scaler = RobustScaler(quantile_range=(5.0, 95.0))
    aug_extra_scaled = scaler.fit_transform(aug_extra)
    extra_scaled = scaler.transform(extra_features)

    model = LSTMAttModel(
        vocab_size=tokenizer.vocab_size, max_length=max_length,
        embed_dim=32, lstm_units=128, tdense_units=64, dense_depth=2,
        dropout=0.3, model_type="classification", n_extra_features=2,
    ).to(device)

    # Train
    from torch.utils.data import DataLoader, TensorDataset
    optimizer = torch.optim.Adam(model.parameters(), lr=1.67e-4, weight_decay=5e-6)
    n_neg = labels.count(0)
    n_pos = labels.count(1)
    pos_weight = torch.tensor([n_neg / n_pos], device=device)
    criterion = torch.nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    train_ds = TensorDataset(
        torch.from_numpy(X_all).long(),
        torch.from_numpy(y_all_aug).float().unsqueeze(1),
        torch.from_numpy(aug_extra_scaled).float(),
    )
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)

    model.train()
    for epoch in range(100):
        total_loss = 0
        for batch in train_loader:
            xb, yb, eb = batch[0].to(device), batch[1].to(device), batch[2].to(device)
            optimizer.zero_grad()
            model.model_type = "regression"
            logits = model(xb, extra=eb)
            model.model_type = "classification"
            loss = criterion(logits, yb)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            total_loss += loss.item()
        if (epoch + 1) % 20 == 0:
            logger.info(f"  Epoch {epoch+1}: loss={total_loss/len(train_loader):.4f}")

    # Predict on ALL original (non-augmented) data with TTA
    model.eval()
    aug_test_smiles, aug_test_labels, aug_test_groups = augment_smiles(smiles, labels, augment=True)
    X_test_aug = tokenizer.encode_batch(aug_test_smiles, max_length)
    aug_test_extra = np.array([extra_features[g] for g in aug_test_groups], dtype=np.float32)
    aug_test_extra_scaled = scaler.transform(aug_test_extra)

    test_ds = TensorDataset(
        torch.from_numpy(X_test_aug).long(),
        torch.from_numpy(aug_test_extra_scaled).float(),
    )
    test_loader = DataLoader(test_ds, batch_size=64, shuffle=False)

    all_probs = []
    with torch.no_grad():
        for batch in test_loader:
            xb, eb = batch[0].to(device), batch[1].to(device)
            pred = model(xb, extra=eb)
            all_probs.append(pred.cpu().numpy().ravel())
    raw_probs = np.concatenate(all_probs)

    # Average per original molecule
    probs = np.zeros(len(smiles))
    for i in range(len(smiles)):
        mask = [j for j, g in enumerate(aug_test_groups) if g == i]
        probs[i] = raw_probs[mask].mean() if mask else 0.0

    print(f"\n  Model trained on ALL {len(smiles)} molecules:")
    for t in [0.30, 0.35, 0.40, 0.45, 0.47, 0.50, 0.55]:
        preds = (probs >= t).astype(int)
        report(f"H2: train(ALL) → predict(ALL) threshold={t:.2f}", y, preds, probs)

    # ═══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("HYPOTHESIS 3: Multi-seed averaging (3 seeds × 5-fold CV)")
    print("=" * 70)

    all_f1s = []
    for seed in [42, 123, 7]:
        clf_s = SmilesXClassifier(
            data=df, smiles_col="smiles", label_col="bin_class",
            extra_feature_cols=extra_cols_paper,
            embed_dim=32, lstm_units=128, tdense_units=64, dense_depth=2,
            dropout=0.3, lr=1.67e-4, weight_decay=5e-6, batch_size=32,
            n_epochs=100, patience=25, class_weight=True,
            outdir=f"models/smilesx_hypotheses/h3_seed{seed}", seed=seed,
        )
        res = clf_s.cross_validate(n_folds=5, augment=True, threshold=0.47)
        print(f"  Seed {seed}: F1={res.mean_f1:.4f}±{res.std_f1:.4f}  AUC={res.mean_auc:.4f}")
        all_f1s.append(res.mean_f1)

    print(f"  3-seed average: F1={np.mean(all_f1s):.4f}±{np.std(all_f1s):.4f}")

    # ═══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("HYPOTHESIS 4: Paper used only ha_num + o_num (no enriched features)")
    print("  Already tested above — H1 uses paper's exact feature set")
    print("=" * 70)

    # ═══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)


if __name__ == "__main__":
    main()
