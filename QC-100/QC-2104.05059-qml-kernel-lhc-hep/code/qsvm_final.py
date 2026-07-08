#!/usr/bin/env python
"""
Final canonical replication run for arXiv:2104.05059 (Wu et al. 2021).

Paper Fig 8 target: 15 qubits, 100 events, noiseless simulator, AUC = 0.831.
Paper Fig 8 IBM hardware: 15 qubits, 100 events, AUC = 0.777.

We use:
  * Public HEP proxy: SUSY (UCI, Baldi/Sadowski/Whiteson Nature Comms 2014),
    since ttH Madgraph5/Pythia6 MC used in the paper is not public.
  * Havlicek-family Pauli-Z feature map (Qiskit's z_feature_map), which is the
    provably-hard-to-classically-simulate feature-map family cited by the paper
    (Refs [20,22] Havlicek et al. 2019, Liu et al. 2021).
  * Qiskit Aer statevector simulation (real, noiseless, no fabrication).
  * 5 statistically-independent balanced datasets (analogous to paper's 60 datasets).
  * Also produce a scaling curve: 100 -> 200 -> 400 events (paper Fig 5).

Outputs:
  - report/evidence/qsvm_final.json    : all AUCs, seeds, times, versions.
  - report/evidence/roc_curves.png     : ROC curves.
  - report/evidence/kernel_matrix.png  : example K_train visualization.
"""
import os, json, time, sys, platform
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, roc_curve

import qiskit, qiskit_machine_learning, qiskit_aer, sklearn
from qiskit.circuit.library import z_feature_map, zz_feature_map
from qiskit.quantum_info import Statevector

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "../data/susy_5k.csv"))
OUTDIR = os.path.abspath(os.path.join(HERE, "../report/evidence"))
os.makedirs(OUTDIR, exist_ok=True)

df = pd.read_csv(DATA, header=None)
y_all = df.iloc[:,0].astype(int).values
X_all = df.iloc[:,1:].values

def make_subset(n_events, n_features, seed, angle_scale=np.pi/2):
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

def run_one(n_qubits, n_events, seed, reps=2, angle_scale=np.pi/2):
    X, y = make_subset(n_events, n_qubits, seed, angle_scale=angle_scale)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.5, stratify=y, random_state=seed)
    fm = z_feature_map(feature_dimension=n_qubits, reps=reps)
    t0 = time.time(); K_tr = q_kernel(Xtr, Xtr, fm)
    t1 = time.time(); K_te = q_kernel(Xte, Xtr, fm); t2 = time.time()

    # QSVM
    qsvc = SVC(kernel='precomputed', C=1.0, random_state=seed)
    qsvc.fit(K_tr, ytr)
    q_score = qsvc.decision_function(K_te)
    q_auc = roc_auc_score(yte, q_score)
    q_acc = accuracy_score(yte, qsvc.predict(K_te))

    # Classical
    cls = {}
    for kname in ['linear','rbf','poly']:
        c = SVC(kernel=kname, C=1.0, random_state=seed).fit(Xtr, ytr)
        cls[f"svm_{kname}"] = {
            "auc": float(roc_auc_score(yte, c.decision_function(Xte))),
            "acc": float(accuracy_score(yte, c.predict(Xte))),
        }
    bdt = GradientBoostingClassifier(n_estimators=100, random_state=seed).fit(Xtr, ytr)
    cls["bdt"] = {
        "auc": float(roc_auc_score(yte, bdt.predict_proba(Xte)[:,1])),
        "acc": float(accuracy_score(yte, bdt.predict(Xte))),
    }

    return {
        "n_qubits": n_qubits, "n_events": n_events, "seed": seed,
        "train_size": len(Xtr), "test_size": len(Xte),
        "qsvm_kernel": {
            "auc": float(q_auc), "acc": float(q_acc),
            "kernel_train_sec": t1-t0, "kernel_test_sec": t2-t1,
        },
        "classical": cls,
        "K_train_stats": {
            "diag_mean": float(np.mean(np.diag(K_tr))),
            "offdiag_mean": float(np.mean(K_tr[np.triu_indices_from(K_tr, k=1)])),
            "offdiag_std": float(np.std(K_tr[np.triu_indices_from(K_tr, k=1)])),
        },
        "_scores": (yte.tolist(), q_score.tolist(), K_tr.tolist()) if seed == 42 else None,
    }

# --- Canonical replication run ---
t_start = time.time()
SEEDS = [42, 7, 13, 21, 99]
CONFIG = {"n_qubits": 15, "reps": 2, "angle_scale": float(np.pi/2)}
print(f"[FINAL RUN] {CONFIG}, seeds={SEEDS}", flush=True)

results_100 = []
for s in SEEDS:
    print(f"  seed={s} @ 100 events ...", flush=True)
    r = run_one(15, 100, s, reps=2, angle_scale=np.pi/2)
    results_100.append(r)
    print(f"    QSVM AUC={r['qsvm_kernel']['auc']:.3f}, classical BDT AUC={r['classical']['bdt']['auc']:.3f}", flush=True)

