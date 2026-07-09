#!/usr/bin/env python3
"""
Real numpy reproduction of the core claim of
Zalka, "Efficient Simulation of Quantum Systems by Quantum Computers"
(arXiv:quant-ph/9603026, 1996).

Core claim (adapted from Zalka Sec.2, and the standard Suzuki-Trotter analysis
that quantifies the "efficient simulation" gate count):

    A short-time unitary evolution exp(-i H dt) of a quantum system with
    a local Hamiltonian H = A + B can be approximated by

        1st order:  U1(dt) = exp(-i A dt) exp(-i B dt)               error/step = O(dt^2)
        2nd order:  U2(dt) = exp(-i A dt/2) exp(-i B dt) exp(-i A dt/2)  error/step = O(dt^3)

    Iterated K = T/dt times to reach total time T, the operator-norm error scales as

        1st order:  epsilon(K) = O(dt)        (log-log slope ~ 1)
        2nd order:  epsilon(K) = O(dt^2)      (log-log slope ~ 2)

    Zalka's Section 2 gives this splitting for kinetic + potential; the same
    scaling underlies his gate-count estimate O(poly(n, 1/eps, T)).

We reproduce this on a 1D Heisenberg spin chain
    H = sum_i (X_i X_{i+1} + Y_i Y_{i+1} + Z_i Z_{i+1})     (open BC)
on n=4 qubits, splitting H = H_odd + H_even (odd/even bonds mutually commute
inside each group but [H_odd, H_even] != 0, exercising the Trotter error).

Ground truth: U_exact = expm(-i H T) via scipy.linalg.expm.
Compare epsilon(K) = ||U_trotter - U_exact||_F for K in {10,20,50,100,200}.
Fit log-log slopes of eps vs dt.
"""

from __future__ import annotations
import json, os, time, platform
from pathlib import Path
import numpy as np
from numpy.linalg import matrix_power
from scipy.linalg import expm

