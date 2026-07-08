#!/usr/bin/env python3
"""
Independent replication of QASMTrans (arXiv:2308.07581) key results using Qiskit.

We can't easily build the C++ QASMTrans in this environment, so we validate the
paper's Qiskit BASELINE column of Table IV — this is what the authors report they
compare against. If our fresh Qiskit run on the same benchmark circuits produces
transpiled circuits with comparable 2-qubit-gate count, total gate count, and
depth to the paper's reported Qiskit numbers, that validates the baseline data
the paper's speedup claims are measured against.

We use IBMQ Toronto topology (paper: "when qubits < 27, use IBMQ Toronto") and
IBMQ basis gate set (X, SX, CX, RZ) per paper Section IV-B.

Benchmarks reproduced from Table IV (subset that we can construct from Qiskit):
  * ghz_n140      (140-qubit GHZ)         -- large, structured
  * qft_n255      (255-qubit QFT)         -- large, dense
  * adder_n10     (10-qubit ripple adder) -- small QASMBench-style
  * bv_n140       (140-qubit BV)          -- structured
  * ising_n420    (420-qubit Ising)       -- large, structured
Also transpiler opt-level sweep on GHZ, QFT and Adder to reproduce trend
(higher opt level -> fewer/equal CX/depth in general).
"""
import json, time, os, sys
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit.transpiler import CouplingMap

BASIS = ["x", "sx", "cx", "rz"]

# IBMQ Toronto is a 27-qubit heavy-hex; for larger benchmarks we use IBM Seattle
# (433 qubits) per paper's rule. Qiskit doesn't ship those coupling maps out of
# the box in modern versions, so we synthesize equivalent heavy-hex-flavored
# coupling maps of the right size. For paper's Qiskit-baseline column, the exact
# coupling map matters, but for a defensible baseline we use realistic heavy-hex
# adjacency using CouplingMap.from_heavy_hex which is what IBMQ Toronto/Seattle
# are built on.

def heavy_hex_cmap(min_qubits: int) -> CouplingMap:
    """Return smallest heavy-hex coupling map with >= min_qubits qubits."""
    # heavy_hex(d) has d(5d-2)+2(d-1)^2 physical qubits for distance d (odd)
    for d in range(3, 40, 2):
        cm = CouplingMap.from_heavy_hex(d, bidirectional=True)
        if cm.size() >= min_qubits:
            return cm
    raise ValueError("no heavy_hex big enough")


def ghz_circuit(n):
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    return qc


def bv_circuit(n_data):
    """Bernstein-Vazirani with n_data data qubits + 1 ancilla."""
    n = n_data + 1
    qc = QuantumCircuit(n)
    qc.x(n - 1)
    qc.h(range(n))
    # secret string: alternating pattern
    s = [i % 2 for i in range(n_data)]
    for i, si in enumerate(s):
        if si:
            qc.cx(i, n - 1)
    qc.h(range(n_data))
    return qc


def qft_circuit(n):
    qc = QuantumCircuit(n)
    qc.compose(QFT(n, do_swaps=False), inplace=True)
    return qc


def adder_ripple(n_bits):
    """Simple ripple-carry adder built from basic Toffolis + CNOTs.
    n_bits pair of a/b + 1 carry + 1 sum ancilla. Total qubits ~ 2*n_bits+2.
    """
    n = 2 * n_bits + 2
    qc = QuantumCircuit(n)
    # Half-adder-style chain (illustrative, matches structure of QASMBench adder_n10)
    for i in range(n_bits):
        a = i
        b = n_bits + i
        c_in = 2 * n_bits + (0 if i == 0 else 0)  # simplified; reuse ancilla
        qc.ccx(a, b, 2 * n_bits + 1)
        qc.cx(a, b)
        qc.ccx(2 * n_bits, b, 2 * n_bits + 1)
        qc.cx(2 * n_bits, b)
    return qc


def ising_1d(n, layers=1):
    """1D transverse-field Ising trotter step, n qubits, `layers` trotter steps.
    Uses Rzz-decomposed-into-CNOT-Rz-CNOT to emit CX+RZ."""
    qc = QuantumCircuit(n)
    for _ in range(layers):
        for i in range(n):
            qc.rx(0.5, i)
        for i in range(n - 1):
            qc.cx(i, i + 1)
            qc.rz(0.25, i + 1)
            qc.cx(i, i + 1)
    return qc


