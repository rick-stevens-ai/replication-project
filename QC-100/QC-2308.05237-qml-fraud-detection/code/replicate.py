#!/usr/bin/env python3
"""
Independent replication of arXiv:2308.05237
"Financial Fraud Detection: A Comparative Study of Quantum Machine Learning Models"
Innan, Khan, Bennai (2023)

Reproducing: QSVC (Quantum Support Vector Classifier), VQC (Variational Quantum
Classifier) with three feature maps (ZFeatureMap, ZZFeatureMap, PauliFeatureMap)
on a 200-record balanced BankSim-style fraud dataset, per Table II.

Also runs a classical baseline (Logistic Regression + classical SVM) for reference.

Uses qiskit 2.5 + qiskit-machine-learning 0.9 + qiskit-aer.
"""
import json
import os
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC as ClassicalSVC
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    classification_report,
)

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------
# 1. Reproducibility
# ---------------------------------------------------------------
SEED = 42
np.random.seed(SEED)

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------
# 2. Synthetic BankSim-style dataset (200 balanced records)
#
# Paper Sec. IV.A specifies:
#   - 200 records: 100 fraud + 100 non-fraud (balanced)
#   - Features selected: age, gender, category, amount
#   - Fraud payments: mean ~567.23, std ~128.47
#   - Non-fraud payments: mean ~145.68, std ~50.32
#   - "sports & toys" + "health" over-represented in fraud
#   - Age 26-35 (category "2") and female (56%) over-represented in fraud
# ---------------------------------------------------------------
CATEGORIES = [
    "es_transportation", "es_health", "es_otherservices",
    "es_food", "es_hotelservices", "es_barsandrestaurants",
    "es_tech", "es_sportsandtoys", "es_wellnessandbeauty",
    "es_hyper", "es_fashion", "es_home", "es_leisure",
    "es_travel", "es_contents",
]
GENDERS = ["F", "M", "E", "U"]
AGE_CATS = ["0", "1", "2", "3", "4", "5", "6", "U"]


def make_banksim_like(n_per_class=100, seed=SEED):
    rng = np.random.default_rng(seed)

    # ---- fraud rows ----
    n = n_per_class
    fraud_age_probs = np.array([0.02, 0.15, 0.45, 0.20, 0.10, 0.05, 0.02, 0.01])
    fraud_age_probs /= fraud_age_probs.sum()
    fraud_age = rng.choice(AGE_CATS, size=n, p=fraud_age_probs)

    fraud_gender_probs = np.array([0.56, 0.34, 0.05, 0.05])  # F,M,E,U
    fraud_gender_probs /= fraud_gender_probs.sum()
    fraud_gender = rng.choice(GENDERS, size=n, p=fraud_gender_probs)

    fraud_cat_probs = np.zeros(len(CATEGORIES))
    for i, c in enumerate(CATEGORIES):
        if c == "es_sportsandtoys":
            fraud_cat_probs[i] = 0.20
        elif c == "es_health":
            fraud_cat_probs[i] = 0.15
        elif c == "es_wellnessandbeauty":
            fraud_cat_probs[i] = 0.12
        elif c == "es_hotelservices":
            fraud_cat_probs[i] = 0.10
        elif c == "es_travel":
            fraud_cat_probs[i] = 0.08
        elif c == "es_leisure":
            fraud_cat_probs[i] = 0.07
        elif c == "es_hyper":
            fraud_cat_probs[i] = 0.06
        elif c == "es_otherservices":
            fraud_cat_probs[i] = 0.06
        elif c == "es_home":
            fraud_cat_probs[i] = 0.05
        elif c == "es_tech":
            fraud_cat_probs[i] = 0.04
        elif c == "es_fashion":
            fraud_cat_probs[i] = 0.04
        else:
            fraud_cat_probs[i] = 0.03
    fraud_cat_probs /= fraud_cat_probs.sum()
    fraud_cat = rng.choice(CATEGORIES, size=n, p=fraud_cat_probs)

    # Amount: mean 567.23, std 128.47 (paper Fig. 8 stats)
    fraud_amt = rng.normal(loc=567.23, scale=128.47, size=n)
    fraud_amt = np.clip(fraud_amt, 20.0, 1500.0)

    # ---- non-fraud rows ----
    nf_age_probs = np.array([0.05, 0.15, 0.20, 0.25, 0.15, 0.10, 0.05, 0.05])
    nf_age_probs /= nf_age_probs.sum()
    nf_age = rng.choice(AGE_CATS, size=n, p=nf_age_probs)

    nf_gender_probs = np.array([0.44, 0.50, 0.03, 0.03])
    nf_gender_probs /= nf_gender_probs.sum()
    nf_gender = rng.choice(GENDERS, size=n, p=nf_gender_probs)

    nf_cat_probs = np.ones(len(CATEGORIES))
    # Give non-fraud a different flavor
    for i, c in enumerate(CATEGORIES):
        if c == "es_transportation":
            nf_cat_probs[i] = 4.0
        elif c == "es_food":
            nf_cat_probs[i] = 3.0
        elif c == "es_barsandrestaurants":
            nf_cat_probs[i] = 2.5
        elif c == "es_health":
            nf_cat_probs[i] = 1.2
        elif c == "es_sportsandtoys":
            nf_cat_probs[i] = 0.5
    nf_cat_probs /= nf_cat_probs.sum()
    nf_cat = rng.choice(CATEGORIES, size=n, p=nf_cat_probs)

    nf_amt = rng.normal(loc=145.68, scale=50.32, size=n)
    nf_amt = np.clip(nf_amt, 5.0, 400.0)

    fraud_df = pd.DataFrame({
        "age": fraud_age, "gender": fraud_gender,
        "category": fraud_cat, "amount": fraud_amt, "fraud": 1,
    })
    nf_df = pd.DataFrame({
        "age": nf_age, "gender": nf_gender,
        "category": nf_cat, "amount": nf_amt, "fraud": 0,
    })
    df = pd.concat([fraud_df, nf_df], ignore_index=True)
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return df


