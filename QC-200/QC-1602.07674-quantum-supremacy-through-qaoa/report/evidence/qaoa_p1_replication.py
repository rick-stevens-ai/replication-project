#!/usr/bin/env python3
"""
Independent replication of the p=1 QAOA construction analyzed in
Farhi & Harrow (arXiv:1602.07674).

This paper is primarily complexity-theoretic (it argues that classically
sampling from a p=1 QAOA output distribution collapses the polynomial
hierarchy). It does not report a new empirical benchmark number. To make a
CONCRETE, REPRODUCIBLE numeric spot-check on top of the same p=1 QAOA object
the paper analyzes, we reproduce two canonical p=1 QAOA MAX-CUT results
inherited from Farhi, Goldstone, Gutmann (refs [18,19] in the paper):

  (A) Rings (2-regular graph, N even): the optimal p=1 QAOA MaxCut
      expected cut fraction per edge is (1/2)(1 + sin(4β) sin(2γ)/1),
      whose maximum equals 3/4 at (γ*, β*) = (π/4, π/8).
      => headline number to hit: 0.75 (approximation ratio for even N).

  (B) A specific 3-regular graph (K_4, the complete graph on 4 vertices,
      which is 3-regular): compute p=1 QAOA expectation numerically via
      statevector simulation, grid-search over (γ,β), report best
      approximation ratio C_QAOA/C_max. The Farhi-Goldstone-Gutmann worst
      case lower bound for 3-regular graphs is 0.6924.

We report REAL statevector-simulated numbers and compare vs the analytic
targets.
"""
import json, itertools, math, sys, time
from pathlib import Path
import numpy as np
import networkx as nx
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

RESULTS = {}

def maxcut_cost_hamiltonian(G):
    """H_C = sum_{(i,j) in E} 0.5*(I - Z_i Z_j).  Return (op, offset).
    Here we build the operator that we use as observable, i.e. actual
    number-of-cut-edges observable.
    """
    n = G.number_of_nodes()
    paulis = []
    coeffs = []
    offset = 0.0
    for (i, j) in G.edges():
        # 0.5*(I - Z_i Z_j) contributes +0.5 to identity and -0.5 to ZZ
        offset += 0.5
        z = ['I'] * n
        # Qiskit label ordering: leftmost is qubit n-1
        z[n-1-i] = 'Z'
        z[n-1-j] = 'Z'
        paulis.append(''.join(z))
        coeffs.append(-0.5)
    op = SparsePauliOp.from_list(list(zip(paulis, coeffs)))
    return op, offset

def qaoa_p1_circuit(G, gamma, beta):
    n = G.number_of_nodes()
    qc = QuantumCircuit(n)
    qc.h(range(n))
    # cost unitary exp(-i gamma H_C).  Each edge contributes
    # exp(-i gamma * 0.5*(I - Z_i Z_j)) = e^{-i gamma/2} * exp(+i gamma/2 Z_i Z_j)
    # global phase drops out; effective 2-qubit rotation is Rzz(-gamma):
    # In Qiskit, rzz(theta) = exp(-i theta/2 Z Z). We want exp(+i gamma/2 ZZ)
    # => theta = -gamma
    for (i, j) in G.edges():
        qc.rzz(-gamma, i, j)
    # mixer exp(-i beta B), B = sum X_i => Rx(2 beta) on each qubit
    for q in range(n):
        qc.rx(2*beta, q)
    return qc

def qaoa_p1_expectation(G, gamma, beta):
    qc = qaoa_p1_circuit(G, gamma, beta)
    sv = Statevector.from_instruction(qc)
    op, offset = maxcut_cost_hamiltonian(G)
    expval = np.real(sv.expectation_value(op)) + offset
    return expval

def brute_maxcut(G):
    n = G.number_of_nodes()
    best = 0
    for bits in range(1 << n):
        cut = 0
        for (i, j) in G.edges():
            bi = (bits >> i) & 1
            bj = (bits >> j) & 1
            if bi != bj:
                cut += 1
        if cut > best:
            best = cut
    return best

def analytic_ring_edge_expectation(gamma, beta):
    """Per-edge expected cut for p=1 QAOA on an even ring (2-regular graph).

    Standard Farhi-Goldstone-Gutmann result for a d-regular triangle-free
    graph edge:
        <C_e> = 1/2 + (1/2) sin(4 beta) sin(2 gamma) cos^{d-1}(2 gamma).
    For a plain even ring, d=2 so the neighborhood-suppression factor is
    cos(2 gamma). The maximum of
        (1/2)(1 + sin(4 beta) sin(2 gamma) cos(2 gamma))
      = (1/2)(1 + (1/2) sin(4 beta) sin(4 gamma))
    is 3/4 at sin(4 beta) = sin(4 gamma) = 1, e.g. beta=pi/8, gamma=pi/8.
    Since this is per-edge and Cmax/|E| = 1 for even ring, the approximation
    ratio equals the per-edge expectation. Analytic headline: 0.75.
    """
    return 0.5 + 0.5*np.sin(4*beta)*np.sin(2*gamma)*np.cos(2*gamma)