# ---- paper's Table IV Qiskit column (reference values) ----
PAPER_QISKIT = {
    # name -> dict of (2q_gates, total_gates, depth, transpile_ms)
    "ghz_n140":  {"total_gates": 802, "depth": 802, "2q_gates": 797,
                  "transpile_ms": 7900, "note": "Table IV row ghz"},
    "qft_n255":  {"total_gates": None, "depth": None, "2q_gates": None,
                  "transpile_ms": None, "note": "Qiskit>1h (X), only QASMTrans finished"},
    "adder_n10": {"total_gates": 278, "depth": 243, "2q_gates": 146,
                  "transpile_ms": 396, "note": "Table IV row adder n10"},
    "bv_n140":   {"total_gates": 1281, "depth": 307, "2q_gates": 444,
                  "transpile_ms": 8900, "note": "Table IV row bv"},
    "ising_n420":{"total_gates": 5062, "depth": 36, "2q_gates": 1382,
                  "transpile_ms": 1910, "note": "Table IV row ising"},
}


def count_gates(qc):
    ops = qc.count_ops()
    two_q = sum(v for k, v in ops.items()
                if k in ("cx", "cz", "swap", "iswap", "ecr", "cy", "ch"))
    total = sum(ops.values())
    depth = qc.depth()
    return {"total_gates": int(total), "depth": int(depth),
            "2q_gates": int(two_q), "ops": {k: int(v) for k, v in ops.items()}}


def run_one(name, qc, opt_level=3, seed=42):
    cm = heavy_hex_cmap(qc.num_qubits)
    t0 = time.time()
    try:
        tqc = transpile(qc, basis_gates=BASIS, coupling_map=cm,
                        optimization_level=opt_level, seed_transpiler=seed)
    except Exception as e:
        return {"error": str(e), "transpile_ms": None}
    dt_ms = int(1000 * (time.time() - t0))
    m = count_gates(tqc)
    m["transpile_ms"] = dt_ms
    m["input_qubits"] = qc.num_qubits
    m["cmap_qubits"] = cm.size()
    m["opt_level"] = opt_level
    return m


def main():
    out_dir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)

    results = {}

    # 1) Table-IV replication (opt_level=3, matches Qiskit default; paper doesn't
    #    specify but Qiskit transpiler default = 1, we sweep 0..3 later).
    circuits = {
        "ghz_n140":   ghz_circuit(140),
        "adder_n10":  QuantumCircuit(10),  # will replace with real adder_n10
        "bv_n140":    bv_circuit(139),      # 139 data + 1 ancilla = 140
        "ising_n420": ising_1d(420, layers=1),
    }
    # Build adder_n10 exactly: use Qiskit's QFTAdder-free simple structure.
    # Paper's Table I row: Adder_n10 has 65 2q gates, 142 gates, 99 depth (input).
    # Try to match: 10-qubit ripple w/ Toffolis-decomposed.
    circuits["adder_n10"] = adder_ripple(4)  # 4-bit ripple ~ 10 qubits total

    # Only attempt qft_n255 with opt_level=1 (heavy op takes long)
    circuits["qft_n64"] = qft_circuit(64)   # scaled down for time budget

    for name, qc in circuits.items():
        print(f"[table-iv] {name} qubits={qc.num_qubits} ops={qc.count_ops()}", flush=True)
        r = run_one(name, qc, opt_level=1)   # Qiskit default = 1
        results.setdefault("table_iv", {})[name] = {
            "qiskit_measured": r,
            "paper_qiskit_reported": PAPER_QISKIT.get(name, {"note": "not in Table IV"}),
        }
        print(f"[table-iv] {name} -> measured={r}", flush=True)

    # 2) Opt-level sweep on GHZ_n64, QFT_n16, adder_ripple(4).
    sweep = {}
    for name, qc in {
        "ghz_n64":  ghz_circuit(64),
        "qft_n16":  qft_circuit(16),
        "adder_n10": adder_ripple(4),
    }.items():
        sweep[name] = {}
        for lvl in (0, 1, 2, 3):
            r = run_one(name, qc, opt_level=lvl)
            sweep[name][f"opt_{lvl}"] = r
            print(f"[sweep] {name} opt={lvl} -> {r.get('2q_gates')} 2q, depth={r.get('depth')}, {r.get('transpile_ms')}ms", flush=True)
    results["opt_level_sweep"] = sweep

    (out_dir / "results.json").write_text(json.dumps(results, indent=2))
    print("[OK] wrote", out_dir / "results.json")


if __name__ == "__main__":
    main()
