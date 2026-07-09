#!/usr/bin/env python3
"""
Berry–Childs–Kothari 2015 (arXiv:1501.01715) — numerical replication
of the LCU–of–Bessel-coefficients simulation of e^{-iHt}.

Purpose
-------
The BCK algorithm constructs a truncated linear combination
   V_k = sum_{m=-k}^{k} J_m(z) U^m
where U is the quantum-walk step with eigenvalues mu_pm = e^{±i arcsin(H/(d||H||_max))},
so that
   V_k acts as e^{-iHt}  (top-left block, exactly in the k -> ∞ limit)
   z = -t * d * ||H||_max = -tau      (choice giving Theorem 1 scaling)

The Jacobi–Anger identity (paper eq. 7–9):
   e^{iz sin theta} = sum_m J_m(z) e^{i m theta}
plus mu_pm = e^{±i arcsin(H/Xd)} gives
   sum_m J_m(z) U^m|H-eigenspace = e^{-iHt}  when z = -Xdt.

The paper proves (Lemma 8 / equation 46 region) that a truncation
k = O( log(1/eps) / log log(1/eps) )
per segment is enough for per-segment error <= eps.

We check numerically that:
 (A) the truncated sum V_k, projected onto the H-eigenspace,
     reproduces e^{-iHt} on a 4-qubit sparse Hamiltonian H (XY chain, d=2)
     to error <= 1e-3 with a small k;
 (B) the required k grows as log(1/eps)/log log(1/eps) — matching Thm 1;
 (C) it uses far fewer H-applications than a Trotter step-count to reach
     the same eps.

We DO NOT implement the full quantum walk W, oblivious amplitude amp,
Kaiser-window smoothing, etc.  Instead we operate directly on the
Hamiltonian eigenspace (which is the invariant subspace that carries the
walk’s spectral relation mu_pm = e^{±i arcsin(H/Xd)}).  This is a faithful
*numerical* check of the LCU/Bessel truncation error that is the heart
of BCK's headline claim — matching the paper's own Lemma 8 error analysis.
Full LCU + oblivious amp + block-encoding on statevectors is heavier and
does not change the query-count scaling being tested.
"""
from __future__ import annotations
import json, math, sys, time
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.special import jv          # Bessel J_m

OUT = Path(__file__).parent
np.set_printoptions(precision=4, suppress=True)


# ---------- 1. Build a small sparse Hamiltonian: 4-qubit XY chain --------
def xy_chain(n_qubits: int = 4, J: float = 1.0, open_bc: bool = True) -> np.ndarray:
    """H = (J/2) sum_i (X_i X_{i+1} + Y_i Y_{i+1}).
    Row-sparsity d for XY on open chain = 2 (per row: at most one flip up + one down)."""
    dim = 1 << n_qubits
    H = np.zeros((dim, dim), dtype=complex)
    # sigma_x, sigma_y, sigma_z
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Id = np.eye(2, dtype=complex)

    def op(site: int, single: np.ndarray) -> np.ndarray:
        mats = [Id] * n_qubits
        mats[site] = single
        out = np.array([[1.0 + 0j]])
        for m in mats:
            out = np.kron(out, m)
        return out

    for i in range(n_qubits - 1):
        H += 0.5 * J * (op(i, X) @ op(i + 1, X) + op(i, Y) @ op(i + 1, Y))
    return H


def row_sparsity(H: np.ndarray, atol: float = 1e-12) -> int:
    """Max number of nonzeros in any row."""
    return int((np.abs(H) > atol).sum(axis=1).max())


