#!/usr/bin/env python3
"""
Reproducible core of arXiv:2306.07208 (Mansuroglu, Fischer, Hartmann):
"Problem specific classical optimization of Hamiltonian simulation".

Headline claim we test:
  For a small model Hamiltonian, a *classically optimized* product formula
  with the SAME number of exponentials as a standard 2nd-order Trotter/Strang
  splitting achieves a lower unitary-error ||U_approx(t) - exp(-i H t)||
  than the standard splitting, at short times.

Model:
  Transverse-Field Ising Model (TFIM) on N sites, open boundary:
      H = A + B
      A = -J * sum_i Z_i Z_{i+1}          (ZZ layer)
      B = -h * sum_i X_i                  (X layer)

Baseline (2nd-order Trotter / Strang):
      U_S(t) = exp(-i (B/2) t) exp(-i A t) exp(-i (B/2) t)
  cost = 3 exponentials of the A/B "chunks".

Optimized product formula (SAME number of exponentials, 3):
      U_opt(t) = exp(-i c1 B t) exp(-i c2 A t) exp(-i c3 B t)
  with (c1, c2, c3) real, classically optimized to minimize spectral norm
  ||U_opt(t) - exp(-i H t)||_2 at a chosen problem-specific time t.
  Strang corresponds to (0.5, 1.0, 0.5); we let a classical optimizer
  find better coefficients for THIS problem instance.

Then we ALSO test a K-fold repeated sequence at K*t total time to check
whether the problem-specific optimum keeps its edge (extrapolation
similar in spirit to Fig. 3 of the paper, but on TFIM instead of XY —
TFIM is the model the paper analyses in Appendix B).

Everything is exact matrix arithmetic — no fabricated numbers.
"""
from __future__ import annotations
import json, os, sys, time, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

# ---------- Hamiltonian ----------
I2 = np.eye(2, dtype=complex)
X  = np.array([[0, 1],[1, 0]], dtype=complex)
Z  = np.array([[1, 0],[0,-1]], dtype=complex)

