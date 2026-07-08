#!/usr/bin/env python3
"""
Extra scaling probe: for small N in {9, 15, 21}, DECOMPOSE the oracle-heavy Shor
circuit down to the cx+u basis via Qiskit transpile, and record the resulting
depth and 2-qubit-gate count. This is what the paper's polynomial-scaling claim
actually refers to (native 2-qubit-gate counts, not logical oracle stages).

We fit y = c * (log2 N)^k to the decomposed depth and cx count and compare
the exponent k to the theoretical O((log N)^3) = k=3.
"""
import csv, json, math, time
from pathlib import Path
import numpy as np
from qiskit import transpile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from shor_sim import iterative_shor_circuit, fit_powerlaw

def main():
    out_dir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Choose bases that are coprime to N.
    targets = [(9, 2), (15, 7), (21, 2)]  # keep small — decomposition is expensive
    rows = []
    for N, a in targets:
        t0 = time.time()
        qc, L, t = iterative_shor_circuit(N, a)
        qc_t = transpile(qc, basis_gates=["cx", "u"], optimization_level=1,
                         seed_transpiler=1)
        ops = dict(qc_t.count_ops())
        wall = time.time() - t0
        rows.append({
            "N": N, "a": a, "L": L, "t": t,
            "log2N": math.log2(N),
            "n_qubits": L + 1 + t,   # counting + work
            "decomposed_depth": qc_t.depth(),
            "decomposed_cx_count": ops.get("cx", 0),
            "decomposed_u_count": ops.get("u", 0),
            "decomposed_gate_count": sum(ops.values()),
            "transpile_seconds": wall,
        })
        print(f"[decomp] N={N} L={L} t={t} depth={qc_t.depth()} "
              f"cx={ops.get('cx',0)} u={ops.get('u',0)} wall={wall:.1f}s",
              flush=True)

    # Fit power-law y = c * (log2 N)^k on the 3 points we have.
    logN = [r["log2N"] for r in rows]
    depth = [r["decomposed_depth"] for r in rows]
    cx = [r["decomposed_cx_count"] for r in rows]
    gates = [r["decomposed_gate_count"] for r in rows]

    k_d, c_d, r2_d = fit_powerlaw(logN, depth)
    k_c, c_c, r2_c = fit_powerlaw(logN, cx)
    k_g, c_g, r2_g = fit_powerlaw(logN, gates)

    results = {
        "rows": rows,
        "fits": {
            "model": "y = c * (log2 N)^k, fit in log-log space with LSQ",
            "decomposed_depth":     {"k": k_d, "c": c_d, "R2": r2_d},
            "decomposed_cx_count":  {"k": k_c, "c": c_c, "R2": r2_c},
            "decomposed_gate_count":{"k": k_g, "c": c_g, "R2": r2_g},
            "note_theoretical_target_for_shor": "O((log N)^3) two-qubit gates.",
        },
        "extrapolation_to_paper_Nmax": {
            "Nmax": 549_755_813_701,
            "log2_Nmax": math.log2(549_755_813_701),
            "predicted_cx_at_Nmax": c_c * (math.log2(549_755_813_701) ** k_c),
        },
    }

    with open(out_dir / "scaling_decomposed.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    with open(out_dir / "scaling_decomposed.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("[write]", out_dir / "scaling_decomposed.json")
    print("[write]", out_dir / "scaling_decomposed.csv")
    print()
    print("KEY FIT (decomposed cx count vs log2 N):")
    print(f"  k = {k_c:.3f}, c = {c_c:.3g}, R^2 = {r2_c:.3f}")
    print(f"  Theoretical Shor target: k=3 (O((log N)^3))")

if __name__ == "__main__":
    main()
