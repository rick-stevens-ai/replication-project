#!/usr/bin/env python3
"""
Independent replication piece 1:
Noiseless QAOA MaxCut approximation ratio on non-planar random 3-regular (RR3)
graphs, matching the paper's problem class (Sud & Egger 2023, arXiv:2307.14427).

We use Qiskit for circuit construction and Qiskit-Aer statevector simulator
to compute exact <H_C> as a function of (beta, gamma) at depth p, then optimize
with scipy. Report approximation ratio r = <H_C> / MaxCut(G).

Non-planarity check: for RR3 with n >= 8, planarity is checked with networkx;
we regenerate until non-planar.

For MaxCut ground truth we brute-force enumerate 2^n cuts (n <= 12 fine).
"""
import json, time, sys, os
import numpy as np
import networkx as nx
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from scipy.optimize import minimize

RNG = np.random.default_rng(20260703)

def make_rr3_nonplanar(n, seed):
    """Return a random 3-regular graph on n nodes that is non-planar. n must be even and >=4."""
    r = np.random.default_rng(seed)
    tries = 0
    while True:
        tries += 1
        s = int(r.integers(0, 2**31 - 1))
        try:
            G = nx.random_regular_graph(3, n, seed=s)
        except nx.NetworkXError:
            continue
        if not nx.is_connected(G):
            continue
        planar, _ = nx.check_planarity(G)
        if not planar:
            return G, tries
        if tries > 500:
            # For very small n non-planarity may be rare; fall back
            return G, tries

def maxcut_bruteforce(G):
    n = G.number_of_nodes()
    edges = list(G.edges())
    best = -1
    for x in range(1 << n):
        cut = 0
        for (u, v) in edges:
            if ((x >> u) & 1) != ((x >> v) & 1):
                cut += 1
        if cut > best:
            best = cut
    return best

def cost_hamiltonian(G):
    """H_C = sum_{(i,j) in E} 0.5 * (Z_i Z_j - I).  For MaxCut, minimizing <H_C>
    over states = -MaxCut. We instead work with <sum (I - Z_i Z_j)/2> = cut count."""
    n = G.number_of_nodes()
    paulis = []
    coeffs = []
    for (i, j) in G.edges():
        z = ['I'] * n
        z[i] = 'Z'; z[j] = 'Z'
        paulis.append(''.join(reversed(z)))
        coeffs.append(0.5)
        # constant term I contributes +0.5 per edge
    # Add identity constant separately (num_edges * (-0.5) so cut = 0.5*|E| - 0.5 <sum ZZ>)
    # We'll represent H_zz = sum ZZ (coeffs 1.0), and compute cut = 0.5*|E| - 0.5<H_zz>.
    paulis = []
    coeffs = []
    for (i, j) in G.edges():
        z = ['I'] * n
        z[i] = 'Z'; z[j] = 'Z'
        paulis.append(''.join(reversed(z)))
        coeffs.append(1.0)
    H_zz = SparsePauliOp.from_list(list(zip(paulis, coeffs)))
    return H_zz

def qaoa_circuit(G, gammas, betas):
    """Standard QAOA ansatz. e^{-i gamma H_C} implemented as product of ZZ rotations
    with angle 2*gamma per edge; e^{-i beta H_B} as product of RX(2*beta)."""
    n = G.number_of_nodes()
    p = len(gammas)
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for k in range(p):
        for (i, j) in G.edges():
            qc.rzz(2.0 * gammas[k], i, j)
        for q in range(n):
            qc.rx(2.0 * betas[k], q)
    return qc

def expectation_zz_sum(G, gammas, betas):
    """<H_zz> via exact statevector."""
    qc = qaoa_circuit(G, gammas, betas)
    sv = Statevector.from_instruction(qc)
    H_zz = cost_hamiltonian(G)
    val = sv.expectation_value(H_zz)
    return float(np.real(val))

def cut_expectation(G, gammas, betas):
    """<cut> = 0.5*|E| - 0.5*<H_zz>."""
    m = G.number_of_edges()
    zz = expectation_zz_sum(G, gammas, betas)
    return 0.5 * m - 0.5 * zz

def optimize_qaoa(G, p, n_restarts=8, seed=0):
    """Maximize <cut> by minimizing negative. Multi-start."""
    r = np.random.default_rng(seed)
    best = None
    for trial in range(n_restarts):
        # Random init: gamma in [0, pi], beta in [0, pi/2]
        g0 = r.uniform(0.0, np.pi, size=p)
        b0 = r.uniform(0.0, np.pi/2, size=p)
        x0 = np.concatenate([g0, b0])
        def neg_cut(x):
            return -cut_expectation(G, x[:p], x[p:])
        res = minimize(neg_cut, x0, method='COBYLA', options={'maxiter': 200, 'rhobeg': 0.3})
        val = -res.fun
        if (best is None) or (val > best['val']):
            best = {'val': val, 'x': res.x.tolist(), 'trial': trial, 'nit': res.nfev}
    return best

def main():
    outdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/results"
    os.makedirs(outdir, exist_ok=True)
    log = []
    sizes = [6, 8, 10]
    depths = [1, 2]
    graphs_per_size = 3
    per_run = []
    for n in sizes:
        for gi in range(graphs_per_size):
            G, tries = make_rr3_nonplanar(n, seed=1000*n + gi)
            m = G.number_of_edges()
            mc = maxcut_bruteforce(G)
            planar, _ = nx.check_planarity(G)
            for p in depths:
                t0 = time.time()
                res = optimize_qaoa(G, p, n_restarts=6, seed=42 + gi*10 + p)
                dt = time.time() - t0
                approx_ratio = res['val'] / mc
                row = {
                    'n': n, 'gi': gi, 'p': p, 'edges': m,
                    'maxcut': mc, 'planar': planar,
                    'nonplanar_tries': tries,
                    'best_cut_expect': res['val'],
                    'approx_ratio': approx_ratio,
                    'time_s': round(dt, 3),
                    'restarts_used': res['trial'] + 1,
                    'params': res['x'],
                }
                per_run.append(row)
                print(f"n={n} gi={gi} p={p} |E|={m} MaxCut={mc} planar={planar} "
                      f"<cut>={res['val']:.4f} r={approx_ratio:.4f} t={dt:.2f}s")
    # Aggregate: mean r per (n, p)
    agg = {}
    for row in per_run:
        key = f"n{row['n']}_p{row['p']}"
        agg.setdefault(key, []).append(row['approx_ratio'])
    summary = {k: {'mean_r': float(np.mean(v)),
                   'std_r': float(np.std(v)),
                   'min_r': float(np.min(v)),
                   'max_r': float(np.max(v)),
                   'count': len(v)} for k, v in agg.items()}
    out = {
        'per_run': per_run,
        'summary': summary,
        'notes': (
            "Noiseless QAOA MaxCut on random 3-regular (RR3) graphs.\n"
            "Non-planarity checked via networkx.check_planarity; RR3 for n>=6 tends to be planar sometimes.\n"
            "Farhi et al. 2014 lower bound for QAOA-p1 on 3-regular MaxCut: r >= 0.6924.\n"
            "Approx ratio r = <cut> / MaxCut(G)."
        )
    }
    with open(f"{outdir}/qaoa_noiseless_results.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nSUMMARY (mean approximation ratio):")
    for k in sorted(summary):
        s = summary[k]
        print(f"  {k}: mean r = {s['mean_r']:.4f} +/- {s['std_r']:.4f}  (n={s['count']})")
    print(f"\nwrote {outdir}/qaoa_noiseless_results.json")

if __name__ == "__main__":
    main()
