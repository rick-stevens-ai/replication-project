"""
Replication of arXiv:2307.05406 (Ikeda, Kono, Fujii 2024)
"Measuring Trotter error and its application to precision-guaranteed
Hamiltonian simulations"

We reproduce the central idea:
- Model: 1D transverse-field Ising / mixed-field spin chain
    H = A + B
    A = hx * sum_j sigma^x_j
    B = sum_j (Jz * sigma^z_j sigma^z_{j+1} + hz * sigma^z_j)
  periodic BCs, Jz=-1.0, hz=0.2, hx=-2.0
  Initial state |psi_0> = fully polarized along -y

- We implement:
    T2(dt) = exp(-i A dt/2) exp(-i B dt) exp(-i A dt/2)          (2nd order symmetric)
    T4(dt) = Forest-Ruth-Suzuki 4th-order composition of T2
    True error:      eta_F(dt)   = sqrt(1 - |<psi(t+dt)|psi_2(t+dt)>|^2)
    Estimator:       eta_F^(24)  = sqrt(1 - |<psi_4(t+dt)|psi_2(t+dt)>|^2)

- Headline reproductions:
  (A) For a range of dt, verify eta_F^(24) ~ eta_F  (estimator tracks truth)
  (B) For target tolerance eps, use the estimator to pick adaptive dt at t=0
      and confirm true error <= eps
  (C) Compare adaptive dt vs dt_bound from Eq. (29):
      dt_bound = ( eps / (||[B,[B,A]]|| + 0.5 ||[A,[B,A]]||) )^(1/3)
      Paper claims ratio ~10x. We check on smaller L (tractable exact expm).

Because we do classical simulation, exact e^{-iHt} is available via scipy.linalg.expm
(dense) for L up to about 12. We use L in {6, 8} for the study.
"""

import json, os, time
import numpy as np
from scipy.linalg import expm
from scipy.sparse import csr_matrix, identity, kron
from scipy.sparse.linalg import expm_multiply

# ---------------- Pauli / operator builders --------------------------------
I2 = np.array([[1,0],[0,1]], dtype=complex)
X  = np.array([[0,1],[1,0]], dtype=complex)
Y  = np.array([[0,-1j],[1j,0]], dtype=complex)
Z  = np.array([[1,0],[0,-1]], dtype=complex)

