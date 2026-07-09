#!/usr/bin/env python3
"""Noise sweep supplement: fix the QAOA optimum (from qaoa_nisq_demo.py) and vary
the two-qubit depolarizing rate to characterize how the approximation ratio
degrades as noise increases — directly probing the NISQ operating band.
"""
import json, os, sys, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qaoa_nisq_demo import (three_regular_graph, classical_max_cut, qaoa_circuit,
                             expected_cut_noiseless, expected_cut_noisy, make_noise_model)

def main():
    N = 10
    edges = three_regular_graph(N, seed=0)
    C_max, _ = classical_max_cut(edges, N)

    # Load previously-optimized parameters
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qaoa_nisq_results.json')) as f:
        prev = json.load(f)

    sweep = {'C_max': C_max, 'shots': 8192, 'sweep': []}
    noise_levels = [0.0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
    for p_layers in [1, 2]:
        block = prev['results'][f'p={p_layers}']
        gammas = block['opt_params_gamma']
        betas = block['opt_params_beta']
        qc = qaoa_circuit(edges, N, gammas, betas)
        for p2 in noise_levels:
            if p2 == 0.0:
                r = expected_cut_noiseless(qc, edges) / C_max
                mode = 'statevector'
            else:
                nm = make_noise_model(p1=p2/10.0, p2=p2)
                r = expected_cut_noisy(qc, edges, nm, shots=8192) / C_max
                mode = 'aer_shots'
            sweep['sweep'].append({
                'p_qaoa_layers': p_layers,
                'p2_two_qubit_error': p2,
                'p1_single_qubit_error': p2/10.0 if p2 > 0 else 0.0,
                'approx_ratio': float(r),
                'mode': mode,
            })
            print(f'p={p_layers} p2={p2:.0e} r={r:.3f}')
    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qaoa_noise_sweep.json')
    with open(outpath, 'w') as f:
        json.dump(sweep, f, indent=2)
    print(f'Wrote {outpath}')

if __name__ == '__main__':
    main()
