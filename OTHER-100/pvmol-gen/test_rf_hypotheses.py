"""Test hypotheses for why the paper reports RF F1=0.75 vs our CV F1=0.46.

Hypotheses:
1. Train-set evaluation: fit on all data, predict on all data
2. Refit after grid search: GridSearchCV(refit=True).predict(X) on full data
3. Single 80/20 split: paper says "split into training and testing subsets
   using an 80:20 ratio" — try many seeds to find one matching their CM
4. 80/20 split with grid search on train, eval on test (paper's stated protocol)
5. OOB score: RF out-of-bag predictions (not truly held out)
"""

import logging
import os
import sys

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    StratifiedKFold, GridSearchCV, train_test_split,
)
from sklearn.metrics import (
    f1_score, roc_auc_score, accuracy_score, precision_score, recall_score,
    confusion_matrix,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/rf_hypotheses.log"),
    ],
)
logger = logging.getLogger(__name__)

# Paper's CM for reference
PAPER_TN, PAPER_FP, PAPER_FN, PAPER_TP = 153, 28, 37, 96
PAPER_F1 = 2 * PAPER_TP / (2 * PAPER_TP + PAPER_FP + PAPER_FN)


def smiles_to_morgan(smiles, radius=2, n_bits=2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.zeros(n_bits)
    return np.array(AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits))


def build_features(df):
    fps = np.array([smiles_to_morgan(s) for s in df["smiles"]])
    ha = df["ha_num"].fillna(df["ha_num"].median()).values.reshape(-1, 1)
    o = df["o_num"].fillna(df["o_num"].median()).values.reshape(-1, 1)
    return np.hstack([fps, ha, o])


def get_best_rf(X_train, y_train, seed=42):
    """Grid search matching paper's exact space."""
    param_grid = {
        "n_estimators": [100, 200, 300],
        "max_depth": [5, 10, 15],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
    }
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    grid = GridSearchCV(
        RandomForestClassifier(random_state=seed, n_jobs=-1),
        param_grid, cv=skf, scoring="f1", n_jobs=-1, refit=True,
    )
    grid.fit(X_train, y_train)
    return grid


