#!/usr/bin/env python3
"""
Replication of Trotter (1st order) and Strang (2nd order symmetric) splitting
error scaling for a small quantum-chemistry-flavored model Hamiltonian.

Paper: Burgarth et al., "Strong Error Bounds for Trotter & Strang-Splittings
and Their Implications for Quantum Chemistry" (arXiv:2312.08044).

Testable claim (generic, non-pathological states — the standard/expected regime
that the paper's bounds recover): for evolution time t decomposed into r steps,
  ||e^{-iHt} - U_Trotter(t,r)|| ~ C1 * t^2 / r      (slope -1 in log-log err vs r)
  ||e^{-iHt} - U_Strang (t,r)|| ~ C2 * t^3 / r^2   (slope -2 in log-log err vs r)
The paper's novelty is showing the FIRST-order slope can degrade for pathological
(fat-tailed) states of unbounded Hamiltonians like hydrogen. For a bounded
model H = A + B (transverse-field Ising, a canonical q-chem-relevant testbed),
the standard scaling is exactly what the paper's general bounds predict.

We measure BOTH operator-norm error and state-error on a physically meaningful
initial state (product state |+>^n), fit slopes in log-log, and compare to the
predicted -1 (Trotter) and -2 (Strang).
"""
import json
import time
import numpy as np
from scipy.linalg import expm
from pathlib import Path

# -----------------------------------------------------------------------------
# Model Hamiltonian: 4-site transverse-field Ising, split H = A + B
# A = -J sum_i Z_i Z_{i+1}   (diagonal, "potential-like")
# B = -h sum_i X_i           ("kinetic-like")
# This is the canonical A+B splitting used in quantum-chemistry Trotter analyses
# (analogous to T+V for chemistry Hamiltonians).
# -----------------------------------------------------------------------------

