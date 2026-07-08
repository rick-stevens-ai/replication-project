#!/usr/bin/env python3
"""
Replication of empirical Trotter (product-formula) error scaling for a 1D
Heisenberg spin chain, following:

  A. M. Childs, D. Maslov, Y. Nam, N. J. Ross, Y. Su,
  "Toward the first quantum simulation with quantum speedup,"
  PNAS 115(38) 9456-9461 (2018). arXiv:1711.10980.

Model Hamiltonian (nearest-neighbor Heisenberg + random z-field), matching the
paper's benchmark system:

    H = sum_j ( X_j X_{j+1} + Y_j Y_{j+1} + Z_j Z_{j+1} )
        + sum_j h_j Z_j ,     h_j ~ Uniform[-h, h]

We compare exact time evolution U = exp(-i H t) against Suzuki-Trotter product
formulas of order 1, 2, 4 (PF1, PF2, PF4), each with r Trotter steps, and measure
the SPECTRAL-NORM (operator) error  ||U_exact - U_PF||_2  as a function of r.

Theory (empirical worst-case scaling used in the paper):
    order-p product formula error  ~  C * (t/r)^{p+1} * r  =  C' * r^{-p}
so on a log-log plot of error vs r the slope should be:
    PF1 -> -1,  PF2 -> -2,  PF4 -> -4.

Everything is pure numpy/scipy state-vector / operator simulation.
"""

import numpy as np
from scipy.linalg import expm
import json, os

np.random.seed(20260702)

# ---- Pauli matrices ----
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def op_on(n, ops):
    """Tensor product operator: ops is dict {site: 2x2}. Sites not listed => I."""
    mats = [ops.get(k, I2) for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def build_terms(n, h_field):
    """Return list of local Hermitian terms whose sum is H.
    Terms are grouped so that PF construction is clean:
      even bonds, odd bonds, and single-site field terms.
    We return a flat ordered list of (matrix) terms for the product formula.
    """
    terms = []
    # bond terms: XX+YY+ZZ on each nearest-neighbor pair (open chain)
    for j in range(n - 1):
        bond = (op_on(n, {j: X, j + 1: X})
                + op_on(n, {j: Y, j + 1: Y})
                + op_on(n, {j: Z, j + 1: Z}))
        terms.append(bond)
    # field terms
    for j in range(n):
        terms.append(h_field[j] * op_on(n, {j: Z}))
    return terms


def total_H(terms):
    H = np.zeros_like(terms[0])
    for t in terms:
        H = H + t
    return H


def pf1(terms, t, r):
    """First-order (Lie-Trotter) product formula, r steps."""
    dt = t / r
    step = np.eye(terms[0].shape[0], dtype=complex)
    for term in terms:
        step = expm(-1j * term * dt) @ step
    U = np.linalg.matrix_power(step, r)
    return U


def pf2(terms, t, r):
    """Second-order (symmetric Strang) product formula, r steps.
    S2(dt) = prod_forward(dt/2) * prod_backward(dt/2)
    """
    dt = t / r
    fwd = [expm(-1j * term * (dt / 2)) for term in terms]
    step = np.eye(terms[0].shape[0], dtype=complex)
    # forward half
    for e in fwd:
        step = e @ step
    # backward half
    for e in reversed(fwd):
        step = e @ step
    U = np.linalg.matrix_power(step, r)
    return U


def _s2_operator(terms, dt):
    fwd = [expm(-1j * term * (dt / 2)) for term in terms]
    step = np.eye(terms[0].shape[0], dtype=complex)
    for e in fwd:
        step = e @ step
    for e in reversed(fwd):
        step = e @ step
    return step


def pf4(terms, t, r):
    """Fourth-order Suzuki product formula (Suzuki's fractal), r steps.
    S4(dt) = S2(u dt)^2 S2((1-4u)dt) S2(u dt)^2,  u = 1/(4 - 4^{1/3}).
    """
    dt = t / r
    u = 1.0 / (4.0 - 4.0 ** (1.0 / 3.0))
    a = _s2_operator(terms, u * dt)
    b = _s2_operator(terms, (1.0 - 4.0 * u) * dt)
    step = a @ a @ b @ a @ a
    U = np.linalg.matrix_power(step, r)
    return U


def spectral_error(U_exact, U_pf):
    return np.linalg.norm(U_exact - U_pf, ord=2)


def fit_slope(rs, errs):
    """Fit log(err) = slope*log(r) + c on the clean (pre-floor) regime."""
    lr = np.log(np.asarray(rs, float))
    le = np.log(np.asarray(errs, float))
    A = np.vstack([lr, np.ones_like(lr)]).T
    slope, c = np.linalg.lstsq(A, le, rcond=None)[0]
    return slope, c


def main():
    n = 6            # spins (2^6 = 64-dim Hilbert space)
    h = 1.0          # random field strength (Uniform[-h,h])
    t = 1.0          # total evolution time
    h_field = np.random.uniform(-h, h, size=n)

    terms = build_terms(n, h_field)
    H = total_H(terms)
    U_exact = expm(-1j * H * t)

    print(f"System: n={n} spins, dim={2**n}, t={t}, random z-field h in [-{h},{h}]")
    print(f"||H||_2 = {np.linalg.norm(H, ord=2):.4f}, #terms={len(terms)}")
    print()

    r_values = [1, 2, 4, 8, 16, 32, 64, 128]
    results = {"PF1": {}, "PF2": {}, "PF4": {}}

    for r in r_values:
        e1 = spectral_error(U_exact, pf1(terms, t, r))
        e2 = spectral_error(U_exact, pf2(terms, t, r))
        e4 = spectral_error(U_exact, pf4(terms, t, r))
        results["PF1"][r] = e1
        results["PF2"][r] = e2
        results["PF4"][r] = e4
        print(f"r={r:4d}   PF1={e1:.3e}   PF2={e2:.3e}   PF4={e4:.3e}")

    print()
    # Fit slopes on the asymptotic (clean) regime, avoiding numerical floor (~1e-13).
    def clean(order, rmin, rmax):
        rs = [r for r in r_values if rmin <= r <= rmax and results[order][r] > 1e-11]
        es = [results[order][r] for r in rs]
        return rs, es

    s1, _ = fit_slope(*clean("PF1", 4, 128))
    s2, _ = fit_slope(*clean("PF2", 4, 64))
    s4, _ = fit_slope(*clean("PF4", 2, 16))
    print("Fitted log-log slopes (empirical error scaling exponent):")
    print(f"  PF1 slope = {s1:.3f}   (theory -1)")
    print(f"  PF2 slope = {s2:.3f}   (theory -2)")
    print(f"  PF4 slope = {s4:.3f}   (theory -4)")

    out = {
        "system": {"n": n, "dim": 2 ** n, "t": t, "h": h,
                   "h_field": h_field.tolist(),
                   "H_spectral_norm": float(np.linalg.norm(H, ord=2))},
        "r_values": r_values,
        "errors": {k: {str(r): float(v) for r, v in d.items()}
                   for k, d in results.items()},
        "fitted_slopes": {"PF1": float(s1), "PF2": float(s2), "PF4": float(s4)},
        "theory_slopes": {"PF1": -1, "PF2": -2, "PF4": -4},
    }
    outpath = os.path.join(os.path.dirname(__file__), "..", "results", "trotter_results.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {os.path.abspath(outpath)}")


if __name__ == "__main__":
    main()