# ---------- 2. LCU / Jacobi-Anger reconstruction of e^{-iHt} -------------
def bck_lcu_evolution(H: np.ndarray, t: float, k: int,
                      d: int | None = None, Hmax: float | None = None
                      ) -> np.ndarray:
    """Return V_k = sum_{m=-k}^{k} J_m(z) U^m  restricted to H-eigenspace,
    where U eigenvalues are mu_pm = e^{±i arcsin(H/(d*Hmax))} and z = -t d Hmax.
    Because the pair (mu+, mu-) gives 0.5*(mu+^m + mu-^m) = cos(m*arcsin(x))
    ( = Chebyshev T_m(sqrt(1-x^2)) after algebra; but we don't need to name it,
    we just evaluate the two-branch average, which is what shows up in the
    top-left projection of the walk after ancilla ptrace ).
    """
    if d is None:
        d = row_sparsity(H)
    if Hmax is None:
        Hmax = float(np.abs(H).max())
    Xd = d * Hmax            # normalisation used in paper (X = ||H||_max)
    z = -t * Xd              # so J_m(z) U^m gives e^{-iHt}
    evals, evecs = np.linalg.eigh(H)
    # theta such that sin(theta) = lambda / Xd   (Jacobi-Anger substitution)
    xs = evals / Xd
    xs = np.clip(xs, -1.0, 1.0)
    theta = np.arcsin(xs)                # (dim,)
    # Jacobi-Anger identity used by BCK (eq. 7-9):
    #   sum_{m=-inf}^{inf} J_m(z) e^{i m theta}  =  e^{i z sin theta}
    # For each H-eigenvalue lambda, arcsin(lambda/Xd) = theta, so sin theta = lambda/Xd,
    # and with z = -Xd*t we get e^{i z sin theta} = e^{-i lambda t}.
    # The paper's walk step U applied to the H-eigenspace has eigenvalue mu_+ = e^{+i theta}
    # (or mu_- = e^{-i theta}); each ancilla branch INDEPENDENTLY gives the correct e^{-iHt}
    # (that is the entire point of the algorithm — the answer does not depend on the branch).
    # So we should use exactly the single-branch sum, NOT average.
    dim = H.shape[0]
    Vk_diag = np.zeros(dim, dtype=complex)
    for m in range(-k, k + 1):
        Jm = jv(m, z)
        Vk_diag += Jm * np.exp(1j * m * theta)
    # Rotate back to computational basis
    Vk = (evecs * Vk_diag) @ evecs.conj().T
    return Vk


def exact_evolution(H: np.ndarray, t: float) -> np.ndarray:
    return expm(-1j * H * t)


def op_err(A: np.ndarray, B: np.ndarray) -> float:
    """Spectral-norm error ||A - B||_2."""
    return float(np.linalg.norm(A - B, ord=2))


# ---------- 3. Baseline: 2nd-order Trotter for XY chain ------------------
def trotter2_evolution(H_terms: list[np.ndarray], t: float, r: int) -> np.ndarray:
    """Second-order Trotter e^{-iHt} ≈ ( prod_j e^{-i H_j dt/2} prod_j-rev e^{-i H_j dt/2} )^r."""
    dt = t / r
    U_half = [expm(-1j * Hj * dt / 2) for Hj in H_terms]
    step = np.eye(H_terms[0].shape[0], dtype=complex)
    for Uh in U_half:
        step = Uh @ step
    for Uh in reversed(U_half):
        step = Uh @ step
    U = np.eye(H_terms[0].shape[0], dtype=complex)
    for _ in range(r):
        U = step @ U
    return U


def xy_chain_terms(n_qubits: int = 4, J: float = 1.0) -> list[np.ndarray]:
    """Nearest-neighbour bond terms — one 2-local term per bond."""
    dim = 1 << n_qubits
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Id = np.eye(2, dtype=complex)

    def op(site: int, single: np.ndarray) -> np.ndarray:
        mats = [Id] * n_qubits
        mats[site] = single
        out = np.array([[1.0 + 0j]])
        for m in mats:
            out = np.kron(out, m)
        return out

    terms = []
    for i in range(n_qubits - 1):
        terms.append(0.5 * J * (op(i, X) @ op(i + 1, X) + op(i, Y) @ op(i + 1, Y)))
    return terms


# ---------- 4. Experiments -----------------------------------------------
def experiment_A_convergence(H, t, ks):
    """V_k vs exact as k grows — expect exponential decrease then plateau."""
    U_exact = exact_evolution(H, t)
    rows = []
    for k in ks:
        Vk = bck_lcu_evolution(H, t, k)
        e = op_err(Vk, U_exact)
        rows.append({"k": int(k), "op_error": e})
    return rows


def experiment_B_scaling(H, t, eps_list):
    """For each target eps, find smallest k with err <= eps.
    Compare against paper's k ~ c * log(1/eps)/loglog(1/eps) prediction."""
    U_exact = exact_evolution(H, t)
    rows = []
    for eps in eps_list:
        for k in range(1, 400):
            Vk = bck_lcu_evolution(H, t, k)
            e = op_err(Vk, U_exact)
            if e <= eps:
                pred = math.log(1 / eps) / max(math.log(math.log(1 / eps)), 1e-9)
                rows.append({
                    "eps": eps,
                    "k_needed": int(k),
                    "achieved_error": e,
                    "log_over_loglog": pred,
                    "ratio_k_over_pred": k / pred,
                })
                break
        else:
            rows.append({"eps": eps, "k_needed": None,
                         "note": "did not converge below eps within k<=399"})
    return rows


