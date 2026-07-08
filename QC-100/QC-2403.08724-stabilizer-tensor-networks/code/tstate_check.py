"""
Direct check of the paper's central worked example (Eq. 11):

    |T>^{tensor n} = prod_i T_i . prod_i H_i . |0>^{tensor n}

Paper claims (arXiv:2403.08724 p.3):
  - In the STABILIZER TN formalism (their contribution), this state is represented
    with a trivial MPS (chi = 1) after the Hadamard layer sets the tableau to
    s_i = X_i, d_i = Z_i, and then each T_i is a "free operation" on the tableau.
  - In the CONVENTIONAL generalization of stabilizer tableaus (the baseline),
    the pseudo-stabilizer rank is xi_tilde = 2^n, i.e. one would need 2^n
    stabilizer terms to represent it.

We verify the second (baseline) claim explicitly: run our stabilizer-decomposition
simulator on this exact circuit for n in {1..6} and confirm the number of
stabilizer branches at the end is exactly 2^n = 2^(number of T-gates).

We also verify the final state matches the statevector reference and matches
the analytic |T> = cos(pi/8)|0> + e^{i pi/4} sin(pi/8) |1> per qubit.
"""

from __future__ import annotations

import cmath
import json
import math
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stabilizer_decomp_sim import statevector_run, stab_decomp_run, fidelity


def tstate_analytic(n: int) -> np.ndarray:
    """|T>^{tensor n} where |T> = T H |0> = (1/sqrt(2))(|0> + e^{i pi/4}|1>)."""
    t1 = np.array([1.0, cmath.exp(1j * math.pi / 4)], dtype=complex) / math.sqrt(2)
    psi = t1.copy()
    for _ in range(n - 1):
        psi = np.kron(psi, t1)
    return psi


def build_tstate_circuit(n: int) -> list[tuple]:
    circ: list[tuple] = []
    for i in range(n):
        circ.append(("H", i))
    for i in range(n):
        circ.append(("T", i))
    return circ


def main():
    out_path = os.path.join(os.path.dirname(__file__), "..", "report", "evidence",
                            "tstate_check.json")
    out_path = os.path.abspath(out_path)

    rows = []
    for n in range(1, 7):
        circ = build_tstate_circuit(n)
        psi_sv = statevector_run(circ, n)
        psi_analytic = tstate_analytic(n)
        fid_sv_analytic = fidelity(psi_sv, psi_analytic)

        psi_sd, nterms, core_t, term_counts, rec_t = stab_decomp_run(circ, n)
        fid_sv_sd = fidelity(psi_sv, psi_sd)
        expected_terms = 2 ** n
        matches_2n = (nterms == expected_terms)

        row = dict(
            n=n,
            num_t_gates=n,
            circuit_len=len(circ),
            final_num_stabilizer_terms=nterms,
            expected_2_to_the_n=expected_terms,
            num_terms_equals_2_to_the_n=matches_2n,
            fidelity_sv_vs_analytic=fid_sv_analytic,
            fidelity_sv_vs_stabdecomp=fid_sv_sd,
            core_time_s=core_t,
            reconstruct_time_s=rec_t,
            term_counts_after_each_T=term_counts,
        )
        rows.append(row)
        print(f"n={n}  #Tgates={n}  final_terms={nterms} (expected 2^n={expected_terms}) match={matches_2n}  "
              f"fid(SV,ana)={fid_sv_analytic:.9f}  fid(SV,SD)={fid_sv_sd:.9f}  "
              f"core={core_t*1e3:.2f}ms")

    all_ok = all(r["num_terms_equals_2_to_the_n"] and
                 r["fidelity_sv_vs_analytic"] > 1 - 1e-6 and
                 r["fidelity_sv_vs_stabdecomp"] > 1 - 1e-6
                 for r in rows)
    print(f"\nAll rows match paper baseline claim (final_terms == 2^n) AND fidelity == 1: {all_ok}")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(dict(rows=rows, all_ok=all_ok), f, indent=2)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
