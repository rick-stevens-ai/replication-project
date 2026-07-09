#!/usr/bin/env python3
"""
Independent replication of Wootters (1998) entanglement of formation formula
for arbitrary 2-qubit density matrices.

Reference: W. K. Wootters, "Entanglement of Formation of an Arbitrary State
of Two Qubits," Phys. Rev. Lett. 80, 2245 (1998); arXiv:quant-ph/9709029.

Central formula (paper eqs. 1-3, and unnumbered "spin-flip"/eigenvalue eqs):

  E(rho) = h( (1 + sqrt(1 - C^2)) / 2 )                                (Wootters eq. after eq. 6)
  h(x)   = -x log_2 x - (1 - x) log_2 (1 - x)                          (binary entropy)
  C(rho) = max(0, lambda_1 - lambda_2 - lambda_3 - lambda_4)           (concurrence)
  where lambda_i are the sqrt of eigenvalues of R = rho * rho_tilde   in decreasing order
  (equivalently, eigenvalues of sqrt(sqrt(rho) rho_tilde sqrt(rho))),
  and rho_tilde = (sigma_y ⊗ sigma_y) rho^* (sigma_y ⊗ sigma_y).
"""

from __future__ import annotations
import json
import os
import sys
import numpy as np
from numpy.random import default_rng

# --- Pauli Y matrix and its two-qubit flip operator ---
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
YY = np.kron(sigma_y, sigma_y)


def binary_entropy(x: float) -> float:
    """h(x) = -x log2 x - (1-x) log2(1-x); h(0)=h(1)=0 by convention."""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * np.log2(x) - (1.0 - x) * np.log2(1.0 - x)


def concurrence(rho: np.ndarray) -> float:
    """Wootters concurrence for a 2-qubit density matrix rho (4x4, complex)."""
    assert rho.shape == (4, 4), "rho must be 4x4"
    rho_tilde = YY @ rho.conj() @ YY
    # R = rho * rho_tilde is not Hermitian in general, but its eigenvalues are
    # nonnegative real. Wootters shows the sqrt of these eigenvalues are the
    # singular values of sqrt(rho) sqrt(rho_tilde) ordering.
    R = rho @ rho_tilde
    eigvals = np.linalg.eigvals(R)
    # Numerical eigenvalues may have tiny imaginary parts; take real, clip >=0.
    eigvals = np.real(eigvals)
    eigvals = np.clip(eigvals, 0.0, None)
    sqrt_eigs = np.sqrt(np.sort(eigvals)[::-1])  # descending order
    C = max(0.0, sqrt_eigs[0] - sqrt_eigs[1] - sqrt_eigs[2] - sqrt_eigs[3])
    return float(C)


def entanglement_of_formation(rho: np.ndarray) -> float:
    """E(rho) = h( (1 + sqrt(1 - C^2)) / 2 )."""
    C = concurrence(rho)
    C = min(max(C, 0.0), 1.0)  # numerical safety
    x = 0.5 * (1.0 + np.sqrt(max(0.0, 1.0 - C * C)))
    return binary_entropy(x)


# --- Reference states ---
def ket(bits: str) -> np.ndarray:
    """2-qubit computational basis ket, e.g. ket('01')."""
    v = np.zeros(4, dtype=complex)
    idx = int(bits, 2)
    v[idx] = 1.0
    return v


def density(psi: np.ndarray) -> np.ndarray:
    psi = psi / np.linalg.norm(psi)
    return np.outer(psi, psi.conj())


def bell_phi_plus() -> np.ndarray:
    v = (ket("00") + ket("11")) / np.sqrt(2)
    return density(v)


def bell_psi_minus() -> np.ndarray:
    v = (ket("01") - ket("10")) / np.sqrt(2)
    return density(v)


def product_00() -> np.ndarray:
    return density(ket("00"))


def werner_state(p: float) -> np.ndarray:
    """rho_W(p) = p |Phi+><Phi+| + (1-p)/4 * I  (Werner-like with Bell mixed w/ max mixed).
    Note: separability threshold via PPT is p <= 1/3 for this parametrization."""
    return p * bell_phi_plus() + (1.0 - p) / 4.0 * np.eye(4, dtype=complex)


