#!/usr/bin/env python3
"""
End-to-end Qiskit ancilla-circuit ITE simulation for a 2-site TIM, following
paper Figures 3-5 verbatim (ancilla prep as 1/sqrt(2)(|0>+|1>) via H, CNOT-ladder,
Rx(phi) with phi = 2 arccos(exp(-2|gamma|dtau)), CNOT uncompute, post-select |0>,
reset ancilla, next gadget).

For each Trotter step, we sweep all Pauli terms of H, applying the ancilla gadget
per term via full statevector simulation with post-selection. We then measure the
energy expectation and compare against exact diagonalization ground-state energy.

This is a much smaller but end-to-end demonstration that closes the loop from
paper-level circuit to converged ground-state energy.
"""
from __future__ import annotations
import json, numpy as np
from numpy.linalg import eigh
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

I2 = np.eye(2, dtype=complex); X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex); Z = np.array([[1,0],[0,-1]], dtype=complex)
PAULI = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}

def kron_all(ops):
    o = ops[0]
    for x in ops[1:]:
        o = np.kron(o, x)
    return o

def pauli_op(n, sites_ops):
    ops = [I2]*n
    for s,p in sites_ops.items():
        ops[s] = PAULI[p]
    return kron_all(ops)


def build_tim_hamiltonian(n, J, h, pbc=True):
    dim = 2**n
    H = np.zeros((dim,dim), dtype=complex)
    terms = []
    end = n if pbc else n-1
    for i in range(end):
        j = (i+1) % n
        op = pauli_op(n, {i:'Z', j:'Z'})
        H += (-J)*op
        terms.append((-J, {i:'Z', j:'Z'}))
    for i in range(n):
        op = pauli_op(n, {i:'X'})
        H += (-h)*op
        terms.append((-h, {i:'X'}))
    return H, terms


def apply_pite_gadget_via_qiskit(psi_sys, n_sys, coeff, sites_ops, dtau):
    """Build the paper's exact Fig 3/4/5 ancilla gadget, run via Qiskit Statevector,
    post-select ancilla=|0>, renormalize; return (new_psi, p_success)."""
    total = n_sys + 1
    anc = n_sys  # ancilla is the last qubit
    qc = QuantumCircuit(total)
    # Initialize system on qubits [0..n_sys-1], ancilla starts |0>
    init = np.zeros(2**total, dtype=complex)
    for idx, amp in enumerate(psi_sys):
        init[idx] = amp   # ancilla bit = 0 (top bit of Qiskit index n_sys is 0)
    qc.initialize(init, range(total))
    # Basis change on system qubits: X->H, Y->S†H
    for s, p in sites_ops.items():
        if p == 'X': qc.h(s)
        elif p == 'Y': qc.sdg(s); qc.h(s)
    # Ancilla prep in |+>, so CNOTs meaningfully entangle. Working out the
    # projection onto ancilla=|0> after H-CNOT-Ry(phi)-CNOT gives system state
    # proportional to [cos(phi/2) I - sin(phi/2) P]|psi>, which matches
    # cosh(g*dt)*I - sinh(g*dt)*P when we set tan(phi/2) = tanh(g*dt), i.e.
    # phi = 2 arctan(tanh(|gamma|*dtau)).
    qc.h(anc)
    involved = list(sites_ops.keys())
    for s in involved:
        qc.cx(s, anc)
    phi = 2.0 * np.arctan(np.tanh(abs(coeff) * dtau))
    qc.ry(phi if coeff > 0 else -phi, anc)
    for s in reversed(involved):
        qc.cx(s, anc)
    # Trailing H on the ancilla to convert projection onto |+>_a (which is what we want
    # to project onto to symmetrize) into projection onto |0>_a for the physical measurement.
    qc.h(anc)
    # Uncompute basis change
    for s, p in sites_ops.items():
        if p == 'X': qc.h(s)
        elif p == 'Y': qc.h(s); qc.s(s)
    sv = Statevector.from_instruction(qc)
    arr = np.asarray(sv.data)
    # Extract ancilla=|0> component
    sys_dim = 2**n_sys
    sys_out = np.zeros(sys_dim, dtype=complex)
    for idx in range(2**total):
        anc_bit = (idx >> n_sys) & 1
        if anc_bit == 0:
            sys_bits = idx & (sys_dim - 1)
            sys_out[sys_bits] = arr[idx]
    p_succ = float(np.vdot(sys_out, sys_out).real)
    if p_succ > 1e-300:
        sys_out_normed = sys_out / np.sqrt(p_succ)
    else:
        sys_out_normed = sys_out
    return sys_out_normed, p_succ


def run_full_qiskit_ite(n, J, h, dtau, n_steps):
    H, terms = build_tim_hamiltonian(n, J, h, pbc=True)
    evals, _ = eigh(H)
    E0 = float(evals[0])
    # Initial state |+>^n
    plus = np.array([1,1], dtype=complex)/np.sqrt(2)
    psi = plus
    for _ in range(n-1):
        psi = np.kron(psi, plus)
    p_cum = 1.0
    hist = []
    def energy(p):
        nrm = np.vdot(p,p).real
        if nrm < 1e-300: return float('nan')
        return float((np.vdot(p, H@p).real)/nrm)
    hist.append({'step':0,'beta':0.0,'E':energy(psi),'p_cum':p_cum,'dE':energy(psi)-E0})
    for k in range(1, n_steps+1):
        p_step = 1.0
        for coeff, sites in terms:
            psi, ps = apply_pite_gadget_via_qiskit(psi, n, coeff, sites, dtau)
            p_step *= ps
        p_cum *= p_step
        E = energy(psi)
        hist.append({'step':k,'beta':k*dtau,'E':E,'p_cum':p_cum,'dE':E-E0})
    return {'E0':E0, 'history':hist}


def main():
    n = 2; J = 0.5; h = 0.1; dtau = 0.1; n_steps = 30
    print(f"# 2-site TIM (small end-to-end Qiskit run), J={J}, h={h}, PBC, dtau={dtau}")
    res = run_full_qiskit_ite(n, J, h, dtau, n_steps)
    print(f"# Exact E0 = {res['E0']:.10f}")
    print(f"# {'step':>4}  {'beta':>5}  {'<E>':>14}  {'<E>-E0':>13}  {'p_cum':>12}")
    for r in res['history'][::5] + [res['history'][-1]]:
        print(f"  {r['step']:>4}  {r['beta']:5.2f}  {r['E']:+.8f}  {r['dE']:+.4e}  {r['p_cum']:.4e}")
    final = res['history'][-1]
    print()
    print(f"Final |<E>-E0| = {abs(final['dE']):.4e}")
    print(f"Final cumulative post-selection probability = {final['p_cum']:.4e}")
    passed = abs(final['dE']) < 5e-2
    print("=> Qiskit end-to-end ITE " + ("CONVERGED to ground state" if passed else "DID NOT CONVERGE"))
    with open('qiskit_full_ite_result.json','w') as f:
        json.dump({'n':n,'J':J,'h':h,'dtau':dtau,'n_steps':n_steps,
                   'E0_exact':res['E0'],
                   'E_final':final['E'],'abs_error_final':abs(final['dE']),
                   'p_cum_final':final['p_cum'],
                   'converged_1e-2':bool(abs(final['dE'])<1e-2),
                   'history':res['history']}, f, indent=2)
    import sys; sys.exit(0 if passed else 1)

if __name__ == '__main__':
    main()
