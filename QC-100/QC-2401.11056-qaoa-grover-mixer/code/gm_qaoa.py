"""
Independent replication of key numerical claims from:
  Bridi & Marquezino, "Analytical results for the QAOA with Grover Mixer",
  arXiv:2401.11056v3 (2024).

Reproduced claims:
  C1  Permutation invariance of Grover-Mixer QAOA (GM-QAOA):
      <C>_GM depends only on the spectrum (distribution of cost values),
      not on which bitstring holds which value.
  C2  Standard transverse-field (X-mixer) QAOA is NOT permutation-invariant.
  C3  Grover-binary closed form: for a binary cost with marked-state ratio
      rho <= rho_Th(r) = sin^2(pi/(4r+2)), the optimal probability of
      measuring a marked element is
              P(rho, r) = sin^2( (2r+1) * arcsin(sqrt(rho)) )
      matches a real GM-QAOA statevector simulation with all angles = pi.
  C4  Approximation-ratio comparison of X-mixer QAOA vs GM-QAOA on MAX-CUT
      for a small graph at p = 1, 2, 3 (numerical optimization).

Implementation: pure statevector, numpy only (Qiskit is installed but for a
small independent numerical check we build the two unitaries by hand — this
also makes the permutation experiment trivial and unambiguous). No fabricated
results: every number in results.json comes from actually diagonalising /
evolving the state.
"""

from __future__ import annotations
import json
import math
import time
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

RNG = np.random.default_rng(20260703)

# ---------------------------------------------------------------------------
# Basic MAX-CUT setup
# ---------------------------------------------------------------------------

def maxcut_costs(n: int, edges: list[tuple[int, int]]) -> np.ndarray:
    """C(x) = number of edges cut by bitstring x  (length 2^n, index = int(x))."""
    N = 1 << n
    C = np.zeros(N, dtype=np.float64)
    for i, j in edges:
        # For each bitstring, edge (i,j) is cut iff bit_i != bit_j
        for x in range(N):
            bi = (x >> i) & 1
            bj = (x >> j) & 1
            if bi != bj:
                C[x] += 1.0
    return C


# ---------------------------------------------------------------------------
# X-mixer (standard QAOA)
# ---------------------------------------------------------------------------

def apply_cost_phase(state: np.ndarray, C: np.ndarray, gamma: float) -> np.ndarray:
    """U_C(gamma) = exp(-i * gamma * C).  C is diagonal in comp basis."""
    return np.exp(-1j * gamma * C) * state


def apply_x_mixer(state: np.ndarray, n: int, beta: float) -> np.ndarray:
    """U_B(beta) = exp(-i * beta * sum_i X_i) = tensor_i exp(-i beta X_i).
    Each single-qubit U = cos(beta) I - i sin(beta) X, acting on qubit i."""
    c = math.cos(beta)
    s = math.sin(beta)
    N = state.shape[0]
    out = state.copy()
    for i in range(n):
        # apply single-qubit gate on qubit i
        mask = 1 << i
        idx0 = np.array([k for k in range(N) if (k & mask) == 0])
        idx1 = idx0 | mask
        a0 = out[idx0]
        a1 = out[idx1]
        out[idx0] = c * a0 - 1j * s * a1
        out[idx1] = -1j * s * a0 + c * a1
    return out


def qaoa_x_expectation(n: int, C: np.ndarray, betas: np.ndarray, gammas: np.ndarray) -> float:
    """<C> for standard X-mixer QAOA with p rounds."""
    N = 1 << n
    psi = np.ones(N, dtype=np.complex128) / math.sqrt(N)
    for beta, gamma in zip(betas, gammas):
        psi = apply_cost_phase(psi, C, gamma)
        psi = apply_x_mixer(psi, n, beta)
    probs = np.abs(psi) ** 2
    return float(np.dot(probs, C))


# ---------------------------------------------------------------------------
# Grover mixer
# ---------------------------------------------------------------------------

