#!/usr/bin/env python3
"""
Independent replication of Shaydulin & Wild (2021), arXiv:2111.05451
"Importance of Kernel Bandwidth in Quantum Machine Learning"

Central claim being tested (Fig. 1b / Fig. 2):
  For a fixed quantum feature map, the SVC accuracy is a non-monotonic function
  of the bandwidth (scaling factor) lambda applied to the inputs:
    - small lambda -> kernel is near-identity (over-wide, underfitting)   --> low acc
    - large lambda -> exponential concentration (over-narrow)             --> low acc  (approach ~0.5)
    - intermediate lambda gives the best accuracy.

Feature map: IQP-style (Eq. 5 of the paper) with tunable scaling factor lambda.
  U_Z(x) = exp[ i * ( sum_j lambda*x_j Z_j + sum_{j<j'} lambda^2 x_j x_{j'} Z_j Z_{j'} ) ]
  applied twice (encoding depth 2) sandwiched between H layers, standard IQP layout.

Kernel: fidelity kernel  k(x, x') = |<phi(x')|phi(x)>|^2, exact statevector sim.
Classifier: sklearn SVC(kernel='precomputed').

Dataset: sklearn make_moons (binary), n_qubits = 4 (=> 4 features), small subset
so the O(N^2) kernel matrix runs in minutes on CPU.

Bandwidth grid: lambda in {0.01, 0.05, 0.1, 0.3, 1.0, 3.0, 10.0}  (7 values, spans
the underfitting -> optimal -> overfitting-concentration regime).

Outputs:
  report/evidence/bandwidth_sweep.csv
  report/evidence/bandwidth_sweep.json
  figures/accuracy_vs_bandwidth.png
"""
import os, sys, json, time, csv, math
import numpy as np
import pennylane as qml
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EVIDENCE = os.path.join(ROOT, "report", "evidence")
FIGURES  = os.path.join(ROOT, "figures")
LOGS     = os.path.join(ROOT, "logs")
os.makedirs(EVIDENCE, exist_ok=True)
os.makedirs(FIGURES,  exist_ok=True)
os.makedirs(LOGS,     exist_ok=True)

# -------------------------------
# Config
# -------------------------------
SEED = 20260703
N_QUBITS = 4                  # matches d = 4 features
N_TRAIN  = 40
N_TEST   = 40
LAMBDAS  = [0.01, 0.05, 0.1, 0.3, 1.0, 3.0, 10.0]
DATASET_NOISE = 0.20

# -------------------------------
# Data: make_moons + expand to 4 features via feature engineering
# The paper uses PCA-reduced high-dim datasets; we use a simple 2->4 map
# so we have a 4-qubit feature map exercising all IQP entangling terms.
# -------------------------------
def build_data(seed=SEED):
    X, y = make_moons(n_samples=(N_TRAIN + N_TEST), noise=DATASET_NOISE, random_state=seed)
    # Standardize to mean=0 std=1 (matches paper's data assumption for scaling factor).
    X = StandardScaler().fit_transform(X)
    # Expand 2 -> 4 features with simple deterministic nonlinear lifts.
    # These provide 4 real-valued features per point without breaking the moons structure.
    x1, x2 = X[:, 0], X[:, 1]
    X4 = np.stack([x1, x2, np.sin(x1), np.cos(x2)], axis=1)
    # Restandardize after lift so features are on a common scale.
    X4 = StandardScaler().fit_transform(X4)
    Xtr, Xte, ytr, yte = train_test_split(
        X4, y, train_size=N_TRAIN, test_size=N_TEST, random_state=seed, stratify=y
    )
    return Xtr, Xte, ytr, yte

