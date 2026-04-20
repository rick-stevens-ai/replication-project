"""Random Forest classifier on T0 data — replicating Fajar et al. methodology.

Uses 2048-bit Morgan fingerprints (radius=2) + hba_num + o_num features.
Grid search over the paper's exact hyperparameter space.
5-fold CV with the same evaluation protocol.
"""

import json
import logging
import os
import sys

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import (
    f1_score, roc_auc_score, accuracy_score, precision_score, recall_score,
    precision_recall_curve, auc, confusion_matrix, classification_report,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/train_t0_rf.log"),
    ],
)
logger = logging.getLogger(__name__)

DATA_PATH = "data/T0.csv"
OUTDIR = "models/t0_rf"


def smiles_to_morgan(smiles, radius=2, n_bits=2048):
    """Convert SMILES to Morgan fingerprint bit vector."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.zeros(n_bits)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
    return np.array(fp)


def build_features(df):
    """Build feature matrix: 2048-bit Morgan FP + hba_num + o_num."""
    fps = np.array([smiles_to_morgan(s) for s in df["smiles"]])

    # Extra features matching paper: hba_num and o_num
    ha_num = df["ha_num"].fillna(df["ha_num"].median()).values.reshape(-1, 1)
    o_num = df["o_num"].fillna(df["o_num"].median()).values.reshape(-1, 1)

    X = np.hstack([fps, ha_num, o_num])
    logger.info(f"Feature matrix: {X.shape} (2048 Morgan bits + 2 extra)")
    return X


def run_grid_search_cv(X, y, n_folds=5, seed=42):
    """Run grid search with 5-fold CV matching paper's exact search space."""

    # Paper's exact grid (Section 2.2)
    param_grid = {
        "n_estimators": [100, 200, 300],
        "max_depth": [5, 10, 15],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
    }

    rf = RandomForestClassifier(random_state=seed, n_jobs=-1)
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)

    grid = GridSearchCV(
        rf, param_grid,
        cv=skf,
        scoring="f1",
        n_jobs=-1,
        verbose=1,
        refit=True,
    )
    grid.fit(X, y)

    logger.info(f"Best params: {grid.best_params_}")
    logger.info(f"Best CV F1: {grid.best_score_:.4f}")

    return grid


def evaluate_cv(X, y, best_params, n_folds=5, seed=42):
    """Run full CV evaluation with the best params, report per-fold metrics."""
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)

    fold_results = []
    all_true = []
    all_pred = []
    all_prob = []

    for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X, y)):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        rf = RandomForestClassifier(**best_params, random_state=seed, n_jobs=-1)
        rf.fit(X_train, y_train)

        y_pred = rf.predict(X_test)
        y_prob = rf.predict_proba(X_test)[:, 1]

        f1 = f1_score(y_test, y_pred)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        try:
            auc_roc = roc_auc_score(y_test, y_prob)
        except ValueError:
            auc_roc = 0.0
        try:
            prec_curve, rec_curve, _ = precision_recall_curve(y_test, y_prob)
            auc_pr = auc(rec_curve, prec_curve)
        except ValueError:
            auc_pr = 0.0

        fold_results.append({
            "fold": fold_idx,
            "f1": f1, "accuracy": acc, "precision": prec, "recall": rec,
            "auc_roc": auc_roc, "auc_pr": auc_pr,
        })

        all_true.extend(y_test.tolist())
        all_pred.extend(y_pred.tolist())
        all_prob.extend(y_prob.tolist())

        logger.info(
            f"  Fold {fold_idx}: F1={f1:.4f}  AUC-ROC={auc_roc:.4f}  "
            f"Prec={prec:.4f}  Rec={rec:.4f}  Acc={acc:.4f}"
        )

    # Aggregate
    all_true = np.array(all_true)
    all_pred = np.array(all_pred)
    all_prob = np.array(all_prob)

    return fold_results, all_true, all_pred, all_prob