def experiment_C_trotter_baseline(H_terms, H_full, t, eps_list):
    """Trotter query count = r * (# bond terms) [as controlled-H uses]."""
    U_exact = exact_evolution(H_full, t)
    n_terms = len(H_terms)
    rows = []
    for eps in eps_list:
        for r in range(1, 20000):
            U = trotter2_evolution(H_terms, t, r)
            e = op_err(U, U_exact)
            if e <= eps:
                rows.append({
                    "eps": eps,
                    "r_steps": r,
                    "trotter_bond_applications": r * n_terms,
                    "achieved_error": e,
                })
                break
        else:
            rows.append({"eps": eps, "r_steps": None,
                         "note": "did not converge below eps within r<=19999"})
    return rows


def main():
    t_start = time.time()

    n = 4
    H = xy_chain(n_qubits=n, J=1.0)
    H_terms = xy_chain_terms(n_qubits=n, J=1.0)
    d = row_sparsity(H)
    Hmax = float(np.abs(H).max())
    t = 1.0
    tau = d * Hmax * t

    meta = {
        "paper": "arXiv:1501.01715 (Berry, Childs, Kothari 2015)",
        "hamiltonian": f"XY chain, {n} qubits, open BC, J=1.0",
        "dim": int(H.shape[0]),
        "sparsity_d": d,
        "H_max": Hmax,
        "t": t,
        "tau": tau,
        "spectral_norm_H": float(np.linalg.norm(H, ord=2)),
    }
    print("Meta:", json.dumps(meta, indent=2))

    # ---- Experiment A: convergence of V_k with k
    ks = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]
    A_rows = experiment_A_convergence(H, t, ks)
    print("\nExperiment A — LCU convergence in k:")
    for r in A_rows:
        print(f"  k={r['k']:3d}  op_err = {r['op_error']:.3e}")

    # ---- Experiment B: k(eps) scaling vs paper's log/loglog
    eps_list = [1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-8, 1e-10]
    B_rows = experiment_B_scaling(H, t, eps_list)
    print("\nExperiment B — k needed for target eps vs paper's log(1/eps)/loglog(1/eps):")
    for r in B_rows:
        if r.get("k_needed") is not None:
            print(f"  eps={r['eps']:.0e}   k_needed={r['k_needed']:3d}   "
                  f"log/loglog≈{r['log_over_loglog']:.2f}   "
                  f"ratio={r['ratio_k_over_pred']:.2f}")
        else:
            print(f"  eps={r['eps']:.0e}   {r.get('note')}")

    # ---- Experiment C: Trotter-2 baseline for same target eps
    eps_list_C = [1e-1, 1e-2, 1e-3]
    C_rows = experiment_C_trotter_baseline(H_terms, H, t, eps_list_C)
    print("\nExperiment C — 2nd-order Trotter baseline:")
    for r in C_rows:
        if r.get("r_steps") is not None:
            print(f"  eps={r['eps']:.0e}   r={r['r_steps']:4d}   "
                  f"bond-applications={r['trotter_bond_applications']:5d}   "
                  f"achieved={r['achieved_error']:.3e}")
        else:
            print(f"  eps={r['eps']:.0e}   {r.get('note')}")

    # ---- Compare BCK vs Trotter "H-applications"
    # BCK: 1 controlled-H per segment per m in [-k,k] -> ~ (2k+1) queries per segment,
    # segments ~ O(tau) if z=O(1); for our small tau ~1.0 we use 1 segment.
    # Trotter: 1 bond application per bond per Trotter step = 2r queries for r Trotter steps and 2 bonds... just count total.
    print("\nQuery-count comparison @ eps=1e-3:")
    B_e3 = next(x for x in B_rows if x['eps'] == 1e-3 and x.get('k_needed') is not None)
    C_e3 = next(x for x in C_rows if x['eps'] == 1e-3 and x.get('r_steps') is not None)
    bck_queries = 2 * B_e3['k_needed'] + 1
    trotter_queries = C_e3['trotter_bond_applications']
    print(f"  BCK LCU:  ~{bck_queries} controlled-H queries (2k+1, k={B_e3['k_needed']})")
    print(f"  Trotter2: {trotter_queries} bond-Hamiltonian applications (r={C_e3['r_steps']})")

    result = {
        "meta": meta,
        "experiment_A_convergence": A_rows,
        "experiment_B_scaling": B_rows,
        "experiment_C_trotter": C_rows,
        "comparison_at_eps_1e-3": {
            "bck_queries_2k_plus_1": bck_queries,
            "bck_k": B_e3['k_needed'],
            "trotter_bond_applications": trotter_queries,
            "trotter_r_steps": C_e3['r_steps'],
        },
        "walltime_sec": round(time.time() - t_start, 2),
    }
    out_json = OUT / "results.json"
    out_json.write_text(json.dumps(result, indent=2, default=str))
    print(f"\nWrote {out_json}")

if __name__ == "__main__":
    main()