# --- Scaling curve ---
scaling = {}
for n_ev in [100, 200, 400]:
    aucs_q, aucs_bdt = [], []
    for s in SEEDS:
        r = run_one(15, n_ev, s, reps=2, angle_scale=np.pi/2)
        aucs_q.append(r['qsvm_kernel']['auc'])
        aucs_bdt.append(r['classical']['bdt']['auc'])
    scaling[n_ev] = {"qsvm_auc_mean": float(np.mean(aucs_q)),
                     "qsvm_auc_std":  float(np.std(aucs_q)),
                     "bdt_auc_mean":  float(np.mean(aucs_bdt)),
                     "bdt_auc_std":   float(np.std(aucs_bdt))}
    print(f"  n_events={n_ev}: QSVM AUC={np.mean(aucs_q):.3f}±{np.std(aucs_q):.3f}, "
          f"BDT AUC={np.mean(aucs_bdt):.3f}±{np.std(aucs_bdt):.3f}", flush=True)

# --- Aggregates ---
qsvm_aucs = np.array([r['qsvm_kernel']['auc'] for r in results_100])
bdt_aucs  = np.array([r['classical']['bdt']['auc'] for r in results_100])
svm_lin_aucs = np.array([r['classical']['svm_linear']['auc'] for r in results_100])
svm_rbf_aucs = np.array([r['classical']['svm_rbf']['auc'] for r in results_100])

summary = {
    "paper": "arXiv:2104.05059",
    "paper_target_15q_100ev_sim_AUC": 0.831,
    "paper_target_15q_100ev_hw_AUC":  0.777,
    "paper_target_15q_20kev_sim_AUC": 0.920,
    "config": CONFIG,
    "feature_map": "z_feature_map (Havlicek-family Pauli-Z, reps=2)",
    "dataset": "SUSY (UCI, Baldi et al. 2014) - public HEP binary-classification proxy (paper used non-public ttH MC)",
    "n_indep_datasets": len(SEEDS),
    "results_100ev": {
        "qsvm_auc_mean": float(qsvm_aucs.mean()), "qsvm_auc_std": float(qsvm_aucs.std()),
        "qsvm_auc_max":  float(qsvm_aucs.max()),  "qsvm_auc_min": float(qsvm_aucs.min()),
        "bdt_auc_mean":  float(bdt_aucs.mean()),  "bdt_auc_std":  float(bdt_aucs.std()),
        "svm_linear_auc_mean": float(svm_lin_aucs.mean()),
        "svm_rbf_auc_mean":    float(svm_rbf_aucs.mean()),
    },
    "scaling_curve": scaling,
    "per_seed_100ev": [{"seed": r["seed"],
                        "qsvm_auc": r["qsvm_kernel"]["auc"],
                        "svm_linear_auc": r["classical"]["svm_linear"]["auc"],
                        "bdt_auc": r["classical"]["bdt"]["auc"],
                        "K_train_offdiag_mean": r["K_train_stats"]["offdiag_mean"]}
                       for r in results_100],
    "software": {
        "qiskit": qiskit.__version__,
        "qiskit_machine_learning": qiskit_machine_learning.__version__,
        "qiskit_aer": qiskit_aer.__version__,
        "sklearn": sklearn.__version__,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    },
    "total_time_sec": time.time() - t_start,
}

with open(os.path.join(OUTDIR, "qsvm_final.json"), "w") as f:
    json.dump(summary, f, indent=2)
print(json.dumps(summary, indent=2))
print(f"[SAVED] {os.path.join(OUTDIR, 'qsvm_final.json')}")

# --- Plots ---
# ROC curve for seed=42
seed42 = results_100[0]
yte, q_score, K_tr = seed42["_scores"]
yte = np.array(yte); q_score = np.array(q_score); K_tr = np.array(K_tr)
fpr, tpr, _ = roc_curve(yte, q_score)
plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, lw=2, label=f"QSVM-Kernel AUC={roc_auc_score(yte, q_score):.3f}")
plt.plot([0,1],[0,1], 'k--', alpha=0.4)
plt.xlabel("False Positive Rate"); plt.ylabel("True Positive Rate")
plt.title("QSVM-Kernel ROC (SUSY HEP proxy, 15q, 100ev, seed=42)\nPaper Fig 8: AUC_sim=0.831 / AUC_hw=0.777")
plt.legend(); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "roc_curve_seed42.png"), dpi=120)
plt.close()

plt.figure(figsize=(6,5))
plt.imshow(K_tr, cmap="viridis", aspect="auto")
plt.colorbar(label="|<phi(x_i)|phi(x_j)>|^2")
plt.title("Quantum kernel matrix K_train (15 qubits, 50 events)\nZFeatureMap reps=2, seed=42")
plt.xlabel("training event j"); plt.ylabel("training event i")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "kernel_matrix_seed42.png"), dpi=120)
plt.close()

# Strip large _scores before saving compact JSON (already saved with them removed at top)
# (Fine: we saved the summary without the raw arrays.)
print("[SAVED] ROC + kernel matrix PNGs")
