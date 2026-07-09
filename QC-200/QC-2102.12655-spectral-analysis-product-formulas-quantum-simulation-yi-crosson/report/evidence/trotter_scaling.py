#!/usr/bin/env python3
"""
Independent replication core for arXiv:2102.12655
(Yi & Crosson, "Spectral Analysis of Product Formulas for Quantum Simulation").

We do NOT reproduce their fine QPE/DAS asymptotic-scaling claims (those are
analytical statements about the effective Hamiltonian). We DO reproduce the
foundational quantitative backdrop the paper builds on:

  * 1st-order Lie-Trotter (S1) product-formula error is O(dt) in operator norm
    and O(dt^2) per step, with per-step leading term  dt^2/2 * ||[H1,H2]||.
  * 2nd-order symmetric Suzuki (S2) error is O(dt^2) in operator norm.
  * 4th-order Suzuki-Trotter (S4) error is O(dt^4) in operator norm.

We also demonstrate the paper's core motif: the operator-norm bound is often
LOOSE compared to a state-fidelity error on a specific initial eigenstate,
which is exactly the paper's central "tighter for structured Hamiltonians"
message (in state-error terms, not commutator-norm terms).

Test Hamiltonian: 1D transverse-field Ising, open boundary, n qubits.
    H1 = -J * sum_i Z_i Z_{i+1}   (ZZ layer)
    H2 = -h * sum_i X_i           (X layer)
    H  = H1 + H2
Non-commuting since [Z_i Z_{i+1}, X_i] != 0.

Reference exact evolution: scipy.linalg.expm(-1j*H*t).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from scipy.linalg import expm, norm

HERE = Path(__file__).resolve().parent


# ---- Pauli / Hamiltonian helpers -------------------------------------------------

I2 = np.eye(2, dtype=complex)
X  = np.array([[0, 1], [1, 0]], dtype=complex)
Z  = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_list(ops):
    out = ops[0]
    for A in ops[1:]:
        out = np.kron(out, A)
    return out


def single_site(op, i, n):
    return kron_list([op if j == i else I2 for j in range(n)])


def tfim_layers(n, J=1.0, h=1.0):
    """Return H1 (ZZ), H2 (X), H = H1+H2 for open-boundary TFIM."""
    d = 2 ** n
    H1 = np.zeros((d, d), dtype=complex)
    H2 = np.zeros((d, d), dtype=complex)
    for i in range(n - 1):
        H1 += -J * (single_site(Z, i, n) @ single_site(Z, i + 1, n))
    for i in range(n):
        H2 += -h * single_site(X, i, n)
    return H1, H2, H1 + H2


# ---- Product formulas ------------------------------------------------------------

def S1(H1, H2, dt):
    """1st-order Lie-Trotter e^{-iH1 dt} e^{-iH2 dt}."""
    return expm(-1j * H1 * dt) @ expm(-1j * H2 * dt)


def S2(H1, H2, dt):
    """2nd-order symmetric Strang: e^{-iH1 dt/2} e^{-iH2 dt} e^{-iH1 dt/2}."""
    A = expm(-1j * H1 * dt / 2)
    B = expm(-1j * H2 * dt)
    return A @ B @ A


def S4(H1, H2, dt):
    """4th-order Suzuki (Yoshida) recursion built on S2."""
    # Standard Suzuki fractal, order 4.
    s = 1.0 / (4.0 - 4.0 ** (1.0 / 3.0))
    return (
        S2(H1, H2, s * dt)
        @ S2(H1, H2, s * dt)
        @ S2(H1, H2, (1 - 4 * s) * dt)
        @ S2(H1, H2, s * dt)
        @ S2(H1, H2, s * dt)
    )


def repeated(fmt, H1, H2, dt, steps):
    U = np.eye(H1.shape[0], dtype=complex)
    step = fmt(H1, H2, dt)
    for _ in range(steps):
        U = step @ U
    return U


# ---- Experiment ------------------------------------------------------------------

def run(n=4, J=1.0, h=1.0, t=1.0, dts=(0.5, 0.25, 0.125, 0.0625, 0.03125)):
    H1, H2, H = tfim_layers(n, J=J, h=h)
    Uex = expm(-1j * H * t)

    # ground state of H for the state-fidelity comparison
    evals, evecs = np.linalg.eigh(H)
    psi0 = evecs[:, 0]
    psi_ex = Uex @ psi0

    # ||[H1,H2]|| for the leading Trotter constant
    comm = H1 @ H2 - H2 @ H1
    comm_norm = np.linalg.norm(comm, ord=2)

    rows = []
    for dt in dts:
        L = int(round(t / dt))
        # exact steps must tile t exactly
        assert abs(L * dt - t) < 1e-12, (L, dt, t)

        errs = {}
        state_infids = {}
        for name, fmt in [("S1", S1), ("S2", S2), ("S4", S4)]:
            U_approx = repeated(fmt, H1, H2, dt, L)
            op_err = np.linalg.norm(Uex - U_approx, ord=2)
            psi_ap = U_approx @ psi0
            # fidelity error = 1 - |<psi_ex|psi_ap>|^2
            infid = 1.0 - abs(np.vdot(psi_ex, psi_ap)) ** 2
            errs[name] = op_err
            state_infids[name] = infid

        # Leading per-step Trotter estimate (2nd-order local error, 1st-order global)
        # For S1: per-step op error ~ dt^2/2 * ||[H1,H2]|| ; global L * that ~ t*dt/2 * ||[H1,H2]||
        s1_leading_global = L * (dt ** 2) / 2.0 * comm_norm

        rows.append(
            dict(
                dt=dt, L=L,
                op_err_S1=errs["S1"],
                op_err_S2=errs["S2"],
                op_err_S4=errs["S4"],
                infid_S1=state_infids["S1"],
                infid_S2=state_infids["S2"],
                infid_S4=state_infids["S4"],
                s1_leading_bound=s1_leading_global,
            )
        )

    return dict(
        n=n, J=J, h=h, t=t, comm_norm=comm_norm,
        rows=rows,
    )


def loglog_slope(xs, ys):
    lx, ly = np.log(np.asarray(xs)), np.log(np.asarray(ys))
    A = np.vstack([lx, np.ones_like(lx)]).T
    slope, intercept = np.linalg.lstsq(A, ly, rcond=None)[0]
    return float(slope), float(intercept)


def main():
    t0 = time.time()
    results_by_n = {}
    for n in (4, 6):
        res = run(n=n)
        # slopes
        dts = [r["dt"] for r in res["rows"]]
        for order_name in ("S1", "S2", "S4"):
            errs = [r[f"op_err_{order_name}"] for r in res["rows"]]
            slope, _ = loglog_slope(dts, errs)
            res[f"slope_op_{order_name}"] = slope
        # slopes on state infidelity
        for order_name in ("S1", "S2", "S4"):
            infids = [max(r[f"infid_{order_name}"], 1e-30) for r in res["rows"]]
            slope, _ = loglog_slope(dts, infids)
            res[f"slope_infid_{order_name}"] = slope

        # tightness check: op-norm bound (leading, S1) vs actual op error
        for r in res["rows"]:
            r["ratio_bound_over_actual_S1"] = r["s1_leading_bound"] / max(r["op_err_S1"], 1e-30)
            r["ratio_actual_op_over_infid_S1"] = r["op_err_S1"] / max(r["infid_S1"], 1e-30)

        results_by_n[str(n)] = res

    payload = dict(
        script="trotter_scaling.py",
        arxiv_id="2102.12655",
        elapsed_sec=time.time() - t0,
        results_by_n=results_by_n,
    )
    out = HERE / "trotter_scaling.json"
    out.write_text(json.dumps(payload, indent=2, default=float))
    print(f"wrote {out}")

    # Print summary
    for nkey, res in results_by_n.items():
        n = res["n"]
        print(f"\n=== n={n} qubits, t={res['t']}, ||[H1,H2]||={res['comm_norm']:.4f} ===")
        print(f"{'dt':>10} {'L':>5} {'opErrS1':>12} {'opErrS2':>12} {'opErrS4':>12} "
              f"{'infS1':>12} {'infS2':>12} {'infS4':>12} {'S1bound':>12} {'bnd/act':>10}")
        for r in res["rows"]:
            print(f"{r['dt']:>10.5f} {r['L']:>5d} "
                  f"{r['op_err_S1']:>12.4e} {r['op_err_S2']:>12.4e} {r['op_err_S4']:>12.4e} "
                  f"{r['infid_S1']:>12.4e} {r['infid_S2']:>12.4e} {r['infid_S4']:>12.4e} "
                  f"{r['s1_leading_bound']:>12.4e} {r['ratio_bound_over_actual_S1']:>10.3f}")
        print(f"  log-log slopes (op-norm err vs dt): "
              f"S1={res['slope_op_S1']:.3f}  S2={res['slope_op_S2']:.3f}  S4={res['slope_op_S4']:.3f}")
        print(f"  log-log slopes (state infidelity vs dt): "
              f"S1={res['slope_infid_S1']:.3f}  S2={res['slope_infid_S2']:.3f}  S4={res['slope_infid_S4']:.3f}")


if __name__ == "__main__":
    main()