# --- Random 2-qubit mixed states via purification (partial trace of 4-qubit pure state) ---
def random_2qubit_mixed(rng: np.random.Generator) -> np.ndarray:
    """Sample a random 2-qubit density matrix by tracing out a random 2-qubit
    ancilla from a Haar-random 4-qubit pure state (dim 16)."""
    dim = 16  # 4 qubits total: system(2) + ancilla(2)
    # Haar-random complex vector
    v = rng.standard_normal(dim) + 1j * rng.standard_normal(dim)
    v = v / np.linalg.norm(v)
    # Reshape to (d_sys=4, d_env=4) and take rho_sys = V V^dagger where V=v.reshape(4,4)
    V = v.reshape(4, 4)
    rho = V @ V.conj().T
    # Ensure Hermitian, trace 1
    rho = 0.5 * (rho + rho.conj().T)
    rho = rho / np.trace(rho).real
    return rho


# --- Brute-force numerical E via random pure-state decompositions (upper bound) ---
def brute_force_ef_upper_bound(rho: np.ndarray,
                               rng: np.random.Generator,
                               n_decomps: int = 200,
                               ensemble_size: int = 4) -> float:
    """Empirical UPPER BOUND on E(rho) by sampling many random pure-state
    decompositions of rho and computing avg pure-state entanglement.

    Uses the Schrödinger-HJW theorem: any decomposition of rho with K pure
    states can be written as p_i = |<phi_i|psi_i>|^2 with |psi_i> = U_ij sqrt(w_j) |e_j>
    where rho = sum_j w_j |e_j><e_j| is the eigendecomposition and U is unitary K x r.

    Since E is convex, this gives an upper bound; the min over many samples
    should approach E_F(rho) for small systems.
    """
    # Eigendecomposition of rho (eigh returns ASCENDING; reverse for descending)
    w, V = np.linalg.eigh(rho)
    w = np.clip(np.real(w), 0.0, None)
    w = w / w.sum()
    order = np.argsort(w)[::-1]
    w = w[order]; V = V[:, order]
    r = int(np.sum(w > 1e-12))  # rank
    # Assemble sqrt(w_j) |e_j> for the r nonzero eigenmodes
    sqrtw_e = V[:, :r] * np.sqrt(w[:r])[None, :]  # 4 x r

    K = max(ensemble_size, r)
    best_avg_E = np.inf
    for _ in range(n_decomps):
        # random K x r isometry (columns orthonormal): take Haar-random unitary K x K, keep first r cols
        A = rng.standard_normal((K, K)) + 1j * rng.standard_normal((K, K))
        Q, _ = np.linalg.qr(A)
        U = Q[:, :r]  # K x r isometry (U^dagger U = I_r)
        # states |psi_i> (unnormalized): sqrtw_e @ U[i,:].conj()  ... wait, need proper HJW form
        # HJW: |phi_i> (unnormalized, sqrt(p_i)|psi_i>) = sum_j U_{ij} sqrt(w_j) |e_j>
        #    = (sqrtw_e @ U.T)[:, i]  -- careful with conjugation convention
        phi = sqrtw_e @ U.T  # shape (4, K); column i is unnormalized state
        avg_E = 0.0
        for i in range(K):
            col = phi[:, i]
            p_i = np.vdot(col, col).real
            if p_i < 1e-14:
                continue
            psi = col / np.sqrt(p_i)
            # entanglement of pure 2-qubit state = h(Schmidt eigenvalue)
            M = psi.reshape(2, 2)
            _, s, _ = np.linalg.svd(M)
            probs = s ** 2
            probs = probs[probs > 1e-14]
            ent = -np.sum(probs * np.log2(probs))
            avg_E += p_i * ent
        if avg_E < best_avg_E:
            best_avg_E = avg_E
    return float(best_avg_E)


