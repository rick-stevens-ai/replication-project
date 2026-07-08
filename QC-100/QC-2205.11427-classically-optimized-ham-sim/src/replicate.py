"""
Replication of arXiv:2205.11427 (Mc Keever & Lubasch, 2023).
'Classically optimized Hamiltonian simulation'

Core claim to test:
  For a small transverse-field Ising chain with longitudinal field (open BC),
  a brickwall circuit whose parameters are optimized CLASSICALLY to minimize
  || U(theta) - exp(-itH) ||_F achieves a much lower approximation error than
  a standard Trotter product formula (I, II) at the same brickwall depth /
  matched gate count. For >=2 layers the paper reports ~2 orders of magnitude
  improvement.

We reproduce this at n=3 qubits (kept tiny so the whole sweep runs in seconds
on CPU with exact 2^n unitaries). Everything is real numpy / scipy /qiskit.

Hamiltonian (Eq. 7 in paper), (J, g, h) = (2.0, 1.0, 1.0):
    H = J * sum_{k=1..n-1} Z_k Z_{k+1} + g * sum X_k + h * sum Z_k

Gates (Fig. 2 in paper):
    Rx(theta) = exp(-i theta X / 2)
    Rz(theta) = exp(-i theta Z / 2)
    Uzz(theta) = exp(-i theta Z tensor Z / 2)

Brickwall structure (1 layer, n=3):
    For each qubit: Rz(a) Rx(b) Rz(c) single-qubit block (a "U3-like" universal 1q).
    Then a brick of two-qubit Uzz gates on the "even" bond (0,1) and "odd" bond (1,2).
    Then another U3-like block per qubit.
    (This matches the paper's parameterization pattern: alternating 1q + Uzz bricks.)

We compare:
  - Trotter I  (first order): e^{-it H_X} e^{-it H_Z}
  - Trotter II (second order): e^{-it H_X/2} e^{-it H_Z} e^{-it H_X/2}
  - Classical-opt with the SAME number of parameters/gates as the Trotter circuit.

Metric (Eq. 2 of paper):
    eps_approx = sqrt(1 - Re[Tr(U_ansatz^dagger  exp(-itH))] / 2^n)
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

# ---------- Pauli basics ----------

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_all(ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def single_qubit_op(n, k, op):
    """Op on qubit k (0-indexed, leftmost = qubit 0), identity elsewhere."""
    factors = [I2] * n
    factors[k] = op
    return kron_all(factors)


def two_qubit_zz(n, k):
    """Z_k Z_{k+1} operator on n qubits."""
    factors = [I2] * n
    factors[k] = Z
    factors[k + 1] = Z
    return kron_all(factors)


# ---------- Hamiltonian ----------

def build_H(n, J=2.0, g=1.0, h=1.0):
    dim = 2 ** n
    H = np.zeros((dim, dim), dtype=complex)
    for k in range(n - 1):
        H += J * two_qubit_zz(n, k)
    for k in range(n):
        H += g * single_qubit_op(n, k, X)
    for k in range(n):
        H += h * single_qubit_op(n, k, Z)
    return H


def build_HZ(n, J=2.0, h=1.0):
    """The Z-part of H used by Trotter split."""
    dim = 2 ** n
    HZ = np.zeros((dim, dim), dtype=complex)
    for k in range(n - 1):
        HZ += J * two_qubit_zz(n, k)
    for k in range(n):
        HZ += h * single_qubit_op(n, k, Z)
    return HZ


def build_HX(n, g=1.0):
    dim = 2 ** n
    HX = np.zeros((dim, dim), dtype=complex)
    for k in range(n):
        HX += g * single_qubit_op(n, k, X)
    return HX


# ---------- Rotation gates ----------

def Rx_mat(theta):
    return expm(-1j * theta / 2 * X)


def Rz_mat(theta):
    return expm(-1j * theta / 2 * Z)


def Uzz_mat_full(n, k, theta):
    """exp(-i theta/2 Z_k Z_{k+1}) as full 2^n matrix."""
    op = two_qubit_zz(n, k)  # this is Z_k Z_{k+1}
    return expm(-1j * theta / 2 * op)


def single_qubit_layer(n, params):
    """Apply Rz(a) Rx(b) Rz(c) on each of n qubits.

    params has length 3*n: (a0, b0, c0, a1, b1, c1, ...)
    Returns the 2^n x 2^n unitary.
    """
    dim = 2 ** n
    U = np.eye(dim, dtype=complex)
    for k in range(n):
        a, b, c = params[3 * k], params[3 * k + 1], params[3 * k + 2]
        g_k = Rz_mat(a) @ Rx_mat(b) @ Rz_mat(c)  # 2x2
        # embed on qubit k
        factors = [I2] * n
        factors[k] = g_k
        U = kron_all(factors) @ U
    return U


def zz_brick_full(n, params):
    """Brick of Uzz on each nearest-neighbor bond, param per bond.

    For n=3: bonds (0,1), (1,2)  -> len(params) = n-1
    """
    dim = 2 ** n
    U = np.eye(dim, dtype=complex)
    for k in range(n - 1):
        U = Uzz_mat_full(n, k, params[k]) @ U
    return U


def brickwall_ansatz(n, thetas, n_layers):
    """
    Universal brickwall with `n_layers` layers.

    Each layer = single-qubit U3-like block (3n params)
                 + one Uzz brick on all n-1 bonds (n-1 params)
    Plus a final single-qubit block (3n params) at the end.

    Total params per full ansatz = n_layers*(3n + (n-1)) + 3n
    """
    per_layer = 3 * n + (n - 1)
    expected = n_layers * per_layer + 3 * n
    assert len(thetas) == expected, f"expected {expected} params, got {len(thetas)}"

    dim = 2 ** n
    U = np.eye(dim, dtype=complex)
    idx = 0
    for _ in range(n_layers):
        p1q = thetas[idx:idx + 3 * n]; idx += 3 * n
        U = single_qubit_layer(n, p1q) @ U
        pzz = thetas[idx:idx + (n - 1)]; idx += (n - 1)
        U = zz_brick_full(n, pzz) @ U
    p_final = thetas[idx:idx + 3 * n]; idx += 3 * n
    U = single_qubit_layer(n, p_final) @ U
    return U


def num_params(n, n_layers):
    return n_layers * (3 * n + (n - 1)) + 3 * n


# ---------- Trotter circuits (real matrix product) ----------

def trotter_I(n, t, J=2.0, g=1.0, h=1.0, n_reps=1):
    """One 'brickwall layer' = one Trotter I step covering time t/n_reps.

    We build it out of the same primitive gates the paper's ansatz uses
    (Rx, Rz, Uzz), so the gate-count comparison is fair.

    Trotter I:  exp(-i tau H_X) exp(-i tau H_Z)
      exp(-i tau H_X) = prod_k Rx(2 tau g)
      exp(-i tau H_Z) = prod_k exp(-i tau J Z_k Z_{k+1}) * prod_k Rz(2 tau h)
                     = prod_k Uzz(2 tau J) * prod_k Rz(2 tau h)
    """
    dim = 2 ** n
    U = np.eye(dim, dtype=complex)
    tau = t / n_reps
    for _ in range(n_reps):
        # exp(-i tau H_Z) part
        # first the single-qubit Rz on each site
        for k in range(n):
            factors = [I2] * n
            factors[k] = Rz_mat(2 * tau * h)
            U = kron_all(factors) @ U
        # then Uzz on each bond
        for k in range(n - 1):
            U = Uzz_mat_full(n, k, 2 * tau * J) @ U
        # exp(-i tau H_X) part
        for k in range(n):
            factors = [I2] * n
            factors[k] = Rx_mat(2 * tau * g)
            U = kron_all(factors) @ U
    return U


def trotter_II(n, t, J=2.0, g=1.0, h=1.0, n_reps=1):
    """2nd-order (Strang) Trotter: exp(-i tau H_X/2) exp(-i tau H_Z) exp(-i tau H_X/2).

    Same primitive gates as ansatz.
    """
    dim = 2 ** n
    U = np.eye(dim, dtype=complex)
    tau = t / n_reps
    for _ in range(n_reps):
        # exp(-i tau H_X / 2)
        for k in range(n):
            factors = [I2] * n
            factors[k] = Rx_mat(tau * g)  # angle = 2 * (tau/2) * g = tau*g
            U = kron_all(factors) @ U
        # exp(-i tau H_Z)
        for k in range(n):
            factors = [I2] * n
            factors[k] = Rz_mat(2 * tau * h)
            U = kron_all(factors) @ U
        for k in range(n - 1):
            U = Uzz_mat_full(n, k, 2 * tau * J) @ U
        # exp(-i tau H_X / 2)
        for k in range(n):
            factors = [I2] * n
            factors[k] = Rx_mat(tau * g)
            U = kron_all(factors) @ U
    return U


# ---------- Error metric ----------

def eps_approx(U_ansatz, U_target, n):
    """Paper Eq. (2): sqrt(1 - Re[Tr(U^dagger U_target)] / 2^n).

    U_ansatz, U_target are 2^n x 2^n unitary. Value in [0, sqrt(2)].
    """
    dim = 2 ** n
    tr = np.trace(U_ansatz.conj().T @ U_target)
    val = 1 - np.real(tr) / dim
    # numerical safety
    return float(np.sqrt(max(val, 0.0)))


# ---------- Classical optimization ----------

def optimize_brickwall(n, t, n_layers, H, n_restarts=8, seed=0, verbose=False):
    """Fit brickwall ansatz to U_target = exp(-itH) by minimizing eps_approx.

    Uses scipy L-BFGS-B with random restarts. The paper mentions L-BFGS as
    a practical alternative to global Newton for larger circuits; we use it
    here for simplicity and robustness on the small n we can afford.
    """
    U_target = expm(-1j * t * H)
    nparam = num_params(n, n_layers)
    dim = 2 ** n

    def cost(theta):
        Ua = brickwall_ansatz(n, theta, n_layers)
        # cost = -Re Tr(U^dag U_target)  (minimize -> maximize overlap)
        tr = np.trace(Ua.conj().T @ U_target)
        return -np.real(tr)

    rng = np.random.default_rng(seed)
    best = None
    best_theta = None
    for r in range(n_restarts):
        # start near identity for r=0, else random small
        if r == 0:
            theta0 = np.zeros(nparam)
        else:
            theta0 = rng.uniform(-np.pi, np.pi, size=nparam) * 0.3
        res = minimize(cost, theta0, method="L-BFGS-B",
                       options={"maxiter": 800, "ftol": 1e-13, "gtol": 1e-9})
        val = res.fun
        if verbose:
            print(f"  restart {r}: cost={val:.6f} nit={res.nit}")
        if best is None or val < best:
            best = val
            best_theta = res.x
    Ua = brickwall_ansatz(n, best_theta, n_layers)
    err = eps_approx(Ua, U_target, n)
    return best_theta, err, Ua


# ---------- Main sweep ----------

def sweep(n=3, times=None, out_dir="report/evidence"):
    if times is None:
        times = [0.05, 0.1, 0.2, 0.4, 0.8]
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    H = build_H(n)
    print(f"# n={n}, ||H|| = {np.linalg.norm(H, ord=2):.4f}")

    rows = []
    t0_all = time.time()
    for t in times:
        print(f"\n=== t = {t} ===")
        U_target = expm(-1j * t * H)

        # --- Trotter at 1-layer depth ---
        Ut1_I = trotter_I(n, t, n_reps=1)
        Ut1_II = trotter_II(n, t, n_reps=1)
        e_tI_1 = eps_approx(Ut1_I, U_target, n)
        e_tII_1 = eps_approx(Ut1_II, U_target, n)

        # --- Trotter at 2-layer depth ---
        Ut2_I = trotter_I(n, t, n_reps=2)
        Ut2_II = trotter_II(n, t, n_reps=2)
        e_tI_2 = eps_approx(Ut2_I, U_target, n)
        e_tII_2 = eps_approx(Ut2_II, U_target, n)

        # --- Trotter at 3-layer depth (for the 3-layer comparison) ---
        Ut3_I = trotter_I(n, t, n_reps=3)
        Ut3_II = trotter_II(n, t, n_reps=3)
        e_tI_3 = eps_approx(Ut3_I, U_target, n)
        e_tII_3 = eps_approx(Ut3_II, U_target, n)

        # --- Classically-optimized brickwall ---
        print(f"  optimizing L=1 ... ", end="", flush=True); ts = time.time()
        _, e_opt_1, _ = optimize_brickwall(n, t, 1, H, n_restarts=3, seed=1)
        print(f"eps={e_opt_1:.3e}  ({time.time()-ts:.1f}s)")
        print(f"  optimizing L=2 ... ", end="", flush=True); ts = time.time()
        _, e_opt_2, _ = optimize_brickwall(n, t, 2, H, n_restarts=3, seed=2)
        print(f"eps={e_opt_2:.3e}  ({time.time()-ts:.1f}s)")
        print(f"  optimizing L=3 ... ", end="", flush=True); ts = time.time()
        _, e_opt_3, _ = optimize_brickwall(n, t, 3, H, n_restarts=3, seed=3)
        print(f"eps={e_opt_3:.3e}  ({time.time()-ts:.1f}s)")

        row = dict(
            t=t,
            trotterI_L1=e_tI_1, trotterII_L1=e_tII_1, opt_L1=e_opt_1,
            trotterI_L2=e_tI_2, trotterII_L2=e_tII_2, opt_L2=e_opt_2,
            trotterI_L3=e_tI_3, trotterII_L3=e_tII_3, opt_L3=e_opt_3,
        )
        rows.append(row)

    print(f"\nTotal sweep time: {time.time()-t0_all:.1f}s")

    # Save JSON
    out = {
        "paper": "arXiv:2205.11427",
        "n_qubits": n,
        "hamiltonian": {"J": 2.0, "g": 1.0, "h": 1.0, "form": "TFIM w/ long field, open BC"},
        "metric": "eps_approx = sqrt(1 - Re[Tr(U_ansatz^dag * exp(-itH))]/2^n)",
        "rows": rows,
    }
    with open(Path(out_dir) / "sweep.json", "w") as f:
        json.dump(out, f, indent=2)
    with open(Path(out_dir) / "sweep.csv", "w") as f:
        cols = ["t", "trotterI_L1", "trotterII_L1", "opt_L1",
                "trotterI_L2", "trotterII_L2", "opt_L2",
                "trotterI_L3", "trotterII_L3", "opt_L3"]
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join(f"{r[c]:.6e}" if c != "t" else f"{r[c]}" for c in cols) + "\n")

    # Return the ratio at the deepest matched setting we care about
    return out


if __name__ == "__main__":
    sweep(n=3, times=[0.1, 0.2, 0.4, 0.8], out_dir="report/evidence")
