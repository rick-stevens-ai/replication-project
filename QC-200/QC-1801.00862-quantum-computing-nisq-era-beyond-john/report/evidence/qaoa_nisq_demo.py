#!/usr/bin/env python3
"""
NISQ representative demonstration for Preskill 2018 (arXiv:1801.00862).

Instantiates the core NISQ thesis: a small variational quantum circuit
(QAOA MAX-CUT, p=1 and p=2) on a 3-regular 10-vertex graph, evaluated
under (a) noiseless statevector and (b) a depolarizing noise model
with two-qubit error 1e-3 and single-qubit 1e-4 — parameters roughly
representative of the "NISQ" regime discussed in Section 3.

We measure:
  - noiseless approximation ratio r = <C>/C_max at optimized parameters
  - noisy approximation ratio r_noisy
  - degradation Delta_p = r_ideal - r_noisy for p=1 and p=2

This tests the paper's central claim that variational shallow-depth
circuits can operate meaningfully under NISQ-level noise.

Output: qaoa_nisq_results.json in this directory.
"""
import json
import os
import time
import itertools
import math
import numpy as np
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import Statevector

# ---------------- Graph construction ----------------
def three_regular_graph(n, seed=0):
    """Return a 3-regular graph on n vertices as edge list (n must be even)."""
    import networkx as nx
    G = nx.random_regular_graph(3, n, seed=seed)
    return sorted(map(tuple, (sorted(e) for e in G.edges())))

# ---------------- Classical brute-force MAX-CUT ----------------
def classical_max_cut(edges, n):
    best = 0
    best_bits = None
    for bits in range(2**n):
        cut = 0
        for (u, v) in edges:
            bu = (bits >> u) & 1
            bv = (bits >> v) & 1
            if bu != bv:
                cut += 1
        if cut > best:
            best = cut
            best_bits = bits
    return best, best_bits

# ---------------- QAOA circuit ----------------
def qaoa_circuit(edges, n, gammas, betas):
    p = len(gammas)
    qc = QuantumCircuit(n)
    for q in range(n):
        qc.h(q)
    for layer in range(p):
        # Cost unitary: exp(-i gamma * sum_edges 0.5*(I - Z_u Z_v))
        # = product exp(-i gamma * 0.5*(I - Z_u Z_v))
        # global phases from I drop out; implement as RZZ(2*gamma)
        for (u, v) in edges:
            qc.cx(u, v)
            qc.rz(2 * gammas[layer], v)
            qc.cx(u, v)
        # Mixer: exp(-i beta X_k) each qubit
        for q in range(n):
            qc.rx(2 * betas[layer], q)
    return qc

# ---------------- Expectation via statevector (noiseless) ----------------
def expected_cut_noiseless(qc, edges):
    sv = Statevector.from_instruction(qc)
    probs = np.abs(sv.data)**2
    n = qc.num_qubits
    exp = 0.0
    for idx in range(2**n):
        if probs[idx] < 1e-15:
            continue
        cut = 0
        for (u, v) in edges:
            bu = (idx >> u) & 1
            bv = (idx >> v) & 1
            if bu != bv:
                cut += 1
        exp += probs[idx] * cut
    return exp

# ---------------- Expectation via sampling (noisy) ----------------
def expected_cut_noisy(qc, edges, noise_model, shots=8192):
    qc_m = qc.copy()
    qc_m.measure_all()
    sim = AerSimulator(noise_model=noise_model)
    from qiskit import transpile
    tqc = transpile(qc_m, sim)
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()
    total = 0
    tot_shots = 0
    for bitstr, c in counts.items():
        # Qiskit bitstring: little-endian display, index 0 is rightmost char
        bs = bitstr.replace(' ', '')
        # For measure_all with n qubits, bs is length n, char[-1-q] is qubit q
        cut = 0
        for (u, v) in edges:
            bu = int(bs[-1 - u])
            bv = int(bs[-1 - v])
            if bu != bv:
                cut += 1
        total += cut * c
        tot_shots += c
    return total / tot_shots

# ---------------- Noise model ----------------
def make_noise_model(p1=1e-4, p2=1e-3):
    nm = NoiseModel()
    e1 = depolarizing_error(p1, 1)
    e2 = depolarizing_error(p2, 2)
    nm.add_all_qubit_quantum_error(e1, ['u1', 'u2', 'u3', 'rz', 'sx', 'x', 'rx', 'h'])
    nm.add_all_qubit_quantum_error(e2, ['cx'])
    return nm

