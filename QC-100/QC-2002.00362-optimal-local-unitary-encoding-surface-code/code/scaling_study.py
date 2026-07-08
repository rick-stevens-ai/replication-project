"""
Scaling study: build canonical Gottesman-style encoder for L=3,5,7 planar surface codes
using Stim's Tableau.from_stabilizers, and compare depth against paper's 2L bound.

The Cleve-Gottesman construction produces a valid unitary encoding circuit for any
stabilizer code from its generators. Stim.Tableau.from_stabilizers does this internally.

The resulting circuit is "canonical" and its depth is a fair proxy for the Dennis et al.
O(L^2) unitary encoder (both are non-optimized generic constructions).
"""

import stim
import time


def build_planar_surface_code(L):
    qubit_coords = {}
    coord_to_idx = {}
    idx = 0
    for r in range(2 * L - 1):
        if r % 2 == 0:
            for c in range(0, 2 * L - 1, 2):
                qubit_coords[idx] = (r, c)
                coord_to_idx[(r, c)] = idx
                idx += 1
        else:
            for c in range(1, 2 * L - 2, 2):
                qubit_coords[idx] = (r, c)
                coord_to_idx[(r, c)] = idx
                idx += 1
    n = idx
    assert n == L * L + (L - 1) * (L - 1)

    x_stabs = []
    for r in range(1, 2 * L - 1, 2):
        for c in range(0, 2 * L - 1, 2):
            support = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in coord_to_idx:
                    support.append(coord_to_idx[(nr, nc)])
            x_stabs.append(tuple(sorted(support)))

    z_stabs = []
    for r in range(0, 2 * L - 1, 2):
        for c in range(1, 2 * L - 2, 2):
            support = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in coord_to_idx:
                    support.append(coord_to_idx[(nr, nc)])
            z_stabs.append(tuple(sorted(support)))

    logical_z = tuple(coord_to_idx[(r, 0)] for r in range(0, 2 * L - 1, 2))
    logical_x = tuple(coord_to_idx[(0, c)] for c in range(0, 2 * L - 1, 2))

    return {
        'L': L, 'n': n,
        'qubit_coords': qubit_coords, 'coord_to_idx': coord_to_idx,
        'x_stabs': x_stabs, 'z_stabs': z_stabs,
        'logical_x': logical_x, 'logical_z': logical_z,
    }


def stabs_to_pauli_strings(code):
    """Convert stab supports to stim.PauliString on n qubits."""
    n = code['n']
    stabs = []
    for xs in code['x_stabs']:
        s = ['_'] * n
        for q in xs:
            s[q] = 'X'
        stabs.append(stim.PauliString(''.join(s)))
    for zs in code['z_stabs']:
        s = ['_'] * n
        for q in zs:
            s[q] = 'Z'
        stabs.append(stim.PauliString(''.join(s)))
    # For |0_L> we also fix logical Z to +1 (this is the "input" for the last logical qubit)
    s = ['_'] * n
    for q in code['logical_z']:
        s[q] = 'Z'
    stabs.append(stim.PauliString(''.join(s)))
    return stabs


def canonical_encoder_circuit(code):
    """
    Build the canonical Cleve-Gottesman-style encoder from Tableau.from_stabilizers.
    Returns a stim.Circuit that maps |0...0> to |0_L>.
    """
    stabs = stabs_to_pauli_strings(code)
    # Tableau.from_stabilizers returns a tableau whose Z_i stabilizers are mapped to the given stabs.
    # Applying this tableau's inverse to the |0...0> state maps it to the code state.
    tab = stim.Tableau.from_stabilizers(stabs, allow_redundant=False, allow_underconstrained=False)
    # Actually: from_stabilizers gives a tableau T such that T * Z_i * T^{-1} = stabs[i].
    # So T |0...0> = |code state>. We need to convert T to a circuit.
    circuit = tab.to_circuit(method='elimination')
    return circuit