def preprocess(df):
    """Follow paper Sec. IV.B: convert 'age' to int (regex strip 'U'->8),
    LabelEncode 'gender' and 'category', keep 'amount'."""
    df = df.copy()
    df["age"] = df["age"].replace({"U": "8"}).astype(int)
    df["gender"] = LabelEncoder().fit_transform(df["gender"].astype(str))
    df["category"] = LabelEncoder().fit_transform(df["category"].astype(str))
    return df


# ---------------------------------------------------------------
# 3. Classical baselines
# ---------------------------------------------------------------
def classical_baselines(X_train, X_test, y_train, y_test):
    out = {}
    for name, clf in [
        ("LogisticRegression", LogisticRegression(max_iter=2000, random_state=SEED)),
        ("ClassicalSVC_rbf", ClassicalSVC(kernel="rbf", random_state=SEED)),
        ("ClassicalSVC_linear", ClassicalSVC(kernel="linear", random_state=SEED)),
    ]:
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        out[name] = _score(y_test, y_pred)
    return out


def _score(y_true, y_pred):
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision_class0": float(precision_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "recall_class0": float(recall_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "f1_class0": float(f1_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "precision_class1": float(precision_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "recall_class1": float(recall_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "f1_class1": float(f1_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
    }


# ---------------------------------------------------------------
# 4. Quantum models: QSVC + VQC across three feature maps
# ---------------------------------------------------------------
def get_feature_map(name, feature_dim, reps=2):
    from qiskit.circuit.library import ZFeatureMap, ZZFeatureMap, PauliFeatureMap
    if name == "ZFeatureMap":
        return ZFeatureMap(feature_dimension=feature_dim, reps=reps)
    if name == "ZZFeatureMap":
        return ZZFeatureMap(feature_dimension=feature_dim, reps=reps, entanglement="linear")
    if name == "PauliFeatureMap":
        return PauliFeatureMap(
            feature_dimension=feature_dim, reps=reps,
            paulis=["Z", "Y", "ZZ"], entanglement="linear",
        )
    raise ValueError(name)


def run_qsvc(fmap_name, X_train, X_test, y_train, y_test):
    from qiskit_machine_learning.algorithms import QSVC
    from qiskit_machine_learning.kernels import FidelityQuantumKernel

    fmap = get_feature_map(fmap_name, feature_dim=X_train.shape[1], reps=2)
    kernel = FidelityQuantumKernel(feature_map=fmap)
    t0 = time.time()
    qsvc = QSVC(quantum_kernel=kernel)
    qsvc.fit(X_train, y_train)
    y_pred = qsvc.predict(X_test)
    dt = time.time() - t0
    scores = _score(y_test, y_pred)
    scores["train_predict_seconds"] = dt
    return scores


def run_vqc(fmap_name, X_train, X_test, y_train, y_test, maxiter=200):
    from qiskit.circuit.library import RealAmplitudes
    from qiskit_machine_learning.algorithms.classifiers import VQC
    from qiskit_machine_learning.optimizers import COBYLA

    fmap = get_feature_map(fmap_name, feature_dim=X_train.shape[1], reps=2)
    ansatz = RealAmplitudes(num_qubits=X_train.shape[1], reps=3)

    loss_history = []

    def cb(_weights, val):
        loss_history.append(float(val))

    t0 = time.time()
    vqc = VQC(
        feature_map=fmap,
        ansatz=ansatz,
        optimizer=COBYLA(maxiter=maxiter),
        callback=cb,
    )
    vqc.fit(X_train, y_train)
    y_pred = vqc.predict(X_test)
    dt = time.time() - t0
    scores = _score(y_test, y_pred)
    scores["train_predict_seconds"] = dt
    scores["final_loss"] = loss_history[-1] if loss_history else None
    scores["loss_history"] = loss_history
    return scores