# ---------------- Parameter optimization (noiseless) ----------------
def optimize_qaoa(edges, n, p, n_restarts=8, seed=0):
    rng = np.random.default_rng(seed)
    best = {'val': -np.inf, 'params': None}
    def neg_obj(x):
        gammas = x[:p]
        betas = x[p:]
        qc = qaoa_circuit(edges, n, gammas, betas)
        return -expected_cut_noiseless(qc, edges)
    for r in range(n_restarts):
        x0 = rng.uniform(0, np.pi, size=2*p)
        # gamma in [0, 2pi], beta in [0, pi]
        x0[:p] *= 2
        res = minimize(neg_obj, x0, method='COBYLA', options={'maxiter': 200, 'rhobeg': 0.3})
        if -res.fun > best['val']:
            best = {'val': -res.fun, 'params': res.x.tolist()}
    return best

# ---------------- Main ----------------
def main():
    out = {'meta': {}}
    out['meta']['paper'] = 'Preskill 2018 arXiv:1801.00862'
    out['meta']['thesis'] = 'NISQ (50-100 noisy qubits, depth 10-100) can plausibly do useful tasks; shallow variational circuits are the main near-term hope.'
    out['meta']['tool'] = 'Qiskit 2.5.0 + Aer 0.17.2 statevector + depolarizing noise model'
    out['meta']['graph'] = '3-regular random graph, n=10, seed=0'
    out['meta']['noise'] = {'p1_single': 1e-4, 'p2_two_qubit': 1e-3, 'model': 'depolarizing (Aer)'}
    out['meta']['shots_noisy'] = 8192

    t0 = time.time()
    N = 10
    edges = three_regular_graph(N, seed=0)
    out['meta']['edges'] = edges
    C_max, best_bits = classical_max_cut(edges, N)
    out['classical_max_cut'] = {'C_max': C_max, 'best_assignment_bits': int(best_bits)}
    print(f'Classical MAX-CUT on n={N}: C_max = {C_max}')

    nm = make_noise_model()

    results = {}
    for p in [1, 2]:
        print(f'--- QAOA p={p} ---')
        opt = optimize_qaoa(edges, N, p, n_restarts=6, seed=42+p)
        params = opt['params']
        r_ideal = opt['val'] / C_max
        # Rebuild circuit at optimum for noisy eval
        gammas = params[:p]
        betas = params[p:]
        qc = qaoa_circuit(edges, N, gammas, betas)
        exp_ideal = expected_cut_noiseless(qc, edges)
        # Sanity: exp_ideal ~= opt['val']
        exp_noisy = expected_cut_noisy(qc, edges, nm, shots=8192)
        r_noisy = exp_noisy / C_max
        depth = qc.decompose().depth()
        n_cx = sum(1 for inst in qc.decompose().data if inst.operation.name == 'cx')
        results[f'p={p}'] = {
            'opt_params_gamma': list(gammas),
            'opt_params_beta': list(betas),
            'exp_cut_noiseless': float(exp_ideal),
            'exp_cut_noisy': float(exp_noisy),
            'approx_ratio_noiseless': float(r_ideal),
            'approx_ratio_noisy': float(r_noisy),
            'degradation_delta': float(r_ideal - r_noisy),
            'circuit_depth': int(depth),
            'cx_count': int(n_cx),
        }
        print(f'  <C>_ideal = {exp_ideal:.3f} / {C_max}  r_ideal = {r_ideal:.3f}')
        print(f'  <C>_noisy = {exp_noisy:.3f} / {C_max}  r_noisy = {r_noisy:.3f}')
        print(f'  depth = {depth}  CX = {n_cx}  Delta = {r_ideal - r_noisy:+.3f}')

    out['results'] = results

    # NISQ-thesis-relevant summary
    out['nisq_thesis_check'] = {
        'central_claim': 'Shallow variational circuits maintain useful signal under NISQ noise.',
        'summary': f"p=1: ideal r={results['p=1']['approx_ratio_noiseless']:.3f}, noisy r={results['p=1']['approx_ratio_noisy']:.3f}, delta={results['p=1']['degradation_delta']:.3f}. "
                   f"p=2: ideal r={results['p=2']['approx_ratio_noiseless']:.3f}, noisy r={results['p=2']['approx_ratio_noisy']:.3f}, delta={results['p=2']['degradation_delta']:.3f}.",
        'random_cut_baseline_ratio': 0.5,
        'goemans_williamson_bound_approx': 0.878,
    }
    out['meta']['wallclock_sec'] = time.time() - t0

    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qaoa_nisq_results.json')
    with open(outpath, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nWrote {outpath}')
    print(f'Wallclock: {out["meta"]["wallclock_sec"]:.1f}s')

if __name__ == '__main__':
    main()
