"""
Dynamical benchmark on 1D Heisenberg chain (mirrors Fig. 2 setup of the paper,
just at smaller N since we're classically diagonalizing 2^N x 2^N matrices).

For each (method, order 2m) pair, evolve for time t using r steps of size
delta = t/r, and record the operator-norm error ||U_approx - exp(-iHt)||_2
as a function of r. In log-log:
  slope = -(2m)  ideally, since global error = O(r * delta^{2m+1}) = O(t^{2m+1}/r^{2m}).
"""

import numpy as np
import scipy.linalg as sla
import json
import time
from pathlib import Path
import sys

from mpf import (
    heisenberg_A_B,
    U2_step,
    U2_k_step,
    U4_step,
    mpf_step,
    chin_coefficients,
    chebyshev_real_coefficients,
    chebyshev_first_half_coefficients,
    rounded_integer_coefficients,
    paper_table_coeffs,
    condition_number,
    k_norm,
)


def op_norm(M):
    return float(sla.norm(M, 2))


def evolve_and_error(A, B, t, r, method):
    """Compose r single-steps of `method(A,B,delta)`, return op-norm error vs exact."""
    dim = A.shape[0]
    H = A + B
    U_exact = sla.expm(-1j * H * t)
    delta = t / r
    step = method(A, B, delta)
    # Repeat r times (composition). r is small (5..200) so straightforward.
    U = np.eye(dim, dtype=complex)
    # For efficiency use matrix_power (all identical steps)
    U = np.linalg.matrix_power(step, r)
    return op_norm(U - U_exact)


def method_factory(name, m):
    """Return a function(A,B,delta) -> single-step approx operator."""
    if name == "U2":
        return lambda A, B, d: U2_step(A, B, d)
    if name == "U4":
        return lambda A, B, d: U4_step(A, B, d)
    if name.startswith("chin"):
        k, a = chin_coefficients(m)
        return lambda A, B, d, k=k, a=a: mpf_step(A, B, d, k, a, base="U2")
    if name.startswith("cheb_real"):
        k, a = chebyshev_real_coefficients(m)
        # k is not integer; use fractional powers -> we approximate by using the
        # base-U2 formula k-times structurally would require fractional stepping.
        # For classical simulation we can still use exp(-i H delta/k) via matrix
        # exponential and raise to the k-th power via product formula k times
        # (integer only). We fall back to a symmetric "matrix" form: U2(delta/k)^k
        # is well-defined only for integer k. We simulate by rounding k to nearest
        # int and rebuilding a via Eq.(5) -> this is essentially the "rounded_int"
        # method already tested. So skip this in the dynamical test to avoid
        # confusing the reader.
        return None
    if name.startswith("cheb_first_half"):
        # Same fractional-exponent problem: skip in dynamical benchmark.
        return None
    if name.startswith("rounded_int"):
        k, a = rounded_integer_coefficients(m)
        return lambda A, B, d, k=k, a=a: mpf_step(A, B, d, k, a, base="U2")
    if name.startswith("paper_table"):
        pt = paper_table_coeffs(m)
        if pt is None:
            return None
        k, a = pt
        return lambda A, B, d, k=k, a=a: mpf_step(A, B, d, k, a, base="U2")
    raise ValueError(name)


def main():
    N = 4  # 4 spins -> 16x16 matrices, fast
    t = 1.0
    A, B = heisenberg_A_B(N)
    print(f"N={N}, dim={2**N}, t={t}")
    print(f"||H||_2 = {op_norm(A+B):.4f}")

    r_values = [1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 120, 200]
    results = {"N": N, "t": t, "r_values": r_values, "methods": {}}

    # Standard formulas
    for name, m in [("U2", 1), ("U4", 2)]:
        fn = method_factory(name, m)
        errs = []
        for r in r_values:
            err = evolve_and_error(A, B, t, r, fn)
            errs.append(err)
        print(f"{name} order={2*m}: min_err={min(errs):.3e} at r={r_values[errs.index(min(errs))]}")
        results["methods"][name] = {"order_2m": 2 * m, "errors": errs}

    # MPF families
    for family in ["chin", "rounded_int", "paper_table"]:
        for m in range(2, 7):
            fn = method_factory(family, m)
            if fn is None:
                continue
            k, a = None, None
            if family == "chin":
                k, a = chin_coefficients(m)
            elif family == "rounded_int":
                k, a = rounded_integer_coefficients(m)
            elif family == "paper_table":
                pt = paper_table_coeffs(m)
                if pt is None:
                    continue
                k, a = pt
            key = f"{family}_m{m}"
            errs = []
            t0 = time.time()
            for r in r_values:
                err = evolve_and_error(A, B, t, r, fn)
                errs.append(err)
            dt = time.time() - t0
            print(f"{key}: 2m={2*m}  ||a||_1={condition_number(a):8.4f}  "
                  f"||k||_1={k_norm(k):4d}  min_err={min(errs):.3e}  ({dt:.1f}s)")
            results["methods"][key] = {
                "order_2m": 2 * m,
                "cond_a_1": condition_number(a),
                "k_1": k_norm(k),
                "k": [int(x) for x in k],
                "a": [float(x) for x in a],
                "errors": errs,
            }

    outp = Path(__file__).parent.parent / "report" / "evidence" / "02_benchmark_N4_t1.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {outp}")


if __name__ == "__main__":
    main()
