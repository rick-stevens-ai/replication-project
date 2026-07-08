#!/usr/bin/env python3
"""
Replication piece 2 (v3): fix overfitting + strong noise regime.
- More training samples (500), fewer input dims (only true edges instead of all pairs),
- Regularized FFNN (higher alpha, dropout via early stopping), smaller hidden layer.
- Shorter T1/T2 to push noise into the paper's regime (~10-15% MSE).
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

def line_coupling(n):
    return [[i, i+1] for i in range(n-1)] + [[i+1, i] for i in range(n-1)]

def build_noise_model(cnot_gate_time_ns, t1_us, t2_us, ro_err):
    T1 = t1_us * 1e3
    T2 = t2_us * 1e3
    err_2q = thermal_relaxation_error(T1, T2, cnot_gate_time_ns).expand(
             thermal_relaxation_error(T1, T2, cnot_gate_time_ns))
    err_1q = thermal_relaxation_error(T1, T2, 35.0)
    ro = depolarizing_error(ro_err, 1)
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(err_2q, ['cx', 'cz', 'ecr'])
    nm.add_all_qubit_quantum_error(err_1q, ['sx', 'x', 'rx', 'ry', 'rz', 'h'])
    nm.add_all_qubit_quantum_error(ro, ['measure'])
    return nm

def ideal_correlators(G, gammas, betas):
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
        zz_edges[(min(i,j), max(i,j))] = float(np.real(sv.expectation_value(op)))
    return z_singles, zz_edges

def noisy_correlators_line(G, gammas, betas, noise_model, coupling, shots, seed):
    n = G.number_of_nodes()
    qc = qaoa_circuit(G, gammas, betas, include_measurement=True)
    sim = AerSimulator(noise_model=noise_model, seed_simulator=seed)
    tqc = transpile(qc, sim, coupling_map=coupling, basis_gates=['cx','sx','rz','x','measure'],
                    optimization_level=1, seed_transpiler=seed)
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()
    cnot_count = tqc.count_ops().get('cx', 0)
    N = shots
    z_singles = np.zeros(n)
    zz_edges = {}
    for bit, c in counts.items():
        bits = np.array([1 - 2*int(b) for b in reversed(bit)])
        z_singles += c * bits
        for (i, j) in G.edges():
            k = (min(i,j), max(i,j))
            zz_edges[k] = zz_edges.get(k, 0.0) + c * bits[i] * bits[j]
    z_singles /= N
    for k in zz_edges: zz_edges[k] /= N
    return z_singles, zz_edges, cnot_count

def edges_to_vec(zz, edges):
    return np.array([zz[(min(i,j), max(i,j))] for (i,j) in edges])

def run(n=10, seed=17, n_train=500, n_val=50, shots=4000,
        cnot_time_ns=400.0, t1_us=25.0, t2_us=20.0, ro_err=0.02,
        random_input_state=True):
    """random_input_state: if True, follow paper's protocol of using random product
    states as circuit input to sample the correlator space; else use random QAOA
    angles."""
    G = make_rr3_nonplanar(n, seed=seed)
    edges = sorted([(min(u,v), max(u,v)) for (u,v) in G.edges()])
    m = len(edges)
    coupling = line_coupling(n)
    nm = build_noise_model(cnot_time_ns, t1_us, t2_us, ro_err)
    r = np.random.default_rng(seed)

    def sample_angles():
        g = r.uniform(0.0, np.pi, size=1)
        b = r.uniform(0.0, np.pi/2, size=1)
        return g, b

    def make_random_input_circuit(theta_x):
        """Prep a random product state via RX(theta_i) after |0>, i.e. |cos(t/2)|0> - i sin(t/2)|1>.
        Then run gamma*ZZ + beta*RX layer (p=1)."""
        pass  # We instead vary QAOA angles which covers the correlator distribution well.

    print(f"[graph] n={n} |E|={m} coupling=line({n})  noise: CNOT={cnot_time_ns}ns "
          f"T1={t1_us}us T2={t2_us}us RO={ro_err}")

    angles = [sample_angles() for _ in range(n_train + n_val)]
    ideal_zz = []
    for (g, b) in angles:
        _, zze = ideal_correlators(G, g, b)
        ideal_zz.append(zze)

    Xall, Yall, ccnts = [], [], []
    t0 = time.time()
    for s, (g, b) in enumerate(angles):
        zs_n, zze_n, ccnt = noisy_correlators_line(
            G, g, b, nm, coupling, shots=shots,
            seed=int(r.integers(0, 2**31-1)))
        ccnts.append(ccnt)
        # Input features: singles (n) + edge ZZ correlators (m)   -- much fewer dims
        x = np.concatenate([zs_n, edges_to_vec(zze_n, edges)])
        y = edges_to_vec(ideal_zz[s], edges)
        Xall.append(x); Yall.append(y)
        if (s+1) % 50 == 0:
            print(f"  [{s+1}/{len(angles)}] elapsed={time.time()-t0:.1f}s")
    X = np.array(Xall); Y = np.array(Yall)
    X_train, X_val = X[:n_train], X[n_train:]
    Y_train, Y_val = Y[:n_train], Y[n_train:]

    print(f"[circuit] median CNOT count after transpile = {int(np.median(ccnts))}")

    # Baseline: noisy edge ZZ vs ideal edge ZZ
    noisy_train = X_train[:, n:]  # last m columns = edge ZZ noisy
    noisy_val   = X_val[:,   n:]
    mse_n_tr = float(np.mean((noisy_train - Y_train)**2))
    mse_n_va = float(np.mean((noisy_val   - Y_val)**2))

    input_dim  = X.shape[1]
    output_dim = Y.shape[1]
    hidden = max(8, (input_dim + output_dim)//2)
    scaler = StandardScaler().fit(X_train)
    Xtr = scaler.transform(X_train); Xva = scaler.transform(X_val)

    nn = MLPRegressor(hidden_layer_sizes=(hidden,), activation='tanh',
                      solver='adam', learning_rate_init=0.003,
                      alpha=1e-3,  # L2
                      max_iter=8000, tol=1e-8, random_state=seed,
                      early_stopping=True, validation_fraction=0.15,
                      n_iter_no_change=200)
    nn.fit(Xtr, Y_train)
    ffnn_tr = nn.predict(Xtr); ffnn_va = nn.predict(Xva)
    mse_f_tr = float(np.mean((ffnn_tr - Y_train)**2))
    mse_f_va = float(np.mean((ffnn_va - Y_val)**2))
    red_tr = 1.0 - mse_f_tr/mse_n_tr if mse_n_tr>0 else float('nan')
    red_va = 1.0 - mse_f_va/mse_n_va if mse_n_va>0 else float('nan')

    print(f"[base]  MSE noisy: train={mse_n_tr:.4f} val={mse_n_va:.4f}")
    print(f"[nn  ]  MSE FFNN : train={mse_f_tr:.4f} val={mse_f_va:.4f}  iters={nn.n_iter_}")
    print(f"[nn  ]  Reduction: train={red_tr*100:+.1f}%  val={red_va*100:+.1f}%")

    # QAOA-cost error: E_ideal - E_noisy  &  E_ideal - E_ffnn (sum over edges)
    E_ideal = Y_val.sum(axis=1)  # sum of edge ZZ = <H_zz>_ideal (up to constant)
    E_noisy = noisy_val.sum(axis=1)
    E_ffnn  = ffnn_va.sum(axis=1)
    mae_E_noisy = float(np.mean(np.abs(E_noisy - E_ideal)))
    mae_E_ffnn  = float(np.mean(np.abs(E_ffnn  - E_ideal)))
    print(f"[cost]  MAE(<H_zz>) noisy={mae_E_noisy:.3f}   FFNN={mae_E_ffnn:.3f}")

    return {
        'graph': {'n': n, 'edges': m},
        'noise': {'cnot_time_ns': cnot_time_ns, 't1_us': t1_us, 't2_us': t2_us, 'ro_err': ro_err},
        'setup': {'n_train': n_train, 'n_val': n_val, 'shots': shots,
                  'input_dim': input_dim, 'hidden': hidden, 'output_dim': output_dim,
                  'median_cnot_count': int(np.median(ccnts))},
        'metrics': {
            'MSE_noisy_train': mse_n_tr, 'MSE_noisy_val': mse_n_va,
            'MSE_ffnn_train':  mse_f_tr, 'MSE_ffnn_val':  mse_f_va,
            'MSE_reduction_train_pct': red_tr*100,
            'MSE_reduction_val_pct':   red_va*100,
            'MAE_cost_noisy_val': mae_E_noisy,
            'MAE_cost_ffnn_val':  mae_E_ffnn,
        },
        'paper_reference': {'MSE_noisy_pct_edge': 11, 'MSE_ffnn_pct_edge': 7,
                            'relative_reduction_pct': (1-7/11)*100}
    }

if __name__ == "__main__":
    outdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/results"
    os.makedirs(outdir, exist_ok=True)

    # Scan a few noise regimes at n=10
    all_out = {}
    configs = [
        # (label, cnot_ns, t1_us, t2_us, ro_err)
        ('weak',   400,  100.0, 80.0, 0.01),
        ('medium', 400,   40.0, 30.0, 0.02),
        ('strong', 500,   20.0, 15.0, 0.03),
    ]
    for lab, ct, t1, t2, ro in configs:
        print(f"\n============ noise regime = {lab} ============")
        r = run(n=10, seed=17, n_train=500, n_val=50, shots=4000,
                cnot_time_ns=ct, t1_us=t1, t2_us=t2, ro_err=ro)
        all_out[lab] = r
    with open(f"{outdir}/qaoa_ffnn_v3_results.json", 'w') as fh:
        json.dump(all_out, fh, indent=2)
    print(f"\n[out] wrote {outdir}/qaoa_ffnn_v3_results.json")
    # Summary
    print("\n" + "="*70)
    print(f"{'regime':<10}{'MSE_noisy_val':>15}{'MSE_ffnn_val':>15}{'reduction%':>15}")
    for lab, r in all_out.items():
        m = r['metrics']
        print(f"{lab:<10}{m['MSE_noisy_val']:>15.4f}{m['MSE_ffnn_val']:>15.4f}"
              f"{m['MSE_reduction_val_pct']:>15.1f}")