def apply_grover_mixer(state: np.ndarray, beta: float) -> np.ndarray:
    """U_GM(beta) = exp(-i * beta * |s><s|), where |s> = uniform superposition.
    |s><s| is a rank-1 projector, so
        U_GM = I + (e^{-i beta} - 1) |s><s|.
    """
    N = state.shape[0]
    s = np.ones(N, dtype=np.complex128) / math.sqrt(N)
    overlap = np.vdot(s, state)          # <s|psi>
    factor = np.exp(-1j * beta) - 1.0
    return state + factor * overlap * s


def qaoa_gm_expectation(n: int, C: np.ndarray, betas: np.ndarray, gammas: np.ndarray) -> float:
    """<C> for GM-QAOA with p rounds. Cost operator is diagonal(C)."""
    N = 1 << n
    psi = np.ones(N, dtype=np.complex128) / math.sqrt(N)
    for beta, gamma in zip(betas, gammas):
        psi = apply_cost_phase(psi, C, gamma)
        psi = apply_grover_mixer(psi, beta)
    probs = np.abs(psi) ** 2
    return float(np.dot(probs, C))


def gm_marked_prob(n: int, C: np.ndarray, betas: np.ndarray, gammas: np.ndarray,
                   marked_value: float) -> float:
    """Prob of measuring any state with C(x) == marked_value under GM-QAOA."""
    N = 1 << n
    psi = np.ones(N, dtype=np.complex128) / math.sqrt(N)
    for beta, gamma in zip(betas, gammas):
        psi = apply_cost_phase(psi, C, gamma)
        psi = apply_grover_mixer(psi, beta)
    probs = np.abs(psi) ** 2
    return float(np.sum(probs[C == marked_value]))


# ---------------------------------------------------------------------------
# Optimization helpers
# ---------------------------------------------------------------------------

def optimize_params(n, C, p, mixer, n_restarts=25, seed=0):
    """Minimize <C> for MAX-CUT means MAXIMIZING cut, so we minimize -<C>."""
    rng = np.random.default_rng(seed)
    if mixer == "x":
        expect = qaoa_x_expectation
    elif mixer == "gm":
        expect = qaoa_gm_expectation
    else:
        raise ValueError(mixer)

    def neg_obj(theta):
        betas = theta[:p]
        gammas = theta[p:]
        return -expect(n, C, betas, gammas)

    best_val = -np.inf
    best_x = None
    for _ in range(n_restarts):
        # X-mixer betas ~ (0, pi), gammas ~ (0, 2*pi).  For GM: both ~ (0, 2*pi).
        if mixer == "x":
            x0 = np.concatenate([rng.uniform(0, math.pi, p),
                                 rng.uniform(0, 2 * math.pi, p)])
        else:
            x0 = rng.uniform(0, 2 * math.pi, 2 * p)
        res = minimize(neg_obj, x0, method="COBYLA",
                       options={"maxiter": 400, "rhobeg": 0.3, "disp": False})
        if -res.fun > best_val:
            best_val = float(-res.fun)
            best_x = res.x
    return best_val, best_x


# ---------------------------------------------------------------------------
# EXPERIMENT 1: permutation invariance of GM-QAOA (C1)
#              & non-invariance of X-mixer QAOA (C2)
# ---------------------------------------------------------------------------

