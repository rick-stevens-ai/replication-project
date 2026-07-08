#!/usr/bin/env python3
"""Verify a FT [[4,2,2]] |00>_L encoding with a flag qubit that catches propagating
X errors on q0 during the middle CNOT window.

Circuit (5 data qubits + 1 flag):
  R q0..q4 (q4 = flag ancilla)
  H q0
  CX q0 -> q1
  CX q0 -> q4    # flag ON
  CX q0 -> q2
  CX q0 -> q4    # flag OFF
  CX q0 -> q3
  M q4           # measure and postselect flag = 0
  (then stabilizer + terminal data readout, still using another physical ancilla q5)

Enumerate all single-qubit Pauli faults; check that NO single fault produces an
undetected La error (postselecting flag=0, syndrome ancilla=0, and even data parity).
"""
import stim


def build_ops():
    data = [0, 1, 2, 3]
    flag = 4
    stab_anc = 5

    ops = []
    # reset
    for q in data + [flag, stab_anc]:
        ops.append(("R", [q]))
    # FT encoding with flag — wrap ALL data CNOTs between two flag CNOTs so
    # any X propagation from q0 during the window flips the flag qubit.
    ops.append(("H", [0]))
    ops.append(("CX", [0, flag]))   # flag ON  (couples q0 to flag)
    ops.append(("CX", [0, 1]))
    ops.append(("CX", [0, 2]))
    ops.append(("CX", [0, 3]))
    ops.append(("CX", [0, flag]))   # flag OFF (uncouples)
    # measure flag (index 0 in measurement stream)
    ops.append(("M", [flag]))

    # Sx stabilizer measurement using stab_anc
    ops.append(("H", [stab_anc]))
    for d in data:
        ops.append(("CX", [stab_anc, d]))
    ops.append(("H", [stab_anc]))
    ops.append(("M", [stab_anc]))    # index 1

    # data terminal measurement
    for d in data:
        ops.append(("M", [d]))       # indices 2..5

    return ops, data, flag, stab_anc


def build_full(ops):
    c = stim.Circuit()
    for name, targets in ops:
        c.append(name, targets)
    return c


def insert_fault(ops, idx, pauli, qubit):
    new = []
    for i, (n, t) in enumerate(ops):
        new.append((n, t))
        if i == idx:
            new.append((pauli, [qubit]))
    return new


def analyze_shot(shot):
    flag = int(shot[0])
    stab = int(shot[1])
    data = [int(x) for x in shot[2:6]]
    parity = sum(data) % 2
    accept = (flag == 0) and (stab == 0) and (parity == 0)
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


def enumerate_faults(verbose=True):
    ops, data, flag, stab_anc = build_ops()
    all_q = list(range(6))
    fault_locations = []
    for i, (n, t) in enumerate(ops):
        if n == "M":
            continue
        for q in all_q:
            for p in ("X", "Y", "Z"):
                fault_locations.append((i, n, tuple(t), p, q))

    counts = {"CAUGHT": 0, "NO_ERR": 0, "La_ERR": 0, "Lb_ERR": 0, "La+Lb_ERR": 0}
    la_errs = []
    for (i, n, t, p, q) in fault_locations:
        new_ops = insert_fault(ops, i, p, q)
        c = build_full(new_ops)
        sampler = c.compile_sampler(seed=0)
        shot = sampler.sample(1).astype(int)[0]
        r = analyze_shot(shot)
        counts[r] += 1
        if r in ("La_ERR", "La+Lb_ERR"):
            la_errs.append((i, n, t, p, q, r))

    if verbose:
        print(f"### FT with flag qubit, {len(fault_locations)} fault points ###")
        for k, v in counts.items():
            print(f"  {k}: {v}")
        if la_errs:
            print(f"\n  BAD single-fault -> La error:")
            for row in la_errs[:15]:
                print(f"    op#{row[0]:2d} {row[1]:3s}{list(row[2])!s:>12s} {row[3]}_{row[4]} -> {row[5]}")
            if len(la_errs) > 15:
                print(f"    ... {len(la_errs)-15} more")
        else:
            print(f"\n  ==> ZERO single faults produce an undetected La error.")
            print(f"  ==> Flag-qubit FT encoding is fault-tolerant for La.")
    return counts, la_errs


if __name__ == "__main__":
    enumerate_faults()
