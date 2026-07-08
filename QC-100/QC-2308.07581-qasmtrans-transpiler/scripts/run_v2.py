#!/usr/bin/env python3
"""V2: Use the real QASMBench adder_n10, linear coupling for GHZ, and IBM Toronto
27-qubit heavy-hex when qubits<=27 per paper Section IV-B. Reproduce closer to
paper Table IV Qiskit column."""
import json, time
from pathlib import Path
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit.transpiler import CouplingMap

BASIS = ["x", "sx", "cx", "rz"]

def toronto_cmap():
    """IBMQ Toronto: 27-qubit heavy-hex. Uses paper's stated topology.
    Qiskit ships from_heavy_hex(distance=3) which yields 19 qubits; distance=5 -> 65.
    Toronto's actual coupling map (public) is a specific 27-qubit heavy-hex.
    We hand-craft it from the published IBMQ Toronto layout.
    """
    # IBM Quantum Toronto edges (public info, symmetric).
    edges = [(0,1),(1,2),(1,4),(2,3),(3,5),(4,7),(5,8),(6,7),(7,10),
             (8,9),(8,11),(10,12),(11,14),(12,13),(12,15),(13,14),(14,16),
             (15,18),(16,19),(17,18),(18,21),(19,20),(19,22),(21,23),
             (22,25),(23,24),(24,25),(25,26)]
    edges += [(b,a) for (a,b) in edges]
    return CouplingMap(couplinglist=edges)

def linear_cmap(n):
    edges = [(i, i+1) for i in range(n-1)] + [(i+1, i) for i in range(n-1)]
    return CouplingMap(couplinglist=edges)

def ghz_circuit(n):
    qc = QuantumCircuit(n); qc.h(0)
    for i in range(n-1): qc.cx(i, i+1)
    return qc

def bv_circuit(n_data):
    n = n_data + 1
    qc = QuantumCircuit(n); qc.x(n-1); qc.h(range(n))
    for i in range(n_data):
        if i % 2: qc.cx(i, n-1)
    qc.h(range(n_data))
    return qc

def qft_circuit(n):
    qc = QuantumCircuit(n); qc.compose(QFT(n, do_swaps=False), inplace=True)
    return qc

def ising_1d(n):
    qc = QuantumCircuit(n)
    for i in range(n): qc.rx(0.5, i)
    for i in range(n-1):
        qc.cx(i, i+1); qc.rz(0.25, i+1); qc.cx(i, i+1)
    return qc

def count_gates(qc):
    ops = qc.count_ops()
    two_q = sum(v for k,v in ops.items() if k in ("cx","cz","swap","iswap","ecr","cy","ch"))
    total = sum(ops.values())
    return {"total_gates": int(total), "depth": int(qc.depth()), "2q_gates": int(two_q),
            "ops": {k:int(v) for k,v in ops.items()}}

def run(name, qc, cm, opt_level=1, seed=42, target_2q_col="both"):
    t0 = time.time()
    tqc = transpile(qc, basis_gates=BASIS, coupling_map=cm,
                    optimization_level=opt_level, seed_transpiler=seed)
    dt_ms = int(1000*(time.time()-t0))
    m = count_gates(tqc)
    m.update({"transpile_ms": dt_ms, "input_qubits": qc.num_qubits,
              "cmap_qubits": cm.size(), "opt_level": opt_level})
    return m

# Paper Table IV Qiskit column (published values)
PAPER = {
    "adder_n10":   {"2q_gates":146, "total_gates":278, "depth":243, "transpile_ms":396},
    "ghz_n140":    {"2q_gates":797, "total_gates":802, "depth":802, "transpile_ms":7900},
    "bv_n140":     {"2q_gates":444, "total_gates":1281,"depth":307, "transpile_ms":8900},
    "ising_n420":  {"2q_gates":1382,"total_gates":5062,"depth":36,  "transpile_ms":1910},
    "qft_n255":    {"2q_gates":None,"total_gates":None,"depth":None,"transpile_ms":None,
                    "note":"Qiskit did not finish within 1h (X)"},
}

