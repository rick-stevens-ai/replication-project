"""Reproduce the sample experiment from ToyotaCRDL/VQAPoisson sample.ipynb.

For each boundary condition (Periodic, Dirichlet, Neumann), build a 1D
Poisson problem on N = 2**num_qubits nodes with f(x) = uniform superposition
(after flipping the top qubit) -- the oracle from the upstream sample, which
encodes a uniform RHS up to phase. Optimize the variational ansatz with BFGS
and analytic parameter-shift gradients. Compare:
  * objective convergence
  * relative L2 error vs. classical np.linalg.solve(A, f)
  * trace-distance-like fidelity error
"""

import argparse
import json
import os
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit

from vqa_poisson_modern import VQAforPoisson


def build_oracle_f(num_qubits: int) -> QuantumCircuit:
    """Match the upstream sample: X on top qubit, then H on all qubits.

    The resulting statevector is, in little-endian Qiskit convention,
    proportional to a vector of +/- 1/sqrt(2**n) -- a sign-modulated uniform
    RHS. The exact pattern depends on qubit ordering; we use the same one as
    the upstream notebook so direct comparison is meaningful.
    """
    qc = QuantumCircuit(num_qubits)
    qc.x(num_qubits - 1)
    qc.h(qc.qubits)
    return qc


def run_single(bc: str, num_qubits: int, num_layers: int, seed: int = 0,
               method: str = 'bfgs', maxiter: int = 200, save_logs: bool = True):
    np.random.seed(seed)
    oracle_f = build_oracle_f(num_qubits)
    vqa = VQAforPoisson(num_qubits, num_layers, bc, oracle_f=oracle_f)

    x0 = list(4*np.pi*np.random.rand(vqa.num_params))
    t0 = time.time()
    res = vqa.minimize(x0,
                       method=method,
                       options={'maxiter': maxiter, 'disp': False},
                       use_grad=True,
                       save_logs=save_logs)
    wall = time.time() - t0

    final_err = vqa.get_errors(res.x)
    cl_sol = vqa.get_cl_sol()
    q_sol = vqa.get_sol(res.x)
    f_vec = vqa.get_f_vec()
    A = vqa.get_A_matrix()
    # Residual of classical and "quantum-reconstructed" solutions
    res_cl = np.linalg.norm(A @ cl_sol - f_vec) / np.linalg.norm(f_vec)
    res_q = np.linalg.norm(A @ q_sol - f_vec) / np.linalg.norm(f_vec)

    # Variational energy J = 0.5 x^T A x - x^T f, evaluated on real parts
    cl_real = np.real(cl_sol)
    q_real = np.real(q_sol)
    f_real = np.real(f_vec)
    J_cl = float(0.5*cl_real @ A @ cl_real - cl_real @ f_real)
    J_q = float(0.5*q_real @ A @ q_real - q_real @ f_real)

    return {
        'bc': bc,
        'num_qubits': num_qubits,
        'num_layers': num_layers,
        'seed': seed,
        'iterations': int(getattr(res, 'nit', len(vqa.objective_logs))),
        'objective_evals': int(vqa.objective_counts),
        'circuit_evals': int(vqa.circuit_counts),
        'final_objective': float(res.fun),
        'final_relative_l2_err': float(final_err['relative']),
        'final_trace_err': float(final_err['trace']),
        'classical_residual': float(res_cl),
        'quantum_residual': float(res_q),
        'classical_energy_J': J_cl,
        'quantum_energy_J': J_q,
        'energy_gap': float(J_q - J_cl),
        'wallclock_sec': float(wall),
        '_vqa': vqa,
        '_res': res,
        '_q_sol': q_sol,
        '_cl_sol': cl_sol,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bcs', nargs='+', default=['Periodic', 'Dirichlet', 'Neumann'])
    ap.add_argument('--num-qubits', type=int, default=3)
    ap.add_argument('--num-layers', type=int, default=4)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--maxiter', type=int, default=200)
    ap.add_argument('--outdir', default=str(Path(__file__).resolve().parent.parent / 'results'))
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    summary = []
    for bc in args.bcs:
        print(f'\n=== {bc}  n={args.num_qubits}  L={args.num_layers}  seed={args.seed} ===')
        r = run_single(bc, args.num_qubits, args.num_layers, args.seed, maxiter=args.maxiter)
        print(f"  iter={r['iterations']}  obj={r['final_objective']:.4e}  "
              f"rel_L2={r['final_relative_l2_err']:.3e}  trace={r['final_trace_err']:.3e}  "
              f"J_q-J_cl={r['energy_gap']:+.3e}  wall={r['wallclock_sec']:.1f}s")

        # plot solutions and convergence
        vqa = r['_vqa']
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        ax = axes[0]
        ax.plot(np.real(r['_q_sol']), 'k-', label='quantum')
        ax.plot(np.real(r['_cl_sol']), 'k--', label='classical')
        ax.set_xlabel('node index')
        ax.set_ylabel('solution amplitude (Re)')
        ax.set_title(f"{bc}  n={args.num_qubits}  L={args.num_layers}")
        ax.legend()
        ax.grid(True, alpha=0.3)

        ax = axes[1]
        if vqa.objective_logs:
            ax.semilogy(np.abs(np.array(vqa.objective_logs) - r['final_objective']) + 1e-16,
                        label='|J - J*|')
            if 'relative' in vqa.error_logs:
                ax.semilogy(vqa.error_logs['relative'], label='rel L2 err')
            if 'trace' in vqa.error_logs:
                ax.semilogy(vqa.error_logs['trace'], label='trace err')
            ax.set_xlabel('callback iter')
            ax.legend()
            ax.grid(True, which='both', alpha=0.3)
            ax.set_title('convergence')
        fig.tight_layout()
        fig.savefig(outdir / f'sol_{bc.lower()}_n{args.num_qubits}_L{args.num_layers}.png', dpi=120)
        plt.close(fig)

        # drop ephemera before JSON
        for k in ['_vqa', '_res', '_q_sol', '_cl_sol']:
            r.pop(k, None)
        summary.append(r)

    out_json = outdir / f'summary_n{args.num_qubits}_L{args.num_layers}.json'
    with out_json.open('w') as f:
        json.dump(summary, f, indent=2)
    print(f'\nWrote {out_json}')


if __name__ == '__main__':
    main()
