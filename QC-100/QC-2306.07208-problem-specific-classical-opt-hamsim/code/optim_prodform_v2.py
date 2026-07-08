#!/usr/bin/env python3
"""
Extended experiment for arXiv:2306.07208 replication.

Adds:
  (i)  A 5-exponential ABABA template with 5 real coefficients
       (Strang gives (1/2, 1/2, 1, 1/2, 1/2) if we substitute for one
       of the layers; here we use the standard 4th-order Yoshida structure
       ABABA with 5 coefficients as a strict same-gate-count comparison).
  (ii) The XY model on a small chain (which is what the paper uses for
       its headline >3-orders-of-magnitude claim, in section IV).
"""
from __future__ import annotations
import json, time
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

I2 = np.eye(2, dtype=complex)
X  = np.array([[0, 1],[1, 0]], dtype=complex)
Y  = np.array([[0, -1j],[1j, 0]], dtype=complex)
Z  = np.array([[1, 0],[0,-1]], dtype=complex)

def kron_list(ops):
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out

def site_op(op, i, N):
    return kron_list([op if k == i else I2 for k in range(N)])

def build_tfim(N, J=1.0, h=1.0):
    dim = 2**N
    A = np.zeros((dim, dim), dtype=complex)
    B = np.zeros((dim, dim), dtype=complex)
    for i in range(N-1):
        A += -J * (site_op(Z, i, N) @ site_op(Z, i+1, N))
    for i in range(N):
        B += -h * site_op(X, i, N)
    return A + B, A, B

def build_xy_chain(N, seed=1, Jy_center=0.5, Jz_center=1.0, hx=0.25, spread=0.25):
    """
    XY model along a chain (paper section IV uses a 3x3 XY lattice with random
    couplings). We use nearest-neighbor XY chain with random Jy,Jz around the
    paper's centers, plus X field h=0.25. Splitting: A = YY+ZZ layer, B = X layer.
    """
    rng = np.random.default_rng(seed)
    dim = 2**N
    A = np.zeros((dim, dim), dtype=complex)
    B = np.zeros((dim, dim), dtype=complex)
    for i in range(N-1):
        Jy = Jy_center + spread * (rng.random() - 0.5)
        Jz = Jz_center + spread * (rng.random() - 0.5)
        A += -Jy * (site_op(Y, i, N) @ site_op(Y, i+1, N))
        A += -Jz * (site_op(Z, i, N) @ site_op(Z, i+1, N))
    for i in range(N):
        B += -hx * site_op(X, i, N)
    return A + B, A, B

def op_norm(M):
    return np.linalg.norm(M, ord=2)

def U_exact(H, t):
    return expm(-1j * H * t)

def U_BAB(A, B, t, c):
    """3-exp BAB: exp(-i c0 B t) exp(-i c1 A t) exp(-i c2 B t)."""
    c1, c2, c3 = c
    return expm(-1j*B*(c1*t)) @ expm(-1j*A*(c2*t)) @ expm(-1j*B*(c3*t))

def U_ABABA(A, B, t, c):
    """5-exp ABABA:
       exp(-i c0 A t) exp(-i c1 B t) exp(-i c2 A t) exp(-i c3 B t) exp(-i c4 A t).
    Strang (2nd-order 3-exp BAB) has cost 3; this 5-exp form costs 5 same-type
    exponentials.  We ALSO give Strang its equivalent 5-exp form for fair
    same-gate-count comparison: applying Strang once has 3 exps; applying
    Strang twice back-to-back with midpoint merge gives 5 exps, which is
    the canonical 'BABAB' 5-exp Strang^{~2}.  We use 5-exp Strang^{~2} as
    baseline for the 5-coefficient ansatz.
    """
    c1, c2, c3, c4, c5 = c
    return (expm(-1j*A*(c1*t)) @ expm(-1j*B*(c2*t)) @ expm(-1j*A*(c3*t))
            @ expm(-1j*B*(c4*t)) @ expm(-1j*A*(c5*t)))

def U_BABAB(A, B, t, c):
    c1, c2, c3, c4, c5 = c
    return (expm(-1j*B*(c1*t)) @ expm(-1j*A*(c2*t)) @ expm(-1j*B*(c3*t))
            @ expm(-1j*A*(c4*t)) @ expm(-1j*B*(c5*t)))

def U_strang(A, B, t):
    """BAB Strang, 3 exp."""
    eB2 = expm(-1j*B*(t/2)); eA = expm(-1j*A*t)
    return eB2 @ eA @ eB2