# ------------------------------------------------------------
# (A) Even ring, N=6
# ------------------------------------------------------------
def run_ring(N=6):
    G = nx.cycle_graph(N)
    Cmax = brute_maxcut(G)  # N for even ring
    E = G.number_of_edges()
    # grid search
    gammas = np.linspace(0, np.pi, 61)
    betas = np.linspace(0, np.pi/2, 31)
    best = (-1, None, None)
    for g in gammas:
        for b in betas:
            v = qaoa_p1_expectation(G, g, b)
            if v > best[0]:
                best = (v, g, b)
    ev, g_star, b_star = best
    # Fine-tune around analytic optimum
    from scipy.optimize import minimize
    res = minimize(lambda x: -qaoa_p1_expectation(G, x[0], x[1]),
                   x0=[g_star, b_star], method='Nelder-Mead',
                   options={'xatol':1e-6, 'fatol':1e-8})
    ev_opt = -res.fun
    g_opt, b_opt = res.x
    ratio = ev_opt / Cmax
    per_edge = ev_opt / E
    # analytic per edge at optimum (gamma=pi/8, beta=pi/8)
    analytic_per_edge = analytic_ring_edge_expectation(np.pi/8, np.pi/8)
    result = dict(
        N=N,
        edges=E,
        Cmax=Cmax,
        best_expectation=float(ev_opt),
        best_gamma=float(g_opt),
        best_beta=float(b_opt),
        approximation_ratio=float(ratio),
        expected_per_edge=float(per_edge),
        analytic_per_edge_at_pi8_pi8=float(analytic_per_edge),
        analytic_expected_ratio=0.75,
        match_analytic_within_1pct=bool(abs(ratio - 0.75) < 0.01),
    )
    return result

# ------------------------------------------------------------
# (B) K_4 (complete graph on 4 vertices, 3-regular)
# ------------------------------------------------------------
def run_k4():
    G = nx.complete_graph(4)  # 3-regular, 6 edges
    Cmax = brute_maxcut(G)  # 4 (two-way split 2+2)
    E = G.number_of_edges()
    gammas = np.linspace(0, np.pi, 101)
    betas = np.linspace(0, np.pi/2, 51)
    best = (-1, None, None)
    for g in gammas:
        for b in betas:
            v = qaoa_p1_expectation(G, g, b)
            if v > best[0]:
                best = (v, g, b)
    ev, g_star, b_star = best
    from scipy.optimize import minimize
    res = minimize(lambda x: -qaoa_p1_expectation(G, x[0], x[1]),
                   x0=[g_star, b_star], method='Nelder-Mead',
                   options={'xatol':1e-6, 'fatol':1e-8})
    ev_opt = -res.fun
    g_opt, b_opt = res.x
    ratio = ev_opt / Cmax
    result = dict(
        graph='K_4 (complete graph on 4 vertices, 3-regular)',
        N=4, edges=E, Cmax=Cmax,
        best_expectation=float(ev_opt),
        best_gamma=float(g_opt),
        best_beta=float(b_opt),
        approximation_ratio=float(ratio),
        farhi_gg_bound_3reg=0.6924,
        beats_farhi_gg_bound=bool(ratio >= 0.6924),
    )
    return result

# ------------------------------------------------------------
# (C) An 8-node 3-regular graph (random 3-regular, seed=42)
# ------------------------------------------------------------
def run_3reg_8():
    G = nx.random_regular_graph(3, 8, seed=42)
    Cmax = brute_maxcut(G)
    E = G.number_of_edges()
    gammas = np.linspace(0, np.pi, 61)
    betas = np.linspace(0, np.pi/2, 31)
    best = (-1, None, None)
    for g in gammas:
        for b in betas:
            v = qaoa_p1_expectation(G, g, b)
            if v > best[0]:
                best = (v, g, b)
    ev, g_star, b_star = best
    from scipy.optimize import minimize
    res = minimize(lambda x: -qaoa_p1_expectation(G, x[0], x[1]),
                   x0=[g_star, b_star], method='Nelder-Mead',
                   options={'xatol':1e-6, 'fatol':1e-8})
    ev_opt = -res.fun
    g_opt, b_opt = res.x
    ratio = ev_opt / Cmax
    result = dict(
        graph='random 3-regular, N=8, seed=42',
        N=8, edges=E, Cmax=Cmax,
        best_expectation=float(ev_opt),
        best_gamma=float(g_opt),
        best_beta=float(b_opt),
        approximation_ratio=float(ratio),
        farhi_gg_bound_3reg=0.6924,
        beats_farhi_gg_bound=bool(ratio >= 0.6924),
    )
    return result

if __name__ == "__main__":
    t0 = time.time()
    RESULTS['env'] = dict(
        qiskit=__import__('qiskit').__version__,
        aer=__import__('qiskit_aer').__version__,
        numpy=np.__version__,
        networkx=nx.__version__,
    )
    print("[1/3] Even ring N=6 (analytic target: approximation ratio = 0.75) ...", flush=True)
    RESULTS['ring_6'] = run_ring(6)
    print(json.dumps(RESULTS['ring_6'], indent=2))
    print("[2/3] K_4 3-regular (target: >= 0.6924 Farhi-GG bound) ...", flush=True)
    RESULTS['k4'] = run_k4()
    print(json.dumps(RESULTS['k4'], indent=2))
    print("[3/3] Random 3-regular N=8 (target: >= 0.6924) ...", flush=True)
    RESULTS['reg3_8'] = run_3reg_8()
    print(json.dumps(RESULTS['reg3_8'], indent=2))
    RESULTS['elapsed_sec'] = time.time() - t0
    out = Path(__file__).parent / "qaoa_p1_results.json"
    out.write_text(json.dumps(RESULTS, indent=2))
    print(f"\nSaved: {out}")
    # Ring analytic check
    print(f"\nRing N=6: ratio={RESULTS['ring_6']['approximation_ratio']:.6f}  target=0.75  match={RESULTS['ring_6']['match_analytic_within_1pct']}")
    print(f"K_4    : ratio={RESULTS['k4']['approximation_ratio']:.6f}  Farhi-GG bound 0.6924  beats={RESULTS['k4']['beats_farhi_gg_bound']}")
    print(f"3-reg8 : ratio={RESULTS['reg3_8']['approximation_ratio']:.6f}  Farhi-GG bound 0.6924  beats={RESULTS['reg3_8']['beats_farhi_gg_bound']}")