# ---------------------------------------------------------------
# 5. Main driver
# ---------------------------------------------------------------
def main():
    print("=" * 72)
    print("Replication of arXiv:2308.05237 (Innan et al. 2023)")
    print("Financial Fraud Detection: Comparative Study of QML Models")
    print("=" * 72)

    # ---- Dataset ----
    print("\n[1] Building 200-record BankSim-style balanced fraud dataset ...")
    df_raw = make_banksim_like(n_per_class=100, seed=SEED)
    df_raw.to_csv(RESULTS_DIR.parent / "data" / "banksim_like_200.csv", index=False)
    print(f"    Rows: {len(df_raw)}, fraud={int((df_raw.fraud==1).sum())},"
          f" nonfraud={int((df_raw.fraud==0).sum())}")
    print(f"    Fraud amount mean={df_raw.loc[df_raw.fraud==1,'amount'].mean():.2f},"
          f" nonfraud mean={df_raw.loc[df_raw.fraud==0,'amount'].mean():.2f}")

    # ---- Preprocess ----
    df = preprocess(df_raw)
    X = df[["age", "gender", "category", "amount"]].values.astype(float)
    y = df["fraud"].values.astype(int)

    # Feature scale — QML feature maps need bounded inputs
    scaler = MinMaxScaler(feature_range=(0.0, np.pi))
    X_scaled = scaler.fit_transform(X)

    X_tr, X_te, y_tr, y_te = train_test_split(
        X_scaled, y, test_size=0.25, random_state=SEED, stratify=y,
    )
    print(f"    Train={len(X_tr)}  Test={len(X_te)}  Features={X_tr.shape[1]}")

    results = {"paper_arxiv_id": "2308.05237", "seed": SEED}

    # ---- Classical baselines ----
    print("\n[2] Classical baselines ...")
    results["classical"] = classical_baselines(X_tr, X_te, y_tr, y_te)
    for k, v in results["classical"].items():
        print(f"    {k:24s} acc={v['accuracy']:.3f} f1_macro={v['f1_macro']:.3f}")

    # ---- Quantum: QSVC across 3 feature maps ----
    fmaps = ["ZFeatureMap", "ZZFeatureMap", "PauliFeatureMap"]
    results["qsvc"] = {}
    print("\n[3] QSVC (Quantum Support Vector Classifier) ...")
    for fm in fmaps:
        print(f"    -> {fm} ...", flush=True)
        try:
            s = run_qsvc(fm, X_tr, X_te, y_tr, y_te)
            results["qsvc"][fm] = s
            print(f"       acc={s['accuracy']:.3f}  f1_c0={s['f1_class0']:.3f}"
                  f"  f1_c1={s['f1_class1']:.3f}  time={s['train_predict_seconds']:.1f}s")
        except Exception as e:
            results["qsvc"][fm] = {"error": repr(e)}
            print(f"       FAIL: {e!r}")

    # ---- Quantum: VQC across 3 feature maps ----
    results["vqc"] = {}
    print("\n[4] VQC (Variational Quantum Classifier), COBYLA maxiter=200 ...")
    for fm in fmaps:
        print(f"    -> {fm} ...", flush=True)
        try:
            s = run_vqc(fm, X_tr, X_te, y_tr, y_te, maxiter=200)
            results["vqc"][fm] = s
            print(f"       acc={s['accuracy']:.3f}  f1_c0={s['f1_class0']:.3f}"
                  f"  f1_c1={s['f1_class1']:.3f}  loss={s['final_loss']}"
                  f"  time={s['train_predict_seconds']:.1f}s")
        except Exception as e:
            results["vqc"][fm] = {"error": repr(e)}
            print(f"       FAIL: {e!r}")

    # ---- Persist ----
    out = RESULTS_DIR / "replication_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[5] Saved: {out}")

    # ---- Headline compare ----
    zf_qsvc = results["qsvc"].get("ZFeatureMap", {})
    paper_qsvc_zf_f1 = 0.98
    if "f1_class1" in zf_qsvc:
        our = zf_qsvc["f1_class1"]
        print(f"\n=== HEADLINE ===  paper QSVC/ZFeatureMap F1 (Class 1) = {paper_qsvc_zf_f1}")
        print(f"                  ours                    F1 (Class 1) = {our:.3f}")
        delta = abs(our - paper_qsvc_zf_f1)
        print(f"                  |Δ| = {delta:.3f}  (tolerance 0.10 for synthetic-data replication)")

    print("\nDone.")
    return results


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
