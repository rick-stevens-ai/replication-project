"""Build a subset of the paper's benchmark circuits (small sizes for CPU tractability).

Circuits produced (as Qiskit QuantumCircuits, saved as QASM 2.0):
  - qaoa5   : 5-qubit QAOA MaxCut (ring)  --  paper: 42 CNOT, 27 sq
  - qaoa10  : 10-qubit QAOA MaxCut (ring) --  paper: 85 CNOT, 40 sq
  - grover3 : 3-qubit Grover (proxy for grover5; grover5 has 48 CNOT/80 sq)
  - adder4  : 4-qubit ripple-carry adder (proxy for adder9)
  - hub4    : Hubbard-ish trotter step on 4 qubits (proxy for hub4)

We follow paper's spec: transpile to {CNOT, U3} gate-set before comparison,
so both baseline and re-optimizer see the same starting representation.
"""
import os, json
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QAOAAnsatz, grover_operator
from qiskit.circuit.library.arithmetic import CDKMRippleCarryAdder
from qiskit.quantum_info import SparsePauliOp
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(OUT, 'benchmarks'), exist_ok=True)

def save(qc: QuantumCircuit, name: str):
    # Decompose to {CNOT, U3} using qiskit's transpiler with level 0 (no opt)
    basis = ['u3', 'cx']
    qc_dec = transpile(qc, basis_gates=basis, optimization_level=0)
    from qiskit.qasm2 import dumps
    path = os.path.join(OUT, 'benchmarks', f'{name}.qasm')
    with open(path, 'w') as f:
        f.write(dumps(qc_dec))
    ops = qc_dec.count_ops()
    print(f'{name}: qubits={qc_dec.num_qubits} depth={qc_dec.depth()} ops={dict(ops)}')
    return path, dict(ops), qc_dec.num_qubits, qc_dec.depth()


def build_qaoa_ring(n, p=1, seed=0):
    """QAOA MaxCut on a ring of n vertices, p layers."""
    rng = np.random.default_rng(seed)
    paulis = []
    for i in range(n):
        j = (i + 1) % n
        s = ['I'] * n
        s[i] = 'Z'; s[j] = 'Z'
        paulis.append((''.join(reversed(s)), 1.0))
    cost = SparsePauliOp.from_list(paulis)
    ans = QAOAAnsatz(cost_operator=cost, reps=p)
    # Bind random parameters
    params = rng.random(ans.num_parameters) * 2 * np.pi
    return ans.assign_parameters(params)


def build_grover(n_data=3):
    """Small Grover: n_data qubits, mark |1..1>."""
    from qiskit.circuit.library import PhaseOracle, MCMTGate, ZGate
    from qiskit.circuit import QuantumCircuit
    # Simple oracle: multi-controlled Z marking |11..1>
    oracle = QuantumCircuit(n_data)
    if n_data == 1:
        oracle.z(0)
    else:
        oracle.h(n_data - 1)
        oracle.mcx(list(range(n_data - 1)), n_data - 1)
        oracle.h(n_data - 1)
    grover_op = grover_operator(oracle)
    qc = QuantumCircuit(n_data)
    qc.h(range(n_data))
    qc.compose(grover_op, inplace=True)
    qc.compose(grover_op, inplace=True)
    return qc


def build_adder(n_bits=2):
    """Ripple-carry adder for two n-bit numbers => 2n+2 qubits."""
    adder = CDKMRippleCarryAdder(n_bits)
    return QuantumCircuit(adder.num_qubits).compose(adder)


def build_hubbard_trotter(n=4, steps=1, dt=0.1):
    """Very simple Hubbard-like trotter step on n qubits: alternating XX+YY (hopping) and Z (interaction).
    This is a proxy: real hub4 uses Bravyi-Kitaev mapping on 4-site spinful.
    """
    from qiskit.circuit.library import PauliEvolutionGate
    terms = []
    for i in range(n - 1):
        s_xx = ['I']*n; s_xx[i]='X'; s_xx[i+1]='X'
        s_yy = ['I']*n; s_yy[i]='Y'; s_yy[i+1]='Y'
        s_zz = ['I']*n; s_zz[i]='Z'; s_zz[i+1]='Z'
        terms.append((''.join(reversed(s_xx)), 1.0))
        terms.append((''.join(reversed(s_yy)), 1.0))
        terms.append((''.join(reversed(s_zz)), 0.5))
    H = SparsePauliOp.from_list(terms)
    evo = PauliEvolutionGate(H, time=dt)
    qc = QuantumCircuit(n)
    for _ in range(steps):
        qc.append(evo, list(range(n)))
    return qc


def main():
    info = {}
    qc = build_qaoa_ring(5, p=1, seed=1)
    p, ops, nq, d = save(qc, 'qaoa5')
    info['qaoa5'] = {'path': p, 'ops': ops, 'qubits': nq, 'depth': d,
                     'paper_cnot': 42, 'paper_sq': 27}

    qc = build_qaoa_ring(10, p=1, seed=2)
    p, ops, nq, d = save(qc, 'qaoa10')
    info['qaoa10'] = {'path': p, 'ops': ops, 'qubits': nq, 'depth': d,
                      'paper_cnot': 85, 'paper_sq': 40}

    qc = build_grover(3)
    p, ops, nq, d = save(qc, 'grover3')
    info['grover3'] = {'path': p, 'ops': ops, 'qubits': nq, 'depth': d,
                       'paper_cnot': 48, 'paper_sq': 80, 'proxy_for': 'grover5'}

    qc = build_adder(2)
    p, ops, nq, d = save(qc, 'adder4')
    info['adder4'] = {'path': p, 'ops': ops, 'qubits': nq, 'depth': d,
                      'paper_cnot': 98, 'paper_sq': 64, 'proxy_for': 'adder9'}

    qc = build_hubbard_trotter(4, steps=2, dt=0.5)
    p, ops, nq, d = save(qc, 'hub4')
    info['hub4'] = {'path': p, 'ops': ops, 'qubits': nq, 'depth': d,
                    'paper_cnot': 180, 'paper_sq': 155}

    with open(os.path.join(OUT, 'benchmarks', 'INDEX.json'), 'w') as f:
        json.dump(info, f, indent=2)
    print('\nWrote', os.path.join(OUT, 'benchmarks', 'INDEX.json'))


if __name__ == '__main__':
    main()