def circuit_depth(circuit):
    """
    Compute depth (longest chain of gates through any qubit).
    Uses stim's own decomposition into ticks — but stim circuits from to_circuit don't have TICKs.
    We compute it manually via ASAP scheduling.
    """
    qubit_time = {}
    depth = 0
    for op in circuit:
        name = op.name
        if name in ('TICK', 'QUBIT_COORDS', 'DETECTOR', 'OBSERVABLE_INCLUDE', 'SHIFT_COORDS'):
            continue
        targets = op.targets_copy()
        # Group targets: two-qubit gates take pairs, single-qubit take singletons
        n_targets_per_gate = 2 if name in ('CNOT', 'CX', 'CZ', 'CY', 'SWAP', 'XCX', 'XCZ', 'XCY', 'YCX', 'YCY', 'YCZ', 'ZCX', 'ZCY', 'ZCZ') else 1
        for i in range(0, len(targets), n_targets_per_gate):
            qubits = [t.value for t in targets[i:i+n_targets_per_gate]]
            t = max(qubit_time.get(q, 0) for q in qubits) + 1
            for q in qubits:
                qubit_time[q] = t
            if t > depth:
                depth = t
    return depth


def count_two_qubit_gates(circuit):
    count = 0
    two_q_gates = {'CNOT', 'CX', 'CZ', 'CY', 'SWAP', 'XCX', 'XCZ', 'XCY', 'YCX', 'YCY', 'YCZ', 'ZCX', 'ZCY', 'ZCZ'}
    for op in circuit:
        if op.name in two_q_gates:
            count += len(op.targets_copy()) // 2
    return count


def verify_encoder_circuit(circuit, code):
    """Simulate the circuit on |0...0> and verify all stabilizers give +1."""
    n = code['n']
    sim = stim.TableauSimulator()
    # Initialize to |0...0>
    for q in range(n):
        sim.reset(q)
    sim.do_circuit(circuit)

    for i, xs in enumerate(code['x_stabs']):
        p = ['_'] * n
        for q in xs:
            p[q] = 'X'
        exp = sim.peek_observable_expectation(stim.PauliString(''.join(p)))
        if abs(exp - 1.0) > 1e-9:
            return False, f"X-stab {i} = {exp}"
    for i, zs in enumerate(code['z_stabs']):
        p = ['_'] * n
        for q in zs:
            p[q] = 'Z'
        exp = sim.peek_observable_expectation(stim.PauliString(''.join(p)))
        if abs(exp - 1.0) > 1e-9:
            return False, f"Z-stab {i} = {exp}"
    p = ['_'] * n
    for q in code['logical_z']:
        p[q] = 'Z'
    exp = sim.peek_observable_expectation(stim.PauliString(''.join(p)))
    if abs(exp - 1.0) > 1e-9:
        return False, f"logical_Z = {exp}"
    return True, "OK"


if __name__ == "__main__":
    print(f"{'L':<4} {'n':<6} {'X':<4} {'Z':<4} {'2L':<4} {'canonical_depth':<18} {'canonical_2Q':<14} {'valid':<8} {'time(s)':<8}")
    print("-" * 80)
    results = []
    for L in [3, 5, 7]:
        code = build_planar_surface_code(L)
        t0 = time.time()
        circ = canonical_encoder_circuit(code)
        depth = circuit_depth(circ)
        n_2q = count_two_qubit_gates(circ)
        valid, msg = verify_encoder_circuit(circ, code)
        elapsed = time.time() - t0
        print(f"{L:<4} {code['n']:<6} {len(code['x_stabs']):<4} {len(code['z_stabs']):<4} {2*L:<4} {depth:<18} {n_2q:<14} {'YES' if valid else 'NO':<8} {elapsed:<8.3f}")
        results.append((L, code['n'], depth, n_2q, valid, 2*L))

    # Save to CSV
    import csv
    with open('../report/evidence/scaling_results.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['L', 'n_qubits', 'canonical_depth', 'canonical_two_qubit_gates', 'valid_code_state', 'paper_2L_claim'])
        for row in results:
            w.writerow(row)
    print("\nSaved: report/evidence/scaling_results.csv")