def experiment_permutation_invariance(n: int, C: np.ndarray, betas: np.ndarray,
                                      gammas: np.ndarray, n_perms: int = 8,
                                      rng: np.random.Generator = RNG):
    """For random permutations pi of [0, 2^n), compare <C>_M with <C_pi>_M
    where C_pi[x] = C[pi(x)]. GM-QAOA must give the same value; X-mixer will
    (generically) not."""
    N = 1 << n
    base_gm = qaoa_gm_expectation(n, C, betas, gammas)
    base_x = qaoa_x_expectation(n, C, betas, gammas)

    gm_vals = [base_gm]
    x_vals = [base_x]
    perms_used = []
    for _ in range(n_perms):
        perm = rng.permutation(N)
        C_perm = C[perm]
        gm_vals.append(qaoa_gm_expectation(n, C_perm, betas, gammas))
        x_vals.append(qaoa_x_expectation(n, C_perm, betas, gammas))
        perms_used.append(perm.tolist())

    gm_arr = np.array(gm_vals)
    x_arr = np.array(x_vals)

    return {
        "n_qubits": n,
        "n_permutations_tested": n_perms + 1,   # including identity
        "betas": betas.tolist(),
        "gammas": gammas.tolist(),
        "gm_expectations": gm_vals,
        "x_expectations": x_vals,
        "gm_max_dev_from_identity": float(np.max(np.abs(gm_arr - base_gm))),
        "x_max_dev_from_identity": float(np.max(np.abs(x_arr - base_x))),
        "gm_std": float(np.std(gm_arr)),
        "x_std": float(np.std(x_arr)),
    }


# ---------------------------------------------------------------------------
# EXPERIMENT 2: Grover-binary closed form (C3, Eq. (8) of paper)
# ---------------------------------------------------------------------------

def experiment_grover_binary_formula(n: int = 6, rounds: list[int] = (1, 2, 3, 4)):
    """For binary cost c(x) = -1 for marked, 0 otherwise, verify that
       GM-QAOA with beta_j = gamma_j = pi (all j) matches
       P(rho, r) = sin^2((2r+1) arcsin(sqrt(rho)))   for rho <= rho_Th(r).
    """
    N = 1 << n
    results = []
    for r in rounds:
        rho_th = math.sin(math.pi / (4 * r + 2)) ** 2
        # pick a marked-fraction rho <= rho_th and >= 1/N
        # Choose k such that k/N <= rho_th
        max_k = max(1, int(math.floor(rho_th * N)))
        k = min(max_k, N - 1)
        rho = k / N
        # build cost function: marked -> -1, else 0
        # place marked at first k indices (permutation-invariant anyway)
        C = np.zeros(N, dtype=np.float64)
        C[:k] = -1.0
        betas = np.full(r, math.pi)
        gammas = np.full(r, math.pi)
        # measured probability of marked state:
        p_meas = gm_marked_prob(n, C, betas, gammas, marked_value=-1.0)
        p_pred = math.sin((2 * r + 1) * math.asin(math.sqrt(rho))) ** 2
        results.append({
            "r": r,
            "rho": rho,
            "k_marked": k,
            "N": N,
            "rho_Th_r": rho_th,
            "P_measured": p_meas,
            "P_predicted_eq8": p_pred,
            "abs_diff": abs(p_meas - p_pred),
        })
    return results


# ---------------------------------------------------------------------------
# EXPERIMENT 3: approximation-ratio comparison, MAX-CUT (C4)
# ---------------------------------------------------------------------------