def report(label, y_true, y_pred, y_prob=None):
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    f1 = f1_score(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    auc = roc_auc_score(y_true, y_prob) if y_prob is not None else 0

    match = "*** MATCH ***" if (tn == PAPER_TN and fp == PAPER_FP and fn == PAPER_FN and tp == PAPER_TP) else ""
    close = ""
    if not match and abs(f1 - PAPER_F1) < 0.03:
        close = "(close to paper)"

    print(
        f"  {label}\n"
        f"    CM: TN={tn} FP={fp} FN={fn} TP={tp}  |  "
        f"F1={f1:.4f}  Prec={prec:.4f}  Rec={rec:.4f}  Acc={acc:.4f}  "
        f"AUC={auc:.4f}  {match}{close}"
    )
    return {"label": label, "tn": tn, "fp": fp, "fn": fn, "tp": tp,
            "f1": f1, "prec": prec, "rec": rec, "acc": acc}


def main():
    os.makedirs("logs", exist_ok=True)

    df = pd.read_csv("data/T0.csv")
    X = build_features(df)
    y = df["bin_class"].values

    print(f"Data: {len(df)} molecules, {y.sum()} class 1, {(1-y).sum()} class 0")
    print(f"\nPaper's RF: TN={PAPER_TN} FP={PAPER_FP} FN={PAPER_FN} TP={PAPER_TP} "
          f"F1={PAPER_F1:.4f}")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 70)
    print("HYPOTHESIS 1: Train-set evaluation (fit all, predict all)")
    print("=" * 70)
    grid = get_best_rf(X, y, seed=42)
    print(f"  Best params: {grid.best_params_}")
    y_pred = grid.predict(X)
    y_prob = grid.predict_proba(X)[:, 1]
    report("H1: fit(all) → predict(all)", y, y_pred, y_prob)

    # ═══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("HYPOTHESIS 2: GridSearchCV refit predictions (still on train data)")
    print("=" * 70)
    # Same as H1 but being explicit — GridSearchCV with refit=True
    # refits on ALL data after finding best params
    report("H2: grid.predict(X_all) after refit", y, grid.predict(X), grid.predict_proba(X)[:, 1])

    # ═══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("HYPOTHESIS 3: Single 80/20 split (sweep seeds)")
    print("=" * 70)
    best_f1 = 0
    best_seed = 0
    results_h3 = []
    for seed in range(200):
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=seed,
        )
        rf = RandomForestClassifier(**grid.best_params_, random_state=42, n_jobs=-1)
        rf.fit(X_tr, y_tr)
        y_pred = rf.predict(X_te)
        f1 = f1_score(y_te, y_pred)
        cm = confusion_matrix(y_te, y_pred)
        results_h3.append({"seed": seed, "f1": f1, "cm": cm.ravel().tolist()})
        if f1 > best_f1:
            best_f1 = f1
            best_seed = seed

    f1s = [r["f1"] for r in results_h3]
    print(f"  200 seeds: F1 range = {min(f1s):.4f} – {max(f1s):.4f}, "
          f"mean = {np.mean(f1s):.4f} ± {np.std(f1s):.4f}")
    print(f"  Best seed = {best_seed}")

    # Show best
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=best_seed,
    )
    rf = RandomForestClassifier(**grid.best_params_, random_state=42, n_jobs=-1)
    rf.fit(X_tr, y_tr)
    report(f"H3: best 80/20 split (seed={best_seed})",
           y_te, rf.predict(X_te), rf.predict_proba(X_te)[:, 1])

    # ═══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("HYPOTHESIS 4: 80/20 split with grid search on train portion only")
    print("=" * 70)
    # Paper says: "split into 80:20, grid search CV on train, eval on test"
    for seed in [42, best_seed, 0, 1, 7, 123]:
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=seed,
        )
        grid_tr = get_best_rf(X_tr, y_tr, seed=seed)
        y_pred = grid_tr.predict(X_te)
        y_prob = grid_tr.predict_proba(X_te)[:, 1]
        report(f"H4: grid_search(80%) → predict(20%) seed={seed}",
               y_te, y_pred, y_prob)

    # ═══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("HYPOTHESIS 5: OOB predictions")
    print("=" * 70)
    rf_oob = RandomForestClassifier(
        **grid.best_params_, random_state=42, n_jobs=-1, oob_score=True,
    )
    rf_oob.fit(X, y)
    y_prob_oob = rf_oob.oob_decision_function_[:, 1]
    y_pred_oob = (y_prob_oob >= 0.5).astype(int)
    report("H5: OOB predictions (threshold=0.50)", y, y_pred_oob, y_prob_oob)
    # Also with 0.47
    y_pred_oob_47 = (y_prob_oob >= 0.47).astype(int)
    report("H5: OOB predictions (threshold=0.47)", y, y_pred_oob_47, y_prob_oob)

    # ═══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("HYPOTHESIS 6: Full-data fit, predict all, with threshold=0.47")
    print("=" * 70)
    y_prob_all = grid.predict_proba(X)[:, 1]
    for t in [0.30, 0.35, 0.40, 0.45, 0.47, 0.50]:
        y_pred_t = (y_prob_all >= t).astype(int)
        report(f"H6: fit(all) → predict(all) threshold={t:.2f}", y, y_pred_t, y_prob_all)

    # ═══════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("HYPOTHESIS 7: Aggregated CV predictions (our method) — sanity check")
    print("=" * 70)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    all_true, all_pred, all_prob = [], [], []
    for train_idx, test_idx in skf.split(X, y):
        rf = RandomForestClassifier(**grid.best_params_, random_state=42, n_jobs=-1)
        rf.fit(X[train_idx], y[train_idx])
        all_true.extend(y[test_idx].tolist())
        all_pred.extend(rf.predict(X[test_idx]).tolist())
        all_prob.extend(rf.predict_proba(X[test_idx])[:, 1].tolist())
    report("H7: aggregated 5-fold CV (held-out)", np.array(all_true),
           np.array(all_pred), np.array(all_prob))


if __name__ == "__main__":
    main()
