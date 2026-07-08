#!/usr/bin/env python
"""Diagnose kernel-matrix conditioning across n_qubits / reps / feature-map choice."""
import os, sys, time, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score
from qiskit.circuit.library import zz_feature_map, z_feature_map, pauli_feature_map
from qiskit.quantum_info import Statevector

csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/susy_5k.csv"))
df = pd.read_csv(csv, header=None)
y_all = df.iloc[:,0].astype(int).values
X_all = df.iloc[:,1:].values

def make_subset(n_events, n_features, seed=42):
    rng = np.random.default_rng(seed)
    pos = np.where(y_all==1)[0]; neg = np.where(y_all==0)[0]
    rng.shuffle(pos); rng.shuffle(neg)
    take = n_events//2
    idx = np.concatenate([pos[:take], neg[:take]]); rng.shuffle(idx)
    X = X_all[idx][:,:n_features]; y = y_all[idx]
    return MinMaxScaler(feature_range=(-np.pi, np.pi)).fit_transform(X), y

def q_kernel(X1, X2, fmap):
    svs1 = np.array([Statevector.from_instruction(fmap.assign_parameters(x)).data for x in X1])
    if X1 is X2:
        svs2 = svs1
    else:
        svs2 = np.array([Statevector.from_instruction(fmap.assign_parameters(x)).data for x in X2])
    return np.abs(svs1.conj() @ svs2.T)**2

def run(n_qubits, reps, fmap_kind, entang='linear', n_events=100, C=1.0):
    X, y = make_subset(n_events, n_qubits)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.5, stratify=y, random_state=42)
    if fmap_kind == 'zz':
        fm = zz_feature_map(feature_dimension=n_qubits, reps=reps, entanglement=entang)
    elif fmap_kind == 'z':
        fm = z_feature_map(feature_dimension=n_qubits, reps=reps)
    elif fmap_kind == 'pauli':
        fm = pauli_feature_map(feature_dimension=n_qubits, reps=reps, paulis=['Z','ZZ'], entanglement=entang)
    K_tr = q_kernel(Xtr, Xtr, fm)
    K_te = q_kernel(Xte, Xtr, fm)
    off_diag = K_tr[np.triu_indices_from(K_tr, k=1)]
    print(f"n_q={n_qubits} reps={reps} map={fmap_kind} entang={entang}: "
          f"off-diag mean={off_diag.mean():.3f} std={off_diag.std():.3f} "
          f"max={off_diag.max():.3f} min={off_diag.min():.3f}", end='')
    try:
        svc = SVC(kernel='precomputed', C=C)
        svc.fit(K_tr, ytr)
        s = svc.decision_function(K_te)
        auc = roc_auc_score(yte, s)
        acc = (svc.predict(K_te)==yte).mean()
        print(f"  => AUC={auc:.3f} ACC={acc:.3f}")
        return auc
    except Exception as e:
        print(f"  => SVC FAIL: {e}")
        return None

print("=== Diagnostic sweep ===\n")
# Try fewer qubits + rep counts + entanglement variations
for nq in [4, 8, 10, 15]:
    for reps in [1, 2]:
        for fmap in ['z','zz']:
            run(nq, reps, fmap)
    print()
