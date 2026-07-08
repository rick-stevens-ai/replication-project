#!/usr/bin/env python
"""Deeper diagnostic: multi-seed average + ZZ with reduced angle scale."""
import os, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score
from qiskit.circuit.library import zz_feature_map, z_feature_map
from qiskit.quantum_info import Statevector

csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/susy_5k.csv"))
df = pd.read_csv(csv, header=None)
y_all = df.iloc[:,0].astype(int).values
X_all = df.iloc[:,1:].values

def make_subset(n_events, n_features, seed, angle_scale=np.pi):
    rng = np.random.default_rng(seed)
    pos = np.where(y_all==1)[0]; neg = np.where(y_all==0)[0]
    rng.shuffle(pos); rng.shuffle(neg)
    take = n_events//2
    idx = np.concatenate([pos[:take], neg[:take]]); rng.shuffle(idx)
    X = X_all[idx][:,:n_features]; y = y_all[idx]
    return MinMaxScaler(feature_range=(-angle_scale, angle_scale)).fit_transform(X), y

def q_kernel(X1, X2, fmap):
    svs1 = np.array([Statevector.from_instruction(fmap.assign_parameters(x)).data for x in X1])
    svs2 = svs1 if X1 is X2 else np.array([Statevector.from_instruction(fmap.assign_parameters(x)).data for x in X2])
    return np.abs(svs1.conj() @ svs2.T)**2

def eval_config(n_qubits, reps, kind, angle, n_events, seeds):
    aucs = []
    for seed in seeds:
        X, y = make_subset(n_events, n_qubits, seed, angle_scale=angle)
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.5, stratify=y, random_state=seed)
        fm = z_feature_map(feature_dimension=n_qubits, reps=reps) if kind=='z' \
             else zz_feature_map(feature_dimension=n_qubits, reps=reps, entanglement='linear')
        K_tr = q_kernel(Xtr, Xtr, fm)
        K_te = q_kernel(Xte, Xtr, fm)
        svc = SVC(kernel='precomputed', C=1.0)
        svc.fit(K_tr, ytr)
        auc = roc_auc_score(yte, svc.decision_function(K_te))
        aucs.append(auc)
    aucs = np.array(aucs)
    return aucs.mean(), aucs.std(), aucs

seeds = [42, 7, 13, 21, 99]
print("=== Multi-seed diagnostic ===")
print("Averaging over 5 statistically-independent balanced datasets (analogous to paper's 60-dataset averaging)")
print()

# Reproduce paper Fig 8 point: 15q, 100 events
print("--- Paper Fig 8 target: 15 qubits, 100 events, AUC_sim=0.831 / AUC_hw=0.777 ---")
for kind in ['z','zz']:
    for reps in [1,2]:
        for angle in [np.pi, np.pi/2]:
            m, s, arr = eval_config(15, reps, kind, angle, 100, seeds)
            print(f"  n_q=15 map={kind} reps={reps} angle=±{angle:.3f}: mean AUC={m:.3f} ± {s:.3f}   ({arr.round(3)})")

print()
print("--- Best-config check at 10 qubits (paper Fig 6: 10q AUC ~ 0.89 at 20k events, expect lower at 100 ev) ---")
for kind in ['z','zz']:
    for reps in [1,2]:
        m, s, arr = eval_config(10, reps, kind, np.pi, 100, seeds)
        print(f"  n_q=10 map={kind} reps={reps}: mean AUC={m:.3f} ± {s:.3f}   ({arr.round(3)})")

print()
print("--- Scaling with events at best-config (15q, Z, reps=2) ---")
for n_ev in [100, 200, 400]:
    m, s, arr = eval_config(15, 2, 'z', np.pi, n_ev, seeds)
    print(f"  n_events={n_ev}: mean AUC={m:.3f} ± {s:.3f}   ({arr.round(3)})")
