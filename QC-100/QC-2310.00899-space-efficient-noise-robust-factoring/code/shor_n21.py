"""
Shor factoring pipeline for N=21 using Qiskit Aer.
N=21 = 3*7, n = ceil(log2(21)) = 5 bits.
Textbook 2n+3 = 13 qubits.

We use a generic 'quantum-arithmetic' modular multiplication:
build the permutation matrix explicitly and apply it as a UnitaryGate,
then wrap with .control().  This is slow for large n but fine for n=5.
"""
import json
import time
import numpy as np
from fractions import Fraction
from math import gcd
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT, UnitaryGate
from qiskit_aer import AerSimulator


def order_mod(a: int, N: int) -> int:
    for r in range(1, N + 1):
        if pow(a, r, N) == 1:
            return r
    return -1


def controlled_mult_a_mod_N(a: int, N: int, n_work: int) -> UnitaryGate:
    """Build a 2^n_work x 2^n_work permutation for x -> a*x mod N
    (identity for x >= N), then wrap as a UnitaryGate."""
    dim = 2 ** n_work
    U = np.zeros((dim, dim), dtype=complex)
    for x in range(dim):
        y = (a * x) % N if x < N else x
        U[y, x] = 1.0
    return UnitaryGate(U, label=f"*{a} mod {N}")


def build_circuit(N: int, a: int, n_count: int) -> QuantumCircuit:
    n_work = int(np.ceil(np.log2(N)))
    qc = QuantumCircuit(n_count + n_work, n_count)
    for q in range(n_count):
        qc.h(q)
    qc.x(n_count)  # |1> in work
    work = list(range(n_count, n_count + n_work))
    ord_a = order_mod(a, N)
    for j in range(n_count):
        power = 2 ** j
        effective = power % ord_a
        if effective == 0:
            continue
        a_pow = pow(a, effective, N)
        U = controlled_mult_a_mod_N(a_pow, N, n_work).control()
        qc.append(U, [j] + work)
    qft_inv = QFT(num_qubits=n_count, do_swaps=True, inverse=True).to_gate()
    qc.append(qft_inv, list(range(n_count)))
    qc.measure(range(n_count), range(n_count))
    return qc


def extract_order(measured_int: int, n_count: int, N: int):
    if measured_int == 0:
        return None
    phase = measured_int / (2 ** n_count)
    frac = Fraction(phase).limit_denominator(N)
    r = frac.denominator
    if r == 0 or r > N:
        return None
    return r


def try_factor(N: int, a: int, r: int):
    if r % 2:
        return None
    x = pow(a, r // 2, N)
    if x in (1, N - 1):
        return None
    f1 = gcd(x - 1, N); f2 = gcd(x + 1, N)
    for f in (f1, f2):
        if 1 < f < N:
            return (f, N // f)
    return None


def run(N=21, a=2, n_count=6, shots=2048):
    qc = build_circuit(N, a, n_count)
    n_work = int(np.ceil(np.log2(N)))
    sim = AerSimulator()
    t0 = time.time()
    tqc = transpile(qc, sim, optimization_level=1)
    t_trans = time.time() - t0
    depth = tqc.depth()
    n_gates = sum(tqc.count_ops().values())
    t1 = time.time()
    counts = sim.run(tqc, shots=shots).result().get_counts()
    sim_sec = time.time() - t1

    success_shots = 0; factor_pairs = {}; order_counts = {}
    for bs, c in counts.items():
        m = int(bs, 2)
        r = extract_order(m, n_count, N)
        if r is None: continue
        order_counts[r] = order_counts.get(r, 0) + c
        f = try_factor(N, a, r)
        if f:
            success_shots += c
            key = str(tuple(sorted(f)))
            factor_pairs[key] = factor_pairs.get(key, 0) + c
    return {
        "N": N, "a": a, "n_count": n_count, "n_work": n_work,
        "total_qubits": n_count + n_work,
        "textbook_shor_2n_plus_3": 2 * n_work + 3,
        "true_order": order_mod(a, N),
        "n_gates_transpiled": n_gates, "circuit_depth": depth,
        "transpile_sec": round(t_trans, 3), "sim_sec": round(sim_sec, 3),
        "shots": shots, "success_shots": success_shots,
        "success_prob": success_shots / shots,
        "factor_pairs": factor_pairs,
        "order_counts": order_counts,
        "top_counts": dict(sorted(counts.items(), key=lambda kv: -kv[1])[:8]),
    }


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("N=21 (=3*7) Shor factoring pipeline\n" + "=" * 60)
    results = []
    # bases coprime to 21
    for a in [2, 4, 5, 8, 10, 11, 13, 16, 17, 19, 20]:
        # skip a where order=1 (trivial) or a=N-1 (order 2, x=N-1)
        if gcd(a, 21) != 1:
            continue
        r_true = order_mod(a, 21)
        if r_true <= 1:
            continue
        res = run(N=21, a=a, n_count=6, shots=1024)
        print(f"  a={a:2d}  ord={r_true}  gates={res['n_gates_transpiled']}"
              f"  depth={res['circuit_depth']}  succ={res['success_prob']:.3f}"
              f"  sim={res['sim_sec']}s  factors={res['factor_pairs']}")
        results.append(res)
    (out_dir / "shor_n21_results.json").write_text(json.dumps({
        "N": 21, "n_count": 6, "n_work": 5, "total_qubits": 11,
        "textbook_shor_2n_plus_3_for_n5": 13,
        "per_base_results": results,
    }, indent=2, default=str))
    print("Wrote shor_n21_results.json")