def experiment_max_cut(edges: list[tuple[int, int]], n: int,
                       depths: list[int] = (1, 2, 3), n_restarts: int = 30):
    C = maxcut_costs(n, edges)
    cmax = float(np.max(C))
    cmin = float(np.min(C))
    # uniform-random baseline expected cut = mean of C
    uniform_expect = float(np.mean(C))
    uniform_ratio = uniform_expect / cmax

    results = []
    for p in depths:
        gm_val, gm_x = optimize_params(n, C, p, "gm",
                                       n_restarts=n_restarts, seed=42 + p)
        xm_val, xm_x = optimize_params(n, C, p, "x",
                                       n_restarts=n_restarts, seed=1000 + p)
        results.append({
            "p": p,
            "gm_expect": gm_val,
            "gm_ratio": gm_val / cmax,
            "gm_params": gm_x.tolist(),
            "x_expect": xm_val,
            "x_ratio": xm_val / cmax,
            "x_params": xm_x.tolist(),
        })
    return {
        "n": n,
        "edges": edges,
        "cost_max": cmax,
        "cost_min": cmin,
        "uniform_random_expect": uniform_expect,
        "uniform_random_ratio": uniform_ratio,
        "by_depth": results,
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    out_dir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_results = {"meta": {}}

    # Small graph for X-mixer feasibility: 6 qubits, ring + 2 chord = triangle-free-ish
    n = 6
    edges_ring6 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
    edges_extra = edges_ring6 + [(0, 3), (1, 4)]  # 6-node graph with 8 edges
    C = maxcut_costs(n, edges_extra)

    # --- Experiment 1: permutation invariance at random-but-fixed angles
    print("[EXP1] Permutation invariance (n=6)...")
    betas1 = np.array([0.7, 1.3])
    gammas1 = np.array([0.4, 1.1])
    exp1 = experiment_permutation_invariance(n, C, betas1, gammas1,
                                             n_perms=12, rng=RNG)
    exp1["graph_edges"] = edges_extra
    all_results["experiment_1_permutation_invariance"] = exp1
    print(f"       GM max |dev| from identity : {exp1['gm_max_dev_from_identity']:.3e}")
    print(f"       X-mixer max |dev|          : {exp1['x_max_dev_from_identity']:.3e}")

    # Second permutation test at DIFFERENT depth (p=1, then p=3) and different graph
    n2 = 5
    edges5 = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 2), (1, 3), (0, 4)]
    C2 = maxcut_costs(n2, edges5)
    exp1b = experiment_permutation_invariance(n2, C2, np.array([0.55, 0.90, 1.25]),
                                              np.array([0.20, 0.75, 1.10]),
                                              n_perms=8, rng=RNG)
    exp1b["graph_edges"] = edges5
    all_results["experiment_1b_permutation_invariance_p3_n5"] = exp1b
    print(f"       (n=5,p=3) GM max |dev|     : {exp1b['gm_max_dev_from_identity']:.3e}")
    print(f"       (n=5,p=3) X-mixer max |dev|: {exp1b['x_max_dev_from_identity']:.3e}")

    # --- Experiment 2: Grover-binary closed form
    print("[EXP2] Grover-binary Eq. (8) formula check (n=6, r=1..4)...")
    exp2 = experiment_grover_binary_formula(n=6, rounds=[1, 2, 3, 4])
    all_results["experiment_2_grover_binary_formula"] = exp2
    for row in exp2:
        print(f"       r={row['r']}  rho={row['rho']:.5f}  "
              f"P_meas={row['P_measured']:.6f}  P_eq8={row['P_predicted_eq8']:.6f}  "
              f"|diff|={row['abs_diff']:.2e}")

    # --- Experiment 3: MAX-CUT approximation ratio, X vs GM at p=1,2,3
    print("[EXP3] MAX-CUT approx ratios, X-mixer vs GM-QAOA (n=6, p=1..3)...")
    exp3 = experiment_max_cut(edges_extra, n=n, depths=[1, 2, 3], n_restarts=40)
    all_results["experiment_3_max_cut_ratios"] = exp3
    for row in exp3["by_depth"]:
        print(f"       p={row['p']}  GM ratio={row['gm_ratio']:.4f}  "
              f"X-mixer ratio={row['x_ratio']:.4f}  (cost_max={exp3['cost_max']}, "
              f"uniform={exp3['uniform_random_ratio']:.4f})")

    all_results["meta"] = {
        "script": "code/gm_qaoa.py",
        "seconds_elapsed": round(time.time() - t0, 2),
        "numpy_version": np.__version__,
        "scipy_note": "scipy.optimize.minimize (COBYLA)",
        "notes": (
            "Pure numpy statevector simulator, no shot noise; costs computed as "
            "exact <psi|C|psi>. Grover mixer implemented from its rank-1 form "
            "U_GM(beta) = I + (e^{-i beta}-1)|s><s|. X-mixer implemented as "
            "product of single-qubit exp(-i beta X)."
        ),
    }

    out_json = out_dir / "results.json"
    out_json.write_text(json.dumps(all_results, indent=2))
    print(f"\nWrote {out_json}  ({out_json.stat().st_size} bytes)  "
          f"elapsed {all_results['meta']['seconds_elapsed']}s")


if __name__ == "__main__":
    main()
