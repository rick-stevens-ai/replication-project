#!/usr/bin/env python3
"""
Independent replication piece 2:
Reproduce the paper's central algorithmic idea (Sud & Egger 2023, arXiv:2307.14427):
train a feed-forward neural network (FFNN) to map NOISY QAOA-circuit expectation
values -> IDEAL (noiseless) expectation values.  Use it for error mitigation on
a small (n=10) non-planar RR3 graph, and compare the mean-squared error of
per-edge ZZ correlators before vs after FFNN mitigation.

Paper reports (App./Sec. IV.A, n=10 RR3, thermal-relaxation noise model):
  MSE(noisy vs ideal)     ~= 11%
  MSE(FFNN-mit vs ideal)  ~=  7%
i.e. FFNN reduces per-edge correlator error by ~35-40% relative.

Training-data protocol (Sec. III.C of paper):
  Generate M ~ 20*|E| training samples, each a random product state on the
  QAOA circuit input (input state <- random product state instead of |+>^n),
  computing Z_i and Z_iZ_j noisy and noiseless.  We instead use the standard
  "random QAOA angles" protocol (equivalent for the purpose of training the
  mapping) since the paper's random-product-state protocol is one specific
  choice; we cite this substitution in REPORT.md.

Network: single hidden layer, size = (input+output)/2, tanh activations,
trained with Adam / MSE loss.  Following paper's App. B FFNN description.

Noise model: thermal_relaxation_error on each CNOT with T1=200us, T2=100us,
gate_time=560ns (reasonable IBM Falcon-class defaults); depolarizing readout
error 1%.  This is a strong-noise regime comparable to the paper's "102 CNOT"
setting for a 10-qubit RR3 QAOA circuit.

We measure:
  - MSE_noisy    = mean_{edges} ( <ZZ>_noisy  -  <ZZ>_ideal )^2
  - MSE_ffnn     = mean_{edges} ( <ZZ>_ffnn   -  <ZZ>_ideal )^2
Reported both on training set (in-sample) and on a held-out validation
set of 20 fresh QAOA angle pairs (paper's protocol).
"""
import json, time, os
import numpy as np
import networkx as nx
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error, depolarizing_error
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

RNG = np.random.default_rng(20260703)

def make_rr3_nonplanar(n, seed):
    r = np.random.default_rng(seed)
    for _ in range(500):
        s = int(r.integers(0, 2**31 - 1))
        try:
            G = nx.random_regular_graph(3, n, seed=s)
        except nx.NetworkXError:
            continue
        if not nx.is_connected(G):
            continue
        planar, _ = nx.check_planarity(G)
        if not planar:
            return G
    return G

def qaoa_circuit(G, gammas, betas, include_measurement=False):
    n = G.number_of_nodes()
    p = len(gammas)
    qc = QuantumCircuit(n, n)
    qc.h(range(n))
    for k in range(p):
        for (i, j) in G.edges():
            qc.rzz(2.0 * gammas[k], i, j)
        for q in range(n):
            qc.rx(2.0 * betas[k], q)
    if include_measurement:
        qc.measure(range(n), range(n))
    return qc

def build_noise_model(cnot_gate_time_ns=560.0, t1_us=200.0, t2_us=100.0, ro_err=0.01):
    """Thermal-relaxation on 2q gates; depolarizing readout error."""
    T1 = t1_us * 1e3   # ns
    T2 = t2_us * 1e3   # ns
    two_q_time = cnot_gate_time_ns
    err_2q = thermal_relaxation_error(T1, T2, two_q_time).expand(
             thermal_relaxation_error(T1, T2, two_q_time))
    # Single-qubit gate noise (much smaller)
    err_1q = thermal_relaxation_error(T1, T2, 50.0)
    ro = depolarizing_error(ro_err, 1)
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(err_2q, ['cx', 'cz', 'ecr', 'rzz'])
    nm.add_all_qubit_quantum_error(err_1q, ['sx', 'x', 'rx', 'ry', 'rz', 'h'])
    nm.add_all_qubit_quantum_error(ro, ['measure'])
    return nm

