#!/usr/bin/env python
"""
Independent replication of arXiv:2104.05059 (Wu et al. 2021)
"Application of QML using the Quantum Kernel Algorithm on HEP Analysis at the LHC"

Implements the QSVM-Kernel pipeline:
  - Quantum feature map (ZZFeatureMap; paper uses a custom map inspired by Havlicek et al.
    but we use Qiskit's ZZFeatureMap which is the same family of pauli-encoding maps
    conjectured to be hard to simulate classically -- see paper refs [20,22]).
  - Compute the quantum kernel matrix via inner products |<phi(x_i)|phi(x_j)>|^2
    on a statevector simulator (Qiskit Aer).
  - Feed the precomputed kernel to sklearn SVC (kernel='precomputed').
  - Compare against classical linear/RBF/poly SVMs and a BDT (XGBoost-style: GradientBoostingClassifier).

Paper headline (Figure 8): with 15 qubits, 100 events (50 train / 50 test),
noiseless simulator, AUC = 0.831. We reproduce this on the SUSY UCI HEP dataset
(public HEP-like binary classification proxy) at the SAME instance size.

Small caveats vs paper:
  * Paper uses proprietary ttH Monte Carlo (Madgraph5+Pythia6+Delphes); we substitute
    the public UCI SUSY dataset (Baldi, Sadowski & Whiteson 2014, Nature Comms).
  * Paper uses a custom feature map with "B gates" (rotation around z by (x_k-1+x_k)/2 * d);
    we use Qiskit's ZZFeatureMap which is the closest built-in analogue in the same
    Havlicek et al. family.
Result: If AUC on public HEP proxy is comparable (>0.75 at 100 events / 15 qubits),
this validates the METHOD; matching the exact numerical 0.831 on a different dataset
is not expected -- see REPORT.md for the correct verdict framing.
"""
import json, sys, time, argparse, pathlib, os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, accuracy_score

from qiskit.circuit.library import ZZFeatureMap, zz_feature_map
from qiskit_aer import AerSimulator
from qiskit import transpile
from qiskit.quantum_info import Statevector

def load_susy_subset(csv_path, n_events, n_features, seed):
    """Load a balanced subset of SUSY, take first n_features columns."""
    df = pd.read_csv(csv_path, header=None)
    y = df.iloc[:, 0].astype(int).values
    X = df.iloc[:, 1:].values
    # Balance classes
    rng = np.random.default_rng(seed)
    pos_idx = np.where(y == 1)[0]
    neg_idx = np.where(y == 0)[0]
    rng.shuffle(pos_idx); rng.shuffle(neg_idx)
    take = n_events // 2
    idx = np.concatenate([pos_idx[:take], neg_idx[:take]])
    rng.shuffle(idx)
    Xs = X[idx][:, :n_features]
    ys = y[idx]
    return Xs, ys

def build_feature_map(n_qubits, reps=2):
    """Havlicek-family Pauli-Z feature map with entanglement (paper Fig 3b analogue).
    Use the function form (Qiskit 2.1+): returns a fully-decomposed QuantumCircuit."""
    fm = zz_feature_map(feature_dimension=n_qubits, reps=reps, entanglement='linear')
    return fm