# --- Pauli operators and tensor helpers --------------------------------------
I2 = np.array([[1, 0], [0, 1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kronN(ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def two_site_term(n: int, i: int, A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Return op with A on qubit i and B on qubit i+1 (open chain, i in [0..n-2])."""
    ops = [I2] * n
    ops[i] = A
    ops[i + 1] = B
    return kronN(ops)


def heisenberg_bond(n: int, i: int) -> np.ndarray:
    """h_{i,i+1} = X_iX_{i+1} + Y_iY_{i+1} + Z_iZ_{i+1}"""
    return two_site_term(n, i, X, X) + two_site_term(n, i, Y, Y) + two_site_term(n, i, Z, Z)


def build_hamiltonian(n: int):
    dim = 2 ** n
    H = np.zeros((dim, dim), dtype=complex)
    H_odd = np.zeros((dim, dim), dtype=complex)   # bonds (0,1),(2,3),...
    H_even = np.zeros((dim, dim), dtype=complex)  # bonds (1,2),(3,4),...
    for i in range(n - 1):
        term = heisenberg_bond(n, i)
        H += term
        if i % 2 == 0:
            H_odd += term
        else:
            H_even += term
    return H, H_odd, H_even


# --- Trotter approximants ----------------------------------------------------
def trotter1_step(H_a, H_b, dt):
    return expm(-1j * H_a * dt) @ expm(-1j * H_b * dt)


def trotter2_step(H_a, H_b, dt):
    half = expm(-1j * H_a * dt / 2.0)
    full = expm(-1j * H_b * dt)
    return half @ full @ half


def approximate_evolution(H_a, H_b, T, K, order=1):
    dt = T / K
    if order == 1:
        U_step = trotter1_step(H_a, H_b, dt)
    elif order == 2:
        U_step = trotter2_step(H_a, H_b, dt)
    else:
        raise ValueError(order)
    return matrix_power(U_step, K)


# --- Experiment --------------------------------------------------------------
def run(n: int = 4, T: float = 1.0, Ks=(10, 20, 50, 100, 200), seed: int = 0):
    rng = np.random.default_rng(seed)
    H, H_odd, H_even = build_hamiltonian(n)

    # sanity: H is Hermitian
    herm_err = np.linalg.norm(H - H.conj().T)
    assert herm_err < 1e-12, f"H not Hermitian: {herm_err}"

    # gold
    t0 = time.perf_counter()
    U_exact = expm(-1j * H * T)
    t_exact = time.perf_counter() - t0

    rows = []
    for K in Ks:
        dt = T / K
        t0 = time.perf_counter()
        U1 = approximate_evolution(H_odd, H_even, T, K, order=1)
        t1 = time.perf_counter() - t0
        eps1 = float(np.linalg.norm(U1 - U_exact, ord="fro"))

        t0 = time.perf_counter()
        U2 = approximate_evolution(H_odd, H_even, T, K, order=2)
        t2 = time.perf_counter() - t0
        eps2 = float(np.linalg.norm(U2 - U_exact, ord="fro"))

        # also sanity-check on a random state to confirm state-vector consistency
        psi = rng.standard_normal(2 ** n) + 1j * rng.standard_normal(2 ** n)
        psi /= np.linalg.norm(psi)
        se1 = float(np.linalg.norm(U1 @ psi - U_exact @ psi))
        se2 = float(np.linalg.norm(U2 @ psi - U_exact @ psi))

        rows.append({
            "K": int(K), "dt": float(dt),
            "eps1_frobenius": eps1, "eps2_frobenius": eps2,
            "state_err1": se1, "state_err2": se2,
            "wall_s_order1": t1, "wall_s_order2": t2,
        })

    # log-log linear fit of eps vs dt (excluding degenerate points if any zero)
    dts = np.array([r["dt"] for r in rows])
    eps1 = np.array([r["eps1_frobenius"] for r in rows])
    eps2 = np.array([r["eps2_frobenius"] for r in rows])

    # numpy polyfit on log-log
    slope1, intercept1 = np.polyfit(np.log(dts), np.log(eps1), 1)
    slope2, intercept2 = np.polyfit(np.log(dts), np.log(eps2), 1)

    # unitarity check on the *approximants* themselves (each Trotter step is unitary
    # because it's a product of unitaries), and gold is unitary
    U1_last = approximate_evolution(H_odd, H_even, T, Ks[-1], order=1)
    U2_last = approximate_evolution(H_odd, H_even, T, Ks[-1], order=2)
    dim = 2 ** n
    unit_err_exact = float(np.linalg.norm(U_exact.conj().T @ U_exact - np.eye(dim)))
    unit_err_U1 = float(np.linalg.norm(U1_last.conj().T @ U1_last - np.eye(dim)))
    unit_err_U2 = float(np.linalg.norm(U2_last.conj().T @ U2_last - np.eye(dim)))

    result = {
        "paper": "Zalka 1996 (arXiv:quant-ph/9603026)",
        "system": f"1D Heisenberg XXX open chain, n={n} spins (dim={dim})",
        "hamiltonian_split": "H = H_odd + H_even (nearest-neighbor bonds grouped by parity)",
        "total_time_T": T,
        "K_values": list(Ks),
        "wall_s_exact_gold": t_exact,
        "rows": rows,
        "loglog_fit_order1": {"slope": float(slope1), "intercept": float(intercept1),
                               "prediction": "slope -> 1 (Zalka/Trotter)"},
        "loglog_fit_order2": {"slope": float(slope2), "intercept": float(intercept2),
                               "prediction": "slope -> 2 (Suzuki-Trotter symmetric)"},
        "unitarity_errors": {
            "exact_expm_minus_identity": unit_err_exact,
            "trotter1_K200_minus_identity": unit_err_U1,
            "trotter2_K200_minus_identity": unit_err_U2,
        },
        "env": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
    }
    return result


def main():
    out_dir = Path(__file__).resolve().parent
    result = run()
    (out_dir / "trotter_results.json").write_text(json.dumps(result, indent=2))

    print("=" * 68)
    print("Zalka (1996) Trotter simulation reproduction  —  1D Heisenberg n=4")
    print("=" * 68)
    print(f"Exact  gold expm wall = {result['wall_s_exact_gold']:.4f} s")
    print(f"System : {result['system']}")
    print(f"Total T: {result['total_time_T']}")
    print()
    print(f"{'K':>5} {'dt':>10} {'eps1 (frob)':>16} {'eps2 (frob)':>16} "
          f"{'state1':>12} {'state2':>12}")
    for r in result["rows"]:
        print(f"{r['K']:>5} {r['dt']:>10.5f} {r['eps1_frobenius']:>16.6e} "
              f"{r['eps2_frobenius']:>16.6e} {r['state_err1']:>12.4e} "
              f"{r['state_err2']:>12.4e}")
    print()
    s1 = result["loglog_fit_order1"]["slope"]
    s2 = result["loglog_fit_order2"]["slope"]
    print(f"log-log fit slope, 1st-order Trotter : {s1:+.4f}   (expect ~ 1.0)")
    print(f"log-log fit slope, 2nd-order Suzuki  : {s2:+.4f}   (expect ~ 2.0)")
    print()
    print("Unitarity check (norm||U^H U - I||):")
    for k, v in result["unitarity_errors"].items():
        print(f"  {k:44s} = {v:.3e}")

    ok1 = 0.85 <= s1 <= 1.15
    ok2 = 1.80 <= s2 <= 2.20
    verdict = "REPLICATED" if (ok1 and ok2) else ("PARTIAL" if ok1 else "SPOT-CHECK")
    print()
    print(f"Slope-1 in [0.85,1.15] : {ok1}   Slope-2 in [1.80,2.20] : {ok2}")
    print(f"Inferred verdict       : {verdict}")

    # dump verdict too
    (out_dir / "trotter_verdict.json").write_text(json.dumps({
        "slope_order1": s1, "slope_order2": s2,
        "ok_order1": ok1, "ok_order2": ok2, "verdict": verdict,
    }, indent=2))


if __name__ == "__main__":
    main()
