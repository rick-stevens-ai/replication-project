"""Control comparison: Draper's QFT-based adder (arXiv:quant-ph/0008033),
using qiskit.circuit.library.DraperQFTAdder as the reference implementation.

Draper adder (fixed): |a>|b> -> |a>|a+b mod 2^n>. 2n qubits (0 ancilla).
Compare gate/qubit resources vs. the CDKM optimized adder (2n+2 qubits,
1 non-input ancilla + 1 output high bit).
"""
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import DraperQFTAdder
from qiskit_aer import AerSimulator
import numpy as np, json, sys
sys.path.insert(0, ".")
from cdkm import optimized_adder, simple_adder


def decompose_fully(qc):
    """Decompose repeatedly until only basic gates remain."""
    prev = -1
    for _ in range(10):
        d = qc.decompose()
        if d.depth() == prev:
            break
        prev = d.depth()
        qc = d
    return qc


def resource(qc):
    ops = qc.count_ops()
    return {"h": ops.get("h", 0), "cp": ops.get("cp", 0),
            "cnot": ops.get("cx", 0), "ccx": ops.get("ccx", 0),
            "x": ops.get("x", 0), "u": ops.get("u", 0),
            "num_qubits": qc.num_qubits, "depth": qc.depth()}


def draper_verify(n, a, b):
    """Spot-check DraperQFTAdder on |a>|b> and read out |a>|a+b mod 2^n>."""
    d = DraperQFTAdder(n, kind='fixed')
    # By DraperQFTAdder convention: register order is [a_0..a_{n-1}, b_0..b_{n-1}]
    prep = QuantumCircuit(2 * n)
    for i in range(n):
        if (a >> i) & 1: prep.x(i)
        if (b >> i) & 1: prep.x(n + i)
    full = prep.compose(d)
    full.save_statevector()
    sim = AerSimulator(method="statevector")
    sv = sim.run(transpile(full, sim)).result().get_statevector()
    probs = np.abs(sv.data) ** 2
    idx = int(np.argmax(probs))
    a_out = sum(((idx >> i) & 1) << i for i in range(n))
    b_out = sum(((idx >> (n + i)) & 1) << i for i in range(n))
    return a_out, b_out, float(probs[idx])


results = {"draper_qft": [], "spot_checks": [], "comparison": []}

for n in [2, 3, 4, 6, 8]:
    d = DraperQFTAdder(n, kind='fixed')
    d_dec = decompose_fully(d)
    r = resource(d_dec); r["n"] = n; r["variant"] = "draper_qft"
    results["draper_qft"].append(r)

    # Spot check a few random pairs
    for (a, b) in [(1, 1), (3, 5), ((1 << n) - 1, (1 << n) - 1)]:
        a %= (1 << n); b %= (1 << n)
        a_out, b_out, prob = draper_verify(n, a, b)
        exp = (a + b) & ((1 << n) - 1)
        ok = (a_out == a and b_out == exp)
        results["spot_checks"].append({"n": n, "a": a, "b": b,
                                       "a_out": a_out, "b_out": b_out,
                                       "expected": exp, "prob": round(prob, 4),
                                       "ok": ok})
        print(f"[{'PASS' if ok else 'FAIL'}] Draper n={n} a={a} b={b} -> "
              f"A={a_out} B={b_out} (expected B={exp}) p={prob:.4f}")

    # Comparison table
    cdkm_opt = optimized_adder(n) if n >= 4 else None
    cdkm_simp = simple_adder(n, "2cnot")
    cmp = {"n": n,
           "cdkm_simple_qubits": cdkm_simp.num_qubits,
           "cdkm_simple_toffoli": cdkm_simp.count_ops().get("ccx", 0),
           "cdkm_simple_cnot": cdkm_simp.count_ops().get("cx", 0),
           "cdkm_simple_depth": cdkm_simp.depth(),
           "cdkm_opt_qubits": cdkm_opt.num_qubits if cdkm_opt else None,
           "cdkm_opt_toffoli": cdkm_opt.count_ops().get("ccx", 0) if cdkm_opt else None,
           "cdkm_opt_cnot":    cdkm_opt.count_ops().get("cx", 0) if cdkm_opt else None,
           "cdkm_opt_depth":   cdkm_opt.depth() if cdkm_opt else None,
           "draper_qubits":    d.num_qubits,
           "draper_cp_gates":  r["cp"],
           "draper_h_gates":   r["h"],
           "draper_depth":     r["depth"],
           }
    results["comparison"].append(cmp)

with open("draper_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nWritten draper_results.json")
