"""
Shor-style factoring pipeline for N=15 using Qiskit Aer (fast version).

Implements order-finding for a in Z_15^* using directly-built controlled
gates (cswap = Fredkin, cx) rather than large synthesized controlled
unitaries; this keeps the transpiled circuit small and the sim fast.

Baseline for the Ragavan-Vaikuntanathan paper (arXiv:2310.00899). Their
paper is a theoretical construction (Regev + Fibonacci exponentiation);
this reproduction demonstrates the underlying Shor-style order-finding
pipeline that Regev's algorithm generalizes, plus qubit-count comparison
and a noise-robustness demonstration.
"""
import math
import json
import time
from fractions import Fraction
from math import gcd
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


def _order_of_a_mod15(a: int) -> int:
    for r in range(1, 16):
        if pow(a, r, 15) == 1:
            return r
    raise ValueError(f"a={a} has no order mod 15")


def add_controlled_amod15(qc: QuantumCircuit, ctrl: int, work: list[int],
                          a: int, power: int) -> None:
    """Append controlled a^power mod 15 to qc, with control qubit `ctrl`
    and 4-qubit work register `work`. Uses cswap + cx directly.
    """
    if a not in (2, 4, 7, 8, 11, 13):
        raise ValueError(f"a={a} must be in {{2,4,7,8,11,13}}")
    ord_a = _order_of_a_mod15(a)
    effective = power % ord_a
    for _ in range(effective):
        if a in (2, 13):
            qc.cswap(ctrl, work[2], work[3])
            qc.cswap(ctrl, work[1], work[2])
            qc.cswap(ctrl, work[0], work[1])
        if a in (7, 8):
            qc.cswap(ctrl, work[0], work[1])
            qc.cswap(ctrl, work[1], work[2])
            qc.cswap(ctrl, work[2], work[3])
        if a in (4, 11):
            qc.cswap(ctrl, work[1], work[3])
            qc.cswap(ctrl, work[0], work[2])
        if a in (7, 11, 13):
            for q in work:
                qc.cx(ctrl, q)


def build_shor_circuit(N: int, a: int, n_count: int) -> QuantumCircuit:
    assert N == 15
    n_work = 4
    qc = QuantumCircuit(n_count + n_work, n_count)
    for q in range(n_count):
        qc.h(q)
    # Initialize |1> in the work register: LSB of work = qubit n_count
    qc.x(n_count)
    work = list(range(n_count, n_count + n_work))
    for j in range(n_count):
        add_controlled_amod15(qc, ctrl=j, work=work, a=a, power=2 ** j)
    # Inverse QFT on counting register
    qft_inv = QFT(num_qubits=n_count, do_swaps=True, inverse=True).to_gate()
    qft_inv.name = "IQFT"
    qc.append(qft_inv, list(range(n_count)))
    qc.measure(range(n_count), range(n_count))
    return qc


def extract_order(measured_int: int, n_count: int, N: int) -> int | None:
    if measured_int == 0:
        return None
    phase = measured_int / (2 ** n_count)
    frac = Fraction(phase).limit_denominator(N)
    r = frac.denominator
    if r == 0 or r > N:
        return None
    return r