def kron_list(ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out

def build_H(n=4, J=1.0, h=0.7):
    I = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    dim = 2 ** n

    A = np.zeros((dim, dim), dtype=complex)  # ZZ part
    for i in range(n - 1):
        ops = [I] * n
        ops[i] = Z
        ops[i + 1] = Z
        A += -J * kron_list(ops)

    B = np.zeros((dim, dim), dtype=complex)  # X part
    for i in range(n):
        ops = [I] * n
        ops[i] = X
        B += -h * kron_list(ops)

    return A, B

def op_norm(M):
    # Spectral (operator) 2-norm = largest singular value
    return np.linalg.norm(M, ord=2)

def trotter_step(A, B, dt):
    # 1st order: e^{-i A dt} e^{-i B dt}
    return expm(-1j * A * dt) @ expm(-1j * B * dt)

def strang_step(A, B, dt):
    # 2nd order symmetric: e^{-i A dt/2} e^{-i B dt} e^{-i A dt/2}
    eA_half = expm(-1j * A * dt / 2)
    return eA_half @ expm(-1j * B * dt) @ eA_half

def evolve(step_fn, A, B, t, r):
    dt = t / r
    U_step = step_fn(A, B, dt)
    # Compose r times via repeated squaring for efficiency at large r
    # For small r (< 200) direct multiply is fine.
    U = np.eye(A.shape[0], dtype=complex)
    for _ in range(r):
        U = U_step @ U
    return U

def measure(A, B, t, r_list, psi0):
    U_exact = expm(-1j * (A + B) * t)
    psi_exact = U_exact @ psi0
    rows = []
    for r in r_list:
        U_tr = evolve(trotter_step, A, B, t, r)
        U_st = evolve(strang_step, A, B, t, r)

        op_err_tr = op_norm(U_exact - U_tr)
        op_err_st = op_norm(U_exact - U_st)

        # State error (per paper's "strong / state-dependent" framing)
        st_err_tr = np.linalg.norm(psi_exact - U_tr @ psi0)
        st_err_st = np.linalg.norm(psi_exact - U_st @ psi0)

        rows.append({
            "r": int(r),
            "dt": float(t / r),
            "op_err_trotter": float(op_err_tr),
            "op_err_strang":  float(op_err_st),
            "state_err_trotter": float(st_err_tr),
            "state_err_strang":  float(st_err_st),
        })
        print(f"  r={r:4d} dt={t/r:.4f} | opTR={op_err_tr:.3e} opST={op_err_st:.3e} | stTR={st_err_tr:.3e} stST={st_err_st:.3e}")
    return rows

def fit_slope(r_arr, err_arr):
    # Fit err ~ C * r^slope => log err = log C + slope * log r
    mask = np.array(err_arr) > 0
    lr = np.log(np.array(r_arr)[mask])
    le = np.log(np.array(err_arr)[mask])
    slope, intercept = np.polyfit(lr, le, 1)
    # RMSE of fit
    pred = slope * lr + intercept
    rmse = float(np.sqrt(np.mean((le - pred) ** 2)))
    return float(slope), float(intercept), rmse

def main():
    t0 = time.time()
    n = 4
    J = 1.0
    h = 0.7
    t = 1.0    # small evolution time
    r_list = [2, 4, 8, 16, 32, 64, 128, 256]

    print(f"# Model: {n}-site TFIM, J={J}, h={h}, t={t}")
    A, B = build_H(n=n, J=J, h=h)
    print(f"# dim = {A.shape[0]}")
    print(f"# ||A||={op_norm(A):.4f}, ||B||={op_norm(B):.4f}, ||[A,B]||={op_norm(A@B - B@A):.4f}")

    dim = A.shape[0]
    # Initial state: product |+>^n = uniform superposition (typical q-chem starting state)
    psi0 = np.ones(dim, dtype=complex) / np.sqrt(dim)

    print("\n# Measuring errors vs r ...")
    rows = measure(A, B, t, r_list, psi0)

    r_arr = [row["r"] for row in rows]
    op_tr = [row["op_err_trotter"] for row in rows]
    op_st = [row["op_err_strang"]  for row in rows]
    st_tr = [row["state_err_trotter"] for row in rows]
    st_st = [row["state_err_strang"]  for row in rows]

    slope_op_tr, ic_op_tr, rmse_op_tr = fit_slope(r_arr, op_tr)
    slope_op_st, ic_op_st, rmse_op_st = fit_slope(r_arr, op_st)
    slope_st_tr, ic_st_tr, rmse_st_tr = fit_slope(r_arr, st_tr)
    slope_st_st, ic_st_st, rmse_st_st = fit_slope(r_arr, st_st)

    print("\n# Fitted slopes (log err vs log r); predicted: Trotter=-1, Strang=-2")
    print(f"  op-norm  Trotter slope = {slope_op_tr:+.4f}  (rmse={rmse_op_tr:.3e})   pred -1")
    print(f"  op-norm  Strang  slope = {slope_op_st:+.4f}  (rmse={rmse_op_st:.3e})   pred -2")
    print(f"  state    Trotter slope = {slope_st_tr:+.4f}  (rmse={rmse_st_tr:.3e})   pred -1")
    print(f"  state    Strang  slope = {slope_st_st:+.4f}  (rmse={rmse_st_st:.3e})   pred -2")

    result = {
        "model": {"type": "TFIM", "n_sites": n, "J": J, "h": h, "t": t},
        "splitting": {"A": "-J sum Z_i Z_{i+1}", "B": "-h sum X_i"},
        "initial_state": "|+>^n uniform superposition",
        "r_list": r_arr,
        "rows": rows,
        "fits": {
            "op_norm_trotter": {"slope": slope_op_tr, "intercept": ic_op_tr, "rmse": rmse_op_tr, "predicted_slope": -1},
            "op_norm_strang":  {"slope": slope_op_st, "intercept": ic_op_st, "rmse": rmse_op_st, "predicted_slope": -2},
            "state_trotter":   {"slope": slope_st_tr, "intercept": ic_st_tr, "rmse": rmse_st_tr, "predicted_slope": -1},
            "state_strang":    {"slope": slope_st_st, "intercept": ic_st_st, "rmse": rmse_st_st, "predicted_slope": -2},
        },
        "elapsed_s": time.time() - t0,
        "numpy_version": np.__version__,
    }
    out_dir = Path(__file__).resolve().parent.parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "trotter_strang_scaling.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n# Wrote {out_dir/'trotter_strang_scaling.json'} ({result['elapsed_s']:.1f}s)")

    # Also save log-log plot data as CSV for the report
    with open(out_dir / "err_vs_r.csv", "w") as f:
        f.write("r,op_trotter,op_strang,state_trotter,state_strang\n")
        for row in rows:
            f.write(f"{row['r']},{row['op_err_trotter']:.6e},{row['op_err_strang']:.6e},{row['state_err_trotter']:.6e},{row['state_err_strang']:.6e}\n")

if __name__ == "__main__":
    main()