def main():
    out = Path(__file__).resolve().parent.parent / "report" / "evidence"
    out.mkdir(parents=True, exist_ok=True)
    qasmbench = Path(__file__).resolve().parent.parent / "work" / "adder_n10.qasm"

    results = {"table_iv_replication": {}, "opt_level_sweep": {}, "meta": {}}

    # --- Table IV replication ---
    # adder_n10: 10 qubits -> IBM Toronto (27q heavy-hex) per paper rule "qubits<27".
    qc = QuantumCircuit.from_qasm_file(str(qasmbench))
    r = run("adder_n10", qc, toronto_cmap(), opt_level=1)
    results["table_iv_replication"]["adder_n10"] = {
        "measured": r, "paper_qiskit": PAPER["adder_n10"],
        "topology":"IBMQ Toronto (27q heavy-hex)",
        "source":"QASMBench adder_n10.qasm (Cuccaro et al ripple)"}

    # ghz_n140: >27 -> IBM Seattle (433q) in paper; we use linear coupling to
    # trigger paper's SWAP-heavy pattern (heavy-hex would give too many free paths).
    # Then also try a heavy-hex-like larger map as sensitivity.
    for topo_name, cm_fn in [("linear_140", lambda: linear_cmap(140)),
                              ("heavy_hex_193", lambda: CouplingMap.from_heavy_hex(9, bidirectional=True))]:
        qc = ghz_circuit(140)
        r = run(f"ghz_n140::{topo_name}", qc, cm_fn(), opt_level=1)
        results["table_iv_replication"][f"ghz_n140::{topo_name}"] = {
            "measured": r, "paper_qiskit": PAPER["ghz_n140"],
            "topology": topo_name}

    # bv_n140
    for topo_name, cm_fn in [("linear_140", lambda: linear_cmap(140)),
                              ("heavy_hex_193", lambda: CouplingMap.from_heavy_hex(9, bidirectional=True))]:
        qc = bv_circuit(139)  # 139 data + 1 ancilla
        r = run(f"bv_n140::{topo_name}", qc, cm_fn(), opt_level=1)
        results["table_iv_replication"][f"bv_n140::{topo_name}"] = {
            "measured": r, "paper_qiskit": PAPER["bv_n140"], "topology": topo_name}

    # ising_n420
    qc = ising_1d(420)
    r = run("ising_n420", qc, linear_cmap(420), opt_level=1)
    results["table_iv_replication"]["ising_n420"] = {
        "measured": r, "paper_qiskit": PAPER["ising_n420"],
        "topology":"linear_420"}

    # --- Opt-level sweep (the KEY reproducible trend) ---
    sweeps = {
        "adder_n10 (QASMBench, IBM Toronto)": (QuantumCircuit.from_qasm_file(str(qasmbench)), toronto_cmap()),
        "ghz_n64 (linear)": (ghz_circuit(64), linear_cmap(64)),
        "qft_n16 (linear)": (qft_circuit(16), linear_cmap(16)),
        "bv_n10  (IBM Toronto)": (bv_circuit(9), toronto_cmap()),
    }
    for name, (qc, cm) in sweeps.items():
        results["opt_level_sweep"][name] = {}
        for lvl in (0,1,2,3):
            r = run(name, qc, cm, opt_level=lvl)
            results["opt_level_sweep"][name][f"opt_{lvl}"] = r

    # meta
    import qiskit
    results["meta"] = {"qiskit_version": qiskit.__version__,
                       "basis_gates": BASIS,
                       "seed_transpiler": 42}

    (out / "results_v2.json").write_text(json.dumps(results, indent=2))
    print("[OK] wrote", out / "results_v2.json")

if __name__ == "__main__":
    main()
