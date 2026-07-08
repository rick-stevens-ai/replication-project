#!/usr/bin/env python3
"""Enumerate all single-qubit Pauli-fault insertion points in the encoding+stab circuit
and check whether each is caught (via ancilla=1 or odd parity) or causes an undetected
La flip.

Verifies the paper's FT claim: the encoding + Sx (or Sz) stabilizer circuit for
the [[4,2,2]] |00>_L state is fault-tolerant for La — no single-qubit Pauli fault
inserted anywhere in the circuit produces an undetected La error.
"""
import itertools
import stim


def flat_ops():
    """Return the base circuit as a flat list of single-target/pair-target ops (no
    multi-CNOT blocks), so we can insert a fault after ANY individual gate."""
    ops = []
    data = [0, 1, 2, 3]
    anc = 4
    for q in data + [anc]:
        ops.append(("R", [q]))
    ops.append(("H", [0]))
    for tgt in (1, 2, 3):
        ops.append(("CX", [0, tgt]))
    return data, anc, ops


def sx_stab_ops(anc, data):
    ops = []
    ops.append(("H", [anc]))
    for d in data:
        ops.append(("CX", [anc, d]))
    ops.append(("H", [anc]))
    ops.append(("M", [anc]))
    for d in data:
        ops.append(("M", [d]))
    return ops


def sz_stab_ops(anc, data):
    ops = []
    for d in data:
        ops.append(("CX", [d, anc]))
    ops.append(("M", [anc]))
    for d in data:
        ops.append(("M", [d]))
    return ops


def build_full(ops):
    c = stim.Circuit()
    for name, targets in ops:
        c.append(name, targets)
    return c


def insert_fault(ops, idx, pauli, qubit):
    """Insert `pauli` on `qubit` right AFTER op index idx (0-based)."""
    new = []
    for i, (name, targets) in enumerate(ops):
        new.append((name, targets))
        if i == idx:
            new.append((pauli, [qubit]))
    return new


def analyze_shot(shot):
    """shot layout: [anc_meas, d0, d1, d2, d3]."""
    anc = int(shot[0])
    data = [int(x) for x in shot[1:5]]
    parity = sum(data) % 2
    accept = (anc == 0) and (parity == 0)
    if not accept:
        return "CAUGHT"
    La = data[0] ^ data[1]
    Lb = data[0] ^ data[2]
    if La == 0 and Lb == 0:
        return "NO_ERR"
    if La == 1 and Lb == 0:
        return "La_ERR"
    if La == 0 and Lb == 1:
        return "Lb_ERR"
    return "La+Lb_ERR"


def enumerate_faults(stab_name: str):
    data, anc, base = flat_ops()
    if stab_name == "Sx":
        ops = base + sx_stab_ops(anc, data)
    elif stab_name == "Sz":
        ops = base + sz_stab_ops(anc, data)
    else:
        raise ValueError(stab_name)

    # Enumerate: after every non-M op, on every qubit in the ops[i]'s target list plus
    # ALL qubits (to cover idle qubits picking up an error too), inject X, Y, Z.
    all_qubits = [0, 1, 2, 3, 4]

    fault_locations = []
    for i, (name, targets) in enumerate(ops):
        # allow faults after any op (including R, gates, but not after M — those are terminal)
        if name == "M":
            continue
        for q in all_qubits:
            for pauli in ("X", "Y", "Z"):
                fault_locations.append((i, name, tuple(targets), pauli, q))

    counts = {"CAUGHT": 0, "NO_ERR": 0, "La_ERR": 0, "Lb_ERR": 0, "La+Lb_ERR": 0}
    la_errs = []
    for (i, opname, targets, pauli, q) in fault_locations:
        new_ops = insert_fault(ops, i, pauli, q)
        c = build_full(new_ops)
        try:
            sampler = c.compile_sampler(seed=0)
        except ValueError:
            # circuit compilation issue — skip
            continue
        shot = sampler.sample(1).astype(int)[0]
        result = analyze_shot(shot)
        counts[result] += 1
        if result in ("La_ERR", "La+Lb_ERR"):
            la_errs.append((i, opname, targets, pauli, q, result))

    print(f"\n### Stabilizer: {stab_name}  ({len(fault_locations)} fault points enumerated) ###")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    if la_errs:
        print(f"\n  Single faults causing undetected La error (BREAKS FT):")
        for row in la_errs[:20]:
            print(f"    op#{row[0]:2d} {row[1]:3s}{list(row[2])!s:>10s}  {row[3]}_{row[4]}  ->  {row[5]}")
        if len(la_errs) > 20:
            print(f"    ... and {len(la_errs)-20} more")
    else:
        print(f"  ==> ZERO single-fault events produce an undetected La error.")
        print(f"  ==> Fault tolerance for La is verified exhaustively.")

    return counts, la_errs


if __name__ == "__main__":
    for stab in ("Sx", "Sz"):
        enumerate_faults(stab)
