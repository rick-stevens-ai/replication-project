"""Label experiment: compare model performance with two different class definitions.

A: Original bin_class (delta_pce >= 2.00) — 133 class 1, 181 class 0
B: Derived from norm_dpce >= 0.10        — 142 class 1, 172 class 0

Runs both RF and SMILES-X classifiers under both label sets.
"""

import json
import logging
import os
import sys

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import (
    f1_score, roc_auc_score, accuracy_score, precision_score, recall_score,
    confusion_matrix,
)

from smilesx import SmilesXClassifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/label_experiment.log"),
    ],
)
logger = logging.getLogger(__name__)
# Keep SMILES-X logs quieter
logging.getLogger("smilesx.train").setLevel(logging.WARNING)

DATA_PATH = "data/T0.csv"
OUTDIR = "models/label_experiment"

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


def smiles_to_morgan(smiles, radius=2, n_bits=2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.zeros(n_bits)
    return np.array(AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits))


# ─── RF ───────────────────────────────────────────────────────────────────────

def run_rf(X, y, label_name, n_folds=5, seed=42):
    """Run RF with paper's grid search and CV."""
    param_grid = {
        "n_estimators": [100, 200, 300],
        "max_depth": [5, 10, 15],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
    }

    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)
    grid = GridSearchCV(
        RandomForestClassifier(random_state=seed, n_jobs=-1),
        param_grid, cv=skf, scoring="f1", n_jobs=-1, refit=True,
    )
    grid.fit(X, y)

    # Per-fold evaluation with best params
    fold_results = []
    all_true, all_pred, all_prob = [], [], []

    for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X, y)):
        rf = RandomForestClassifier(**grid.best_params_, random_state=seed, n_jobs=-1)
        rf.fit(X[train_idx], y[train_idx])
        y_pred = rf.predict(X[test_idx])
        y_prob = rf.predict_proba(X[test_idx])[:, 1]

        fold_results.append({
            "fold": fold_idx,
            "f1": f1_score(y[test_idx], y_pred),
            "auc_roc": roc_auc_score(y[test_idx], y_prob),
            "precision": precision_score(y[test_idx], y_pred, zero_division=0),
            "recall": recall_score(y[test_idx], y_pred, zero_division=0),
            "accuracy": accuracy_score(y[test_idx], y_pred),
        })
        all_true.extend(y[test_idx].tolist())
        all_pred.extend(y_pred.tolist())
        all_prob.extend(y_prob.tolist())

    f1s = [f["f1"] for f in fold_results]
    aucs = [f["auc_roc"] for f in fold_results]
    cm = confusion_matrix(all_true, all_pred)

    return {
        "label": label_name,
        "model": "RF",
        "best_params": grid.best_params_,
        "best_grid_f1": grid.best_score_,
        "folds": fold_results,
        "mean_f1": float(np.mean(f1s)),
        "std_f1": float(np.std(f1s)),
        "mean_auc": float(np.mean(aucs)),
        "std_auc": float(np.std(aucs)),
        "aggregate_cm": cm.tolist(),
        "aggregate_f1": float(f1_score(all_true, all_pred)),
    }


# ─── SMILES-X ────────────────────────────────────────────────────────────────

