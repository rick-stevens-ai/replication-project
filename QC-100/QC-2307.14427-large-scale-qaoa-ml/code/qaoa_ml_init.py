#!/usr/bin/env python3
"""
Piece 3 (side experiment, requested by task brief):
Train a small MLP to predict good QAOA (gamma, beta) initial angles from
graph structural features, and compare its predicted-init approximation
ratio vs random-init approximation ratio on held-out RR3 graphs.

This isn't the paper's central claim (the paper is about ML *error mitigation*
of expectation values, not ML angle prediction), but the task brief asked us
to also test the well-known "ML-predicted initial angles > random init" idea
for QAOA on non-planar graphs. We use graph structural features (n, m, avg
degree, spectral gap, etc.) as MLP input and (gamma_1, beta_1, gamma_2, beta_2)
as output.
"""
import json, time, os
import numpy as np
import networkx as nx
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from scipy.optimize import minimize
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

def make_rr3(n, seed):
    r = np.random.default_rng(seed)
    for _ in range(500):
        s = int(r.integers(0, 2**31 - 1))
        try:
            G = nx.random_regular_graph(3, n, seed=s)
        except nx.NetworkXError:
            continue
        if nx.is_connected(G):
            return G
    return G

def qaoa_circuit(G, gammas, betas):
    n = G.number_of_nodes()
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for k in range(len(gammas)):
        for (i, j) in G.edges():
            qc.rzz(2.0 * gammas[k], i, j)
        for q in range(n):
            qc.rx(2.0 * betas[k], q)
    return qc

def cut_expectation(G, gammas, betas):
    n = G.number_of_nodes()
    m = G.number_of_edges()
    qc = qaoa_circuit(G, gammas, betas)
    sv = Statevector.from_instruction(qc)
    paulis, coeffs = [], []
    for (i, j) in G.edges():
        z = ['I']*n; z[i]='Z'; z[j]='Z'
        paulis.append(''.join(reversed(z))); coeffs.append(1.0)
    H = SparsePauliOp.from_list(list(zip(paulis, coeffs)))
    zz = float(np.real(sv.expectation_value(H)))
    return 0.5 * m - 0.5 * zz  # <cut>

def maxcut(G):
    n = G.number_of_nodes()
    best = 0
    E = list(G.edges())
    for x in range(1 << n):
        c = 0
        for (u, v) in E:
            if ((x >> u) & 1) != ((x >> v) & 1): c += 1
        if c > best: best = c
    return best

def graph_features(G):
    n = G.number_of_nodes()
    m = G.number_of_edges()
    degs = [d for _, d in G.degree()]
    L = nx.normalized_laplacian_matrix(G).toarray()
    eigs = np.sort(np.linalg.eigvalsh(L))
    algebraic_connectivity = eigs[1] if len(eigs) > 1 else 0.0
    lambda_max = eigs[-1]
    tri = sum(nx.triangles(G).values()) / 3.0
    return np.array([n, m, np.mean(degs), np.std(degs),
                     algebraic_connectivity, lambda_max, tri,
                     nx.diameter(G), nx.average_shortest_path_length(G)])

def find_best_angles(G, p, n_restarts=12, seed=0):
    """Use expensive multi-start optimization to find near-optimal angles."""
    r = np.random.default_rng(seed)
    best = None
    for trial in range(n_restarts):
        g0 = r.uniform(0.0, np.pi, size=p)
        b0 = r.uniform(0.0, np.pi/2, size=p)
        x0 = np.concatenate([g0, b0])
        def neg_cut(x):
            return -cut_expectation(G, x[:p], x[p:])
        res = minimize(neg_cut, x0, method='COBYLA', options={'maxiter': 300, 'rhobeg': 0.2})
        val = -res.fun
        if (best is None) or (val > best['val']):
            best = {'val': val, 'x': res.x.copy()}
    return best

def local_optimize(G, p, x0, maxiter=50):
    """Cheap local optimization from x0. Simulates a real-world setting where
    you have limited quantum time and can only afford a few iterations."""
    def neg_cut(x):
        return -cut_expectation(G, x[:p], x[p:])
    res = minimize(neg_cut, x0, method='COBYLA', options={'maxiter': maxiter, 'rhobeg': 0.15})
    return -res.fun