# --- Test suite ---
def run_all_tests(seed: int = 12345) -> dict:
    rng = default_rng(seed)
    results = {"seed": seed, "tests": []}

    # 1. Bell state Phi+: E should be 1
    rho = bell_phi_plus()
    C = concurrence(rho)
    E = entanglement_of_formation(rho)
    results["tests"].append({
        "name": "Bell state |Phi+>",
        "expected_E": 1.0, "expected_C": 1.0,
        "computed_E": E, "computed_C": C,
        "pass": abs(E - 1.0) < 1e-10 and abs(C - 1.0) < 1e-10
    })

    # 1b. Bell state Psi-: E should be 1
    rho = bell_psi_minus()
    C = concurrence(rho); E = entanglement_of_formation(rho)
    results["tests"].append({
        "name": "Bell state |Psi->",
        "expected_E": 1.0, "expected_C": 1.0,
        "computed_E": E, "computed_C": C,
        "pass": abs(E - 1.0) < 1e-10 and abs(C - 1.0) < 1e-10
    })

    # 2. Product state |00>: E=0, C=0
    rho = product_00()
    C = concurrence(rho); E = entanglement_of_formation(rho)
    results["tests"].append({
        "name": "Product state |00>",
        "expected_E": 0.0, "expected_C": 0.0,
        "computed_E": E, "computed_C": C,
        "pass": abs(E) < 1e-10 and abs(C) < 1e-10
    })

    # 3. Werner: sweep p in [0,1], check E=0 for p<=1/3, monotone above
    werner_data = []
    ps = np.linspace(0, 1, 41)
    for p in ps:
        rho = werner_state(p)
        C = concurrence(rho); E = entanglement_of_formation(rho)
        # Analytic concurrence for this state: C = max(0, (3p-1)/2)
        C_analytic = max(0.0, (3 * p - 1) / 2)
        werner_data.append({
            "p": float(p),
            "C": C, "E": E,
            "C_analytic": C_analytic,
            "C_matches_analytic": abs(C - C_analytic) < 1e-8
        })
    # separability threshold check
    below_thresh = [d for d in werner_data if d["p"] <= 1/3 + 1e-9]
    above_thresh = [d for d in werner_data if d["p"] > 1/3 + 1e-3]
    sep_ok = all(d["C"] < 1e-8 for d in below_thresh)
    # monotone above (E nondecreasing in p)
    mono_ok = all(above_thresh[i]["E"] <= above_thresh[i + 1]["E"] + 1e-10
                  for i in range(len(above_thresh) - 1))
    analytic_ok = all(d["C_matches_analytic"] for d in werner_data)
    results["werner_sweep"] = werner_data
    results["tests"].append({
        "name": "Werner separability p<=1/3 => C=0",
        "pass": sep_ok
    })
    results["tests"].append({
        "name": "Werner E monotone above threshold",
        "pass": mono_ok
    })
    results["tests"].append({
        "name": "Werner concurrence matches analytic C=max(0,(3p-1)/2)",
        "pass": analytic_ok
    })
    # explicit numerical value at p=1: E should be 1 (pure Bell)
    results["tests"].append({
        "name": "Werner p=1 => E=1",
        "expected_E": 1.0,
        "computed_E": werner_data[-1]["E"],
        "pass": abs(werner_data[-1]["E"] - 1.0) < 1e-10
    })

    # 4. Random 2-qubit density matrices: 1000 samples, verify 0<=C<=1, 0<=E<=1,
    # and that E is monotone-nondecreasing in C (sorted-order comparison).
    N = 1000
    Cs = np.zeros(N); Es = np.zeros(N)
    for i in range(N):
        rho = random_2qubit_mixed(rng)
        Cs[i] = concurrence(rho)
        Es[i] = entanglement_of_formation(rho)
    range_ok = bool(np.all((Cs >= -1e-12) & (Cs <= 1.0 + 1e-9)) and
                    np.all((Es >= -1e-12) & (Es <= 1.0 + 1e-9)))
    # Monotone check: sort by C, verify E is nondecreasing in sorted order
    order = np.argsort(Cs)
    E_sorted = Es[order]
    diffs = np.diff(E_sorted)
    # allow floating tolerance
    monotone_violations = int(np.sum(diffs < -1e-10))
    monotone_ok = monotone_violations == 0
    results["tests"].append({
        "name": "Random 1000 states: 0<=C<=1 and 0<=E<=1",
        "n": N, "pass": range_ok
    })
    results["tests"].append({
        "name": "Random 1000 states: E monotone in C",
        "n": N, "monotone_violations": monotone_violations,
        "max_neg_diff": float(diffs.min()) if len(diffs) else 0.0,
        "pass": monotone_ok
    })
    results["random_summary"] = {
        "N": N,
        "C_min": float(Cs.min()), "C_max": float(Cs.max()),
        "C_mean": float(Cs.mean()),
        "E_min": float(Es.min()), "E_max": float(Es.max()),
        "E_mean": float(Es.mean()),
        "n_separable_C_zero": int(np.sum(Cs < 1e-10)),
    }

    # 5. Bell-diagonal state: brute-force decomposition test.
    # rho = 0.7|Phi+><Phi+| + 0.3|Psi-><Psi-|
    rho_bd = 0.7 * bell_phi_plus() + 0.3 * bell_psi_minus()
    C_bd = concurrence(rho_bd); E_bd = entanglement_of_formation(rho_bd)
    # For Bell-diagonal state with eigenvalues (l1,l2,l3,l4) on Bell basis,
    # concurrence = max(0, 2*max(li) - 1). Here max=0.7 so C = 0.4.
    C_bd_analytic = max(0, 2 * 0.7 - 1)
    E_brute = brute_force_ef_upper_bound(rho_bd, rng, n_decomps=400, ensemble_size=4)
    # brute-force gives upper bound; should be >= Wootters value within numerical slack
    results["bell_diagonal"] = {
        "rho": "0.7|Phi+><Phi+| + 0.3|Psi-><Psi-|",
        "C_wootters": C_bd, "C_analytic": C_bd_analytic,
        "E_wootters": E_bd, "E_brute_upper_bound": E_brute,
        "brute_ge_wootters": E_brute + 1e-6 >= E_bd,
    }
    results["tests"].append({
        "name": "Bell-diagonal concurrence matches analytic",
        "pass": abs(C_bd - C_bd_analytic) < 1e-10
    })
    results["tests"].append({
        "name": "Bell-diagonal: brute-force E >= Wootters E (upper bound property)",
        "pass": E_brute + 1e-6 >= E_bd
    })

    # 6. Sanity: E and C consistent with each other via the formula
    # For every random state, recompute E from C and check equality.
    max_disc = 0.0
    for i in range(min(N, 200)):
        C = Cs[i]
        x = 0.5 * (1.0 + np.sqrt(max(0.0, 1.0 - C * C)))
        E_from_C = binary_entropy(x)
        max_disc = max(max_disc, abs(E_from_C - Es[i]))
    results["tests"].append({
        "name": "E computed from C via formula matches direct E",
        "max_discrepancy": max_disc,
        "pass": max_disc < 1e-12
    })

    # Overall verdict
    all_pass = all(t.get("pass", False) for t in results["tests"])
    results["overall_pass"] = all_pass
    results["n_tests"] = len(results["tests"])
    results["n_pass"] = sum(1 for t in results["tests"] if t.get("pass"))

    return results


if __name__ == "__main__":
    out = run_all_tests(seed=20260705)
    outpath = os.path.join(os.path.dirname(__file__), "results.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"Wrote {outpath}")
    print(f"Overall: {out['n_pass']}/{out['n_tests']} tests passed")
    for t in out["tests"]:
        mark = "PASS" if t.get("pass") else "FAIL"
        name = t["name"]
        extra = ""
        if "computed_E" in t and "expected_E" in t:
            extra = f"  expected_E={t['expected_E']:.6f} computed_E={t['computed_E']:.6f}"
        print(f"  [{mark}] {name}{extra}")
    print("\nWerner sweep summary (p, C, E):")
    for d in out["werner_sweep"][::5]:
        print(f"  p={d['p']:.3f}  C={d['C']:.6f}  E={d['E']:.6f}  C_analytic={d['C_analytic']:.6f}")
    print("\nRandom-state summary:", json.dumps(out["random_summary"], indent=2))
    print("Bell-diagonal:", json.dumps(out["bell_diagonal"], indent=2, default=float))