def run_smilesx(df, label_col, extra_cols, label_name, outdir, n_folds=5, seed=42):
    """Run SMILES-X classifier with best Optuna config."""
    clf = SmilesXClassifier(
        data=df,
        smiles_col="smiles",
        label_col=label_col,
        extra_feature_cols=extra_cols,
        embed_dim=32,
        lstm_units=128,
        tdense_units=64,
        dense_depth=2,
        dropout=0.3,
        lr=1.67e-4,
        weight_decay=5e-6,
        batch_size=32,
        n_epochs=100,
        patience=25,
        class_weight=True,
        outdir=outdir,
        seed=seed,
    )

    result = clf.cross_validate(n_folds=n_folds, augment=True, threshold=None)

    return {
        "label": label_name,
        "model": "SMILES-X",
        "folds": [
            {"fold": f.fold, "f1": f.f1, "auc_roc": f.auc_roc, "precision": f.precision,
             "recall": f.recall, "accuracy": f.accuracy, "threshold": f.threshold}
            for f in result.folds
        ],
        "mean_f1": result.mean_f1,
        "std_f1": result.std_f1,
        "mean_auc": result.mean_auc,
        "std_auc": result.std_auc,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def print_result(res):
    model = res["model"]
    label = res["label"]
    print(f"\n  {model} — {label}")
    for f in res["folds"]:
        print(
            f"    Fold {f['fold']}: F1={f['f1']:.4f}  AUC={f['auc_roc']:.4f}  "
            f"Prec={f['precision']:.4f}  Rec={f['recall']:.4f}  Acc={f['accuracy']:.4f}"
        )
    print(f"    Mean: F1={res['mean_f1']:.4f}±{res['std_f1']:.4f}  AUC={res['mean_auc']:.4f}±{res['std_auc']:.4f}")
    if "aggregate_cm" in res:
        cm = np.array(res["aggregate_cm"])
        print(f"    Aggregate CM: TN={cm[0,0]} FP={cm[0,1]} FN={cm[1,0]} TP={cm[1,1]}")


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    df = compute_descriptors(df)

    # Two label sets
    df["label_A"] = df["bin_class"]  # original: delta_pce >= 2.00
    df["label_B"] = (df["norm_dpce"] >= 0.10).astype(int)  # paper's stated: norm_dpce >= 0.10

    print(f"Label A (delta_pce >= 2.00): class 1={df['label_A'].sum()}, class 0={(1-df['label_A']).sum()}")
    print(f"Label B (norm_dpce >= 0.10): class 1={df['label_B'].sum()}, class 0={(1-df['label_B']).sum()}")
    print(f"Disagreements: {(df['label_A'] != df['label_B']).sum()}")

    # RF features
    fps = np.array([smiles_to_morgan(s) for s in df["smiles"]])
    ha = df["ha_num"].fillna(df["ha_num"].median()).values.reshape(-1, 1)
    o = df["o_num"].fillna(df["o_num"].median()).values.reshape(-1, 1)
    X_rf = np.hstack([fps, ha, o])

    # SMILES-X extra features
    extra_cols = ["ha_num", "o_num"] + list(DESCRIPTOR_FUNCS.keys())

    all_results = []

    # ── RF with label A ──
    logger.info("Running RF with label A (delta_pce >= 2.00)")
    res = run_rf(X_rf, df["label_A"].values, "A: delta_pce >= 2.00")
    all_results.append(res)
    print_result(res)

    # ── RF with label B ──
    logger.info("Running RF with label B (norm_dpce >= 0.10)")
    res = run_rf(X_rf, df["label_B"].values, "B: norm_dpce >= 0.10")
    all_results.append(res)
    print_result(res)

    # ── SMILES-X with label A ──
    logger.info("Running SMILES-X with label A (delta_pce >= 2.00)")
    res = run_smilesx(df, "label_A", extra_cols, "A: delta_pce >= 2.00",
                      os.path.join(OUTDIR, "smilesx_A"))
    all_results.append(res)
    print_result(res)

    # ── SMILES-X with label B ──
    logger.info("Running SMILES-X with label B (norm_dpce >= 0.10)")
    res = run_smilesx(df, "label_B", extra_cols, "B: norm_dpce >= 0.10",
                      os.path.join(OUTDIR, "smilesx_B"))
    all_results.append(res)
    print_result(res)

    # ── Summary table ──
    print(f"\n{'='*70}")
    print("LABEL EXPERIMENT SUMMARY")
    print(f"{'='*70}")
    print(f"  {'Model':<12} {'Labels':<25} {'F1':>12} {'AUC-ROC':>14}")
    print(f"  {'-'*12} {'-'*25} {'-'*12} {'-'*14}")
    for r in all_results:
        print(f"  {r['model']:<12} {r['label']:<25} {r['mean_f1']:.4f}±{r['std_f1']:.4f}   {r['mean_auc']:.4f}±{r['std_auc']:.4f}")
    print(f"{'='*70}")

    with open(os.path.join(OUTDIR, "label_experiment_results.json"), "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    logger.info(f"Results saved to {OUTDIR}/label_experiment_results.json")


if __name__ == "__main__":
    main()