def U_strang_5exp_via_two_halves(A, B, t):
    """Apply Strang twice with step t/2: BAB . BAB with merged middle B halves.
    Explicit form: exp(-i B t/4) exp(-i A t/2) exp(-i B t/2) exp(-i A t/2) exp(-i B t/4).
    Cost: 5 exponentials. This is a same-gate-count baseline for the 5-coeff ansatz.
    """
    tq = t/4; th = t/2
    return (expm(-1j*B*tq) @ expm(-1j*A*th) @ expm(-1j*B*th)
            @ expm(-1j*A*th) @ expm(-1j*B*tq))

# ---------- Optimizers ----------
def opt_3(A, B, t, x0=(0.5, 1.0, 0.5)):
    U_tgt = U_exact(A + B, t)
    def loss(c):
        return op_norm(U_BAB(A, B, t, c) - U_tgt)
    res = minimize(loss, x0=np.array(x0), method='Nelder-Mead',
                   options={'xatol': 1e-11, 'fatol': 1e-13, 'maxiter': 8000, 'adaptive': True})
    return res.x, float(res.fun)

def opt_5_BABAB(A, B, t, x0=(0.25, 0.5, 0.5, 0.5, 0.25)):
    """5-exp BABAB, initialized at the '2 Strang halves' baseline."""
    U_tgt = U_exact(A + B, t)
    def loss(c):
        return op_norm(U_BABAB(A, B, t, c) - U_tgt)
    # one good init (two-Strang-halves) — Nelder-Mead is enough for 5 params.
    res = minimize(loss, x0=np.array(x0), method='Nelder-Mead',
                   options={'xatol': 1e-10, 'fatol': 1e-12, 'maxiter': 4000, 'adaptive': True})
    return res.x, float(res.fun)

# ---------- Experiment ----------
def run(model_name, H_builder, N, times, out):
    H, A, B = H_builder(N)
    Hn = op_norm(H)
    rows = []
    for t in times:
        U_tgt = U_exact(H, t)
        # 3-exp
        e3_strang = op_norm(U_strang(A, B, t) - U_tgt)
        c3_opt, e3_opt = opt_3(A, B, t)
        # 5-exp same-gate-count baseline + optimized
        e5_strang = op_norm(U_strang_5exp_via_two_halves(A, B, t) - U_tgt)
        c5_opt, e5_opt = opt_5_BABAB(A, B, t)
        rows.append({
            "t": t, "t*||H||": t*Hn,
            "err_strang_3exp": e3_strang,
            "err_opt_3exp":    e3_opt,
            "ratio_3exp":      e3_strang / max(e3_opt, 1e-300),
            "c_opt_3exp":      [float(x) for x in c3_opt],
            "err_strang_5exp_twoHalves": e5_strang,
            "err_opt_5exp_BABAB":        e5_opt,
            "ratio_5exp":                e5_strang / max(e5_opt, 1e-300),
            "c_opt_5exp":                [float(x) for x in c5_opt],
        })
    result = {"model": model_name, "N": N, "||H||": Hn, "rows": rows}
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(result, f, indent=2)
    return result

def print_table(res):
    print(f"\n{res['model']}  N={res['N']}  ||H||={res['||H||']:.4f}")
    hdr = f"{'t':>6}  {'t||H||':>7}  {'e_S(3)':>10}  {'e_O(3)':>10}  {'R(3)':>6}   {'e_S(5)':>10}  {'e_O(5)':>10}  {'R(5)':>7}"
    print(hdr); print('-'*len(hdr))
    for r in res["rows"]:
        print(f"{r['t']:>6.3f}  {r['t*||H||']:>7.3f}  "
              f"{r['err_strang_3exp']:>10.3e}  {r['err_opt_3exp']:>10.3e}  {r['ratio_3exp']:>6.2f}   "
              f"{r['err_strang_5exp_twoHalves']:>10.3e}  {r['err_opt_5exp_BABAB']:>10.3e}  {r['ratio_5exp']:>7.2f}")

def main():
    outdir = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/QC-100/QC-2306.07208-problem-specific-classical-opt-hamsim/report/evidence")
    outdir.mkdir(parents=True, exist_ok=True)
    times = [0.02, 0.05, 0.1, 0.2, 0.4, 0.8]

    all_res = {}
    for name, builder, N in [
        ("TFIM_chain", build_tfim, 5),
        ("XY_random_chain", build_xy_chain, 5),
        ("XY_random_chain", build_xy_chain, 6),
    ]:
        t0 = time.time()
        r = run(name, builder, N, times, str(outdir / f"{name}_N{N}.json"))
        r["_wall_s"] = time.time() - t0
        all_res[f"{name}_N{N}"] = r
        print_table(r); print(f"[wall {r['_wall_s']:.1f}s]")

    with open(outdir / "v2_summary.json", "w") as f:
        json.dump(all_res, f, indent=2)

if __name__ == "__main__":
    main()