def ideal_correlators(G, gammas, betas):
    """<Z_i>, <Z_iZ_j> under noiseless statevector."""
    n = G.number_of_nodes()
    qc = qaoa_circuit(G, gammas, betas)
    sv = Statevector.from_instruction(qc)
    z_singles = np.zeros(n)
    for i in range(n):
        z = ['I']*n; z[i] = 'Z'
        op = SparsePauliOp.from_list([(''.join(reversed(z)), 1.0)])
        z_singles[i] = float(np.real(sv.expectation_value(op)))
    zz_edges = {}
    for (i, j) in G.edges():
        z = ['I']*n; z[i] = 'Z'; z[j] = 'Z'
        op = SparsePauliOp.from_list([(''.join(reversed(z)), 1.0)])
        zz_edges[(i, j)] = float(np.real(sv.expectation_value(op)))
    return z_singles, zz_edges

def noisy_correlators(G, gammas, betas, noise_model, shots=4000, seed=0):
    """Sample counts under noise model; estimate <Z_i>, <Z_iZ_j> for all i,j (full)."""
    n = G.number_of_nodes()
    qc = qaoa_circuit(G, gammas, betas, include_measurement=True)
    sim = AerSimulator(noise_model=noise_model, seed_simulator=seed)
    tqc = transpile(qc, sim, optimization_level=0)
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()
    # Convert bitstrings to per-shot 0/1 arrays; qiskit bitstring index 0 = qubit n-1
    N = shots
    z_singles = np.zeros(n)
    zz_full = {}
    for bit, c in counts.items():
        # bit like '01001' with bit[0] = q_{n-1}
        bits = np.array([1 - 2*int(b) for b in reversed(bit)])  # +1 for 0, -1 for 1 -> <Z>
        z_singles += c * bits
        for i in range(n):
            for j in range(i+1, n):
                key = (i, j)
                zz_full[key] = zz_full.get(key, 0.0) + c * bits[i] * bits[j]
    z_singles /= N
    for k in zz_full:
        zz_full[k] /= N
    return z_singles, zz_full

def edges_to_vec(zz_full, edges):
    return np.array([zz_full[(min(i,j), max(i,j))] for (i, j) in edges])

