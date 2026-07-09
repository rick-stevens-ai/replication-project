"""
Numerically compute the average eigenvalue-estimation success probability p_bar
from Mosca-Zalka (2003), Section 4.

The paper claims:
    p_bar = (1/p) sum_{k=0}^{p-1} f^2(k/p),    f(z) = sin(pi z) / (N sin(pi z/N))
which for large p (and large N) approaches ~0.4514 (the integral of sinc^2).

We reproduce this by:
  - fixing N = 2^n with N > p, varying p over increasing prime values,
  - computing p_bar exactly,
  - confirming p_bar -> 0.4513... (int_{-inf}^inf sinc^2(t) dt / integration =
    the "Fejer-like" limit specific to this window).

The paper's stated limit value 0.4514 for p, N -> infinity is our headline
numeric check.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sympy import isprime

OUT = Path(__file__).with_name("results_pbar.json")


def f(z: float, N: int) -> float:
    """f(z) = sin(pi z) / (N sin(pi z / N))."""
    if abs(z) < 1e-15:
        return 1.0
    num = np.sin(np.pi * z)
    den = N * np.sin(np.pi * z / N)
    return num / den


def f_squared_average(p: int, N: int) -> float:
    """(1/p) sum_{k=0}^{p-1} f^2(k/p)."""
    total = 0.0
    for k in range(p):
        total += f(k / p, N) ** 2
    return total / p


def theoretical_limit_by_integral(N: int) -> float:
    """Integrate f^2(z) over z in [0,1], approximating the p->infinity limit.

    p_bar = int_0^1 f^2(z) dz  (Riemann sum limit of (1/p) sum f^2(k/p))
    """
    zs = np.linspace(0, 1, 200_001)[1:-1]  # avoid endpoints
    vals = np.array([f(z, N) ** 2 for z in zs])
    return float(np.trapezoid(vals, zs))


def main() -> None:
    results: dict = {"convergence": []}

    # For each n choose smallest N=2^n > p (so N/p ratio is between 1 and 2)
    # and also try N ~ 4p to check N-dependence.
    for p in [7, 11, 31, 61, 127, 251, 509, 1021]:
        if not isprime(p):
            continue
        # N just above p
        n_min = int(np.ceil(np.log2(p))) + 0  # smallest 2^n >= p
        while 2**n_min < p:
            n_min += 1
        for n_extra in [0, 1, 2]:
            n = n_min + n_extra
            N = 2**n
            pbar = f_squared_average(p, N)
            results["convergence"].append(
                {"p": int(p), "N": int(N), "N_over_p": N / p, "pbar": float(pbar)}
            )

    # Theoretical p -> infty limit (Riemann integral), for large N
    for N in [1024, 4096, 16384]:
        results.setdefault("large_p_integral_limit", []).append(
            {"N": int(N), "pbar_limit_integral": theoretical_limit_by_integral(N)}
        )

    # The classic sinc^2 integral over one period gives approximately 0.4514
    # in the N-> infty limit (integral_0^1 sinc^2(pi z) dz).  Let's confirm.
    zs = np.linspace(1e-9, 1, 1_000_001)
    sinc2 = (np.sin(np.pi * zs) / (np.pi * zs)) ** 2
    val_inf_N = float(np.trapezoid(sinc2, zs))
    results["sinc2_over_0_to_1"] = val_inf_N
    results["paper_reported_limit"] = 0.4514
    results["deviation_from_paper"] = abs(val_inf_N - 0.4514)

    OUT.write_text(json.dumps(results, indent=2))
    print(f"Wrote {OUT}")
    print("\nConvergence of p_bar:")
    for row in results["convergence"]:
        print(f"  p={row['p']:5d}  N={row['N']:6d}  N/p={row['N_over_p']:.3f}  "
              f"p_bar={row['pbar']:.6f}")
    print(f"\nsinc^2 integral (0 to 1) = {val_inf_N:.6f}")
    print(f"Paper claims  p_bar_infty ≈ 0.4514   |diff| = {results['deviation_from_paper']:.6f}")


if __name__ == "__main__":
    main()