def quantum_kernel_matrix(X1, X2, feature_map):
    """Compute |<phi(x)|phi(y)>|^2 kernel matrix via statevector."""
    # Precompute all statevectors for X1
    n1 = len(X1); n2 = len(X2)
    print(f"  Computing {n1} statevectors for set 1...", flush=True)
    svs1 = []
    for i, x in enumerate(X1):
        qc = feature_map.assign_parameters(x)
        sv = Statevector.from_instruction(qc)
        svs1.append(sv.data)
        if (i+1) % 20 == 0: print(f"    {i+1}/{n1}", flush=True)
    svs1 = np.array(svs1)  # (n1, 2^n)
    same = (X1 is X2)
    if same:
        svs2 = svs1
    else:
        print(f"  Computing {n2} statevectors for set 2...", flush=True)
        svs2 = []
        for i, x in enumerate(X2):
            qc = feature_map.assign_parameters(x)
            sv = Statevector.from_instruction(qc)
            svs2.append(sv.data)
            if (i+1) % 20 == 0: print(f"    {i+1}/{n2}", flush=True)
        svs2 = np.array(svs2)
    print(f"  Computing kernel matrix ({n1} x {n2})...", flush=True)
    # K[i,j] = |<sv1_i | sv2_j>|^2
    inner = svs1.conj() @ svs2.T  # (n1, n2)
    K = np.abs(inner) ** 2
    return K

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="../data/susy_5k.csv")
    ap.add_argument("--n_qubits", type=int, default=15,
                    help="Number of qubits = number of input features (paper: 15).")
    ap.add_argument("--n_events", type=int, default=100,
                    help="Total events (paper Fig 8: 100 = 50 train / 50 test).")
    ap.add_argument("--reps", type=int, default=2, help="Feature map repetitions.")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="../report/evidence/qsvm_result.json")
    args = ap.parse_args()

    t_start = time.time()
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), args.data))
    print(f"[QSVM-Kernel replication] loading SUSY from {csv_path}", flush=True)
    X, y = load_susy_subset(csv_path, args.n_events, args.n_qubits, args.seed)
    print(f"  Loaded X={X.shape}, y balance={np.bincount(y)}", flush=True)

    # Feature scaling: Havlicek/Wu-family Pauli-Z maps encode features as rotation angles.
    # Paper scales inputs to O(1) range (Sec IIID); using [-pi, pi] gives full angular
    # coverage and matches the ZZFeatureMap convention.
    scaler = MinMaxScaler(feature_range=(-np.pi, np.pi))
    Xs = scaler.fit_transform(X)

    # Split 50/50 (paper Fig 8: 100 events, 50 train / 50 test)
    X_tr, X_te, y_tr, y_te = train_test_split(Xs, y, test_size=0.5, random_state=args.seed,
                                              stratify=y)

    print(f"[Build feature map] n_qubits={args.n_qubits}, reps={args.reps}", flush=True)
    fmap = build_feature_map(args.n_qubits, reps=args.reps)
    print(f"  Circuit depth={fmap.depth()}, params={fmap.num_parameters}", flush=True)

    # --- Quantum kernel training ---
    print(f"[Compute training kernel] {len(X_tr)}x{len(X_tr)}", flush=True)
    t0 = time.time()
    K_train = quantum_kernel_matrix(X_tr, X_tr, fmap)
    t_train_k = time.time() - t0
    print(f"  Training kernel done in {t_train_k:.1f}s. Symm err = {np.max(np.abs(K_train - K_train.T)):.2e}", flush=True)

    print(f"[Compute test kernel] {len(X_te)}x{len(X_tr)}", flush=True)
    t0 = time.time()
    K_test = quantum_kernel_matrix(X_te, X_tr, fmap)
    t_test_k = time.time() - t0
    print(f"  Test kernel done in {t_test_k:.1f}s", flush=True)

    # --- QSVM training ---
    print("[Train QSVM with precomputed quantum kernel]", flush=True)
    qsvc = SVC(kernel='precomputed', C=1.0, random_state=args.seed)
    qsvc.fit(K_train, y_tr)
    y_pred_q = qsvc.predict(K_test)
    y_score_q = qsvc.decision_function(K_test)
    auc_q = roc_auc_score(y_te, y_score_q)
    acc_q = accuracy_score(y_te, y_pred_q)
    print(f"  QSVM-Kernel AUC={auc_q:.4f}, ACC={acc_q:.4f}", flush=True)

    # --- Classical baselines ---
    print("[Classical baselines]", flush=True)
    results_classical = {}
    for name, ker in [("linear","linear"), ("rbf","rbf"), ("poly","poly")]:
        clf = SVC(kernel=ker, C=1.0, random_state=args.seed)
        clf.fit(X_tr, y_tr)
        s = clf.decision_function(X_te)
        auc = roc_auc_score(y_te, s)
        acc = accuracy_score(y_te, clf.predict(X_te))
        results_classical[f"svm_{name}"] = {"auc": auc, "acc": acc}
        print(f"  SVM-{name}: AUC={auc:.4f}, ACC={acc:.4f}", flush=True)

    bdt = GradientBoostingClassifier(n_estimators=100, random_state=args.seed)
    bdt.fit(X_tr, y_tr)
    s = bdt.predict_proba(X_te)[:,1]
    auc_bdt = roc_auc_score(y_te, s)
    acc_bdt = accuracy_score(y_te, bdt.predict(X_te))
    results_classical["bdt"] = {"auc": auc_bdt, "acc": acc_bdt}
    print(f"  BDT: AUC={auc_bdt:.4f}, ACC={acc_bdt:.4f}", flush=True)

    total_time = time.time() - t_start

    result = {
        "paper": "arXiv:2104.05059",
        "instance": {
            "n_qubits": args.n_qubits,
            "n_events": args.n_events,
            "train_size": len(X_tr),
            "test_size": len(X_te),
            "feature_map": f"ZZFeatureMap(reps={args.reps}, entanglement=linear)",
            "dataset": "SUSY (UCI, Baldi et al. 2014) - HEP proxy for ttH",
            "seed": args.seed,
        },
        "qsvm_kernel": {
            "auc": float(auc_q),
            "acc": float(acc_q),
            "kernel_train_sec": t_train_k,
            "kernel_test_sec": t_test_k,
        },
        "classical": results_classical,
        "paper_reference_points": {
            "fig8_qsvm_sim_noiseless_15q_100ev_AUC": 0.831,
            "fig8_qsvm_ibm_hardware_15q_100ev_AUC": 0.777,
            "fig4_qsvm_sim_15q_20kev_AUC": 0.920,
        },
        "total_time_sec": total_time,
    }
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), args.out))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[DONE] total time = {total_time:.1f}s. Results -> {out_path}", flush=True)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