def evaluate_with_threshold(all_true, all_prob, threshold=0.47):
    """Re-evaluate predictions using the paper's fixed threshold of 0.47."""
    preds = (all_prob >= threshold).astype(int)
    f1 = f1_score(all_true, preds)
    acc = accuracy_score(all_true, preds)
    prec = precision_score(all_true, preds, zero_division=0)
    rec = recall_score(all_true, preds, zero_division=0)
    auc_roc = roc_auc_score(all_true, all_prob)
    cm = confusion_matrix(all_true, preds)
    return {
        "threshold": threshold, "f1": f1, "accuracy": acc,
        "precision": prec, "recall": rec, "auc_roc": auc_roc,
        "confusion_matrix": cm.tolist(),
    }


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    X = build_features(df)
    y = df["bin_class"].values

    logger.info(f"Dataset: {len(df)} molecules, {y.sum()} class 1, {(1-y).sum()} class 0")

    # --- Grid Search (paper's protocol) ---
    logger.info("\n" + "=" * 60)
    logger.info("GRID SEARCH — Paper's hyperparameter space")
    logger.info("=" * 60)
    grid = run_grid_search_cv(X, y, n_folds=5, seed=42)
    best_params = grid.best_params_

    # --- Full CV evaluation with best params ---
    logger.info("\n" + "=" * 60)
    logger.info("5-FOLD CV — Best params")
    logger.info("=" * 60)
    fold_results, all_true, all_pred, all_prob = evaluate_cv(X, y, best_params, n_folds=5, seed=42)

    # Per-fold summary
    f1s = [f["f1"] for f in fold_results]
    aucs = [f["auc_roc"] for f in fold_results]
    print(f"\n{'='*70}")
    print("RF CLASSIFIER — 5-Fold CV Results")
    print(f"{'='*70}")
    for f in fold_results:
        print(
            f"  Fold {f['fold']}: F1={f['f1']:.4f}  AUC-ROC={f['auc_roc']:.4f}  "
            f"Prec={f['precision']:.4f}  Rec={f['recall']:.4f}  Acc={f['accuracy']:.4f}"
        )
    print(f"{'-'*70}")
    print(f"  Mean: F1={np.mean(f1s):.4f}±{np.std(f1s):.4f}  AUC-ROC={np.mean(aucs):.4f}±{np.std(aucs):.4f}")
    print(f"  Best params: {best_params}")

    # --- Aggregate confusion matrix (default threshold 0.5) ---
    cm = confusion_matrix(all_true, all_pred)
    print(f"\n  Aggregate confusion matrix (threshold=0.50):")
    print(f"    TN={cm[0,0]}  FP={cm[0,1]}")
    print(f"    FN={cm[1,0]}  TP={cm[1,1]}")
    print(f"  Aggregate: F1={f1_score(all_true, all_pred):.4f}  Acc={accuracy_score(all_true, all_pred):.4f}")

    # --- Re-evaluate with paper's threshold of 0.47 ---
    res_047 = evaluate_with_threshold(all_true, all_prob, threshold=0.47)
    cm47 = np.array(res_047["confusion_matrix"])
    print(f"\n  Aggregate confusion matrix (threshold=0.47, paper's value):")
    print(f"    TN={cm47[0,0]}  FP={cm47[0,1]}")
    print(f"    FN={cm47[1,0]}  TP={cm47[1,1]}")
    print(f"  Aggregate: F1={res_047['f1']:.4f}  Prec={res_047['precision']:.4f}  "
          f"Rec={res_047['recall']:.4f}  Acc={res_047['accuracy']:.4f}")

    # --- Paper's confusion matrix for reference ---
    print(f"\n  Paper's RF confusion matrix (Figure S2b):")
    print(f"    TN=153  FP=28")
    print(f"    FN=37   TP=96")
    paper_f1 = 2*96 / (2*96 + 28 + 37)
    print(f"  Paper: F1={paper_f1:.4f}  Prec={96/(96+28):.4f}  Rec={96/(96+37):.4f}  Acc={(153+96)/314:.4f}")

    print(f"{'='*70}")

    # --- Also try 10-fold CV ---
    logger.info("\n" + "=" * 60)
    logger.info("10-FOLD CV — Best params")
    logger.info("=" * 60)
    fold_results_10, all_true_10, all_pred_10, all_prob_10 = evaluate_cv(
        X, y, best_params, n_folds=10, seed=42
    )
    f1s_10 = [f["f1"] for f in fold_results_10]
    aucs_10 = [f["auc_roc"] for f in fold_results_10]
    print(f"\n{'='*70}")
    print("RF CLASSIFIER — 10-Fold CV Results")
    print(f"{'='*70}")
    for f in fold_results_10:
        print(
            f"  Fold {f['fold']:2d}: F1={f['f1']:.4f}  AUC-ROC={f['auc_roc']:.4f}  "
            f"Prec={f['precision']:.4f}  Rec={f['recall']:.4f}  Acc={f['accuracy']:.4f}"
        )
    print(f"{'-'*70}")
    print(f"  Mean: F1={np.mean(f1s_10):.4f}±{np.std(f1s_10):.4f}  AUC-ROC={np.mean(aucs_10):.4f}±{np.std(aucs_10):.4f}")
    print(f"{'='*70}")

    # Save results
    all_results = {
        "best_params": best_params,
        "best_cv_f1": grid.best_score_,
        "5fold": {
            "folds": fold_results,
            "mean_f1": float(np.mean(f1s)),
            "std_f1": float(np.std(f1s)),
            "mean_auc": float(np.mean(aucs)),
            "aggregate_cm_050": cm.tolist(),
            "aggregate_cm_047": res_047,
        },
        "10fold": {
            "folds": fold_results_10,
            "mean_f1": float(np.mean(f1s_10)),
            "std_f1": float(np.std(f1s_10)),
            "mean_auc": float(np.mean(aucs_10)),
        },
    }
    with open(os.path.join(OUTDIR, "rf_results.json"), "w") as f:
        json.dump(all_results, f, indent=2)

    logger.info(f"\nResults saved to {OUTDIR}/rf_results.json")


if __name__ == "__main__":
    main()