def kron_list(mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

def single_site_op(L, j, op):
    ms = [I2]*L
    ms[j] = op
    return kron_list(ms)

def two_site_op(L, j, k, op_j, op_k):
    ms = [I2]*L
    ms[j] = op_j
    ms[k] = op_k
    return kron_list(ms)

def build_H(L, Jz=-1.0, hz=0.2, hx=-2.0, pbc=True):
    """A = hx sum sigma^x_j ; B = sum (Jz sigma^z sigma^z + hz sigma^z)"""
    dim = 2**L
    A = np.zeros((dim,dim), dtype=complex)
    B = np.zeros((dim,dim), dtype=complex)
    for j in range(L):
        A += hx * single_site_op(L, j, X)
        B += hz * single_site_op(L, j, Z)
    for j in range(L):
        k = (j+1) % L
        if not pbc and k == 0:
            continue
        B += Jz * two_site_op(L, j, k, Z, Z)
    H = A + B
    return A, B, H

def init_state_minus_y(L):
    """Fully polarized along -y: eigenstate of sigma^y with eigenvalue -1.
    sigma^y |-y> = -|-y>; the state is (|0> - i|1>)/sqrt(2)? Let's verify:
       Y = [[0,-i],[i,0]];  Y * (a,b)^T = (-i b, i a).
       For eigenvalue -1: (-i b, i a) = -(a, b) => b = -i a  (choose a=1/sqrt2)
       => state = (1, -i)/sqrt(2).  Check Y*state = (-i*(-i), i*1)/sqrt2
          = (-1, i)/sqrt2  = -(1, -i)/sqrt2  ✓
    """
    single = np.array([1, -1j], dtype=complex)/np.sqrt(2.0)
    v = single
    for _ in range(L-1):
        v = np.kron(v, single)
    return v

# ---------------- Trotter formulas ----------------------------------------

def _expmH(H, dt):
    return expm(-1j * dt * H)

def T2_operator(A, B, dt):
    """Second-order Strang / symmetric Trotter."""
    UA_half = _expmH(A, dt/2.0)
    UB      = _expmH(B, dt)
    return UA_half @ UB @ UA_half

def T4_operator(A, B, dt):
    """4th-order Forest-Ruth composition of T2, standard triple-jump:
       s = 1/(2 - 2^{1/3})
       T4(dt) = T2(s dt) T2((1-2s) dt) T2(s dt)
    (Note: the paper's Eq. 13 (FRS) is written flat over exponentials of A,B;
     this triple-jump is the algebraically equivalent standard form.)
    """
    s = 1.0 / (2.0 - 2.0**(1.0/3.0))
    return T2_operator(A,B, s*dt) @ T2_operator(A,B, (1.0-2.0*s)*dt) @ T2_operator(A,B, s*dt)

def U_exact_operator(H, dt):
    return expm(-1j * dt * H)

# ---------------- Metrics --------------------------------------------------

def infidelity_error(psi_ref, psi_approx):
    ov = np.vdot(psi_ref, psi_approx)
    val = 1.0 - abs(ov)**2
    return float(np.sqrt(max(val, 0.0)))

def true_and_estimator_error(A, B, H, psi, dt):
    """Compute
       eta_true (2nd-order T2 vs exact U):  sqrt(1 - |<psi_exact|psi_2>|^2)
       eta_est^(24) (T4 vs T2):             sqrt(1 - |<psi_4|psi_2>|^2)
    """
    U  = U_exact_operator(H, dt)
    T2 = T2_operator(A, B, dt)
    T4 = T4_operator(A, B, dt)
    psi_exact = U @ psi
    psi_2 = T2 @ psi
    psi_4 = T4 @ psi
    return infidelity_error(psi_exact, psi_2), infidelity_error(psi_4, psi_2)

# ---------------- Adaptive step-size search --------------------------------

def pick_adaptive_dt(A, B, H, psi, eps, dt0=0.5, C=0.95, max_iter=60):
    """
    Reproduce the paper's step-selection rule.
    Since eta = O(dt^3) for m=2, given a trial dt0 with measured eta(dt0),
    dt_target = C * dt0 * (eps / eta(dt0))^{1/3}.
    We iterate a few times (recompute eta at proposed dt, then adjust).
    Returns final dt and the true & estimator error at that dt.
    """
    dt = dt0
    hist = []
    for it in range(max_iter):
        eta_true, eta_est = true_and_estimator_error(A, B, H, psi, dt)
        hist.append((dt, eta_est, eta_true))
        if eta_est <= 0:
            break
        # scale toward target using cube-root (m+1 = 3)
        dt_new = C * dt * (eps / eta_est)**(1.0/3.0)
        # convergence when relative move is small
        if abs(dt_new - dt) / max(dt, 1e-30) < 1e-3:
            dt = dt_new
            break
        dt = dt_new
    eta_true, eta_est = true_and_estimator_error(A, B, H, psi, dt)
    hist.append((dt, eta_est, eta_true))
    return dt, eta_est, eta_true, hist

# ---------------- dt_bound from Eq.(29) ------------------------------------

def op_norm(M):
    # spectral norm
    return float(np.linalg.norm(M, ord=2))

def dt_bound(A, B, eps):
    """dt_bound = (eps / (||[B,[B,A]]|| + 0.5 ||[A,[B,A]]||))^{1/3}"""
    BA = B @ A - A @ B
    BBA = B @ BA - BA @ B
    ABA = A @ BA - BA @ A
    denom = op_norm(BBA) + 0.5 * op_norm(ABA)
    return (eps / denom) ** (1.0/3.0), denom

# ---------------- Main experiment ------------------------------------------

def scan_experiment(L=6, dts=None, outdir="."):
    print(f"[scan] L={L}")
    A, B, H = build_H(L)
    psi = init_state_minus_y(L)
    # sanity
    from numpy.linalg import eigh
    _ = None
    if dts is None:
        dts = np.geomspace(0.01, 0.4, 12)
    rows = []
    for dt in dts:
        et, ee = true_and_estimator_error(A, B, H, psi, dt)
        rows.append({"dt": float(dt), "eta_true": et, "eta_est_24": ee,
                     "ratio": (ee/et if et > 0 else None)})
        print(f"  dt={dt:.4f}  eta_true={et:.3e}  eta_est24={ee:.3e}  ratio={rows[-1]['ratio']}")
    return rows

def adaptive_experiment(L=6, epss=(1e-3, 10**(-1.5), 1e-2), outdir="."):
    print(f"[adaptive] L={L}")
    A, B, H = build_H(L)
    psi = init_state_minus_y(L)
    rows = []
    for eps in epss:
        dt_star, eta_est, eta_true, hist = pick_adaptive_dt(A, B, H, psi, eps, dt0=0.4, C=0.95)
        dt_b, denom = dt_bound(A, B, eps)
        ratio = dt_star / dt_b
        row = {"eps": float(eps),
               "dt_adapt": float(dt_star),
               "eta_est_at_dt": float(eta_est),
               "eta_true_at_dt": float(eta_true),
               "meets_tolerance": bool(eta_true <= eps),
               "dt_bound": float(dt_b),
               "bound_denom_norm": float(denom),
               "ratio_dt_adapt_over_bound": float(ratio),
               "iterations": len(hist)}
        rows.append(row)
        print(f"  eps={eps:.3e}  dt_adapt={dt_star:.4f}  dt_bound={dt_b:.4f}  "
              f"ratio={ratio:.2f}  eta_true={eta_true:.3e}  meets={row['meets_tolerance']}")
    return rows

if __name__ == "__main__":
    outdir = os.path.dirname(os.path.abspath(__file__))
    t0 = time.time()

    result = {"paper": "arXiv:2307.05406",
              "model": {"type":"1D mixed-field Ising (TFIM+longitudinal)",
                        "Jz": -1.0, "hz": 0.2, "hx": -2.0,
                        "boundary": "periodic",
                        "initial_state": "fully polarized -y"}}

    # (A) estimator-vs-truth scan on L=6 and L=8
    result["scan_L6"] = scan_experiment(L=6)
    result["scan_L8"] = scan_experiment(L=8)

    # (B) & (C) adaptive step size vs tolerance / vs dt_bound on L=6 and L=8
    result["adaptive_L6"] = adaptive_experiment(L=6)
    result["adaptive_L8"] = adaptive_experiment(L=8)

    result["runtime_sec"] = time.time() - t0

    outpath = os.path.join(outdir, "trotter24_results.json")
    with open(outpath, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n[saved] {outpath}   (runtime {result['runtime_sec']:.1f}s)")
