"""Extended C3 experiment: push 2D cluster states larger to look for the
exponential DD-size blowup predicted in Lemma / Theorem 2 of arXiv:2108.00931
(App. B). The paper's lower bound is 2^{floor(n/12)} for the n x n grid state,
so we should start to see clear growth only for n >= ~12 (144 qubits total).

We test 2D grids of increasing size and record DD node counts plus wall time.
We stop early if a single sim runs longer than TIMEOUT_S seconds.
"""

from __future__ import annotations
import json, time, sys, signal
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from experiment import (
    grid_cluster_state_circuit,
    ddsim_statevector,
    EVID,
)

TIMEOUT_S = 60.0

def run():
    rows = []
    # Snake through: square + near-square shapes
    shapes = [(4, 4), (4, 5), (5, 5), (5, 6), (6, 6), (6, 7), (7, 7), (7, 8), (8, 8)]
    for r, c in shapes:
        n = r * c
        print(f"  2D cluster {r}x{c}  n={n} ... ", flush=True, end="")
        t0 = time.perf_counter()
        try:
            _, dd_nodes, dd_t = ddsim_statevector(grid_cluster_state_circuit(r, c))
            elapsed = time.perf_counter() - t0
            print(f"DD_nodes={dd_nodes}   elapsed={elapsed:.2f}s")
            rows.append({
                "rows": r, "cols": c, "n_qubits": n,
                "dd_active_vector_nodes": dd_nodes,
                "ddsim_time_s": dd_t,
                "wall_time_s": elapsed,
                "dense_statevector_amplitudes": 2 ** n,
            })
            (EVID / "C3_stabilizer_dd_size_extended.json").write_text(
                json.dumps(rows, indent=2, default=str)
            )
            if elapsed > TIMEOUT_S:
                print("  (exceeded soft budget, stopping)")
                break
        except Exception as e:
            print(f"FAILED: {e}")
            rows.append({
                "rows": r, "cols": c, "n_qubits": n,
                "error": str(e),
            })
            (EVID / "C3_stabilizer_dd_size_extended.json").write_text(
                json.dumps(rows, indent=2, default=str)
            )
            break
    print(json.dumps(rows[-1] if rows else {}, indent=2))

if __name__ == "__main__":
    run()