# -------------------------------
# Quantum feature map (IQP-style, Eq. 5 of paper, single-repetition IQP layer)
#   U(x) = H^{\otimes n} exp(i H_Z(x)) H^{\otimes n} exp(i H_Z(x))
#   H_Z(x) = sum_j lambda x_j Z_j + sum_{j<j'} lambda^2 (x_j x_{j'}) Z_j Z_{j'}
# -------------------------------
def iqp_layer(x, wires, lam):
    n = len(wires)
    # single-qubit Z rotations: exp(-i * theta/2 * Z)  =>  we want phase exp(i * lambda * x_j * Z_j)
    # Use PauliZ rotation with angle 2*lambda*x_j (RZ(theta)=exp(-i theta/2 Z))
    for j in range(n):
        qml.RZ(-2.0 * lam * x[j], wires=wires[j])
    # two-qubit ZZ interactions with angle 2 * lambda^2 * x_j * x_{j'}
    for j in range(n):
        for k in range(j + 1, n):
            qml.IsingZZ(-2.0 * (lam ** 2) * x[j] * x[k], wires=[wires[j], wires[k]])

def feature_map(x, wires, lam, depth=2):
    for _ in range(depth):
        for w in wires:
            qml.Hadamard(wires=w)
        iqp_layer(x, wires, lam)

# Build a device + statevector-return QNode; we compute fidelity as |<phi(x')|phi(x)>|^2.
DEV = qml.device("default.qubit", wires=N_QUBITS)

@qml.qnode(DEV, interface="numpy")
def state_circuit(x, lam):
    feature_map(x, wires=range(N_QUBITS), lam=lam)
    return qml.state()

def kernel_matrix(X1, X2, lam):
    """Fidelity kernel matrix K[i,j] = |<phi(X2[j])|phi(X1[i])>|^2."""
    # Precompute all statevectors for X1 and X2 (statevector sim; no shots).
    S1 = np.array([state_circuit(x, lam) for x in X1])
    if X1 is X2:
        S2 = S1
    else:
        S2 = np.array([state_circuit(x, lam) for x in X2])
    # inner products
    inner = S1.conj() @ S2.T
    return np.abs(inner) ** 2

def run_one_lambda(lam, Xtr, Xte, ytr, yte, C_svm=1.0):
    t0 = time.time()
    Ktr = kernel_matrix(Xtr, Xtr, lam)
    Kte = kernel_matrix(Xte, Xtr, lam)
    t_kernel = time.time() - t0

    clf = SVC(kernel="precomputed", C=C_svm)
    clf.fit(Ktr, ytr)
    train_acc = clf.score(Ktr, ytr)
    test_acc  = clf.score(Kte, yte)

    # Kernel-value diagnostics
    off_diag = Ktr[~np.eye(Ktr.shape[0], dtype=bool)]
    mean_off = float(off_diag.mean())
    std_off  = float(off_diag.std())
    return {
        "lambda": lam,
        "C_svm": C_svm,
        "train_acc": float(train_acc),
        "test_acc":  float(test_acc),
        "kernel_offdiag_mean": mean_off,
        "kernel_offdiag_std":  std_off,
        "seconds": float(t_kernel),
    }

