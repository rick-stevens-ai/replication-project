#!/usr/bin/env python3
"""
Replication piece 2 (v2): stronger noise regime + line-topology transpilation
so 2-qubit gate count inflates like the paper (their n=10 RR3 depth-1 circuit
uses ~102 CNOTs after SWAP insertion on a line).

Also runs at multiple noise levels to trace the FFNN benefit vs noise strength,
which is the paper's "increase noise strength" experiment (Sec IV.A) that
observed the FFNN stops helping when noise becomes too strong.
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

def build_noise_model(cnot_gate_time_ns, t1_us=100.0, t2_us=80.0, ro_err=0.02):
    T1 = t1_us * 1e3
    T2 = t2_us * 1e3
    err_2q = thermal_relaxation_error(T1, T2, cnot_gate_time_ns).expand(
             thermal_relaxation_error(T1, T2, cnot_gate_time_ns))
    err_1q = thermal_relaxation_error(T1, T2, 50.0)
    ro = depolarizing_error(ro_err, 1)
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(err_2q, ['cx', 'cz', 'ecr'])
    nm.add_all_qubit_quantum_error(err_1q, ['sx', 'x', 'rx', 'ry', 'rz', 'h', 'u', 'u3', 'u2', 'u1'])
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
    """Transpile QAOA to line coupling map so ZZ gates get decomposed to CNOTs +
    SWAP layers are inserted; then sample with noise."""
    n = G.number_of_nodes()
    qc = qaoa_circuit(G, gammas, betas, include_measurement=True)
    sim = AerSimulator(noise_model=noise_model, seed_simulator=seed)
    tqc = transpile(qc, sim, coupling_map=coupling, basis_gates=['cx','sx','rz','x','measure'],
                    optimization_level=2, seed_transpiler=seed)
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()
    cnot_count = tqc.count_ops().get('cx', 0)
    # Read out from CLASSICAL BITS in the order they were measured. In our
    # circuit, cbit c gets qubit c's measurement; but after transpile, the
    # virtual-physical layout is remapped; qiskit's classical-bit ordering
    # still corresponds to the ORIGINAL virtual qubit labels because we
    # measure(range(n), range(n)) on the ORIGINAL circuit. So bit c = original qubit c.
    N = shots
    z_singles = np.zeros(n)
    zz_full = {}
    for bit, c in counts.items():
        bits = np.array([1 - 2*int(b) for b in reversed(bit)])
        z_singles += c * bits
        for i in range(n):
            for j in range(i+1, n):
                key = (i, j)
                zz_full[key] = zz_full.get(key, 0.0) + c * bits[i] * bits[j]
    z_singles /= N
    for k in zz_full:
        zz_full[k] /= N
    return z_singles, zz_full, cnot_count

def edges_to_vec(zz, edges):
    return np.array([zz[(min(i,j), max(i,j))] for (i,j) in edges])

def all_pairs_vec(zz_full, n):
    v = np.zeros(n*(n-1)//2); idx=0
    for i in range(n):
        for j in range(i+1, n):
            v[idx] = zz_full[(i,j)]; idx += 1
    return v

def run_sweep(n=10, seed=17, n_train=200, n_val=40, shots=4000,
              cnot_times_ns=(200.0, 400.0, 600.0)):
    G = make_rr3_nonplanar(n, seed=seed)
    edges = sorted([(min(u,v), max(u,v)) for (u,v) in G.edges()])
    m = len(edges)
    planar, _ = nx.check_planarity(G)
    coupling = line_coupling(n)
    print(f"[graph] n={n} |E|={m} planar={planar}, coupling=line({n})")

    r = np.random.default_rng(seed)
    def sample_angles():
        g = r.uniform(0.0, np.pi, size=1)
        b = r.uniform(0.0, np.pi/2, size=1)
        return g, b

    # Pre-generate a single common set of angle pairs for all noise levels
    angles = [sample_angles() for _ in range(n_train + n_val)]
    # Pre-compute ideal Y (same for all noise levels)
    print(f"[ideal] computing {n_train+n_val} ideal targets ...")
    t0 = time.time()
    ideal_z = []
    ideal_zz = []
    for (g, b) in angles:
        zs, zze = ideal_correlators(G, g, b)
        ideal_z.append(zs); ideal_zz.append(zze)
    print(f"[ideal] done in {time.time()-t0:.1f}s")

    results = {}
    for cnot_t in cnot_times_ns:
        print(f"\n=== Noise: CNOT gate time = {cnot_t} ns ===")
        nm = build_noise_model(cnot_t)
        Xall = []; Yall = []; cnot_counts = []
        t0 = time.time()
        for s, (g, b) in enumerate(angles):
            zs_n, zzf_n, ccnt = noisy_correlators_line(
                G, g, b, nm, coupling, shots=shots,
                seed=int(r.integers(0, 2**31-1)))
            cnot_counts.append(ccnt)
            x = np.concatenate([zs_n, all_pairs_vec(zzf_n, n)])
            y = edges_to_vec(ideal_zz[s], edges)
            Xall.append(x); Yall.append(y)
            if (s+1) % 25 == 0:
                print(f"  [{s+1}/{len(angles)}] elapsed={time.time()-t0:.1f}s")
        X = np.array(Xall); Y = np.array(Yall)
        X_train, X_val = X[:n_train], X[n_train:]
        Y_train, Y_val = Y[:n_train], Y[n_train:]

        # Noisy per-edge extraction
        def extract_noisy_edges(x):
            zzfull = x[n:]
            d = {}; idx=0
            for i in range(n):
                for j in range(i+1, n):
                    d[(i,j)] = zzfull[idx]; idx += 1
            return edges_to_vec(d, edges)

        noisy_train = np.array([extract_noisy_edges(x) for x in X_train])
        noisy_val   = np.array([extract_noisy_edges(x) for x in X_val])
        mse_n_tr = float(np.mean((noisy_train - Y_train)**2))
        mse_n_va = float(np.mean((noisy_val   - Y_val)**2))
        rmse_n_va = float(np.sqrt(mse_n_va))

        # FFNN
        input_dim = X.shape[1]; output_dim = Y.shape[1]
        hidden = max(8, (input_dim + output_dim)//2)
        scaler = StandardScaler().fit(X_train)
        Xtr = scaler.transform(X_train); Xva = scaler.transform(X_val)
        nn = MLPRegressor(hidden_layer_sizes=(hidden,), activation='tanh',
                          solver='adam', learning_rate_init=0.005,
                          max_iter=5000, tol=1e-7, random_state=seed,
                          early_stopping=True, validation_fraction=0.15,
                          n_iter_no_change=100)
        nn.fit(Xtr, Y_train)
        ffnn_tr = nn.predict(Xtr); ffnn_va = nn.predict(Xva)
        mse_f_tr = float(np.mean((ffnn_tr - Y_train)**2))
        mse_f_va = float(np.mean((ffnn_va - Y_val)**2))
        rmse_f_va = float(np.sqrt(mse_f_va))
        red_tr = 1.0 - mse_f_tr/mse_n_tr if mse_n_tr>0 else float('nan')
        red_va = 1.0 - mse_f_va/mse_n_va if mse_n_va>0 else float('nan')

        # Bias in <ZZ>: mean absolute deviation on val
        bias_noisy = float(np.mean(np.abs(noisy_val - Y_val)))
        bias_ffnn  = float(np.mean(np.abs(ffnn_va   - Y_val)))

        print(f"  CNOT count (median transpiled): {int(np.median(cnot_counts))}")
        print(f"  MSE  noisy train={mse_n_tr:.4f} val={mse_n_va:.4f}   "
              f"(RMSE val = {rmse_n_va:.3f})")
        print(f"  MSE  FFNN  train={mse_f_tr:.4f} val={mse_f_va:.4f}   "
              f"(RMSE val = {rmse_f_va:.3f})")
        print(f"  MAE  noisy val={bias_noisy:.3f}   FFNN val={bias_ffnn:.3f}")
        print(f"  MSE reduction (val) = {red_va*100:.1f}%")
        results[f"cnot_{int(cnot_t)}ns"] = {
            'cnot_time_ns': cnot_t,
            'median_cnot_count': int(np.median(cnot_counts)),
            'MSE_noisy_train': mse_n_tr, 'MSE_noisy_val': mse_n_va,
            'MSE_ffnn_train':  mse_f_tr, 'MSE_ffnn_val':  mse_f_va,
            'MAE_noisy_val': bias_noisy, 'MAE_ffnn_val': bias_ffnn,
            'RMSE_noisy_val': rmse_n_va, 'RMSE_ffnn_val': rmse_f_va,
            'MSE_reduction_train_pct': red_tr*100,
            'MSE_reduction_val_pct':   red_va*100,
            'nn_iters': int(nn.n_iter_),
        }
    out = {
        'graph': {'n': n, 'edges': m, 'planar': planar},
        'setup': {'n_train': n_train, 'n_val': n_val, 'shots': shots,
                  'T1_us': 100, 'T2_us': 80, 'readout_err': 0.02,
                  'topology': f'line({n})'},
        'paper_reference': {
            'MSE_noisy_pct': 11, 'MSE_ffnn_pct': 7,
            'relative_reduction_pct': (1 - 7/11)*100,
            'CNOT_count_paper_n10_depth1': 102,
        },
        'sweep': results,
    }
    return out

if __name__ == "__main__":
    outdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/results"
    os.makedirs(outdir, exist_ok=True)
    out = run_sweep(n=10, seed=17, n_train=200, n_val=40, shots=4000,
                    cnot_times_ns=(200.0, 400.0, 600.0))
    path = f"{outdir}/qaoa_ffnn_sweep_results.json"
    with open(path, 'w') as fh:
        json.dump(out, fh, indent=2)
    print(f"\n[out] wrote {path}")
