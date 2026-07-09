"""Fast exhaustive verification of CDKM adders.

We exploit the fact that all circuits consist only of X, CNOT, CCX gates,
which act as permutations on computational basis states. So we can simulate
classically by walking the gate list and updating a bit vector. This makes
n=8 (2^17 = 131072 inputs) feasible in seconds.
"""

import json, time, sys
sys.path.insert(0, ".")
from cdkm import simple_adder, optimized_adder, resource_counts


def classical_run(qc, init_bits):
    """Simulate a QuantumCircuit (only X/CX/CCX allowed) on classical bits.
    init_bits: list of ints (0/1), length = qc.num_qubits.
    Returns the final bit list.
    """
    bits = list(init_bits)
    q_of = {q: i for i, q in enumerate(qc.qubits)}
    for instr in qc.data:
        name = instr.operation.name
        qs = [q_of[q] for q in instr.qubits]
        if name == "x":
            bits[qs[0]] ^= 1
        elif name == "cx":
            if bits[qs[0]]:
                bits[qs[1]] ^= 1
        elif name == "ccx":
            if bits[qs[0]] and bits[qs[1]]:
                bits[qs[2]] ^= 1
        else:
            raise RuntimeError(f"unexpected gate {name}")
    return bits


def verify_fast(adder_fn, n, tag, **kwargs):
    if kwargs:
        qc = adder_fn(n, **kwargs)
    else:
        qc = adder_fn(n)
    nq = qc.num_qubits
    n_tests = 0
    n_pass = 0
    failures = []
    for a in range(1 << n):
        for b in range(1 << n):
            for z in (0, 1):
                init = [0] * nq
                # X ancilla (qubit 0) stays 0
                # A_i on 2i+2, B_i on 2i+1, Z on 2n+1
                for i in range(n):
                    if (a >> i) & 1: init[2 * i + 2] = 1
                    if (b >> i) & 1: init[2 * i + 1] = 1
                if z: init[2 * n + 1] = 1
                out = classical_run(qc, init)
                X_out = out[0]
                B_out = sum(out[2 * i + 1] << i for i in range(n))
                A_out = sum(out[2 * i + 2] << i for i in range(n))
                Z_out = out[2 * n + 1]
                s_full = a + b
                s_mod = s_full & ((1 << n) - 1)
                s_n = (s_full >> n) & 1
                ok = (X_out == 0 and A_out == a and B_out == s_mod and Z_out == (z ^ s_n))
                n_tests += 1
                if ok:
                    n_pass += 1
                else:
                    if len(failures) < 5:
                        failures.append({"a": a, "b": b, "z": z, "s_mod": s_mod,
                                         "s_n": s_n, "X": X_out, "A": A_out,
                                         "B": B_out, "Z": Z_out})
    return {"tag": tag, "n": n, "n_tests": n_tests, "n_pass": n_pass,
            "all_pass": n_pass == n_tests, "failures_sample": failures}


def main():
    results = {"simple_2cnot": [], "simple_3cnot": [], "optimized": []}
    for n in [2, 3, 4, 6, 8]:
        for tag, fn, kwargs in [
            ("simple_2cnot", simple_adder, {"uma_variant": "2cnot"}),
            ("simple_3cnot", simple_adder, {"uma_variant": "3cnot"}),
            ("optimized",    optimized_adder, {}),
        ]:
            if tag == "optimized" and n < 4:
                continue
            t0 = time.time()
            r = verify_fast(fn, n, tag, **kwargs)
            r["elapsed_s"] = round(time.time() - t0, 2)
            if fn is optimized_adder:
                qc = fn(n)
            else:
                qc = fn(n, **kwargs)
            r["resources"] = resource_counts(qc)
            results[tag].append(r)
            status = "PASS" if r["all_pass"] else "FAIL"
            print(f"[{status}] {tag} n={n}: {r['n_pass']}/{r['n_tests']} in {r['elapsed_s']}s "
                  f"(T={r['resources']['toffoli']} C={r['resources']['cnot']} "
                  f"N={r['resources']['not']} d={r['resources']['depth_high_level']})")
            if not r["all_pass"]:
                print("  failures:", r["failures_sample"][:2])
    with open("verify_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nWritten verify_results.json")


if __name__ == "__main__":
    main()