def main():
    print(f"[cfg] n_qubits={N_QUBITS}, n_train={N_TRAIN}, n_test={N_TEST}, "
          f"lambdas={LAMBDAS}, seed={SEED}, pennylane={qml.__version__}")
    Xtr, Xte, ytr, yte = build_data(seed=SEED)
    print(f"[data] train shape={Xtr.shape}, test shape={Xte.shape}, class balance train={np.bincount(ytr)}, test={np.bincount(yte)}")

    results = []
    for lam in LAMBDAS:
        res = run_one_lambda(lam, Xtr, Xte, ytr, yte, C_svm=1.0)
        print(f"[lam={lam:>7.4f}] train_acc={res['train_acc']:.3f}  test_acc={res['test_acc']:.3f}  "
              f"K_off_mean={res['kernel_offdiag_mean']:.4f}  K_off_std={res['kernel_offdiag_std']:.4f}  "
              f"t={res['seconds']:.1f}s")
        results.append(res)

    # baseline: classical linear + RBF SVM for reference
    from sklearn.svm import SVC as SkSVC
    linear = SkSVC(kernel="linear", C=1.0).fit(Xtr, ytr)
    rbf    = SkSVC(kernel="rbf",    C=1.0, gamma="scale").fit(Xtr, ytr)
    baseline = {
        "classical_linear_test_acc": float(linear.score(Xte, yte)),
        "classical_rbf_test_acc":    float(rbf.score(Xte, yte)),
    }
    print(f"[baseline] linear={baseline['classical_linear_test_acc']:.3f}  rbf={baseline['classical_rbf_test_acc']:.3f}")

    # Save evidence
    csv_path = os.path.join(EVIDENCE, "bandwidth_sweep.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        for r in results:
            w.writerow(r)
    json_path = os.path.join(EVIDENCE, "bandwidth_sweep.json")
    with open(json_path, "w") as f:
        json.dump({
            "config": {
                "seed": SEED, "n_qubits": N_QUBITS, "n_train": N_TRAIN, "n_test": N_TEST,
                "lambdas": LAMBDAS, "dataset": "sklearn.make_moons (2D -> 4D lift)",
                "dataset_noise": DATASET_NOISE, "feature_map": "IQP-style, depth=2, Eq.5 of paper",
                "kernel": "fidelity |<phi(x')|phi(x)>|^2, statevector sim (exact, no shots)",
                "classifier": "sklearn SVC(kernel='precomputed', C=1.0)",
                "pennylane": qml.__version__,
            },
            "results": results,
            "baseline": baseline,
        }, f, indent=2)
    print(f"[write] {csv_path}")
    print(f"[write] {json_path}")

    # Figure
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        lams = [r["lambda"] for r in results]
        tr   = [r["train_acc"] for r in results]
        te   = [r["test_acc"]  for r in results]
        km   = [r["kernel_offdiag_mean"] for r in results]
        fig, ax1 = plt.subplots(figsize=(7, 4.5))
        ax1.plot(lams, tr, "o--", label="train acc", color="tab:blue", alpha=0.7)
        ax1.plot(lams, te, "s-",  label="test acc",  color="tab:red")
        ax1.axhline(0.5, ls=":", color="gray", label="random guess (0.5)")
        ax1.axhline(baseline["classical_rbf_test_acc"], ls="--", color="tab:green",
                    label=f"classical RBF SVM ({baseline['classical_rbf_test_acc']:.2f})")
        ax1.set_xscale("log")
        ax1.set_xlabel("Bandwidth (scaling factor) λ")
        ax1.set_ylabel("Accuracy")
        ax1.set_ylim(0.35, 1.02)
        ax1.legend(loc="lower center", fontsize=9)
        ax1.set_title("Quantum-kernel SVC accuracy vs bandwidth\n(IQP feature map, 4 qubits, make_moons)")
        ax2 = ax1.twinx()
        ax2.plot(lams, km, "d-", color="tab:orange", alpha=0.5, label="mean off-diag K")
        ax2.set_ylabel("Mean off-diagonal kernel value", color="tab:orange")
        ax2.tick_params(axis='y', labelcolor="tab:orange")
        fig.tight_layout()
        fig_path = os.path.join(FIGURES, "accuracy_vs_bandwidth.png")
        plt.savefig(fig_path, dpi=140)
        print(f"[write] {fig_path}")
    except Exception as e:
        print(f"[warn] plot failed: {e}")

    # Print a small verdict-support summary
    best = max(results, key=lambda r: r["test_acc"])
    worst_small = min(results[:2], key=lambda r: r["test_acc"])
    worst_large = min(results[-2:], key=lambda r: r["test_acc"])
    print(f"\n[summary] best test_acc={best['test_acc']:.3f} at lambda={best['lambda']}")
    print(f"[summary] small-lambda regime (lam<=0.05): worst test_acc={worst_small['test_acc']:.3f} at lambda={worst_small['lambda']}")
    print(f"[summary] large-lambda regime (lam>=3.0):  worst test_acc={worst_large['test_acc']:.3f} at lambda={worst_large['lambda']}")

if __name__ == "__main__":
    main()