def try_factor(N: int, a: int, r: int) -> tuple[int, int] | None:
    if r % 2 != 0:
        return None
    x = pow(a, r // 2, N)
    if x == N - 1 or x == 1:
        return None
    f1 = gcd(x - 1, N)
    f2 = gcd(x + 1, N)
    if 1 < f1 < N and 1 < f2 < N and f1 * f2 == N:
        return (f1, f2)
    for f in (f1, f2):
        if 1 < f < N:
            return (f, N // f)
    return None


def run(N: int = 15, a: int = 7, n_count: int = 5, shots: int = 1024,
        noise_p: float = 0.0):
    qc = build_shor_circuit(N, a, n_count)
    n_work = 4
    total_qubits = n_count + n_work
    sim = AerSimulator()
    if noise_p > 0:
        nm = NoiseModel()
        err1 = depolarizing_error(noise_p, 1)
        err2 = depolarizing_error(noise_p, 2)
        err3 = depolarizing_error(noise_p, 3)
        nm.add_all_qubit_quantum_error(err1, ['h', 'x'])
        nm.add_all_qubit_quantum_error(err2, ['cx', 'swap'])
        nm.add_all_qubit_quantum_error(err3, ['cswap'])
        sim = AerSimulator(noise_model=nm)

    t_transpile_start = time.time()
    tqc = transpile(qc, sim, optimization_level=1)
    t_transpile = time.time() - t_transpile_start
    depth = tqc.depth()
    n_gates = sum(tqc.count_ops().values())

    t0 = time.time()
    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()
    elapsed = time.time() - t0

    success_shots = 0
    factor_pairs = {}
    order_counts = {}
    for bitstr, c in counts.items():
        # bitstr is measurement result; classical bit 0 (LSB counting qubit) is
        # on the RIGHT in Qiskit's default string, so int(bitstr, 2) is the
        # integer with c_{n-1} as MSB. Verified via docs.
        measured_int = int(bitstr, 2)
        r = extract_order(measured_int, n_count, N)
        if r is None:
            continue
        order_counts[r] = order_counts.get(r, 0) + c
        fac = try_factor(N, a, r)
        if fac is not None:
            success_shots += c
            key = tuple(sorted(fac))
            factor_pairs[str(key)] = factor_pairs.get(str(key), 0) + c

    return {
        "N": N,
        "a": a,
        "n_count": n_count,
        "n_work": n_work,
        "total_qubits": total_qubits,
        "textbook_shor_qubits_2n_plus_3": 2 * 4 + 3,
        "circuit_depth_transpiled": depth,
        "n_gates_transpiled": n_gates,
        "transpile_sec": round(t_transpile, 3),
        "shots": shots,
        "noise_p": noise_p,
        "sim_sec": round(elapsed, 3),
        "success_shots": success_shots,
        "success_prob": success_shots / shots,
        "top_counts": dict(sorted(counts.items(), key=lambda kv: -kv[1])[:10]),
        "order_counts": order_counts,
        "factor_pairs": factor_pairs,
    }


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_results = []
    print("=" * 72)
    print("Shor factoring pipeline for N=15 (Qiskit Aer)")
    print("Baseline against Ragavan-Vaikuntanathan arXiv:2310.00899")
    print("=" * 72)

    for a in [2, 4, 7, 8, 11, 13]:
        r_true = _order_of_a_mod15(a)
        res = run(N=15, a=a, n_count=5, shots=2048, noise_p=0.0)
        res["true_order"] = r_true
        print(f"  a={a:2d}  true_order={r_true}  gates={res['n_gates_transpiled']}"
              f"  depth={res['circuit_depth_transpiled']}"
              f"  success_prob={res['success_prob']:.3f}"
              f"  sim={res['sim_sec']}s  factors={res['factor_pairs']}")
        all_results.append(res)

    print("\nNoise-robustness sweep for a=7 (order 4):")
    noise_sweep = []
    for p in [0.0, 0.001, 0.005, 0.01, 0.02, 0.05]:
        r = run(N=15, a=7, n_count=5, shots=1024, noise_p=p)
        noise_sweep.append({
            "noise_p": p,
            "success_prob": r["success_prob"],
            "n_gates_transpiled": r["n_gates_transpiled"],
        })
        print(f"  p={p:.3f}  success_prob={r['success_prob']:.3f}")

    out = {
        "paper": "arXiv:2310.00899 - Ragavan & Vaikuntanathan",
        "paper_headline_qubit_formula": "(10.32 + o(1))*n asymptotic (Table 1)",
        "textbook_shor_qubits_2n_plus_3_for_n4": 11,
        "this_replication_total_qubits_n_count_5": 9,
        "N": 15,
        "n_count_used": 5,
        "n_work": 4,
        "per_base_results": all_results,
        "noise_sweep_a7": noise_sweep,
    }
    (out_dir / "shor_n15_results.json").write_text(json.dumps(out, indent=2, default=str))
    print(f"\nWrote {out_dir / 'shor_n15_results.json'}")