def all_pairs_vec(zz_full, n):
    v = np.zeros(n*(n-1)//2)
    idx = 0
    for i in range(n):
        for j in range(i+1, n):
            v[idx] = zz_full[(i, j)]
            idx += 1
    return v

def run(n=10, n_train=200, n_val=20, shots=4000, seed=17, outpath=None):
    print(f"[setup] building non-planar RR3 graph n={n} ...")
    G = make_rr3_nonplanar(n, seed=seed)
    m = G.number_of_edges()
    edges = sorted([(min(u,v), max(u,v)) for (u,v) in G.edges()])
    planar, _ = nx.check_planarity(G)
    print(f"[setup] |V|={n} |E|={m} planar={planar}")

    nm = build_noise_model()
    r = np.random.default_rng(seed)
    print(f"[gen ] generating {n_train} training + {n_val} validation samples "
          f"(each shots={shots}) ...")

    # Sample QAOA angle pairs uniformly
    def sample_angles():
        # depth p=1 to keep circuits small; also matches paper's depth-1 landscape section
        g = r.uniform(0.0, np.pi, size=1)
        b = r.uniform(0.0, np.pi/2, size=1)
        return g, b

    X_train, Y_train = [], []
    X_val, Y_val = [], []
    t0 = time.time()
    for s in range(n_train + n_val):
        g, b = sample_angles()
        z_ideal, zz_ideal = ideal_correlators(G, g, b)
        z_noisy, zz_noisy_full = noisy_correlators(
            G, g, b, nm, shots=shots, seed=int(r.integers(0, 2**31-1)))
        # Feature vector: n singles + all pairs (n choose 2)
        x = np.concatenate([z_noisy, all_pairs_vec(zz_noisy_full, n)])
        # Target: only edge correlators (|E| dims)
        y = edges_to_vec(zz_ideal, edges)
        if s < n_train:
            X_train.append(x); Y_train.append(y)
        else:
            X_val.append(x);   Y_val.append(y)
        if (s+1) % 25 == 0:
            print(f"  [{s+1}/{n_train+n_val}] elapsed={time.time()-t0:.1f}s")
    X_train = np.array(X_train); Y_train = np.array(Y_train)
    X_val   = np.array(X_val);   Y_val   = np.array(Y_val)

    # Baseline: noisy per-edge ZZ (extracted from noisy vector) vs ideal ZZ
    def extract_noisy_edges(x):
        z_noisy = x[:n]; zz_full = x[n:]
        # Reconstruct into (i,j)->val
        d = {}
        idx = 0
        for i in range(n):
            for j in range(i+1, n):
                d[(i,j)] = zz_full[idx]; idx += 1
        return edges_to_vec(d, edges)

    noisy_pred_train = np.array([extract_noisy_edges(x) for x in X_train])
    noisy_pred_val   = np.array([extract_noisy_edges(x) for x in X_val])

    mse_noisy_train = float(np.mean((noisy_pred_train - Y_train)**2))
    mse_noisy_val   = float(np.mean((noisy_pred_val   - Y_val)**2))
    print(f"[base] MSE(noisy vs ideal): train={mse_noisy_train:.4f} val={mse_noisy_val:.4f}")

    # FFNN per paper's App. B: single hidden layer, size = (input+output)/2, tanh
    input_dim = X_train.shape[1]
    output_dim = Y_train.shape[1]
    hidden = max(8, (input_dim + output_dim) // 2)
    print(f"[nn  ] FFNN input={input_dim} hidden={hidden} output={output_dim}")

    scaler_x = StandardScaler().fit(X_train)
    Xtr = scaler_x.transform(X_train); Xva = scaler_x.transform(X_val)

    nn = MLPRegressor(hidden_layer_sizes=(hidden,), activation='tanh',
                      solver='adam', learning_rate_init=0.005,
                      max_iter=3000, tol=1e-6, random_state=seed,
                      early_stopping=True, validation_fraction=0.1,
                      n_iter_no_change=50)
    nn.fit(Xtr, Y_train)
    ffnn_pred_train = nn.predict(Xtr)
    ffnn_pred_val   = nn.predict(Xva)

    mse_ffnn_train = float(np.mean((ffnn_pred_train - Y_train)**2))
    mse_ffnn_val   = float(np.mean((ffnn_pred_val   - Y_val)**2))
    print(f"[nn  ] MSE(FFNN  vs ideal): train={mse_ffnn_train:.4f} val={mse_ffnn_val:.4f}")

    # Report: MSE reduction ratio
    red_train = 1.0 - (mse_ffnn_train / mse_noisy_train) if mse_noisy_train > 0 else float('nan')
    red_val   = 1.0 - (mse_ffnn_val   / mse_noisy_val)   if mse_noisy_val   > 0 else float('nan')
    print(f"[nn  ] MSE reduction: train={red_train*100:.1f}%  val={red_val*100:.1f}%")

    # Compare with paper: noisy 11%, mitigated 7%; reduction ~36% relative.
    # Note: paper's "11%" and "7%" appear to be MSE in units of correlator^2
    # (i.e. absolute), matching our units.
    result = {
        'graph': {'n': n, 'edges': m, 'planar': planar},
        'noise_model': {'T1_us': 200, 'T2_us': 100,
                        'cnot_gate_time_ns': 560, 'readout_err': 0.01},
        'training': {'n_train': n_train, 'n_val': n_val, 'shots': shots,
                     'hidden_units': hidden, 'iters': int(nn.n_iter_)},
        'metrics': {
            'MSE_noisy_train': mse_noisy_train,
            'MSE_noisy_val':   mse_noisy_val,
            'MSE_ffnn_train':  mse_ffnn_train,
            'MSE_ffnn_val':    mse_ffnn_val,
            'MSE_reduction_train_pct': red_train*100,
            'MSE_reduction_val_pct':   red_val*100,
        },
        'paper_reference_MSE_noisy':   0.11,
        'paper_reference_MSE_ffnn':    0.07,
        'paper_reference_reduction_pct': (1.0 - 0.07/0.11)*100,
        'notes': (
            "Training data uses random QAOA angle pairs rather than the paper's "
            "random-product-state input protocol; both yield a distribution of "
            "(X, Y) pairs suitable for learning the noisy->ideal correlator map. "
            "Shots-per-run modest (4000) to keep runtime tractable on CPU."
        )
    }
    if outpath:
        with open(outpath, 'w') as fh:
            json.dump(result, fh, indent=2)
        print(f"[out ] wrote {outpath}")
    return result

if __name__ == "__main__":
    outdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/results"
    os.makedirs(outdir, exist_ok=True)
    run(n=10, n_train=200, n_val=20, shots=4000, seed=17,
        outpath=f"{outdir}/qaoa_ffnn_mitigation_results.json")
