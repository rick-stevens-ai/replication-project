"""
Extension of simulate.py: scan evolution time t to see the crossover regime
between low-order Trotter, high-order Trotter, and qDRIFT.

Central Childs-et-al./Campbell claim: at LARGE evolution time (many Trotter
steps needed), the SCALING of error per gate favors random-compilation
(qDRIFT) over deterministic low-order Trotter because qDRIFT eliminates the
worst-case commutator scaling.
"""
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from simulate import build_tfim, trotter1, trotter2, qdrift, op_norm

def scan():
    n = 3
    times = [0.5, 1.0, 2.0, 4.0, 8.0]
    all_results = []
    for t in times:
        terms, H = build_tfim(n)
        U_exact = expm(-1j * H * t)
        # Fixed BUDGET of 200 two-qubit-scale exponentials
        # Trotter1 with 5 terms: r_t1 = 200/5 = 40 steps
        # Trotter2 with 5 terms: r_t2 = 200/(2*5) = 20 steps
        # qDRIFT: N = 200
        U1, ne1 = trotter1(terms, t, 40)
        U2, ne2 = trotter2(terms, t, 20)
        Uq, neq = qdrift(terms, t, 200)
        e1 = op_norm(U1 - U_exact)
        e2 = op_norm(U2 - U_exact)
        eq = op_norm(Uq - U_exact)
        # Also higher budget
        U1b, _ = trotter1(terms, t, 200)
        U2b, _ = trotter2(terms, t, 100)
        Uqb, _ = qdrift(terms, t, 1000)
        e1b = op_norm(U1b - U_exact)
        e2b = op_norm(U2b - U_exact)
        eqb = op_norm(Uqb - U_exact)
        rec = {
            "t": t,
            "budget_200": {"Trotter1": float(e1), "Trotter2": float(e2), "qDRIFT": float(eq)},
            "budget_1000": {"Trotter1": float(e1b), "Trotter2": float(e2b), "qDRIFT": float(eqb)},
        }
        all_results.append(rec)
        print(f"t={t}: budget=200 -> T1={e1:.3e}, T2={e2:.3e}, qD={eq:.3e}")
        print(f"      budget=1000 -> T1={e1b:.3e}, T2={e2b:.3e}, qD={eqb:.3e}")

    outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    (outdir / "time_scan.json").write_text(json.dumps(all_results, indent=2))

    # Assess Trotter1 vs qDRIFT crossover  (the paper's near-term claim)
    print("\nqDRIFT-vs-Trotter1 comparison (near-term-friendly claim proxy):")
    for r in all_results:
        for bkey in ["budget_200", "budget_1000"]:
            t1 = r[bkey]["Trotter1"]
            qd = r[bkey]["qDRIFT"]
            winner = "qDRIFT" if qd < t1 else "Trotter1"
            ratio = t1 / qd if qd > 0 else float("inf")
            print(f"  t={r['t']}, {bkey}: T1/qD={ratio:.3f}, winner={winner}")

if __name__ == "__main__":
    scan()