def main():
    outdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/results"
    os.makedirs(outdir, exist_ok=True)

    p = 2
    n_train = 20
    n_test  = 10
    train_ns = [6, 8, 10]
    test_ns  = [6, 8, 10]

    print(f"[data] building {n_train} training + {n_test} test graphs "
          f"(n in {train_ns} / {test_ns}, depth p={p})...")
    train_X = []; train_y = []; train_meta = []
    rng = np.random.default_rng(42)
    seed_i = 0
    for _ in range(n_train):
        n = int(rng.choice(train_ns))
        seed_i += 1
        G = make_rr3(n, seed=seed_i)
        best = find_best_angles(G, p, n_restarts=12, seed=seed_i)
        feats = graph_features(G)
        train_X.append(feats); train_y.append(best['x'])
        train_meta.append({'n': n, 'best_cut': best['val']})
    train_X = np.array(train_X); train_y = np.array(train_y)

    # Train small MLP
    scaler = StandardScaler().fit(train_X)
    Xtr = scaler.transform(train_X)
    nn = MLPRegressor(hidden_layer_sizes=(16, 8), activation='tanh',
                      solver='lbfgs', max_iter=3000, random_state=1)
    nn.fit(Xtr, train_y)
    print(f"[nn  ] trained MLP with {n_train} samples; train R2 = {nn.score(Xtr, train_y):.3f}")

    # Evaluate on test graphs
    test_ns_all = list(test_ns) * (n_test // len(test_ns) + 1)
    per_test = []
    for k in range(n_test):
        n = int(rng.choice(test_ns))
        seed_i += 1000
        G = make_rr3(n, seed=seed_i)
        mc = maxcut(G)
        feats = graph_features(G)
        x_pred = nn.predict(scaler.transform(feats.reshape(1, -1)))[0]

        # (a) Predicted init + cheap local polish
        val_ml   = local_optimize(G, p, x_pred, maxiter=50)
        # (b) Random init + cheap local polish (best of same total "quantum budget"
        # = same number of maxiter but averaged over K restarts, matched budget)
        K = 3  # random baseline: K restarts * maxiter/K to keep budget the same
        best_rand = -np.inf
        for kr in range(K):
            rrng = np.random.default_rng(seed_i + kr)
            g0 = rrng.uniform(0.0, np.pi, size=p)
            b0 = rrng.uniform(0.0, np.pi/2, size=p)
            x0 = np.concatenate([g0, b0])
            vr = local_optimize(G, p, x0, maxiter=50 // K)
            if vr > best_rand: best_rand = vr
        # (c) Random init single-shot (same budget as ML)
        rrng2 = np.random.default_rng(seed_i + 999)
        g0 = rrng2.uniform(0.0, np.pi, size=p)
        b0 = rrng2.uniform(0.0, np.pi/2, size=p)
        x_rand = np.concatenate([g0, b0])
        val_rand_single = local_optimize(G, p, x_rand, maxiter=50)
        # (d) Best-possible (heavy multi-start), for reference
        best_ref = find_best_angles(G, p, n_restarts=8, seed=seed_i + 12345)['val']

        r_ml = val_ml / mc
        r_rand_single = val_rand_single / mc
        r_rand_multi  = best_rand / mc
        r_ref = best_ref / mc
        per_test.append({
            'n': n, 'edges': G.number_of_edges(), 'maxcut': mc,
            'val_ML_init':      val_ml,   'r_ML_init':      r_ml,
            'val_rand_single':  val_rand_single, 'r_rand_single':  r_rand_single,
            'val_rand_best3':   best_rand,'r_rand_best3':   r_rand_multi,
            'val_reference':    best_ref, 'r_reference':    r_ref,
        })
        print(f"  test #{k+1} n={n} MaxCut={mc}: "
              f"r_ML={r_ml:.3f}  r_rand1={r_rand_single:.3f}  "
              f"r_rand_best3={r_rand_multi:.3f}  r_ref={r_ref:.3f}")

    mean_r_ml   = float(np.mean([t['r_ML_init']     for t in per_test]))
    mean_r_r1   = float(np.mean([t['r_rand_single'] for t in per_test]))
    mean_r_r3   = float(np.mean([t['r_rand_best3']  for t in per_test]))
    mean_r_ref  = float(np.mean([t['r_reference']   for t in per_test]))
    print(f"\n[summary] mean approx ratio ({n_test} test graphs, depth p={p}):")
    print(f"  ML-init + polish       : r = {mean_r_ml:.4f}")
    print(f"  Random init (single)   : r = {mean_r_r1:.4f}")
    print(f"  Random init (best of 3): r = {mean_r_r3:.4f}")
    print(f"  Heavy multi-start ref  : r = {mean_r_ref:.4f}")

    out = {
        'depth': p, 'n_train_graphs': n_train, 'n_test_graphs': n_test,
        'per_test': per_test,
        'summary': {
            'mean_r_ML_init': mean_r_ml,
            'mean_r_rand_single': mean_r_r1,
            'mean_r_rand_best3':  mean_r_r3,
            'mean_r_reference':   mean_r_ref,
        }
    }
    with open(f"{outdir}/qaoa_ml_init_results.json", 'w') as fh:
        json.dump(out, fh, indent=2)
    print(f"[out] wrote {outdir}/qaoa_ml_init_results.json")

if __name__ == "__main__":
    main()