def kron_list(ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out

def site_op(op, i, N):
    return kron_list([op if k == i else I2 for k in range(N)])

def build_tfim(N, J=1.0, h=1.0):
    """Return (H, A, B) where H = A + B, A = ZZ layer, B = X layer."""
    dim = 2**N
    A = np.zeros((dim, dim), dtype=complex)
    B = np.zeros((dim, dim), dtype=complex)
    for i in range(N-1):
        A += -J * (site_op(Z, i, N) @ site_op(Z, i+1, N))
    for i in range(N):
        B += -h * site_op(X, i, N)
    return A + B, A, B

def op_norm(M):
    # spectral (2-)norm
    return np.linalg.norm(M, ord=2)

# ---------- Product formulas ----------
def U_exact(H, t):
    return expm(-1j * H * t)

def U_strang(A, B, t):
    """Standard 2nd-order Trotter (BAB): exp(-i B t/2) exp(-i A t) exp(-i B t/2)."""
    eB2 = expm(-1j * B * (t/2.0))
    eA  = expm(-1j * A * t)
    return eB2 @ eA @ eB2

def U_paramBAB(A, B, t, c):
    """3-exponential BAB template: exp(-i c0 B t) exp(-i c1 A t) exp(-i c2 B t).

    Strang corresponds to c=(0.5, 1.0, 0.5).
    """
    c1, c2, c3 = c
    eB1 = expm(-1j * B * (c1 * t))
    eA  = expm(-1j * A * (c2 * t))
    eB2 = expm(-1j * B * (c3 * t))
    return eB1 @ eA @ eB2

# ---------- Optimization ----------
def opt_coeffs(A, B, t, x0=(0.5, 1.0, 0.5)):
    """Classically optimize c=(c1,c2,c3) to minimize ||U_paramBAB - U_exact||_2."""
    U_tgt = U_exact(A + B, t)
    def loss(c):
        Uv = U_paramBAB(A, B, t, c)
        return op_norm(Uv - U_tgt)
    # BFGS-family works fine here (small, smooth).
    res = minimize(loss, x0=np.array(x0, dtype=float),
                   method='Nelder-Mead',
                   options={'xatol': 1e-10, 'fatol': 1e-12, 'maxiter': 5000, 'adaptive': True})
    return res.x, float(res.fun), res

# ---------- Repeated sequences ----------
def U_repeat(builder, K):
    """Given single-step unitary builder() -> matrix, return builder()^K.

    Equivalent to K-fold repetition of the same short step.
    """
    U1 = builder()
    Uk = np.eye(U1.shape[0], dtype=complex)
    for _ in range(K):
        Uk = Uk @ U1
    return Uk

# ---------- Experiments ----------
def experiment(N=4, J=1.0, h=1.0, times=None, K_extrap=None, out=None, seed=0):
    if times is None:
        # short-time regime is exactly the regime the paper claims >3 orders of magnitude
        times = [0.02, 0.05, 0.1, 0.2, 0.4, 0.8]
    if K_extrap is None:
        K_extrap = [1, 2, 4, 8]

    np.random.seed(seed)
    H, A, B = build_tfim(N, J=J, h=h)
    Hn = op_norm(H)

    rows = []
    for t in times:
        U_tgt = U_exact(H, t)
        # baseline: Strang at this t
        U_s = U_strang(A, B, t)
        err_strang = op_norm(U_s - U_tgt)
        # optimized: 3-exp BAB, initialized at Strang, optimized for THIS (H, t)
        c_opt, err_opt, _res = opt_coeffs(A, B, t)
        ratio = err_strang / max(err_opt, 1e-300)
        rows.append({
            "N": N, "J": J, "h": h, "t": t, "||H||": Hn, "t*||H||": t*Hn,
            "n_exp": 3,
            "err_strang": err_strang,
            "err_opt": err_opt,
            "ratio_err_strang_over_err_opt": ratio,
            "c_opt": [float(x) for x in c_opt],
            "delta_from_strang": [float(c_opt[0]-0.5), float(c_opt[1]-1.0), float(c_opt[2]-0.5)],
        })

    # Extrapolation: pick the middle time, optimize once at that step,
    # then repeat the same 3-exp sequence K times; compare to full Trotter
    # sequence repeated K times.
    t_ref = 0.1
    c_opt_ref, err_opt_ref, _ = opt_coeffs(A, B, t_ref)
    extrap = []
    for K in K_extrap:
        T = K * t_ref
        U_tgt_T = U_exact(H, T)
        U_s_T = U_repeat(lambda: U_strang(A, B, t_ref), K)
        U_o_T = U_repeat(lambda: U_paramBAB(A, B, t_ref, c_opt_ref), K)
        err_s = op_norm(U_s_T - U_tgt_T)
        err_o = op_norm(U_o_T - U_tgt_T)
        extrap.append({
            "K": K, "t_ref": t_ref, "T_total": T,
            "err_strang_repK": err_s,
            "err_opt_repK": err_o,
            "ratio_repK": err_s / max(err_o, 1e-300),
        })

    result = {
        "model": "TFIM",
        "N": N, "J": J, "h": h,
        "||H||": Hn,
        "note": "Both formulas use identical 3-exponential BAB template; only the 3 real coefficients differ (Strang=(1/2,1,1/2) vs classically optimized). Cost/gate-count is IDENTICAL.",
        "single_step_scan": rows,
        "extrapolation_repeatedK_at_t_ref": {"c_opt_at_t_ref": [float(x) for x in c_opt_ref], "table": extrap},
    }
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as f:
            json.dump(result, f, indent=2)
    return result

def main():
    outdir = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2306.07208-problem-specific-classical-opt-hamsim/report/evidence")
    outdir.mkdir(parents=True, exist_ok=True)
    all_res = {}
    for N in (4, 5, 6):
        t0 = time.time()
        r = experiment(N=N, J=1.0, h=1.0,
                       out=str(outdir / f"tfim_N{N}.json"))
        r["_wall_s"] = time.time() - t0
        all_res[f"N={N}"] = r
        print(f"[N={N}] ||H||={r['||H||']:.4f}   wall={r['_wall_s']:.1f}s")
        print(f"{'t':>7}  {'t||H||':>7}  {'err_strang':>12}  {'err_opt':>12}  {'ratio':>9}  {'c_opt':>28}")
        for row in r["single_step_scan"]:
            print(f"{row['t']:>7.3f}  {row['t*||H||']:>7.3f}  {row['err_strang']:>12.3e}  {row['err_opt']:>12.3e}  {row['ratio_err_strang_over_err_opt']:>9.2e}  {['%.5f' % x for x in row['c_opt']]}")
        print("  Extrapolation @ t_ref=0.1 (repeat K):")
        for row in r["extrapolation_repeatedK_at_t_ref"]["table"]:
            print(f"    K={row['K']:>2d}  T={row['T_total']:>4.2f}  err_S={row['err_strang_repK']:>10.3e}  err_O={row['err_opt_repK']:>10.3e}  ratio={row['ratio_repK']:>7.2e}")
        print()

    with open(outdir / "tfim_summary.json", "w") as f:
        json.dump(all_res, f, indent=2)
    print(f"Wrote evidence to {outdir}")

if __name__ == "__main__":
    main()
